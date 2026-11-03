#!/usr/bin/env python3
"""Exact rational checks of constants and noncommuting model identities.
These model checks are NOT a new theta positivity certificate.
"""
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import json
p=Path(__file__).resolve().parent

def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def neg(a):return [[-x for x in r] for r in a]
def sub(a,b):return add(a,neg(b))
def scale(c,a):return [[c*x for x in r] for r in a]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def eye(n):return [[F(int(i==j)) for j in range(n)] for i in range(n)]
def inv2(a):
 d=a[0][0]*a[1][1]-a[0][1]*a[1][0];assert d
 return scale(1/d,[[a[1][1],-a[0][1]],[-a[1][0],a[0][0]]])
def psd2(a):
 assert a==tr(a)
 return a[0][0]>=0 and a[1][1]>=0 and a[0][0]*a[1][1]-a[0][1]**2>=0
def enc(a):return [[str(x) for x in row] for row in a]

R=2**18;d=36;k=F(d,R)
table=[]
with localcontext() as ctx:
 ctx.prec=60
 for n in range(7):
  t=k**(2*n)/(1-k);e=F(d*d,R)*t
  table.append({'n':n,'polynomial_degree':2*n-1 if n else None,
    'relative_tail_exact':str(t),'absolute_tail_exact':str(e),
    'absolute_tail_decimal':str(Decimal(e.numerator)/Decimal(e.denominator))})
assert F(table[1]['absolute_tail_exact'])<F(933,10**13)
assert F(table[2]['absolute_tail_exact'])<F(176,10**20)
assert F(table[3]['absolute_tail_exact'])<F(332,10**28)
for j in range(1,len(table)):
 assert F(table[j]['absolute_tail_exact'])==k*k*F(table[j-1]['absolute_tail_exact'])
prime_tail=F(3609,10**21)
prime_schur_error=prime_tail*(1+F(d,R-d)**2)
assert prime_schur_error<F(361,10**20)
combined=F(table[2]['absolute_tail_exact'])+prime_schur_error
assert combined<F(537,10**20)
# High Gamma and D do not commute, so no simultaneous diagonalization shortcut.
G=[[F(4),F(0)],[F(0),F(9)]]
D=[[F(1),F(1,2)],[F(1,2),F(-1)]]
assert mul(G,D)!=mul(D,G)
I=eye(2);half_inv=[[F(1,2),F(0)],[F(0),F(1,3)]]
K=mul(mul(half_inv,D),half_inv);kap=F(1,2)
assert psd2(sub(scale(kap,I),K)) and psd2(add(scale(kap,I),K))
C=sub(G,D);Ci=inv2(C)
assert Ci==mul(mul(half_inv,inv2(sub(I,K))),half_inv)
B=[[F(1,3),F(1,4)],[F(1,5),F(-1,7)]]
T=mul(half_inv,B);W=mul(tr(T),T);cost=mul(mul(tr(B),Ci),B)
models=[]
for name,A in [('positive',add(cost,I)),('zero',cost),('negative',sub(cost,I))]:
 S=sub(A,cost);P=[[F(0),F(0)],[F(0),F(0)]];power=I
 previous_lower=previous_upper=None
 stages=[]
 for n in range(5):
  if n:
   P=add(P,power);power=mul(power,K)
   P=add(P,power);power=mul(power,K)
  tail=kap**(2*n)/(1-kap)
  upper=sub(A,mul(mul(tr(T),P),T));lower=sub(upper,scale(tail,W))
  assert psd2(sub(S,lower)) and psd2(sub(upper,S))
  assert psd2(sub(scale(tail,W),sub(upper,S)))
  assert psd2(sub(scale(tail,W),sub(S,lower)))
  if previous_lower is not None:
   assert psd2(sub(lower,previous_lower)) and psd2(sub(previous_upper,upper))
  if name=='zero':assert not psd2(lower) # Exact endpoint need not have a finite lower PSD certificate.
  if name=='negative':assert not psd2(S)
  stages.append({'n':n,'lower':enc(lower),'upper':enc(upper)})
  previous_lower=lower;previous_upper=upper
 models.append({'name':name,'S':enc(S),'stages':stages})
out={'status':'PASS','R':R,'d':d,'kappa':str(k),'error_table':table,'prime_tail_rational_upper':str(prime_tail),
 'prime_Schur_error_upper':str(prime_schur_error),'cubic_plus_prime_error_upper':str(combined),
 'noncommuting_models':models,
 'scope':'Exact scalar constants and finite model tests of the proved identities; no new actual-theta low matrix or spectral projection is evaluated.',
 'not_proved':['actual theta Schur positivity on the whole low sector','global one-half','RH']}
(p/'RESPONSE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: exact error constants; three noncommuting models; monotone upper/lower brackets.')
for row in table[:4]:print('n=',row['n'],'absolute error <=',row['absolute_tail_decimal'])
print('PASS: full prime-tail Schur perturbation < 3.610e-18; cubic plus prime error < 5.37e-18.')
