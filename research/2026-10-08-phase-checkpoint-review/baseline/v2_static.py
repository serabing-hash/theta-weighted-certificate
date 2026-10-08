"""CC BY-NC 4.0. Saved-byte/AST/static checks and small source-free fixtures."""
import ast, gc, json, os, pathlib, resource, subprocess, sys, tempfile, time
import v2_support as s
F=s.F
def fixture():
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(30,30))
    s.backend();import flint,v2_action as a
    a.get_backend();arb=s.arb;acb=s.acb;poly=s.acb_poly
    assert flint.__version__=='0.9.0' and s.ctx.prec==160 and s.ctx.threads==1
    actual_flint=flint.__FLINT_VERSION__
    assert arb(1).overlaps(arb(1)) and arb(1).intersection(arb(1)).contains(1)
    sign=acb.dft([acb(0),acb(1),acb(0),acb(0)])
    assert all(z.contains(w) for z,w in zip(sign,[acb(1),acb(0,-1),acb(-1),acb(0,1)]))
    original=(s.K,s.MSTAR,s.KOLD,s.KH,s.M)
    s.K,s.MSTAR,s.KOLD,s.KH,s.M=2,3,5,7,32
    fixed={'alpha':[arb(1)],'shifts':[3]};qc=[F(2),F(3),F(5)];p=[F(7),F(11),F(13)]
    FC=poly([]);FP=poly([]);count=0
    for r in range(3):
        base=[arb(1),arb(2),arb(3)] if not r%2 else [arb(0),arb(2),arb(3)]
        src=poly([s.signed_primitive(base,r,k) for k in range(-2,3)])
        FC+=src*a.modulation(qc,r,fixed);count+=1
        FP+=src*a.modulation(p,r,fixed);count+=1
    for k in range(6):assert a.real_even(FC,5,k).is_finite() and a.real_even(FP,5,k).is_finite()
    # Exact signed origins and FC/kap embedding, with an independent DC convolution sum.
    B=poly([3*FP[k] for k in range(11)])
    src=poly([acb(1),acb(2),acb(3),acb(2),acb(1)])
    H=src*B;count+=1;assert count==7 and H.degree()==14 and not H[14].is_zero()
    dc=sum((src[k]*B[7-k] for k in range(5)),acb(0));assert H[7].overlaps(dc)
    out=[]
    for k in range(8):
        val=a.real_even(H,7,k)+(a.real_even(FC,5,k) if k<=5 else arb(0))
        out.append(-3*val*(1 if k==0 else 2))
    assert not out[0].contains(0),'fixture must verify nonzero combined-J DC'
    vec=[acb(0)]*32
    for k,z in enumerate(out):
        vec[k]=acb(z if k==0 else z/2)
        if k:vec[32-k]=acb(z/2)
    transform=acb.dft(vec)
    for n in range(32):
        expected=sum((v*(arb(2)*arb.pi()*k*n/32).cos() for k,v in enumerate(out)),arb(0))
        assert transform[n].imag.contains(0) and transform[n].real.overlaps(expected)
    # A constant plus one cosine explicitly establishes normalization and DC.
    small=[acb(0)]*8;small[0]=acb(3);small[1]=small[7]=acb(1)
    result=acb.dft(small);assert result[0].real.contains(5) and result[4].real.contains(1)
    rho=acb(0,1);z=acb(1)
    for k in range(1,17):z*=rho;assert z.contains(rho**k)
    (s.K,s.MSTAR,s.KOLD,s.KH,s.M)=original
    oldout=s.OUT;s.OUT=s.ROOT/'static'
    values=[arb(0),arb(3),arb(-2),s.pad(arb(1),F(1,1<<120))]
    md=s.packed_write(s.OUT/'fixture/roundtrip.bin',values,140,[4],'source-free serialization fixture',{})
    loaded=list(s.packed_read(s.OUT/'fixture/roundtrip.bin',140));assert all(x.contains(y) for x,y in zip(loaded,values))
    # The six numerical cache/phase/digamma APIs are exercised without the physical source.
    assert acb(F(1,4).numerator,F(1,4).denominator).digamma().is_finite()
    assert (poly([1,2])*poly([3,4])).coeffs()==[acb(3),acb(10),acb(8)]
    original_reader=s.REL/'code/action_common.py';tree=ast.parse(original_reader.read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='full_approximation')
    reader_scope={'A':s.aa,'arb':arb,'OUT_BITS':100}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),str(original_reader),'exec'),reader_scope)
    try:reader_scope['full_approximation'](0,arb(0),{'format':'SERABI_SOURCE_PRODUCT_U_H64_ACTION_V2','J_cosine_numerators':['3']})
    except KeyError as exc:assert exc.args==('Gamma_cosine_numerators',)
    else:raise AssertionError('original V1 reader accepted V2')
    data={'status':'PASS-SOURCE-FREE-FIXTURES','precision_bits':160,'python_flint':'0.9.0','FLINT':actual_flint,'threads':1,'small_products':7,'DFT_fixture_lengths':[4,32,8],'physical_source_evaluations':0,'physical_action_columns':0,'physical_kernel_integrals':0,'pilot_attempts':0,'nonzero_DC_verified':True,'negative_DFT_sign_verified':True,'unnormalized_DFT_verified':True,'signed_origins_and_support_verified':True,'real_even_inclusions_verified':True,'original_V1_reader_rejects_V2_before_source_evaluation':True,'original_V1_reader_sha256':s.sha(original_reader),'serialized_interval_roundtrip':md,'memory':s.proc_memory()}
    s.save(s.ROOT/'static/SOURCE_FREE_FIXTURES.json',data);s.OUT=oldout;print(json.dumps(data))
