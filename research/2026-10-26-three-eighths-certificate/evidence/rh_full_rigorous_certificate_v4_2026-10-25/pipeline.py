"""Replace the old H functional dependency; fixed 58-point baseline plus certified saved patch."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,signal,time,json,hashlib,subprocess
from pathlib import Path
from fractions import Fraction
START=time.monotonic()
if os.getpgrp()!=os.getpid():raise RuntimeError('isolated process group required')
def hard_alarm(signum,frame):os.killpg(os.getpgrp(),signal.SIGKILL)
signal.signal(signal.SIGALRM,hard_alarm)
V1=Path('../rh_full_rigorous_certificate_2026-10-25');V2=Path('../rh_full_rigorous_certificate_v2_2026-10-25');V3=Path('../rh_full_rigorous_certificate_v3_2026-10-25')
def verify():
 for line in Path('PRELAUNCH_SHA256SUMS').read_text().splitlines():
  digest,name=line.split(maxsplit=1);name=name.lstrip('*')
  if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest:raise RuntimeError('source fingerprint mismatch: '+name)
 for name,digest in json.loads(Path('REUSED_INPUTS.json').read_text()).items():
  if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest:raise RuntimeError('reused hash mismatch: '+name)
 p=json.loads((V3/'refinement_plan.json').read_text());old=json.loads((V2/'H_domain_ledger.json').read_text());schedule=json.loads(Path('POINT_SCHEDULE.json').read_text());patchschedule=json.loads((V3/'POINT_SCHEDULE.json').read_text())
 src={int(r['template']):Fraction.from_float(float(r['used_upper']))for r in old['panels']if not r.get('analytic_tail_reused',False)}
 seen=set();total=Fraction(0);cost=0;parents=[];patch=[]
 for r in p['panels']:
  i,k=int(r['template']),int(r['split'])
  if i in seen or i not in src or k<1 or k&(k-1):raise RuntimeError('invalid fixed split')
  if Fraction(r['old_bound_fraction'])!=src[i] or Fraction(r['new_bound_fraction'])!=src[i]/k**4:raise RuntimeError('panel budget mismatch')
  seen.add(i);total+=src[i]/k**4;cost+=k;parents.append({'template':i,'split':1,'child':0,'sign':1})
  if k>1:patch +=[{'template':i,'split':1,'child':0,'sign':-1}]+[{'template':i,'split':k,'child':j,'sign':1}for j in range(k)]
 if len(src)!=58 or seen!=set(src) or total!=Fraction(p['quad_budget_fraction']) or total>Fraction(1,128) or cost!=130:raise RuntimeError('full budget mismatch')
 if Fraction.from_float(p['quad_budget_upper'])<total:raise RuntimeError('budget is not upper')
 if schedule['tasks']!=parents or schedule['point_tasks']!=58 or patchschedule['tasks']!=patch or len(patch)!=104:raise RuntimeError('schedule mismatch')
 pl=json.loads((V3/'POINT_PATCH_LEDGER.json').read_text())
 if len(pl['tasks'])!=104 or pl['point_tasks']!=104:raise RuntimeError('patch incomplete')
 for a,b in zip(pl['tasks'],patch):
  if any(a[k]!=v for k,v in b.items()):raise RuntimeError('patch ledger mismatch')
def run():
 from runtime_guard import verify as runtime_verify
 runtime_verify('pipeline_before')
 verify();subprocess.run([sys.executable,'runtime_guard.py','before'],check=True)
 subprocess.run([sys.executable,'h_point_assemble.py'],check=True)
 verify();subprocess.run([sys.executable,'runtime_guard.py','after_points'],check=True)
 import numpy as np
 from h_arithmetic import ua,um,usum,norms,gam,center_guard,boundfield,TINY
 from inertia_check import certify_inertia,_check_rounding
 from threadpoolctl import threadpool_info,threadpool_limits
 limiter=threadpool_limits(limits=1,user_api='blas');pools=[p for p in threadpool_info() if p.get('user_api')=='blas']
 if not pools or any(p.get('internal_api')!='openblas' or p.get('num_threads')!=1 for p in pools):raise RuntimeError('single-thread OpenBLAS required')
 _check_rounding()
 E=json.loads((V1/'exact_candidate.json').read_text());h1=json.loads((V1/'H_ledger.json').read_text());hs=json.loads(Path('HSAFE_LEDGER.json').read_text());patch=json.loads((V3/'POINT_PATCH_LEDGER.json').read_text());plan=json.loads((V3/'refinement_plan.json').read_text())
 D=np.load('scale.npy',allow_pickle=False);center_guard(D);mant,ex=np.frexp(D)
 if D.shape!=(552,) or not np.all(mant==.5):raise RuntimeError('invalid scaling')
 ex=ex.astype(np.int64)-1;Dmax=float(np.max(D));U0=np.fromfile(V1/'Ufloat.bin','<f8').reshape(1104,552);U=np.ldexp(U0,ex[None,:]);center_guard(U)
 if not np.array_equal(np.ldexp(U,-ex[None,:]),U0):raise RuntimeError('source scaling not exact')
 G=np.fromfile(V1/'Gmid.bin','<f8').reshape(1104,1104);R=np.fromfile(V1/'Grad.bin','<f8').reshape(1104,1104);H0=np.fromfile('Hsafe_mid.bin','<f8').reshape(552,552);DH=np.fromfile(V3/'DeltaHmid.bin','<f8').reshape(552,552)
 for z in (G,H0,DH):
  center_guard(z)
  if not np.array_equal(z,z.T):raise RuntimeError('center symmetry failure')
 if not np.isfinite(R).all() or np.any(R<0) or not np.array_equal(R,R.T):raise RuntimeError('form radius failure')
 Un=float(um(boundfield(E,'U_norm_upper'),Dmax));eta=float(um(boundfield(E,'U_error_norm_upper'),Dmax));Uf=float(norms(U,axis=None))
 dGfine=float(np.max(usum(R,axis=1)));Gnorm=float(np.max(usum(np.abs(G),axis=1)))
 dG=float(ua(um(um(Un,Un),dGfine),um(ua(um(2*Uf,eta),um(eta,eta)),Gnorm)))
 B=G@U;center_guard(B);Gc=U.T@B;center_guard(Gc)
 roundG=float(um(gam(2*1104+20),ua(um(Uf,norms(B,axis=None)),um(um(Uf,Uf),norms(G,axis=None)))))
 roundG=float(ua(roundG,um(TINY*(4*1104*1104),ua(1,Uf))))
 roundG=float(ua(ua(roundG,1e-280),um(gam(5),norms(Gc,axis=None))));Gc=(Gc+Gc.T)/2
 sumH=float(um(gam(6),ua(norms(H0,axis=None),norms(DH,axis=None))));H=H0+DH;H=(H+H.T)/2;center_guard(H)
 sub=float(um(gam(6),ua(norms(Gc,axis=None),norms(H,axis=None))));F=Gc-H;F=(F+F.T)/2;center_guard(F)
 tail=float(um(h1['analytic_tail_operator_error_upper'],um(Dmax,Dmax)));theta=float(um(h1['theta_operator_error_upper'],um(Dmax,Dmax)))
 parts={'G_congruence_exactification':dG,'G_BLAS_symmetry':roundG,'safe_baseline_point_rounding':hs['total_error_upper'],'saved_patch_point_rounding':patch['total_error_upper'],'H_sum_symmetry':sumH,'F_subtraction_symmetry':sub,'theta':theta,'analytic_caps':tail,'composite_quadrature':plan['quad_budget_upper']}
 delta=float(usum(np.array(list(parts.values()))));F.astype('<f8').tofile('Fmid_composite.bin');H.astype('<f8').tofile('Hmid_composite.bin')
 ledger={'status':'full_safe_baseline_composite_enclosure','dimension':552,'safe_parent_points':58,'reused_patch_points':104,'composite_smooth_panels':130,'components':parts,'total_error_upper':delta,'excluded_dependencies':['v1 Hmid','v1 H point error','v1 H BLAS/symmetry','v1 Fmid','v3 Fmid','old coefficient-radius repair'],'scope':'Fixed exact candidate U D and trial C D; newly explicit-multiply certified original functional plus saved explicit-multiply patch.'}
 Path('error_ledger.json').write_text(json.dumps(ledger,indent=2,allow_nan=False));result=certify_inertia(F,delta,provenance=ledger,output_dir=Path('inertia'))
 verify();subprocess.run([sys.executable,'runtime_guard.py','after'],check=True)
 runtime_verify('pipeline_after')
 Path('output.json').write_text(json.dumps({'status':'completed','inertia':result,'total_error_upper':delta,'wall_seconds':time.monotonic()-START,'RH_PROOF':'NOT_OBTAINED'},indent=2,allow_nan=False))
if __name__=='__main__':
 try:run()
 except Exception as e:
  Path('failure.json').write_text(json.dumps({'status':'incomplete','reason':str(e),'type':type(e).__name__,'wall_seconds':time.monotonic()-START}));raise
