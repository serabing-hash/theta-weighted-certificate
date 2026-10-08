"""Immutable rank32 inputs and validated finite analytic action format.

All stored approximants are ordinary-dx U coordinates.  No eigensolver,
inverse, trial search, or residual Gram is used in this task.
"""
from pathlib import Path
from fractions import Fraction as F
from math import ceil
import csv, gc, hashlib, json, os, resource, time
from flint import arb, acb, acb_poly, arb_mat, fmpq, ctx

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'sources/fixed_inputs'
PREC = 160
ctx.prec = PREC
N = 65536
K = 8192
DEN_BITS = 140
OUT_BITS = 100
PERIOD = 32 * arb.pi()
COUNTS = {}

def A(x):
    if isinstance(x, F):
        return arb(fmpq(x.numerator, x.denominator))
    return arb(x)

def exact(x):
    n, e = x.man_exp(); n, e = int(n), int(e)
    return F(n << e) if e >= 0 else F(n, 1 << (-e))

def upper(x): return exact(A(x).abs_upper())
def pad(x, e): return x + arb(0, A(e).abs_upper())
def count(k, n=1): COUNTS[k] = COUNTS.get(k, 0) + n
def fracstr(x): return str(F(x))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def save(p, data):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + '.partial')
    with tmp.open('w') as f: json.dump(data, f, separators=(',', ':'))
    os.replace(tmp, p)

def guard(start, limit=600):
    if time.monotonic() - start >= limit:
        raise RuntimeError('fixed wall-clock budget reached')
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= 512 * 1024:
        raise RuntimeError('fixed RSS 512 MiB budget reached')

