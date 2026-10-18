"""One fixed, nonmathematical lifecycle bundle. NOT RUN during preparation.

The trusted outer fixture host creates three held case processes before sealing
itself. This finite factory is a fixture-only exception: each case then makes
exactly one child and seals immediately, as production parents do. No retries,
theta imports, native scientific runtime, numerical inputs, or Gram values.
"""
import errno
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
AS=67_108_864
CASES=('normal_and_spawn_denied','early_exit_before_binding','controller_death_cleanup')


def need(ok,label):
    if not ok: raise RuntimeError(label)


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    def unique(items):
        out={}
        for k,v in items: need(k not in out,'duplicate JSON key'); out[k]=v
        return out
    return json.loads(Path(p).read_bytes(),object_pairs_hook=unique)


def save(p,value):
    b=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
    with Path(p).open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    need(Path(p).read_bytes()==b,'fixture audit byte readback')
    fd=os.open(Path(p).parent,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)


def send(fd,value):
    b=json.dumps(value,separators=(',',':')).encode()+b'\n'
    need(len(b)<=4096 and os.write(fd,b)==len(b),'fixture pipe packet')


def forbid_science(event,args):
    if event=='import':
        name=args[0]
        need(not (name.startswith(('flint','numpy','scipy','theta','shift_'))),
             'scientific/local module import forbidden in fixture')


