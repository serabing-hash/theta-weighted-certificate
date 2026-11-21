"""Fixed B=2 genuine 2-column plane only. Compile-time none. Python 3+SymPy, system MPFI/GMP/MPFR. Directed operations. No numerical zeta zero inputs."""
from fractions import Fraction as F
from math import factorial,comb,ceil
from functools import lru_cache
from ctypes import *
import sympy as sp, json,sys
lib=CDLL('libmpfi.so.0'); fr=CDLL('libmpfr.so.6')
class I:
    def __init__(self,v=None):
        self.a=create_string_buffer(128);lib.mpfi_init2(self.a,384)
        if v is not None:
            f=F(v);lib.mpfi_set_str(self.a,str(f.numerator).encode(),10)
            if f.denominator!=1:
                den=I(f.denominator);lib.mpfi_div(self.a,self.a,den.a)
    def __del__(self):lib.mpfi_clear(self.a)
    def op(self,fn,b=None):
        z=I(); f=getattr(lib,'mpfi_'+fn)
        if b is None:f(z.a,self.a)
        else:
            q=b if isinstance(b,I) else I(b);f(z.a,self.a,q.a)
        return z
    def __add__(s,b):return s.op('add',b)
    __radd__=__add__
    def __sub__(s,b):return s.op('sub',b)
    def __rsub__(s,b):return I(b).op('sub',s)
    def __mul__(s,b):return s.op('mul',b)
    __rmul__=__mul__
    def __truediv__(s,b):return s.op('div',b)
    def __rtruediv__(s,b):return I(b).op('div',s)
    def __neg__(s):return s.op('neg')
    def __pow__(s,k):
        assert type(k)==int and k>=0
        z=I(1)
        while k:
            if k%2:z=z*s
            k//=2
            if k:s=s*s
        return z
    def ab(s):
        out=[];fr.mpfr_get_d.restype=c_double
        for name,rnd in [('mpfi_get_left',3),('mpfi_get_right',2)]:
            a=create_string_buffer(64);fr.mpfr_init2(a,384);getattr(lib,name)(a,s.a)
            out.append(fr.mpfr_get_d(a,rnd));fr.mpfr_clear(a)
        assert out[0]<=out[1]
        return out
def const(name):
    z=I();getattr(lib,'mpfi_const_'+name)(z.a);return z
def hull(a,b):
    z=I();a=i(a);b=i(b);lib.mpfi_union(z.a,a.a,b.a);return z
def i(v):return v if isinstance(v,I) else I(v)
x,S=sp.symbols('x s')
def pol(k):
    g=sp.Poly((1-x*x/4)**k,x)
    return g.diff((x,2))-g/4
def mass(f,g):
    return F(sum(c*sp.Rational(2**(p+2),p+1) for (p,),c in sp.Poly(f*g,x).terms() if p%2==0))
g=[sp.Poly(pol(j),x) for j in (8,9)]
ratio=mass(*g)/mass(g[0],g[0]);g[1]=sp.Poly(g[1]-g[0]*ratio,x);M=[mass(v,v) for v in g]
def corr(f,g):
    # shifted y=x+2, on [0,4-s]. By expansion of both polynomials about -2 and +2,
    # x=-2+y, x+s=2-(4-s-y), beta monomial integration gives C(s)=sum b_d(4-s)^d
    f=sp.Poly(f.as_expr().subs(x,x-2),x);g=sp.Poly(g.as_expr().subs(x,2-x),x)
    L=[F(0)]*(f.degree()+g.degree()+2)
    for (j,),a in f.terms():
        for (k,),b in g.terms():L[j+k+1]+=F(a*b)*F(factorial(j)*factorial(k),factorial(j+k+1))
    # ascending derivatives around s=0 and 4.
    a=[sum(L[d]*comb(d,j)*4**(d-j)*(-1)**j for d in range(j,len(L))) for j in range(len(L))]
    b=[v*(-1)**j for j,v in enumerate(L)]
    return a,b
K=32; E=8
@lru_cache(None)
def powers(p):
    assert p>1
    h=F(2*K*2+1,2)
    v=h**(1-p)/(2*(p-1))+h**(-p)/2
    for r in range(1,E+1):
        t=F(sp.bernoulli(2*r))*F(factorial(p+2*r-2),factorial(p-1)*factorial(2*r))*2**(2*r-1)*h**(-p-2*r+1)
        v+=t
    err=abs(t)
    short=sum((F(4*k+1,2)**(-p) for k in range(K)),F(0))
    return I(short)+hull(v-err,v+err)
@lru_cache(None)
def epowers(p):
    # pr/(1-exp(-8)) at λ(K) bounds geometric remainder.
    short=sum((I(-2*(4*k+1)).op('exp')*F(2,4*k+1)**p for k in range(K)),I(0))
    rem=I(-2*(4*K+1)).op('exp')*F(2,4*K+1)**p/(1-I(-8).op('exp'))
    return short+hull(0,rem)
exponent=int(sys.argv[1]) if len(sys.argv)>1 else 6
assert exponent in (6,9);eps=F(1,10**exponent); B=2;k=5;d=1;n=100*10**exponent
beta=(I(12).op('exp')-1)*eps**2/(2*k)
pi=const('pi');c=pi.op('log')+const('euler')+pi/2+3*I(2).op('log')
powers_active=[]
for pp in list(sp.primerange(2,55)):
    nn=pp
    while nn<=54:powers_active.append((nn,pp));nn*=pp
