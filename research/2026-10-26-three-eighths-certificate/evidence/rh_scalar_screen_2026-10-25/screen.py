#!/usr/bin/env python3
"""Single frozen scalar screen. Never import this module as a test fixture."""
import json, os, time, resource, traceback, signal
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path
P=70
DOWN=Context(prec=P,rounding=ROUND_FLOOR)
UP=Context(prec=P,rounding=ROUND_CEILING)
NEAR=Context(prec=P,rounding=ROUND_HALF_EVEN)
class I:
    def __init__(self,lo,hi=None):
        self.lo=D(lo); self.hi=D(lo if hi is None else hi)
        assert self.lo<=self.hi
    @staticmethod
    def cast(x): return x if isinstance(x,I) else I(x)
    def __add__(self,x):
        x=I.cast(x); return I(DOWN.add(self.lo,x.lo),UP.add(self.hi,x.hi))
    __radd__=__add__
    def __neg__(self): return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,x): return self+-I.cast(x)
    def __rsub__(self,x): return I.cast(x)+-self
    def __mul__(self,x):
        x=I.cast(x); pairs=[(a,b) for a in (self.lo,self.hi) for b in (x.lo,x.hi)]
        return I(min(DOWN.multiply(a,b) for a,b in pairs),max(UP.multiply(a,b) for a,b in pairs))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=I.cast(x); assert not x.lo<=0<=x.hi
        return self*I(DOWN.divide(D(1),x.hi),UP.divide(D(1),x.lo))
    def __rtruediv__(self,x): return I.cast(x)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        if n==2:
            hi=max(UP.multiply(self.lo,self.lo),UP.multiply(self.hi,self.hi))
            lo=D(0) if self.lo<=0<=self.hi else min(DOWN.multiply(self.lo,self.lo),DOWN.multiply(self.hi,self.hi))
            return I(lo,hi)
        y=I(1)
        for _ in range(n): y=y*self
        return y
    def exp(self): return I(NEAR.next_minus(NEAR.exp(self.lo)),NEAR.next_plus(NEAR.exp(self.hi)))
    def ln(self):
        assert self.lo>0
        return I(NEAR.next_minus(NEAR.ln(self.lo)),NEAR.next_plus(NEAR.ln(self.hi)))
    def sqrt(self):
        assert self.lo>=0
        low=NEAR.next_minus(NEAR.sqrt(self.lo)) if self.lo else D(0)
        return I(low,NEAR.next_plus(NEAR.sqrt(self.hi)))
    def realpow(self,x): return (self.ln()*x).exp()
    def data(self): return {'lo':str(self.lo),'hi':str(self.hi)}
def rat(n,d=1): return I(n)/d
def frac(f): return rat(f.numerator,f.denominator)
def imin(a,b): return I(min(a.lo,b.lo),min(a.hi,b.hi))
def imax0(a): return I(max(D(0),a.lo),max(D(0),a.hi))
def gate_le(a,b):
    a=I.cast(a); b=I.cast(b)
    return 'pass' if a.hi<=b.lo else ('fail' if a.lo>b.hi else 'inconclusive')
def atan_recip(m):
    # 128 alternating terms, even length: S <= atan(1/m) <= S+next term.
    s=sum((Fraction((-1)**j,(2*j+1)*m**(2*j+1)) for j in range(128)),Fraction(0))
    rem=Fraction(1,257*m**257)
    return I(frac(s).lo,frac(s+rem).hi)
def constants():
    pi=16*atan_recip(5)-4*atan_recip(239)
    # gamma = H_n-ln(n)-1/(2n)+sum B_2k/(2k n^2k),
    # remainder after k=11 has sign B24 and magnitude at most its term.
    n=256
    bs=[Fraction(1,6),Fraction(-1,30),Fraction(1,42),Fraction(-1,30),Fraction(5,66),Fraction(-691,2730),Fraction(7,6),Fraction(-3617,510),Fraction(43867,798),Fraction(-174611,330),Fraction(854513,138),Fraction(-236364091,2730)]
    h=sum((Fraction(1,j) for j in range(1,n+1)),Fraction(0))
    s=frac(h)-I(n).ln()-rat(1,2*n)
    for k,b in enumerate(bs[:11],1): s=s+frac(b/Fraction(2*k*n**(2*k)))
    remainder=frac(bs[11]/Fraction(24*n**24))
    euler=I((s+remainder).lo,s.hi)
    return pi,euler

