"""CC BY-NC 4.0. Exactly the 437 j=2 mixed kernels; no consumer."""
import gc, time
import v2_support as s
F=s.F
def get_backend():
    globals().update({k:getattr(s,k) for k in ('arb','acb','arb_mat')})
def polynomial_nodes(desc):
    s.phase('j2-polynomial-evaluation-DFT',{'input_complex':s.M,'output_complex':s.M,'retained_nodes':s.NODES})
    assert desc['KOUT']==s.KH and s.KH<s.M//2
    vec=[acb(0)]*s.M
    for k,n in enumerate(s.iter_array(s.OUT/'J2_ACTION_V2.json','J_cosine_numerators')):
        z=acb(arb((int(n),-100 if k==0 else -101)))
        vec[k]=z
        if k:vec[s.M-k]=z
    s.guard();s.inc('new_polynomial_evaluation_DFT_calls')
    transformed=acb.dft(vec);s.guard();del vec;gc.collect()
    max_imag=F(0);max_radius=F(0)
    def values():
        nonlocal max_imag,max_radius
        for i in range(s.NODES):
            z=transformed[i];assert z.is_finite() and z.imag.contains(0)
            max_imag=max(max_imag,s.upper(z.imag));max_radius=max(max_radius,s.upper(z.real.rad()))
            yield z.real
    md=s.packed_write(s.OUT/'cache/J2_POLYNOMIAL_NODES.bin',values(),140,[s.NODES],'J2 cosine polynomial analytic nodes, including DC, unnormalized negative-sign DFT',{'descriptor_sha256':s.sha(s.OUT/'J2_ACTION_V2.json'),'M':s.M,'grid':'pi/4096','source_DFT':False})
    del transformed;gc.collect()
    s.save(s.OUT/'J2_DFT_CERTIFICATE.json',{'nodes':md,'max_native_real_radius':str(max_radius),'max_imaginary_inclusion_magnitude':str(max_imag),'length':s.M,'normalization':'none, Fourier coefficients already normalized','sign':'negative; signed even real embedding yields cosine values','calls':1,'source_DFT_calls':0,'vectors_released_before_quadrature':True})
    return md
def source_a(x):
    """Inherited reflected 8-term real evaluator + full theta tail, not a strip evaluator."""
    x=abs(x);z=arb.pi()*(2*x).exp();total=arb(0)
    for n in range(1,9):
        t=z*n*n;total+=(4*t*t-6*t)*(-t).exp()
    a=total/(1+(-x).exp());s.inc('real_finite_theta_source_evaluations');s.inc('real_finite_theta_terms',8)
    assert a.is_finite() and a.lower()>0
    return s.pad(a,F(1,1<<321))
def shift_cache(fixed,terms):
    items=[(n,w,sgn*logn) for n,w,logn in terms for sgn in (-1,1)]
    co=arb_mat(36,124);sn=arb_mat(36,124)
    for i,(_,w,shift) in enumerate(items):
        for j,m in enumerate(fixed['shifts']):
            si,c=(s.aa(F(m,16))*shift).sin_cos();co[i,j]=c;sn[i,j]=si
    s.inc('prime_shift_phase_pairs',36*124)
    return items,co,sn
