"""CC BY-NC 4.0. REVIEW-ONLY one-checkpoint continuation; never auto-runs.

Install as code/v2_checkpoint_continue.py, phase patch as
code/v2_action_phase_repair.py. Requires a separately supplied review/approval
record. Preparing that record is NOT authorization; parent approval is external.
Original pilot/, supervisor/, marker and all inherited artifacts remain unchanged.
"""
import argparse, gc, hashlib, io, json, math, os, pathlib, resource, shutil
import signal, subprocess, sys, time, traceback, zipfile
from fractions import Fraction as F

PRIOR_WALL=25.47436677800033
PRIOR_CPU=25.447844999999997
SOFT=564.0
HARD=574.0
AS=512*1024*1024
GAMMA_HASH='bedc238709490a75279450e0dfd8462121d9cd4bd0513e61664d52896102c025'
SUPPORT_HASH='c52eb2bff3d740fee31c455ed8d166dc4e9ef104224d219b1ea04ae5298b8de7'
MANIFEST_HASH='b0086c980d08452f2aba246619342355ce3312bf4cd94cac740d3c1e3fdc247b'
PRIOR_STATUS_HASH='4a0ae20062cfcc585a6612f413ed4bf0981052045235d1cf0a636b8f07f69f14'
PRIOR_SUPERVISOR_HASH='b384ff6401b64f1ef48527446aebea35986e1d4c12e1cba0153a4fc925bb54fe'
SOURCE_INDEX_HASH='8884528f3a0985ff11fa6b38d0c7c2b469b5b795daae682c922a042a9d68ff0f'

def sha(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return h.hexdigest()
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(p,d):
    p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+'.partial')
    with t.open('w') as f:json.dump(d,f,separators=(',',':'));f.flush();os.fsync(f.fileno())
    os.replace(t,p)
def safe(root,relative):
    p=pathlib.Path(relative)
    if p.is_absolute() or '..' in p.parts:raise ValueError('relative path required')
    return root/p

def validate_authority(root,approval):
    a=load(approval)
    assert a['status']=='PASS-PHASE-REPAIR-STATIC-ENTRY'
    assert a['approved_scope']=='ONE_CHECKPOINT_CONTINUATION_J2_THROUGH_437_KERNELS'
    assert a['prior_pilot_status_sha256']==PRIOR_STATUS_HASH
    assert a['prior_supervisor_sha256']==PRIOR_SUPERVISOR_HASH
    expected={'code/v2_checkpoint_continue.py','code/v2_action_phase_repair.py'}
    assert set(a['reviewed_code_sha256'])==expected
    for rel,h in a['reviewed_code_sha256'].items():assert sha(safe(root,rel))==h
    assert sha(root/'pilot/PILOT_STATUS.json')==PRIOR_STATUS_HASH
    assert sha(root/'supervisor/SUPERVISOR_TERMINATION.json')==PRIOR_SUPERVISOR_HASH
    status=load(root/'pilot/PILOT_STATUS.json');old=load(root/'supervisor/SUPERVISOR_TERMINATION.json')
    assert status['status']=='HOLD' and status['failure_stage']=='shared-D-phase-recurrence'
    assert status['pilot_attempts']==1 and status['retries']==0
    assert status['counts']['new_Gamma_multiplier_evaluations']==8192
    assert status['counts']['complex_phase_recurrence_products']==741384
    assert old['wall_seconds']==PRIOR_WALL and old['worker_CPU_seconds']==PRIOR_CPU
    assert (root/'PILOT_SINGLE_USE.json').is_file()
    provenance=a['runtime_provenance']
    assert provenance['status']=='RECOGNIZED_INSTALL_OR_OFFICIAL_SOURCE_VERIFIED'
    assert provenance['evidence'] and provenance['runtime_hash_manifest_path']
    runtime_manifest=safe(root,provenance['runtime_hash_manifest_path'])
    assert sha(runtime_manifest)==provenance['runtime_hash_manifest_sha256']
    runtime=load(runtime_manifest)
    assert runtime['status']=='FULL_RECOGNIZED_RUNTIME_IDENTITY_VERIFIED'
    assert runtime['native_dependency_closure_verified'] is True
    assert runtime['official_source_or_recognized_install_evidence']
    assert any('.so' in rec['path'] for rec in runtime['files'])
    fixture=a['native_fixture'];fp=safe(root,fixture['record_path'])
    assert sha(fp)==fixture['record_sha256']
    test=load(fp)
    assert test['status']=='PASS_NATIVE_GENERIC_PHASE_FIXTURE'
    assert test['phase_code_sha256']==a['reviewed_code_sha256']['code/v2_action_phase_repair.py']
    assert test['support_code_sha256']==SUPPORT_HASH==sha(root/'code/v2_support.py')
    assert test['runtime_hash_manifest_sha256']==provenance['runtime_hash_manifest_sha256']
    assert test['precision_bits']==160 and test['coordinate_denominator_bits']==140
    assert test['actual_phase_cache_generated'] is False and test['source_evaluations']==0
    assert test['exact_generic_roots_checked']>=4 and test['full_error_roundtrip_pass'] is True
    return a

