#!/usr/bin/env python3
"""Saved-endpoint arithmetic only. Does not import/evaluate producer or Gamma/primes."""
import json, hashlib
try:
 import resource
except ImportError:
 resource=None
from pathlib import Path
from fractions import Fraction as Q
if resource is not None:
 resource.setrlimit(resource.RLIMIT_CPU,(60,60)); resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
p=Path(__file__).resolve().parent
hashfile=lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
expected={'joint_gamma_result.diagnostic.json':'b6b37c6df9ae30ffb1011f06ea36f621b2eb871705c7a522924f4a335fa6fd03','joint_gamma_result.failure.json':'473688a4fea0997ee7b5c063a11954503142472c47ccaa03b0eec827a6511e88'}
for f,h in expected.items(): assert hashfile(p/f)==h
assert __debug__, 'Do not use Python -O'
assert hashfile(p/'verify_three_quarters_joint_gamma.py')=='6351a53b9b31ff9cd4e015c32103d42eda113cf273cc14eda51a667b7bb96d51'
d=json.loads((p/'joint_gamma_result.diagnostic.json').read_text()); fail=json.loads((p/'joint_gamma_result.failure.json').read_text())
assert d['status']=='NOT_CERTIFICATE' and fail['status']=='FAILED_POSITIVITY_GATE_NOT_CERTIFICATE'
assert fail['failed_pivot_index']==3 and fail['diagnostic']['sha256']==expected['joint_gamma_result.diagnostic.json']
S=1<<512
class I:
 def __init__(self,a,b=None):
  if isinstance(a,dict):a,b=Q(a['lower_rational']),Q(a['upper_rational'])
  if b is None:b=a
  a,b=Q(a),Q(b);assert a<=b
  self.a=Q((a*S).__floor__(),S);self.b=Q((b*S).__ceil__(),S)
 def __add__(a,b):
  if not isinstance(b,I):b=I(b)
  return I(a.a+b.a,a.b+b.b)
 __radd__=__add__
 def __neg__(a):return I(-a.b,-a.a)
 def __sub__(a,b):return a+-b if isinstance(b,I) else a+I(-b)
 def __mul__(a,b):
  if not isinstance(b,I):b=I(b)
  v=[a.a*b.a,a.a*b.b,a.b*b.a,a.b*b.b];return I(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(a,b):
  if not isinstance(b,I):b=I(b)
  assert not b.a<=0<=b.b
  return a*I(1/b.b,1/b.a)
 def data(a):return {'lower_rational':str(a.a),'upper_rational':str(a.b),'approx':[float(a.a),float(a.b)]}
def mat(v):return [[I(x) for x in row] for row in v]
def ldl(A):
 n=len(A);L=[[I(0) for _ in range(n)] for _ in range(n)];D=[]
 for j in range(n):
  L[j][j]=I(1);D.append(A[j][j]-sum((L[j][k]*L[j][k]*D[k] for k in range(j)),I(0)))
  for i in range(j+1,n):L[i][j]=(A[i][j]-sum((L[i][k]*L[j][k]*D[k] for k in range(j)),I(0)))/D[j]
 return D
w=d['witness_matrices']
for name in ['H9','F9','F_failed_formula_comparison']:
 m=w[name]
 assert all(m[i][j]['lower_rational']==m[j][i]['lower_rational'] and m[i][j]['upper_rational']==m[j][i]['upper_rational'] for i in range(len(m)) for j in range(len(m)))
H=mat(w['H9']);F=mat(w['F9']);Old=mat(w['F_failed_formula_comparison'])
hp=ldl(H);fp=ldl([r[:4] for r in F[:4]])
assert all(x.a>0 for x in hp);assert all(x.a>0 for x in fp[:3]) and fp[3].b<0
ov=d['finite_overlap_diagnostics']
zeta=[I(x) for x in ov['zeta']];ys=[I(x) for row in ov['Y_s'] for x in row]
assert len(zeta)==32 and len(ys)==256 and all(x.a>0 or x.b<0 for x in zeta+ys)
mid=lambda x:(x.a+x.b)/2
# Exact rational 3x3 elimination followed by explicit denominator-10^12 rounding.
A=[[mid(F[i][j]) for j in range(3)]+[-mid(F[i][3])] for i in range(3)]
for k in range(3):
 q=A[k][k];assert q
 A[k]=[v/q for v in A[k]]
 for i in range(3):
  if i!=k:
   q=A[i][k];A[i]=[a-q*b for a,b in zip(A[i],A[k])]
z_exact=[r[3] for r in A]+[Q(1)]+[Q(0)]*28
z=[Q(round(x*10**12),10**12) for x in z_exact]
def quadratic(M,z):return sum((M[i][j]*z[i]*z[j] for i in range(4) for j in range(4)),I(0))
new=quadratic(F,z);old=quadratic(Old,z);delta=quadratic([[F[i][j]-Old[i][j] for j in range(4)] for i in range(4)],z)
norm=sum(x*x for x in z)
budget={name:quadratic(mat(w[name]),z) for name in ['A','C0','joint_correction','C_new']}
assert budget['A'].a>0
assembled=budget['A']-budget['C0']+budget['joint_correction']
assert assembled.b<0
# Independently assembled and saved F9 quadratic enclosures must overlap.
assert max(assembled.a,new.a)<=min(assembled.b,new.b)
assert new.b<0 and old.b<0 and delta.a>0
short={}
for name,v,lo,hi in [('F9',new,'-0.0000004941393','-0.0000004941391'),('F_failed',old,'-0.0000005664564','-0.0000005664563'),('deltaF',delta,'0.0000000723171','0.0000000723172')]:
 assert Q(lo)<=v.a<=v.b<=Q(hi)
 short[name]={'lower_exact_decimal':lo,'upper_exact_decimal':hi}
out={'status':'SAVED_COMPARISON_MATRIX_NEGATIVITY_CERTIFIED_NOT_PHYSICAL_COUNTEREXAMPLE','verified_input_hashes':expected,'source_sha256':hashfile(p/'verify_three_quarters_joint_gamma.py'),'same_vector_budget':{k:v.data() for k,v in budget.items()},'assembled_A_minus_C0_plus_correction':assembled.data(),'short_exact_enclosures':short,'symmetric_interval_matrices_verified':True,'fixedpoint_bits':512,'H9_independent_LDL_pivots':[x.data() for x in hp],'F9_independent_leading4_LDL_pivots':[x.data() for x in fp],'overlap_nonzero_counts':{'zeta':len(zeta),'Y_s':len(ys)},'z_32_rational':[str(x) for x in z],'exact_midpoint_solve_first3':[str(x) for x in z_exact[:3]],'z_norm_squared_exact':str(norm),'z_norm_squared_approx':float(norm),'z_F9_z':new.data(),'z_F_failed_z':old.data(),'z_deltaF_z':delta.data(),'normalized_F9':(new/I(norm)).data(),'normalized_F_failed':(old/I(norm)).data(),'normalized_improvement':(delta/I(norm)).data(),'trust_boundary':'Only saved rational interval arithmetic is independently checked. Analytic validity and construction of input intervals remain source-relative. Negative F9 is failure of a sufficient comparison, NOT negativity of physical q and NOT an RH counterexample.'}
(p/'saved_arithmetic_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k in ['status','z_32_rational','z_norm_squared_exact','z_norm_squared_approx','z_F9_z','z_F_failed_z','z_deltaF_z','overlap_nonzero_counts']},indent=2))
