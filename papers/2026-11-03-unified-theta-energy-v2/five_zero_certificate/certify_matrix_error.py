#!/usr/bin/env python3
"""Matrix interpolation bound preserving derivative cross terms.
Requires python-flint==0.9.0. Reads the five-zero certificate unchanged.
"""
from flint import arb,acb,arb_mat,ctx
from pathlib import Path
import json,hashlib
ctx.prec=160
OUT=Path(__file__).resolve().parent
src=(OUT/'CERTIFICATE.json').read_bytes();d=json.loads(src)
n=5;pi=arb.pi();R=arb(2);h=arb(1)/2048;tiny=arb('1e-90')
roots=acb.zeta_zeros(1,n);T=[z.imag for z in roots]
assert d['settings']['cells']==8192 and d['settings']['gamma_labels']==128
assert d['settings']['theta_terms']==8 and d['settings']['prime_max']==32
checks={}
def require(k,v):
    checks[k]=bool(v)
    if not v:raise AssertionError(k)
def mat(key):return arb_mat([[arb(x) for x in row] for row in d[key]])
def matrix_json(A):return [[str(A[i,j]) for j in range(A.ncols())] for i in range(A.nrows())]
def up(x):return x.upper()
def inflate(x,r):return x+arb(0,r.upper())
def F(a,b):return 4*a+a/2*(1+4*b/a).log()
def Wparts(x,k):
    s=1/(1+(-x).exp());sp=s*(1-s);ex=(2*x).exp();N=[0,0,0]
    for j in range(1,9):
        t=pi*j*j*ex;e=(-t).exp()
        N[0]+=(4*t*t-6*t)*e
        N[1]+=(-8*t**3+28*t*t-12*t)*e
        N[2]+=(16*t**4-104*t**3+136*t*t-24*t)*e
    return [s*N[0],s*N[1]+sp*N[0],s*N[2]+2*sp*N[1]+sp*(1-2*s)*N[0]][k]
def second(x,t):return Wparts(x,2)*(t*x).cos()-2*t*Wparts(x,1)*(t*x).sin()-t*t*Wparts(x,0)*(t*x).cos()
def J(n,a,E):
    z=(-a*E).exp();v=z/a
    for k in range(1,n+1):v=z*E**k/a+k*v/a
    return v
E=(2*R).exp();tail=[c*J(3+2*k,2*pi,E).sqrt() for k,c in enumerate([42,700,10000])]
boundary=42*E**2*(-pi*E).exp()
N=[arb(x) for x in d['W_derivative_norm_upper']]
D=[up(N[2]+2*t*N[1]+t*t*N[0]) for t in T]
TD=[up(tail[2]+2*t*tail[1]+t*t*tail[0]) for t in T]
ED=[up(2*tiny*(1+2*t+t*t)) for t in T]
D2=arb_mat(n,n)
for i in range(n):
    for j in range(i,n):
        z=2*acb.integral(lambda x,analytic:second(x,T[i])*second(x,T[j]),0,R,
                        abs_tol=arb('1e-23'),rel_tol=arb('1e-23'),eval_limit=300000,depth_limit=40)
        require('D2_integral_finite_'+str((i,j)),z.is_finite())
        require('D2_integral_real_'+str((i,j)),z.imag.contains(0))
        rad=ED[i]*D[j]+ED[j]*D[i]+ED[i]*ED[j]+TD[i]*TD[j]
        D2[i,j]=D2[j,i]=inflate(z.real,rad)
chi=up(h**4/pi**4*(4+arb(1)/2*(1+4*pi*pi/h**2).log()))
tau=arb(0)
for t in T:
    r0=up((2*h/3).sqrt()*boundary+tail[0])
    r1=up((2/h).sqrt()*boundary+tail[1]+t*tail[0])
    tau+=up(F(r0*r0,r1*r1))