def verify_sources(root,s):
    # Validate the unchanged 91-source index and BOTH archive and extracted bytes.
    index=s.CONTRACT/'SOURCE_INDEX.json';assert sha(index)==SOURCE_INDEX_HASH
    records=load(index);assert len(records)==91
    def original(p):
        prefix='/workspace/shared/'
        assert p.startswith(prefix)
        return safe(root/'original',p[len(prefix):])
    # Nested archives are cached only during read-only verification, then released.
    nested={};checked=0
    for row in records:
        if 'path' in row:
            assert sha(original(row['path']))==row['sha256']
        else:
            archive=original(row['archive'])
            if 'nested_archive' in row:
                key=(str(archive),row['nested_archive'])
                if key not in nested:
                    with zipfile.ZipFile(archive) as z:nested[key]=z.read(row['nested_archive'])
                with zipfile.ZipFile(io.BytesIO(nested[key])) as z:data=z.read(row['member'])
                extracted=root/'inherited_runtime/A_action'/row['member']
            else:
                with zipfile.ZipFile(archive) as z:data=z.read(row['member'])
                extracted=root/'inherited_runtime/A'/row['member']
            assert hashlib.sha256(data).hexdigest()==row['sha256']
            assert sha(extracted)==row['sha256']
            del data
        checked+=1;s.guard()
    del nested;gc.collect();return checked

