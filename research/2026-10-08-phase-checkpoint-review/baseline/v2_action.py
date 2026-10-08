"""CC BY-NC 4.0. One fixed H64 residual action; no work at import."""
import gc, json, pathlib, time
import v2_support as s
F=s.F
def get_backend():
    globals().update({k:getattr(s,k) for k in ('arb','acb','acb_poly','arb_mat')})
def old_facts(fixed,convert_nodes=True):
    gamma_l1=[];df_l1=[];poles=[];AI=[];eold=[];lold=[];frames=arb_mat(372,64);old_hashes=[];nodes=[]
    budget=s.small_json(s.REL/'certificates/ALL64_ACTION_AND_QUADRATURE_BUDGET.json')
    assert len(budget['analytic_extension_to_saved_G_L2_errors'])==64
    for i in range(64):
        path=s.action_path(i);h=s.sha(path);md=s.metadata(path)
        assert md['format']=='SERABI_FINITE_ANALYTIC_U_ACTION_V1' and md['KOUT']==s.KOLD
        assert md['support']==['-2','2'] and md['outside_support']=='exactly zero'
        assert md['cell_sha256']==s.sha(s.REL/'inputs/retained_cells_exact.csv')
        g=sum((abs(F(int(n),1<<100)) for n in s.iter_array(path,'Gamma_cosine_numerators')),F(0));gamma_l1.append(g)
        frame=list(map(int,s.iter_array(path,'frame_numerators')));assert len(frame)==372
        for l,v in enumerate(frame):frames[l,i]=arb((v,-100))
        df=sum((abs(F(v,1<<100)) for v in frame),F(0));df_l1.append(df)
        pole=F(int(md['pole_numerator']),1<<100);poles.append(pole)
        ai=2*sum((F(97,96)*abs(F(fixed['T'][3*j][i],1<<30))+abs(F(fixed['T'][3*j+1][i],1<<30))/4+abs(F(fixed['T'][3*j+2][i],1<<30))/48 for j in range(124)),F(0));AI.append(ai)
        ei=(ai*F(16561,16)+g+2*df+abs(pole)+ai)*F(1,1<<94)
        assert ei==F(budget['analytic_extension_to_saved_G_L2_errors'][i]);eold.append(ei)
        v=[F(fixed['T'][l][i],1<<30) for l in range(372)];dv=[F(n,1<<100) for n in frame]
        # Both prime directions total below 32, |log n| < 4; all bounds rational.
        cz=s.feature_majorant(v)/16+g+70*s.feature_majorant(v)+224*s.feature_majorant(v,F(4))+s.feature_majorant(dv)
        lold.append(cz+abs(pole));old_hashes.append(h)
        nodepath=s.gamma_path(i);nmd=s.metadata(nodepath)
        assert nmd['descriptor_sha256']==h and nmd['length']==s.M and nmd['dyadic_bits']==100
        if convert_nodes:
            md=s.packed_write(s.OUT/'cache'/f'OLD_GAMMA_{i:02d}.bin',s.iter_array(nodepath,'nodes'),100,[s.NODES], 'inherited Gamma-only analytic polynomial nodes; not complete Z',{'descriptor_sha256':h,'original_node_sha256':s.sha(nodepath),'grid':'pi/4096','column':i})
            nodes.append(md)
        s.inc('inherited_action_descriptors_scanned');s.guard()
    eps=sum((abs(F(fixed['Y'][i][2],1<<40))*eold[i] for i in range(64)),F(0))
    s.save(s.OUT/'OLD_ANALYTIC_TRANSFER.json',{'errors':[str(v) for v in eold],'epsilon_j2':str(eps),'old_bracket_L':[str(v) for v in lold],'old_action_hashes':old_hashes,'gamma_cache_records':nodes})
    frame_cache=s.packed_write(s.OUT/'cache/OLD_FRAME_DYADICS.bin',(frames[l,i] for l in range(372) for i in range(64)),100,[372,64],'exact old frame coefficients, row-major l,i',{'old_action_hashes':old_hashes})
    del frames;gc.collect()
    return {'poles':poles,'AI':AI,'eold':eold,'epsilon':eps,'lold':lold,'old_hashes':old_hashes,'frame_cache':frame_cache}
