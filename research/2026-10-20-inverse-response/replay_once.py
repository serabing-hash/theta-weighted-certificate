#!/usr/bin/env python3
"""Optional reader arithmetic replay; never invoked by package verification."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def save(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("shared", "rank-one"), required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--execute-once", action="store_true")
    args = parser.parse_args()
    need(args.execute_once, "explicit --execute-once required")
    need(sys.platform == "linux" and sys.version_info >= (3, 11),
         "Linux and CPython >=3.11 required")
    need(sys.flags.isolated and sys.flags.dont_write_bytecode and not sys.flags.optimize,
         "invoke python3 -I -B without optimization")
    package = Path(__file__).resolve().parent
    output = Path(args.output_root).absolute()
    need(not output.is_symlink() and output.parent.resolve() == output.parent,
         "canonical output parent required")
    need(not output.resolve().is_relative_to(package), "output must be outside package")
    need(not output.exists(), "output already exists; attempt consumed; no retry")
    # A permanent mark is created BEFORE admission or scientific work.
    output.mkdir(mode=0o700)
    save(output / "ATTEMPT_CONSUMED.json",
         {"kind": args.kind, "automatic_retry": False, "attempts": 1})
    record = {"status": "HOLD", "kind": args.kind, "automatic_retry": False,
              "historical_host_chain_recreated": False, "RH_PROOF": "NOT-OBTAINED"}
    child = None
    try:
        verify_result = subprocess.run(
            [sys.executable, "-I", "-B", str(package / "verify_package.py"), "--require-inputs"],
            capture_output=True, text=True, timeout=45, check=False)
        need(verify_result.returncode == 0, "package/dependency verification failed")
        record["package_verification"] = json.loads(verify_result.stdout)
        manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
        verifier = next(r for r in manifest["files"] if r["path"] == "verify_package.py")
        need(hashlib.sha256((package / "verify_package.py").read_bytes()).hexdigest()
             == verifier["sha256"], "verifier hash changed")
        cpu = min(os.sched_getaffinity(0))
        os.sched_setaffinity(0, {cpu})
        start = time.monotonic()
        def limits():
            os.sched_setaffinity(0, {cpu})
            resource.setrlimit(resource.RLIMIT_AS, (402653184, 402653184))
            resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
        environment = {k: v for k, v in os.environ.items()
                       if k not in ("PYTHONPATH", "LD_PRELOAD", "LD_LIBRARY_PATH")}
        environment.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                           MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1")
        with (output / "stdout.txt").open("x") as stdout, (output / "stderr.txt").open("x") as stderr:
            child = subprocess.Popen(
                [sys.executable, "-I", "-S", "-B", str(package / "code/public_worker.py"),
                 "--kind", args.kind, "--package-root", str(package),
                 "--output-dir", str(output / "math")],
                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                env=environment, start_new_session=True, preexec_fn=limits)
            peak = 0
            violation = None
            while True:
                pid, status, usage = os.wait4(child.pid, os.WNOHANG)
                if pid:
                    child.returncode = os.waitstatus_to_exitcode(status)
                    break
                if time.monotonic() - start >= 60:
                    violation = "60-second worker spawn-to-reap wall cap"
                try:
                    info = Path(f"/proc/{child.pid}/status").read_text()
                    values = {line.split(":")[0]: line.split(":")[1].strip()
                              for line in info.splitlines() if ":" in line}
                    rss = int(values.get("VmRSS", "0 kB").split()[0])
                    hwm = int(values.get("VmHWM", "0 kB").split()[0])
                    peak = max(peak, rss, hwm)
                    if peak > 327680:
                        violation = "320-MiB worker RSS cap"
                    if int(values.get("Threads", "1")) != 1:
                        violation = "one-thread cap"
                    children = Path(f"/proc/{child.pid}/task/{child.pid}/children").read_text().strip()
                    if children:
                        violation = "unexpected child process"
                except FileNotFoundError:
                    pass
                if violation:
                    os.killpg(child.pid, signal.SIGKILL)
                    _, status, usage = os.wait4(child.pid, 0)
                    child.returncode = os.waitstatus_to_exitcode(status)
                    break
                time.sleep(0.01)
        elapsed = time.monotonic() - start
        record.update(exit_code=child.returncode, wall_seconds=elapsed,
                      worker_cpu_seconds=usage.ru_utime + usage.ru_stime,
                      observed_worker_peak_kib=max(peak, usage.ru_maxrss),
                      cpu_affinity=[cpu], actual_wait4_completed=True)
        need(violation is None, violation or "resource violation")
        need(child.returncode == 0 and elapsed < 60 and
             usage.ru_utime + usage.ru_stime <= 60 and
             max(peak, usage.ru_maxrss) <= 327680, "exit/resource acceptance failed")
        result = json.loads((output / "math/PUBLIC_REPLAY_RESULT.json").read_text())
        need(result["status"] == "EXACT-MATHEMATICAL-REPORT-MATCH" and
             result["kind"] == args.kind, "mathematical field comparison not accepted")
        record.update(status="PUBLIC-ARITHMETIC-REPLAY-COMPLETE",
                      numerical_status=result["numerical_status"],
                      resource_acceptance=True, result=result)
        save(output / "REPLAY_COMPLETION.json", record)
        print(json.dumps(record, sort_keys=True))
        return 0
    except BaseException as error:
        if child is not None and child.returncode is None:
            try:
                os.killpg(child.pid, signal.SIGKILL)
                os.wait4(child.pid, 0)
            except (ProcessLookupError, ChildProcessError):
                pass
        record.update(status="HOLD", reason=str(error), resource_acceptance=False)
        save(output / "REPLAY_HOLD.json", record)
        print(json.dumps(record, sort_keys=True))
        return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"status": "HOLD", "reason": str(error), "automatic_retry": False}))
        raise SystemExit(2)