def worker(root,approval):
    assert 'V2_CONTINUATION_START' in os.environ
    marker=load(root/'CONTINUATION_SINGLE_USE.json')
    assert marker['continuation']==1 and marker['no_retry'] is True
    assert marker['approval_record_sha256']==sha(approval)
    assert marker['prior_status_sha256']==PRIOR_STATUS_HASH
    assert marker['prior_marker_sha256']==sha(root/'PILOT_SINGLE_USE.json')
    assert marker['launcher_pid']==os.getppid()
    assert sha(root/'code/v2_support.py')==SUPPORT_HASH
    sys.path.insert(0,str(root/'code'));import v2_support as s
    assert s.ROOT.resolve()==root.resolve()
    out=root/'continuation_01/pilot';out.mkdir(parents=True,exist_ok=False)
    s.OUT=out;s.START=float(os.environ['V2_CONTINUATION_START']);s.COUNTS={}
    def guard():
        if time.monotonic()-s.START>=SOFT:raise RuntimeError('aggregate continuation soft wall stop')
        if time.process_time()>=563:raise RuntimeError('conservative continuation CPU soft stop')
        if s.proc_memory().get('VmRSS_KiB',0)>=500*1024:raise MemoryError('500 MiB RSS stop')
    s.guard=guard
    def stop(sig,frame):raise RuntimeError('supervisor continuation stop')
    signal.signal(signal.SIGTERM,stop)
    try:
        admission=validate_authority(root,approval)
        assert resource.getrlimit(resource.RLIMIT_AS)==(AS,AS)
        cpu=resource.getrlimit(resource.RLIMIT_CPU);assert 0<cpu[0]==cpu[1]<=573
        assert sha(root/'OUTPUT_FILE_MANIFEST.json')==MANIFEST_HASH
        manifest=load(root/'OUTPUT_FILE_MANIFEST.json')
        for rec in manifest['files']:
            p=safe(root,rec['path']);assert p.stat().st_size==rec['bytes'] and sha(p)==rec['sha256'];guard()
        verified=verify_sources(root,s)
        # Copy accepted data to distinct outputs, retaining all original bytes.
        (out/'cache').mkdir()
        for p in (root/'pilot/cache').iterdir():
            if p.is_file():shutil.copyfile(p,out/'cache'/p.name)
        for name in ('OLD_ANALYTIC_TRANSFER.json','J2_FRAME_CERTIFICATE.json'):
            shutil.copyfile(root/'pilot'/name,out/name)
        for p in (out/'cache').iterdir():assert sha(p)==sha(root/'pilot/cache'/p.name)
        assert sha(out/'cache/GAMMA_EXTENSION.bin')==GAMMA_HASH
        # Import ONLY the fully verified runtime tree, whether preinstalled or
        # independently authenticated against an official artifact. File hashes
        # alone do not establish provenance; the preflight approval binds both.
        import importlib.util
        provenance=admission['runtime_provenance']
        runtime=load(safe(root,provenance['runtime_hash_manifest_path']))
        runtime_root=pathlib.Path(runtime['runtime_root']).resolve()
        expected=set()
        for rec in runtime['files']:
            p=safe(runtime_root,rec['path']);assert p.stat().st_size==rec['bytes'] and sha(p)==rec['sha256'];expected.add(rec['path']);guard()
        observed=set()
        for tree in runtime['tree_roots']:
            for p in safe(runtime_root,tree).rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':observed.add(str(p.relative_to(runtime_root)))
        assert observed==expected,'runtime tree differs from complete reviewed identity'
        sys.path.insert(0,str(runtime_root))
        assert 'flint' not in sys.modules
        spec=importlib.util.find_spec('flint');assert spec and spec.origin
        assert pathlib.Path(spec.origin).resolve()==safe(runtime_root,runtime['flint_module_relative_path']).resolve()
        import flint
        from flint import arb,acb,acb_poly,arb_mat,fmpq,ctx
        ctx.prec=160;ctx.threads=1
        for key,value in dict(arb=arb,acb=acb,acb_poly=acb_poly,arb_mat=arb_mat,fmpq=fmpq,ctx=ctx).items():setattr(s,key,value)
        assert flint.__version__=='0.9.0' and flint.__FLINT_VERSION__=='3.6.0'
        assert s.ctx.prec==160 and s.ctx.threads==1
        import v2_action_phase_repair as action, v2_nodes as nodes
        action.get_backend();nodes.get_backend()
        s.phase('checkpoint-inputs-and-reused-caches-verified')
        fixed=s.load_fixed();transfer=load(out/'OLD_ANALYTIC_TRANSFER.json')
        poles=[];AI=[]
        for i,h in enumerate(transfer['old_action_hashes']):
            p=s.action_path(i);assert sha(p)==h
            poles.append(F(int(s.metadata(p)['pole_numerator']),1<<100))
            AI.append(2*sum((F(97,96)*abs(F(fixed['T'][3*j][i],1<<30))+abs(F(fixed['T'][3*j+1][i],1<<30))/4+abs(F(fixed['T'][3*j+2][i],1<<30))/48 for j in range(124)),F(0)))
        assert len(poles)==64
        facts={'poles':poles,'AI':AI,'eold':list(map(F,transfer['errors'])),'epsilon':F(transfer['epsilon_j2']),'lold':list(map(F,transfer['old_bracket_L'])),'old_hashes':transfer['old_action_hashes']}
        assert facts['epsilon']==sum((abs(F(fixed['Y'][i][2],1<<40))*facts['eold'][i] for i in range(64)),F(0))
        frame=load(out/'J2_FRAME_CERTIFICATE.json');frame_nums=frame['dyadic_numerators_bits100']
        assert len(frame_nums)==len(frame['moment_records_bits140'])==372
        errors=[F(abs(int(rec[0])-int(n)*(1<<40))+int(rec[1]),1<<140) for rec,n in zip(frame['moment_records_bits140'],frame_nums)]
        frame_error=2048*sum(errors,F(0));assert str(frame_error)==frame['2048_sum_error'] and frame_error<=F(1,1<<30)
        md=load(out/'cache/GAMMA_EXTENSION.bin.json');assert md['sha256']==GAMMA_HASH and md['count']==8192 and md['bits']==140
        original=s.OLD/'outputs/GAMMA_MULTIPLIERS.json';assert sha(original)==md['bindings']['original_multiplier_sha256']
        mult=[s.restore(v,140) for v in s.iter_array(original,'values')]
        assert len(mult)==32997 and mult[0].is_zero()
        ext=list(s.packed_read(out/'cache/GAMMA_EXTENSION.bin',140));assert len(ext)==8192
        assert all(v.is_finite() and v.lower()>0 and v.rad()<s.aa(F(1,1<<100)) for v in ext)
        mult.extend(ext);del ext
        save(out/'CHECKPOINT_REUSE.json',{'prior_status_sha256':PRIOR_STATUS_HASH,'prior_wall_seconds':PRIOR_WALL,'prior_CPU_seconds':PRIOR_CPU,'Gamma_sha256':GAMMA_HASH,'Gamma_evaluations_this_continuation':0,'frame_recomputed':False,'source_bindings_checked':verified,'scope':'j=2 only through 437 kernels; no consumer'})
        D,mult,terms=action.shared_D_phase(mult,original,md)
        desc,cert=action.produce(fixed,D,mult,frame_nums,frame_error)
        del D,mult,frame_nums;gc.collect();s.phase('producer-lifetimes-ended')
        nodes.polynomial_nodes(desc);nodes.integrate(fixed,facts,desc,cert,terms)
        assert s.COUNTS.get('new_Gamma_multiplier_evaluations',0)==0
        assert s.COUNTS.get('new_H64_residual_action_columns',0)==1
        assert s.COUNTS.get('polynomial_products',0)==7
        assert s.COUNTS.get('new_polynomial_evaluation_DFT_calls',0)==1
        assert s.COUNTS.get('physical_Gram_scalar_multiply_adds',0)==1709544
        # Scope the original integer-only checker to the new result directory.
        # Its original output destination is intercepted so old evidence cannot
        # be overwritten. This is saved arithmetic, not a second numerical run.
        import verify_saved_v2
        original_save=s.save
        def continuation_check_save(path,obj):
            assert pathlib.Path(path)==root/'INDEPENDENT_SAVED_VERIFICATION.json'
            original_save(root/'continuation_01/INDEPENDENT_SAVED_VERIFICATION.json',obj)
        try:
            s.save=continuation_check_save
            verify_saved_v2.main()
        finally:s.save=original_save
        checked=load(root/'continuation_01/INDEPENDENT_SAVED_VERIFICATION.json')
        assert checked['status']=='PASS-INDEPENDENT-SAVED-ARITHMETIC' and not checked['missing']
        guard()
        save(out/'CONTINUATION_STATUS.json',{'status':'PASS-CONTINUATION-SAVED-CHECK-PENDING-EXTERNAL-REVIEW','counts':s.COUNTS,'column_zero_based':2,'kernels':437,'other_columns':0,'consumers':0,'prior_attempts':1,'continuations':1,'original_HOLD_preserved':True})
    except BaseException as exc:
        save(out/'CONTINUATION_STATUS.json',{'status':'HOLD','phase':s.PHASE,'exception_type':type(exc).__name__,'reason':str(exc),'traceback':traceback.format_exc(),'counts':s.COUNTS,'prior_attempts':1,'continuations':1,'no_automatic_retry':True})
        raise

