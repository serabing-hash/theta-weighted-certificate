#!/usr/bin/env python3
"""Two exact polynomial checks, not a verifier of the analytic theorems."""
import json

NVAR = 7
ZERO = (0,) * NVAR


def const(value):
    return {} if value == 0 else {ZERO: value}


def var(index):
    power = list(ZERO)
    power[index] = 1
    return {tuple(power): 1}


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for power, coefficient in polynomial.items():
            result[power] = result.get(power, 0) + coefficient
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def neg(polynomial):
    return {power: -coefficient for power, coefficient in polynomial.items()}


def sub(left, right):
    return add(left, neg(right))


def mul(*polynomials):
    result = const(1)
    for polynomial in polynomials:
        next_result = {}
        for left_power, left_coefficient in result.items():
            for right_power, right_coefficient in polynomial.items():
                power = tuple(a + b for a, b in zip(left_power, right_power))
                next_result[power] = next_result.get(power, 0) + left_coefficient * right_coefficient
        result = {power: coefficient for power, coefficient in next_result.items() if coefficient}
    return result


def square(polynomial):
    return mul(polynomial, polynomial)


a, b, ur, ui, vr, vi, alpha = (var(index) for index in range(NVAR))
abs_u2 = add(square(ur), square(ui))
abs_v2 = add(square(vr), square(vi))
abs_au_bv2 = add(square(sub(mul(a, ur), mul(b, vr))), square(sub(mul(a, ui), mul(b, vi))))
abs_u_v2 = add(square(sub(ur, vr)), square(sub(ui, vi)))
edge_remainder = sub(
    sub(abs_au_bv2, mul(sub(a, b), sub(mul(a, abs_u2), mul(b, abs_v2)))),
    mul(a, b, abs_u_v2),
)

# Multiply Young's difference by alpha to avoid any division or square roots.
alpha_plus_one = add(alpha, const(1))
young_left = sub(
    add(mul(alpha, alpha_plus_one, square(sub(ur, vr))), mul(alpha_plus_one, square(vr))),
    mul(alpha, square(ur)),
)
young_right = square(sub(mul(alpha, ur), mul(alpha_plus_one, vr)))
young_remainder = sub(young_left, young_right)

assert not edge_remainder
assert not young_remainder

print(json.dumps({
    "complex_edge_polynomial_remainder_terms": len(edge_remainder),
    "young_polynomial_remainder_terms": len(young_remainder),
    "arithmetic": "exact integer coefficients",
    "analytic_theorem_verification": "NOT_PERFORMED_BY_THIS_SCRIPT",
    "numerical_theta_or_zero_evaluations": 0,
    "RH_PROOF": "NOT-OBTAINED"
}, indent=2))
