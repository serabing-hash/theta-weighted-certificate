"""One bounded full certificate pipeline. No retry or automatic refinement."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import subprocess,json,time,hashlib,sys,signal
from pathlib import Path
START=time.monotonic()
if os.getpgrp()!=os.getpid():raise RuntimeError('pipeline must own its isolated process group')
def hard_alarm(signum,frame):os.killpg(os.getpgrp(),signal.SIGKILL)
signal.signal(signal.SIGALRM,hard_alarm)
def stage(name,cmd):
 Path('pipeline_progress.json').write_text(json.dumps({'stage':name,'wall_seconds':time.monotonic()-START}))
 subprocess.run(cmd,check=True)
def run():
 stage('exact_candidate_prepare',[sys.executable,'prepare_candidate.py'])
 stage('exact_candidate_bounds',['./exact_candidate'])
 stage('fine_form_certificate',['./g_generator'])
 stage('full_residual_certificate',[sys.executable,'h_assemble.py'])
 # The prior stages were separate processes to bound peak memory and retain outputs.
 import numpy as np
 from h_assemble import norms,usum,ua,um,gam,boundfield,center_guard
 from inertia_check import certify_inertia,_check_rounding
 from threadpoolctl import threadpool_info,threadpool_limits
 limiter=threadpool_limits(limits=1,user_api="blas")
 pools=[p for p in threadpool_info() if p.get("user_api")=="blas"]
 if not pools or any(p.get("internal_api")!="openblas" or p.get("num_threads")!=1 for p in pools):raise RuntimeError("single-thread OpenBLAS required")
 _check_rounding()
 D=1104;K=552
 E=json.loads(Path('exact_candidate.json').read_text());J=json.loads(Path('H_ledger.json').read_text())
 U=np.fromfile('Ufloat.bin','<f8').reshape(D,K);G=np.fromfile('Gmid.bin','<f8').reshape(D,D);R=np.fromfile('Grad.bin','<f8').reshape(D,D);H=np.fromfile('Hmid.bin','<f8').reshape(K,K)
 for z in (U,G,H):center_guard(z)
 if not np.isfinite(R).all():raise RuntimeError('nonfinite form radius')
 if np.any(R<0) or not np.array_equal(G,G.T) or not np.array_equal(R,R.T) or not np.array_equal(H,H.T):raise RuntimeError('form symmetry/radius failure')
 Un=boundfield(E,'U_norm_upper');eta=boundfield(E,'U_error_norm_upper');Uf=float(norms(U,axis=None))
 dGfine=float(np.max(usum(R,axis=1)));Gnorm=float(np.max(usum(np.abs(G),axis=1)))
 # Gexact-Ustored congruence: (Uexact norm)^2 dGfine + (2||Ustored|| eta+eta²)||Gmid||.
 dG=float(ua(um(um(Un,Un),dGfine),um(ua(um(2*Uf,eta),um(eta,eta)),Gnorm)))
 B=G@U;center_guard(B);Gc=U.T@B
 roundG=float(um(gam(2*D+20),ua(um(Uf,norms(B,axis=None)),um(um(Uf,Uf),norms(G,axis=None)))))
 roundG=float(ua(roundG,um(np.finfo(float).tiny*(4*D*D),ua(1,Uf))))
 roundG=float(ua(ua(roundG,1e-280),um(gam(5),norms(Gc,axis=None))));Gc=(Gc+Gc.T)/2
 F=Gc-H
 subtraction=float(um(gam(5),ua(norms(Gc,axis=None),norms(H,axis=None))))
 F=(F+F.T)/2
 total=float(usum(np.array([dG,roundG,float(J['total_error_upper']),subtraction])))
 F.astype('<f8').tofile('Fmid.bin')
 ledger={'classification':'FULL_ENCLOSURE_PENDING_INERTIA','dimension':K,'fine_source_dimension':D,
 'Gfine_entry_radius_operator_bound':dGfine,'G_congruence_and_exactification_error_upper':dG,'G_BLAS_rounding_error_upper':roundG,
 'H_error_upper':J['total_error_upper'],'subtraction_symmetrization_error_upper':subtraction,'total_error_upper':total,
 'scope':'Exact analytic original P/X and dyadic penalty Z; original moments; arbitrary dyadic residual trial. Full finite sufficient lower matrix only; fixed R=1 and epsilon=1/8.'}
 Path('error_ledger.json').write_text(json.dumps(ledger,indent=2,allow_nan=False))
 result=certify_inertia(F,total,provenance=ledger,output_dir=Path('inertia'))
 Path('output.json').write_text(json.dumps({'status':'completed','inertia':result,'total_error_upper':total,'wall_seconds':time.monotonic()-START,'RH_PROOF':'NOT_OBTAINED'},indent=2,allow_nan=False))
if __name__=='__main__':
 try:run()
 except Exception as e:
  Path('failure.json').write_text(json.dumps({'status':'incomplete','reason':str(e),'type':type(e).__name__,'wall_seconds':time.monotonic()-START}))
  raise
