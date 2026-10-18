"""Trusted host boundary: spawn-to-reap monotonic witness, then immutable audit.

STATIC PREPARATION ONLY. Not imported or exercised in preparation.
The candidate observer/controller/worker serialize all results before exiting.
Only read-only hash checks and this external receipt follow their actual exit.
"""
import hashlib
import json
import os
from pathlib import Path
import resource
import select
import signal
import sys
import time
import types

NS=1_000_000_000
LIMITS={'wall_seconds':60,'tree_cpu_seconds':60,'worker_as_bytes':402653184,
        'worker_rss_kib':327680,'threads':1,'scientific_workers':1,'poll_seconds':0.01}


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def decode(data):
    def unique(items):
        out={}
        for k,v in items: need(k not in out,'duplicate JSON key'); out[k]=v
        return out
    return json.loads(data,object_pairs_hook=unique)


def read(p): return decode(Path(p).read_bytes())


def write_audit(p,value):
    data=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
    with Path(p).open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    need(Path(p).read_bytes()==data,'external audit byte readback')
    fd=os.open(Path(p).parent,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)


def load_lifecycle(plan):
    p=Path(plan['code_root'])/'shift_lifecycle.py'; data=p.read_bytes()
    need(hashlib.sha256(data).hexdigest()==plan['code_sha256'][p.name],'host lifecycle source binding')
    module=types.ModuleType('bound_host_lifecycle'); module.__file__=str(p)
    exec(compile(data,str(p),'exec',dont_inherit=True,optimize=0),module.__dict__)
    need(module.PROTOCOL==plan['tree_protocol'],'host lifecycle protocol')
    return module


def fixture_release_gate(plan,plan_hash):
    release=read(plan['execution_release'])
    need(release['launch_id']==plan['launch_id'] and release['plan_sha256']==plan_hash and
         release['independent_static_review']=='GO' and release['fixture_tool_exit_code']==0 and
         release['scientific_dispatches_authorized']==1 and release['automatic_retry'] is False,
         'review/fixture/re-execution release absent or mismatched')
    contract=Path(plan['fixture_contract']); result_path=Path(plan['fixture_result'])
    need(sha(contract)==plan['fixture_contract_sha256'],'fixture contract bytes')
    need(sha(result_path)==release['fixture_result_sha256'],'fixture result bytes')
    result=read(result_path); fixture_contract=read(contract)
    need(result['status']=='FIXTURE-PASS' and result['contract_sha256']==plan['fixture_contract_sha256'] and
         result['lifecycle_sha256']==plan['code_sha256']['shift_lifecycle.py'] and
         result['fixture_source_sha256']==fixture_contract['fixture_source_sha256'] and
         result['launch_id']==fixture_contract['launch_id'] and result['cases']==fixture_contract['cases'] and
         result['bundles_executed']==1 and result['automatic_retry'] is False and
         result['closed_tree'] is True and result['scientific_imports']==0 and
         0<result['wall_ns']==result['tree_cpu_capacity_upper_ns']<10_000_000_000 and
         result['CPU_affinity']==[plan['cpu_affinity']],'fixture result did not satisfy frozen contract')


