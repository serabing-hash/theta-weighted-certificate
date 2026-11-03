#!/usr/bin/env python3
"""Exact symbolic consistency checks, not a proof of the analytic theorem."""
from sympy import symbols, cos, diff, trigsimp, simplify
x, y, a, t = symbols('x y a t', real=True, nonzero=True)
# The positive-orientation cross correlation includes the opposite shift
# through the factor 2 in p[u].
assert trigsimp(2*cos(x+y)*cos(y-x) - cos(2*x) - cos(2*y)) == 0
# One complete Gamma-series term and its derivative.
f = 2*t**2/(a*(a*a+t*t))
assert simplify(diff(f,t) - 4*t*a/(a*a+t*t)**2) == 0
# Lower theta summand: 4*pi^2*n^2 - 6*pi*n - 2*pi^2*n^2
# factors as 2*pi*n*(pi*n-3), nonnegative for n>=2, pi>3.
p, n = symbols('p n', positive=True)
assert simplify((4*p*p*n*n-6*p*n-2*p*p*n*n)-2*p*n*(p*n-3)) == 0
print('PASS: paired-packet identity, Gamma-series derivative, theta lower-bound factorization')