def progress(start, phase):
    guard(start)
    d = {'phase': phase, 'wall_seconds': time.monotonic()-start,
         'CPU_seconds': time.process_time(),
         'peak_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'counts': COUNTS.copy()}
    save(ROOT/'logs/PROGRESS.json', d)
    print(json.dumps(d), flush=True)

def quantize(x, bits):
    f = exact(x.mid()) * (1 << bits)
    n = f.numerator // f.denominator
    m = arb((n, -bits))
    return n, upper(abs(x-m))

def record(x, bits=DEN_BITS):
    n, err = quantize(x, bits)
    v = err * (1 << bits)
    rn = -(-v.numerator // v.denominator)
    return [str(n), str(rn)]

def restore(r, bits=DEN_BITS):
    return pad(arb((int(r[0]), -bits)), arb((int(r[1]), -bits)))

def load_inputs():
    rows = list(csv.DictReader((INPUT/'retained_cells_exact.csv').open()))
    assert len(rows) == 124
    T = [list(map(int, r)) for r in csv.reader((INPUT/'T32_dyadic_numerators.csv').open())]
    C = [list(map(int, r)) for r in csv.reader((INPUT/'C32_dyadic_numerators.csv').open())]
    assert len(T) == 372 and all(len(r) == 32 for r in T)
    assert len(C) == 32 and all(len(r) == 372 for r in C)
    alpha, m = [], []
    for s, row in enumerate(rows):
        assert int(row['block_index']) == s and F(row['width']) == F(1,2)
        c, V = F(row['centre']), F(row['V_upper'])
        assert 0 < V < 12 and (16*c).denominator == 1
        alpha.append((A(V)/arb.pi()).sqrt())
        assert alpha[-1].upper() < 2
        m.append(int(16*c))
    assert max(m) < 16*2048
    Ai=[]
    for i in range(32):
        e=2*sum((F(abs(T[3*s][i]),2**30)*F(97,96)
                 +F(abs(T[3*s+1][i]),2**30)/4
                 +F(abs(T[3*s+2][i]),2**30)/48 for s in range(124)),F(0))
        Ai.append(e)
        assert 0 < e < 128
    return rows,T,C,alpha,m,Ai

ROWS,T,C,ALPHA,SHIFTS,AI = load_inputs()
MMAX=max(SHIFTS)
KOUT=K+MMAX
TMAT=arb_mat([[arb((v,-30)) for v in row] for row in T])

def finite_source(x):
    """Exact eight-term source function used in the approximant itself.

    Primitive interval arithmetic is separate from the proved full-source
    discrepancy <2^-320. Even reflection is explicit.
    """
    x=abs(A(x)); z=arb.pi()*(2*x).exp(); S=arb(0)
    for n in range(1,9):
        t=z*n*n; S+=(4*t*t-6*t)*(-t).exp()
    a=S/(1+(-x).exp())
    kappa=(x/2).exp()*S
    count('finite_theta_source_evaluations')
    count('finite_theta_terms',8)
    if not a.is_finite() or not a.lower() > 0:
        raise ArithmeticError('finite theta positivity/evaluation failure')
    return kappa,a

def feature_polynomials(x):
    """All 372 source-free Q_j, with the original Cholesky coordinates."""
    x=A(x); out=[]
    for al,m in zip(ALPHA,SHIFTS):
        sn,co=(A(F(m,16))*x).sin_cos()
        out.extend([al*(1-x*x/96)*co,
                    -al*x*sn/(4*arb(3).sqrt()),
                    -al*x*x*co/(48*arb(5).sqrt())])
    count('feature_trigonometric_pairs',124)
    return out

def trial_P(i,x):
    q=feature_polynomials(x)
    return sum((z*arb((T[j][i],-30)) for j,z in enumerate(q)),arb(0))

def prime_terms():
    pairs=[(2,2),(3,3),(4,2),(5,5),(7,7),(8,2),(9,3),(11,11),
           (13,13),(16,2),(17,17),(19,19),(23,23),(25,5),(27,3),
           (29,29),(31,31),(32,2)]
    out=[(n,A(p).log()/A(n).sqrt(),A(n).log()) for n,p in pairs]
    assert sum((z[1] for z in out),arb(0)).upper()<32
    return out

def analytic_budget():
    t=(-A(F(1,128))).exp(); k=K+1; c=A(F(MMAX,16))
    B=A(F(k,16))+c
    tail=40*2**20*t**k*(B*B/(1-t)+B*t/(8*(1-t)**2)
                              +t*(1+t)/(256*(1-t)**3))
    copies=2**23*A(1).exp()*(-PERIOD/2).exp()/(1-(-PERIOD/2).exp())
    delta=F(14*(9*32**2+24*32+20),27*4**32)
    Y=arb(4).exp()
    I3=(-3*Y).exp()*(Y**3/3+Y**2/3+2*Y/9+A(F(2,27)))
    I2=(-3*Y).exp()*(Y**2/3+2*Y/9+A(F(2,27)))
    assert (164*I3).upper() < A(F(1,2**190))
    assert (164*I2).upper() < A(F(1,2**190))
    assert (128*9**4*arb(-243).exp()).upper() < A(F(1,2**320))
    assert (512*A(400)**4*arb(-1000).exp()).upper() < A(F(1,2**1000))
    assert PERIOD.lower()>96
    return {'Gamma_frequency_tail_per_AI':str(upper(tail)/2),
            'Gamma_periodic_copies_per_AI':str(upper(copies)/2),
            'infinite_prime_tail_per_AI':str(delta*2**10),
            'finite_action_exterior_per_AI':str(F(1,2**50)),
            'theta8_uniform_source_error':'1/'+str(2**320),
            'base_coefficient_model_error':'1/'+str(2**300),
            'base_analytic_coefficient_majorant':2**20,
            'strip_half_width':'1/8',
            'exterior_b_polynomial_norm_upper':'1/'+str(2**95),
            'exterior_p0_norm_upper':'1/'+str(2**95),
            'native_tail_I3_upper':str(upper(164*I3)),
            'native_tail_I2_upper':str(upper(164*I2)),
            'Ai_exact':[str(x) for x in AI]}

def load_base():
    out={}
    for kind,r in [('a',r) for r in range(5)]+[('kappa',r) for r in range(3)]:
        d=json.loads((ROOT/'outputs'/f'BASE_{kind}_{r}.json').read_text())
        assert d['K']==K and d['component']==('imag' if r%2 else 'real')
        values=[restore(v) for v in d['values']]
        assert len(values)==K+1
        out[(kind,r)]=values
    return out

def coefficient(base,kind,r,k):
    if abs(k)>K: raise ValueError('stored base coefficient outside range')
    z=base[(kind,r)][abs(k)]
    if r%2: return acb(0,z if k>=0 else -z)
    return acb(z,0)

def moment(base,kind,r,k,trig):
    if (trig=='cos' and r%2) or (trig=='sin' and not r%2):return arb(0)
    if k==0 and trig=='sin':return arb(0)
    kk=abs(k)
    if kk<=K:
        z=PERIOD*base[(kind,r)][kk]
        return z if trig=='cos' else (-z if k>0 else z)
    e=PERIOD*2**20*(-A(F(kk,128))).exp()
    return arb(0,e.abs_upper())

def feature_terms(j):
    al=ALPHA[j//3]
    if j%3==0:return [(0,'cos',al),(2,'cos',-al/96)]
    if j%3==1:return [(1,'sin',-al/(4*arb(3).sqrt()))]
    return [(2,'cos',-al/(48*arb(5).sqrt()))]

def full_approximation(i,x,descriptor=None):
    """Evaluate the stored finite analytic function, not H or an integral.

    Ordinary-dx compact support [-2,2]; endpoints may use either value.
    This is not a Chebyshev-panel or weighted-space coefficient packet.
    """
    x=A(x)
    if x.lower() < -2 or x.upper()>2:
        if x.upper()<-2 or x.lower()>2:return arb(0),{}
        raise ValueError('input interval straddles approximant support')
    d=descriptor or json.loads((ROOT/'outputs'/f'ACTION_{i:02d}.json').read_text())
    co=[arb((int(n),-OUT_BITS)) for n in d['Gamma_cosine_numerators']]
    # Rectangular complex Horner wraps exponentially on a long unit-circle
    # polynomial. Direct validated cosine terms evaluate the same formula.
    if x.is_zero():
        ga=sum(co,arb(0))
    else:
        ga=sum((c*(x*A(F(k,16))).cos() for k,c in enumerate(co)
                if not c.is_zero()),arb(0))
    count('stored_Gamma_cosine_term_evaluations',
          sum(not c.is_zero() for c in co) if not x.is_zero() else 0)
    q=feature_polynomials(x)
    P=sum((v*arb((T[j][i],-30)) for j,v in enumerate(q)),arb(0))
    kp,a=finite_source(x);b=a.sqrt();p0=2*b*(x/2).cosh()
    cg=arb.pi().log()+arb.const_euler()+arb.pi()/2+3*arb.const_log2()
    prime=arb(0)
    for n,weight,s in prime_terms():
        for sign in (-1,1):
            y=x+sign*s; ky,ay=finite_source(y)
            prime+=weight*ay*trial_P(i,y)
            count('approximant_prime_shift_evaluations')
    frame=[arb((int(n),-OUT_BITS)) for n in d['frame_numerators']]
    pole=arb((int(d['pole_numerator']),-OUT_BITS))
    parts={'shift':b*P/16,'Gamma':b*ga,'local':-cg*a*b*P,
           'finite_prime':-b*prime,'pole':p0*pole/2,
           'full_372_frame':b*sum((v*c for v,c in zip(q,frame)),arb(0))}
    value=sum(parts.values(),arb(0))
    if not value.is_finite() or not value.rad()<A(F(1,2**60)):
        raise ArithmeticError('stored-function finite evaluation gate: '+value.repr())
    count('complete_stored_function_evaluations')
    return value,parts
