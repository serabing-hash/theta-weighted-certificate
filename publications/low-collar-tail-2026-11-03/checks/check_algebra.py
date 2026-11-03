#!/usr/bin/env python3
"""Finite exact checks of identities and the explicit Gamma cutoff, not a spectral certificate."""
from sympy import Matrix, Rational, symbols, exp, sqrt, simplify
from math import factorial
H = symbols('H', positive=True)
T = sqrt(exp(2*H)-1)/2
assert simplify(1+4*T**2-exp(2*H)) == 0
# Verify true Gram and radical projection algebra with exact rational entries.
R = Matrix([[1,0],[0,1],[1,1],[2,-1]])
Z = Matrix([[1,2],[3,-1],[0,1],[1,0]])
P = R*(R.T*R).inv()*R.T
G = Z.T*(Matrix.eye(4)-P)*Z
cross = R.T*Z
assert G == Z.T*Z-cross.T*(R.T*R).inv()*cross
assert all(v >= 0 for v in G.eigenvals())
# The factorial estimate used for the Taylor schedule, checked on small m.
# The general inequality follows from the integral estimate log(m!) >= m log(m)-m.
from math import e
assert all(factorial(m) >= (m/e)**m for m in range(1, 101))
print('PASS: explicit Gamma inversion, exact projected Gram, sample factorial bounds')