tau=up(tau);eta=arb(1)/1024;epsilon=arb(1)/16384
Err=(1+eta)*chi*D2
for i in range(n):Err[i,i]+=(1+1/eta)*tau
G=mat('G');H=mat('H');P=mat('P_head');Gamma=mat('Gamma_positive_truncation')
cGamma=pi.log()-(arb(1)/4).digamma();prime_tail=arb(d['prime_tail_operator_upper'])
Qlower=(1-epsilon)*Gamma-(1/epsilon-1)*Err-cGamma*H-P-prime_tail*G
floor=arb(1)/25
M=Qlower-floor*G
L=[[arb(0) for j in range(n)] for i in range(n)];pivots=[]
for i in range(n):
    L[i][i]=arb(1)
    p=M[i,i]-sum((L[i][k]**2*pivots[k] for k in range(i)),arb(0))
    require('shifted_pivot_'+str(i),p>0);pivots.append(p)
    for j in range(i+1,n):L[j][i]=(M[j,i]-sum((L[j][k]*L[i][k]*pivots[k] for k in range(i)),arb(0)))/p
A=arb_mat([[M[i,j] for j in range(4)] for i in range(4)])
b=arb_mat([[M[i,4]] for i in range(4)]);c=M[4,4]
cost=(b.transpose()*A.inv()*b)[0,0];s=c-cost
G4=arb_mat([[G[i,j] for j in range(4)] for i in range(4)]);g=arb_mat([[G[i,4]] for i in range(4)])
projection=G4.inv()*g;innovation=G[4,4]-(g.transpose()*projection)[0,0]
bp=b-A*projection;cp=c-2*(b.transpose()*projection)[0,0]+(projection.transpose()*A*projection)[0,0]
costp=(bp.transpose()*A.inv()*bp)[0,0]
require('Schur_positive',s>0);require('innovation_positive',innovation>0)
require('Schur_exceeds_1_over_2000',s>arb(1)/2000)
require('normalized_Schur_exceeds_27_over_1000',s/innovation>arb(27)/1000)
Mscalar=mat('certifying_matrix')-(floor-arb(1)/32)*G
Asc=arb_mat([[Mscalar[i,j] for j in range(4)] for i in range(4)])
bsc=arb_mat([[Mscalar[i,4]] for i in range(4)])
Ls=[[arb(0) for j in range(4)] for i in range(4)];ps=[]
for i in range(4):
    Ls[i][i]=arb(1)
    z=Asc[i,i]-sum((Ls[i][k]**2*ps[k] for k in range(i)),arb(0))
    require('scalar_shifted_low_pivot_'+str(i),z>0);ps.append(z)
    for j in range(i+1,4):Ls[j][i]=(Asc[j,i]-sum((Ls[j][k]*Ls[i][k]*ps[k] for k in range(i)),arb(0)))/z
scalar_s=Mscalar[4,4]-(bsc.transpose()*Asc.inv()*bsc)[0,0]
require('scalar_comparison_is_negative',scalar_s<0)
result={'precision_bits':ctx.prec,'input_sha256':hashlib.sha256(src).hexdigest(),
 'dimension':n,'floor':'1/25','epsilon':str(epsilon),'eta':str(eta),'chi_upper':str(chi),'boundary_Gamma_trace_upper':str(tau),
 'D2_Gram':matrix_json(D2),'Gamma_error_matrix_upper':matrix_json(Err),
 'sufficient_q0_matrix':matrix_json(Qlower),'certifying_matrix':matrix_json(M),
 'pivots':[str(x) for x in pivots],'shifted_diagonal':str(c),'shifted_response':str(cost),
 'shifted_Schur':str(s),'Gram_innovation_norm':str(innovation),'Schur_over_innovation':str(s/innovation),
 'orthogonalized_diagonal':str(cp),'orthogonalized_response':str(costp),
 'mean':'m(v_j)=Xi(gamma_j)/2=0 exactly; no numerical centering',
 'scalar_debit_comparison_Schur_at_1_over_25':str(scalar_s),'checks':checks,'status':'PASS: q0 >= (1/25) H norm squared on first five actual zero functions only'}
(OUT/'MATRIX_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
for k in ['chi_upper','boundary_Gamma_trace_upper','shifted_diagonal','shifted_response','shifted_Schur','Gram_innovation_norm','Schur_over_innovation','orthogonalized_diagonal','orthogonalized_response','status']:print(k,result[k])
