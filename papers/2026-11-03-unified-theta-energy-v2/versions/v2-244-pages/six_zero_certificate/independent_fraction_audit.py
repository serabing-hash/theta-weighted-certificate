#!/usr/bin/env python3
"""Independent exact interval reconstruction and determinant verification.
Standard library only. Does not prove the analytic origins of input enclosures.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
x=json.loads((p/'CERTIFICATE.json').read_text());y=json.loads((p/'MATRIX_ENCLOSURE.json').read_text())
z=json.loads((p/'FIXED_SPLIT_CERTIFICATE.json').read_text());L=json.loads((p/'RATIONAL_MATRICES.json').read_text())
def iv(s):
 s=s.strip()
 if s.startswith('['):
  m,r=s[1:-1].split(' +/- ');return (F(m)-F(r),F(m)+F(r))
 return F(s),F(s)
def pt(s):return F(s),F(s)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 t=[v*w for v in a for w in b];return min(t),max(t)
def scale(a,s):return mul(a,pt(s))
def mats(rows):return [[iv(s) for s in row] for row in rows]
def bound(E,sgn):
 n=len(E);assert all(E[i][j]==E[j][i] for i in range(n) for j in range(n))
 rho=max(sum((b-a)/2 for a,b in row) for row in E)
 return [[sum(E[i][j])/2+(sgn*rho if i==j else 0) for j in range(n)] for i in range(n)],rho
def principal(A,k):return [r[:k] for r in A[:k]]
def det(A):
 # Ordinary Gaussian determinant, not the source LDL recurrence.
 B=[r[:] for r in A];value=F(1)
 for k in range(len(B)):
  if not B[k][k]:
   rows=[j for j in range(k+1,len(B)) if B[j][k]]
   if not rows:return F(0)
   j=rows[0];B[j],B[k]=B[k],B[j];value=-value
  pivot=B[k][k];value*=pivot
  for i in range(k+1,len(B)):
   ratio=B[i][k]/pivot
   for j in range(k+1,len(B)):B[i][j]-=ratio*B[k][j]
 return value
def schur(A):return det(A)/det(principal(A,len(A)-1))
G=mats(x['G']);H=mats(x['H']);D=mats(y['D2_Gram']);Q=mats(y['sufficient_q0_matrix'])
a=iv(z['gamma_tangent_a']);b=iv(z['gamma_tangent_b'])
acoef=scale(mul(a,a),F(153,8));bcoef=scale(mul(b,b),306)
row=[[add(add(mul(acoef,H[i][j]),mul(bcoef,D[i][j])),scale(G[i][j],1458)) for j in range(6)] for i in range(6)]
reconstructed={
 'source':[[sub(Q[i][j],scale(G[i][j],F(1,40))) for j in range(6)] for i in range(6)],
 'derivative':[[sub(scale(G[i][j],2**20),D[i][j]) for j in range(6)] for i in range(6)],
 'fixed_split':[[sub(Q[i][j],scale(G[i][j],F(2704,262108)+F(1,70))) for j in range(6)] for i in range(6)],
 'matrix_graph':[[sub(sub(Q[i][j],scale(row[i][j],F(1,262108))),scale(G[i][j],F(1,50))) for j in range(6)] for i in range(6)]}
floors={'source':list(map(F,['.030','.032','.008','.011','.0014','.0004'])),
 'fixed_split':list(map(F,['.030','.032','.008','.011','.0014','.0005'])),
 'matrix_graph':list(map(F,['.030','.032','.008','.010','.0014','.0002'])),
 'derivative':list(map(F,[127000,108000,56000,61000,14000,20000]))}
out={};containment=[]
for name,ledger in L.items():
 d=int(ledger['scale']);E=[[(F(int(lo),d),F(int(hi),d)) for lo,hi in r] for r in ledger['entries']]
 for i in range(6):
  for j in range(6):
   lo,hi=reconstructed[name][i][j];assert E[i][j][0]<=lo<=hi<=E[i][j][1],(name,i,j,lo,hi,E[i][j])
   containment.append([name,i,j,True])
 A,rho=bound(E,-1);ms=[F(1)]+[det(principal(A,k)) for k in range(1,7)]
 assert all(m>0 for m in ms)
 ps=[ms[k+1]/ms[k] for k in range(6)]
 assert all(a>b for a,b in zip(ps,floors[name]))
 out[name]={'radius_row_sum':str(rho),'principal_determinants':[str(m) for m in ms[1:]],
  'determinant_ratios':[str(t) for t in ps],'ratio_decimals':[float(t) for t in ps],
  'strict_floors':[str(v) for v in floors[name]],'last_schur':str(ps[-1]),'last_schur_decimal':float(ps[-1])}
Gl,_=bound(G,-1);Gu,_=bound(G,1)
assert all(det(principal(Gl,k))>0 for k in range(1,7))
gl=schur(Gl);gu=schur(Gu);assert gl>F('.04273614502025') and gu<F('.04273614502027')
strong=[[sub(Q[i][j],scale(G[i][j],F(1,25))) for j in range(6)] for i in range(6)]
Sl,_=bound(strong,-1);Su,_=bound(strong,1)
assert all(det(principal(Sl,k))>0 for k in range(1,6))
ss=schur(Su);assert ss<0
r=2**18;d=36;g=r-d
scalar=F(1,40)-F(52**2,g);assert scalar>F(1,70)
attach=F(1,50)/(1+2*F(d,g)**2);assert attach==F(4293787729,214689394550) and attach>F(1,51) and F(g,2)>F(1,51)
kappa=F(d,r);coupling=F(50*d*d,r);assert kappa==F(9,65536) and coupling==F(2025,8192) and coupling<1-kappa
report={'status':'PASS','method':'Exact Fraction interval reconstruction plus Gaussian determinants; no supplied LDL routine imported',
 'matrices':out,'all_144_reconstructed_entries_inside_ledger':containment,
 'raw_Gram_innovation_lower':str(gl),'raw_Gram_innovation_upper':str(gu),
 'stronger_1_over_25_sufficient_Schur_upper':str(ss),'stronger_comparison_decimal':float(ss),
 'scalar_transfer':str(scalar),'attachment':str(attach),'kappa':str(kappa),'complete_coupling':str(coupling),
 'input_hashes':{f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['CERTIFICATE.json','MATRIX_ENCLOSURE.json','FIXED_SPLIT_CERTIFICATE.json','RATIONAL_MATRICES.json']},
 'scope':'Finite rational signs, exact affine reconstruction and scalar transfer only. Analytic quadrature, sector admission and exhaustion premises are separately audited.'}
(p/'INDEPENDENT_FRACTION_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: all 144 entries reconstructed within ledger, 24 positive determinant ratios above claimed floors, Gram innovation, stronger-comparison failure and exact scalar transfers.')
print('Matrix graph sixth Schur:',out['matrix_graph']['last_schur_decimal'])
