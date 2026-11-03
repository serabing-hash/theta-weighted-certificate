"""Certified primal ell_a lower matrix for the frozen compact spline candidate.

The complete Gamma form dominates a finite sum of its positive exponential
labels. No missing primal Gamma tail is replaced by an unproved small error.
The remaining full residual head is a different, still unverified obligation.
"""
import argparse
from decimal import Decimal
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy import linalg
import interval_bounds as ib
from target import A
from verify_gram_upper import common_dyadic,gram_integer_matrix
from weighted64 import prime_powers


def label_kernel(alpha,h,count):
    """Exact-meaning single-label full-line hat Gamma bilinear intervals."""
    t=alpha*h;z=(-t).exp();den=h**2*alpha**4
    values=[(4*t-6+8*z-2*z*z)/den,
            (-2*t+4-7*z+4*z*z-z**3)/den]
    term=-(1-z)**4/den
    for lag in range(2,count):
        values.append(term);term*=z
    return values[:count]


def absolute(x):
    if x.lo>=0:return x
    if x.hi<=0:return -x
    return ib.IV(0,max(x.lo.copy_abs(),x.hi.copy_abs()))


def positive_part(x):return ib.IV(max(Decimal(0),x.lo),max(Decimal(0),x.hi))


def correlation(x,h):
    t=absolute(x)/h
    return h*(positive_part(2-t)**3-4*positive_part(1-t)**3)/6


def cgamma_upper():
    # H_N-log(N+1) < Euler gamma < H_N-log(N), from integral comparison.
    # The exact identity psi(1/4)=-EulerGamma-pi/2-3 log 2 fixes the constant.
    n=16384
    harmonic=sum((ib.IV.rational(1,j) for j in range(1,n+1)),ib.IV(0))
    upper=(harmonic-ib.IV(n).log()+ib.pi_interval()/2+3*ib.IV(2).log()+ib.pi_interval().log()).hi
    value=float(upper)
    if Decimal.from_float(value)<upper:value=math.nextafter(value,math.inf)
    assert Decimal.from_float(value)>=upper
    return ib.IV(Decimal.from_float(value)),{'harmonic_N':n,'upper_exact_dyadic':list(value.as_integer_ratio())}


def quantize_kernel(kernel,power=70):
    denominator=1<<power;values=[];radius=Fraction(1,1<<(power-1))
    for v in kernel:
        middle=(Fraction(v.lo)+Fraction(v.hi))/2
        num=(middle*denominator).__floor__()
        point=Fraction(num,denominator)
        if max(abs(point-Fraction(v.lo)),abs(point-Fraction(v.hi)))>radius:
            raise ArithmeticError('Kernel interval wider than the exact fixed quantization budget')
        values.append(num)
    return values,denominator,radius


def contract_even_kernel(node_pairs,kernel_int,kernel_den):
    from integer_convolution import signed_convolution
    n=len(node_pairs);k=len(node_pairs[0])
    values,p=common_dyadic([v for row in node_pairs for v in row])
    nodes=np.array(values,dtype=object).reshape(n,k)
    full=np.vstack([nodes[:0:-1],nodes]);center=2*n-2
    kernel=list(reversed(kernel_int[1:2*n-1]))+list(kernel_int[:2*n-1])
    response=np.empty((n,k),dtype=object)
    for col in range(k):
        con=signed_convolution(kernel,full[:,col]);cut=con[center:center+2*n-1]
        assert len(cut)==2*n-1 and cut[:n-1]==cut[:n-1:-1]
        response[0,col]=cut[n-1]
        for i in range(1,n):response[i,col]=2*cut[n-1+i]
        if (col+1)%32==0:print(f'exact primal convolutions {col+1}/{k}',flush=True)
    matrix=nodes.T@response
    assert np.array_equal(matrix,matrix.T)
    node_trace=sum(int(x)*int(x) for x in nodes.flat)
    return matrix,kernel_den*(1<<(2*p)),Fraction(node_trace,1<<(2*p))


