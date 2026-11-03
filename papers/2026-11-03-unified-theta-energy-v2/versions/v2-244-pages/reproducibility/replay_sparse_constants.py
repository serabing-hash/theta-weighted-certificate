#!/usr/bin/env python3
"""Rational constants in the sparse-window analytic branch; no source production.

Adapted from the independent consolidated-proof arithmetic checks. This verifies
only the listed finite rational inequalities, not the analytic proof or PNT.
"""
from fractions import Fraction as F
import json
if not __debug__: raise SystemExit('Run without Python -O.')
checks = {}
def ck(name, value):
    checks[name] = bool(value)
    assert value, name

# New optimized-anchor arithmetic; exact rationals only.
theta, c = F(39,40), F(31,40)
slack = F(157,50)*c-(1+2*F(7,10)+F(1,39))
ck('anchor_slack', slack == F(613,78000) > 0)
ck('d0', slack/c == F(613,60450))
ck('gamma0', slack/(2*c) == F(613,120900))
ck('Dtheta', (11-7*theta)/2 == F(167,80))
ck('slow_power', theta-1 == -F(1,40))
ck('H0_prefactor', 8*F(42,9)**2 == F(1568,9))
ck('two_pi_upper', 2*F(22,7) == F(44,7))
ck('theta_range', 0 < theta < 1)
ck('eight_band_radicand', c*8/2 == F(31,10))
ck('pi_lower_reduction', F(31,10)/F(157,50) == F(155,157))
ck('margin_square_comparison', F(155,157) < F(199,200)**2)
ck('margin_integer_certificate', 157*39601-155*40000 == 17357 > 0)
ck('one_two_hundred_margin', 1-F(199,200) == F(1,200) > F(1,1000))
ck('fixed_epsilon_coefficient', F(1001,1000)*F(199,200) == F(199199,200000) < F(997,1000))
ck('fixed_epsilon_slack', 1-F(199199,200000) > F(3,1000))
ck('full_head_leakage_constant', 2*(1+1) == 4)
ck('two_tail_substitution_factor', 2*F(1,2) == 1)

# Retained finite constants remain unaltered and algebraically valid.
ck('finite_mass_absorption', F(17,40)+F(31,40)+F(77,160)+F(11,7)-6 == -F(3077,1120))
ck('finite_weighted_absorption', F(7,40)+F(31,40)+F(21,160)+F(11,7)-3 == -F(389,1120))
ck('finite_prime_head', 12**2*8 < 34**2)
ck('finite_prime_tail', F(4,2**16) < 1)
ck('old_Gamma_37', 1+16*F(3,2)**2 == 37)
ck('old_delta_prime_quarter', 35**2*2*F(1,39200) == F(1,16))
ck('old_eta_conversion', 200*F(1,7840000) == F(1,39200))
ck('old_half_margin', F(7,8)-F(1,4)-F(1,8) == F(1,2))
ck('old_sparse_near_constant', 128*4*2**8 == 2**17)
ck('HSW_shift', F('9.367419')+F(1,8) == F('9.492419') < F('9.5'))


print(json.dumps({'status':'PASS','checks':checks,
'scope':'Exact rational constant checks only; analytic hypotheses and cited external theorems are not established by this script.'},indent=2,sort_keys=True))
