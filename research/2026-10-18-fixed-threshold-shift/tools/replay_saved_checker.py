#!/usr/bin/env python3
"""Optional reader replay adapter. Not executed during paper preparation.

No producer, native arithmetic, coefficient solve or factor production is used.
The unchanged checker verifies saved full matrices. This is a NEW reader
arithmetic replay, not the historical full-run resource certificate.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
def load(p):
    return json.loads(p.read_text())
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok, text):
    if not ok:
        raise RuntimeError(text)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    started = time.monotonic()
    require(sys.platform.startswith("linux") and os.getuid() != 0, "isolated non-root Linux required")
    require(sys.version_info[:3] == (3, 12, 14), "documented CPython 3.12.14 required")
    require(not args.output.exists(), "fresh output path required")
    require(not args.output.resolve().is_relative_to(ROOT), "output must be outside immutable artifact tree")
    code = ROOT / "frozen/code/shift_checker.py"
    require(digest(code) == "e6ba2e463ea098276a99ea03175051ff2b9b5cbce09b2e602edf1387bc5b2a2f", "original checker hash")
    manifest = ROOT / "inputs/INPUT_MANIFEST.json"
    require(digest(manifest) == "5bb28142e4bbc8fee7060467097db8b732fceb1564857b5dcca5ef3326b3fc58", "original input manifest")
    bound_root = Path(load(manifest)["source_root"])
    require(bound_root.is_dir() and bound_root.resolve() == bound_root, "bind-mount inputs at the original absolute root")
    caps = dict(line.split(":", 1) for line in Path("/proc/self/status").read_text().splitlines() if ":" in line)
    require(all(int(caps[k].strip(), 16) == 0 for k in ["CapEff","CapPrm","CapInh","CapAmb"]), "zero active/permitted capabilities required")
    cpu = min(os.sched_getaffinity(0))
    os.sched_setaffinity(0, {cpu})
    resource.setrlimit(resource.RLIMIT_AS, (402653184, 402653184))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
    def alarm(_signum, _frame):
        raise TimeoutError("reader replay 60-second wall limit")
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, max(0.001, 60 - (time.monotonic() - started)))
    def guard():
        require(time.monotonic() - started < 60, "reader replay wall limit")
        require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= 327680, "reader RSS limit")
        require(os.sched_getaffinity(0) == {cpu}, "reader CPU affinity")
    saved = ROOT / "evidence/timed/math"
    archived = load(saved / "INDEPENDENT_CHECK.json")
    args.output.mkdir(parents=True, exist_ok=False)
    math = args.output / "math"
    math.mkdir()
    for name, expected in archived["output_hashes"].items():
        guard()
        require(digest(saved / name) == expected, "saved output hash " + name)
        shutil.copyfile(saved / name, math / name)
    single = load(saved / "SINGLE_USE.json")
    for env, key in [("SHIFT_LAUNCH_ID","launch_id"),("SHIFT_EPOCH_NS","epoch_ns"),
                     ("SHIFT_PLAN_SHA256","plan_sha256"),("SHIFT_INPUT_SHA256","input_manifest_sha256")]:
        os.environ[env] = str(single[key])
    spec = importlib.util.spec_from_file_location("reader_frozen_checker", code)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.run(bound_root, manifest, math, guard)
    guard()
    # A historical-context field is literal in the original checker source.
    # Preserve its raw emitted report and explicitly disambiguate this replay.
    context = {
        "status":"READER-SAVED-ARITHMETIC-REPLAY-COMPLETE",
        "historical_full_run_reproduced":False,
        "native_arithmetic_imported_by_adapter":False,
        "raw_checker_report_sha256":digest(math / "INDEPENDENT_CHECK.json"),
        "raw_report_context_correction":{
            "same_worker_native_runtime_remains_mapped":
            "Historical literal in unchanged checker; not an assertion about this standard-library-only replay."
        },
        "local_elapsed_seconds":time.monotonic()-started,
        "recorded_exact_mu1":report["exact_check_values"]["mu372"],
        "inherited_premises":"A1-A4/N1-N4 unchanged",
        "RH_PROOF":"NOT-OBTAINED"
    }
    (args.output / "REPLAY_CONTEXT.json").write_text(json.dumps(context, indent=2)+"\n")
    signal.setitimer(signal.ITIMER_REAL, 0)
    print(json.dumps(context))
if __name__ == "__main__":
    main()