def main(args):
    started=time.time();folder=Path(args.candidate);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    packet=json.loads((folder/'candidate.json').read_text());n=packet['n'];k=packet['k'];h=Fraction(packet['h']);L=Fraction(packet['L'])
    ib.pi_interval=lru_cache(maxsize=1)(ib.pi_interval)
    hh=ib.IV.rational(h.numerator,h.denominator)
    assert packet['a']==str(A)
    cache=None
    if args.scalar_cache:
        path=Path(args.scalar_cache);cache=json.loads(path.read_text())
        expected=json.loads(Path('inputs/cache_inventory.json').read_text())['primal_scalar_bounds']['sha256']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
        assert cache['status']=='CERT_SCALAR_CACHE'
        assert cache['geometry']=={key:packet[key] for key in ['n','h','L','B']}
        assert cache['Gamma_labels']==args.labels
    else:
        gamma=[ib.IV(0) for _ in range(2*n)]
        for j in range(args.labels):
            alpha=ib.IV.rational(4*j+1,2)
            term=label_kernel(alpha,hh,len(gamma))
            gamma=[x+y for x,y in zip(gamma,term)]
            if (j+1)%128==0:print(f'interval Gamma labels {j+1}/{args.labels}',flush=True)
        cg,cgrecord=cgamma_upper()
    cap=(2*ib.IV.rational(L.numerator,L.denominator)).exp()
    ncap=math.floor(float(cap.hi))
    if not cap.hi<ncap+1:raise ArithmeticError('Ambiguous primal prime cutoff')
    if cache:
        points=[int(x) for x in cache['kernel_quantized_numerators']]
        kden=int(cache['kernel_denominator']);radius=Fraction(cache['kernel_entry_radius'])
        cgrecord=cache['cgamma_upper']
        assert len(points)==2*n and cache['primal_prime_head']==[num for num,_,_ in prime_powers(ncap)]
    else:
        kernel=gamma[:]
        for lag in range(len(kernel)):
            if lag<2:kernel[lag]-=cg*hh*ib.IV.rational(2,3) if lag==0 else cg*hh/6
        for num,base,_ in prime_powers(ncap):
            shift=ib.IV(num).log();weight=ib.IV(base).log()/ib.IV(num).sqrt()
            for lag in range(len(kernel)):
                distance=hh*lag
                for diff in [distance-shift,distance+shift]:
                    if absolute(diff).lo>=(2*hh).hi:continue
                    kernel[lag]-=weight*correlation(diff,hh)
        points,kden,radius=quantize_kernel(kernel)
    print('exact integer contraction of primal kernel',flush=True)
    qnum,qden,node_trace=contract_even_kernel(packet['node_dyadics'],points,kden)
    # Each folded entry perturbation is <=4 radius; spectral norm <=4n radius.
    # After contraction, ||nodes||_op^2<=sum nodal squares=node_trace.
    error=4*n*radius*node_trace
    weights=[] if cache is None else cache['reciprocal_weight_cell_lower_dyadics']
    if cache is None:
        for j in range(n):
            lo=hh*j;hi=hh*(j+1);W=ib.weight_interval(ib.IV(lo.lo,hi.hi))
            lower=(1/ib.IV(W.hi)).lo
            val=float(lower)
            if Decimal.from_float(val)>lower:val=math.nextafter(val,-math.inf)
            if val<=0 or Decimal.from_float(val)>lower:raise ArithmeticError('Invalid lower reciprocal weight')
            weights.append(list(val.as_integer_ratio()))
    assert len(weights)==n and 2-4*A>0
    hnum,hden=gram_integer_matrix(packet['node_dyadics'],weights,h)
    # Exact centering adds (2-4a)mm^T>=0, which is safely dropped.
    den=math.lcm(qden,hden*A.denominator,error.denominator)
    T=qnum*(den//qden)+hnum*A.numerator*(den//(hden*A.denominator))
    for i in range(k):T[i,i]-=error.numerator*(den//error.denominator)
    record={'status':'CERT','scope':'Loewner lower enclosure of full exact centered candidate ell_a Gram T ONLY',
            'candidate_sha256':hashlib.sha256((folder/'candidate.json').read_bytes()).hexdigest(),
            'matrix_numerators':[[str(x) for x in row] for row in T],'common_denominator':str(den),
            'Gamma_labels':args.labels,'Gamma_omitted_primal_cost':'0: omitted labels are nonnegative quadratic forms, so truncation is a LOWER bound',
            'cgamma_upper':cgrecord,'primal_prime_head':[num for num,_,_ in prime_powers(ncap)],
            'kernel_quantized_numerators':[str(v) for v in points],'kernel_denominator':str(kden),
            'kernel_entry_radius':str(radius),'contracted_kernel_error_scalar':str(error),
            'reciprocal_weight_cell_lower_dyadics':weights,
            'a':str(A),'centering':'T=ell(raw)+(2-4a)mm^T, omitted term is PSD at a=1/2048',
            'scalar_cache_sha256':hashlib.sha256(Path(args.scalar_cache).read_bytes()).hexdigest() if cache else None,
            'actual_global256_gate':'NOT_RUN','elapsed_seconds':time.time()-started}
    (out/'T_lower_exact.json').write_text(json.dumps(record,indent=2)+'\n')
    summary={key:record[key] for key in ['status','scope','candidate_sha256','Gamma_labels','elapsed_seconds','actual_global256_gate']}
    summary['T_lower_sha256']=hashlib.sha256((out/'T_lower_exact.json').read_bytes()).hexdigest()
    if args.diagnostic:
        data=np.load(Path(args.diagnostic)/'matrices.npz')
        tt=np.array([[float(Fraction(int(x),den)) for x in row] for row in T])
        summary['DIAG_T_minus_Tlower_eigen_min']=float(linalg.eigvalsh(data['T']-tt)[0])
        summary['DIAG_T_minus_Tlower_eigen_max']=float(linalg.eigvalsh(data['T']-tt)[-1])
    (out/'result.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--labels',type=int,default=1024);ap.add_argument('--diagnostic');ap.add_argument('--scalar-cache');main(ap.parse_args())