def main():
    need(len(sys.argv)==4 and sys.argv[1]=='--fixture-once','explicit fixture command required')
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and not sys.flags.optimize,
         'fixture source-only flags')
    need(not any(os.environ.get(k) for k in ('LD_PRELOAD','LD_LIBRARY_PATH','PYTHONPATH')),'injected path')
    contract_path=Path(sys.argv[2]); expected=sys.argv[3]
    need(sha(contract_path)==expected,'fixture contract bytes'); contract=read(contract_path)
    need(contract['cases']==list(CASES) and contract['limits']=={
         'wall_seconds':10,'tree_cpu_seconds':10,'worker_as_bytes':AS,'cpu_affinity':0,
         'bundles':1,'automatic_retry':False},'fixture budget/scope changed')
    need(sha(__file__)==contract['fixture_source_sha256'],'fixture source binding')
    need(Path(sys.executable).resolve()==Path(contract['python_executable']).resolve() and
         sha(Path(sys.executable).resolve())==contract['python_sha256'],'fixture interpreter binding')
    root=Path(contract['attempt_root']); need(not root.exists(),'fixture already consumed')
    # Reserve before capability checks: an unsupported interface consumes this
    # one bundle too. No error path removes this directory.
    root.mkdir(mode=0o700,exist_ok=False)
    save(root/'FIXTURE_RESERVED.json',{'launch_id':contract['launch_id'],'contract_sha256':expected,
                                     'automatic_retry':False})
    children=[]; remote_fd=None; life=None; deadline=None; start_ns=None
    def kill_all():
        if remote_fd is not None:
            try: signal.pidfd_send_signal(remote_fd,signal.SIGKILL)
            except ProcessLookupError: pass
        for child in children: child.kill()
    def expired(signum,frame):
        kill_all(); os._exit(124)
    # One deadline also charges fixture source admission and primitive setup.
    # It is never restarted for a case or for failure cleanup.
    start_ns=time.monotonic_ns(); deadline=start_ns+10*NS
    signal.signal(signal.SIGALRM,expired); signal.setitimer(signal.ITIMER_REAL,10)
    try:
        release=read(contract['static_review_release'])
        need(release=={'contract_sha256':expected,'independent_static_review':'GO',
                       'fixture_bundles_authorized':1,'automatic_retry':False},'static review release missing')
        p=Path(contract['lifecycle_source']); b=p.read_bytes()
        need(hashlib.sha256(b).hexdigest()==contract['lifecycle_sha256'],'production lifecycle bytes')
        life=types.ModuleType('bound_fixture_lifecycle'); life.__file__=str(p)
        exec(compile(b,str(p),'exec',dont_inherit=True,optimize=0),life.__dict__)
        need(life.PROTOCOL==contract['tree_protocol'],'lifecycle protocol')
        sys.addaudithook(forbid_science)
        cpu=contract['limits']['cpu_affinity']; need(cpu in os.sched_getaffinity(0),'fixture CPU unavailable')
        os.sched_setaffinity(0,{cpu}); resource.setrlimit(resource.RLIMIT_AS,(AS,AS))
        resource.setrlimit(resource.RLIMIT_CORE,(0,0))
        life.prepare_parent(cpu,subreaper=True)
        # All primitive setup, case births, handshakes, assertions,
        # serialization, cleanup and reaping use the already-running interval.
        request_r,request_w=os.pipe(); ack_r,ack_w=os.pipe()
        def guard():
            need(time.monotonic_ns()<deadline,'fixture common10second deadline')
            need(os.sched_getaffinity(0)=={cpu} and len(list(Path('/proc/self/task').iterdir()))==1,
                 'fixture CPU/thread changed')
        def wait_child(child,exitcode):
            while not child.reaped:
                guard()
                if child.poll()[0]: break
                child.sample(); select.select([child.fd],[],[],0.001)
            need(os.waitstatus_to_exitcode(child.status)==exitcode,'unexpected fixture child status')
        def normal_case():
            life.prepare_parent(cpu)
            def leaf():
                life.require_sealed(os.getpid())
                need(resource.getrlimit(resource.RLIMIT_AS)==(AS,AS),'fixture leaf AS')
                # No Python process-denial audit hook here: EAGAIN must be the
                # kernel NPROC result, not an exception synthesized by a hook.
                try: unexpected=os.fork()
                except OSError as exc: need(exc.errno==errno.EAGAIN,'spawn denial was not NPROC EAGAIN')
                else:
                    if unexpected==0: os._exit(98)
                    os.kill(unexpected,signal.SIGKILL); os.waitpid(unexpected,0)
                    raise RuntimeError('extra spawn succeeded; fixture failure')
                life.assert_no_children()
                save(root/'NORMAL_LEAF.json',{'spawn_errno':errno.EAGAIN,'AS':AS,'NPROC':[0,0]})
                return 0
            child=life.fork_one(cpu,deadline,leaf,{'as_bytes':AS,'cpu_seconds':10})
            child.release(); wait_child(child,0); life.assert_no_children(); life.require_sealed(os.getpid())
            save(root/'NORMAL_CASE.json',{'status':'EXPECTED','registered_child':child.record(),'exit_code':0})
            return 0
        def early_case():
            life.prepare_parent(cpu)
            # Deliberate fault case: child exits as its first operation, before
            # READY or pidfd binding. WNOWAIT retains its PID as our zombie.
            pid=os.fork()
            if pid==0: os._exit(23)
            child=life.Child(pid,cpu,os.getpid()); life.seal()
            seen=os.waitid(os.P_PID,pid,os.WEXITED|os.WNOWAIT)
            need(seen.si_pid==pid and seen.si_status==23,'early exit was not observed')
            row=child.bind(); need(row['state']=='Z' and life.ready(child.fd),'unreaped zombie binding')
            rd,wr=os.pipe(); child.release_fd=wr
            try: child.release()
            except RuntimeError: rejected=True
            else: rejected=False
            os.close(rd); os.close(wr); child.release_fd=None
            need(rejected,'early child incorrectly released')
            wait_child(child,23); life.assert_no_children()
            save(root/'EARLY_CASE.json',{'status':'EXPECTED-HOLD','registered_child':child.record(),
                 'prebinding_zombie_retained':True,'release_rejected':True,'exit_code':23})
            return 0
        def death_case():
            life.prepare_parent(cpu)
            alive_r,alive_w=os.pipe()
            def leaf():
                os.close(alive_r); life.require_sealed(os.getpid())
                need(resource.getrlimit(resource.RLIMIT_AS)==(AS,AS),'death leaf AS')
                need(os.write(alive_w,b'ALIVE\n')==6,'leaf alive handshake'); os.close(alive_w)
                signal.pause()
                raise RuntimeError('death leaf unexpectedly continued')
            child=life.fork_one(cpu,deadline,leaf,{'as_bytes':AS,'cpu_seconds':10})
            os.close(alive_w)
            send(request_w,{'pid':child.pid,'parent_pid':os.getpid(),'start_ticks':child.start})
            need(life.read_line(ack_r,deadline)==b'REGISTERED\n','outer worker registration acknowledgement')
            child.release(); need(life.read_line(alive_r,deadline)==b'ALIVE\n','leaf did not start')
            os.close(alive_r)
            # Intentionally skip waiting: PDEATHSIG must kill the leaf, and
            # the outer subreaper must adopt and reap that exact registered PID.
            os._exit(29)
        functions=(normal_case,early_case,death_case)
        # The fixed three-birth factory is confined to this fixture host. All
        # case children remain blocked until all three are bound and it seals.
        for index,case in enumerate(CASES):
            guard(); rel_r,rel_w=os.pipe(); ready_r,ready_w=os.pipe(); parent=os.getpid()
            pid=os.fork()
            if pid==0:
                try:
                    os.close(rel_w); os.close(ready_r)
                    signal.signal(signal.SIGALRM,signal.SIG_DFL)
                    signal.setitimer(signal.ITIMER_REAL,max(0.000001,(deadline-time.monotonic_ns())/NS))
                    resource.setrlimit(resource.RLIMIT_CPU,(10,10))
                    life.prctl(1,signal.SIGKILL); need(os.getppid()==parent,'fixture host disappeared')
                    # Close inherited factory handles. No case may reap another
                    # case or hold another case's release pipe open.
                    for previous in children:
                        os.close(previous.fd)
                        if previous.release_fd is not None: os.close(previous.release_fd)
                    os.close(request_r); os.close(ack_w)
                    row=life.shape(os.getpid(),cpu,parent)
                    send(ready_w,{'pid':row['pid'],'start_ticks':row['start_ticks'],'case':case}); os.close(ready_w)
                    need(life.read_line(rel_r,deadline)==life.RELEASE,'fixture case release'); os.close(rel_r)
                    code=functions[index](); os._exit(code)
                except BaseException: os._exit(127)
            child=life.Child(pid,cpu,parent); child.release_fd=rel_w; children.append(child)
            os.close(rel_r); os.close(ready_w); child.bind()
            message=json.loads(life.read_line(ready_r,deadline)); os.close(ready_r)
            need(message=={'pid':pid,'start_ticks':child.start,'case':case},'fixture case identity')
        life.seal(); os.close(request_w); os.close(ack_r)
        for index in (0,1):
            children[index].release(); wait_child(children[index],0)
        children[2].release()
        reg=json.loads(life.read_line(request_r,deadline))
        need(set(reg)=={'pid','parent_pid','start_ticks'} and reg['parent_pid']==children[2].pid and
             type(reg['pid']) is int and type(reg['start_ticks']) is int,'death worker registration')
        remote_fd=os.pidfd_open(reg['pid'],0)
        need(life.remote_sample(remote_fd,reg['pid'],cpu,reg['parent_pid'],reg['start_ticks'],True) is not None,
             'death worker exited before registration')
        life.shape(children[2].pid,cpu,os.getpid(),children[2].start,True)
        need(os.write(ack_w,b'REGISTERED\n')==11,'death acknowledgement'); os.close(ack_w); os.close(request_r)
        wait_child(children[2],29)
        # Its direct parent is gone; subreaper adoption is now expected here.
        life.shape(reg['pid'],cpu,os.getpid(),reg['start_ticks'],True)
        adopted=life.Child(reg['pid'],cpu,os.getpid()); adopted.fd=remote_fd
        adopted.start=reg['start_ticks']; adopted.sealed=True
        children.append(adopted); wait_child(adopted,-signal.SIGKILL)
        life.assert_no_children(); life.require_sealed(os.getpid())
        save(root/'DEATH_CASE.json',{'status':'EXPECTED-HOLD-CLEANUP-CLOSED','controller_exit_code':29,
             'worker_exit_code':-signal.SIGKILL,'registered_worker':reg,'adopted_and_reaped':True})
        need(read(root/'NORMAL_LEAF.json')=={'spawn_errno':errno.EAGAIN,'AS':AS,'NPROC':[0,0]},'normal leaf evidence')
        need(read(root/'EARLY_CASE.json')['release_rejected'] is True,'early case evidence')
        need(not any(n.startswith(('flint','numpy','scipy','theta','shift_')) for n in sys.modules),'scientific module present')
        guard(); life.assert_no_children()
        end_ns=time.monotonic_ns(); need(0<end_ns-start_ns<10*NS,'whole fixture wall/one-CPU capacity')
        signal.setitimer(signal.ITIMER_REAL,0)
        # Immutable external audit only after actual exits/closure. No test,
        # retry, native import, or numerical operation follows this boundary.
        files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.iterdir()) if p.is_file()]
        result={'status':'FIXTURE-PASS','contract_sha256':expected,'launch_id':contract['launch_id'],
                'lifecycle_sha256':contract['lifecycle_sha256'],'fixture_source_sha256':contract['fixture_source_sha256'],
                'cases':list(CASES),'closed_tree':True,'closure_evidence':'final ECHILD',
                'wall_ns':end_ns-start_ns,'tree_cpu_capacity_upper_ns':end_ns-start_ns,
                'start_ns':start_ns,'end_ns':end_ns,'CPU_affinity':[cpu],
                'factory_direct_children':3,'case_child_births':3,'normal_expected_failed_forks':1,
                'bundles_executed':1,'automatic_retry':False,'scientific_imports':0,
                'test_files':files,'requires_external_tool_exit_code':0,'RH_PROOF':'NOT-OBTAINED'}
        save(root/'FIXTURE_RESULT.json',result)
        print(json.dumps({'status':'FIXTURE-PASS','result_sha256':sha(root/'FIXTURE_RESULT.json')}),flush=True)
        return 0
    except BaseException as exc:
        kill_all(); closure={'closed':False,'reason':'setup/deadline unavailable'}
        if life is not None and deadline is not None:
            try: closure=life.cleanup(children,deadline)
            except BaseException as e: closure={'closed':False,'reason':str(e)}
        signal.setitimer(signal.ITIMER_REAL,0)
        try: save(root/'FIXTURE_HOLD.json',{'status':'HOLD','reason':str(exc),
                  'exception_type':type(exc).__name__,'cleanup':closure,'automatic_retry':False})
        except BaseException: pass
        return 2


if __name__=='__main__': raise SystemExit(main())
