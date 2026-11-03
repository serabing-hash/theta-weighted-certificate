"""Check fresh final statuses, reconstruct both matrices, and verify integer signs.

The stronger witness is freshly proposed by the unchanged exact_congruence.py;
all matrix entries and both sign witnesses are independently rechecked below
using Python Fraction/int arithmetic, not BLAS or floating sign decisions.
"""
import argparse,hashlib,importlib.util,json,math,time
from fractions import Fraction as F
from pathlib import Path


def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main(args):
 root=Path(args.fresh);out=Path(args.output)
 def read(rel):return load(root/rel)
 stages=['T','G','K'];parts=[read(f'results/{s}256_n3072/{s}'+('_lower_exact.json' if s=='T' else '_upper_exact.json')) for s in stages]
 source=read('results/frozen256_n3072/verified_components.json');f=F(source['coordinates']['F_trial_scalar_lower']);a=F(1,2048);n=256
 csha=sha(root/'results/frozen256_n3072/candidate.json')
 assert csha=='a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d'
 assert all(p['candidate_sha256']==csha and p['status']=='CERT' for p in parts+[source])
 exact_result=read('results/gate256_n3072_p400/result.json')
 assert exact_result['status']=='CERT'
 ldl=exact_result['interval_LDL_of_M_minus_gap_I']
 assert ldl['positive'] and len(ldl['pivots'])==256
 assert all(F(p['lower'])>0 for p in ldl['pivots'])
 conservative_result=read('results/conservative_gate/result.json')
 assert conservative_result['status']=='CERT_EXACT_INTEGER_SIGN'
 checker=Path(args.exact_checker)
 spec=importlib.util.spec_from_file_location('fresh_exact_sign_checker',checker);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 mod.A=root/'results/gate256_n3072_p400'
 mod.run(mod.A/'sufficient_gate_exact.json',F(1,2000))
 rows=[[[int(v) for v in row] for row in x['matrix_numerators']] for x in parts]
 reports=[]
 for name in ['gate256_n3072_p400','conservative_gate']:
  started=time.time();folder=root/'results'/name;path=folder/'sufficient_gate_exact.json';m=load(path);w=load(folder/'independent_congruence_certificate.json')
  assert m['candidate_sha256']==csha and F(m['a'])==a
  assert w['status']=='EXACT_INTEGER_POSITIVE_DEFINITE' and w['gate_sha256']==sha(path) and F(w['gap'])==F(1,2000)
  coeff=[F(4,int(parts[0]['common_denominator'])),-5*a/4/int(parts[1]['common_denominator']),-F(m['penalty'])/int(parts[2]['common_denominator']),a*f/4]
  den=math.lcm(*(x.denominator for x in coeff));cs=[int(x*den) for x in coeff]
  md=int(m['common_denominator']);mi=[[int(v) for v in row] for row in m['matrix_numerators']]
  assert len(mi)==n and all(len(r)==n for r in mi)
  for i in range(n):
   for j in range(n):
    value=sum(cs[h]*rows[h][i][j] for h in range(3))+(cs[3] if i==j else 0)
    assert value*md==mi[i][j]*den,(name,i,j)
  D=math.lcm(md,2000)
  assert D==int(w['matrix_denominator'])
  A=[[v*(D//md)-(D//2000 if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(mi)]
  Q=[[int(v) for v in row] for row in w['witness_integer_rows']]
  assert len(Q)==n and all(len(r)==n for r in Q)
  cols=list(zip(*Q));AQ=[[sum(x*y for x,y in zip(row,col)) for col in cols] for row in A];ac=list(zip(*AQ))
  H=[[sum(x*y for x,y in zip(qcol,acol)) for acol in ac] for qcol in cols]
  assert all(H[i][j]==H[j][i] for i in range(n) for j in range(n))
  margins=[r[i]-sum(abs(v) for j,v in enumerate(r) if j!=i) for i,r in enumerate(H)]
  assert min(margins)>0 and margins==[int(v) for v in w['strict_diagonal_dominance_margin_numerators']]
  reports.append({'gate':name,'status':'PASS','penalty':m['penalty'],'reconstructed_entries':n*n,'positive_integer_congruence_margins':n,'minimum_integer_margin':str(min(margins)),'gate_sha256':sha(path),'certificate_sha256':sha(folder/'independent_congruence_certificate.json'),'elapsed_seconds':time.time()-started})
  print('PASS',name,'65536 reconstructed entries,256 positive exact integer margins',flush=True)
 report={'status':'PASS','candidate_sha256':csha,'stronger_terminal_status':'CERT','stronger_positive_shifted_LDL_pivots':256,'conservative_terminal_status':'CERT_EXACT_INTEGER_SIGN','fresh_source_enclosures_required':True,'arithmetic_profile':'directed_integer_power_repair_v1','independent_sign_arithmetic':'Python Fraction and int','results':reports,'RH':'NOT_PROVED'}
 out.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
 if not __debug__:raise RuntimeError('Assertions must be enabled')
 p=argparse.ArgumentParser(description=__doc__)
 for x in ['fresh','exact-checker','output']:p.add_argument('--'+x,required=True)
 main(p.parse_args())
