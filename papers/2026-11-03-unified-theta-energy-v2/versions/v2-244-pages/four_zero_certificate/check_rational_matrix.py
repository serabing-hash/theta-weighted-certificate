#!/usr/bin/env python3
"""Standard-library-only exact sign check; does not regenerate the analytic enclosures."""
from fractions import Fraction as F
from pathlib import Path
import json
p=Path(__file__).resolve().parent
data=json.loads((p/'RATIONAL_MATRIX.json').read_text());D=int(data['scale'])
E=[[(F(int(lo),D),F(int(hi),D)) for lo,hi in row] for row in data['entries']]
n=len(E)
assert all(E[i][j]==E[j][i] for i in range(n) for j in range(n))
mid=[[(lo+hi)/2 for lo,hi in row] for row in E]
rad=[[(hi-lo)/2 for lo,hi in row] for row in E]
rho=max(map(sum,rad))
A=[[mid[i][j]-(rho if i==j else 0) for j in range(n)] for i in range(n)]
L=[[F(0) for j in range(n)] for i in range(n)];ds=[]
for i in range(n):
    L[i][i]=F(1)
    d=A[i][i]-sum(L[i][k]**2*ds[k] for k in range(i))
    assert d>0,(i,d)
    ds.append(d)
    for j in range(i+1,n):
        L[j][i]=(A[j][i]-sum(L[j][k]*L[i][k]*ds[k] for k in range(i)))/d
floors=[F(29,1000),F(31,1000),F(7,1000),F(8,1000)]
assert all(d>floor for d,floor in zip(ds,floors))
out={'status':'PASS','row_radius':str(rho),'LDL_pivots':[str(d) for d in ds],
     'rational_pivot_floors':[str(d) for d in floors],
     'scope':'Exact rational positivity of the sufficient interval matrix only; '
             'analytic quadrature and tail correctness are verified separately.'}
(p/'RATIONAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: exact rational LDL, pivot floors',out['rational_pivot_floors'])
