"""Reuse frozen center and all nonquadrature certificates; sharpen remainder only."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,signal,time,json,hashlib,subprocess
from pathlib import Path
START=time.monotonic()
if os.getpgrp()!=os.getpid():raise RuntimeError('isolated process group required')
def hard_alarm(signum,frame):os.killpg(os.getpgrp(),signal.SIGKILL)
signal.signal(signal.SIGALRM,hard_alarm)
OLD=Path('../rh_full_rigorous_certificate_2026-10-25')
def verify():
 manifest=json.loads(Path('REUSED_INPUTS.json').read_text())
 for name,digest in manifest.items():
  if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest:raise RuntimeError('reused input hash mismatch: '+name)
def run():
 verify()
 subprocess.run([sys.executable,'h_domain_bound.py'],check=True)
 verify()
 import numpy as np
 from h_arithmetic import ua,um,usum,center_guard
 from h_domain_bound import read_scale
 from inertia_check import certify_inertia
 olde=json.loads((OLD/'error_ledger.json').read_text());oldh=json.loads((OLD/'H_ledger.json').read_text());newh=json.loads(Path('H_domain_ledger.json').read_text())
 D,ex=read_scale();Dmax=float(np.max(D));F=np.fromfile(OLD/'Fmid.bin','<f8').reshape(552,552)
 center_guard(F);M=np.ldexp(F,ex[:,None]+ex[None,:]);center_guard(M)
 if not np.array_equal(M,M.T) or not np.array_equal(np.ldexp(M,-ex[:,None]-ex[None,:]),F):raise RuntimeError('exact symmetric dyadic center congruence failed')
 parts={
 'G_congruence_and_exactification':olde['G_congruence_and_exactification_error_upper'],
 'G_BLAS':olde['G_BLAS_rounding_error_upper'],
 'H_point_input_exactification':oldh['point_input_exactification_error_upper'],
 'H_BLAS':oldh['blas_and_accumulation_error_upper'],
 'H_symmetrization':oldh['symmetrization_rounding_upper'],
 'H_theta':oldh['theta_operator_error_upper'],
 'H_analytic_tails':oldh['analytic_tail_operator_error_upper'],
 'F_subtraction_symmetrization':olde['subtraction_symmetrization_error_upper']}
 scale2=float(um(Dmax,Dmax));nonquad=float(um(usum(np.array(list(parts.values()))),scale2))
 delta=float(ua(nonquad,newh['quadrature_operator_error_upper']))
 M.astype('<f8').tofile('Fmid_scaled.bin')
 ledger={'status':'full_scaled_enclosure','dimension':552,'source_fine_dimension':1104,'same_fixed_templates':60,
 'scale_min':float(np.min(D)),'scale_max':Dmax,'scale_invertible_exact_powers_two':True,
 'unscaled_reused_nonquadrature_components':parts,'scaled_nonquadrature_error_upper':nonquad,
 'new_quadrature_error_upper':newh['quadrature_operator_error_upper'],'total_error_upper':delta,
 'scope':'Exact diagonal D congruence of the same fixed candidate/form; moment map is D, not I, and D is invertible. Reuses exact old center and all nonquadrature certificates.'}
 Path('error_ledger.json').write_text(json.dumps(ledger,indent=2,allow_nan=False))
 result=certify_inertia(M,delta,provenance=ledger,output_dir=Path('inertia'))
 Path('output.json').write_text(json.dumps({'status':'completed','inertia':result,'total_error_upper':delta,'wall_seconds':time.monotonic()-START,'RH_PROOF':'NOT_OBTAINED'},indent=2,allow_nan=False))
if __name__=='__main__':
 try:run()
 except Exception as e:
  Path('failure.json').write_text(json.dumps({'status':'incomplete','reason':str(e),'type':type(e).__name__,'wall_seconds':time.monotonic()-START}));raise
