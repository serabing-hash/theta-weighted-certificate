#!/usr/bin/env python3
"""Independent exact rational audit of exported balls, determinant signs and Schur bounds.

Uses only the Python standard library. Does not prove the analytic enclosures.
"""
from fractions import Fraction as F
from pathlib import Path
import json, re

p=Path(__file__).resolve().parent
data=json.loads((p/'MATRIX_CERTIFICATE.json').read_text())
base=json.loads((p/'CERTIFICATE.json').read_text())
ledger=json.loads((p/'RATIONAL_MATRIX.json').read_text())

def interval(s):
    s=s.strip()
    if s.startswith('['):
        m,r=s[1:-1].split(' +/- ')
        return F(m)-F(r),F(m)+F(r)
    return F(s),F(s)

def matrix_boxes(rows):return [[interval(s) for s in row] for row in rows]
def bounding_matrix(E,sign):
    n=len(E)
    assert all(E[i][j]==E[j][i] for i in range(n) for j in range(n))
    rho=max(sum((hi-lo)/2 for lo,hi in row) for row in E)
    return [[sum(E[i][j])/2+(sign*rho if i==j else 0) for j in range(n)] for i in range(n)],rho
def det(A):
    B=[row[:] for row in A];value=F(1)
    for k in range(len(B)):
        if not B[k][k]:
            j=next(j for j in range(k+1,len(B)) if B[j][k])
            B[j],B[k]=B[k],B[j];value=-value
        pivot=B[k][k];value*=pivot
        for i in range(k+1,len(B)):
            f=B[i][k]/pivot
            for j in range(k+1,len(B)):B[i][j]-=f*B[k][j]
    return value
def principal(A,k):return [row[:k] for row in A[:k]]
def schur(A):return det(A)/det(principal(A,len(A)-1))

E=matrix_boxes(data['certifying_matrix']);D=int(ledger['scale'])
export_checks=[]
for i in range(5):
    for j in range(5):
        lo,hi=map(int,ledger['entries'][i][j]);a,b=E[i][j]
        assert F(lo,D)<=a<=b<=F(hi,D),(i,j)
        export_checks.append([i,j,True])
LE=[[(F(int(lo),D),F(int(hi),D)) for lo,hi in row] for row in ledger['entries']]
M,rho=bounding_matrix(LE,-1)
minors=[F(1)]+[det(principal(M,k)) for k in range(1,6)]
assert all(x>0 for x in minors)
pivots=[minors[i+1]/minors[i] for i in range(5)]
assert all(x>y for x,y in zip(pivots,map(F,['0.028','0.031','0.007','0.007','0.0005'])))
s=pivots[-1];assert s>F('0.000528')
G=matrix_boxes(base['G']);Gl,gr=bounding_matrix(G,-1);Gu,_=bounding_matrix(G,1)
assert all(det(principal(Gl,k))>0 for k in range(1,6))
gu=schur(Gu);assert gu>0 and gu<F('0.019467')
assert s/gu>F(27,1000)

# Compare the old scalar sufficient matrix at precisely the new target.
SC=matrix_boxes(base['certifying_matrix']);shift=F(1,25)-F(1,32)
SC=[[(SC[i][j][0]-shift*G[i][j][1],SC[i][j][1]-shift*G[i][j][0]) for j in range(5)] for i in range(5)]
Sl,sr=bounding_matrix(SC,-1);Su,_=bounding_matrix(SC,1)
assert all(det(principal(Sl,k))>0 for k in range(1,5))
ss=schur(Su);assert ss<F('-0.000949')
kv=interval(base['K_V_squared_upper'])[1];assert kv<F(75)
out={'status':'PASS','method':'Exact Fraction Gaussian determinants, distinct from supplied LDL implementation',
     'row_radius':str(rho),'leading_principal_minors':[str(x) for x in minors[1:]],
     'pivot_ratios':[str(x) for x in pivots],'Schur_lower':str(s),'Schur_lower_decimal':float(s),
     'Gram_innovation_upper':str(gu),'Gram_innovation_upper_decimal':float(gu),
     'normalized_Schur_lower':str(s/gu),'normalized_Schur_lower_decimal':float(s/gu),
     'scalar_Schur_upper':str(ss),'scalar_Schur_upper_decimal':float(ss),
     'K_V_squared_upper_below_75':True,'all_25_decimal_balls_inside_rational_ledger':export_checks,
     'scope':'Finite five-function sufficient-matrix signs and quotient bounds only. No analytic quadrature, all-dimension positivity or RH claim.'}
(p/'INDEPENDENT_FRACTION_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: exact determinant signs, Schur > 0.000528, quotient reserve > 0.027, scalar Schur < -0.000949, K5 squared < 75.')
