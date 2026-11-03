#!/usr/bin/env python3
"""Exact rational checks for derivative matrix, constants and structural identity."""
from fractions import Fraction as F
from pathlib import Path
import json
p=Path(__file__).resolve().parent
x=json.loads((p/'DERIVATIVE_RATIONAL_MATRIX.json').read_text());scale=int(x['scale'])
E=[[(F(int(lo),scale),F(int(hi),scale)) for lo,hi in row] for row in x['entries']]
n=len(E);assert n==5
assert all(E[i][j]==E[j][i] for i in range(n) for j in range(n))
mid=[[(a+b)/2 for a,b in row] for row in E];rad=[[(b-a)/2 for a,b in row] for row in E]
rho=max(map(sum,rad));A=[[mid[i][j]-(rho if i==j else 0) for j in range(n)] for i in range(n)]
L=[[F(0) for j in range(n)] for i in range(n)];piv=[]
for i in range(n):
    L[i][i]=F(1);z=A[i][i]-sum(L[i][k]**2*piv[k] for k in range(i));assert z>0;piv.append(z)
    for j in range(i+1,n):L[j][i]=(A[j][i]-sum(L[j][k]*L[i][k]*piv[k] for k in range(i)))/z
R=2**18;d=36;g=R-d
s=F(1,25)-F(52**2,g);assert s>F(1,35)
mu=F(1,35)/(1+2*F(d,g)**2);assert mu>F(1,36) and F(g,2)>F(1,36)
kappa=F(d,R);eta_squared=F(35*d*d,R);assert eta_squared<1-kappa
# Synthetic example only: Gamma=diag(1,4), D=[[2,1],[1,0]], v=(1,1).
# q(v)=1, but Schur on its low projection is -5/4.
qv=F(1);C=F(4);residual=F(3);schur=F(-5,4)
assert qv-residual**2/C==schur
result={'status':'PASS','derivative_row_radius':str(rho),'derivative_LDL_pivots':[str(v) for v in piv],
 'Schur_floor_exact':str(s),'attachment_floor_exact':str(mu),'kappa':str(kappa),
 'relative_coupling_eta_squared':str(eta_squared),'one_minus_kappa':str(1-kappa),
 'synthetic_projection_example':{'qv':str(qv),'Schur':str(schur),'residual':str(residual)},
 'scope':'Derivative sufficient-matrix sign, scalar transfer inequalities and one synthetic identity; no new full theta quadrature.'}
(p/'RATIONAL_TRANSFER_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: derivative matrix and all rational transfer inequalities.')
print('Schur floor',s,'>',F(1,35),'whole attachment',mu,'>',F(1,36))
print('kappa',kappa,'relative coupling',eta_squared,'<',1-kappa)
