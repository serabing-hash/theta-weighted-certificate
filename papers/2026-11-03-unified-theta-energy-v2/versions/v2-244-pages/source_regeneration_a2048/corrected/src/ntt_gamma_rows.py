"""Exact modular convolution of quantized interval Gamma-potential samples.

All modular transforms and CRT reconstruction are INTEGER operations. The
separate analytic budget pays source quantization and conversion to binary64.
"""
from fractions import Fraction
from functools import lru_cache
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from interval_bounds import IV
from freeze_candidate import cosine_table
from validated_phi import phi,constants

PRIMES=((998244353,3),(1004535809,3),(469762049,3),(2013265921,31),(1224736769,3))
H_BITS=60
J_BITS=60


@lru_cache(maxsize=8)
def reverse_indices(n):
    a=np.arange(n,dtype=np.int64);r=np.zeros(n,dtype=np.int64)
    for _ in range(n.bit_length()-1):r=(r<<1)|(a&1);a>>=1
    return r


@lru_cache(maxsize=256)
def twiddles(length,prime,root,inverse):
    w=pow(root,(prime-1)//length,prime)
    if inverse:w=pow(w,prime-2,prime)
    out=np.empty(length//2,dtype=np.int64);v=1
    for j in range(len(out)):out[j]=v;v=v*w%prime
    return out


def ntt(values,prime,root,inverse=False):
    a=np.array(values,dtype=np.int64,copy=True)%prime
    vector=a.ndim==1
    if vector:a=a[:,None]
    n=len(a)
    if n&(n-1) or (prime-1)%n:raise ValueError('Unsupported NTT length')
    if prime*prime>=1<<63:raise ValueError('Potential signed int64 product overflow')
    a=a[reverse_indices(n)].copy()
    length=2
    while length<=n:
        view=a.reshape(-1,length,a.shape[1]);half=length//2
        u=view[:,:half,:].copy()
        v=(view[:,half:,:]*twiddles(length,prime,root,inverse)[None,:,None])%prime
        view[:,:half,:]=(u+v)%prime;view[:,half:,:]=(u-v)%prime
        length*=2
    if inverse:a=(a*pow(n,prime-2,prime))%prime
    return a[:,0] if vector else a


def crt_signed(residues):
    result=residues[0].astype(object);modulus=PRIMES[0][0]
    for residue,(p,_) in zip(residues[1:],PRIMES[1:]):
        delta=(residue-np.array(result%p,dtype=np.int64))%p
        t=(delta*pow(modulus%p,p-2,p))%p
        result+=modulus*t.astype(object);modulus*=p
    mask=result>modulus//2
    result[mask]-=modulus
    return result


def nearest_integer(q):return (q+Fraction(1,2)).__floor__()


def exact_jumps(packet):
    rows=[[Fraction(*x) for x in row] for row in packet['node_dyadics']]
    k=len(rows[0]);zero=[Fraction(0)]*k
    full=[zero]+rows[:0:-1]+rows+[zero]
    h=Fraction(packet['h'])
    slopes=[[(b-a)/h for a,b in zip(left,right)] for left,right in zip(full,full[1:])]
    jumps=[slopes[0]]+[[b-a for a,b in zip(left,right)] for left,right in zip(slopes,slopes[1:])]+[[-v for v in slopes[-1]]]
    return jumps


def main(args):
    start=time.time();folder=Path(args.candidate);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    packet=json.loads((folder/'candidate.json').read_text());h=Fraction(packet['h']);n=packet['n'];k=packet['k'];cells=(Fraction(2)/h).numerator;degree=args.degree
    assert (Fraction(2)/h).denominator==1
    assert k==256 and packet['B']=='log(8)/2' and packet['a']=='1/2048'
    jumps=exact_jumps(packet)
    integer_jumps=np.array([[nearest_integer(-v*(1<<J_BITS)) for v in row] for row in jumps],dtype=object)
    # Convolution output needs integer offsets in [-n,cells-1+n].
    size=1
    while size<cells+2*n+2:size*=2
    source_ffts=[]
    for p,g in PRIMES:
        source=np.zeros((size,k),dtype=np.int64)
        for j,row in enumerate(integer_jumps):source[(j-n)%size]=np.array(row%p,dtype=np.int64)
        source_ffts.append(ntt(source,p,g))
    product=math.prod(p for p,_ in PRIMES)
    table=cosine_table(degree)
    phases=[(1+table[j])/2 for j in range(degree+1)]
    H0,_,_=constants()
    if H0.hi>=5:raise ArithmeticError('H0 bound failed')
    absjump=[sum(abs(row[col]) for row in jumps) for col in range(k)]
    hradius=Fraction(1,1<<(H_BITS-1));jradius=Fraction(1,1<<(J_BITS+1))
    if Fraction(H0.hi)+hradius>=5:raise ArithmeticError('Quantized Phi is not bounded by5')
    error=[hradius*s+jradius*len(jumps)*5 for s in absjump]
    gamma=np.empty((degree+1,cells,k));radii=np.empty_like(gamma)
    for phase_index,phase in enumerate(phases):
        kernel=np.zeros(size,dtype=np.int64)
        maximum=0
        for offset in range(-n,cells+n+1):
            d=(IV(offset)+phase)*IV.rational(h.numerator,h.denominator)
            if d.hi<0:d=-d
            elif d.lo<0:
                if abs(float(d.lo))+abs(float(d.hi))<1e-60 and (offset,phase_index) in [(0,degree),(-1,0)]:d=IV(0)
                else:raise ArithmeticError('Unresolved distance sign')
            ball=phi(d)
            middle=(Fraction(ball.lo)+Fraction(ball.hi))/2
            number=nearest_integer(middle*(1<<H_BITS))
            point=Fraction(number,1<<H_BITS)
            if max(abs(point-Fraction(ball.lo)),abs(point-Fraction(ball.hi)))>hradius:
                raise ArithmeticError('Phi interval exceeds quantization radius')
            kernel[offset%size]=number;maximum=max(maximum,abs(number))
        bound=maximum*max(sum(abs(int(x)) for x in integer_jumps[:,j]) for j in range(k))
        if 2*bound>=product:raise ArithmeticError('Insufficient CRT dynamic range')
        residues=[]
        for source_fft,(p,g) in zip(source_ffts,PRIMES):
            spectrum=ntt(kernel,p,g)
            residues.append(ntt((spectrum[:,None]*source_fft)%p,p,g,True)[:cells])
        exact=crt_signed(residues)
        midpoint=np.ldexp(np.array(exact,dtype=float),-(H_BITS+J_BITS))
        rad=np.nextafter(np.abs(midpoint)*2**-52+np.array([float(x) for x in error])[None,:]*(1+2**-50),np.inf)
        gamma[phase_index]=midpoint;radii[phase_index]=rad
        print(f'validated Gamma phase {phase_index+1}/{degree+1}',flush=True)
    np.savez_compressed(out/'gamma_nodes.npz',mid=gamma,rad=radii)
    record={'status':'CERT','scope':'complete Gamma row enclosures at Chebyshev nodes ONLY',
            'candidate_sha256':hashlib.sha256((folder/'candidate.json').read_bytes()).hexdigest(),
            'degree':degree,'cells':cells,'NTT_length':size,'primes':[p for p,_ in PRIMES],
            'H_bits':H_BITS,'jump_bits':J_BITS,'H_point_radius':str(hradius),'jump_point_radius':str(jradius),
            'column_error_bounds_before_float':[str(x) for x in error],
            'max_binary64_point_radius':float(np.max(radii)),
            'raw_nodes_sha256':hashlib.sha256((out/'gamma_nodes.npz').read_bytes()).hexdigest(),
            'elapsed_seconds':time.time()-start,'actual_global256_gate':'NOT_RUN'}
    (out/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True);ap.add_argument('--degree',type=int,default=32)
    main(ap.parse_args())
