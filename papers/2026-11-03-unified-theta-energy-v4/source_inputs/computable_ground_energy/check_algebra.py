#!/usr/bin/env python3
"""Checks of finite identities, not implementation of the analytic enclosure."""
from fractions import Fraction as F
from sympy import Matrix, eye, Rational
# Equality at either overlapping threshold leaves a strict succeeding branch.
L, U = F(-16), F(0)
a, b = L+(U-L)/3, L+2*(U-L)/3
for ground in [L, a, (a+b)/2, b, U]:
    positive_branch = ground > a
    negative_branch = ground < b
    assert positive_branch or negative_branch
    if positive_branch:
        assert a <= ground <= U and U-a == F(2,3)*(U-L)
    if negative_branch:
        assert L <= ground <= b and b-L == F(2,3)*(U-L)
# Concrete finite-dimensional constrained inverse identity.
A = Matrix([[3,1,0],[1,4,1],[0,1,2]])
V = Matrix([[1],[0],[1]])
R = A.inv(); Rs = R-R*V*(V.T*R*V).inv()*V.T*R
assert V.T*Rs == Matrix.zeros(1,3)
# For the sample basis of ker(V.T), Rs A acts as the identity.
K = Matrix([[1,0],[0,1],[-1,0]])
assert Rs*A*K == K
# Exact finite Neumann remainder in a scalar spectral example.
delta, alpha, ell = F(1,2), F(3), 7
y = 1-delta/alpha
partial = sum((y**j for j in range(ell+1)),F(0))/alpha
assert partial + y**(ell+1)/delta == 1/delta
print('PASS: overlap/equality branches, constrained inverse, finite Neumann remainder')
