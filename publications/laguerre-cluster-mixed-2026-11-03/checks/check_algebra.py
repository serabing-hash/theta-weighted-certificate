#!/usr/bin/env python3
"""Exact symbolic checks only; no Xi zeros, operator-domain facts or numerical sign are certified."""
import sympy as s
h,v,u,z,n1,n2,eps,K,I,J,m,n=s.symbols('h v u z n1 n2 eps K I J m n',real=True)
Q=(h-2*v)*((h+1)**2-4*v)/(h**2*(h+1-2*v))
assert s.factor((1+1/h-Q)-2*v*(3*h+1-4*v)/(h**2*(h+1-2*v))) == 0
num=s.factor((Q-1)*h**2*(h+1-2*v))
assert s.expand(num.subs({h:u+1,v:(1-z)/4})-(u**2+2*u*z+u+z**2/2+3*z/2)) == 0
assert s.expand(2*(1+h-2*v)-((1+h)**2-4*v)-(1-h**2)) == 0
# In q-normalized coordinates, the selected coefficient vector has norm one,
# and the squared source coefficients agree up to the required common factor.
c1=s.sqrt(n2)/s.sqrt(n1+n2); c2=-s.sqrt(n1)/s.sqrt(n1+n2)
assert s.simplify(c1**2+c2**2-1)==0
assert s.simplify((2*s.sqrt(n1)*c1)**2-4*n1*n2/(n1+n2))==0
assert s.simplify((2*s.sqrt(n2)*c2)**2-4*n1*n2/(n1+n2))==0
M=s.Matrix([[2*m*K+eps,-2*s.sqrt(2*m*n)*J],[-2*s.sqrt(2*m*n)*J,4*n*I-eps]])
assert s.simplify(M.det()-((2*m*K+eps)*(4*n*I-eps)-8*m*n*J**2))==0
x=s.symbols('x',real=True)
r=s.symbols('r',positive=True)
# Earlier radius comparison, where x=A*y^2/nu lies in (0,1).
assert s.factor(2*x/(3-x)-x/(2-x)-x*(1-x)/((3-x)*(2-x))) == 0
print('PASS: pair ratio identities, far-pair positivity polynomial, cone comparison, pair Poisson lower bound, mixed source coefficients and 2x2 determinant')
print('Scope: algebra only; analytic inputs, zeros, inequalities involving actual theta integrals, and global positivity are not tested.')
