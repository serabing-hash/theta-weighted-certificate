"""Exact fixed-integer/Fraction certificate checker; no numerical libraries. Python >=3.10."""
from fractions import Fraction as F
from math import comb,factorial,isqrt
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--out',default='certificate.json');p.add_argument('--bits',type=int,default=320);p.add_argument('--order',type=int,default=256);a=p.parse_args()
D=1<<a.bits; N=a.order
def fl(x):return x.numerator//x.denominator
def ce(x):return -fl(-x)
class I:
    def __init__(self,x=0,y=None):
        if y is None:y=x
        self.l=fl(F(x)*D);self.u=ce(F(y)*D)
    @staticmethod
    def raw(l,u):
        x=I();x.l=l;x.u=u;assert l<=u;return x
    def __add__(x,y):
        y=iv(y);return I.raw(x.l+y.l,x.u+y.u)
    __radd__=__add__
    def __neg__(x):return I.raw(-x.u,-x.l)
    def __sub__(x,y):return x+-iv(y)
    def __rsub__(x,y):return iv(y)+-x
    def __mul__(x,y):
        y=iv(y);g=[s*t for s in (x.l,x.u) for t in (y.l,y.u)];return I.raw(min(g)//D,-(-max(g)//D))
    __rmul__=__mul__
    def __truediv__(x,y):
        y=iv(y); assert not y.l<=0<=y.u
        return x*I(F(D,y.u),F(D,y.l))
    def __rtruediv__(x,y):return iv(y)/x
    def __pow__(x,k):
        assert isinstance(k,int) and k>=0
        if k==0:return I(1)
        c=x**(k//2);return c*c*x if k%2 else c*c
def iv(x):return x if isinstance(x,I) else I(x)
def bounds(x,places=32):
    vals=[]
    for n,r in [(x.l,ROUND_FLOOR),(x.u,ROUND_CEILING)]:
        with localcontext() as c:
            c.prec=places;c.rounding=r;vals.append(str(Decimal(n)/Decimal(D)))
    return vals
def sqrt_int(i):
    f=isqrt(i*D*D);return I.raw(f, f+(f*f!=i*D*D))
def atan_unit(k):
    m=90;r=F(1,k);s=sum((-1)**j*r**(2*j+1)/(2*j+1) for j in range(m))
    return I(s,s+r**(2*m+1)/(2*m+1))
def ln(x):
    x=iv(x);z=(x-1)/(x+1);assert 0<=z.l and z.u<D
    t=z;z2=z*z;s=I();m=410
    for j in range(m):s=s+t/(2*j+1);t=t*z2
    return 2*s+I.raw(0,(2*t/((2*m+1)*(1-z2))).u)
pi=16*atan_unit(5)-4*atan_unit(239)
logs={n:ln(I(n)) for n in (2,3,5,7)}; logs[4]=2*logs[2]
n0=1024; H=sum((F(1,i) for i in range(1,n0+1)),F())
b0=H-F(1,2*n0)+F(1,12*n0**2)-F(1,120*n0**4)+F(1,252*n0**6)
gamma=I(b0-F(1,240*n0**8),b0)-10*logs[2]
cg=ln(pi)+pi/2+gamma+3*logs[2]
# exp(-1) alternating series through degree100, then omitted negative term.
eu=sum(F((-1)**k,factorial(k)) for k in range(101)); e=I(eu-F(1,factorial(101)),eu)
Jout=I();ep=e;ratio=e**4
for m in range(50):
    Jout=Jout+ep/F(4*m+1,2);ep=ep*ratio
Jout=Jout+I(0,2*F(3,8)**201/(1-F(3,8)**4))
# Rational integrated Legendre construction, independent from the probe basis formula.
def poly(k):
    v0=[F((-1)**j*comb(k,j)*comb(k+j,j),2**j) for j in range(k+1)]
    h=[F() for _ in range(k+3)]
    for j,c in enumerate(v0):
        h[j]-=c; h[j+2]+=c/F(4*(j+1)*(j+2))
    return h
def weights(x,y):
    w=[F()]*(len(x)+len(y))
    for i,c in enumerate(x):
        for j,b in enumerate(y):
            m=i+j+1;w[m]+=c*b*F(2**m,m*comb(i+j,i))
    return w
d=12;K=4*d+5;h=[poly(2*j) for j in range(1,d+1)]
Harm=[F()];J=[I()];vs=[[F() for j in range(d)] for i in range(d)]
for m in range(1,K+1):Harm.append(Harm[-1]+F(1,m))
# D(2x)=.5 e^x/(sinh(2x)/(2x)). Rigorous bound on |s|=5/2 gives Taylor
# tail sup|D(s)-D_N(s)|<=50(4/5)^(N+1) on [0,2].
bn=[];cc=[F(4**j,factorial(2*j+1)) for j in range(N//2+1)]
for k in range(N+1):
    bn.append(F(1,2*factorial(k))-sum((cc[j]*bn[k-2*j] for j in range(1,k//2+1)),F()))
err=50*F(4,5)**(N+1)
for m in range(1,K+1):
    J.append(I(2*(bn[0]*Harm[m]+sum((bn[k]*(F(1,k)-F(1,k*comb(k+m,m))) for k in range(1,N+1)),F())))+2*Jout)
P=[[2*logs[2 if n==4 else n]/sqrt_int(n)*(1-logs[n]/2)**m for m in range(K+1)] for n in (2,3,4,5,7)]
g=[[F() for _ in range(d)] for _ in range(d)];Q=[[I() for _ in range(d)] for _ in range(d)]; wmat={}
for i in range(d):
    for j in range(i+1):
        w=wmat[i,j]=weights(h[i],h[j]);g[i][j]=g[j][i]=sum(w)
        vs[i][j]=vs[j][i]=sum(w[m]*Harm[m] for m in range(len(w)))
        q=sum((iv(c0)*(J[m]-sum((p0[m] for p0 in P),I())) for m,c0 in enumerate(w)), I())-cg*g[i][j]
        Q[i][j]=Q[j][i]=q
for i in range(d):
    assert vs[i][i]>0
    for j in range(i+1):
        delta=err*(vs[i][i]+vs[j][j]);Q[i][j]=Q[j][i]=Q[i][j]+I(-delta,delta)
# independent fixed rational (10^-8 grid) witness
ci=[51115584,-137278221,150680293,-89895696,31366529,-9136646,6352108,-5230840,2812355,-972178,210323,-22568]
coef=[F(j,10**8) for j in ci]; norm=sum(coef[i]*g[i][j]*coef[j] for i in range(d) for j in range(d))
val=sum((iv(coef[i]*coef[j])*Q[i][j] for i in range(d) for j in range(d)),I());rq=val/norm
assert F(rq.l,D)>F(1,10**11) and F(rq.u,D)<F(11,10**12)
# Loewner test Q - 10^-11 physical G positive on all real/complex coefficients.
A=[[Q[i][j]-iv(F(1,10**11)*g[i][j]) for j in range(d)] for i in range(d)]
def ildl(A):
    d=len(A);ll=[[I() for j in range(d)] for i in range(d)];piv=[]
    for i in range(d):
        t=A[i][i]-sum((ll[i][j]*ll[i][j]*piv[j] for j in range(i)),I())
        assert t.l>0, ('pivot not positive',i,bounds(t));piv.append(t)
        for k in range(i+1,d):
            ll[k][i]=(A[k][i]-sum((ll[k][j]*ll[i][j]*piv[j] for j in range(i)),I()))/t
    return [bounds(t) for t in piv]
def stable_ldl(T):
    size=len(T)
    mid=[[(t.l+t.u)//2 for t in row] for row in T]
    charges=[sum(max(mid[i][j]-T[i][j].l,T[i][j].u-mid[i][j]) for j in range(size)) for i in range(size)]
    # For any represented symmetric T, D*T >= mid-diag(charges) by diagonal dominance.
    b=[[mid[i][j]-(charges[i] if i==j else 0) for j in range(size)] for i in range(size)]
    previous=1; ps=[]
    for i in range(size):
        pivot=b[i][i]
        assert pivot>0, ('exact comparison not positive',i)
        ps.append(bounds(I(F(pivot,previous*D))))
        for r in range(i+1,size):
            for c in range(i+1,size):
                bn=pivot*b[r][c]-b[r][i]*b[i][c]; assert bn%previous==0
                b[r][c]=bn//previous
        previous=pivot
    return ps,bounds(I(F(max(charges),D)))
piv,row_error=stable_ldl(A)
g_floor=F(1,100);g_cap=F(1,2)
mass_lower_piv=ildl([[iv(g[i][j]-(g_floor if i==j else 0)) for j in range(d)] for i in range(d)])
mass_upper_piv=ildl([[iv((g_cap if i==j else 0)-g[i][j]) for j in range(d)] for i in range(d)])
res={'scope':'12-dimensional clamped even Legendre image only, no high-space or global extension','integer_interval_math':'outward dyadic rational with exact Fraction ground truth','bits':a.bits,'gamma_taylor_order':N,'gamma_kernel_sup_error_upper':bounds(iv(err)),'witness_denominator':10**8,'witness_numerators':ci,'norm2_exact':str(norm),'q_interval':bounds(val),'q_integer_endpoints_den_2powbits':[str(val.l),str(val.u)],'RQ_interval':bounds(rq),'RQ_integer_endpoints_den_2powbits':[str(rq.l),str(rq.u)],'matrix_floor':'10^-11 physical squared norm','matrix_cmp_Bareiss_LDL_pivots':piv,'max_unnormalized_row_error':row_error,'mass_matrix_bounds':['1/100 I','1/2 I'],'mass_lower_pivots':mass_lower_piv,'mass_upper_pivots':mass_upper_piv}
print(json.dumps(res,indent=2));open(a.out,'w').write(json.dumps(res,indent=2)+'\n')
