"""Exact integer replay of stored Gamma coefficient algebra.

No source evaluation, DFT, digamma, integral, H action or spectral matrix.
Inputs are the stored base/multiplier enclosures and exact scalar phase
enclosures.  Native fmpz polynomial multiplication is exact integer algebra.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import argparse,csv,hashlib,json,resource,time
from flint import fmpz_poly

ROOT=Path(__file__).resolve().parents[1]

def J(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,separators=(',',':'))+'\n')
def atan_inverse(q,n):
    v=sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
    e=F(1,(2*n+1)*q**(2*n+1))
    return (v-e,v) if n%2 else (v,v+e)
def sqrt_enclosure(x):
    n=isqrt((x.numerator<<360)//x.denominator)
    return F(n,2**180),F(n+1,2**180)
def multiply_intervals(a,b):
    v=[a[x]*b[y] for x in (0,1) for y in (0,1)]
    return min(v),max(v)
def contained(pair,bounds,bits=140):
    n,r=map(int,pair)
    assert F(n-r,2**bits)<=bounds[0]<=bounds[1]<=F(n+r,2**bits)

def replay(emit=False):
    start=time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(600,600))
    phase=J(ROOT/'outputs/PHASE_COEFFICIENT_ENCLOSURES.json')
    K=phase['K'];M=phase['MMAX'];KO=K+M
    table=list(csv.DictReader((ROOT/'sources/fixed_inputs/retained_cells_exact.csv').open()))
    T=[list(map(int,r)) for r in csv.reader((ROOT/'sources/fixed_inputs/T32_dyadic_numerators.csv').open())]
    a5=atan_inverse(5,128);a239=atan_inverse(239,64)
    pi=(16*a5[0]-4*a239[1],16*a5[1]-4*a239[0])
    sq3=sqrt_enclosure(F(3));sq5=sqrt_enclosure(F(5))
    al=[]
    for row in table:
        V=F(row['V_upper'])
        low=sqrt_enclosure(V/pi[1])[0];high=sqrt_enclosure(V/pi[0])[1]
        al.append((low,high))
    # Independently validate all phase inputs with rational pi and isqrt.
    for i in range(32):
        for s in range(124):
            t0,t1,t2=[F(T[3*s+r][i],2**30) for r in range(3)]
            p0=multiply_intervals(al[s],(t0/2,t0/2))
            p1=multiply_intervals(multiply_intervals(al[s],(t1/8,t1/8)),(1/sq3[1],1/sq3[0]))
            b2=multiply_intervals((t2/48,t2/48),(1/sq5[1],1/sq5[0]))
            b2=(t0/96+b2[0],t0/96+b2[1])
            p2=multiply_intervals(al[s],(-b2[1]/2,-b2[0]/2))
            for r,p in enumerate((p0,p1,p2)):contained(phase['columns'][i][r][s],p)
    base=[];BE=[];BN=[]
    for r in range(3):
        b=J(ROOT/'outputs'/f'BASE_a_{r}.json')['values']
        ns=[int(z[0]) for z in b];rs=[int(z[1]) for z in b]
        vals=[(-ns[-k] if r%2 else ns[-k]) for k in range(-K,0)]+ns
        base.append(fmpz_poly(vals))
        BE.append(F(rs[0]+2*sum(rs[1:]),2**140))
        BN.append(F(abs(ns[0])+2*sum(abs(n) for n in ns[1:]),2**140))
    mb=J(ROOT/'outputs/GAMMA_MULTIPLIERS.json')['values']
    mn=[int(z[0]) for z in mb];mr=[int(z[1]) for z in mb]
    MM=F(max(abs(n)+r for n,r in zip(mn,mr)),2**140)
    ME=F(max(mr),2**140)
    rows=[];num_convolutions=0
    for i in range(32):
        hs=fmpz_poly([]);phaseE=[];phaseN=[]
        for r in range(3):
            vals=[0]*(2*M+1);ps=phase['columns'][i][r]
            for s,p in enumerate(ps):
                n=int(p[0]);m=phase['shifts'][s]
                vals[M+m]=n;vals[M-m]=-n if r%2 else n
            poly=base[r]*fmpz_poly(vals)
            hs=hs-poly if r%2 else hs+poly
            phaseE.append(F(2*sum(int(z[1]) for z in ps),2**140))
            phaseN.append(F(2*sum(abs(int(z[0])) for z in ps),2**140))
            num_convolutions+=1
        Eh=sum((BE[r]*phaseN[r]+(BN[r]+BE[r])*phaseE[r] for r in range(3)),F(0))
        Hn=sum((BN[r]*phaseN[r] for r in range(3)),F(0))
        input_error=MM*Eh+ME*Hn
        out=J(ROOT/'outputs'/f'ACTION_{i:02d}.json')
        numer=0
        for k,s in enumerate(out['Gamma_cosine_numerators']):
            hp=int(hs[KO+k]);hm=int(hs[KO-k]);assert hp==hm
            expected=mn[k]*hp*(1 if k==0 else 2)
            actual=int(s)<<320
            numer+=abs(actual-expected)
        discrepancy=F(numer,2**420)
        certified=input_error+discrepancy
        rows.append({'column_zero_based':i,'exact_midpoint_discrepancy':str(discrepancy),
                     'input_enclosure_L1_error':str(input_error),
                     'independent_Gamma_coefficient_L1_upper':str(certified),
                     'all_coefficients_verified':KO+1})
        if time.monotonic()-start>=600:raise RuntimeError('cached algebra time limit')
    data={'verdict':'PASS-CACHED-INTEGER-COEFFICIENT-ALGEBRA',
          'columns':32,'phase_inputs_exactly_checked':32*124*3,
          'Gamma_cosine_coefficients_exactly_checked':32*(KO+1),
          'exact_integer_polynomial_products':num_convolutions,
          'fresh_source_action_DFT_digamma_integral_spectrum_calls':0,
          'rows':rows,'wall_seconds':time.monotonic()-start,
          'CPU_seconds':time.process_time(),
          'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if emit:save(ROOT/'logs/CACHED_ALGEBRA_REPLAY.json',data)
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');a=p.parse_args()
    d=replay(a.emit);print(json.dumps({k:v for k,v in d.items() if k!='rows'}))
