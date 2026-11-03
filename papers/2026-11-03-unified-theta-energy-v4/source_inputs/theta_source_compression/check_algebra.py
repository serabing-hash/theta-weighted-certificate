#!/usr/bin/env python3
"""Elementary exact checks; no actual theta Gram or eigenvalues are computed."""
from fractions import Fraction as F
from math import factorial
from sympy import Matrix, eye
# e^4 exceeds its degree-five positive Taylor partial sum, which exceeds 42.
assert sum((F(4)**k / factorial(k) for k in range(6)), F(0)) > 42
# Base case of 160 M² < (5/2)^(3M/2) at M=8.
assert 160 * 8**2 < F(5,2)**12
# With h>=1, the proof's slack 1/(2h)+1/(16h²) <= 9/(16h).
for h in [F(1), F(2), F(7,2), F(100)]:
    assert F(1,2)/h + F(1,16)/(h*h) <= F(9,16)/h
# Actual-projection algebra in an exact finite model; P is not a coefficient identity.
V=Matrix([[1,0],[0,1],[1,1],[2,-1]])
G=V.T*V; P=V*G.inv()*V.T; Q=eye(4)-P
g=Matrix([1,2,3,-1]); a=V*Matrix([2,-1])
assert Q*V == Matrix.zeros(4,2)
assert (g.T*Q*g)[0] <= ((g-a).T*(g-a))[0]
print('PASS: explicit elementary constants, tail slack, and true projection model')
