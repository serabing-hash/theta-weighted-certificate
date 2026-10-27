#!/usr/bin/env python3
"""Source-free finite arithmetic checks for the collective central-band note.

Uses integer arithmetic and fractions only. It does not import research source
files, sample the theta kernel, enumerate primes, evaluate PNT errors, perform
quadrature, execute a spectral calculation, or certify the analytic proof.
Prints deterministic JSON to stdout. No network or third-party package is used.
"""
from fractions import Fraction as F
import json

checks = []
def check(name, condition, detail):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "passed": True, "detail": detail})

# Rational consequences of elementary bounds proved or stated in the text.
factorial = 1
exp3_lower = F(1)
for k in range(1, 9):
    factorial *= k
    exp3_lower += F(3**k, factorial)
check("exponential_series_lower_bound", exp3_lower > 20,
      "sum_{k=0}^8 3^k/k! = " + str(exp3_lower) + " > 20; no source evaluation")
ratio_upper = F(16, 20**3)
check("complete_theta_geometric_ratio", ratio_upper == F(1, 500),
      "16/20^3 = 1/500, using e^pi > e^3 > 20")
k_upper = 4 * F(22, 7)**2 / (1-ratio_upper)
check("theta_envelope_constant", k_upper == F(968000, 24451) and k_upper < 40,
      "4(22/7)^2/(1-1/500) = " + str(k_upper) + " < 40")
check("gamma_coefficient", 2*(8+1) == 18,
      "2 times the decreasing-sum bound 8+1 is 18")
check("mass_factor", F(1, 2)**2 == F(1, 4),
      "(2 cosh(x/2))^{-2} <= 1/4 in the normalized mass")
check("PNT_exponent_weakening", F(8274, 10000) > F(4, 5),
      "0.8274 > 4/5, an exact decimal comparison")
check("PNT_polynomial_degree", 2*F(1515, 1000) == F(303, 100) < 4,
      "2*1.515 = 3.03 < 4")
check("PNT_discarded_factor", 10*(1+625) < 10**4,
      "10(1+625) = 6260 < 10000")
check("prime_decay_exponent", F(2, 25) > F(1, 16),
      "(sqrt(2)/5)^2 = 2/25 > (1/4)^2")
check("prime_threshold_prefactor", 192*10**4 < 2**21,
      "1920000 < 2097152")
check("prime_threshold_exponent", 21+120-256 == -115 < 0,
      "2^(21+120-256) = 2^(-115) < 1")
check("prime_threshold_monotonicity", F(12, 2**10) < F(1, 4),
      "12/y - 1/4 is negative at and beyond y=2^10")
check("gamma_threshold_exponent", 66-2**19 < 0,
      "2^(66-2^19) < 1")
check("gamma_threshold_monotonicity", F(3, 2**20) < F(1, 2),
      "3/L - 1/2 is negative at and beyond L=2^20")
check("sampling_radius", F(320, 2**20) < F(1, 4),
      "4*pi*log(L)/L < 320/2^20 < 1/4 at the threshold")
check("sampling_absorption", 1-8*F(1, 4)**2 == F(1, 2),
      "1-8(ar)^2 >= 1/2 when ar <= 1/4")
check("sampling_constant", 4/F(1, 12) == 48,
      "H = 4/gamma = 48")
check("two_split_coefficient", 4*192 == 768,
      "The two quadratic splits multiply the central coefficient by four")
check("log_radius_coefficient", F(768*48, 2) == 18432,
      "768*48*(log L)/2 = 18432 log L")
check("theta_threshold_coefficient", F(18432*20, 2**20) == F(45, 128),
      "theta(2^20) = (45/128) log(2)/pi")
check("theta_threshold_margin", F(45, 128)/3 == F(15, 128) < F(1, 2),
      "log(2)<1 and pi>3 imply theta < 15/128 < 1/2")
check("window_error_coefficient", 2*3*16*48 == 4608,
      "2*e_v coefficient after inserting the two-sided window tail")
check("fixed_radius_coefficient", F(768*48, 73728) == F(1, 2),
      "r=(pi/73728)L gives theta(r)=1/2")
check("fixed_radius_sampling", F(22, 7)**2/9216 < F(1, 4),
      "pi^2/9216 < (22/7)^2/9216 < 1/4")
check("fixed_radius_minimum", F(128*3, 9) > 1,
      "r >= 128*pi/9 > 1 at L=2^20")
check("fixed_vector_observation_constant", F(1, 2)*F(1, 3)*F(1, 4)*F(1, 4) == F(1, 96),
      "Fourier factor, interval length, multiplier lower bound, and |U|^2 lower bound")
check("fixed_vector_divergence_constant", 18432/F(96) == 192,
      "theta times the lower observation coefficient is 192/pi")

# Finite coefficient identities, not testing the identities at sampled points.
def mul(p, q):
    out = [0]*(len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return out

def sub(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0)-(q[i] if i < len(q) else 0) for i in range(n)]

check("weighted_window_polynomial", mul([-2, 1], [1, 1]) == [-2, -1, 1],
      "t^2-t-2 = (t-2)(t+1), nonnegative for t>=2")
factorial_difference = sub([12*x for x in mul([1, 1], [1, 1])], mul([3, 2], [2, 2]))
check("Gevrey_factorial_induction", factorial_difference == [6, 14, 8],
      "12(k+1)^2-(2k+3)(2k+2) = 8k^2+14k+6 >= 0 for k>=0")
check("Gevrey_factorial_base", 1 == 12**0,
      "(2k+1)! <= 12^k(k!)^2 has equality at k=0")

print(json.dumps({
    "scope": "Finite integer, rational and coefficient checks only; not an analytic proof certificate",
    "source_evaluation": False,
    "checks_passed": len(checks),
    "checks": checks,
}, indent=2, sort_keys=True))
