"""Small exponent-range tests of gradual underflow and fail-closed overflow."""
import argparse,importlib.util,sys,json,hashlib
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_DOWN,Overflow,Underflow
from fractions import Fraction
sys.dont_write_bytecode=True
parser=argparse.ArgumentParser()
parser.add_argument('--snapshot',required=True)
parser.add_argument('--output',required=True)
args=parser.parse_args()
source=Path(args.snapshot)/'interval_bounds.py'
spec=importlib.util.spec_from_file_location('boundary_iv',source);ib=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ib;spec.loader.exec_module(ib)
count=0;rejected=0;failures=[]
for p in [1,7,28,70]:
 ib.PRECISION=p
 for text in ['1E-8','-1E-8','1E-9','-1E-9']:
  for n in [2,3,9,80]:
   with localcontext() as c:
    c.prec=7;c.rounding=ROUND_DOWN;c.Emin=-9;c.Emax=9
    c.traps[Underflow]=False
    v=ib.IV(text)**n
   exact=Fraction(Decimal(text))**n
   if not Fraction(v.lo)<=exact<=Fraction(v.hi):failures.append([p,text,n,v.record()])
   count+=1
 for text,n in [('1E+8',2),('-1E+8',3),('1E-8',-2),('-1E-8',-3)]:
  for trap in [False,True]:
   try:
    with localcontext() as c:
     c.prec=7;c.Emin=-9;c.Emax=9;c.traps[Overflow]=trap
     v=ib.IV(text)**n
   except (ValueError,Overflow):rejected+=1
   else:failures.append({'overflow_not_rejected':[p,text,n,trap,v.record()]})
out={'status':'PASS' if not failures else 'FAIL','finite_exact_enclosure_tests':count,
 'overflow_fail_closed_tests':rejected,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'Emin':-9,'Emax':9,'precisions':[1,7,28,70],'failures':failures}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));raise SystemExit(bool(failures))
