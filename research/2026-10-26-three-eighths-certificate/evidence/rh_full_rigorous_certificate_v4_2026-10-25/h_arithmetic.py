"""Fixed full H_trial enclosure; MPFR row jets and binary64 BLAS with norm budgets.
No adaptive mesh, precision escalation, or selected-subspace substitution.
"""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import ctypes,json,time,math
from pathlib import Path
import numpy as np
NF=552; DF=1104; DC=552; NC=276
EPS=2.0**-53; TINY=np.finfo(float).tiny
START=time.monotonic()

def promote(a):
    a=np.asarray(a)
    if np.any(a<0) or not np.isfinite(a).all():raise RuntimeError('invalid nonnegative bound input')
    return np.maximum(a,TINY)
def ua(a,b): return np.nextafter(promote(a)+promote(b)+TINY,np.inf)
def um(a,b): return np.nextafter(promote(a)*promote(b)+TINY,np.inf)
def center_guard(a):
    a=np.asarray(a)
    bits=np.ascontiguousarray(a,dtype=np.float64).view(np.uint64)
    sub=((bits & np.uint64(0x7ff0000000000000))==0)&((bits & np.uint64(0x000fffffffffffff))!=0)
    if not np.isfinite(a).all() or np.any(sub) or np.max(np.abs(a),initial=0)>1e50:raise RuntimeError('nonfinite/subnormal/overflow-risk center input unsupported')
def usum(a,axis=None):
    a=promote(a); n=a.size if axis is None else a.shape[axis]
    z=np.sum(a,axis=axis)
    return np.nextafter((z+n*TINY)/(1-(n+2)*EPS),np.inf)
def norms(a,axis=-1):
    a=np.asarray(a); n=a.size if axis is None else a.shape[axis]
    z=np.sum(a*a,axis=axis)
    return np.nextafter(np.sqrt((z+n*TINY)/(1-(2*n+4)*EPS))/(1-EPS),np.inf)
def gam(n):return np.nextafter((n*EPS)/(1-n*EPS),np.inf)
def ensure(a):
    if not np.isfinite(a).all():raise RuntimeError('nonfinite floating intermediary')
def savej(name,x):
    p=Path(name);t=Path(name+'.tmp');t.write_text(json.dumps(x,indent=2,allow_nan=False));t.replace(p)
def boundfield(x,key):
    v=x[key]
    if isinstance(v,dict):return float(v.get('upper_float',v.get('upper',v.get('hi'))))
    return float(v)
