"""Certified point-only correction of a frozen midpoint Taylor functional."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import ctypes,json,time,math,hashlib
from pathlib import Path
import numpy as np
from h_arithmetic import ua,um,usum,norms,gam,center_guard,boundfield,TINY
from inertia_check import _check_rounding
from threadpoolctl import threadpool_info,threadpool_limits
OLD=Path('../rh_full_rigorous_certificate_2026-10-25');NF=552;DF=1104;DC=552;NC=276;START=time.monotonic()
def savej(name,obj):
 p=Path(name);t=Path(name+'.tmp');t.write_text(json.dumps(obj,indent=2,allow_nan=False));t.replace(p)
def run():
 limiter=threadpool_limits(limits=1,user_api='blas');pools=[p for p in threadpool_info() if p.get('user_api')=='blas']
 if not pools or any(p.get('internal_api')!='openblas' or p.get('num_threads')!=1 for p in pools):raise RuntimeError('single-thread classical OpenBLAS required')
 _check_rounding()
 schedule=json.loads(Path('POINT_SCHEDULE.json').read_text());tasks=schedule['tasks']
 if len(tasks)!=104 or schedule['point_tasks']!=len(tasks):raise RuntimeError('fixed point count mismatch')
 E=json.loads((OLD/'exact_candidate.json').read_text());D=np.load('scale.npy',allow_pickle=False);center_guard(D);mant,ex=np.frexp(D)
 if D.shape!=(DC,) or not np.all(mant==.5):raise RuntimeError('invalid positive dyadic D')
 ex=ex.astype(np.int64)-1;Dmax=float(np.max(D));U0=np.fromfile(OLD/'Ufloat.bin','<f8').reshape(DF,DC);C0=np.fromfile(OLD/'Ctrial.bin','<f8').reshape(NC,2,DC)
 U=np.ldexp(U0,ex[None,:]);C=np.ldexp(C0,ex[None,None,:]);center_guard(U);center_guard(C)
 if not np.array_equal(np.ldexp(U,-ex[None,:]),U0) or not np.array_equal(np.ldexp(C,-ex[None,None,:]),C0):raise RuntimeError('source scaling not exact')
 eta=float(um(boundfield(E,'U_error_norm_upper'),Dmax));Un=float(um(boundfield(E,'U_norm_upper'),Dmax));Uf=float(norms(U,axis=None))
 Uloc=U.reshape(NF,2,DC);Uln=np.array([norms(z,axis=None) for z in Uloc]);Cloc=C[np.arange(NF)//2];Cn=np.array([norms(z,axis=None) for z in Cloc])
 lib=ctypes.CDLL('./h_point.so');pd=ctypes.POINTER(ctypes.c_double);lib.h_init.restype=ctypes.c_int;lib.h_error.restype=ctypes.c_char_p
 lib.h_point.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_int,pd,pd,pd];lib.h_t0.argtypes=[pd]
 if lib.h_init()!=60:raise RuntimeError('old template count mismatch')
 tc=np.zeros(2);lib.h_t0(tc.ctypes.data_as(pd));tm,tr=tc
 rm=np.empty((NF,3,DF));rr=np.empty_like(rm);aux=np.empty((NF,64));Delta=np.zeros((DC,DC));point_error=0.;round_error=0.;ledger=[]
 for index,task in enumerate(tasks):
  if time.monotonic()-START>550:raise TimeoutError('point stage reserve reached')
  tid,split,child,sgn=(int(task[k])for k in ('template','split','child','sign'))
  if sgn not in (-1,1):raise RuntimeError('invalid patch sign')
  if lib.h_point(tid,split,child,rm.ctypes.data_as(pd),rr.ctypes.data_as(pd),aux.ctypes.data_as(pd))<0:raise RuntimeError(lib.h_error().decode())
  ph=aux[:,:12].reshape(NF,3,2,2);mv=aux[:,12:18].reshape(NF,3,2);wv=aux[:,18:24].reshape(NF,3,2);pb=aux[:,32:40].reshape(NF,2,2,2)
  pcm=pb[:,:,:,0];pcr=pb[:,:,:,1];center_guard(pcm);center_guard(Cloc)
  pcC=np.einsum('nik,nkj->nij',pcm,Cloc);center_guard(pcC)
  pbn=np.array([norms(z,axis=None)for z in pcm]);pbr=np.array([norms(z,axis=None)for z in pcr])
  pcerr=ua(um(pbr,Cn),um(gam(20),um(pbn,Cn)))
  BC=[];BE=[];BN=[]
  for j in range(3):
   coeff=tm*mv[:,j,0];center_guard(coeff)
   er=ua(ua(ua(um(abs(tm),mv[:,j,1]),um(tr,np.abs(mv[:,j,0]))),um(tr,mv[:,j,1])),um(gam(5),np.abs(coeff)))
   bj=coeff[:,None,None]*Uloc
   if j==0:bj=bj-pcC
   center_guard(bj)
   eb=ua(um(er,ua(Uln,eta)),um(np.abs(coeff),eta));eb=ua(eb,um(gam(10),um(np.abs(coeff),Uln)))
   if j==0:eb=ua(eb,ua(pcerr,um(gam(5),np.array([norms(z,axis=None)for z in pcC]))))
   BC.append(bj);BE.append(ua(eb,1e-280));BN.append(np.array([norms(z,axis=None)for z in bj]))
  R=[];RN=[];RE=[]
  for j in range(3):
   r=rm[:,j,:];rad=rr[:,j,:];center_guard(r)
   A=r@U;center_guard(A)
   er=ua(um(norms(rad),Un),um(norms(r),eta));er=ua(er,um(gam(2*DF+20),um(norms(r),Uf)));er=ua(er,1e-280)
   for l in range(j+1):
    b=j-l;pv=ph[:,l,:,0];pr=ph[:,l,:,1];center_guard(pv)
    add=np.einsum('ni,nij->nj',pv,BC[b]);center_guard(add)
    ee=ua(um(norms(pr),ua(BN[b],BE[b])),um(norms(pv),BE[b]));ee=ua(ee,um(gam(20),um(norms(pv),BN[b])))
    ee=ua(ee,um(gam(5),ua(norms(A),norms(add))));A=A+add;er=ua(er,ua(ee,1e-280))
   R.append(A);RN.append(norms(A));RE.append(er)
  pe=0.;re=0.;hh=aux[:,24]
  for n in (0,2):
   scale=sgn*(2*hh if n==0 else hh*hh*hh/6)
   for k in range(n+1):
    for l in range(n-k+1):
     m=n-k-l;cm=scale*wv[:,k,0];cr=ua(um(ua(np.abs(scale),um(gam(12),np.abs(scale))),wv[:,k,1]),um(gam(12),np.abs(cm)))
     center_guard(cm);center_guard(R[l]);center_guard(R[m]);scaled=cm[:,None]*R[m];center_guard(scaled)
     product=R[l].T@scaled
     ln=float(norms(R[l],axis=None));rn=float(norms(scaled,axis=None))
     ro=ua(um(gam(2*NF+20),um(ln,rn)),um(TINY*1024,ln));ro=ua(ro,um(gam(4),ua(norms(Delta,axis=None),norms(product,axis=None))))
     Delta+=product;re=float(ua(re,ua(ro,1e-280)))
     ee=ua(um(cr,um(ua(RN[l],RE[l]),ua(RN[m],RE[m]))),um(np.abs(cm),ua(ua(um(RE[l],RN[m]),um(RE[m],RN[l])),um(RE[l],RE[m]))))
     pe=float(ua(pe,usum(ee)))
  point_error=float(ua(point_error,pe));round_error=float(ua(round_error,re))
  ledger.append({**task,'point_input_exactification_error_upper':pe,'blas_accumulation_error_upper':re})
  np.savez('Delta_checkpoint.npz',Delta=Delta,completed_points=index+1,total_points=len(tasks))
  savej('point_progress.json',{'completed_points':index+1,'total_points':len(tasks),'wall_seconds':time.monotonic()-START,'point_error_upper':point_error,'round_error_upper':round_error})
 sym=float(um(gam(5),norms(Delta,axis=None)));Delta=(Delta+Delta.T)/2;Delta.astype('<f8').tofile('DeltaHmid.bin')
 total=float(usum(np.array([point_error,round_error,sym])))
 savej('POINT_PATCH_LEDGER.json',{'status':'complete_point_patch_enclosure','point_tasks':len(tasks),'point_input_exactification_error_upper':point_error,'blas_accumulation_error_upper':round_error,'symmetrization_error_upper':sym,'total_error_upper':total,'wall_seconds':time.monotonic()-START,'tasks':ledger})
if __name__=='__main__':run()
