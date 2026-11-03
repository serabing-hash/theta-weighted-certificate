#!/usr/bin/env python3
"""Ball-arithmetic certificate for six actual theta zero functions, reusing the saved five-zero integral block.

Requires python-flint 0.9.0. No floating eigenvalue is a sign premise.
All finite Gamma labels below are positive subforms of the full energy.
"""
from flint import arb, acb, arb_mat, ctx
from pathlib import Path
import flint, json, time, math

ctx.prec = 160
START=time.time()
OUT=Path(__file__).resolve().parent
DIM=6; JTHETA=8; R=arb(2); CELLS=8192; LABELS=128; PRIME_MAX=32
pi=arb.pi(); zero=arb(0); one=arb(1)
import hashlib
input_bytes=(OUT/'INPUT5_CERTIFICATE.json').read_bytes()
assert hashlib.sha256(input_bytes).hexdigest()=="0b3b7cb219fd6706ede678887e09fe29cf502ca0c151a2d8aff64e45827f452b"
INPUT=json.loads(input_bytes)
assert INPUT['settings']['cells']==CELLS and INPUT['settings']['gamma_labels']==LABELS
assert INPUT['settings']['prime_max']==PRIME_MAX
assert INPUT['settings']['theta_terms']==JTHETA and arb(INPUT['settings']['radius'])==R
assert len(INPUT['G'])==DIM-1 and len(INPUT['zeros'])==DIM-1

tiny=arb('1e-90')
checks={}
def require(name, truth):
    checks[name]=bool(truth)
    if not truth: raise AssertionError(name)
def announce(msg):
    print(f'{time.time()-START:.2f}s {msg}',flush=True)
def ball(x): return str(x)
def matrix_json(A): return [[ball(A[i,j]) for j in range(A.ncols())] for i in range(A.nrows())]
def inflate(x,rad): return x + arb(0,rad.upper())
def up(x): return x.upper()
def upper_gamma(m0,m1):
    # Increasing in both nonnegative arguments.
    return 4*m0 + m0/2*(1+4*m1/m0).log()
def integral(f,a,b):
    z=acb.integral(f,acb(a),acb(b),abs_tol=arb('1e-23'),rel_tol=arb('1e-23'),
                   eval_limit=300000,depth_limit=40)
    require('integral_finite_'+str(len(checks)),z.is_finite())
    require('integral_real_'+str(len(checks)),z.imag.contains(0))
    return z.real

def Wparts(x,order=0):
    """Meromorphic finite theta expression; caller uses the nonnegative branch."""
    s=1/(1+(-x).exp()); ex=(2*x).exp()
    n0=0; n1=0; n2=0
    for j in range(1,JTHETA+1):
        t=pi*(j*j)*ex; E=(-t).exp(); t2=t*t
        n0+=(4*t2-6*t)*E
        if order>=1: n1+=(-8*t2*t+28*t2-12*t)*E
        if order>=2: n2+=(16*t2*t2-104*t2*t+136*t2-24*t)*E
    if order==0:return s*n0
    sp=s*(1-s)
    if order==1:return s*n1+sp*n0
    return s*n2+2*sp*n1+sp*(1-2*s)*n0

def exp_moment(n,a,E):
    # Exact expression for int_E^infty t^n exp(-a*t) dt.
    z=(-a*E).exp(); value=z/a
    for k in range(1,n+1):value=z*E**k/a+k*value/a
    return value

def von_mangoldt(n):
    for p in range(2,n+1):
        if n%p==0:
            k=n
            while k%p==0:k//=p
            return arb(p).log() if k==1 else zero
    return zero

def ldlt(A,label):
    n=A.nrows(); L=[[arb(0) for j in range(n)] for i in range(n)]; ds=[]
    for i in range(n):
        L[i][i]=arb(1)
        d=A[i,i]-sum((L[i][k]**2*ds[k] for k in range(i)),arb(0))
        require(label+'_pivot_'+str(i),d>0);ds.append(d)
        for j in range(i+1,n):
            L[j][i]=(A[j,i]-sum((L[j][k]*L[i][k]*ds[k] for k in range(i)),arb(0)))/d
    return ds