def evaluate_chunk(start,count,fixed,facts,tm,fm,shifts):
    items,co_shift,sn_shift=shifts
    cx=arb_mat(count,124);sx=arb_mat(count,124);Q=arb_mat(count,372)
    xs=[];aval=[];weights=[];step=arb.pi()/4096;sq3=arb(3).sqrt();sq5=arb(5).sqrt()
    for row in range(count):
        index=start+row;x=step*index;xs.append(x);ax=source_a(x);aval.append(ax)
        weights.append(ax*step*(1 if index==0 else 2))
        for j,(alpha,m) in enumerate(zip(fixed['alpha'],fixed['shifts'])):
            si,c=(s.aa(F(m,16))*x).sin_cos();cx[row,j]=c;sx[row,j]=si
            Q[row,3*j]=alpha*(1-x*x/96)*c
            Q[row,3*j+1]=-alpha*x*si/(4*sq3)
            Q[row,3*j+2]=-alpha*x*x*c/(48*sq5)
    s.inc('node_feature_phase_pairs',count*124);s.guard()
    ds=[arb_mat(count,36) for _ in range(3)]
    for row,x in enumerate(xs):
        for k,(_,w,shift) in enumerate(items):
            y=x+shift
            if abs(y).lower()>2:
                s.inc('proved_skipped_shifted_source_nodes');continue
            ay=source_a(y);z=w*ay;ds[0][row,k]=z;ds[1][row,k]=z*y;ds[2][row,k]=z*y*y
        if row%8==0:s.guard()
    bc=[d*co_shift for d in ds];bs=[d*sn_shift for d in ds]
    s.inc('prime_phase_native_matrix_products',6);s.inc('prime_phase_scalar_multiply_adds',6*count*36*124)
    del ds;gc.collect();pf=arb_mat(count,372)
    for row in range(count):
        for j,alpha in enumerate(fixed['alpha']):
            co=cx[row,j];si=sx[row,j]
            pf[row,3*j]=alpha*(co*(bc[0][row,j]-bc[2][row,j]/96)-si*(bs[0][row,j]-bs[2][row,j]/96))
            pf[row,3*j+1]=-alpha*(si*bc[1][row,j]+co*bs[1][row,j])/(4*sq3)
            pf[row,3*j+2]=-alpha*(co*bc[2][row,j]-si*bs[2][row,j])/(48*sq5)
    del bc,bs,cx,sx;gc.collect();s.guard()
    pp=Q*tm;ff=Q*fm;prime=pf*tm
    s.inc('old64_main_native_matrix_products',3);s.inc('old64_main_scalar_multiply_adds',3*count*372*64)
    del pf;gc.collect();Z=arb_mat(count,64)
    cg=arb.pi().log()+arb.const_euler()+arb.pi()/2+3*arb.const_log2()
    cosh=[(x/2).cosh() for x in xs]
    for i in range(64):
        cache=s.packed_read(s.OUT/'cache'/f'OLD_GAMMA_{i:02d}.bin',100,start,count)
        for row,zg in enumerate(cache):
            z=zg+(s.aa(F(1,16))-cg*aval[row])*pp[row,i]+ff[row,i]-prime[row,i]+s.aa(facts['poles'][i])*cosh[row]
            Z[row,i]=s.pad(z,32*facts['AI'][i]*F(1,1<<200));assert Z[row,i].is_finite()
    s.inc('complete_old64_bracket_node_evaluations',count*64)
    del pp,ff,prime,aval,xs;gc.collect();return Q,Z,weights,cosh
