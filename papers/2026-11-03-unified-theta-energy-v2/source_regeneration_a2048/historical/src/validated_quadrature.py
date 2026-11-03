"""Exact breakpoint geometry, logarithmic moments and verified Gauss data."""
from fractions import Fraction
from functools import lru_cache
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from interval_bounds import IV
from ball_array import pairs_ball,iv_pair,Ball,ua,um,up
from weighted64 import prime_powers


def prime_geometry(refinement=16,h=Fraction(1,640),extra_breakpoints=()):
    records=[];points={Fraction(j,refinement) for j in range(refinement+1)}
    for x in extra_breakpoints:
        assert 0<x<1;points.add(x)
    for n,p,_ in prime_powers(24):
        exponent=0;value=n
        while value%p==0:exponent+=1;value//=p
        assert value==1
        shift=Fraction(float(math.log(p)))*exponent
        weight=Fraction(float(math.log(p)/math.sqrt(n)))
        true_s=IV(n).log();true_a=IV(p).log()/IV(n).sqrt()
        es=max(abs(shift-Fraction(true_s.lo)),abs(shift-Fraction(true_s.hi)))
        ea=max(abs(weight-Fraction(true_a.lo)),abs(weight-Fraction(true_a.hi)))
        q=shift/h
        for x in [q,-q]:points.add(x-x.__floor__())
        records.append({'n':n,'p':p,'exponent':exponent,'shift':shift,'weight':weight,'shift_error':es,'weight_error':ea})
    return records,sorted(points)


def cheb_integer_coefficients(degree):
    out=[[1]]
    if degree==0:return out
    out.append([-1,2])
    for n in range(1,degree):
        v=[0]*(n+2)
        for j,c in enumerate(out[-1]):v[j]-=2*c;v[j+1]+=4*c
        for j,c in enumerate(out[-2]):v[j]-=c
        out.append(v)
    return out


def frac_iv(x):return IV.rational(x.numerator,x.denominator)


@lru_cache(maxsize=1024)
def log_primitives(point,degree):
    if point==0:return [IV(0)]*(degree+2),IV(0),IV(0)
    t=frac_iv(point);log=t.log();powers=[IV(1)]
    for j in range(degree+4):powers.append(powers[-1]*t)
    moments=[powers[m+1]*(log/(m+1)-IV.rational(1,(m+1)**2)) for m in range(degree+2)]
    square=powers[3]*(log*log/3-2*log/9+IV.rational(2,27))
    return moments,square,log


@lru_cache(maxsize=1024)
def cross_primitive(point):
    if point==0:return IV(0)
    if point>Fraction(1,2):return 2*cross_primitive(Fraction(1,2))-cross_primitive(1-point)
    t=frac_iv(point);log=t.log();N=80
    power=t*t
    total=IV(0)
    # -sum [J_(k+1)-J_(k+2)]/k, where J_m=integral t^m log(t).
    for k in range(1,N+1):
        power*=t
        j1=power*(log/(k+2)-IV.rational(1,(k+2)**2))
        j2=power*t*(log/(k+3)-IV.rational(1,(k+3)**2))
        total-=(j1-j2)/k
    # Positive full tail <= integral_0^t s^(N+2)(-log s)/(N+1) ds.
    tail=-(t**(N+3))*(log/(N+3)-IV.rational(1,(N+3)**2))/(N+1)
    return total+IV(0,tail.hi)


def logarithmic_moments(points,degree):
    coefficients=cheb_integer_coefficients(degree)
    def left(a,b):
        ja=log_primitives(a,degree)[0];jb=log_primitives(b,degree)[0]
        diff=[y-x for x,y in zip(ja,jb)]
        return [sum((c*diff[r+1] for r,c in enumerate(row)),IV(0)) for row in coefficients]
    IL=[];IR=[];UU=[];VV=[];UV=[]
    for a,b in zip(points,points[1:]):
        IL.append([iv_pair(v) for v in left(a,b)])
        IR.append([iv_pair(((-1)**j)*v) for j,v in enumerate(left(1-b,1-a))])
        UU.append(iv_pair(log_primitives(b,degree)[1]-log_primitives(a,degree)[1]))
        VV.append(iv_pair(log_primitives(1-a,degree)[1]-log_primitives(1-b,degree)[1]))
        UV.append(iv_pair(cross_primitive(b)-cross_primitive(a)))
    return tuple(pairs_ball(v) for v in [IL,IR,UU,VV,UV])


def legendre(x,n):
    a=IV(1);b=x
    if n==0:return a
    for j in range(2,n+1):a,b=b,((2*j-1)*x*b-(j-1)*a)/j
    return b


def gauss_verified(n):
    seeds,_=leggauss(n);roots=[];weights=[];intervals=[]
    for seed in seeds:
        if abs(seed)<1e-15 and n%2:lo=hi=Fraction(0)
        else:
            center=Fraction(float(seed));radius=Fraction(1,1<<44);lo=center-radius;hi=center+radius
            pl=legendre(frac_iv(lo),n);ph=legendre(frac_iv(hi),n)
            if not (pl.hi<0<ph.lo or ph.hi<0<pl.lo):raise ArithmeticError('Initial Gauss bracket not certified')
            lower_negative=pl.hi<0
            for _ in range(80):
                mid=(lo+hi)/2;pm=legendre(frac_iv(mid),n)
                if pm.lo<=0<=pm.hi:raise ArithmeticError('Increase precision for Gauss bisection')
                if (pm.hi<0)==lower_negative:lo=mid
                else:hi=mid
        x=IV(frac_iv(lo).lo,frac_iv(hi).hi)
        pn=legendre(x,n);prev=legendre(x,n-1)
        derivative=n*(x*pn-prev)/(x*x-1)
        if derivative.lo<=0<=derivative.hi:raise ArithmeticError('Gauss derivative not separated from zero')
        weight=2/((1-x*x)*derivative**2)
        roots.append(iv_pair(x));weights.append(iv_pair(weight));intervals.append((lo,hi))
    if not all(a[1]<b[0] for a,b in zip(intervals,intervals[1:])):raise ArithmeticError('Overlapping root brackets')
    return pairs_ball(roots),pairs_ball(weights)


def cheb_vandermonde_ball(x,degree):
    # Direct natural interval recurrence loses dependency. Instead use the
    # exact bound |T'_j|<=j^2 on [-1,1], and U_j propagation of rounding errors.
    if np.any(np.abs(x.mid)+x.rad>1):raise ArithmeticError('Chebyshev argument exceeds [-1,1]')
    values=[np.ones_like(x.mid)]
    if degree:values.append(x.mid.copy())
    for j in range(1,degree):values.append(2*x.mid*values[-1]-values[-2])
    if max(float(np.max(np.abs(v))) for v in values)>2:raise ArithmeticError('Unexpected recurrence growth')
    mid=np.stack(values,axis=-1)
    rad=np.stack([ua(um(x.rad,j*j),16*2**-52*(j+1)**2) for j in range(degree+1)],axis=-1)
    rad[...,0]=0
    return Ball(mid,rad)
