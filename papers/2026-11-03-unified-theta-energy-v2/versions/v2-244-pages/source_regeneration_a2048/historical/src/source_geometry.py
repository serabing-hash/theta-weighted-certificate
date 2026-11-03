"""Directed true-log-radius geometry; a dyadic cutoff is only a residual model."""
from fractions import Fraction
import math
import numpy as np
from interval_bounds import IV,pi_interval
from ball_array import Ball,iv_pair,pairs_ball,fraction_pair
from target import radius_interval

def abs_upper(x):return max(x.lo.copy_abs(),x.hi.copy_abs())

def cos_small(x):
    x=IV(x);z=x*x;v=IV(0)
    for j in reversed(range(40)):v=v*z+IV.rational((-1)**j,math.factorial(2*j))
    e=IV(abs_upper(x))**80/math.factorial(80)
    return v+IV(e.hi.copy_negate(),e.hi)

def sin_small(x):
    x=IV(x);z=x*x;v=IV(0)
    for j in reversed(range(40)):v=v*z+IV.rational((-1)**j,math.factorial(2*j+1))
    v*=x;e=IV(abs_upper(x))**81/math.factorial(81)
    return v+IV(e.hi.copy_negate(),e.hi)

def geometry(h,k,radius=None):
    B=radius_interval() if radius is None else IV(radius)
    hh=IV.rational(h.numerator,h.denominator);ratio=B/hh
    q=Fraction(ratio.lo).__floor__()
    assert Fraction(ratio.hi).__floor__()==q and (hh*q).hi<B.lo and B.hi<(hh*(q+1)).lo
    cutoff=Fraction((Fraction(B.lo)+Fraction(B.hi))/2*(1<<120)).__round__()/Fraction(1<<120)
    displacement=max(abs(cutoff-Fraction(B.lo)),abs(cutoff-Fraction(B.hi)))
    theta=pi_interval()*hh/B
    assert (theta*(k-1)).hi<1
    norms=[(2*B).sqrt().reciprocal()]+[B.sqrt().reciprocal()]*(k-1)
    # Directly enclose each binary-angle rotation, then compose at most log2(q)
    # rotations per point. This does NOT propagate natural intervals q times.
    cb=Ball(np.ones((q+2,k)));sb=Ball(np.zeros((q+2,k)))
    indices=np.arange(q+2)
    for bit in range((q+1).bit_length()):
        cvals=[];svals=[]
        for m in range(k):
            halfturn=IV.rational(m*h.numerator*(1<<bit),h.denominator)/B
            quarter=int(round(float((halfturn*2).lo)))
            residual=pi_interval()*(halfturn-IV.rational(quarter,2))
            assert abs_upper(residual)<1
            cc=cos_small(residual);ss=sin_small(residual)
            cval,sval=[(cc,ss),(-ss,cc),(-cc,-ss),(ss,-cc)][quarter%4]
            cvals.append(iv_pair(cval));svals.append(iv_pair(sval))
        bc=pairs_ball(cvals);bs=pairs_ball(svals);selected=(indices&(1<<bit))!=0
        left=cb[selected];right=sb[selected]
        nc=left*bc-right*bs;ns=right*bc+left*bs
        cm=cb.mid.copy();cr=cb.rad.copy();sm=sb.mid.copy();sr=sb.rad.copy()
        cm[selected]=nc.mid;cr[selected]=nc.rad;sm[selected]=ns.mid;sr[selected]=ns.rad
        cb=Ball(cm,cr);sb=Ball(sm,sr)
    assert np.isfinite(cb.rad).all() and np.isfinite(sb.rad).all()
    return B,q,cutoff,displacement,cb,sb,norms


def moment_coefficients(n,h,k,geom):
    B,q,cutoff,displacement,cosgrid,singrid,norms=geom
    assert q+1<n
    hh=IV.rational(h.numerator,h.denominator);theta=pi_interval()*hh/B
    coeff=Ball(np.zeros((k,n)))
    mid=coeff.mid.copy();rad=coeff.rad.copy()
    delta=B-q*hh
    zeroweights=[hh/2]+[hh]*(q-1)+[hh/2+delta-delta**2/(2*hh),delta**2/(2*hh)]
    for j,v in enumerate(zeroweights):mid[0,j],rad[0,j]=iv_pair(2*norms[0]*v)
    for m in range(1,k):
        omega=pi_interval()*m/B;t=theta*m
        sinc2=2*(1-cos_small(t))/(t*t)
        factor=Ball.iv(2*norms[m]*hh*sinc2)
        inside=cosgrid[:q,m]*factor
        mid[m,:q]=inside.mid;rad[m,:q]=inside.rad
        mid[m,0]/=2;rad[m,0]/=2
        scale=Ball.iv(2*norms[m]/(hh*omega**2))
        terminal=(2*cosgrid[q,m]-cosgrid[q-1,m]-((-1)**m))*scale
        final=((((-1)**m)-cosgrid[q,m]))*scale
        mid[m,q]=terminal.mid;rad[m,q]=terminal.rad
        mid[m,q+1]=final.mid;rad[m,q+1]=final.rad
    return Ball(mid,rad)

def ball_to_intervals(x):
    out=[]
    for rowmid,rowrad in zip(x.mid,x.rad):
        row=[]
        for mid,rad in zip(rowmid,rowrad):
            a=Fraction(float(mid));b=Fraction(float(rad));lo=a-b;hi=a+b
            row.append(IV(IV.rational(lo.numerator,lo.denominator).lo,IV.rational(hi.numerator,hi.denominator).hi))
        out.append(row)
    return out