def envelopes(fixed,facts,desc,cert):
    gamma=s.column_array(fixed['gamma_aggregate_path'],'Gamma_cosine_numerators')
    gamma_l1=sum((F(abs(int(v)),1<<140) for v in gamma),F(0))
    CR=s.feature_majorant(fixed['qc'])+gamma_l1+70*s.feature_majorant(fixed['p'])+224*s.feature_majorant(fixed['p'],F(4))
    DR=abs(fixed['py']);dv=[F(int(v),1<<100) for v in desc['frame_numerators_bits100']]
    m=F(int(desc['moment_m_numerator_bits100']),1<<100)
    CF=F(cert['J_midpoint_l1'])+CR/64+s.feature_majorant(dv);DF=DR/64+2*abs(m);LF=CF+DF
    AP=F(s.small_json(s.CONTRACT/'outputs/FROZEN_CONSTANTS.json')['columns'][2]['A_P']);BR=1234*AP;delta=F(1,1<<320)
    TF=s.aa(9*CF)+s.aa(DF)*arb(1).cosh()+s.aa(delta*BR/64)
    interior=2*(s.aa(F(1,1<<160))*TF+(s.aa(7)+s.aa(delta)).sqrt()*s.aa(delta*BR/64))
    u=arb(4).exp();exterior=(s.aa(128*LF*LF)*(-3*u).exp()*(u**3/3+u*u/3+2*u/9+s.aa(F(2,27)))).sqrt()
    xi=s.upper(interior+exterior)
    alias_unit=s.upper(16*(s.aa(F(2*s.KH-s.M,128))).exp()/(1-arb(-1024).exp()))
    u0=s.aa(F(299,50)).exp()
    tail_unit=s.upper(128*(-3*u0).exp()*(u0**3/3+u0*u0/3+2*u0/9+s.aa(F(2,27))))
    lW=[]
    for l in range(372):
        v=[F(0)]*372;v[l]=F(1);lW.append(s.feature_majorant(v))
    # Use each actual frequency pair, not the old family's 2^-400 gate.
    alias_W=s.upper(16*s.aa(F(s.KH+s.MSTAR-s.M,128)).exp()/(1-arb(-1024).exp()))
    alias_Z=s.upper(16*s.aa(F(s.KH+s.KOLD-s.M,128)).exp()/(1-arb(-1024).exp()))
    data={'CR':str(CR),'DR':str(DR),'CF':str(CF),'DF':str(DF),'LF':str(LF),'proxy_norm_upper':str(3*LF),'new_xi':str(xi),'new_xi_interior_upper':str(s.upper(interior)),'new_xi_exterior_upper':str(s.upper(exterior)),'BR':str(BR),'delta':'2^-320','alias_per_LF_LW':str(alias_W),'alias_per_LF_LZ':str(alias_Z),'alias_per_LF_squared':str(alias_unit),'sampling_tail_per_product_L':str(tail_unit),'old_xi':[str(e) for e in facts['eold']],'norm_proof':'128*(26/27)*exp(-3)<9, so norm <= 3L','alias_proof':'MIXED_GRAM_CONTRACT.md equation (4)','new_xi_proof':'MIXED_GRAM_CONTRACT.md analytic-to-saved interior plus entire real exterior'}
    s.save(s.OUT/'MIXED_ENVELOPE_AND_TRANSFER.json',data)
    return LF,xi,lW,alias_W,alias_Z,alias_unit,tail_unit
