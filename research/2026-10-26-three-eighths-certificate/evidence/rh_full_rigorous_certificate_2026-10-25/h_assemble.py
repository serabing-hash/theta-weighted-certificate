"""Fixed full H_trial enclosure; MPFR row jets and binary64 BLAS with norm budgets.
No adaptive mesh, precision escalation, or selected-subspace substitution.
"""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import ctypes,json,time,math
from pathlib import Path
import numpy as np
NF=552; DF=1104; DC=552; NC=276
EPS=2.0**-53; TINY=np.finfo(float).tiny
START=time.monotonic()

def promote(a):
    a=np.asarray(a)
    if np.any(a<0) or not np.isfinite(a).all():raise RuntimeError('invalid nonnegative bound input')
    return np.maximum(a,TINY)
def ua(a,b): return np.nextafter(promote(a)+promote(b)+TINY,np.inf)
def um(a,b): return np.nextafter(promote(a)*promote(b)+TINY,np.inf)
def center_guard(a):
    a=np.asarray(a)
    bits=np.ascontiguousarray(a,dtype=np.float64).view(np.uint64)
    sub=((bits & np.uint64(0x7ff0000000000000))==0)&((bits & np.uint64(0x000fffffffffffff))!=0)
    if not np.isfinite(a).all() or np.any(sub) or np.max(np.abs(a),initial=0)>1e50:raise RuntimeError('nonfinite/subnormal/overflow-risk center input unsupported')
def usum(a,axis=None):
    a=promote(a); n=a.size if axis is None else a.shape[axis]
    z=np.sum(a,axis=axis)
    return np.nextafter((z+n*TINY)/(1-(n+2)*EPS),np.inf)
def norms(a,axis=-1):
    a=np.asarray(a); n=a.size if axis is None else a.shape[axis]
    z=np.sum(a*a,axis=axis)
    return np.nextafter(np.sqrt((z+n*TINY)/(1-(2*n+4)*EPS))/(1-EPS),np.inf)
def gam(n):return np.nextafter((n*EPS)/(1-n*EPS),np.inf)
def ensure(a):
    if not np.isfinite(a).all():raise RuntimeError('nonfinite floating intermediary')
def savej(name,x):
    p=Path(name);t=Path(name+'.tmp');t.write_text(json.dumps(x,indent=2,allow_nan=False));t.replace(p)
def boundfield(x,key):
    v=x[key]
    if isinstance(v,dict):return float(v.get('upper_float',v.get('upper',v.get('hi'))))
    return float(v)

