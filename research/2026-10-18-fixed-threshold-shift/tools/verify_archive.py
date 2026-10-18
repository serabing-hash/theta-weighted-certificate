#!/usr/bin/env python3
"""Read-only byte/binding verification. Never imports scientific code."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads(path.read_text())
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def check(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)

def main():
    public = load(ROOT / "PUBLIC_ALLOWLIST.json")
    listed = set(public["files"]) | {"PUBLIC_ALLOWLIST.json", "MANIFEST.sha256"}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
    check(actual == listed, "public file allowlist")
    for line in (ROOT / "MANIFEST.sha256").read_text().splitlines():
        expected, name = line.split("  ", 1)
        p = ROOT / name
        check(not p.is_symlink() and p.resolve().is_relative_to(ROOT), "safe file " + name)
        check(digest(p) == expected, "public hash " + name)
    manifest = ROOT / "inputs/INPUT_MANIFEST.json"
    check(digest(manifest) == "5bb28142e4bbc8fee7060467097db8b732fceb1564857b5dcca5ef3326b3fc58", "original input manifest")
    inputs = load(manifest)["inputs"]
    check(len(inputs) == 63, "63 input roles")
    for role, record in inputs.items():
        p = ROOT / "inputs/evidence" / record["path"]
        check(p.stat().st_size == record["size"] and digest(p) == record["sha256"], "input " + role)
    timed = ROOT / "evidence/timed"
    final = load(timed / "FINAL_ARTIFACT_MANIFEST.json")
    check(len(final["files"]) == 29, "29 timed artifacts")
    for record in final["files"]:
        p = timed / record["path"]
        check(p.stat().st_size == record["bytes"] and digest(p) == record["sha256"], "timed " + record["path"])
    report = load(timed / "math/INDEPENDENT_CHECK.json")
    check(len(report["output_hashes"]) == 16, "16 checker outputs")
    for name, expected in report["output_hashes"].items():
        check(digest(timed / "math" / name) == expected, "checker output " + name)
    check(digest(ROOT / "frozen/code/shift_checker.py") == report["checker_sha256"], "checker source")
    plan = ROOT / "frozen/LAUNCH_PLAN.json"
    check(digest(plan) == final["plan_sha256"] == "b4b1dccccd64259ca7d2c91f4675340c178a6f947320339709bba7bbe2cffb49", "plan")
    for name, expected in load(plan)["code_sha256"].items():
        check(digest(ROOT / "frozen/code" / name) == expected, "source " + name)
    values = load(ROOT / "EXACT_RESULT_VALUES.json")
    check(values["mu1"] == report["exact_check_values"]["mu372"], "verbatim mu1")
    for key in ["h", "delta1", "eta1", "previous_lower_edge", "new_lower_edge", "strict_improvement"]:
        check(values[key] == report[key], "verbatim " + key)
    host = load(ROOT / "evidence/host/EXTERNAL_TERMINAL_WITNESS.json")
    check(host["final_artifact_manifest_sha256"] == digest(timed / "FINAL_ARTIFACT_MANIFEST.json"), "host artifact binding")
    transcript = load(ROOT / "evidence/ACTUAL_HOST_TOOL_TRANSCRIPT.json")
    check(transcript["dispatch_count"] == 1, "one historical dispatch")
    print(json.dumps({"status":"BYTE-AND-BINDING-VERIFIED-NO-MATHEMATICAL-REPLAY",
                      "public_files":len(actual), "input_roles":63, "timed_artifacts":29,
                      "checker_output_hashes":16, "RH_PROOF":"NOT-OBTAINED"}))
if __name__ == "__main__":
    main()