powers_active.sort()
assert (I(4)+2*eps).op('exp').ab()[0]>54 and (I(4)+2*eps).op('exp').ab()[1]<55
assert (I(B)+eps+I(16).op('log')).ab()[0]>4 and (I(B)+eps+I(16).op('log')).ab()[1]<5
assert all((I(nn).op('log')-2*eps).ab()[0]>0 and (I(nn).op('log')+2*eps).ab()[1]<4 for nn,p in powers_active)
def moments(deg):
    # E[X^l]/l! for sum of 2k independent uniform[-eps/k,eps/k] (actual autocorr smoother)
    a=[F(1)]+[F(0)]*deg; b=[(eps/k)**j/F(factorial(j+1)) if j%2==0 else 0 for j in range(deg+1)]
    for _ in range(2*k):
        a=[sum(a[j]*b[l-j] for j in range(l+1)) for l in range(deg+1)]
    return [v*factorial(l) for l,v in enumerate(a)]
def horner(a,t):
    z=I(0)
    for v in a[::-1]:z=z*t+v
    return z
def vals(f,g):
    a,b=corr(f,g); assert a[0]==mass(f,g) and a[1]==0
    ga=-2*sum((I(a[j]*factorial(j))*powers(j+1) for j in range(1,len(a)) if a[j]),I(0))
    ga+=2*sum((I(b[j]*factorial(j))*epowers(j+1) for j in range(len(b)) if b[j]),I(0))
    mom=moments(len(a)-1)
    sm=[sum(a[l]*comb(l,j)*mom[l-j] for l in range(j,len(a))) for j in range(len(a))]
    prime=sum((2*I(p).op('log')/I(nn).op('sqrt')*horner(sm,I(nn).op('log')) for nn,p in powers_active),I(0))
    bareprime=sum((2*I(p).op('log')/I(nn).op('sqrt')*horner(a,I(nn).op('log')) for nn,p in powers_active),I(0))
    return ga-c*a[0]-prime+2*beta*a[0],ga-c*a[0]-bareprime,ga,prime
out={}
for l,j in [(0,0),(0,1),(1,1)]:
    out[l,j]=vals(g[l],g[j])
print('B,eps,k,n,m',B,eps,k,n,n//2,'prime powers',powers_active,'mass',[str(v) for v in M],'orthog coeff',str(ratio))
print('2beta',(2*beta).ab())
for key,vs in out.items():
    norm=I(M[key[0]]*M[key[1]]).op('sqrt')
    print('key',key,'raw H',vs[0].ab(),'actual physical-mass normalized (H_qj,H_bare,Gamma,Psmooth)',[(v/norm).ab() for v in vs])
def normmat(t):
    return {(l,j):vs[t]/I(M[l]*M[j]).op('sqrt') for (l,j),vs in out.items()}
for t in (0,1):
    A=normmat(t); a,b,c0=A[0,0],A[0,1],A[1,1]
    print('eigen H',t,((a+c0-((a-c0)**2+4*b**2).op('sqrt'))/2).ab(),((a+c0+((a-c0)**2+4*b**2).op('sqrt'))/2).ab())

# Rigorous mixed high residual bound. Project true full-line signed load onto W.
T0=10**5
# 2*sum lambda^-3 < 17; 2sum Lambda/sqrt(n)+cGamma+2beta < 126.
pm=sum((2*I(p).op('log')/I(nn).op('sqrt') for nn,p in powers_active),I(0))
Kmass=pm+c+2*beta
der={}
for j in (0,2,4,6):
    der[j]=[mass(f.diff((x,j)),f.diff((x,j))) for f in g] if j else M
    print('sqrt deriv trace',j, sum((I(v/w) for v,w in zip(der[j],M)),I(0)).op('sqrt').ab())
dT=lambda j:sum((I(v/w) for v,w in zip(der[j],M)),I(0)).op('sqrt')
low=17*dT(2)+Kmass*dT(0)
hi=(17*dT(6)+Kmass*dT(4))/T0**4
# Moment-band concentration for W bounded by <2^-100 at T0, see accompanying report.
J=low*F(1,2**100)+hi
print('Kmass',Kmass.ab(),'low full',low.ab(),'high tail',hi.ab(),'joint R',J.ab(),'A-dual Gram norm',(J**2*F(23,42)).ab(),'C-dual debit norm',(2*J**2).ab())

# Unsmoothed fixed-box high coercivity via physical row sums, no smoothed-P high bound transferred.
A_p=lambda v:sum((I(p).op('log')/I(nn).op('sqrt') for nn,p in powers_active if nn<=v),I(0))
assert I(2).op('exp').ab()[1]<8 and I(4).op('exp').ab()[1]<55
rows=[A_p(j)+A_p(54//j) for j in range(1,8)]
print('unsmoothed row sums', [r.ab() for r in rows])
Th=8_000_000
gamma_high = 4*I(Th*Th)/(I(Th*Th)+F(1,4)) + (1+I(4*Th*Th)/25).op('log')/2
assert gamma_high.ab()[0]>18.9 and c.ab()[1]<5.38 and all(r.ab()[1]<12.2 for r in rows)
assert (I(1).op('exp')*B*Th/n).ab()[1]<0.5 and n>=10**8
print('unreg high gamma raw',gamma_high.ab(),'cGamma',c.ab(),'C_bare >= 1.3, unsmoothed joint Schur debit upper',(J**2*F(10,13)).ab())