def run():
    from threadpoolctl import threadpool_info,threadpool_limits
    from inertia_check import _check_rounding
    limiter=threadpool_limits(limits=1,user_api='blas')
    pools=[p for p in threadpool_info() if p.get('user_api')=='blas']
    if not pools or any(p.get('internal_api')!='openblas' or p.get('num_threads')!=1 for p in pools):raise RuntimeError('single-thread classical OpenBLAS required')
    _check_rounding()
    meta=json.loads(Path('exact_candidate.json').read_text())
    U=np.fromfile('Ufloat.bin',dtype='<f8').reshape(DF,DC)
    C=np.fromfile('Ctrial.bin',dtype='<f8').reshape(NC,2,DC)
    Un=boundfield(meta,'U_norm_upper'); Ue=boundfield(meta,'U_error_norm_upper')
    Cn=np.asarray(meta['C_cell_norm_upper'],dtype=float)[np.arange(NF)//2]
    Uf=float(norms(U,axis=None))
    for ar in (U,C):center_guard(ar)
    lib=ctypes.CDLL('./h_core.so');pd=ctypes.POINTER(ctypes.c_double)
    lib.h_init.restype=ctypes.c_int;lib.h_error.restype=ctypes.c_char_p
    lib.h_eval.argtypes=[ctypes.c_int,pd,pd,pd];lib.h_tail.argtypes=[ctypes.c_int,pd]
    nt=lib.h_init()
    if nt<0:raise RuntimeError(lib.h_error().decode())
    lib.h_t0.argtypes=[pd]
    tc=np.zeros(2);lib.h_t0(tc.ctypes.data_as(pd));tm,tr=tc
    H=np.zeros((DC,DC));qerror=0.;point_error=0.;theta_error=0.;tail_error=0.;round_error=0.;ledger=[]
    rm=np.empty((NF,3,DF));rr=np.empty_like(rm);aux=np.empty((NF,128));ta=np.empty((NF,16))
    for tid in range(nt):
        if time.monotonic()-START>550:raise TimeoutError('H assembly reserve reached; checkpoint preserved')
        if lib.h_is_tail(tid):
            if lib.h_tail(tid,ta.ctypes.data_as(pd))<0:raise RuntimeError(lib.h_error().decode())
            # q residual affine log profile; all coefficients norm-bounded.
            AA=ua(um(ua(ta[:,0],um(um(ta[:,9],ta[:,5]),ta[:,2])),Un),um(ta[:,3],Cn))
            BB=um(ta[:,1],Un)
            z=ua(ua(um(um(AA,AA),ta[:,6]),um(um(um(2,AA),BB),ta[:,7])),um(um(BB,BB),ta[:,8]))
            e=float(usum(um(um(2,ta[:,4]),z)));tail_error=float(ua(tail_error,e))
            ledger.append({'template':tid,'analytic_tail':True,'operator_error_upper':e})
        else:
            if lib.h_eval(tid,rm.ctypes.data_as(pd),rr.ctypes.data_as(pd),aux.ctypes.data_as(pd))<0:raise RuntimeError(lib.h_error().decode())
            # Three point normalized jets of r,phi,v. Exact-candidate deviations are enclosed in eS/eP.
            pv=aux[:,30:42].reshape(NF,3,2,2); vv=aux[:,42:54].reshape(NF,3,2,2)
            S=[];P=[];Sn=[];Pn=[];eS=[];eP=[]
            for j in range(3):
                rj=rm[:,j,:]; vr=vv[:,j,:,0]; pr=pv[:,j,:,0]
                for z in (rj,vr,pr):center_guard(z)
                vc=np.einsum('ni,nij->nj',vr,C[np.arange(NF)//2])
                sj=rj@U-vc
                uparts=U.reshape(NF,2,DC)
                pj=np.einsum('ni,nij->nj',pr,uparts)
                rn=norms(rj);vn=norms(vr);pn=norms(pr)
                es=ua(ua(um(norms(rr[:,j,:]),Un),um(rn,Ue)),um(norms(vv[:,j,:,1]),Cn))
                es=ua(es,um(gam(2*DF+20),ua(um(rn,Uf),um(vn,Cn))))
                ep=ua(um(norms(pv[:,j,:,1]),Un),um(pn,Ue))
                ep=ua(ep,um(gam(20),um(pn,np.array([norms(z,axis=None) for z in uparts]))))
                S.append(sj);P.append(pj);Sn.append(norms(sj));Pn.append(norms(pj));eS.append(ua(es,1e-280));eP.append(ua(ep,1e-280))
            # Domain norms use original-cell trial coefficients, not a global C norm.
            SD=ua(um(aux[:,:5],Un),um(aux[:,10:15],Cn[:,None]));PD=um(aux[:,5:10],Un)
            rem=np.zeros(NF)
            for k in range(5):
                for l in range(5-k):
                    m=4-k-l
                    rem=ua(rem,um(aux[:,15+k],um(SD[:,l],SD[:,m])))
                    rem=ua(rem,um(um(2,aux[:,20+k]),ua(um(SD[:,l],PD[:,m]),um(PD[:,l],SD[:,m]))))
                    rem=ua(rem,um(um(um(2,aux[:,76]),aux[:,25+k]),um(PD[:,l],PD[:,m])))
            hh=aux[:,75];qcoef=np.nextafter(um(2,um(um(um(um(hh,hh),hh),hh),hh))/80,np.inf);qe=float(usum(um(qcoef,rem)))
            # Division by exact80 and Python nearest is rounded upward separately.
            qe=float(np.nextafter(qe,np.inf));qerror=float(ua(qerror,qe))
            th=ua(um(aux[:,73],um(SD[:,0],SD[:,0])),um(um(um(2,aux[:,76]),aux[:,74]),um(PD[:,0],PD[:,0])))
            te=float(usum(um(um(2,aux[:,72]),th)));theta_error=float(ua(theta_error,te))
            pe=0.;re=0.
            def term(L,R,Ln,Rn,Le,Re,cm,cr):
                nonlocal H,pe,re
                center_guard(L);center_guard(R);center_guard(cm);ensure(cr)
                scaled=cm[:,None]*R;center_guard(scaled)
                product=L.T@scaled
                lnf=float(norms(L,axis=None));rnf=float(norms(scaled,axis=None))
                eround=float(ua(um(gam(2*NF+20),um(lnf,rnf)),um(TINY*1024,lnf)))
                eround=float(ua(eround,um(gam(4),ua(norms(H,axis=None),norms(product,axis=None)))))
                H+=product;re=float(ua(re,ua(eround,1e-280)))
                ee=ua(um(cr,um(ua(Ln,Le),ua(Rn,Re))),um(np.abs(cm),ua(ua(um(Le,Rn),um(Re,Ln)),um(Le,Re))))
                pe=float(ua(pe,usum(ee)))
            for n in (0,2):
                scale=2*hh if n==0 else hh**3/6
                # All h are exact dyadic u widths; arithmetic scaling error enclosed below.
                for k in range(n+1):
                    for l in range(n-k+1):
                        m=n-k-l
                        wm=aux[:,54+2*k];wr=aux[:,55+2*k]
                        cm=scale*wm;cr=ua(um(np.abs(scale),wr),um(gam(12),np.abs(cm)))
                        term(S[l],S[m],Sn[l],Sn[m],eS[l],eS[m],cm,cr)
                        jm=aux[:,60+2*k];jr=aux[:,61+2*k]
                        cm=scale*2*jm;cr=ua(um(np.abs(scale*2),jr),um(gam(16),np.abs(cm)))
                        term(S[l],P[m],Sn[l],Pn[m],eS[l],eP[m],cm,cr)
                        term(P[l],S[m],Pn[l],Sn[m],eP[l],eS[m],cm,cr)
                        mm=aux[:,66+2*k];mr=aux[:,67+2*k]
                        cm=scale*2*tm*mm
                        cr=ua(um(np.abs(scale*2),ua(ua(um(abs(tm),mr),um(tr,np.abs(mm))),um(tr,mr))),um(gam(20),np.abs(cm)))
                        term(P[l],P[m],Pn[l],Pn[m],eP[l],eP[m],cm,cr)
            point_error=float(ua(point_error,pe));round_error=float(ua(round_error,re))
            ledger.append({'template':tid,'analytic_tail':False,'quadrature_operator_error_upper':qe,'theta_operator_error_upper':te,'point_input_source_error_upper':pe,'blas_and_accumulation_error_upper':re})
        ensure(H)
        np.savez('H_checkpoint.npz',Hmid=H,completed_templates=tid+1,total_templates=nt)
        savej('h_progress.json',{'completed_templates':tid+1,'total_templates':nt,'wall_seconds':time.monotonic()-START,'quadrature_error_upper':qerror,'tail_error_upper':tail_error})
    symround=float(um(gam(5),norms(H,axis=None)));H=(H+H.T)/2
    total=float(usum(np.array([qerror,point_error,theta_error,tail_error,round_error,symround])))
    H.astype('<f8').tofile('Hmid.bin')
    savej('H_ledger.json',{'status':'full_coverage_enclosure','dimension':DC,'original_projection_cells':NC,'fine_sources':DF,'fixed_templates':nt,'quadrature_operator_error_upper':qerror,'point_input_exactification_error_upper':point_error,'theta_operator_error_upper':theta_error,'analytic_tail_operator_error_upper':tail_error,'blas_and_accumulation_error_upper':round_error,'symmetrization_rounding_upper':symround,'total_error_upper':total,'wall_seconds':time.monotonic()-START,'panels':ledger})

if __name__=='__main__':run()
