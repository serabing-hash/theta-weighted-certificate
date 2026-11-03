#!/usr/bin/env python3
"""Exact structural checks only; does not evaluate any actual spectral bound."""
from sympy import symbols, log, atan, diff, simplify, Matrix, eye, Rational
C, t = symbols('C t', positive=True)
# The scalar integral used in the trace estimate.
primitive = C*t - t*log(1+4*t*t)/2 + t - atan(2*t)/2
assert simplify(diff(primitive,t) - (C-log(1+4*t*t)/2)) == 0
# The real weighted Gram identity for a finite model.
R = Matrix([[1,0],[0,1],[1,1],[2,-1]])
g = Matrix([1,2,3,-1]); H=R.T*R; v=R.T*g
Q=eye(4)-R*H.inv()*R.T
assert (g.T*Q*g)[0] == (g.T*g)[0]-(v.T*H.inv()*v)[0]
# A closed threshold includes equality: q=-1, B=1, delta=1, tau=0.
q, B, delta, tau = -1, 1, 1, 0
assert q <= -delta and B >= delta-tau and not (B > delta-tau)
print('PASS: integrated Gamma majorant, true Gram projection, closed-threshold equality')
