#!/usr/bin/env python3
"""Audit this frozen evidence package, without source evaluation or RH claims.

Default operation checks SHA256 bytes only. --verify-budget additionally
replays exact rational identities in the two saved evidence JSON files.
This program does not import the historical whole-R implementation.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_hashes(root):
    seen = set()
    for line in (root / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        require(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected),
                "invalid digest")
        rel = Path(relative)
        require(not rel.is_absolute() and ".." not in rel.parts and relative not in seen,
                "invalid or duplicate manifest path")
        seen.add(relative)
        target = root / rel
        require(target.resolve().is_relative_to(root.resolve()) and target.is_file(),
                "manifest path outside package or missing")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        require(actual == expected, "SHA256 mismatch: " + relative)
    actual_files = {p.relative_to(root).as_posix() for p in root.rglob("*")
                    if p.is_file() and p.name != "MANIFEST.sha256"
                    and "__pycache__" not in p.parts}
    require(seen == actual_files, "manifest and package file list differ")
    return len(seen)


def check_budget(root, response_factor):
    saved = json.loads((root / "evidence/SAVED_ERROR_DECOMPOSITION.json").read_text())
    budget = json.loads((root / "evidence/R_SIGN_SEPARATION_BUDGET.json").read_text())
    q = Fraction
    lo, hi = map(q, saved["R"])
    midpoint = q(saved["R_midpoint_exact"])
    radius = q(saved["R_radius_exact"])
    require(lo <= hi and midpoint == (lo + hi) / 2 and radius == (hi - lo) / 2,
            "saved interval midpoint/radius identity fails")
    parts = {k: q(v) for k, v in saved["radius_parts_exact"].items()}
    require(all(v >= 0 for v in parts.values()), "negative saved radius component")
    require(sum(parts.values(), q(0)) == radius, "radius component sum fails")
    response = parts["response_enlargement"]
    nonresponse = sum((v for k, v in parts.items() if k != "response_enlargement"), q(0))
    require(q(budget["center_exact"]) == midpoint and q(budget["radius_exact"]) == radius,
            "cross-file center/radius mismatch")
    require(q(budget["response_radius_exact"]) == response,
            "cross-file response component mismatch")
    require(q(budget["nonresponse_radius_exact"]) == nonresponse,
            "cross-file nonresponse component mismatch")
    require(midpoint != 0, "ratio design condition requires nonzero midpoint")
    center_abs = abs(midpoint)
    require(q(budget["required_total_improvement_strictly_greater_than_exact"])
            == radius / center_abs, "total-improvement ratio mismatch")
    require(q(budget["nonresponse_over_center_exact"]) == nonresponse / center_abs,
            "nonresponse-to-midpoint ratio mismatch")
    require(q(budget["response_allowance_if_other_fixed_exact"]) == center_abs - nonresponse,
            "response allowance mismatch")
    minimum_factor = budget["minimum_sufficient_integer_factor_fixed_center"]
    require(isinstance(minimum_factor, int) and minimum_factor > 1,
            "invalid sufficient integer factor")
    require(radius / minimum_factor < center_abs
            and radius / (minimum_factor - 1) >= center_abs,
            "minimum sufficient integer factor mismatch")
    require(saved["contains_zero"] == (lo <= 0 <= hi)
            and budget["same_reported_R_contains_zero"] == saved["contains_zero"],
            "saved zero-containment mismatch")
    require(saved["numeric_count"] == budget["same_numeric_count"] == 11,
            "historical snapshot count mismatch")
    require(saved["new_source_evaluations"] == budget["new_source_evaluations"] == 0,
            "unexpected snapshot source-evaluation count")
    response_only_suffices = nonresponse < center_abs
    require(budget["response_only_reduction_can_decide_fixed_center"] == response_only_suffices,
            "response-only decision flag mismatch")
    require(nonresponse > center_abs,
            "package's strict fixed-center nonresponse inequality fails")
    if response_factor == "all":
        remaining_response = q(0)
        factor_description = "all saved response attribution removed"
    else:
        factor = q(response_factor)
        require(factor >= 1, "response factor must be at least 1")
        remaining_response = response / factor
        factor_description = str(factor)
    fixed_radius = nonresponse + remaining_response
    fixed_lo, fixed_hi = midpoint - fixed_radius, midpoint + fixed_radius
    return {
        "audit_status": "PASS_SAVED_EXACT_RATIONAL_IDENTITIES",
        "scope": "frozen center and frozen nonresponse attribution only",
        "historical_numeric_count": saved["numeric_count"],
        "source_evaluations_by_this_verifier": 0,
        "nonresponse_strictly_exceeds_abs_saved_midpoint": True,
        "response_factor": factor_description,
        "fixed_center_radius_exact": str(fixed_radius),
        "fixed_center_interval_exact": [str(fixed_lo), str(fixed_hi)],
        "fixed_center_interval_contains_zero": fixed_lo <= 0 <= fixed_hi,
        "scientific_status": "HOLD_NO_ACTUAL_SIGN_CERTIFICATION",
        "RH_proof": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-budget", action="store_true",
                        help="also replay the saved exact rational budget identities")
    parser.add_argument("--response-factor", default="all",
                        help="with --verify-budget: all (default) or rational factor >= 1")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    file_count = check_hashes(root)
    result = {"hash_status": "PASS", "manifest_payload_files": file_count}
    if args.verify_budget:
        result.update(check_budget(root, args.response_factor))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