def integrate(fixed,facts,desc,cert,terms):
    s.phase('old64-and-j2-node-Gram-start',{'TM':372*64,'old_frame':372*64,'max_chunk':128,'Q':128*372,'Z64':128*64,'F2':128,'no_weighted_Q_duplicate':True})
    LF,xi,lW,aW,aZ,aF,tail=envelopes(fixed,facts,desc,cert)
    tm=arb_mat([[arb((n,-30)) for n in row] for row in fixed['T']])
    fm=arb_mat(372,64)
    for pos,z in enumerate(s.packed_read(s.OUT/'cache/OLD_FRAME_DYADICS.bin',100)):fm[pos//64,pos%64]=z
    shifts=shift_cache(fixed,terms)
    combined=arb_mat([[s.aa((F(fixed['X'][l][2],1<<40)+F(3,64)*fixed['p'][l])/64)+arb((int(desc['frame_numerators_bits100'][l]),-100))] for l in range(372)])
    y=arb_mat([[arb((fixed['Y'][i][2],-46))] for i in range(64)])
    m=arb((int(desc['moment_m_numerator_bits100']),-100));KW=arb_mat(1,372);CZ=arb_mat(1,64);NF=arb(0);checkpoints=[]
    for start in range(0,s.NODES,s.CHUNK):
        clock=time.monotonic();count=min(s.CHUNK,s.NODES-start)
        Q,Z,weights,cosh=evaluate_chunk(start,count,fixed,facts,tm,fm,shifts)
        new=Q*combined-Z*y;s.inc('new_F_assembly_native_matrix_products',2);s.inc('new_F_assembly_scalar_multiply_adds',count*(372+64))
        for row,jn in enumerate(s.packed_read(s.OUT/'cache/J2_POLYNOMIAL_NODES.bin',140,start,count)):new[row,0]+=jn+2*m*cosh[row]
        del cosh;gc.collect();bind={'descriptor_sha256':cert['descriptor_sha256'],'old_transfer_sha256':s.sha(s.OUT/'OLD_ANALYTIC_TRANSFER.json'),'source_index_sha256':s.sha(s.CONTRACT/'SOURCE_INDEX.json'),'start_node':start,'node_count':count,'grid':'pi/4096','full_line_pads_added':False}
        prefix=s.OUT/'checkpoints'/f'nodes_{start:04d}'
        mdQ=s.packed_write(str(prefix)+'_Q.bin',(Q[r,c] for r in range(count) for c in range(372)),140,[count,372],'source-free Q feature bracket nodes row-major; U W=b Q',bind)
        mdZ=s.packed_write(str(prefix)+'_Z64.bin',(Z[r,c] for r in range(count) for c in range(64)),140,[count,64],'complete analytic old G0 brackets incl. source tail and proved skip pads, not affine G',bind)
        mdF=s.packed_write(str(prefix)+'_F2.bin',(new[r,0] for r in range(count)),140,[count,1],'new analytic action bracket J+R/64+Q d+2m cosh; U action=b F; compact delivered action differs by xi',bind)
        mdw=s.packed_write(str(prefix)+'_weight.bin',weights,140,[count],'a-weighted even lattice weights h a(0),2h a(nh), full theta pointwise inclusion',bind)
        # Integrate the actual serialized/re-read intervals so their outward radii are charged.
        del Q,Z,new,weights;gc.collect();Q=arb_mat(count,372);Z=arb_mat(count,64);new=arb_mat(count,1)
        for pos,z in enumerate(s.packed_read(str(prefix)+'_Q.bin',140)):Q[pos//372,pos%372]=z
        for pos,z in enumerate(s.packed_read(str(prefix)+'_Z64.bin',140)):Z[pos//64,pos%64]=z
        for pos,z in enumerate(s.packed_read(str(prefix)+'_F2.bin',140)):new[pos,0]=z
        weights=list(s.packed_read(str(prefix)+'_weight.bin',140));nw=arb_mat(1,count)
        for row,w in enumerate(weights):nw[0,row]=w*new[row,0]
        KW+=nw*Q;CZ+=nw*Z;NF+=(nw*new)[0,0]
        s.inc('physical_Gram_native_matrix_products',3);s.inc('physical_Gram_scalar_multiply_adds',437*count);s.inc('completed_lattice_nodes',count);s.inc('completed_chunks')
        del Q,Z,new,nw,weights;gc.collect()
        checkpoint={'start':start,'count':count,'nodes':[mdQ,mdZ,mdF,mdw],'chunk_wall_seconds':time.monotonic()-clock,'completed_nodes':start+count,'unique_integral_targets':437,'whole_line_integrals_complete':False}
        checkpoints.append(checkpoint)
        s.save(s.OUT/'checkpoints/NODE_CHECKPOINT_INDEX.json',{'chunks':checkpoints,'completed_nodes':start+count,'required_nodes':s.NODES,'analytic_brackets':True,'full_line_pads_added':False})
        s.save(s.OUT/'checkpoints/PARTIAL_437_LATTICE_SUMS.json',{'completed_nodes':start+count,'bits':140,'KW':[s.rec(KW[0,l],140) for l in range(372)],'G0F':[s.rec(CZ[0,i],140) for i in range(64)],'self':s.rec(NF,140),'whole_line_integrals_complete':False})
        s.phase('node-chunk-complete',{'completed_nodes':start+count,'persistent_native':372*64*2+437,'chunk_arrays_released':True})
    assert s.COUNTS['completed_lattice_nodes']==3912 and s.COUNTS['physical_Gram_scalar_multiply_adds']==1709544
    del fm,shifts,combined,y;gc.collect();rawW=[s.rec(KW[0,l],140) for l in range(372)];rawZ=[s.rec(CZ[0,i],140) for i in range(64)];rawN=s.rec(NF,140)
    padsW=[];padsZ=[]
    for l in range(372):
        qpad=(aW+tail)*LF*lW[l];transfer=xi*2048;pad=qpad+transfer;padsW.append({'quadrature':str(qpad),'analytic_transfer':str(transfer),'total':str(pad)});KW[0,l]=s.pad(s.restore(rawW[l],140),pad)
    for i in range(64):
        qpad=(aZ+tail)*LF*facts['lold'][i];transfer=xi*3*facts['lold'][i]+facts['eold'][i]*3*LF+xi*facts['eold'][i];pad=qpad+transfer;padsZ.append({'quadrature':str(qpad),'analytic_transfer':str(transfer),'total':str(pad)});CZ[0,i]=s.pad(s.restore(rawZ[i],140),pad)
    qN=(aF+tail)*LF*LF;tN=2*xi*3*LF+xi*xi;NF=s.pad(s.restore(rawN,140),qN+tN)
    kwrec=[s.rec(KW[0,l],140) for l in range(372)];czrec=[s.rec(CZ[0,i],140) for i in range(64)]
    for l,r in enumerate(kwrec):KW[0,l]=s.restore(r,140)
    for i,r in enumerate(czrec):CZ[0,i]=s.restore(r,140)
    affine=(KW*tm)*(s.aa(F(3,64)));ar=[s.rec(affine[0,i],140) for i in range(64)]
    for i,r in enumerate(ar):affine[0,i]=s.restore(r,140)
    CG=CZ-affine;del tm;gc.collect()
    final={'format':'SERABI_J2_437_MIXED_KERNELS_V2','column_zero_based':2,'bits':140,'KW':kwrec,'GF':[s.rec(CG[0,i],140) for i in range(64)],'self':s.rec(NF,140),'physical_kernel_count':437,'physical_Gram_multiply_adds':1709544,'grid_nodes':3912,'full_line_pads_added_once':True,'affine_formula':'G*F=G0*F-(3/64) T^T K_F^T; whole-line W T exterior retained','descriptor_sha256':cert['descriptor_sha256'],'envelope_sha256':s.sha(s.OUT/'MIXED_ENVELOPE_AND_TRANSFER.json'),'checkpoint_index_sha256':s.sha(s.OUT/'checkpoints/NODE_CHECKPOINT_INDEX.json')}
    s.save(s.OUT/'J2_437_KERNELS.json',final)
    s.save(s.OUT/'J2_437_LEDGER.json',{'bits':140,'raw_lattice_KW':rawW,'raw_lattice_G0F':rawZ,'raw_lattice_self':rawN,'KW_pads':padsW,'G0F_pads':padsZ,'self_pad':{'quadrature':str(qN),'analytic_transfer':str(tN),'total':str(qN+tN)},'padded_G0F_records':czrec,'affine_correction_records':ar,'physical_action_error_B2_separate_from_xi':cert['B2'],'whole_line_exterior':'included by new xi and G0-transfer, with explicit -3V/64 on whole line','native_and_serialization_radii':'all checkpoint and lattice ledger records rehydrated before accumulation or padding; final rec is outward','other_residual_columns':0,'positivity_consumers':0})
    reread=s.small_json(s.OUT/'J2_437_KERNELS.json');assert reread==final
    for row in final['KW']+final['GF']+[final['self']]:assert s.restore(row,140).is_finite()
    del KW,CZ,CG,NF,affine;gc.collect();s.phase('437-kernels-certified',{'consumer_matrices':0})
    return final
