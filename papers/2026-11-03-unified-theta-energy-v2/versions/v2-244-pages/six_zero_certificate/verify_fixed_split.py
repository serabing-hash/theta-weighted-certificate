#!/usr/bin/env python3
"""Certify six-source forms and full graph transfer at a FIXED Gamma split.
Actual projections and the high inverse are used analytically, not sampled.
"""
from flint import arb,arb_mat,ctx
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
ctx.prec=160
p=Path(__file__).resolve().parent
x=json.loads((p/'CERTIFICATE.json').read_text())
y=json.loads((p/'MATRIX_ENCLOSURE.json').read_text())
assert y['input_sha256']==hashlib.sha256((p/'CERTIFICATE.json').read_bytes()).hexdigest()
n=6
G=arb_mat([[arb(s) for s in row] for row in x['G']])
H=arb_mat([[arb(s) for s in row] for row in x['H']])
D2=arb_mat([[arb(s) for s in row] for row in y['D2_Gram']])
Qlo=arb_mat([[arb(s) for s in row] for row in y['sufficient_q0_matrix']])
checks={}
def require(k,v):
 checks[k]=bool(v)
 if not v:raise AssertionError(k)
def ldlt(A,key):
 L=[[arb(0) for _ in range(n)] for _ in range(n)];ds=[]
 for i in range(n):
  L[i][i]=arb(1)
  d=A[i,i]-sum((L[i][k]**2*ds[k] for k in range(i)),arb(0))
  require(key+'_pivot_'+str(i),d>0);ds.append(d)
  for j in range(i+1,n):L[j][i]=(A[j,i]-sum((L[j][k]*L[i][k]*ds[k] for k in range(i)),arb(0)))/d
 return ds

def schur(A):
 H=arb_mat([[A[i,j] for j in range(n-1)] for i in range(n-1)])
 b=arb_mat([[A[i,n-1]] for i in range(n-1)])
 diagonal=A[n-1,n-1];response=(b.transpose()*H.inv()*b)[0,0]
 return {'diagonal':str(diagonal),'response':str(response),'remainder':str(diagonal-response)}

def export(A,scale,label):
 entries=[[[str(int((A[i,j].lower()*scale).floor().fmpz())),str(int((A[i,j].upper()*scale).ceil().fmpz()))] for j in range(n)] for i in range(n)]
 return {'scale':str(scale),'entries':entries,'meaning':label}