def saved_checks():
    start=time.monotonic();inputs=s.small_json(s.ROOT.parent/'ATTACHED_INPUT_VERIFICATION.json')
    for entry in inputs:assert pathlib.Path(entry['path']).stat().st_size==entry['expected_bytes'] and s.sha(entry['path'])==entry['expected_sha256']
    previous=[s.ROOT.parent/'SERABI_RH_V2_J2_HOLD_20261008/HOLD_STATUS.json',s.ROOT.parent/'SERABI_RH_V2_J2_TRANSFER_TOOL_HOLD_20261008/PREVIOUS_EXECUTION_RECONFIRMATION.json']
    for path in previous:
        d=s.small_json(path);assert d.get('pilot_attempts',d.get('previous_pilot_attempts'))==0 and d.get('V2_implemented',d.get('previous_V2_implemented')) is False
    assert not (s.ROOT/'PILOT_SINGLE_USE.json').exists() and not (s.OUT/'PILOT_STATUS.json').exists()
    # Re-use only the provided path-only source verifier, not producer imports.
    r=subprocess.run([sys.executable,str(s.ROOT/'portable_replay/code/verify_source_bindings.py'),'--shared-root',str(s.ORIGINAL)],capture_output=True,text=True)
    (s.ROOT/'static/SOURCE_BINDINGS_FINAL.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
    T=s.integers(s.REL/'inputs/T64_dyadic_numerators.csv');X=s.integers(s.ADM/'outputs/X40.csv');Y=s.integers(s.ADM/'outputs/Y40.csv')
    assert len(T)==len(X)==372 and all(len(v)==64 for v in T) and all(len(v)==4 for v in X) and len(Y)==64 and all(len(v)==4 for v in Y)
    agg=s.CONTRACT/'outputs/FROZEN_AGGREGATE_COEFFICIENTS.json';p=list(map(int,s.column_array(agg,'P_Q_numerators_bits70')))
    assert p==[sum(T[l][i]*Y[i][2] for i in range(64)) for l in range(372)]
    source=[]
    for kind in ('a','kappa'):
        for r in range(3):
            path=s.OLD/'outputs'/f'BASE_{kind}_{r}.json';md=s.metadata(path)
            assert md['K']==8192 and md['denominator_power_of_two']==140 and md['component']==('imag' if r%2 else 'real')
            count=0
            for n,rad in s.iter_array(path,'values'):assert int(rad)>=0;count+=1
            assert count==8193;source.append({'path':str(path.relative_to(s.ROOT)),'sha256':s.sha(path),'records':count,'component':md['component']})
    nodes=[];maxmid=maxrad=0
    for i in range(64):
        action=s.action_path(i);md=s.metadata(action);assert md['format']=='SERABI_FINITE_ANALYTIC_U_ACTION_V1' and md['KOUT']==32996 and md['support']==['-2','2'] and md['outside_support']=='exactly zero'
        np=s.gamma_path(i);nm=s.metadata(np);ah=s.sha(action)
        assert nm['descriptor_sha256']==ah and nm['length']==131072 and nm['dyadic_bits']==100
        count=0
        for mid,rad in s.iter_array(np,'nodes'):
            n,r=int(mid),int(rad);assert -(1<<255)<=n<(1<<255) and 0<=r<(1<<256)
            maxmid=max(maxmid,abs(n).bit_length());maxrad=max(maxrad,r.bit_length());count+=1
        assert count==3912;nodes.append({'column':i,'action_sha256':ah,'node_sha256':s.sha(np),'records':count})
    mp=s.OLD/'outputs/GAMMA_MULTIPLIERS.json';mm=s.metadata(mp);assert mm['KOUT']==32996 and mm['denominator_power_of_two']==140
    count=0
    for n,rad in s.iter_array(mp,'values'):
        if count==0:assert int(n)==int(rad)==0
        assert int(rad)>=0;count+=1
    assert count==32997
    assert s.PRIME_PAIRS==((2,2),(3,3),(4,2),(5,5),(7,7),(8,2),(9,3),(11,11),(13,13),(16,2),(17,17),(19,19),(23,23),(25,5),(27,3),(29,29),(31,31),(32,2))
    sources={str(p.relative_to(s.ROOT)):s.sha(p) for p in sorted(s.CODE.glob('*.py'))}
    for p in s.CODE.glob('v2_*.py'):
        tree=ast.parse(p.read_text());assert not any(isinstance(n,(ast.Import,ast.ImportFrom)) and any(a.name.split('.')[0] in ('numpy','scipy','action_common','cert_support','extension') for a in n.names) for n in ast.walk(tree))
    remaining=s.small_json(s.CONTRACT/'outputs/REMAINING_PREBUDGET.json')['columns'][2]
    names=['Gamma_product_image_L2_upper','Gamma_physical_image_L2_upper','finite_prime_and_local_transfer_L2_upper','infinite_prime_tail_L2_upper','finite_action_exterior_L2_upper','theta8_transfer_L2_upper']
    analytic=sum((F(remaining[k]) for k in names),F(0))+F(s.small_json(s.CONTRACT/'outputs/ANALYTIC_PREBUDGET.json')['columns'][2]['Gamma_truncation_L2_upper'])
    assert analytic==F(remaining['analytic_total_L2_upper'])
    for check in ('SOURCE_FREE_FIXTURES.json','supervisor_fixture/FIXTURE_PASS.json'):assert s.small_json(s.ROOT/'static'/check)['result' if 'supervisor' in check else 'status'].startswith('PASS')
    review=s.ROOT/'static/IMPLEMENTATION_REVIEW.md';assert review.exists()
    gate={'status':'PASS-STATIC-ENTRY','column_zero_based':2,'prior_pilot_attempts':0,'scope_of_history_check':'this Work workspace and visible saved records, not other sessions','input_bytes_and_hashes':inputs,'source_binding_count':91,'provided_path_only_replay_receipt_sha256':s.sha(s.ROOT/'portable_replay/PORTABLE_REPLAY_RECEIPT.json'),'three_saved_scalar_replays':'PASS; logs retained','frozen_admission_two_exact_replays':'PASS; logs retained','six_primitive_caches':source,'old64_node_bindings':nodes,'old_node_max_midpoint_bits':maxmid,'old_node_max_radius_bits':maxrad,'old_multiplier_sha256':s.sha(mp),'old_multiplier_records':32997,'all_18_primes_both_directions':True,'fixed_constants':{'K':8192,'KOLD':32996,'KOUT':41188,'M':131072,'nodes':3912,'precision':160,'prime_cutoff':32,'chunk_max':128,'products':7,'kernels':437},'code_sha256':sources,'review_sha256':s.sha(review),'schema_sha256':s.sha(s.CODE/'V2_DESCRIPTOR_SCHEMA.json'),'physical_source_evaluations':0,'physical_action_columns':0,'physical_kernels':0,'wall_seconds':time.monotonic()-start}
    s.save(s.ROOT/'static/STATIC_GATE.json',gate);print(json.dumps({'status':gate['status'],'wall_seconds':gate['wall_seconds'],'old_midpoint_bits':maxmid,'old_radius_bits':maxrad,'code_files':len(sources)}))
if __name__=='__main__':
    (s.ROOT/'static').mkdir(parents=True,exist_ok=True)
    if '--fixture' in sys.argv:fixture()
    else:saved_checks()
