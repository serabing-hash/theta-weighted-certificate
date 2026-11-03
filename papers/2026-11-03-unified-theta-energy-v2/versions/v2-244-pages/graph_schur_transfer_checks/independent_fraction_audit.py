#!/usr/bin/env python3
"""Independent exact checks for the frozen graph-to-Schur transfer certificate.
Uses decimal rational endpoints and determinant expansion, not interval LDL.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
import json,re,hashlib
P=Path(__file__).resolve().parent
S=P
checks={}
def check(key,value):
    checks[key]=bool(value)
    if not value: raise AssertionError(key)
def ball(s):
    s=str(s).strip()
    if '+/-' not in s: a=F(s);return a,a
    a,r=s.strip('[]').split('+/-');a,r=F(a.strip()),F(r.strip())
    check('nonnegative_decimal_radii',r>=0)
    return a-r,a+r
def det(A):
    n=len(A);out=F(0)
    for p in permutations(range(n)):
        z=F((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n): z*=A[i][p[i]]
        out+=z
    return out
x=json.loads((S/'INPUT5_CERTIFICATE.json').read_text());y=json.loads((S/'INPUT5_MATRIX_CERTIFICATE.json').read_text())
r=json.loads((S/'DERIVATIVE_RATIONAL_MATRIX.json').read_text());scale=int(r['scale'])
G=[[ball(z) for z in row] for row in x['G']];D=[[ball(z) for z in row] for row in y['D2_Gram']]
E=[[(F(int(a),scale),F(int(b),scale)) for a,b in row] for row in r['entries']]
for i in range(5):
    for j in range(5):
        lo,hi=2**20*G[i][j][0]-D[i][j][1],2**20*G[i][j][1]-D[i][j][0]
        check(f'export_contains_exact_decimal_interval_{i}_{j}',E[i][j][0]<=lo<=hi<=E[i][j][1])
        check(f'symmetry_{i}_{j}',E[i][j]==E[j][i])
mid=[[(a+b)/2 for a,b in row] for row in E];rho=max(sum((b-a)/2 for a,b in row) for row in E)
A=[[mid[i][j]-(rho if i==j else 0) for j in range(5)] for i in range(5)]
mins=[det([row[:k] for row in A[:k]]) for k in range(1,6)]
for k,d in enumerate(mins,1):check(f'leading_principal_minor_{k}_positive',d>0)
piv=[mins[0]]+[mins[k]/mins[k-1] for k in range(1,5)]
check('minimum_LDL_pivot_exceeds_14000',all(t>14000 for t in piv))
g=2**18-36;schur=F(1,25)-F(52**2,g);mu=F(1,35)/(1+2*F(36,g)**2)
check('exact_gap',g==262108)
check('exact_schur_floor',schur==F(48627,1638175))
check('schur_exceeds_1_over_35',schur>F(1,35))
check('exact_attachment_floor',mu==F(613398247,21468939455))
check('attachment_exceeds_1_over_36',mu>F(1,36))
check('high_square_floor_exceeds_1_over_36',F(g,2)>F(1,36))
kappa=F(36,2**18);eta2=F(35*36**2,2**18)
check('kappa',kappa==F(9,65536));check('eta_squared',eta2==F(2835,16384));check('complete_relative_coupling',eta2<1-kappa)
# A general symbolic identity is proved analytically; this verifies a nonsymmetric-size
# rational block instance in addition to the source's one-dimensional example.
Ab=[[F(3),F(1)],[F(1),F(2)]];B=[[F(2),F(-1)],[F(1),F(3)],[F(-2),F(1)]];Cd=[F(4),F(5),F(7)]
ell=[F(2),F(-3)];h=[F(1,2),F(-2,3),F(4,5)]
bell=[sum(B[i][j]*ell[j] for j in range(2)) for i in range(3)]
q=sum(ell[i]*Ab[i][j]*ell[j] for i in range(2) for j in range(2))+2*sum(bell[i]*h[i] for i in range(3))+sum(Cd[i]*h[i]**2 for i in range(3))
s=sum(ell[i]*Ab[i][j]*ell[j] for i in range(2) for j in range(2))-sum(bell[i]**2/Cd[i] for i in range(3))
res=[bell[i]+Cd[i]*h[i] for i in range(3)]
check('independent_2_by_3_block_identity',q-sum(res[i]**2/Cd[i] for i in range(3))==s)
out={'status':'PASS','checks':checks,'input_sha256':{n:hashlib.sha256((S/n).read_bytes()).hexdigest() for n in ['INPUT5_CERTIFICATE.json','INPUT5_MATRIX_CERTIFICATE.json','DERIVATIVE_RATIONAL_MATRIX.json']},'derivative_row_radius':str(rho),'leading_principal_minors':[str(t) for t in mins],'derived_LDL_pivots':[str(t) for t in piv],'Schur_floor':str(schur),'attachment_floor':str(mu),'kappa':str(kappa),'relative_coupling_eta_squared':str(eta2),'scope':'Exact exported-matrix containment and sufficient-matrix sign, rational constants, and a finite test of the analytically proved block identity; not a new theta integration or proof of sector membership.'}
(P/'INDEPENDENT_FRACTION_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:',len(checks),'exact checks; all five determinant-ratio pivots >14000.')
