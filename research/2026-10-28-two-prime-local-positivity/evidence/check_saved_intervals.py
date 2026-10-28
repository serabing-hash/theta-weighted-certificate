"""Independent saved-data audit. No producer import or evaluation, no flint."""
import resource
resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(60,60))
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib,time
start=time.monotonic(); root=Path(__file__).resolve().parent
expected={root/'three_fifths_certificate.json':'a03d1c4b18e70eab850ec1624b59c2cc74be9778f31a279ffb0d489b0aec3f99',root/'verify_three_fifths.py':'6a66a20e3c74433680921865f53bb9dea9cdd742f88d915d44110445ee63205a'}
for p,h in expected.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==h,str(p)
d=json.loads((root/'three_fifths_certificate.json').read_text())
assert d['verifier_sha256']==expected[root/'verify_three_fifths.py']
count=0
def readball(a):
 lo,hi=Q(a['lower_rational']),Q(a['upper_rational']);assert lo<=hi;return lo,hi
def walk(a):
 global count
 if isinstance(a,dict):
  if 'lower_rational' in a:readball(a);count+=1
  else:
   for v in a.values():walk(v)
 elif isinstance(a,list):
  for v in a:walk(v)
walk(d);assert count==1305
w=d['witness_matrices']; mats={}
for name in ['A','C','F','L','L_inverse']:
 a=w[name];assert len(a)==16 and all(len(r)==16 for r in a);mats[name]=[[readball(x) for x in r] for r in a]
assert len(w['LDL_pivots'])==16
for name in ['A','C','F']:
 for i in range(16):
  for j in range(16):assert mats[name][i][j]==mats[name][j][i]
for name in ['L','L_inverse']:
 for i in range(16):
  assert mats[name][i][i]==(Q(1),Q(1))
  for j in range(i+1,16):assert mats[name][i][j]==(Q(0),Q(0))
piv=[readball(x) for x in w['LDL_pivots']];ds=min(x[0] for x in piv);assert ds>0 and ds==Q(d['pivot_lower_bound'])
U=sum(max(abs(l),abs(h))**2 for row in mats['L_inverse'] for l,h in row)
assert U==Q(d['inverse_L_frobenius_squared_upper_bound'])
mu=Q(d['schur_margin_low_mode_L2']);assert mu==ds/U
tau=Q(d['coupling_trace_upper_bound']);assert tau>=sum(mats['C'][i][i][1] for i in range(16)) and tau>0
assert tau==readball(d['coupling_bound_trace'])[1]
g=Q(d['q_lower_bound_L2']);assert g==min(3*mu/(3+5*tau),Q(3,5)) and g>=Q(1,20000000000000)
assert readball(d['high_block_floor_at_M'])[0]>Q(6,5) and readball(d['high_block_floor_at_N'])[0]>Q(36,5)
# Independently enclose matrix operations with fixed outward dyadic rounding.
scale=1<<512
def rnd(lo,hi):return Q((lo.numerator*scale)//lo.denominator,scale),Q(-((-hi.numerator*scale)//hi.denominator),scale)
def add(a,b):return rnd(a[0]+b[0],a[1]+b[1])
def mul(a,b):
 v=[x*y for x in a for y in b];return rnd(min(v),max(v))
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def div(a,b):
 assert b[0]>0;return mul(a,(1/b[1],1/b[0]))
def mm(a,b):
 out=[]
 for row in a:
  r=[]
  for j in range(len(b[0])):
   s=(Q(0),Q(0))
   for k in range(len(b)):s=add(s,mul(row[k],b[k][j]))
   r.append(s)
  out.append(r)
 return out
# Direct independent LDL, using only stored F as input.
F=mats['F'];Li=[[(Q(0),Q(0)) for j in range(16)] for i in range(16)];pi=[]
for i in range(16):
 Li[i][i]=(Q(1),Q(1));p=F[i][i]
 for k in range(i):p=sub(p,mul(mul(Li[i][k],Li[i][k]),pi[k]))
 assert p[0]>0;pi.append(p)
 for j in range(i+1,16):
  v=F[j][i]
  for k in range(i):v=sub(v,mul(mul(Li[j][k],Li[i][k]),pi[k]))
  Li[j][i]=div(v,p)
# Independent congruence: saved inverse midpoint is merely a chosen rational
# invertible preconditioner; no assumption that it actually inverts L is needed.
Z=[[(Q(l+h,2),Q(l+h,2)) for l,h in row] for row in mats['L_inverse']]
G=mm(mm(Z,F),list(map(list,zip(*Z))))
dG=min(G[i][i][0]-sum(max(abs(G[i][j][0]),abs(G[i][j][1])) for j in range(16) if j!=i) for i in range(16));assert dG>0
UZ=sum(x[0]**2 for row in Z for x in row);mu2=dG/UZ;g2=min(3*mu2/(3+5*tau),Q(3,5));assert g2>=Q(1,20000000000000)
# Check residuals of supplied factor enclosures, consistency not exact identity.
LD=[ [mul(mats['L'][i][j],piv[j]) for j in range(16)] for i in range(16)]
recon=mm(LD,list(map(list,zip(*mats['L']))));invprod=mm(mats['L'],mats['L_inverse'])
for i in range(16):
 for j in range(16):
  rr=sub(recon[i][j],F[i][j]);assert rr[0]<=0<=rr[1]
  target=Q(int(i==j));assert invprod[i][j][0]<=target<=invprod[i][j][1]
out={'status':'PASS_INDEPENDENT_SAVED_INTERVAL_AUDIT','result_sha256':expected[root/'three_fifths_certificate.json'],'unique_interval_records':count,'independent_LDL_positive':True,'independent_min_pivot_lower':str(min(x[0] for x in pi)),'independent_congruence_gershgorin_lower':str(dG),'independent_mu':str(mu2),'independent_full_gap':str(g2),'independent_full_gap_float':float(g2),'simple_full_gap':'1/20000000000000','saved_scalar_equalities_checked':True,'saved_LDL_and_inverse_residuals_contain_zero':True,'producer_imported_or_rerun':False,'rounding_bits':512,'elapsed_seconds':time.monotonic()-start,'scope':'Arithmetic conditional on saved F and C enclosing the analytically specified Schur matrices; no special-function source inclusion or domain proof rerun.'}
(root/'INDEPENDENT_SAVED_INTERVAL_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['independent_min_pivot_lower','independent_congruence_gershgorin_lower','independent_mu','independent_full_gap']},indent=2))
