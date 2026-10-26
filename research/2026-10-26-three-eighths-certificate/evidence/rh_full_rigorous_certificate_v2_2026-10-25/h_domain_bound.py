"""Sharpen only the frozen60-panel quadrature remainder; reuse old exact functional.
The power-of-two diagonal scale is a fixed, explicitly bound input.
"""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import ctypes,json,time,math,hashlib
from pathlib import Path
import numpy as np
from h_arithmetic import ua,um,usum,norms,gam,center_guard,boundfield,TINY
from inertia_check import _check_rounding
from threadpoolctl import threadpool_info,threadpool_limits
OLD=Path('../rh_full_rigorous_certificate_2026-10-25')
NF=552;DF=1104;DC=552;NC=276
START=time.monotonic()

def savej(name,obj):
 p=Path(name);t=Path(name+'.tmp');t.write_text(json.dumps(obj,indent=2,allow_nan=False));t.replace(p)
def read_scale():
 D=np.load('scale.npy',allow_pickle=False).astype(np.float64,copy=False)
 if D.shape!=(DC,) or not np.all(D>0):raise RuntimeError('invalid positive diagonal scale')
 center_guard(D)
 mant,ex=np.frexp(D)
 if not np.all(mant==.5):raise RuntimeError('scale entries must be exact powers of two')
 return D,ex.astype(np.int64)-1

