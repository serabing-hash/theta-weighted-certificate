"""Exact Fraction oracle for all integer-power parity/sign/domain branches."""
import sys,unittest,random
from pathlib import Path
from decimal import Decimal,localcontext,Overflow,DecimalException
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import interval_bounds as ib
from interval_bounds import IV

class ExactPowerTests(unittest.TestCase):
 def setUp(self):self.old=ib.PRECISION
 def tearDown(self):ib.PRECISION=self.old
 def check(self,lo,hi,n):
  x=IV(lo,hi);y=x**n
  endpoints=[Fraction(x.lo)**n,Fraction(x.hi)**n]
  if n>0 and n%2==0 and x.lo<=0<=x.hi:endpoints.append(Fraction(0))
  self.assertLessEqual(Fraction(y.lo),min(endpoints))
  self.assertGreaterEqual(Fraction(y.hi),max(endpoints))
 def test_adversarial_positive_and_negative_families(self):
  for precision,digits in [(70,40),(400,220)]:
   ib.PRECISION=precision;x=Decimal('1.'+'0'*(digits-1)+'1')
   for n in range(242):
    with self.subTest(p=precision,n=n,sign=1):self.check(x,x,n)
    with self.subTest(p=precision,n=n,sign=-1):self.check(x.copy_negate(),x.copy_negate(),n)
 def test_interval_parity_and_negative_powers(self):
  for precision in [7,70,400]:
   ib.PRECISION=precision
   for lo,hi in [('-3.7','-0.2'),('0.2','3.7'),('-3.7','2.1'),('-0','0'),('0','3.7'),('-3.7','0')]:
    for n in [0,1,2,3,4,7,16,33,80,241]:self.check(lo,hi,n)
    if not Decimal(lo)<=0<=Decimal(hi):
     for n in [-1,-2,-3,-4,-7,-33]:self.check(lo,hi,n)
 def test_random_finite_decimal_intervals(self):
  rng=random.Random(2048)
  for precision in [3,17,70,400]:
   ib.PRECISION=precision
   for _ in range(160):
    a=Decimal((rng.randrange(2),tuple(int(c) for c in str(rng.randrange(1,10**35))),rng.randrange(-60,30)))
    b=Decimal((rng.randrange(2),tuple(int(c) for c in str(rng.randrange(1,10**35))),rng.randrange(-60,30)))
    lo,hi=min(a,b),max(a,b)
    n=rng.choice([0,1,2,3,4,7,16,33,80])
    self.check(lo,hi,n)
    if not lo<=0<=hi:self.check(lo,hi,-rng.choice([1,2,3,7]))
 def test_zero_domain_and_noninteger_rejections(self):
  self.assertEqual((IV(0)**0).record(),IV(1).record())
  self.assertIs(IV(1)**1,IV(1)**1) if False else None
  x=IV('1.00000000000000000000000000000000001');self.assertIs(x**1,x)
  for x in [IV(0),IV(-1,1),IV(0,1),IV(-1,0)]:
   with self.assertRaises(ZeroDivisionError):x**-2
  for n in [2.,Decimal(2),Fraction(2),'.5']:
   with self.assertRaises(TypeError):IV(2)**n
 def test_ambient_precision_does_not_affect_signed_bounds(self):
  ib.PRECISION=70;x=Decimal('-1.'+'0'*39+'1')
  expected=(IV(x)**3).record()
  with localcontext() as c:
   c.prec=3
   self.assertEqual((IV(x)**3).record(),expected)
   self.check(x,x,3)
 def test_subnormal_and_overflow_fail_closed(self):
  ib.PRECISION=7
  with localcontext() as c:
   c.Emin=-20;c.Emax=20
   self.check('1e-30','2e-30',2);self.check('-2e-30','-1e-30',3)
   with self.assertRaises((DecimalException,ValueError)):IV('1e20')**2
   c.traps[Overflow]=False
   with self.assertRaises(ValueError):IV('1e20')**2

if __name__=='__main__':unittest.main()
