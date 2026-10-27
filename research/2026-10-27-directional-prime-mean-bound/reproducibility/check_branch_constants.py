"""Exact branch scalar checks; no theta, source or prime evaluator."""
from fractions import Fraction as F
from math import factorial
import json

checks = {}

def record(name, left, right, relation="<"):
    left, right = F(left), F(right)
    passed = left < right if relation == "<" else left == right
    checks[name] = {"left": str(left), "relation": relation,
                    "right": str(right), "pass": passed}
    assert passed, (name, left, relation, right)

def taylor(x, degree):
    x = F(x)
    return sum((x ** j / factorial(j) for j in range(degree + 1)), F())

record("exp3_lower_partial", 20, taylor(3, 8))
record("exp1_lower_partial", F(8, 3), taylor(1, 4))
record("exp_half_partial_identity", taylor(F(1, 2), 3), F(79, 48), "=")
record("exp_three_quarter_partial_identity", taylor(F(3, 4), 3), F(269, 128), "=")
record("exp29over16_lower_partial", 6, taylor(F(29, 16), 6))
record("exp1_upper_geometric", F(65, 24) + F(1, 100), 3)
record("fourthroot2", 2, F(6, 5) ** 4)
record("fourthroot3", 3, F(4, 3) ** 4)
record("threequarter_power2", 8, F(27, 16) ** 4)
record("sqrt2_lower", F(140, 99) ** 2, 2)
record("sqrt2_upper", 2, F(99, 70) ** 2)
record("kappa1_derivative_negative_threshold", F(5, 4) / F(16, 5) + 1 / (F(16, 5) - F(3, 2)), 1)
record("kappa1_fourthroot_factor", F(128, 125), F(101, 100) ** 4)
theta_tail = F(16, 8000) / F(13, 25) / (1 - F(81, 16 * 20 ** 5))
record("relative_theta_tail", theta_tail, F(1, 250))
global_kappa = F(251, 250) * 4 * F(101, 100) * F(16, 5) * F(17, 10) * F(2, 45)
record("global_kappa_prefactor", global_kappa, 1)
record("right_ratio_prefactor", F(500, 499) * F(25, 22), F(8, 7))
record("left_ratio_prefactor", F(500, 499) * F(25, 19), F(4, 3))
record("right_ratio_geometric", F(4, 3) ** 5 / 20 ** 7, F(1, 2))
record("right_relative_label_tail", F(1, 14) * 2 * 3 ** 5 / 20 ** 5, F(1, 1000))
rzero = (F(1001, 1000) * F(99, 200) * F(251, 250) * F(99, 70)
         * (64 * F(22, 7) ** 2 - 24 * F(25, 8))
         / (20 ** 4 * F(79, 48)))
record("Rzero", rzero, F(3, 2000))
ra = F(1001, 1000) * 2160 / (20 ** 8 * F(8, 3))
record("Ra", ra, F(1, 30000000))
record("right_main_label_ratio", F(4, 3) ** 6 / 500, F(3, 250))
first = F(7, 10) * F(96, 5) / (20 ** 4 * F(79, 48))
other = F(162) / (20 ** 6 * F(269, 128)) * F(250, 247)
main_bound = 1680 * F(400, 399) * (first + other)
record("right_main_exact_identity", main_bound, F(1097188704, 12466367875), "=")
record("right_main_squared", main_bound, F(9, 100))
record("right_rest_ratio", F(4, 3) ** 3 / 20 ** 3, F(1, 1000))
right_rest = F(3, 35) * F(27, 2400) * F(1000, 999)
record("right_rest_exact_identity", right_rest, F(1, 1036), "=")
record("right_rest_norm", right_rest, F(1, 1000))
record("left_low_main_squared", F(5, 4) * F(7, 10) * F(6, 5) * F(3, 2000), F(1, 625))
record("left_low_coupled_prefactor", 5 * F(1001, 1000) * F(4, 3) * 40 * F(6, 5), 18 ** 2)
left_rest = F(243) / (20 ** 4 * F(79, 48)) / (1 - F(64, 13500))
record("left_rest_exact_identity", left_rest, F(19683, 21228880), "=")
record("left_rest_norm", left_rest, F(1, 1000))
high = F(15, 2) * F(896, 5) * F(1, 30000000)
record("left_high_exact_identity", high, F(7, 156250), "=")
record("left_high_squared", high, F(49, 1000000))
record("five_piece_sum", F(3, 10) + F(1, 1000) + F(1, 25) + F(1, 1000) + F(7, 1000), F(349, 1000), "=")
full = (F(349, 1000) + F(1, 10 ** 48)) ** 2 + F(9, 10 ** 18)
record("full_main_coefficient", full, F(49, 400))
record("main_absorption_margin", F(49, 400), F(1, 8))

# Independent exact checks for the analytic core-mass entry dependency.
record("theta_boundary_first", F(6, 5) * F(475, 4) / (400 * taylor(F(1, 4), 3)), F(684, 2465), "=")
record("theta_boundary_tail", F(49152, 5 * 20 ** 8), F(1, 1000000))
record("theta_boundary_margin", F(1, 1000000), F(5, 18) - F(684, 2465))
record("core_mass_exterior_integral", F(5, 9) * (F(6, 5) / F(13, 2) + 1 / F(15, 2)), F(62, 351), "=")
record("core_cosh_squared", F(577, 560), F(41, 40) ** 2)
record("core_mass_lower", F(2, 5), F(5780, 14391))

# Safe corollary: disjoint low/high left-output supports.
record("orthogonal_left_pieces", F(41, 1000) ** 2 + F(7, 1000) ** 2, F(42, 1000) ** 2)
record("corollary_core_sum", F(301, 1000) + F(42, 1000), F(343, 1000), "=")
sharper_full = (F(343, 1000) + F(1, 10 ** 48)) ** 2 + F(9, 10 ** 18)
record("corollary_full_coefficient", sharper_full, F(3, 25))
record("corollary_absorption_margin", F(3, 25), F(1, 8))

print(json.dumps({
    "scope": "Exact rational scalar comparisons only; not an analytic proof verifier",
    "all_passed": all(c["pass"] for c in checks.values()),
    "check_count": len(checks),
    "checks": checks,
}, indent=2))