def run():
 limiter=threadpool_limits(limits=1,user_api='blas');pools=[p for p in threadpool_info() if p.get('user_api')=='blas']
 if not pools or any(p.get('internal_api')!='openblas' or p.get('num_threads')!=1 for p in pools):raise RuntimeError('single-thread OpenBLAS required')
 _check_rounding()
 E=json.loads((OLD/'exact_candidate.json').read_text());oldh=json.loads((OLD/'H_ledger.json').read_text())
 oldpan={int(p['template']):p for p in oldh['panels']}
 D,ex=read_scale();Dmax=float(np.max(D));U0=np.fromfile(OLD/'Ufloat.bin','<f8').reshape(DF,DC);C0=np.fromfile(OLD/'Ctrial.bin','<f8').reshape(NC,2,DC)
 U=np.ldexp(U0,ex[None,:]);C=np.ldexp(C0,ex[None,None,:]);center_guard(U);center_guard(C)
 if not np.array_equal(np.ldexp(U,-ex[None,:]),U0) or not np.array_equal(np.ldexp(C,-ex[None,None,:]),C0):raise RuntimeError('dyadic scaling failed exact readback')
 eta=float(um(boundfield(E,'U_error_norm_upper'),Dmax));Uf=float(norms(U,axis=None));Uabs=np.abs(U)
 Uloc=U.reshape(NF,2,DC);Uln=np.array([norms(z,axis=None) for z in Uloc]);Cloc=C[np.arange(NF)//2];Cn=np.array([norms(z,axis=None) for z in Cloc])
 lib=ctypes.CDLL('./h_domain.so');pd=ctypes.POINTER(ctypes.c_double);lib.h_init.restype=ctypes.c_int;lib.h_error.restype=ctypes.c_char_p
 lib.h_domain.argtypes=[ctypes.c_int,pd,pd,pd];lib.h_t0.argtypes=[pd]
 nt=lib.h_init()
 if nt!=60 or nt!=oldh['fixed_templates']:raise RuntimeError('frozen template count mismatch')
 tc=np.zeros(2);lib.h_t0(tc.ctypes.data_as(pd));tm,tr=tc
 dm=np.empty((NF,5,DF));dr=np.empty_like(dm);aux=np.empty((NF,96));ledger=[];qsum=0.
 for tid in range(nt):
  if time.monotonic()-START>550:raise TimeoutError('domain-only reserve reached')
  if lib.h_is_tail(tid):
   if not oldpan[tid]['analytic_tail']:raise RuntimeError('tail partition mismatch')
   ledger.append({'template':tid,'analytic_tail_reused':True});continue
  if oldpan[tid]['analytic_tail']:raise RuntimeError('smooth partition mismatch')
  if lib.h_domain(tid,dm.ctypes.data_as(pd),dr.ctypes.data_as(pd),aux.ctypes.data_as(pd))<0:raise RuntimeError(lib.h_error().decode())
  phi=aux[:,:20].reshape(NF,5,2,2);mv=aux[:,20:30].reshape(NF,5,2);pb=aux[:,40:48].reshape(NF,2,2,2)
  pcm=pb[:,:,:,0];pcr=pb[:,:,:,1]
  center_guard(pcm);center_guard(Cloc)
  pcC=np.einsum('nik,nkj->nij',pcm,Cloc);center_guard(pcC)
  pbn=np.array([norms(z,axis=None) for z in pcm]);pbr=np.array([norms(z,axis=None) for z in pcr])
  pcerr=ua(um(pbr,Cn),um(gam(20),um(pbn,Cn)))
  BC=[];BE=[];BN=[]
  for j in range(5):
   coeff=tm*mv[:,j,0]
   er=ua(ua(ua(um(abs(tm),mv[:,j,1]),um(tr,np.abs(mv[:,j,0]))),um(tr,mv[:,j,1])),um(gam(5),np.abs(coeff)))
   center_guard(coeff)
   bj=coeff[:,None,None]*Uloc
   if j==0:bj=bj-pcC
   center_guard(bj)
   eb=ua(um(er,ua(Uln,eta)),um(np.abs(coeff),eta))
   eb=ua(eb,um(gam(10),um(np.abs(coeff),Uln)))
   if j==0:eb=ua(eb,ua(pcerr,um(gam(5),np.array([norms(z,axis=None) for z in pcC]))))
   BC.append(bj);BE.append(ua(eb,1e-280));BN.append(np.array([norms(z,axis=None) for z in bj]))
  RN=[]
  for j in range(5):
   r=dm[:,j,:];rad=dr[:,j,:];center_guard(r)
   A=r@U;center_guard(A)
   # Componentwise interval radius preserves column/local downweight before taking a norm.
   center_guard(rad)
   radprod=rad@Uabs;center_guard(radprod)
   radnorm=norms(radprod)
   radnorm=ua(radnorm,um(gam(2*DF+20),um(norms(rad),Uf)))
   er=ua(radnorm,um(ua(norms(r),norms(rad)),eta))
   er=ua(er,um(gam(2*DF+20),um(norms(r),Uf)))
   er=ua(er,1e-280)
   for l in range(j+1):
    b=j-l;ph=phi[:,l,:,0];pr=phi[:,l,:,1];center_guard(ph)
    add=np.einsum('ni,nij->nj',ph,BC[b]);center_guard(add)
    ee=ua(um(norms(pr),ua(BN[b],BE[b])),um(norms(ph),BE[b]))
    ee=ua(ee,um(gam(20),um(norms(ph),BN[b])))
    ee=ua(ee,um(gam(5),ua(norms(A),norms(add))))
    A=A+add;er=ua(er,ua(ee,1e-280))
   RN.append(ua(norms(A),er))
  rem=np.zeros(NF)
  for k in range(5):
   for l in range(5-k):
    m=4-k-l;rem=ua(rem,um(aux[:,30+k],um(RN[l],RN[m])))
  hh=aux[:,35];coef=np.nextafter(um(2,um(um(um(um(hh,hh),hh),hh),hh))/80,np.inf)
  qnew=float(usum(um(coef,rem)))
  qold=float(um(oldpan[tid]['quadrature_operator_error_upper'],um(Dmax,Dmax)))
  chosen=min(qnew,qold);qsum=float(ua(qsum,chosen))
  ledger.append({'template':tid,'new_direct_residual_quadrature_upper':qnew,'old_bound_scaled_upper':qold,'used_upper':chosen})
  savej('domain_progress.json',{'completed_templates':tid+1,'total_templates':nt,'quadrature_error_upper':qsum,'wall_seconds':time.monotonic()-START})
  savej('domain_partial_ledger.json',ledger)
 savej('H_domain_ledger.json',{'status':'complete_same_functional_remainder','fixed_templates':nt,'dimension':DC,'scaled_source':True,'scale_max':Dmax,'quadrature_operator_error_upper':qsum,'wall_seconds':time.monotonic()-START,'panels':ledger,'reuse_statement':'Same exact60-panel midpoint j0+j2 functional. Only domain remainder bounds replaced; original Hmid and nonquadrature ledgers remain unchanged before exact power-of-two congruence.'})
if __name__=='__main__':run()