def frame(fixed,facts):
    s.phase('j2-frame-saved-Gram',{'Aobs':372*372,'K0':64*372,'saved-D':64*372,'one-frame-column':372})
    x=arb_mat([[arb((fixed['X'][l][2],-40))] for l in range(372)])
    y=arb_mat([[arb((fixed['Y'][i][2],-40))] for i in range(64)])
    a=arb_mat([[s.restore(v) for v in row] for row in s.iter_array(s.DIAG/'sources/AOBS_ENCLOSURE.json','entries')]);assert a.nrows()==a.ncols()==372
    result=a*x;del a,x;gc.collect()
    k=arb_mat([[s.restore(v) for v in row] for row in s.iter_array(s.DIAG/'sources/G0_GRAM_ENCLOSURES.json','K0')]);assert k.nrows()==64 and k.ncols()==372
    result-=k.transpose()*y;del k;gc.collect()
    d=arb_mat([[s.restore(v) for v in row] for row in s.iter_array(s.DIAG/'sources/AFFINE_GRAM_ENCLOSURES.json','D')]);assert d.nrows()==64 and d.ncols()==372
    result+=F(3,64).numerator*d.transpose()*y/64;del d,y;gc.collect()
    nums=[];records=[];errors=[]
    for l in range(372):
        value=s.pad(result[l,0],2048*facts['epsilon']);before=s.rec(value,140);n,_=s.quantize(value)
        e=F(abs(int(before[0])-n*(1<<40))+int(before[1]),1<<140)
        nums.append(str(n));records.append(before);errors.append(e)
    total=2048*sum(errors,F(0));assert total<=F(1,1<<30),'2048 sum(e_d) measured gate'
    s.save(s.OUT/'J2_FRAME_CERTIFICATE.json',{'moment_records_bits140':records,'dyadic_numerators_bits100':nums,'errors':[str(x) for x in errors],'2048_sum_error':str(total),'analytic_transfer_epsilon':str(facts['epsilon']),'formula':'A X - (K0 - 3 D/64)^T Y; radius += 2048 epsilon per entry','physical_integrals':0})
    del result;gc.collect();return nums,total
def shared():
    s.phase('shared-multiplier-extension',{'D':s.KH+1,'Gamma':s.KH+1})
    path=s.OLD/'outputs/GAMMA_MULTIPLIERS.json';md=s.metadata(path);assert md['KOUT']==s.KOLD and md['denominator_power_of_two']==140
    multipliers=[s.restore(v,140) for v in s.iter_array(path,'values')];assert len(multipliers)==s.KOLD+1 and multipliers[0].is_zero()
    psi0=-arb.const_euler()-arb.pi()/2-3*arb.const_log2();new=[]
    for k in range(s.KOLD+1,s.KH+1):
        v=acb(s.aa(F(1,4)),s.aa(F(k,32))).digamma().real-psi0
        assert v.is_finite() and v.lower()>0 and v.rad()<s.aa(F(1,1<<100)),'new Gamma inclusion gate'
        new.append(s.rec(v,140));s.inc('new_Gamma_multiplier_evaluations')
        if k%512==0:s.guard()
    md=s.packed_write(s.OUT/'cache/GAMMA_EXTENSION.bin',new,140,[8192],'new Gamma multiplier inclusions k=32997..41188',{'original_multiplier_sha256':s.sha(path),'start_k':32997,'end_k':41188})
    multipliers.extend(s.packed_read(s.OUT/'cache/GAMMA_EXTENSION.bin',140));assert len(multipliers)==s.KH+1
    del new;gc.collect()
    cg=arb.pi().log()+arb.const_euler()+arb.pi()/2+3*arb.const_log2()
    terms=[(n,s.aa(p).log()/s.aa(n).sqrt(),s.aa(n).log()) for n,p in s.PRIME_PAIRS]
    assert len(terms)==18 and (2*sum((w for _,w,_ in terms),arb(0))).upper()<32 and cg.upper()<10
    D=[arb(cg) for _ in range(s.KH+1)];phase_records=[]
    s.phase('shared-D-phase-recurrence',{'D_real':s.KH+1,'one_complex_phase':1,'Gamma_real':s.KH+1})
    for n,w,logn in terms:
        rho=(acb(0,logn/16)).exp();z=acb(1);maxrad=F(0)
        for k in range(s.KH+1):
            if k:z*=rho;s.inc('complex_phase_recurrence_products')
            assert z.is_finite();maxrad=max(maxrad,s.upper(z.real.rad()),s.upper(z.imag.rad()))
            D[k]+=2*w*z.real
            if k%2048==0:s.guard()
        phase_records.append({'n':n,'weight_bits140':s.rec(w,140),'log_n_bits140':s.rec(logn,140),'seed_real_bits140':s.rec(rho.real,140),'seed_imag_bits140':s.rec(rho.imag,140),'terminal_real_bits140':s.rec(z.real,140),'terminal_imag_bits140':s.rec(z.imag,140),'max_native_radius':str(maxrad),'recurrence_products':s.KH,'recurrence_resets':0})
    assert all(v.is_finite() and s.upper(v)<42 for v in D)
    dmd=s.packed_write(s.OUT/'cache/D_PHASE_DIAGONAL.bin',D,140,[s.KH+1],'D_k=cGamma+2 sum c_n Re(rho_n^k), k=0..41188; both inner and outer uses',{'prime_terms':18,'both_shift_signs':True,'resets':0})
    del D;gc.collect();D=list(s.packed_read(s.OUT/'cache/D_PHASE_DIAGONAL.bin',140))
    s.save(s.OUT/'SHARED_MULTIPLIER_PHASE_CERTIFICATE.json',{'original_multiplier_sha256':s.sha(path),'original_entries_unchanged':32997,'extension':md,'D':dmd,'phase_records':phase_records,'precision_bits':160,'new_source_DFTs':0,'total_recurrence_products':s.COUNTS['complex_phase_recurrence_products']})
    return D,multipliers,terms