require('theta_omission_bound',20000*arb(9)**8*arb(-243).exp()<tiny)
# j>=9: ratio of j^8 exp(-3j^2) is bounded by (10/9)^8 exp(-57)<1/2.
require('theta_omission_ratio',(arb(10)/9)**8*arb(-57).exp()<arb(1)/2)
roots=acb.zeta_zeros(1,DIM)
for i,z in enumerate(roots):
    require('root_real_half_'+str(i),z.real==arb(1)/2)
    require('root_positive_'+str(i),z.imag>0)
T=[z.imag for z in roots]
announce('rigorous zero balls: '+', '.join(str(t) for t in T))

E=(2*R).exp()
# Envelopes: |W^(k)(r)| <= C_k exp((4+2k)r-pi exp(2r)).
# The elementary series checks below pay their omitted j terms as well.
sum4=sum((arb(j)**4*(-pi*(j*j-1)).exp() for j in range(1,9)),zero)
sum6=sum((arb(j)**6*(-pi*(j*j-1)).exp() for j in range(1,9)),zero)
sum8=sum((arb(j)**8*(-pi*(j*j-1)).exp() for j in range(1,9)),zero)
series_tail=arb('1e-90')
require('envelope_C0',4*pi**2*(sum4+series_tail)<42)
require('envelope_C1',22*pi**3*(sum6+series_tail)<700)
require('envelope_C2',80*pi**4*(sum8+series_tail)<10000)
Ck=[42,700,10000]
tailW=[(Ck[k]**2*exp_moment(3+2*k,2*pi,E)).sqrt() for k in range(3)]
tailG=42*exp_moment(1,pi,E)
Wboundary=42*E**2*(-pi*E).exp()

Dnorm=[]
for k in range(3):
    I=2*integral(lambda x,a:Wparts(x,k)**2,zero,R)
    Dnorm.append(up(I.sqrt()+2*tiny+tailW[k]))
announce('full W derivative norm upper bounds: '+str(Dnorm))
G=arb_mat(DIM,DIM); H=arb_mat(DIM,DIM)
for i in range(DIM):
    for j in range(i,DIM):
        if j<5:
            G[i,j]=G[j,i]=arb(INPUT['G'][i][j])
            H[i,j]=H[j,i]=arb(INPUT['H'][i][j])
            continue
        gi=2*integral(lambda x,a:Wparts(x)*(T[i]*x).cos()*(T[j]*x).cos(),zero,R)
        hi=2*integral(lambda x,a:Wparts(x)**2*(T[i]*x).cos()*(T[j]*x).cos(),zero,R)
        G[i,j]=G[j,i]=inflate(gi,4*tiny+tailG)
        # W,W8 <42 suffices for the finite-interval difference.
        H[i,j]=H[j,i]=inflate(hi,4*tiny*(84+tiny)+tailW[0]**2)
G_pivots=ldlt(G,'true_Gram')
Ginv=G.inv()
KV2=up(Dnorm[0]**2*sum((Ginv[i,i].sqrt() for i in range(DIM)),zero)**2)
announce('weighted Gram certified; K_V^2 upper '+str(KV2))

P=arb_mat(DIM,DIM)
for i in range(5):
    for j in range(5): P[i,j]=arb(INPUT['P_head'][i][j])
prime_powers=[]
for n in range(2,PRIME_MAX+1):
    vm=von_mangoldt(n)
    if vm==0:continue
    prime_powers.append(n); s=arb(n).log()/2; weight=vm/arb(n).sqrt()
    for i in range(DIM):
        for j in range(i,DIM):
            if j<5:continue
            def make(sign):
                def fn(y,analytic):
                    plus=y+s; minus=y-s
                    w=Wparts(plus)*Wparts(sign*minus)
                    return w*((T[i]*plus).cos()*(T[j]*minus).cos()+
                              (T[j]*plus).cos()*(T[i]*minus).cos())
                return fn
            cij=integral(make(-1),zero,s)+integral(make(1),s,R)
            # Both y tails: CS, with one argument outside |x|>R.
            cij=inflate(cij,2*Dnorm[0]*tailW[0]+8*tiny*(84+tiny))
            P[i,j]+=2*weight*cij
            if j!=i:P[j,i]=P[i,j]
    announce('prime power '+str(n)+' included')
# For n>=33, sqrt(n) log(n)<=n^2. Sum the complete integer tail exactly.
z=(-pi/2).exp(); m=PRIME_MAX+1
prime_tail=up(84*z**m*(arb(m*m)/(1-z)+2*m*z/(1-z)**2+z*(1+z)/(1-z)**3))