def main():
    pi,euler=constants(); b=rat(1,4); theta=rat(9,10); eps=rat(1,8); q=rat(1,2)
    k=4*pi**2-6*pi
    def kt(j): return I(j**4)*(-pi*(j*j-1)).exp()
    ksum=sum((kt(j) for j in range(1,9)),I(0))
    kr=rat(10,9)**4*(-19*pi).exp()
    ktail=4*pi**2*kt(9)/(1-kr)
    K=4*pi**2*ksum+I(0,ktail.hi)
    W=K*(-pi).exp(); gamma=pi*(1-(-2*b).exp())
    BH=(K/k)*(rat(9,2)*b).exp()*((b/2).exp()+(-b/2).exp())/2
    aa=(1-theta)*pi/2
    def st(n): return I(n).ln()*I(n).realpow(rat(1,2)-theta)*(-aa*n).exp()
    ssum=sum((st(n) for n in range(2,258)),I(0))
    sr=rat(259,258)*(-aa).exp()
    stail=st(258)/(1-sr)
    S=K.realpow((1-theta)/2)*(ssum+I(0,stail.hi))
    M=2*I(2).sqrt()*pi*W.realpow(1-theta/2)+2*W.sqrt()*S
    m0=pi.exp()/K
    c=pi.ln()+euler+pi/2+3*I(2).ln()
    # Complete exact prime-power enumeration n<=54, with exp(4)<55 certified below.
    assert I(54).ln().hi<4<I(55).ln().lo
    primes=[p for p in range(2,55) if all(p%d for d in range(2,p))]
    pp=[]
    for p in primes:
        n=p
        while n<=54:
            pp.append((n,p,I(n).ln(),I(p).ln()/I(n).sqrt())); n*=p
    pp.sort()
    def active(threshold):
        out=[]
        for n,p,logn,weight in pp:
            if logn.hi<threshold.lo: out.append((n,p,weight))
            elif logn.lo>threshold.hi: pass
            else: raise ArithmeticError('unresolved strict prime cutoff')
        return out
    def beta(r): return sum((w for n,p,w in active(2*r)),I(0))+sum((w for n,p,w in active(r)),I(0))
    rows=[]
    for rnum in [3,4,5,6,7,8]:
        R=rat(rnum,4); L=R-b
        defect=gamma*(2*R).exp()-(2*BH/eps).ln()
        eta=2*M**2*K.realpow(theta)*(4*theta*R-pi*theta*(2*R).exp()).exp()/eps
        hardy=gate_le(0,defect); interface=gate_le(eta,eps/2)
        admission='pass' if hardy==interface=='pass' else ('fail' if 'fail' in (hardy,interface) else 'inconclusive')
        row={'R':str(rnum)+'/4','L':str(rnum-1)+'/4','hardy_defect':defect.data(),'hardy_gate':hardy,'etabar':eta.data(),'interface_gate':interface,'admission':admission}
        if admission!='pass':
            row['conclusion']='not admitted by sufficient bridge' if admission=='fail' else 'inconclusive at frozen precision'
            rows.append(row); continue
        t0=eps-eta; br=beta(R); bl=beta(L)
        T=(q*t0/K)*(pi*(2*L).exp()-4*L).exp()
        DD=bl-br+T
        root=(DD**2+4*br**2).sqrt()
        K2=bl+2*br**2/(root+DD) if DD.lo>0 else (bl+br-T+root)/2
        khat=imin(br-q*t0*m0,K2)
        caprhs=(1+(pi*1024/R)**2).ln()/2
        opts=[]
        for mode,kh,qq in [('baseline',br,I(0)),('weighted',khat,q)]:
            for a0 in [0,1]:
                F=c+kh+a0
                realcount=R/pi*imax0((2*F).exp()-1).sqrt()
                lo=max(1,int(realcount.lo.to_integral_value(rounding=ROUND_CEILING)))
                hi=max(1,int(realcount.hi.to_integral_value(rounding=ROUND_CEILING)))
                astar=a0+(1-qq)*t0*m0
                gate=gate_le(F,caprhs)
                opts.append({'mode':mode,'a0':a0,'F':F.data(),'a_star':astar.data(),'N_req_integer_bounds':[lo,hi],'N_req_exact':lo if lo==hi else None,'cap_gate':gate,'conclusion':'cell-count candidate only' if gate=='pass' else ('sufficient count exceeds cap' if gate=='fail' else 'inconclusive at frozen precision')})
        row.update({'t0':t0.data(),'beta_R':br.data(),'beta_L':bl.data(),'p_R':len(active(2*R)),'active_prime_powers':[n for n,p,w in active(2*R)],'T':T.data(),'D':DD.data(),'K2':K2.data(),'Khat':khat.data(),'cap_rhs':caprhs.data(),'options':opts})
        rows.append(row)
    return {'status':'completed','precision_decimal_digits':P,'arithmetic':'directed Decimal interval; transcendental nearest then outward neighbor','frozen':{'b':'1/4','theta':'9/10','epsilon':'1/8','q':'1/2','a0':[0,1],'R':['3/4','1','5/4','3/2','7/4','2'],'L':'R-1/4','integer_cap':1024,'K_terms':8,'Sbar_integer_terms':256,'Sbar_indices':'2..257'},'constants':{name:val.data() for name,val in [('pi',pi),('gamma_E',euler),('K',K),('K_tail_upper',ktail),('K_tail_ratio',kr),('Sbar',S),('S_unscaled_tail_upper',stail),('S_tail_ratio',sr),('Mbar',M),('B_H',BH),('gamma',gamma),('m0',m0),('c',c)]},'rows':rows,'limitations':'Only sufficient admission and cell-count gates. No residual sign, eigenvalues, matrix, quadrature, certificate or RH conclusion.'}

if __name__=='__main__':
    path=Path(__file__).with_name('output.json'); start=time.monotonic()
    path.write_text(json.dumps({'status':'started','pid':os.getpid()}))
    try:
        assert resource.getrlimit(resource.RLIMIT_AS)[0]<=256*1024**2
        assert resource.getrlimit(resource.RLIMIT_CPU)[0]<=60
        result=main(); code=0
    except BaseException as exc:
        result={'status':'inconclusive_execution_failure','error':repr(exc),'traceback':traceback.format_exc()}; code=1
    result['elapsed_wall_seconds']=time.monotonic()-start
    usage=resource.getrusage(resource.RUSAGE_SELF)
    result['cpu_seconds']=usage.ru_utime+usage.ru_stime
    result['max_rss_KiB']=usage.ru_maxrss
    path.write_text(json.dumps(result,indent=2)+'\n')
    receipt={'status':'terminal','exit_code':code,'wall_alarm_seconds':59,'cpu_limit_seconds':59,'address_space_limit_bytes':268435456,'process_tree':'single process; guard exec replaces itself; no children','automatic_retries':0}
    path.with_name('guard_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'elapsed_wall_seconds':result['elapsed_wall_seconds'],'max_rss_KiB':result['max_rss_KiB']}),flush=True)
    raise SystemExit(code)
