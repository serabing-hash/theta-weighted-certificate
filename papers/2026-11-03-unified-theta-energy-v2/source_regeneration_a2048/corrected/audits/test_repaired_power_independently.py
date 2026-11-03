"""Independent exact-rational audit of a separate candidate IV power repair.

Reads/imports the supplied snapshot without changing it; only synthetic
primitive inputs are evaluated. Never runs a producer or certificate pipeline.
"""
import argparse, hashlib, importlib.util, json, random, sys
from decimal import Decimal, localcontext, ROUND_DOWN, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True

def exact_image(lo, hi, n):
    lo,hi=Fraction(lo),Fraction(hi)
    if n < 0 and lo <= 0 <= hi:
        raise ZeroDivisionError
    if n == 0:return Fraction(1),Fraction(1)
    a,b=lo**n,hi**n
    if n>0 and n%2==0 and lo<=0<=hi:return Fraction(0),max(a,b)
    return min(a,b),max(a,b)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True)
    ap.add_argument('--output',required=True);args=ap.parse_args()
    source=Path(args.snapshot).resolve()/'interval_bounds.py'
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    spec=importlib.util.spec_from_file_location('independent_repaired_iv',source)
    ib=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ib;spec.loader.exec_module(ib)
    failures=[];count=0;by_precision={};rejections=0
    def check(lo,hi,n,p):
        nonlocal count
        lo,hi=Decimal(lo),Decimal(hi)
        ib.PRECISION=p
        qlo,qhi=exact_image(lo,hi,n)
        # A deliberately unrelated ambient context catches context-rounded
        # abs/negation or arithmetic leaking outside the directed context.
        with localcontext() as ambient:
            ambient.prec=7;ambient.rounding=ROUND_DOWN
            got=ib.IV(lo,hi)**n
        count+=1;by_precision[str(p)]=by_precision.get(str(p),0)+1
        if not Fraction(got.lo)<=qlo<=qhi<=Fraction(got.hi):
            failures.append({'p':p,'lo':str(lo),'hi':str(hi),'n':n,'got':got.record()})
    x='1.'+'0'*39+'1'
    for n in range(2,242):
        check(x,x,n,70);check('-'+x,'-'+x,n,70)
    bases=['0','1','-1','2','-2','0.2','-0.2','1E-80','-1E-80','1E+80','-1E+80',x,'-'+x,
           '0.'+'9'*70,'1.'+'0'*219+'1','-1.'+'0'*219+'1']
    exponents=[-241,-81,-80,-9,-4,-3,-2,-1,0,1,2,3,4,9,17,80,81,241]
    for p in [1,7,28,70,400]:
        for base in bases:
            for n in exponents:
                if Decimal(base)==0 and n<0:continue
                check(base,base,n,p)
        for lo,hi in [('0','2'),('-2','0'),('-2','3'),('-3','2'),('-3','-2'),('2','3'),
                      ('-1E-80','1E-80'),('0.9999999999999999999999999999999999999999',x)]:
            for n in exponents:
                if Decimal(lo)<=0<=Decimal(hi) and n<0:continue
                check(lo,hi,n,p)
        rng=random.Random(20261103+p)
        for j in range(20):
            a=rng.randrange(-10**42,10**42);b=rng.randrange(-10**42,10**42)
            lo,hi=sorted([Decimal((int(v<0),tuple(map(int,str(abs(v)))),-41)) for v in [a,b]])
            for n in [-9,-4,-1,0,1,2,3,4,9,80,81]:
                if lo<=0<=hi and n<0:continue
                check(lo,hi,n,p)
    # Zero-containing negative powers must reject rather than return an interval.
    for lo,hi in [('0','0'),('-1','0'),('0','1'),('-1','1')]:
        for n in [-1,-2,-3,-80]:
            try:ib.IV(lo,hi)**n
            except ZeroDivisionError:rejections+=1
            else:failures.append({'zero_negative_rejection_missing':[lo,hi,n]})
    for exponent in [2.0,Decimal(2),Fraction(2), '2', None]:
        try:ib.IV(2)**exponent
        except TypeError:rejections+=1
        else:failures.append({'noninteger_type_rejection_missing':str(exponent)})
    after=hashlib.sha256(source.read_bytes()).hexdigest()
    if after!=before:failures.append({'source_changed_during_review':True})
    out={'status':'PASS' if not failures else 'FAIL','source_file':source.name,
         'source_sha256_before':before,'source_sha256_after':after,
         'exact_rational_interval_tests':count,'tests_by_precision':by_precision,
         'expected_exceptions_passed':rejections,'failures':failures,
         'ambient_context':'precision7 ROUND_DOWN; each IV operation must set own context',
         'scope':'Synthetic primitive tests support the separate inductive proof; not an actual-operand replay or universal proof by testing.'}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='failures'},indent=2))
    if failures:print('failures',len(failures),failures[:3])
    raise SystemExit(bool(failures))

if __name__=='__main__':main()
