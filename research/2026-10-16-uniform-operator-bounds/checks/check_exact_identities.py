#!/usr/bin/env python3
"""Small exact-algebra checks, not an all-low16 numerical certificate.

Python 3 standard library only. No network, quadrature, source moments,
large source matrices, eigenvalue search, or earlier certificate execution.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, value):
    if not value:
        raise AssertionError(name)
    checks.append({'name': name, 'passed': True})

def mat(rows):
    return [[F(x) for x in row] for row in rows]

def add(A, B):
    return [[a+b for a,b in zip(ar,br)] for ar,br in zip(A,B)]

def scale(s, A):
    return [[s*x for x in row] for row in A]

def sub(A, B):
    return add(A, scale(-1,B))

def tr(A):
    return [list(row) for row in zip(*A)]

def mul(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]

def det(A):
    return A[0][0]*A[1][1]-A[0][1]*A[1][0]

def inv(A):
    return scale(1/det(A), [[A[1][1],-A[0][1]],[-A[1][0],A[0][0]]])

def psd2(A):
    return A == tr(A) and A[0][0]>=0 and A[1][1]>=0 and det(A)>=0

B=F(3,4)
check('low16 dimension and endpoint sum 496', len(range(0,31,2))==16 and sum(4*j+1 for j in range(16))==496)
check('k96 output degree and full 65-mode prefix', max(96,95+30+1)==126 and 126<=128 and len(range(0,129,2))==65)
# p1=(t²−1)/2=(P2(t)−1)/3; coefficients in monomial order.
p1=[-F(1,2),0,F(1,2)]
P2=[-F(1,2),0,F(3,2)]
check('endpoint profile normalization', p1==[(P2[0]-1)/3,P2[1]/3,P2[2]/3])
check('profile physical norm', 2*B*(F(1,5)-F(2,3)+1)/4 == F(4,15)*B)
check('Legendre tail telescoping coefficient', all(F(2*m+1,m*m*(m+1)*(m+1)) == F(1,m*m)-F(1,(m+1)*(m+1)) for m in range(2,40)))
# Formal power series of s*exp(−s/2)/(1−exp(−2s)), through degree 3.
num=[F(-1,2)**i/factorial(i) for i in range(4)]
den=[-F(-2)**(i+1)/factorial(i+1) for i in range(4)]
quo=[]
for i in range(4):
    quo.append((num[i]-sum(den[j]*quo[i-j] for j in range(1,i+1)))/den[0])
check('kernel Taylor and cusp coefficients', quo==[F(1,2),F(1,4),-F(1,48),-F(1,32)] and 2*quo[2]==-F(1,24))
# Complete exact scalar remainder only; no source integration.
U=[F(1)]; V=[F(1)]
for n in range(1,49):
    U.append(-sum(U[n-j]/factorial(2*j+1) for j in range(1,n+1)))
    V.append(-sum(V[n-j]/factorial(2*j) for j in range(1,n+1)))
check('reciprocal recurrence annihilation through degree 96', all(sum(U[n-j]/factorial(2*j+1) for j in range(n+1))==0 and sum(V[n-j]/factorial(2*j) for j in range(n+1))==0 for n in range(1,49)))
a=B

def tail(j,e):
    return a**(2*j)/factorial(2*j+e)/(1-a*a/F((2*j+e+1)*(2*j+e+2)))
Ek=sum(a**(2*n)*(abs(U[n])*tail(49-n,1)/a+abs(V[n])*tail(49-n,0)) for n in range(49))/4
th=F(3,8)**32/factorial(32)/(1-F(3,8)**2/(33*34))
saved=json.loads((ROOT/'sources/REMAINDER_CONSTANTS.json').read_text())
check('complete kernel remainder matches inherited exact rational', Ek==F(saved['kernel_error']))
check('complete pole remainder matches inherited exact rational', th==F(saved['pole_high_tail']))
check('all defined cosh tail denominators positive', all(1-(B/2)**2/((M+3)*(M+4))>0 for M in range(30,131,2)))
I=mat([[1,0],[0,1]])
A0=mat([[1,0],[0,2]])
P=scale(F(1,10),mat([[1,1],[1,1]]))
K=inv(add(A0,P))
R=scale(F(1,2),I)
Mr=add(mul(mul(K,P),K),mul(mul(mul(mul(K,A0),R),A0),K))
check('exact noncommutative response counterexample matrix', K==scale(F(1,23),mat([[21,-1],[-1,11]])) and Mr==scale(F(1,1058),mat([[525,-25],[-25,505]])))
check('inverse norm alone does not give response half-bound', det(sub(scale(F(1,2),I),Mr))<0)
# Independent rational residual-identity fixture.
H=mat([[3,1],[1,2]]); R=inv(H)
J=mat([[F(1,3),F(2,5)],[F(-1,4),F(3,7)]])
F0=mat([[F(5,3),F(-2,7)],[F(4,9),F(7,5)]])
Xi=sub(F0,mul(H,J))
lhs=mul(mul(tr(F0),R),F0)
rhs=add(sub(add(mul(tr(F0),J),mul(tr(J),F0)),mul(mul(tr(J),H),J)),mul(mul(tr(Xi),R),Xi))
check('exact finite residual identity fixture', lhs==rhs)
Vcoord=mat([[1,1],[0,2]]); N=mul(tr(Vcoord),Vcoord); eps=F(3,11)
check('physical metric isotropic congruence', mul(mul(tr(Vcoord),scale(eps,I)),Vcoord)==scale(eps,N))
E=mat([[2,F(3,4)],[F(3,4),-1]])
Dr=mat([[F(11,4),0],[0,F(7,4)]])
check('row-radius Loewner fixture both directions', psd2(add(Dr,E)) and psd2(sub(Dr,E)))
check('response scalar bound endpoint and monotonicity premises', all(2*(a*c/(a+c))<=a and 1/a-(a*c/(a+c))/a**2==1/(a+c) for a in [F(1),F(4,5),F(7,3)] for c in [a/5,a/2,a]))
check('elementary shift separation lower exponential bound', sum(F(3)**j/factorial(j) for j in range(5))>16)
result={'status':'PASS_EXACT_ALGEBRA_ONLY','check_groups':len(checks),'checks':checks,'source_moment_computations':0,'actual_16x16_matrix_evaluations':0,'schur_sign_evaluated':False,'full_certificate_reruns':0,'limitations':'Finite fixtures and rational identities do not replace the analytical proofs or the remaining numerical all-coefficient certificate.'}
print(json.dumps(result,indent=2))
