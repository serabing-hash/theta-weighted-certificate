#!/usr/bin/env python3
"""Finite, source-free exact checks accompanying the scalar-allocation preprint.

This script reads no files and uses only the Python standard library. It does
not prove the analytic theorem or evaluate any theta, prime, integral, or
spectral data. All arithmetic below is integer or rational arithmetic.
"""
from fractions import Fraction as F
import json

checks = []
def check(name, condition, scope):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "passed": True, "scope": scope})

check("pnt_leading_decimal", F(939, 100) < 10,
      "The displayed 9.39 is strictly below 10.")
check("pnt_decay_decimal", F(8274, 10000) > F(4, 5),
      "The displayed 0.8274 is strictly above 4/5.")
check("pnt_polynomial_exponent", 0 < 2 * F(1515, 1000) < 4,
      "The exponent after y=sqrt(log x) lies between zero and four.")
check("pnt_weakening_integer_margin", 10 * (1 + 625) < 10000,
      "Finite arithmetic in the weakening to A=10^4.")
check("pnt_maximum_coefficient", F(10**4, 2**4) == 625,
      "Coefficient bound using e>2; not a numerical exponential evaluation.")
check("gamma_geometric_integral_coefficient", 2 * (8 + 1) == 18,
      "Arithmetic in the series-plus-integral bound for d_Gamma.")
check("gamma_constant_upper_sum", 2 + 1 + 2 + 3 == 8,
      "Sum of the elementary strict upper bounds for c_Gamma.")
check("phase_derivative_endpoint", F(4, 2) - 2 == 0,
      "Endpoint of L-2 >= L/2 for L>=4; the remaining slope is positive.")
check("phase_image_length", F(1, 2) * 8 == 4,
      "A block of length 8*pi/L has phase length at least 4*pi.")
check("phase_thickness_fraction", F(2, 3) / 8 == F(1, 12),
      "One negative-cosine arc yields the stated block fraction.")
check("interval_thickness_fraction", F(1, 2) * F(1, 12) == F(1, 24),
      "Complete blocks occupying half an interval yield ell/24.")
check("bulk_lower_coefficient", F(1, 2) * F(1, 2) * F(1, 24) == F(1, 96),
      "Coefficient of b^2*ell/[pi*(1+beta)] in the bulk bound.")
check("central_upper_coefficient", F(1, 2) * 6 * 2 == 6,
      "Coefficient of ||u||_1^2*sqrt(N)/(pi*L).")
check("central_lower_coefficient", F(1, 2) * F(1, 4) * F(1, 4) * 2 == F(1, 16),
      "Coefficient of A^2*sqrt(N)/(pi*L) for the bump a.")
check("forced_scalar_coefficient", F(1, 2) * F(1, 16) == F(1, 32),
      "Half the divergent lower bound remains after a bounded error.")
check("second_derivative_central_coefficient", F(1, 2) * 6 * F(2, 5) == F(6, 5),
      "Coefficient of A^2*sqrt(N)/(pi*L^5) for a second derivative.")
check("second_derivative_power_gap", 5 - 1 == 4,
      "Power difference after factoring sqrt(N)/L in the contradiction.")

# Sparse polynomial arithmetic. Monomials are sorted tuples of variable names.
def add(*polys):
    out = {}
    for p in polys:
        for monomial, coefficient in p.items():
            out[monomial] = out.get(monomial, F(0)) + coefficient
    return {m: c for m, c in out.items() if c}
def neg(poly):
    return {m: -c for m, c in poly.items()}
def mul(p, q):
    out = {}
    for m, c in p.items():
        for n, d in q.items():
            key = tuple(sorted(m + n))
            out[key] = out.get(key, F(0)) + c * d
    return {m: c for m, c in out.items() if c}
def v(name):
    return {(name,): F(1)}
def c(value):
    return {(): F(value)} if value else {}

P, C, O, H, theta, B = map(v, ("P", "C", "O", "H", "theta", "B"))
q = add(P, neg(C), neg(O), H)
S = add(mul(theta, B), neg(C))
residual = add(P, neg(mul(theta, B)), neg(O), H)
check("residual_is_full_form_minus_slack", residual == add(q, neg(S)),
      "Exact formal polynomial identity R=q-S.")
check("exact_refund_identity", O == add(P, neg(mul(theta, B)), H, S, neg(q)),
      "Exact formal polynomial identity for the outer negative observation.")

r, T, xi = map(v, ("r", "T", "xi"))
check("positive_observation_denominator", 
      add(mul(c(4), mul(add(c(1), r), add(c(1), r))), neg(add(c(1), mul(c(4), mul(r, r)))))
      == add(c(3), mul(c(8), r)),
      "Polynomial identity 4(1+r)^2-(1+4r^2)=3+8r; positivity for r>=0 is analytic context.")
check("positive_observation_remainder", 
      add(mul(c(2), add(c(1), T)), neg(add(c(1), r)), neg(add(c(1), T)))
      == add(T, neg(r)),
      "Cross-multiplied remainder in the positive bulk lower bound is T-r.")
check("stieltjes_endpoint_modulus", 
      add(c(F(-1, 2)**2), mul(xi, xi)) == add(c(F(1, 2)**2), mul(xi, xi)),
      "|q-1|^2=|q|^2 when q=1/2+i*xi, hence the endpoint quotient has modulus one.")

print(json.dumps({
    "artifact": "Scalar allocation obstruction exact checks",
    "arithmetic": "integer and rational only",
    "checks_passed": len(checks),
    "checks": checks,
    "scope": {
        "analytic_proof_certified": False,
        "theta_evaluation": False,
        "prime_enumeration": False,
        "pnt_numerical_verification": False,
        "quadrature": False,
        "spectral_numerics": False,
        "external_data": False,
        "network_access": False,
        "input_file_reads": False
    }
}, indent=2, sort_keys=True))
