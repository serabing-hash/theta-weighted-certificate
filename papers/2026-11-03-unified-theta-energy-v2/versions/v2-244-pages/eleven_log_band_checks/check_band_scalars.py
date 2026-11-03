#!/usr/bin/env python3
"""Exact scalar checks for flexible-anchor and sparse-band inequalities.

Standard library only. Fractions certify scalar inequalities, not a theta
matrix, external theorem, PNT threshold, or formal proof. Decimal strings are
outward truncations of rational enclosures, not binary floating-point tests.
"""
from fractions import Fraction as F
from math import isqrt
import json


def atan_bounds(x, terms):
    assert F(0) < x < F(1) and terms > 0
    s = sum(((-1)**k * x**(2*k+1) / (2*k+1)
             for k in range(terms)), F(0))
    next_term = (-1)**terms * x**(2*terms+1) / (2*terms+1)
    return min(s, s+next_term), max(s, s+next_term)


def log_two_bounds(terms=48):
    x = F(1, 3)
    s = 2*sum((x**(2*k+1)/(2*k+1) for k in range(terms)), F(0))
    tail = 2*x**(2*terms+1)/((2*terms+1)*(1-x*x))
    return s, s+tail


def sqrt_bounds(x, digits=40):
    assert x >= 0
    scale = 10**digits
    q = isqrt(x.numerator*scale*scale//x.denominator)
    lower = F(q, scale)
    upper = lower if lower*lower == x else F(q+1, scale)
    assert lower*lower <= x <= upper*upper
    return lower, upper


def decimal_out(x, up=False, digits=18):
    scale = 10**digits
    n = x.numerator*scale
    q = -((-n)//x.denominator) if up else n//x.denominator
    sign = '-' if q < 0 else ''
    q = abs(q)
    return f'{sign}{q//scale}.{q%scale:0{digits}d}'


def interval_json(bounds):
    return {'lower': decimal_out(bounds[0]), 'upper': decimal_out(bounds[1], True)}


def run():
    checks = {}
    def test(name, truth):
        checks[name] = bool(truth)
        assert truth, name

    a5 = atan_bounds(F(1, 5), 32)
    a239 = atan_bounds(F(1, 239), 12)
    pi = (16*a5[0]-4*a239[1], 16*a5[1]-4*a239[0])
    log2 = log_two_bounds()
    test('Machin_pi_lower_157_over_50', pi[0] > F(157, 50))
    test('log2_upper_7_over_10', log2[1] < F(7, 10))
    theta, delta, c = F(99,100), F(1,100), F(11,20)
    ratio = (1/theta-delta)/(1-2*delta)
    test('anchor_ratio_9901_over_9702', ratio == F(9901,9702))
    test('anchor_ratio_excess_199_over_9702', ratio-1 == F(199,9702))
    slack = F(157,50)*c-F(17,10)-F(199,9702)
    test('anchor_exact_positive_slack', slack == F(31477,4851000) and slack > 0)
    test('prime_coefficient_rational_majorant', F(121,40)/F(157,50) == F(605,628))
    certificate = 628*9801-605*10000
    test('eleven_prime_margin_integer', certificate == 105028 and certificate > 0)
    test('eleven_prime_below_99_over_100_squared', F(605,628) < F(99,100)**2)
    test('HSW_one_eighth_charged', F(9367419,1000000)+F(1,8) < F(19,2))
    test('old_eight_rational_margin', 157*39601-155*40000 == 17357)
    test('near_row_coefficient', 2**11 * 4 * 2**12 == 2**25)
    test('near_row_power', 9-12+1 == -2)
    test('lower_far_derivative_on_log_ge_26', 1-F(25,2)/26 >= F(1,2))
    test('lower_far_power', F(19,2)-F(25,2) == -3)
    test('upper_far_integrable_log_power', F(19,2)-12 == -F(5,2))
    test('upper_far_integral_coefficient', 1/(F(5,2)-1) == F(2,3))
    test('upper_far_normalized_power', -F(3,2)-F(1,2) == -2)
    test('exponential_row_monotone_on_log_ge_26', 9-F(26) < 0)
    test('lower_far_exponential_monotone_on_log_ge_26', F(19,2)-26 < 0)
    test('adjacent_counterexample_two_by_two_minor', 1-F(3,4)**2 == F(7,16))
    test('adjacent_counterexample_three_by_three_determinant', 1-2*F(3,4)**2 == -F(1,8))
    test('adjacent_counterexample_negative_eigenvalue', F(3,4)**2*2 > 1)
    old_width = (2*pi[0]**2/(1+2*log2[1]), 2*pi[1]**2/(1+2*log2[0]))
    new_width = (2*pi[0]**2/(1+log2[1]), 2*pi[1]**2/(1+log2[0]))
    test('improved_width_exceeds_eleven', new_width[0] > 11)
    kappas = {}
    for A in (8,10,11):
        ratio_lo = A*(1+log2[0])/(2*pi[1]**2)
        ratio_hi = A*(1+log2[1])/(2*pi[0]**2)
        bounds = (1-sqrt_bounds(ratio_hi)[1], 1-sqrt_bounds(ratio_lo)[0])
        kappas[str(A)] = interval_json(bounds)
        if A == 10:
            test('two_five_log_pieces_margin_above_7_over_100', bounds[0] > F(7,100))
        if A == 11:
            test('eleven_asymptotic_margin_above_1_over_100', bounds[0] > F(1,100))
    result = {
        'status': 'PASS', 'checks_passed': len(checks), 'checks': checks,
        'exact_anchor_slack': str(slack), 'eleven_prime_margin_integer': certificate,
        'old_width_interval': interval_json(old_width),
        'improved_width_interval': interval_json(new_width),
        'improved_kappa_intervals': kappas,
        'scope': 'Exact scalar arithmetic only; analytic arguments are separately audited.',
        'actual_theta_matrix_computed': False,
        'effective_final_threshold_computed': False,
        'formal_proof_verified': False,
        'RH_proof': False,
    }
    return result


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
