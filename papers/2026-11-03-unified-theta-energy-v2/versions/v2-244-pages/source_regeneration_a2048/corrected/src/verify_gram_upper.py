"""Certified weighted Gram upper matrix for a frozen compact spline candidate.

Each reciprocal weight is bounded on its entire cell using directed intervals.
Spline polynomial integrals and all matrix contractions then use exact integers.
The exact centered Gram is <= the raw Gram, so no subtraction is necessary.
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


def common_dyadic(pairs):
    powers=[int(d).bit_length()-1 for n,d in pairs]
    if any(int(d)!=(1<<p) for (_,d),p in zip(pairs,powers)):raise ValueError('Non-dyadic input')
    power=max(powers,default=0)
    return [int(n)<<(power-p) for (n,_),p in zip(pairs,powers)],power


def upper_dyadic(decimal_upper):
    value=float(decimal_upper)
    if not math.isfinite(value) or value<=0:raise ValueError('Positive finite bound required')
    if Decimal.from_float(value)<decimal_upper:value=math.nextafter(value,math.inf)
    assert Decimal.from_float(value)>=decimal_upper
    return list(value.as_integer_ratio())


def gram_integer_matrix(node_pairs,weight_pairs,h):
    n=len(node_pairs);k=len(node_pairs[0])
    flat,p=common_dyadic([v for row in node_pairs for v in row])
    weights,q=common_dyadic(weight_pairs)
    A=np.array(flat,dtype=object).reshape(n,k)
    B=np.vstack([A[1:],np.zeros((1,k),dtype=object)])
    S=A+B
    ww=np.array(weights,dtype=object)[:,None]
    # Full-line integral per half-cell is h/3*[aa^T+bb^T+(a+b)(a+b)^T].
    numerator=(A.T@(ww*A)+B.T@(ww*B)+S.T@(ww*S))*h.numerator
    denominator=3*h.denominator*(1<<(2*p+q))
    if not np.array_equal(numerator,numerator.T):raise ArithmeticError('Lost exact symmetry')
    return numerator,denominator


def gram_trace_exact(node_pairs,h):
    n=len(node_pairs);k=len(node_pairs[0])
    flat,p=common_dyadic([v for row in node_pairs for v in row])
    total=0
    for j in range(n):
        for c in range(k):
            left=flat[j*k+c];right=flat[(j+1)*k+c] if j+1<n else 0
            total+=left*left+right*right+(left+right)**2
    return Fraction(total*h.numerator,3*h.denominator*(1<<(2*p)))


def main(args):
    started=time.time();folder=Path(args.candidate);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    packet=json.loads((folder/'candidate.json').read_text());h=Fraction(packet['h']);n=packet['n']
    if len(packet['node_dyadics'])!=n:raise ValueError('Candidate shape mismatch')
    # Cache a constant only; interval arithmetic precision is fixed at 70 digits.
    ib.pi_interval=lru_cache(maxsize=1)(ib.pi_interval)
    weights=[];bounds=[]
    for j in range(n):
        lo=ib.IV.rational(h.numerator*j,h.denominator)
        hi=ib.IV.rational(h.numerator*(j+1),h.denominator)
        x=ib.IV(lo.lo,hi.hi)
        W=ib.weight_interval(x)
        if W.lo<=0:raise ArithmeticError(f'Could not bound positive W on cell {j}')
        reciprocal=1/ib.IV(W.lo)
        weights.append(upper_dyadic(reciprocal.hi))
        bounds.append({'cell':j,'W_lower':str(W.lo),'reciprocal_dyadic_upper':weights[-1]})
    numerator,denominator=gram_integer_matrix(packet['node_dyadics'],weights,h)
    exact={'status':'CERT','scope':'Loewner upper enclosure of exact centered candidate H Gram ONLY',
           'matrix_numerators':[[str(v) for v in row] for row in numerator],
           'common_denominator':str(denominator),
           'candidate_sha256':hashlib.sha256((folder/'candidate.json').read_bytes()).hexdigest(),
           'construction':'sum of exact cell polynomial Grams with whole-cell reciprocal-weight upper bounds; G_centered<=G_raw',
           'cell_bounds':bounds,'precision_decimal_digits':ib.PRECISION,'elapsed_seconds':time.time()-started,
           'actual_global256_gate':'NOT_RUN'}
    (out/'G_upper_exact.json').write_text(json.dumps(exact,indent=2)+'\n')
    g=np.array([[float(Fraction(int(v),denominator)) for v in row] for row in numerator])
    result={'status':'CERT','scope':exact['scope'],'candidate_sha256':exact['candidate_sha256'],
            'G_upper_sha256':hashlib.sha256((out/'G_upper_exact.json').read_bytes()).hexdigest(),
            'actual_global256_gate':'NOT_RUN','elapsed_seconds':exact['elapsed_seconds']}
    if args.diagnostic:
        data=np.load(Path(args.diagnostic)/'matrices.npz')
        result['comparison_with_DIAG_centered_Gram_eigen_min_DIAG']=float(linalg.eigvalsh(g-data['G'])[0])
        result['comparison_with_DIAG_centered_Gram_eigen_max_DIAG']=float(linalg.eigvalsh(g-data['G'])[-1])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True);ap.add_argument('--diagnostic')
    main(ap.parse_args())
