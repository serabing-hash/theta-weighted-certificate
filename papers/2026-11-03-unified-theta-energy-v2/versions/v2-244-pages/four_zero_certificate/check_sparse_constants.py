#!/usr/bin/env python3
"""Verify the explicit scalar choices in the assumed sparse-window theorem.
Uses upper theta envelope constants. Never constructs exp(2**512).
"""
from flint import arb,ctx
from pathlib import Path
import json
ctx.prec=160
checks={}
def check(name,condition):
    checks[name]=bool(condition)
    assert condition,name
p=arb.pi();e=arb(1).exp();ln2=arb(2).log();ln3=arb(3).log()
C4=arb(42);C6=arb(700)
cW=(4*p*p-6*p)/2;m0=cW*(-p*e*e).exp();LW=C6/cW
D0=10*arb(18)**(arb(3)/2)
# The largest candidate can be checked by inequalities, without float ordering.
B=2*C4*D0*e/m0
for k,x in enumerate([arb(1),4*e,2*C4*e.sqrt()/m0,2*C6*e.sqrt()/m0]):
    check('B_dominates_'+str(k),B>=x)
K=arb(2)**16;b=arb(13)/2;d=arb(7)/2
absorb=(B.log()/(2*ln3)+d+(2*B).log()/ln3+(b+1)*(1+K.log()/(2*ln3)))/K
check('uniform_absorption',absorb<p/2)
check('K_at_least_e_squared',K>=e*e)
K1=12*K.sqrt()+4/e/(1-1/e)**2
K2=K*(D0*(LW*e*e).exp()+LW+2)
C0=arb(8);A0=C0+1;B0=C0+2;L0=1+B0.log()
B1=K2*A0**4*L0;CX=K*A0*L0+5+2*arb(3).log()
G0=6+arb(9).log();cg=p.log()-arb('0.25').digamma()
E0=2*G0+cg.abs_upper()+12*CX.sqrt();Cstar=8*E0*B1+16
check('K1_below_2pow12',K1<arb(2)**12)
check('B1_below_2pow800',B1<arb(2)**800)
check('Cstar_below_2pow800',Cstar<arb(2)**800)
check('cGamma_below_6',cg.abs_upper()<6)

t0=arb(2)**512
# U=exp(t0), so the following tests are in the logarithmic coordinate.
log_condition38=arb(16).log()+2*B1.log()+10*t0.log()-2*t0
check('sparse_condition_38',log_condition38<-(arb(8).log()))
condition39=K1*(A0*(B0*t0).log()/t0).sqrt()+cg.abs_upper()/t0
check('sparse_condition_39',condition39<arb(1)/8)
row_first=Cstar*((arb(2)**17+arb(4)/3)/t0**2+arb(2)**(arb(19)/2)/t0**3)
check('sparse_row_first_two',row_first<arb(1)/8)
log_row_last=Cstar.log()+(2+arb(2)**(arb(11)/2)).log()+5*t0.log()-t0
check('sparse_row_last',log_row_last<-arb(8).log())
check('threshold_gt_18',t0>18)
check('low_carriers_below_U_over2',t0>arb(62).log())
check('low_envelope_derivative_threshold',t0>(2*K2*16*arb(3).log()).log())
check('low_complexity_budget',1<8*t0)
# K_V^2<32 and Cstar<2^800 give epsilon<=2^1606*Theta(exp(t0)).
# Theta(exp(t)) <= 17*t^11*exp(-t) < 2^5*t^11*exp(-t), for t>=1.
log_epsilon_bound=(1606+5+11*512)*ln2-t0
check('epsilon_below_1_over_128',log_epsilon_bound<-7*ln2)

data={"status":"PASS for scalar conditions of the stated sparse analytical input",
      "C0":"8","K":"2^16","log_U":"2^512", "U":"exp(2^512)",
      "absorption_expression":str(absorb),"log2_K2":str(K2.log()/ln2),
      "log2_Cstar":str(Cstar.log()/ln2),"Cstar_upper":"2^800",
      "epsilon_upper":"1/128", "checks":checks,
      "scope":"These arithmetic checks do not independently prove the exponential-polynomial "
              "envelope or sparse-window theorem. They verify its explicit constant recipe. "
              "The enormous threshold is not a practical numerical cutoff."}
Path(__file__).with_name('SPARSE_CONSTANTS.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