def modulation(vector,r,fixed):
    values=[acb(0)]*(2*s.MSTAR+1);effective=False
    for j,(alpha,m) in enumerate(zip(fixed['alpha'],fixed['shifts'])):
        v0,v1,v2=map(s.aa,vector[3*j:3*j+3])
        if r==0:z=acb(alpha*v0/2)
        elif r==1:z=acb(0,alpha*v1/(8*arb(3).sqrt()))
        else:z=acb(-alpha*(v0/96+v2/(48*arb(5).sqrt()))/2)
        values[s.MSTAR+m]=values[s.MSTAR+m]+z;values[s.MSTAR-m]=values[s.MSTAR-m]+z.conjugate();effective=effective or not z.is_zero()
    assert effective,'all seven products must have nonzero operands'
    return acb_poly(values)
def real_even(poly,origin,k):
    zp=poly[origin+k];zm=poly[origin-k]
    assert zp.is_finite() and zm.is_finite() and zp.imag.contains(0) and zm.imag.contains(0),'real-even coefficient inclusion'
    assert zp.real.overlaps(zm.real)
    return (zp.real+zm.real)/2
def linear_pole(fixed):
    total=arb(0)
    for r in range(3):
        cache=s.primitive(r,'kappa')
        for j,(al,m) in enumerate(zip(fixed['alpha'],fixed['shifts'])):
            v0,v1,v2=map(s.aa,fixed['qc'][3*j:3*j+3])
            if r==0:total+=al*v0*s.moments(cache,r,m,'cos')
            elif r==1:total-=al*v1*s.moments(cache,r,m,'sin')/(4*arb(3).sqrt())
            else:total-=al*(v0/96+v2/(48*arb(5).sqrt()))*s.moments(cache,r,m,'cos')
        del cache;gc.collect()
    return total/2
