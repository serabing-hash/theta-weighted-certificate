#!/usr/bin/env python3
"""Exact rational checks for the displayed scalar bounds, not an analytic audit.
No theta/prime evaluation, numerical integration, or spectrum is computed.
"""
from fractions import Fraction as F
from math import factorial
import json

def exp_lower(x, n):
    return sum((x**j / factorial(j) for j in range(n+1)), F(0))

def record(name, lhs, relation, rhs):
    assert {'<': lhs < rhs, '>': lhs > rhs, '=': lhs == rhs}[relation], name
    return {'name': name, 'lhs': str(lhs), 'relation': relation, 'rhs': str(rhs)}

checks = []
checks += [record('pi alternating lower rational', 4*sum((F((-1)**k,2*k+1) for k in range(8)),F(0)), '>', F(3))]
checks += [record('exp3 positive Taylor lower', exp_lower(F(3),4), '>', F(16))]
checks += [record('theta envelope coefficient', 4*F(22,7)**2*F(256,255), '<', F(40))]
checks += [record('theta envelope exact margin', F(40)-4*F(22,7)**2*F(256,255), '=', F(4184,12495))]
checks += [record('gamma second moment majorant', F(16)+F(3,8), '<', F(18))]
checks += [record('cubic endpoint at zero', F(3)*F(0)**2-F(2)*F(0)**3, '=', F(0))]
checks += [record('cubic endpoint at one', F(3)-F(2), '=', F(1))]
checks += [record('cubic derivative maximum', 6*F(1,2)*(1-F(1,2)), '=', F(3,2))]
checks += [record('crossing-point square ratio', F(288)/F(9,32), '=', F(32)**2)]
checks += [record('gamma large-shift majorant', 2*F(2,3)/F(3,4), '<', F(2))]
checks += [record('geometric tail coefficient', F(8,7)+F(16,49)+F(72,343), '=', F(576,343))]
checks += [record('geometric tail bound', F(576,343), '<', F(2))]
checks += [record('strict prime tail scalar', 160*F(5,4)**2, '=', F(250))]
checks += [record('continuous tail scalar', 80/F(21,8)*F(5,4)*F(1,2), '<', F(25))]
checks += [record('combined residual scalar', F(320+250+25), '<', F(600))]
checks += [record('cross-edge scalar', 11520*F(16,625), '<', F(300))]
checks += [record('taper contribution', F(2*300*7), '=', F(4200))]
checks += [record('residual contribution', F(600*8), '=', F(4800))]
checks += [record('final constant', F(4200+4800), '=', F(9000))]
print(json.dumps({'scope':'source-free exact rational arithmetic only',
                  'analytic_proof_not_certified_by_this_script':True,
                  'check_count':len(checks),'checks':checks},indent=2))
