#!/usr/bin/env python3
"""New graph-norm bound from frozen five-function Gram certificates.
No theta integral, spectral projection, or high response is regenerated.
"""
from flint import arb,arb_mat,ctx
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ctx.prec=160
p=Path(__file__).resolve().parent
hashes={'INPUT5_CERTIFICATE.json':'0b3b7cb219fd6706ede678887e09fe29cf502ca0c151a2d8aff64e45827f452b',
        'INPUT5_MATRIX_CERTIFICATE.json':'5b4f2e77f69aac2602719efaf2b9cfc0c6466caaf18a07c79178c5ddcde7dff5'}
for n,h in hashes.items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h
x=json.loads((p/'INPUT5_CERTIFICATE.json').read_text());y=json.loads((p/'INPUT5_MATRIX_CERTIFICATE.json').read_text())
assert x['status'].startswith('PASS') and y['floor']=='1/25'
G=arb_mat([[arb(s) for s in row] for row in x['G']]);D=arb_mat([[arb(s) for s in row] for row in y['D2_Gram']])
n=5;lam=2**20;M=lam*G-D
L=[[arb(0) for j in range(n)] for i in range(n)];piv=[]
for i in range(n):
    L[i][i]=arb(1)
    a=M[i,i]-sum((L[i][k]**2*piv[k] for k in range(i)),arb(0))
    assert a>0;piv.append(a)
    for j in range(i+1,n):L[j][i]=(M[j,i]-sum((L[j][k]*L[i][k]*piv[k] for k in range(i)),arb(0)))/a
pi=arb.pi();z=(-pi/2).exp()
weight_sup=42*(-pi).exp();assert weight_sup<2
c=pi.log()-(arb(1)/4).digamma()
pnorm=84*z**2*(4/(1-z)+4*z/(1-z)**2+z*(1+z)/(1-z)**3)
dnorm=2*c+pnorm
assert dnorm<arb(143)/4
k=arb(40);a=4+(1+4*k*k).log()/2-2*k*k/(1+4*k*k);b=2/(1+4*k*k)
gamma_norm=arb(2).sqrt()*(a*arb(2).sqrt()+b*arb(lam).sqrt())
assert a>0 and gamma_norm<arb(65)/4
assert gamma_norm+dnorm<52
R=2**18;d=36;gap=R-d;beta=52**2
schur_floor=F(1,25)-F(beta,gap)
assert schur_floor>F(1,35)
whole_floor=F(1,35)/(1+2*F(d,gap)**2)
assert whole_floor>F(1,36) and F(gap,2)>F(1,36)
scale=10**10
entries=[[[str(int((M[i,j].lower()*scale).floor().fmpz())),str(int((M[i,j].upper()*scale).ceil().fmpz()))] for j in range(n)] for i in range(n)]
(p/'DERIVATIVE_RATIONAL_MATRIX.json').write_text(json.dumps({'scale':str(scale),'entries':entries,'meaning':'Encloses 2^20 G - D2; D2 is the actual second-derivative Gram.'},indent=2)+'\n')
result={'status':'PASS: graph-norm constants and finite derivative comparison; sector inputs remain conditional',
'input_sha256':hashes,'D2_relative_upper':str(lam),'weight_sup_upper':str(weight_sup),'complete_Db_norm_upper':str(dnorm),
'gamma_tangent_a':str(a),'gamma_tangent_b':str(b),'TGamma_norm_on_V5_upper':str(gamma_norm),
'L_norm_on_V5_upper':'52','beta':'2704','Gamma_spectral_R':str(R),'d':'36','high_gap':str(gap),
'Schur_projected_floor_exact':str(schur_floor),'Schur_projected_floor_rounded':'1/35',
'full_high_attachment_floor_exact':str(whole_floor),'full_high_attachment_floor_rounded':'1/36',
'derivative_LDL_pivots':[str(a) for a in piv],
'not_computed':['spectral projections','high response inverse','remaining low Schur signs','new theta integrals']}
(p/'GRAPH_BOUND.json').write_text(json.dumps(result,indent=2)+'\n')
for k,v in result.items():
    if k not in ['input_sha256','derivative_LDL_pivots']:print(k,v)
