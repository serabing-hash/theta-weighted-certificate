#!/usr/bin/env python3
"""Exact finite-dimensional checks, not a proof of the analytic inputs."""
from fractions import Fraction
from sympy import Matrix, Rational, eye, symbols, expand

# A concrete P and its expansion in the actual derivative radical basis.
y = symbols('y')
P = 1 - 2*y + 3*y**2
Q = expand((y + Rational(1, 4))*P)
assert Q.subs(y, Rational(-1, 4)) == 0
# Q(y)=sum b_j ((-1)^j y^j - 4^-j), with y=t^2.
b = [Q.coeff(y, j) * (-1)**j for j in range(1, 4)]
assert expand(Q - sum(b[j-1]*((-1)**j*y**j - Rational(1,4)**j) for j in range(1,4))) == 0

# Exact representative matrix check of the algebra in equations (Fdef), (rows).
R = Matrix([[1, 0], [0, 1], [1, 1], [2, -1]])
D = Matrix([[2,1,0,-1],[1,-1,2,0],[0,2,3,1],[-1,0,1,-2]])
G = R.T*R; Pm = R*G.inv()*R.T; Y = D*R
F = Pm*D+D*Pm-Pm*D*Pm
Frows = R*G.inv()*Y.T + Y*G.inv()*R.T - R*G.inv()*(R.T*Y)*G.inv()*R.T
assert F == Frows and (D-F)*R == Matrix.zeros(4,2)
assert F.rank() <= 2*R.cols
# Rational majorants for the two elementary summations in the text.
q = Fraction(1, 20)  # exp(-pi) < 1/20
assert (1+q)/(1-q)**3 < 2
assert 4*Fraction(22,7)**2*Fraction(500,499) < 40
print('PASS: radical polynomial identity; finite-row repair; rank bound; rational majorants')
