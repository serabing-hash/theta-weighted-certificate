#!/usr/bin/env python3
"""Exact scalar identities in the low-to-sparse response proof.

This is not a theta matrix, Gram enclosure, packet-estimate verification,
prime/Gamma residual calculation, or positivity certificate.
It has no third-party dependencies and writes no files.
"""
from fractions import Fraction as Q
import json


def add(*polys):
    out = {}
    for poly in polys:
        for monomial, value in poly.items():
            out[monomial] = out.get(monomial, Q(0)) + value
    return {m: v for m, v in out.items() if v}


def scale(poly, value):
    return {m: value * v for m, v in poly.items() if value * v}


def multiply(left, right):
    out = {}
    for (z1, k1), a in left.items():
        for (z2, k2), b in right.items():
            key = (z1 + z2, k1 + k2)
            out[key] = out.get(key, Q(0)) + a * b
    return {m: v for m, v in out.items() if v}


checks = {}
P = [Q(6), Q(6), Q(3), Q(1)]  # ascending powers of t
derivative_minus_P = [
    (i + 1) * P[i + 1] - P[i] if i + 1 < len(P) else -P[i]
    for i in range(len(P))
]
checks["packing_antiderivative"] = derivative_minus_P == [0, 0, 0, -1]

lhs = {(2, 0): Q(1, 2), (1, 1): Q(-2)}
for retained, shift, loss, name in [
    (Q(0), Q(2), Q(2), "complete_square_cost_2"),
    (Q(1, 4), Q(4), Q(4), "retained_quarter_cost_4"),
]:
    linear = {(1, 0): Q(1), (0, 1): -shift}
    square = scale(multiply(linear, linear), Q(1, 2) - retained)
    rhs = add(square, {(2, 0): retained, (0, 2): -loss})
    checks[name] = rhs == lhs

# d/dU [log(U)^11/U^2] has the sign of 11 - 2 log(U).
checks["packing_F_decreases_for_logU_at_least_18"] = 11 - 2 * 18 < 0
# Squaring the t^6 estimate, dividing by energy t and density t^8:
checks["integrated_log_power"] = 2 * 6 - 1 - 8 == 3

if not all(checks.values()):
    raise AssertionError(checks)
print(json.dumps({
    "scope": "Five scalar identities only; not a numerical theta certificate.",
    "checks": checks,
    "checks_passed": len(checks),
}, indent=2, sort_keys=True))

