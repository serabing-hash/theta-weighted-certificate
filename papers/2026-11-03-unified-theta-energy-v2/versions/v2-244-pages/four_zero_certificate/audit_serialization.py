#!/usr/bin/env python3
"""Replay the producer and verify live-ball serialization and every rational box.

This is a serialization/reproduction check, not an independent quadrature engine.
It regenerates the producer outputs beside certify_four_zeros.py.
"""
from pathlib import Path
from fractions import Fraction
import json, re, runpy, sys
from flint import arb, acb, ctx
import flint

base = Path(__file__).resolve().parent
g = runpy.run_path(str(base / "certify_four_zeros.py"), run_name="__main__")
live = g["M"]
data = json.loads((base / "CERTIFICATE.json").read_text())
ctx.prec = 256
runpy.run_path(str(base / "export_rational_matrix.py"), run_name="__main__")
runpy.run_path(str(base / "check_rational_matrix.py"), run_name="__main__")
ledger = json.loads((base / "RATIONAL_MATRIX.json").read_text())
D = int(ledger["scale"])
entries = []
for i in range(4):
    for j in range(4):
        parsed = arb(data["certifying_matrix"][i][j])
        lo, hi = map(int, ledger["entries"][i][j])
        roundtrip = parsed.contains(live[i,j])
        lower_ok = arb(lo) / D <= live[i,j].lower()
        upper_ok = arb(hi) / D >= live[i,j].upper()
        parsed_lower_ok = arb(lo) / D <= parsed.lower()
        parsed_upper_ok = arb(hi) / D >= parsed.upper()
        assert all((roundtrip,lower_ok,upper_ok,parsed_lower_ok,parsed_upper_ok)), (i,j)
        entries.append({"row":i,"column":j,"parsed_contains_live":bool(roundtrip),
                        "rational_box_contains_live":bool(lower_ok and upper_ok),
                        "rational_box_contains_parsed":bool(parsed_lower_ok and parsed_upper_ok)})
roots = []
for i,z in enumerate(acb.zeta_zeros(1,4)):
    supplied = arb(re.search(r"(\[.*?\])j", data["zeros"][i]).group(1))
    inside = supplied.contains(z.imag)
    residual = z.zeta().contains(0)
    assert inside and residual and z.real == arb(1)/2
    roots.append({"index":i+1,"supplied_contains_256_bit_root":bool(inside),
                  "zeta_residual_contains_zero":bool(residual)})
# Rational coefficient majorants for tau>=pi>3.
d1 = 8+Fraction(28,3)+Fraction(12,9)+Fraction(1,3)
d2 = 16+Fraction(104,3)+Fraction(136,9)+Fraction(24,27)+Fraction(1,2)*(
     Fraction(8,3)+Fraction(28,9)+Fraction(12,27))+Fraction(1,9)
assert d1 < 22 and d2 < 80
out = {"status":"PASS","python_flint":flint.__version__,
       "flint_version":flint.__FLINT_VERSION__,"producer_bits":g["data"]["precision_bits"],
       "export_check_bits":ctx.prec,"entry_checks":entries,"root_consistency_checks":roots,
       "derivative_majorants":{"first":str(d1),"second":str(d2)},
       "scope":"All 16 live sufficient-matrix balls survive string serialization and outward rational export. Root residual checks supplement, not replace, FLINT zero isolation/counting."}
(base / "SERIALIZATION_CHECK.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS: all 16 live balls enclosed after serialization and rational export.")