def supervisor(root,approval):
    started=time.monotonic();cpu_started=time.process_time()
    validate_authority(root,approval)
    out=root/'continuation_01';out.mkdir(exist_ok=False)
    with (root/'CONTINUATION_SINGLE_USE.json').open('x') as f:
        json.dump({'launcher_pid':os.getpid(),'prior_marker_sha256':sha(root/'PILOT_SINGLE_USE.json'),'prior_status_sha256':PRIOR_STATUS_HASH,'approval_record_sha256':sha(approval),'continuation':1,'no_retry':True,'prior_wall':PRIOR_WALL,'prior_CPU':PRIOR_CPU,'wall_soft':SOFT,'wall_hard':HARD,'AS_bytes':AS},f)
    own_before=time.process_time()-cpu_started
    child_cpu_cap=math.floor(HARD-own_before-1.0)
    assert 0<child_cpu_cap<=573
    def limits():
        resource.setrlimit(resource.RLIMIT_AS,(AS,AS));resource.setrlimit(resource.RLIMIT_CPU,(child_cpu_cap,child_cpu_cap));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
        save(out/'PROCESS_ID_MAP.json',{'namespace_PID':os.getpid(),'procfs_PID':int(os.readlink('/proc/self'))})
    events=[];term=False;killed=False;peak={};ticks=os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    command=[sys.executable,str(pathlib.Path(__file__).resolve()),'--root',str(root),'--approval-record',str(approval),'--worker']
    with (out/'worker.stdout.log').open('xb') as stdout,(out/'worker.stderr.log').open('xb') as stderr:
        p=subprocess.Popen(command,stdout=stdout,stderr=stderr,start_new_session=True,preexec_fn=limits,env={**os.environ,'V2_CONTINUATION_START':repr(started),'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
        pidmap=load(out/'PROCESS_ID_MAP.json');assert pidmap['namespace_PID']==p.pid
        while True:
            elapsed=time.monotonic()-started;own_cpu=time.process_time()-cpu_started;child_cpu=0.0
            try:
                stat=pathlib.Path(f"/proc/{pidmap['procfs_PID']}/stat").read_text().rsplit(')',1)[1].split();child_cpu=(int(stat[11])+int(stat[12]))/ticks
                for line in pathlib.Path(f"/proc/{pidmap['procfs_PID']}/status").read_text().splitlines():
                    k,_,v=line.partition(':')
                    if k in ('VmRSS','VmHWM','VmSize','VmPeak'):peak[k+'_KiB']=max(peak.get(k+'_KiB',0),int(v.split()[0]))
            except (FileNotFoundError,ProcessLookupError):pass
            total_cpu=own_cpu+child_cpu
            if not term and (elapsed>=SOFT or total_cpu>=SOFT):
                term=True
                try:os.killpg(p.pid,signal.SIGTERM);events.append({'signal':'SIGTERM','wall':elapsed,'CPU':total_cpu})
                except ProcessLookupError:pass
            if not killed and (elapsed>=HARD or total_cpu>=HARD):
                killed=True
                try:os.killpg(p.pid,signal.SIGKILL);events.append({'signal':'SIGKILL','wall':elapsed,'CPU':total_cpu})
                except ProcessLookupError:pass
            pid,status,usage=os.wait4(p.pid,os.WNOHANG)
            if pid:p.returncode=os.waitstatus_to_exitcode(status);break
            time.sleep(min(0.05,max(0.001,(SOFT if not term else HARD)-elapsed)))
    wall=time.monotonic()-started;worker_cpu=usage.ru_utime+usage.ru_stime;supervisor_cpu=time.process_time()-cpu_started
    budget_pass=(PRIOR_WALL+wall<=600 and PRIOR_CPU+worker_cpu+supervisor_cpu<=600)
    save(out/'SUPERVISOR_TERMINATION.json',{'aggregate_budget_gate_pass':budget_pass,'exit_code':p.returncode,'prior_wall_seconds':PRIOR_WALL,'prior_CPU_seconds':PRIOR_CPU,'continuation_wall_seconds':wall,'continuation_worker_CPU_seconds':worker_cpu,'continuation_supervisor_CPU_seconds':supervisor_cpu,'aggregate_wall_seconds':PRIOR_WALL+wall,'aggregate_CPU_seconds':PRIOR_CPU+worker_cpu+supervisor_cpu,'wall_soft_seconds':SOFT,'wall_hard_seconds':HARD,'child_RLIMIT_CPU_seconds':child_cpu_cap,'aggregate_CPU_monitored':True,'RLIMIT_AS_bytes':AS,'wait4_peak_RSS_KiB':usage.ru_maxrss,'sampled_peak_memory':peak,'events':events,'OS_granularity':'50ms sampling; signal scheduling/accounting may overshoot; no success implied by cap','original_HOLD_preserved':True,'no_retry':True})
    # A scheduling/cleanup overrun is a HOLD, never a successful certificate.
    final_status='PASS-PENDING-EXTERNAL-REVIEW' if p.returncode==0 and budget_pass else 'HOLD'
    save(out/'CONTINUATION_FINAL_STATUS.json',{'status':final_status,'worker_exit_code':p.returncode,'aggregate_budget_gate_pass':budget_pass,'aggregate_wall_seconds':PRIOR_WALL+wall,'aggregate_CPU_seconds':PRIOR_CPU+worker_cpu+supervisor_cpu,'reason':None if final_status.startswith('PASS') else ('aggregate600-second budget exceeded' if not budget_pass else 'worker did not complete'),'original_HOLD_preserved':True,'automatic_retry':False})
    return p.returncode if budget_pass else 2

def main():
    a=argparse.ArgumentParser();a.add_argument('--root',required=True);a.add_argument('--approval-record',required=True);a.add_argument('--worker',action='store_true');v=a.parse_args()
    root=pathlib.Path(v.root).resolve();approval=pathlib.Path(v.approval_record).resolve()
    if v.worker:worker(root,approval)
    else:raise SystemExit(supervisor(root,approval))
if __name__=='__main__':main()