def main():
    need(len(sys.argv)==6 and sys.argv[1]=='--execute-once','explicit host command required')
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and not sys.flags.optimize,
         'host requires -I -S -B without optimization')
    need(not any(os.environ.get(k) for k in ('LD_PRELOAD','LD_LIBRARY_PATH','PYTHONPATH')),'host injected path')
    plan_path=Path(sys.argv[2]).resolve(); plan_hash=sys.argv[3]
    command_path=Path(sys.argv[4]).resolve(); command_hash=sys.argv[5]
    plan_bytes=plan_path.read_bytes(); command_bytes=command_path.read_bytes()
    need(hashlib.sha256(plan_bytes).hexdigest()==plan_hash,'host plan bytes')
    need(hashlib.sha256(command_bytes).hexdigest()==command_hash,'host command bytes')
    plan=decode(plan_bytes); command=decode(command_bytes); argv=command['argv']
    need(plan['limits']==LIMITS and plan['scope']=='SHIFT372_H2_DELTA_STAR_FIXED_C_ONCE_V1','unchanged contract')
    need(plan['host_terminal_protocol']=='TRUSTED_HOST_MONOTONIC_SPAWN_REAP_V1','host boundary protocol')
    need(Path(__file__).resolve()==Path(plan['host_wrapper']) and sha(__file__)==plan['host_wrapper_sha256'],
         'reviewed host source binding')
    need(Path(sys.executable).resolve()==Path(plan['python_executable']).resolve() and
         sha(Path(sys.executable).resolve())==plan['python_sha256'],'host interpreter binding')
    need(len(argv)==11 and argv[0]==plan['python_executable'] and argv[1:5]==['-I','-S','-B','-c'] and
         hashlib.sha256(argv[5].encode()).hexdigest()==plan['observer_trampoline_sha256'] and
         argv[6]==str(Path(plan['code_root'])/'source_bootstrap.py') and
         argv[7]==plan['code_sha256']['source_bootstrap.py'] and argv[8]=='observer' and
         argv[9]==str(plan_path) and argv[10]==plan_hash,'exact observer argv')
    argv_hash=hashlib.sha256(json.dumps(argv,separators=(',',':')).encode()).hexdigest()
    audit=Path(plan['host_audit_root']); attempt=Path(plan['attempt_root']); cpu=plan['cpu_affinity']
    need(not audit.exists() and not attempt.exists(),'one-use host/attempt mark already present')
    # Conservative host reservation prevents retry even if the observer dies
    # between receiving BEGIN and its first atomic directory creation.
    audit.mkdir(mode=0o700,exist_ok=False)
    write_audit(audit/'HOST_ATTEMPT_RESERVED.json',{'plan_sha256':plan_hash,
                'observer_command_file_sha256':command_hash,'observer_argv_sha256':argv_hash,
                'launch_id':plan['launch_id'],'automatic_retry':False})
    pid=None; pidfd=None; reaped=False; terminal_status=None; usage=None; start_ticks=None
    child=None; life=None; start_ns=None; deadline=None
    def kill_observer():
        if pidfd is not None:
            try: signal.pidfd_send_signal(pidfd,signal.SIGKILL)
            except ProcessLookupError: pass
        elif pid is not None and not reaped:
            try: os.kill(pid,signal.SIGKILL)
            except ProcessLookupError: pass
    def alarm(signum,frame):
        kill_observer(); raise TimeoutError('host60second outer bracket expired')
    signal.signal(signal.SIGALRM,alarm)
    try:
        fixture_release_gate(plan,plan_hash)
        life=load_lifecycle(plan)
        need(cpu in os.sched_getaffinity(0),'host reviewed CPU unavailable'); os.sched_setaffinity(0,{cpu})
        life.prepare_parent(cpu,subreaper=True)
        stdin_read,stdin_write=os.pipe()
        outfd=os.open(audit/'OBSERVER_STDOUT.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_SYNC,0o600)
        errfd=os.open(audit/'OBSERVER_STDERR.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_SYNC,0o600)
        # TRUSTED OUTER START precedes the first fork and every child handshake.
        start_ns=time.monotonic_ns(); deadline=start_ns+60*NS
        signal.setitimer(signal.ITIMER_REAL,max(0.000001,(deadline-time.monotonic_ns())/NS))
        owner=os.getpid()
        def observer_exec():
            os.close(stdin_write)
            os.dup2(stdin_read,0); os.close(stdin_read)
            os.dup2(outfd,1); os.dup2(errfd,2); os.close(outfd); os.close(errfd)
            os.execve(plan['python_executable'],argv,dict(os.environ))
        child=life.fork_one(cpu,deadline,observer_exec)
        pid=child.pid; pidfd=child.fd; start_ticks=child.start
        os.close(stdin_read); os.close(outfd); os.close(errfd)
        child.release()
        sent=False
        while True:
            need(time.monotonic_ns()<deadline,'host outer deadline')
            need(os.sched_getaffinity(0)=={cpu} and len(list(Path('/proc/self/task').iterdir()))==1,
                 'host shared CPU/thread changed')
            life.require_sealed(os.getpid())
            done,st,ru=child.poll()
            if done:
                reaped=True; terminal_status=st; usage=ru
                break
            if not sent:
                output=(audit/'OBSERVER_STDOUT.log').read_bytes()
                need(len(output)<=65536,'unexpected pre-BEGIN output volume')
                if b'\n' in output:
                    ready=decode(output.split(b'\n',1)[0])
                    need(ready=={'status':'READY-NO-SCIENCE','plan_sha256':plan_hash,
                                 'required_stdin':'BEGIN '+plan_hash},'observer READY binding')
                    token=('BEGIN '+plan_hash+'\n').encode()
                    need(os.write(stdin_write,token)==len(token),'single BEGIN transport')
                    os.close(stdin_write); sent=True
            child.sample()
            select.select([pidfd],[],[],min(0.01,max(0,(deadline-time.monotonic_ns())/NS)))
        need(sent and os.waitstatus_to_exitcode(terminal_status)==0,'observer incomplete or nonzero exit')
        life.assert_no_children()
        # Close the bracket only after both actual reap and final ECHILD.
        end_ns=time.monotonic_ns()
        need(0<end_ns-start_ns<60*NS,'whole spawn-to-reap wall and single-CPU capacity gates')
        # Only after all candidate serialization and actual exit is observed.
        # The following operations are read-only attestation, not science.
        signal.setitimer(signal.ITIMER_REAL,0)
        manifest_path=attempt/'FINAL_ARTIFACT_MANIFEST.json'
        manifest_bytes=manifest_path.read_bytes(); manifest_hash=hashlib.sha256(manifest_bytes).hexdigest()
        manifest=decode(manifest_bytes)
        need(manifest['format']=='SHIFT372_FINAL_BYTES_V1' and manifest['plan_sha256']==plan_hash and
             manifest['status']=='EXTERNAL-TERMINAL-WITNESS-PENDING','final manifest binding')
        seen=set()
        for item in manifest['files']:
            rel=Path(item['path']); need(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen,
                                       'manifest path/duplicate'); seen.add(str(rel))
            p=attempt/rel; need(not p.is_symlink() and p.resolve().is_relative_to(attempt.resolve()),'artifact path escape')
            b=p.read_bytes(); need(len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],
                                  'immutable final artifact '+str(rel))
        actual=set()
        for p in attempt.rglob('*'):
            need(not p.is_symlink(),'final tree symlink')
            if p.is_file(): actual.add(str(p.relative_to(attempt)))
        need(actual==seen|{'FINAL_ARTIFACT_MANIFEST.json'},'final artifact tree changed')
        epoch=read(attempt/'OBSERVER_EPOCH.json'); observer=read(attempt/'OBSERVER_RECEIPT.json')
        status=read(attempt/'OBSERVER_FINAL_STATUS.json')
        need(epoch['observer_pid']==pid and epoch['plan_sha256']==plan_hash and
             epoch['consumed_before_source_admission'] is True and
             start_ns<=epoch['t0_ns']<end_ns,'host/observer epoch identity')
        need(observer['plan_sha256']==plan_hash and observer['controller_exit_code']==0 and
             observer['worker_exit_observed'] is True and observer['no_unreaped_descendants'] is True and
             observer['tree_protocol']==life.PROTOCOL and observer['observer_NPROC_soft_hard']==[0,0] and
             observer['CPU_affinity']==[cpu] and observer['threads_per_process']==1 and
             observer['scientific_workers']==1,'closed candidate tree receipt')
        need(status['plan_sha256']==plan_hash and status['resource_acceptance'] is False and
             status['observer_receipt_sha256']==sha(attempt/'OBSERVER_RECEIPT.json'),'provisional observer status')
        lines=(audit/'OBSERVER_STDOUT.log').read_bytes().splitlines()
        final=decode(lines[-1]); need(final['status']=='EXTERNAL-TERMINAL-WITNESS-PENDING' and
             final['plan_sha256']==plan_hash and final['final_manifest_sha256']==manifest_hash,'terminal stdout binding')
        need(sha(plan_path)==plan_hash and sha(command_path)==command_hash,'external command/plan unchanged')
        need(sha(manifest_path)==manifest_hash,'final manifest unchanged during audit')
        receipt={'status':'EXTERNAL-RESOURCE-WITNESS-VERIFIED','resource_acceptance':True,
                 'plan_sha256':plan_hash,'observer_command_file_sha256':command_hash,
                 'observer_argv_sha256':argv_hash,'host_source_sha256':plan['host_wrapper_sha256'],
                 'launch_id':plan['launch_id'],'observer_pid':pid,'observer_start_ticks':start_ticks,
                 'observer_exit_code':0,'actual_wait4_completed':True,'no_remaining_descendants':True,
                 'tree_protocol':life.PROTOCOL,'closure_evidence':'wait4(-1,WNOHANG|__WALL) -> ECHILD',
                 'registered_observer':child.record(),'host_NPROC_soft_hard':[0,0],
                 'monotonic_start_ns':start_ns,'monotonic_end_ns':end_ns,'complete_wall_ns':end_ns-start_ns,
                 'tree_cpu_capacity_upper_ns':end_ns-start_ns,'CPU_affinity':[cpu],
                 'cpu_scope':'All candidate scientific/controller/observer CPU plus host control during the bracket; no usage sums.',
                 'wait4_diagnostic_only':{'user_seconds':usage.ru_utime,'system_seconds':usage.ru_stime,'maxrss_kib':usage.ru_maxrss},
                 'final_artifact_manifest_sha256':manifest_hash,'final_artifacts_readback_verified':len(seen),
                 'host_stdout_sha256':sha(audit/'OBSERVER_STDOUT.log'),'host_stderr_sha256':sha(audit/'OBSERVER_STDERR.log'),
                 'post_exit_scope':'Read-only immutable artifact/identity audit and this external receipt; no candidate call or numeric replay.',
                 'trust_boundary':'Reviewed host wrapper, OS monotonic clock and wait/reap; final tool exit confirms receipt-writer completion.',
                 'automatic_retry':False,'RH_PROOF':'NOT-OBTAINED'}
        write_audit(audit/'EXTERNAL_TERMINAL_WITNESS.json',receipt)
        print(json.dumps({'status':receipt['status'],'plan_sha256':plan_hash,
                          'external_receipt_sha256':sha(audit/'EXTERNAL_TERMINAL_WITNESS.json')}),flush=True)
        return 0
    except BaseException as exc:
        kill_observer()
        closure={'closed':False,'reason':'lifecycle setup or deadline unavailable'}
        if life is not None and deadline is not None:
            try: closure=life.cleanup([child],deadline)
            except BaseException as cleanup_error: closure={'closed':False,'reason':str(cleanup_error)}
        if child is not None: reaped=child.reaped
        signal.setitimer(signal.ITIMER_REAL,0)
        # A failure may leave termination unobserved. Never convert it to PASS.
        try: write_audit(audit/'EXTERNAL_TERMINAL_HOLD.json',{'status':'HOLD','resource_acceptance':False,
                   'reason':str(exc),'exception_type':type(exc).__name__,'plan_sha256':plan_hash,
                   'observer_pid':pid,'actual_wait4_completed':reaped,'automatic_retry':False,
                   'cleanup':closure,
                   'termination_outcome':'reaped' if reaped else 'uncertain',
                   'resource_bracket_started':start_ns is not None,'RH_PROOF':'NOT-OBTAINED'})
        except BaseException: pass
        return 2


if __name__=='__main__': raise SystemExit(main())
