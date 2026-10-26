"""One fixed point-only composite patch, with preproved remainder allocation."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,signal,time,json,hashlib,subprocess,math
from pathlib import Path
from fractions import Fraction
START=time.monotonic()
if os.getpgrp()!=os.getpid():raise RuntimeError('isolated process group required')
def hard_alarm(signum,frame):os.killpg(os.getpgrp(),signal.SIGKILL)
signal.signal(signal.SIGALRM,hard_alarm)
V1=Path('../rh_full_rigorous_certificate_2026-10-25');V2=Path('../rh_full_rigorous_certificate_v2_2026-10-25')
def verify():
 for name,digest in json.loads(Path('REUSED_INPUTS.json').read_text()).items():
  if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest:raise RuntimeError('reused input hash mismatch: '+name)
 p=json.loads(Path('refinement_plan.json').read_text());old=json.loads((V2/'H_domain_ledger.json').read_text());schedule=json.loads(Path('POINT_SCHEDULE.json').read_text())
 if p['source_sha256']!=hashlib.sha256((V2/'H_domain_ledger.json').read_bytes()).hexdigest():raise RuntimeError('planning source hash mismatch')
 src={int(r['template']):Fraction.from_float(float(r['used_upper']))for r in old['panels']if not r.get('analytic_tail_reused',False)}
 seen=set();total=Fraction(0);cost=0;expected=[]
 for r in p['panels']:
  i,k=int(r['template']),int(r['split'])
  if i in seen or i not in src or k<1 or k&(k-1):raise RuntimeError('invalid fixed split')
  if Fraction(r['old_bound_fraction'])!=src[i] or Fraction(r['new_bound_fraction'])!=src[i]/k**4:raise RuntimeError('exact panel budget mismatch')
  seen.add(i);total+=src[i]/k**4;cost+=k
  if k>1:expected +=[{'template':i,'split':1,'child':0,'sign':-1}]+[{'template':i,'split':k,'child':j,'sign':1}for j in range(k)]
 if seen!=set(src) or total!=Fraction(p['quad_budget_fraction']) or total>Fraction(1,128) or cost!=130 or cost>256:raise RuntimeError('exact full budget mismatch')
 if Fraction.from_float(p['quad_budget_upper'])<total:raise RuntimeError('budget float is not upper')
 if schedule['tasks']!=expected or len(expected)!=104:raise RuntimeError('point schedule mismatch')
 if schedule['plan_sha256']!=hashlib.sha256(Path('refinement_plan.json').read_bytes()).hexdigest():raise RuntimeError('schedule binding failed')
def run():
 verify();subprocess.run([sys.executable,'h_point_assemble.py'],check=True);verify()
 import numpy as np
 from h_arithmetic import ua,um,usum,norms,gam,center_guard
 from inertia_check import certify_inertia,_check_rounding
 _check_rounding()
 old=json.loads((V2/'error_ledger.json').read_text());h1=json.loads((V1/'H_ledger.json').read_text());patch=json.loads(Path('POINT_PATCH_LEDGER.json').read_text());plan=json.loads(Path('refinement_plan.json').read_text())
 M=np.fromfile(V2/'Fmid_scaled.bin','<f8').reshape(552,552);DH=np.fromfile('DeltaHmid.bin','<f8').reshape(552,552);center_guard(M);center_guard(DH)
 if not np.array_equal(M,M.T) or not np.array_equal(DH,DH.T):raise RuntimeError('center symmetry failure')
 sub=float(um(gam(6),ua(norms(M,axis=None),norms(DH,axis=None))));F=M-DH;F=(F+F.T)/2;center_guard(F)
 # Extra conservative guard for rounded scalar quadrature coefficients multiplying input radii in the frozen old assembly.
 reuse_guard=float(um(um(gam(32),h1['point_input_exactification_error_upper']),um(old['scale_max'],old['scale_max'])))
 delta=float(usum(np.array([old['scaled_nonquadrature_error_upper'],reuse_guard,plan['quad_budget_upper'],patch['total_error_upper'],sub])))
 F.astype('<f8').tofile('Fmid_composite.bin')
 ledger={'status':'full_fixed_composite_enclosure','dimension':552,'fine_sources':1104,'old_templates':60,'new_smooth_point_templates':130,'evaluated_patch_points':104,
 'certified_composite_quadrature_upper':plan['quad_budget_upper'],'reused_nonquadrature_upper':old['scaled_nonquadrature_error_upper'],'reused_scale_radius_guard_upper':reuse_guard,
 'new_patch_point_rounding_error_upper':patch['total_error_upper'],'final_subtraction_symmetrization_error_upper':sub,'total_error_upper':delta,
 'scope':'Same fixed source Uexact D and trial C D; only selected midpoint Taylor panels subdivided uniformly. Existing derivative-domain certificates give q_i/k_i^4, verified with exact fractions.'}
 Path('error_ledger.json').write_text(json.dumps(ledger,indent=2,allow_nan=False));result=certify_inertia(F,delta,provenance=ledger,output_dir=Path('inertia'))
 Path('output.json').write_text(json.dumps({'status':'completed','inertia':result,'total_error_upper':delta,'wall_seconds':time.monotonic()-START,'RH_PROOF':'NOT_OBTAINED'},indent=2,allow_nan=False))
if __name__=='__main__':
 try:run()
 except Exception as e:
  Path('failure.json').write_text(json.dumps({'status':'incomplete','reason':str(e),'type':type(e).__name__,'wall_seconds':time.monotonic()-START}));raise