def produce(fixed,D,mult,frame_nums,frame_error):
    s.phase('j2-six-first-products',{'one-source':16385,'one-modulation':49609,'FC':65993,'FP':65993,'one-product':65993})
    FC=acb_poly([]);FP=acb_poly([])
    for r in range(3):
        base=s.primitive(r);A=acb_poly([s.signed_primitive(base,r,k) for k in range(-s.K,s.K+1)]);del base
        pc=modulation(fixed['qc'],r,fixed);s.inc('polynomial_products_started');product=A*pc;s.inc('polynomial_products');FC+=product;del product,pc;gc.collect();s.guard()
        pp=modulation(fixed['p'],r,fixed);s.inc('polynomial_products_started');product=A*pp;s.inc('polynomial_products');FP+=product;del product,pp,A;gc.collect();s.guard()
    assert FC.degree()<=2*s.KOLD and FP.degree()<=2*s.KOLD
    gy=list(map(int,s.column_array(fixed['gamma_aggregate_path'],'Gamma_cosine_numerators')));assert len(gy)==s.KOLD+1
    values=[]
    for k in range(-s.KOLD,s.KOLD+1):
        v=D[abs(k)]*real_even(FP,s.KOLD,abs(k))-arb((gy[abs(k)],-140 if k==0 else -141))
        values.append(acb(v));s.inc('inner_D_coefficient_products')
    B=acb_poly(values);del values,FP;gc.collect()
    m=linear_pole(fixed);kap=s.primitive(0,'kappa');dot=arb(0)
    for k in range(s.K+1):dot+=kap[k]*real_even(B,s.KOLD,k)*(1 if k==0 else 2);s.inc('pole_dot_terms')
    m+=(32*arb.pi()/2)*dot-s.aa(fixed['py'])/4
    constants=s.small_json(s.CONTRACT/'outputs/FROZEN_CONSTANTS.json');col=constants['columns'][2];AP=F(col['A_P']);gamma0=F(col['Gamma_derivative_l1'][0])
    tau=F(s.small_json(s.CONTRACT/'outputs/ANALYTIC_PREBUDGET.json')['coefficient_tail_derivative_bounds'][0])
    nA=max(F(d['D0_fourier_l1_upper']) for k,d in constants['fourier_base_bounds'].items() if k.startswith('a_'));nk=F(constants['fourier_base_bounds']['kappa_0']['D0_fourier_l1_upper'])
    qP=arb(-2*32*arb.pi()).exp();delta=(1<<17)*1024*qP*(5-4*qP)/(1-qP)**2
    pole_pad=(32*arb.pi()/2)*(s.aa(tau*(42*AP*nA+gamma0)+(nk+tau)*42*AP*tau)+delta*42*s.aa(AP))
    m=s.pad(m,s.upper(pole_pad));mrec=s.rec(m,140);mn,_=s.quantize(m);em=F(abs(int(mrec[0])-mn*(1<<40))+int(mrec[1]),1<<140)
    s.save(s.OUT/'J2_POLE_CERTIFICATE.json',{'prequantization_bits140':mrec,'numerator_bits100':str(mn),'error_upper':str(em),'analytic_tail_and_product_image_pad':str(s.upper(pole_pad)),'stored_value':'m = integral h cosh; action cost |delta m|','formula':'1/2 integral kappa Q_C + P/2 DC(K0*B) - p_y/4','physical_integrals':0,'dot_terms':s.K+1})
    assert em<=F(1,1<<30),'measured pole gate'
    del kap,dot,m;gc.collect()
    s.phase('j2-seventh-product',{'A0':16385,'B':65993,'FC':65993,'product_output':82377})
    base=s.primitive(0);A=acb_poly([acb(base[abs(k)]) for k in range(-s.K,s.K+1)]);del base
    s.inc('polynomial_products_started');H=A*B;s.inc('polynomial_products');del A,B;gc.collect();assert s.COUNTS['polynomial_products']==7
    assert H.degree()==2*s.KH and not H[2*s.KH].real.contains(0),'actual outer product support must reach 41188'
    # Add shifted F_C and the kappa term in an explicit signed origin.
    nums=[];eJ=F(0);l1=F(0);before_records=[];kap=s.primitive(0,'kappa')
    for k in range(s.KH+1):
        h=real_even(H,s.KH,k)
        if k<=s.KOLD:h+=real_even(FC,s.KOLD,k)
        if k<=s.K:h-=s.aa(fixed['py'])*kap[k]/2
        coefficient=(mult[k]-D[k])*h*(1 if k==0 else 2);s.inc('final_multiplier_coefficient_products')
        before=s.rec(coefficient,140);n,_=s.quantize(coefficient)
        e=F(abs(int(before[0])-n*(1<<40))+int(before[1]),1<<140)
        nums.append(str(n));before_records.append(before);eJ+=e;l1+=F(abs(n),1<<100)
        if k%1024==0:s.guard()
    del H,FC,kap;gc.collect();assert eJ/2<=F(1,1<<30),'measured J gate'
    s.save(s.OUT/'J2_COEFFICIENT_INTERVALS.json',{'bits':140,'role':'combined J=(mGamma-D)H, cosine coordinates with DC','values':before_records});del before_records
    remaining=s.small_json(s.CONTRACT/'outputs/REMAINING_PREBUDGET.json')['columns'][2]
    analytic={k:F(remaining[k]) for k in ['Gamma_product_image_L2_upper','Gamma_physical_image_L2_upper','finite_prime_and_local_transfer_L2_upper','infinite_prime_tail_L2_upper','finite_action_exterior_L2_upper','theta8_transfer_L2_upper']}
    analytic['Gamma_frequency_truncation_L2_upper']=F(s.small_json(s.CONTRACT/'outputs/ANALYTIC_PREBUDGET.json')['columns'][2]['Gamma_truncation_L2_upper'])
    assert sum(analytic.values(),F(0))==F(remaining['analytic_total_L2_upper'])
    errors={**analytic,'measured_J_coefficient_error_half':eJ/2,'measured_frame_error_2048_sum':frame_error,'measured_pole_error':em};B2=sum(errors.values(),F(0))
    assert B2<F(1,1<<18),'B2 gate'
    bindings={'X40_sha256':s.sha(s.ADM/'outputs/X40.csv'),'Y40_sha256':s.sha(s.ADM/'outputs/Y40.csv'),'T64_sha256':s.sha(s.REL/'inputs/T64_dyadic_numerators.csv'),'C64_sha256':s.sha(s.REL/'inputs/C64_dyadic_numerators.csv'),'cell_sha256':s.sha(s.REL/'inputs/retained_cells_exact.csv'),'contract_sha256':s.sha(s.CONTRACT/'REPORT.md'),'mixed_Gram_contract_sha256':s.sha(s.CONTRACT/'review/MIXED_GRAM_CONTRACT.md'),'source_index_sha256':s.sha(s.CONTRACT/'SOURCE_INDEX.json'),'old64_hashes_and_transfer_sha256':s.sha(s.OUT/'OLD_ANALYTIC_TRANSFER.json'),'coefficient_intervals_sha256':s.sha(s.OUT/'J2_COEFFICIENT_INTERVALS.json'),'shared_certificate_sha256':s.sha(s.OUT/'SHARED_MULTIPLIER_PHASE_CERTIFICATE.json'),'frame_certificate_sha256':s.sha(s.OUT/'J2_FRAME_CERTIFICATE.json'),'pole_certificate_sha256':s.sha(s.OUT/'J2_POLE_CERTIFICATE.json')}
    desc={'format':'SERABI_SOURCE_PRODUCT_U_H64_ACTION_V2','column_zero_based':2,'operator':'H64=L+I/64; same minimum closed even weighted operator','coordinate':'ordinary Lebesgue L2(dx), Uq=bR','true_source':'infinite theta kappa; no log-concavity assumption','trial':'frozen X40,Y40; R=Q_C-Gamma_y+D(a P_y)-p_y cosh','support':['-2','2'],'outside_support':'exactly zero','K_source':s.K,'KOUT':s.KH,'J_role':'combined (mGamma-D)H; DC allowed','J_denominator_bits':100,'J_cosine_numerators':nums,'frame_numerators_bits100':frame_nums,'moment_m_numerator_bits100':str(mn),'stored_pole_convention':'m, action coefficient 2m','frozen_aggregate_bits':140,'X_Y_bits':40,'T_bits':30,'prime_cutoff':32,'prime_terms':list(s.PRIME_PAIRS),'both_shift_signs':True,'theta_terms_in_approximant':8,'M':s.M,'grid':'pi/4096','bindings':bindings}
    desc['eta64_exact']='1446776856241610348487954379752034183297365381007/92620636523388719034562694367509285563269120000000'
    desc['precision_bits']=160;desc['true_q_definition']='U q_2=b[Q(X40_2+(3/64)T64 Y40_2)-Z64 Y40_2], with full infinite theta source and analytic old G0 brackets'
    desc['prime_terms']=[list(p) for p in s.PRIME_PAIRS]
    s.validate_descriptor(desc)
    s.save(s.OUT/'J2_ACTION_V2.json',desc)
    # Hash-bound rehydration checks: never apply the old zero-DC invariant.
    assert s.metadata(s.OUT/'J2_ACTION_V2.json')['format']=='SERABI_SOURCE_PRODUCT_U_H64_ACTION_V2'
    assert list(s.iter_array(s.OUT/'J2_ACTION_V2.json','J_cosine_numerators'))==nums
    cert={'status':'PASS-J2-ACTION-ONLY','column_zero_based':2,'B2':str(B2),'target':'2^-18','errors_L2_upper':{k:str(v) for k,v in errors.items()},'eJ':str(eJ),'2048_sum_ed':str(frame_error),'em':str(em),'J_midpoint_l1':str(l1),'descriptor_sha256':s.sha(s.OUT/'J2_ACTION_V2.json'),'counts':s.COUNTS.copy(),'analytic_prebudget_is_not_measured_error':True,'new_H_action_columns':1,'other_columns':0}
    s.save(s.OUT/'J2_ACTION_CERTIFICATE.json',cert);s.inc('new_H64_residual_action_columns');s.phase('j2-action-certified',{'serialized_J_coefficients':s.KH+1})
    return desc,cert