R=2**18;d=36;gap=R-d;lam=2**20;beta=52**2
alpha=F(1,40);s=F(1,70);whole=F(1,71)
source=Qlo-arb(1)/40*G
Dcomp=lam*G-D2
# This is a sufficient matrix in the RAW source coefficient coordinates.
# Its positivity gives S[Pv] >= (1/70)||v||_H^2 >= (1/70)||Pv||_H^2.
low=Qlo-(arb(beta)/gap+arb(1)/70)*G
matrices={'source':source,'derivative':Dcomp,'fixed_split':low}
pivots={k:[str(v) for v in ldlt(A,k)] for k,A in matrices.items()}
pi=arb.pi();z=(-pi/2).exp();weight_sup=42*(-pi).exp()
require('weight_sup_lt_2',weight_sup<2)
c=pi.log()-(arb(1)/4).digamma()
pnorm=84*z*z*(4/(1-z)+4*z/(1-z)**2+z*(1+z)/(1-z)**3)
dnorm=2*c+pnorm
require('full_D_norm_lt_143_over_4',dnorm<arb(143)/4)
k=arb(40);a=4+(1+4*k*k).log()/2-2*k*k/(1+4*k*k);b=2/(1+4*k*k)
tnorm=arb(2).sqrt()*(a*arb(2).sqrt()+b*arb(lam).sqrt())
require('full_Gamma_row_lt_65_over_4',tnorm<arb(65)/4)
require('full_L_row_lt_52',tnorm+dnorm<52)
exact_s=alpha-F(beta,gap)
require('transferred_s_exceeds_1_over_70',exact_s>s)
# Preserve the physical and derivative Gram correlations in the complete row.
# Young parameters theta=8 and zeta=1/16, M<=2 and ||D_b||<=36 give this matrix.
row_majorant=arb(153)/8*a*a*H+306*b*b*D2+1458*G
matrix_graph=Qlo-row_majorant/gap-arb(1)/50*G
matrices['matrix_graph']=matrix_graph
pivots['matrix_graph']=[str(v) for v in ldlt(matrix_graph,'matrix_graph')]
matrix_graph_s=schur(matrix_graph)
require('matrix_graph_extension_schur_exceeds_1_over_5000',arb(matrix_graph_s['remainder'])>arb(1)/5000)
s_matrix=F(1,50);whole_matrix=F(1,51)
attachment=s_matrix/(1+2*F(d,gap)**2)
require('attachment_exceeds_1_over_51',attachment>whole_matrix and F(gap,2)>whole_matrix)
kappa=F(d,R);coupling=F(d*d,R)/s_matrix
require('relative_full_coupling',coupling<1-kappa)
G5=arb_mat([[G[i,j] for j in range(5)] for i in range(5)])
g5=arb_mat([[G[i,5]] for i in range(5)])
innovation=G[5,5]-(g5.transpose()*G5.inv()*g5)[0,0]
require('sixth_true_Gram_innovation_positive',innovation>0)
source_s=schur(source);low_s=schur(low)
require('source_schur_exceeds_4_over_10000',arb(source_s['remainder'])>arb(4)/10000)
require('fixed_split_schur_exceeds_5_over_10000',arb(low_s['remainder'])>arb(5)/10000)
# Record failure of a stronger sufficient comparison, not failure of q0 itself.
comparison=schur(Qlo-arb(1)/25*G)
require('stronger_sufficient_comparison_negative',arb(comparison['remainder'])<0)
ledger={k:export(A,10**10 if k=='derivative' else 10**18,
  {'source':'Q_lower - G/40','derivative':'2^20 G - D2','fixed_split':'Q_lower - (2704/262108 + 1/70) G','matrix_graph':'Q_lower - H_row/262108 - G/50'}[k]) for k,A in matrices.items()}
(p/'RATIONAL_MATRICES.json').write_text(json.dumps(ledger,indent=2)+'\n')
result={'status':'PASS: six projected low directions plus the complete Gamma high form sector; not all low directions',
 'inputs':{f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['CERTIFICATE.json','MATRIX_ENCLOSURE.json','INPUT5_CERTIFICATE.json','INPUT5_MATRIX_CERTIFICATE.json']},
 'dimension':n,'source_floor':str(alpha),'D2_relative_upper':str(lam),
 'weight_sup_upper':str(weight_sup),'full_D_norm_upper':str(dnorm),'gamma_tangent_a':str(a),'gamma_tangent_b':str(b),
 'full_Gamma_row_upper':str(tnorm),'full_L_row_upper':'52','beta':str(beta),
 'fixed_Gamma_spectral_R':str(R),'d':str(d),'high_gap':str(gap),
 'scalar_transfer_floor_exact':str(exact_s),'scalar_transfer_floor_rounded':str(s),
 'Schur_floor_certified':str(s_matrix),
 'full_row_Gram_majorant':[[str(row_majorant[i,j]) for j in range(n)] for i in range(n)],
 'matrix_graph_Schur':matrix_graph_s,
 'whole_floor_exact_from_rounded_Schur':str(attachment),'whole_floor_rounded':str(whole_matrix),
 'kappa':str(kappa),'relative_complete_coupling':str(coupling),
 'source_Schur':source_s,'fixed_split_Schur':low_s,'true_Gram_innovation':str(innovation),
 'source_Schur_over_innovation':str(arb(source_s['remainder'])/innovation),
 'fixed_split_Schur_over_innovation':str(arb(low_s['remainder'])/innovation),
 'failed_stronger_comparison_at_1_over_25':comparison,
 'LDL_pivots':pivots,'checks':checks,
 'analytic_inputs':['closed restricted Gamma form on K','raw exact zero functions belong to K','admitted full operator row','frozen enclosing first-five integral blocks'],
 'not_established':['positivity on all of P_R K','cofinal exhaustion by the six functions','all-size derivative or Schur bounds','global one-half bound','RH'],
 'not_numerically_constructed':['Gamma spectral projections','complete high response inverse']}
(p/'FIXED_SPLIT_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
for key,value in result.items():
 if key not in ['inputs','checks','LDL_pivots']:print(key,value)
