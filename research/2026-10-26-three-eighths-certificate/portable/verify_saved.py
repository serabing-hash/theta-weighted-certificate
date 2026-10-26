#!/usr/bin/env python3
"""Portable identity + exact saved-ledger consistency checks. NOT a producer rerun."""
import hashlib,json,struct,ast,sys,re
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence'; V1=E/'rh_full_rigorous_certificate_2026-10-25'; V2=E/'rh_full_rigorous_certificate_v2_2026-10-25'; V3=E/'rh_full_rigorous_certificate_v3_2026-10-25'; V4=E/'rh_full_rigorous_certificate_v4_2026-10-25'
count=0
def check(c,msg):
 global count
 if not c: raise ValueError(msg)
 count+=1
def j(p):return json.loads(p.read_text())
def f(x):return Q.from_float(float(x))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def npy_data(p):
 b=p.read_bytes();check(b[:6]==b'\x93NUMPY','NPY magic');v=b[6];off=10 if v==1 else 12;n=int.from_bytes(b[8:off],'little');h=ast.literal_eval(b[off:off+n].decode('latin1'));check(h['descr']=='<f8' and not h['fortran_order'],'NPY format');return h,b[off+n:]
def main():
 for line in (ROOT/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split('  ',1);p=(ROOT/name).resolve();check(p.is_relative_to(ROOT),'manifest containment');check(p.is_file() and sha(p)==digest,'manifest '+name)
 for r in j(ROOT/'SOURCE_ORIGINS.json')['files']:check(sha(ROOT/r['path'])==r['public_sha256'],'public origin '+r['path'])
 scalar=j(E/'rh_scalar_screen_2026-10-25/output.json');row=next(r for r in scalar['rows'] if Q(r['R'])==1)
 expected_constants={'PI':scalar['constants']['pi'],'CG':scalar['constants']['c'],'T0':row['t0']}
 for header in list(E.glob('rh_full_rigorous_certificate*/inputs.hpp'))+[E/'rh_two_direction_certificate_2026-10-25/inputs.hpp']:
  constants=dict((name,(Q(lo),Q(hi))) for name,lo,hi in re.findall(r'const I (\w+)\("([^"]+)","([^"]+)"\)',header.read_text()))
  for name,bound in expected_constants.items():check(constants[name]==(Q(bound['lo']),Q(bound['hi'])),'scalar-to-C++ constant identity')
 plan=j(V3/'refinement_plan.json');old=j(V2/'H_domain_ledger.json');src={int(r['template']):f(r['used_upper']) for r in old['panels'] if not r.get('analytic_tail_reused',False)}
 total=Q(0);cost=0;seen=set();parents=[];patch=[]
 for r in plan['panels']:
  i,k=int(r['template']),int(r['split']);check(i not in seen and i in src and k>=1 and k&(k-1)==0,'dyadic split');check(Q(r['old_bound_fraction'])==src[i] and Q(r['new_bound_fraction'])==src[i]/k**4,'exact child budget');seen.add(i);total+=src[i]/k**4;cost+=k;parents.append(dict(template=i,split=1,child=0,sign=1))
  if k>1:patch+=[dict(template=i,split=1,child=0,sign=-1)]+[dict(template=i,split=k,child=t,sign=1) for t in range(k)]
 check(len(src)==58 and seen==set(src) and cost==130,'full panel coverage');check(total==Q(plan['quad_budget_fraction']) and total<=Q(1,128) and total<=f(plan['quad_budget_upper']),'total exact budget')
 for v,tasks,n in [(V3,patch,104),(V4,parents,58)]:
  schedule=j(v/'POINT_SCHEDULE.json');check(schedule['tasks']==tasks and schedule['point_tasks']==n,'point schedule');led=j(v/('POINT_PATCH_LEDGER.json' if v==V3 else 'HSAFE_LEDGER.json'));check(led['point_tasks']==n and len(led['tasks'])==n,'point coverage')
  for a,b in zip(led['tasks'],tasks):check(all(a[k]==x for k,x in b.items()),'task identity')
 ledger=j(V4/'error_ledger.json');delta=f(ledger['total_error_upper']);check(sum(map(f,ledger['components'].values()),Q(0))<=delta,'total error outward sum');check(f(ledger['components']['composite_quadrature'])>=total,'quadrature component')
 inertia=j(V4/'inertia/inertia_ledger.json');check(inertia['dimension']==552 and inertia['trial_dimension']==551,'restriction dimensions');check(f(inertia['delta_upper_binary64'])==delta and f(float.fromhex(inertia['delta_upper_binary64_hex']))==delta,'delta identity');check(sha(V4/'Fmid_composite.bin')==inertia['center_binary64_sha256'],'center identity')
 check(f(inertia['trial_gram_defect_norm_upper'])<1 and inertia['trial_columns_independent'] is True,'saved Gram premise');check(delta*f(inertia['trial_norm_squared_upper'])<=f(inertia['input_loewner_error_after_congruence_upper']),'propagated error');check(f(inertia['positive_subspace_margin_lower'])<=f(inertia['projected_center_gershgorin_lower'])-f(inertia['input_loewner_error_after_congruence_upper']),'saved margin subtraction');check(f(inertia['positive_subspace_margin_lower'])>Q(2972,100000),'margin threshold')
 # Reconcile the saved projected matrix/error arrays by exact dyadic row arithmetic.
 # This does not regenerate or prove the matrix-product error bounds themselves.
 hc,bc=npy_data(V4/'inertia/projected_center_float.npy');he,be=npy_data(V4/'inertia/projected_product_error_upper.npy')
 check(hc['shape']==he['shape']==(551,551),'projected array dimensions')
 c=struct.unpack('<'+str(551*551)+'d',bc);e=struct.unpack('<'+str(551*551)+'d',be)
 for row in range(551):
  lo=Q(0);es=Q(0)
  for col in range(551):
   idx=row*551+col;cv=f(c[idx]);ev=f(e[idx]);check(ev>=0,'nonnegative projected error')
   es+=ev;lo+=(cv-ev) if col==row else -(abs(cv)+ev)
  check(f(inertia['projected_center_gershgorin_lower'])<=lo,'exact saved projected Gershgorin row')
  check(es<=f(inertia['projected_product_error_max_row_sum_upper']),'saved projected error row sum')
 h,b=npy_data(V4/'inertia/trial_positive_subspace.npy');check(h['shape']==(552,551) and hashlib.sha256(b).hexdigest()==inertia['trial_sha256'],'trial payload identity')
 h,b=npy_data(V4/'scale.npy');check(h['shape']==(552,),'scale dimension');vals=struct.unpack('<552d',b);check(all(x>0 and f(x).numerator==1 and f(x).denominator&(f(x).denominator-1)==0 for x in vals),'exact powers of two')
 expected=j(V4/'RUNTIME_EXPECTED.json')
 for name in ['before','after_points','after','worker_before','worker_after','pipeline_before','pipeline_after']:
  snap=j(V4/f'runtime_{name}.json');check(snap['status']=='MATCH' and snap['files']==len(expected)==1538 and snap['fingerprints']==expected,'saved runtime snapshot identity')
 check(j(V4/'output.json')['RH_PROOF']=='NOT_OBTAINED','scope guard')
 print(json.dumps({'status':'PASS','checks':count,'scope':'file identity and exact saved-ledger reconciliation only','new_integrals':False,'new_eigensolves':False,'producer_regeneration':False,'RH_PROOF':'NOT_OBTAINED'},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