data={"precision_bits":ctx.prec,"python_flint":flint.__version__,"zeros":[str(z) for z in roots],
      "settings":{"theta_terms":JTHETA,"radius":str(R),"cells":CELLS,
                  "gamma_labels":LABELS,"prime_max":PRIME_MAX},
      "G":matrix_json(G),"H":matrix_json(H),"P_head":matrix_json(P),
      "W_derivative_norm_upper":[str(x) for x in Dnorm],"K_V_squared_upper":str(KV2),
      "prime_powers":prime_powers,"prime_tail_operator_upper":str(prime_tail)}
(OUT/'quadrature_checkpoint.json').write_text(json.dumps(data,indent=2)+'\n')
announce('finite integrals and full prime tail complete')

# Interpolate actual u_i nodal values using enclosing balls. Endpoints are zero.
h=2*R/CELLS
Y=[]
for k in range(CELLS+1):
    if k in (0,CELLS):Y.append([arb(0) for j in range(DIM)]);continue
    x=-R+k*h; wx=inflate(Wparts(abs(x)),tiny)
    Y.append([wx*(t*x).cos() for t in T])
slopes=[[(Y[k+1][i]-Y[k][i])/h for i in range(DIM)] for k in range(CELLS)]
S0=[[sum((row[i]*row[j] for row in slopes),zero) for j in range(DIM)] for i in range(DIM)]
mass_trace=zero
for k in range(CELLS):
    mass_trace+=h/3*sum((Y[k][i]**2+Y[k][i]*Y[k+1][i]+Y[k+1][i]**2 for i in range(DIM)),zero)
derivative_trace=h*sum((S0[i][i] for i in range(DIM)),zero)
gamma_F=up(upper_gamma(up(mass_trace),up(derivative_trace)))
err_gamma=zero
err_list=[]
for t in T:
    d2=up(Dnorm[2]+2*t.abs_upper()*Dnorm[1]+t.abs_upper()**2*Dnorm[0])
    e0=up(h**2/pi**2*d2+(2*h/3).sqrt()*Wboundary+tailW[0])
    e1=up(h/pi*d2+(2/h).sqrt()*Wboundary+tailW[1]+t.abs_upper()*tailW[0])
    eg=up(upper_gamma(e0**2,e1**2));err_gamma+=eg
    err_list.append({"D2_upper":str(d2),"L2_error_upper":str(e0),"H1_seminorm_error_upper":str(e1),"Gamma_error_upper":str(eg)})
gamma_debit=up(2*(gamma_F*err_gamma).sqrt())
announce('Gamma interpolation debit upper '+str(gamma_debit))

Gamma=arb_mat(DIM,DIM)
for i in range(5):
    for j in range(5): Gamma[i,j]=arb(INPUT['Gamma_positive_truncation'][i][j])
pairs=[(i,j) for i in range(DIM) for j in range(i,DIM) if j>=5]
for label in range(LABELS):
    a=arb(2*label)+arb(1)/2; r=(-a*h).exp()
    off=(1-r)**2/a**2
    diag=2*(h/a-(1-r)/a**2)
    past=[arb(0) for i in range(DIM)]
    cross=[arb(0) for ij in pairs]
    for row in slopes:
        for zidx,(i,j) in enumerate(pairs):
            cross[zidx]+=row[i]*past[j]+past[i]*row[j]
        past=[r*past[i]+row[i] for i in range(DIM)]
    for zidx,(i,j) in enumerate(pairs):
        Gamma[i,j]+=(diag*S0[i][j]+off*cross[zidx])/a**2
        if j!=i:Gamma[j,i]=Gamma[i,j]
    if (label+1)%16==0:announce('positive Gamma labels '+str(label+1)+'/'+str(LABELS))

data.update({"Gamma_positive_truncation":matrix_json(Gamma),
             "interpolation_errors":err_list,"Gamma_F_trace_upper":str(gamma_F),
             "Gamma_error_trace_upper":str(err_gamma),"Gamma_debit_upper":str(gamma_debit),
             "Gram_LDL_pivots":[str(d) for d in G_pivots],
             "input5_sha256":hashlib.sha256(input_bytes).hexdigest(),
             "checks":checks,"elapsed_seconds":time.time()-START,
             "status":"ENCLOSED: six actual zero functions; sign checked separately"})
(OUT/'CERTIFICATE.json').write_text(json.dumps(data,indent=2)+'\n')
announce('ENCLOSED: six-function matrices including all prime and spatial errors')
