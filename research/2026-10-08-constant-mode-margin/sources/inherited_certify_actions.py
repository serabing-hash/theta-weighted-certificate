"""Common-cache pilot and single fixed32 run, using validated Arb only."""
import argparse, sys, traceback
from common import *

def build_base(start):
    # Sampling only the true small source region.  Every skipped sample and
    # every omitted periodic copy is covered by the frozen analytic bias.
    samples=[]; n=0
    while True:
        x=PERIOD*A(F(n,N))
        if x.lower()>3:break
        if x.upper()>3:raise ArithmeticError('ambiguous source cutoff')
        kp,a=finite_source(x)
        if not kp.rad()<A(F(1,2**130)) or not a.rad()<A(F(1,2**130)):
            raise ArithmeticError('sample primitive radius')
        samples.append((x,kp,a));n+=1
    assert n<2048
    save(ROOT/'outputs/SOURCE_SAMPLES.json',{
        'N':N,'period':'32*pi','positive_samples':len(samples),
        'theta_terms':8,'source_cutoff':'3',
        'rows':[{'n':j,'x':record(x),'kappa8':record(kp),'a8':record(a)}
                for j,(x,kp,a) in enumerate(samples)]})
    for kind,r in [('a',r) for r in range(5)]+[('kappa',r) for r in range(3)]:
        vec=[acb(0)]*N
        for j,(x,kp,a) in enumerate(samples):
            v=(a if kind=='a' else kp)*x**r
            vec[N//2+j]=acb(v)
            if j:vec[N//2-j]=acb(-v if r%2 else v)
        ts=time.monotonic(); dft=acb.dft(vec); elapsed=time.monotonic()-ts
        count('native_forward_DFT_calls');count('native_forward_DFT_length_sum',N)
        vals=[];native_max=F(0)
        for k in range(K+1):
            z=dft[k]/N
            if k%2:z=-z
            active=z.imag if r%2 else z.real
            inactive=z.real if r%2 else z.imag
            if not z.is_finite() or not inactive.contains(0):
                raise ArithmeticError('DFT parity/finite gate')
            native_max=max(native_max,upper(active.rad()))
            enclosed=pad(active,F(1,2**300))
            vals.append(record(enclosed))
        assert native_max<F(1,2**100)
        save(ROOT/'outputs'/f'BASE_{kind}_{r}.json',{
            'kind':kind,'source_power':r,'N':N,'K':K,
            'component':'imag' if r%2 else 'real',
            'denominator_power_of_two':DEN_BITS,'values':vals,
            'native_max_radius':str(native_max),
            'model_bias_per_retained_coefficient':str(F(1,2**300)),
            'DFT_wall_seconds':elapsed,
            'normalization':'(-1)^k DFT(samples)[k]/N; frequency k/16',
            'parity_inactive_components_checked':K+1})
        del dft,vec,vals;gc.collect()
        progress(start,f'validated common transform {kind} x^{r}')

def build_multiplier(start):
    psi0=-arb.const_euler()-arb.pi()/2-3*arb.const_log2()
    vals=[]
    for k in range(KOUT+1):
        v=arb(0) if k==0 else acb(A(F(1,4)),A(F(k,32))).digamma().real-psi0
        assert v.is_finite() and (k==0 or v.lower()>0)
        assert v.rad()<A(F(1,2**100))
        vals.append(record(v))
        if k:count('new_Gamma_digamma_multiplier_evaluations')
        if k and k%8192==0:guard(start)
    save(ROOT/'outputs/GAMMA_MULTIPLIERS.json',{
        'frequency':'k/16','KOUT':KOUT,'denominator_power_of_two':DEN_BITS,
        'values':vals,'DC_exactly_zero':True,
        'normalization':'Re psi(1/4+i*k/32)-psi(1/4)'})
    progress(start,'common Gamma multipliers')

def build_frame_and_pole(start,base):
    # This source-overlap cache is not a residual Gram or a spectral matrix.
    # It is used only to apply the unchanged full 372-coordinate frame.
    memo={}
    def M(kind,r,k,trig):
        key=(kind,r,k,trig)
        if key not in memo:memo[key]=moment(base,kind,r,k,trig)
        return memo[key]
    terms=[feature_terms(j) for j in range(372)]
    Gf=arb_mat(372,372)
    for j in range(372):
        m=SHIFTS[j//3]
        for l in range(j+1):
            n=SHIFTS[l//3]; val=arb(0)
            for r,tr,al in terms[j]:
                for s,ts,be in terms[l]:
                    R=r+s
                    if tr==ts=='cos':
                        integral=(M('a',R,m-n,'cos')+M('a',R,m+n,'cos'))/2
                    elif tr==ts=='sin':
                        integral=(M('a',R,m-n,'cos')-M('a',R,m+n,'cos'))/2
                    elif tr=='cos':
                        integral=(M('a',R,n+m,'sin')+M('a',R,n-m,'sin'))/2
                    else:
                        integral=(M('a',R,m+n,'sin')+M('a',R,m-n,'sin'))/2
                    val+=al*be*integral
            if not val.is_finite():raise ArithmeticError('frame overlap')
            Gf[j,l]=val;Gf[l,j]=val
            count('finite_source_frame_overlap_entries')
        if j%64==0:guard(start)
    D=Gf*TMAT
    polew=[]
    for j in range(372):
        val=sum((al*M('kappa',r,SHIFTS[j//3],tr)
                 for r,tr,al in terms[j]),arb(0))
        polew.append(val)
    pole=arb_mat([polew])*TMAT
    save(ROOT/'outputs/FRAME_AND_POLE_ENCLOSURES.json',{
        'D_shape':[372,32], 'D_WstarV':[[record(D[j,i]) for i in range(32)] for j in range(372)],
        'pole_integrals':[record(pole[0,i]) for i in range(32)],
        'denominator_power_of_two':DEN_BITS,
        'unique_finite_moment_calls':len(memo),
        'full_372_coordinates_maintained':True,
        'residual_Gram_computed':False})
    count('finite_source_moment_cache_keys',len(memo))
    count('frame_action_columns',32)
    count('pole_moment_columns',32)
    del Gf,D,memo,pole;gc.collect()
    progress(start,'full frame and pole finite moment cache')

def gamma_column(i,base,mult,start):
    As=[]
    for r in range(3):
        As.append(acb_poly([coefficient(base,'a',r,k) for k in range(-K,K+1)]))
    total=acb_poly([])
    for r in range(3):
        pv=[acb(0)]*(2*MMAX+1)
        for s,(al,m) in enumerate(zip(ALPHA,SHIFTS)):
            t0=arb((T[3*s][i],-30));t1=arb((T[3*s+1][i],-30));t2=arb((T[3*s+2][i],-30))
            if r==0:z=acb(al*t0/2)
            elif r==1:z=acb(0,al*t1/(8*arb(3).sqrt()))
            else:z=acb(-al*(t0/96+t2/(48*arb(5).sqrt()))/2)
            pv[MMAX+m]=z;pv[MMAX-m]=z.conjugate()
        total+=As[r]*acb_poly(pv)
        count('native_validated_polynomial_convolutions')
        guard(start)
    nums=[];err=F(0);l1=F(0)
    for k in range(KOUT+1):
        zp=total[KOUT+k];zm=total[KOUT-k]
        assert zp.is_finite() and zm.is_finite()
        assert zp.imag.contains(0) and zm.imag.contains(0)
        even=(zp.real+zm.real)/2
        co=mult[k]*even*(1 if k==0 else 2)
        n,e=quantize(co,OUT_BITS);nums.append(str(n));err+=e;l1+=F(abs(n),2**OUT_BITS)
    assert nums[0]=='0'
    count('new_certified_Gamma_action_columns')
    return nums,err,l1

def finish_column(i,base,mult,fp,budget,start,phase):
    t0=time.monotonic()
    nums,errg,l1=gamma_column(i,base,mult,start)
    dn=[];derr=F(0)
    for j in range(372):
        d=restore(fp['D_WstarV'][j][i]);n,e=quantize(d,OUT_BITS)
        dn.append(str(n));derr+=e
    p=restore(fp['pole_integrals'][i]);pn,perr=quantize(p,OUT_BITS)
    uniform=(AI[i]*(F(5,16)+30+2368)
             +l1+2*F(abs(pn),2**OUT_BITS)
             +10*sum((F(abs(int(n)),2**OUT_BITS) for n in dn),F(0)))*F(1,2**160)
    errors={
        'Gamma_frequency_truncation':AI[i]*F(budget['Gamma_frequency_tail_per_AI']),
        'Gamma_periodic_copies':AI[i]*F(budget['Gamma_periodic_copies_per_AI']),
        'Gamma_source_DFT_convolution_multiplier_and_serialization':errg/2,
        'infinite_prime_operator_tail':AI[i]*F(budget['infinite_prime_tail_per_AI']),
        'full_frame_moment_and_coefficient_error':2**11*derr,
        'pole_moment_and_coefficient_error':perr/2,
        'finite_theta8_nonGamma_source_transfer':2*uniform,
        'exterior_finite_action_zero_extension':AI[i]*F(budget['finite_action_exterior_per_AI']),
        'spatial_interpolation':'0',
    }
    total=sum((F(e) for e in errors.values()),F(0))
    if not total<F(1,2**18):raise ArithmeticError(f'action error gate column {i}: {total}')
    descriptor={
        'format':'SERABI_FINITE_ANALYTIC_U_ACTION_V1','column_zero_based':i,
        'coordinate':'U Hnew (U^-1 V_i), ordinary Lebesgue L2(dx)',
        'support':['-2','2'],'outside_support':'exactly zero',
        'basis':'Gamma cosine frequency k/16 plus six finite analytic source terms',
        'denominator_power_of_two':OUT_BITS,'KOUT':KOUT,
        'Gamma_cosine_numerators':nums,'frame_numerators':dn,'pole_numerator':str(pn),
        'theta_terms_in_approximant':8,'prime_cutoff':32,
        'full_frame_dimension':372,'T_denominator_power_of_two':30,
        'T_file':'../sources/fixed_inputs/T32_dyadic_numerators.csv',
        'T_sha256':sha(INPUT/'T32_dyadic_numerators.csv'),
        'cell_sha256':sha(INPUT/'retained_cells_exact.csv'),
        'action_is_not_residual_Gram_or_inverse':True}
    save(ROOT/'outputs'/f'ACTION_{i:02d}.json',descriptor)
    # Actual full expression, including both directions of every retained
    # prime power and every observation. No new source/action integral.
    point_checks=[]
    for x in (F(0),F(1,2),F(2)):
        value,parts=full_approximation(i,x,descriptor)
        point_checks.append({'x':str(x),'value':record(value,120),
                             'component_order':list(parts),
                             'components':{k:record(v,120) for k,v in parts.items()}})
    cert={'verdict':'PASS-ONE-FIXED-RANK32-COLUMN','column_zero_based':i,
          'phase':phase,'minimum_operator_domain_admitted':True,
          'Ai_exact':str(AI[i]),'errors_L2_upper':{k:str(v) for k,v in errors.items()},
          'whole_line_error_upper':str(total),'target':str(F(1,2**18)),
          'Gamma_arithmetic_coefficient_L1_error':str(errg),
          'Gamma_midpoint_L1_norm':str(l1),'frame_coefficient_error_L1':str(derr),
          'pole_coefficient_error':str(perr),'descriptor_sha256':sha(ROOT/'outputs'/f'ACTION_{i:02d}.json'),
          'complete_finite_assembly_point_checks':point_checks,
          'wall_seconds':time.monotonic()-t0}
    save(ROOT/'certificates'/f'ACTION_CERTIFICATE_{i:02d}.json',cert)
    progress(start,f'certified fixed column {i:02d}')
    return cert

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['pilot','pilot-repair','main']);args=ap.parse_args()
    start=time.monotonic(); budget=analytic_budget()
    if args.mode in ('pilot','pilot-repair'):
        if args.mode=='pilot':
            if (ROOT/'outputs/BASE_a_0.json').exists():raise RuntimeError('pilot is fresh-only')
            build_base(start);build_multiplier(start)
            base=load_base();build_frame_and_pole(start,base)
        else:
            history=ROOT/'logs/implementation_correction_001'
            expected=json.loads((history/'PRESERVED_OUTPUT_HASHES.json').read_text())
            for n,h in expected.items():assert sha(ROOT/n)==h
            assert not (ROOT/'certificates/ACTION_CERTIFICATE_31.json').exists()
            base=load_base()
        mult=[restore(r) for r in json.loads((ROOT/'outputs/GAMMA_MULTIPLIERS.json').read_text())['values']]
        fp=json.loads((ROOT/'outputs/FRAME_AND_POLE_ENCLOSURES.json').read_text())
        c=finish_column(31,base,mult,fp,budget,start,args.mode)
        dt=time.monotonic()-start
        # Main will reuse all eight transforms, every finite moment, the
        # multiplier array and the completed pilot column; no duplication.
        estimate=31*c['wall_seconds']+15
        gate=estimate<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<480*1024
        save(ROOT/'outputs/PILOT_RESULT.json',{'verdict':'PASS-RESOURCE-GATE' if gate else 'NOT-ADMITTED-RESOURCE',
            'wall_seconds':dt,'CPU_seconds':time.process_time(),
            'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'common_caches_certified':True,'actual_passed_columns':[31],
            'main_estimated_wall_seconds':estimate,'estimate_is_not_a_guarantee':True,
            'counts':COUNTS.copy()})
        if not gate:raise RuntimeError('main resource gate not passed')
    else:
        gate=json.loads((ROOT/'outputs/PILOT_RESULT.json').read_text())
        assert gate['verdict']=='PASS-RESOURCE-GATE'
        if (ROOT/'outputs/MAIN_COMPLETE.json').exists():raise RuntimeError('main cannot repeat')
        if any((ROOT/'outputs'/f'ACTION_{i:02d}.json').exists() for i in range(31)):
            raise RuntimeError('fresh fixed main: existing nonpilot column')
        base=load_base()
        mult=[restore(r) for r in json.loads((ROOT/'outputs/GAMMA_MULTIPLIERS.json').read_text())['values']]
        fp=json.loads((ROOT/'outputs/FRAME_AND_POLE_ENCLOSURES.json').read_text())
        for i in range(31):finish_column(i,base,mult,fp,budget,start,'main')
        guard(start)
        certs=[json.loads((ROOT/'certificates'/f'ACTION_CERTIFICATE_{i:02d}.json').read_text()) for i in range(32)]
        assert all(F(c['whole_line_error_upper'])<F(1,2**18) for c in certs)
        save(ROOT/'outputs/MAIN_COMPLETE.json',{'verdict':'PASS-32-FIXED-NEW-ACTIONS',
            'actual_new_main_columns':31,'pilot_column_reused':[31],
            'all_columns':list(range(32)),'counts':COUNTS.copy(),
            'wall_seconds':time.monotonic()-start,'CPU_seconds':time.process_time(),
            'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'maximum_whole_line_error_upper':str(max(F(c['whole_line_error_upper']) for c in certs)),
            'target':str(F(1,2**18)),'Bnew_less_than_I':'NOT-OBTAINED',
            'new_residual_Gram_LDL_spectrum_calls':0})
        guard(start)

if __name__=='__main__':
    try:main()
    except Exception as e:
        save(ROOT/'logs/FAILURE.json',{'exception':repr(e),'traceback':traceback.format_exc(),
            'counts':COUNTS.copy(),'no_automatic_retry':True})
        raise
