#!/usr/bin/env python3
"""Standard-library exact rational sign check of the exported interval matrices.
It checks matrix signs, not the analytic origins of the intervals.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
raw=(p/'RATIONAL_MATRICES.json').read_bytes();data=json.loads(raw)
results={}
floors={'source':[F(30,1000),F(32,1000),F(8,1000),F(11,1000),F(14,10000),F(4,10000)],
        'fixed_split':[F(30,1000),F(32,1000),F(8,1000),F(11,1000),F(14,10000),F(5,10000)],
        'matrix_graph':[F(30,1000),F(32,1000),F(8,1000),F(10,1000),F(14,10000),F(1,5000)],
        'derivative':[F(127000),F(108000),F(56000),F(61000),F(14000),F(20000)]}
for key,ledger in data.items():
 scale=int(ledger['scale'])
 E=[[(F(int(lo),scale),F(int(hi),scale)) for lo,hi in row] for row in ledger['entries']]
 n=len(E);assert n==6
 assert all(E[i][j]==E[j][i] for i in range(n) for j in range(n))
 mid=[[(lo+hi)/2 for lo,hi in row] for row in E]
 rad=[[(hi-lo)/2 for lo,hi in row] for row in E]
 rho=max(map(sum,rad))
 A=[[mid[i][j]-(rho if i==j else 0) for j in range(n)] for i in range(n)]
 L=[[F(0) for _ in range(n)] for _ in range(n)];ds=[]
 for i in range(n):
  L[i][i]=F(1)
  d=A[i][i]-sum(L[i][k]**2*ds[k] for k in range(i));assert d>floors[key][i]
  ds.append(d)
  for j in range(i+1,n):L[j][i]=(A[j][i]-sum(L[j][k]*L[i][k]*ds[k] for k in range(i)))/d
 results[key]={'status':'PASS','radius_row_sum':str(rho),'pivots':[str(d) for d in ds],
               'strict_pivot_floors':[str(v) for v in floors[key]]}
 print('PASS:',key,'exact rational pivot floors',results[key]['strict_pivot_floors'])
R=2**18;d=36;g=R-d
s=F(1,40)-F(52**2,g);assert s>F(1,70)
a=F(1,50)/(1+2*F(d,g)**2);assert a>F(1,51) and F(g,2)>F(1,51)
kappa=F(d,R);eta=F(50*d*d,R);assert eta<1-kappa
out={'status':'PASS','ledger_sha256':hashlib.sha256(raw).hexdigest(),
     'matrices':results,'scalar_Schur_floor_exact':str(s),'matrix_Schur_floor':'1/50','whole_floor_exact':str(a),
     'kappa':str(kappa),'relative_complete_coupling':str(eta),
     'scope':'Four enclosing six-by-six sufficient matrix signs and final rational inequalities; analytic tails are separate premises.'}
(p/'EXACT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: fixed split',R,'Schur >= 1/50; complete attachment >= 1/51')
