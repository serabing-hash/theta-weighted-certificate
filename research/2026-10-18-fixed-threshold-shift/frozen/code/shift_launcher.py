"""Explicit one-use launcher and watchdog; never imported to run a calculation.

No fixture mode, no automatic retry, no source producer. Linux/flat-procfs gate.
One controller and one scientific worker, under an external observer; all share one CPU.
RLIMIT_AS is a kernel allocation limit. RSS and whole-tree CPU are observed
stopping/acceptance limits; scheduling/kill latency is not claimed to be zero.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import select
import signal
import sys
import time
import shift_lifecycle as life

NS=1_000_000_000
LIMITS={'wall_seconds':60,'tree_cpu_seconds':60,'worker_as_bytes':402653184,
        'worker_rss_kib':327680,'threads':1,'scientific_workers':1,'poll_seconds':0.01}


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        while block:=f.read(1<<20): h.update(block)
    return h.hexdigest()


def read(p):
    def unique(items):
        d={}
        for k,v in items: need(k not in d,'duplicate key'); d[k]=v
        return d
    return json.loads(Path(p).read_text(),object_pairs_hook=unique)


def write_new(p,obj):
    data=(json.dumps(obj,sort_keys=True,indent=2)+'\n').encode()
    with Path(p).open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    need(Path(p).read_bytes()==data,'audit receipt byte readback')
    fd=os.open(Path(p).parent,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)


def status_fields(pid):
    return dict(line.split(':',1) for line in Path('/proc',str(pid),'status').read_text().splitlines() if ':' in line)


def worker_sample(pid, expected_start, cpu):
    return life.shape(pid,cpu,os.getpid(),expected_start,True)


def main():
    admission=getattr(sys,'_shift_source_admission',None)
    need(admission and admission['role']=='launcher' and admission['source_only'] is True, 'source-only controller admission')
    need(len(sys.argv)==6 and sys.argv[1]=='--execute-once' and sys.argv[2]=='--plan'
         and sys.argv[4]=='--expected-plan-sha256','explicit execute-once and plan hash required')
    need(sys.flags.isolated and sys.flags.no_site and not sys.flags.optimize,'launch with -I -S -B, no optimization')
    need(not any(os.environ.get(k) for k in ('LD_PRELOAD','LD_LIBRARY_PATH','PYTHONPATH')),
         'injected environment')
    plan_path=Path(sys.argv[3]).resolve(); expected=sys.argv[5]
    need(sha(plan_path)==expected,'exact reviewed plan hash')
    plan=read(plan_path)
    need(plan['scope']=='SHIFT372_H2_DELTA_STAR_FIXED_C_ONCE_V1' and plan['limits']==LIMITS,'fixed contract')
    need(plan['tree_protocol']==life.PROTOCOL,'registered tree protocol')
    code=Path(plan['code_root']); attempt=Path(plan['attempt_root'])
    need(Path(__file__).resolve()==code/'shift_launcher.py','bound launcher path')
    need(attempt.is_dir() and (attempt/'OBSERVER_EPOCH.json').is_file(),'observer epoch directory absent')
    need(os.getppid()==int(os.environ['SHIFT_OBSERVER_PID']),'observer parent absent')
    epoch_record=read(attempt/'OBSERVER_EPOCH.json')
    need(epoch_record['plan_sha256']==expected and str(epoch_record['t0_ns'])==os.environ['SHIFT_EPOCH_NS'],'observer epoch binding')
    need(os.readlink('/proc/self')==str(os.getpid()),'flat procfs PID mapping required')
    need(os.getuid()!=0 and int(status_fields(os.getpid())['CapEff'],16)&((1<<21)|(1<<24))==0,
         'unprivileged NPROC enforcement required')
    need(len(list(Path('/proc/self/task').iterdir()))==1,'one controller thread')
    need(hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal'),'pidfd control unavailable')
    cpu=plan['cpu_affinity']; need(type(cpu) is int and cpu in os.sched_getaffinity(0),'reviewed CPU unavailable')
    os.sched_setaffinity(0,{cpu})
    # The external observer owns the one common epoch; no new READY/BEGIN.
    cpu_baseline=time.process_time_ns(); t0=int(os.environ['SHIFT_EPOCH_NS']); deadline=t0+60*NS
    pid=None; pidfd=None; child_usage=None; wait_status=None; reaped=False; worker_child=None
    first_start=None; samples=0; peak=0; peak_cpu_upper=0; stopped=None
    def kill_worker():
        if pidfd is not None:
            try: signal.pidfd_send_signal(pidfd,signal.SIGKILL)
            except ProcessLookupError: pass
        elif pid is not None and not reaped:
            # This is our own unreaped child; its PID cannot have been reused.
            try: os.kill(pid,signal.SIGKILL)
            except ProcessLookupError: pass
    def alarm(signum,frame):
        kill_worker()
        # No result serialization after the absolute deadline.
        os._exit(124)
    signal.signal(signal.SIGALRM,alarm)
    signal.setitimer(signal.ITIMER_REAL,max(0.000001,(deadline-time.monotonic_ns())/NS))
    resource.setrlimit(resource.RLIMIT_AS,(402653184,402653184))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    parent_cpu_fallback=math.ceil(time.process_time())+60
    resource.setrlimit(resource.RLIMIT_CPU,(parent_cpu_fallback,parent_cpu_fallback))
    def guard_parent():
        need(time.monotonic_ns()<deadline,'60second wall gate')
        need(os.getppid()==int(os.environ['SHIFT_OBSERVER_PID']),'observer disappeared')
        need(os.sched_getaffinity(0)=={cpu},'controller affinity changed')
        need(len(list(Path('/proc/self/task').iterdir()))==1,'controller extra thread')
        if worker_child is not None: life.require_sealed(os.getpid())
    result={'status':'HOLD','scope':plan['scope'],'plan_sha256':expected,'launch_id':plan['launch_id']}
    try:
        write_new(attempt/'SINGLE_ATTEMPT_CONSUMED.json',{'plan_sha256':expected,'t0_ns':t0,
                   'launch_id':plan['launch_id'],'automatic_retry':False})
        for name,h in plan['code_sha256'].items():
            guard_parent(); need(sha(code/name)==h,'bound code '+name)
        need(sha(plan['input_manifest'])==plan['input_manifest_sha256'],'bound inputs')
        need(sha(plan['frozen_contract'])==plan['frozen_contract_sha256'],'unchanged previous contract')
        need(sha(plan['shift_proof'])==plan['shift_proof_sha256'],'unchanged shift proof')
        need(sha(Path(sys.executable).resolve())==plan['python_sha256'],'interpreter bytes')
        guard_parent()
        # Do not inherit an ignored SIGCHLD disposition that would auto-reap
        # the child and make full-life wait4 accounting unavailable.
        life.prepare_parent(cpu)
        logfd=os.open(attempt/'WORKER_STDOUT.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_SYNC,0o600)
        errfd=os.open(attempt/'WORKER_STDERR.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_SYNC,0o600)
        env={**os.environ,'SHIFT_PLAN':str(plan_path),'SHIFT_PLAN_SHA256':expected,
             'SHIFT_INPUT_SHA256':plan['input_manifest_sha256'],'SHIFT_LAUNCH_ID':plan['launch_id'],
             'SHIFT_EPOCH_NS':str(t0),'SHIFT_CONTROLLER_PID':str(os.getpid()),'SHIFT_CPU':str(cpu),
             'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1',
             'PYTHONNOUSERSITE':'1'}
        def worker_exec():
            os.dup2(logfd,1); os.dup2(errfd,2); os.close(logfd); os.close(errfd)
            env['SHIFT_RELEASED']=plan['launch_id']
            os.close(int(env['SHIFT_OBSERVER_REQUEST_FD'])); os.close(int(env['SHIFT_OBSERVER_REPLY_FD']))
            os.execve(sys.executable,admission['argv_for']('entry'),env)
        worker_child=life.fork_one(cpu,deadline,worker_exec,
                                   {'as_bytes':402653184,'cpu_seconds':60})
        pid=worker_child.pid; pidfd=worker_child.fd; first_start=worker_child.start
        os.close(logfd); os.close(errfd)
        # Register the still-blocked worker with the observer before release.
        packet=json.dumps({'op':'worker','pid':pid,'start_ticks':first_start,
                           'controller_pid':os.getpid(),'launch_id':plan['launch_id']},separators=(',',':')).encode()+b'\n'
        request_fd=int(os.environ['SHIFT_OBSERVER_REQUEST_FD']); reply_fd=int(os.environ['SHIFT_OBSERVER_REPLY_FD'])
        need(len(packet)<=4096 and os.write(request_fd,packet)==len(packet),'observer registration write')
        reply=b''
        while not reply.endswith(b'\n'):
            guard_parent(); ready=select.select([reply_fd],[],[],min(0.01,max(0,(deadline-time.monotonic_ns())/NS)))[0]
            if ready:
                part=os.read(reply_fd,4096); need(part,'observer registration pipe closed'); reply+=part
                need(len(reply)<=4096,'observer registration reply length')
        ack=json.loads(reply); need(ack=={'release_worker':pid,'start_ticks':first_start,
                                        'launch_id':plan['launch_id']},'observer worker release binding')
        worker_child.release()
        ticks=os.sysconf('SC_CLK_TCK')
        while True:
            guard_parent()
            done,st,u=worker_child.poll()
            if done:
                wait_status=st; child_usage=u; reaped=True; break
            before=time.monotonic_ns()
            row=worker_sample(pid,first_start,cpu); first_start=row['start_ticks']
            peak=max(peak,row['hwm_kib'],row['rss_kib']); samples+=1
            need(peak<=327680,'worker320MiB RSS/HWM gate')
            now=time.monotonic_ns()
            # Lifetime worker counters include its pre-exec work. Two ticks
            # pad counter granularity; the one-CPU elapsed gap covers reads.
            cpu_upper=(time.process_time_ns()-cpu_baseline)+((row['cpu_ticks']+2)*NS+ticks-1)//ticks+(now-before)
            peak_cpu_upper=max(peak_cpu_upper,cpu_upper)
            need(cpu_upper<60*NS,'whole controller+worker CPU upper gate')
            select.select([pidfd],[],[],min(0.01,max(0,(deadline-now)/NS)))
        need(os.waitstatus_to_exitcode(wait_status)==0,'worker failed or was killed')
        life.assert_no_children()
        need(child_usage.ru_maxrss<=327680,'final kernel worker RSS high-water mark')
        wr=read(attempt/'WORKER_RESULT.json')
        need(wr['status']=='MATH-COMPLETE-RESOURCE-GATE-PENDING' and wr['plan_sha256']==expected
             and wr['input_manifest_sha256']==plan['input_manifest_sha256'],'worker result binding')
        need(wr['check_report_sha256']==sha(attempt/'math/INDEPENDENT_CHECK.json') and
             wr['checker_sha256']==plan['code_sha256']['shift_checker.py'],'exact checker report bytes')
        for name,h in plan['code_sha256'].items(): need(sha(code/name)==h,'post-run code bytes '+name)
        need(sha(plan_path)==expected,'plan unchanged')
        guard_parent()
        # wait4 measures the complete child lifetime; it has no descendants.
        # Float-to-ns ceilings plus4us cover reported usage rounding.
        child_cpu_upper=math.ceil(child_usage.ru_utime*NS)+math.ceil(child_usage.ru_stime*NS)+4000
        final_cpu_upper=time.process_time_ns()-cpu_baseline+child_cpu_upper
        before_serialization=time.monotonic_ns()
        need(before_serialization-t0<60*NS and final_cpu_upper<60*NS,'pre-serialization gates')
        result.update(status='CONTROLLER-COMPLETE-EXTERNAL-ACCEPTANCE-PENDING',
             t0_ns=t0,before_serialization_ns=before_serialization,
             controller_worker_cpu_snapshot_upper_ns=final_cpu_upper,
             live_cpu_upper_max_ns=peak_cpu_upper,worker_exit_code=0,
             worker_wait4={'user_seconds':child_usage.ru_utime,'system_seconds':child_usage.ru_stime,
                           'maxrss_kib':child_usage.ru_maxrss},
             worker_reaped=True,worker_pid=pid,observed_worker_peak_kib=peak,samples=samples,
             tree_protocol=life.PROTOCOL,registered_worker=worker_child.record(),
             controller_NPROC_soft_hard=[0,0],closure_evidence='wait4(-1,WNOHANG|__WALL) -> ECHILD',
             CPU_affinity=[cpu],worker_descendants_permitted=0,scientific_workers=1,
             checker_report_sha256=wr['check_report_sha256'],RH_PROOF='NOT-OBTAINED',
             acceptance='No file/status string is final acceptance; observer must see actual controller exit and final bytes.',
             snapshot_is_not_endpoint=True)
        # Every JSON encoding/write/fsync/readback and final stdout emission is
        # BEFORE the post-serialization gate; timer is never disarmed.
        write_new(attempt/'RESOURCE_RECEIPT.json',result)
        status={'status':'CONTROLLER-RESULT-SERIALIZED-OBSERVER-PENDING',
                'plan_sha256':expected,'resource_receipt_sha256':sha(attempt/'RESOURCE_RECEIPT.json'),
                'checker_report_sha256':wr['check_report_sha256']}
        write_new(attempt/'CONTROLLER_FINAL_STATUS.json',status)
        print(json.dumps(status),flush=True); os.fsync(1); os.fsync(2)
        guard_parent()
        need(time.process_time_ns()-cpu_baseline+child_cpu_upper<60*NS,'post-serialization CPU gate')
        need(time.monotonic_ns()-t0<60*NS,'post-serialization wall gate')
        life.assert_no_children()
        guard_parent()
        # This process cannot attest its own exit time. The external observer
        # waits for actual exit, rechecks files, and charges its work as well.
        os._exit(0)
    except BaseException as exc:
        kill_worker()
        closure={'closed':False,'reason':'cleanup incomplete'}
        try: closure=life.cleanup([worker_child],deadline)
        except BaseException as cleanup_error: closure={'closed':False,'reason':str(cleanup_error)}
        # Failure evidence is best effort only while the same deadline remains.
        # After expiration, stop with no late result serialization or PASS.
        if time.monotonic_ns()<deadline and attempt.is_dir():
            try:
                write_new(attempt/'CONTROLLER_HOLD.json',{'status':'HOLD','reason':str(exc),
                     'exception_type':type(exc).__name__,'automatic_retry':False,'cleanup':closure})
            except BaseException: pass
        os._exit(2 if time.monotonic_ns()<deadline else 124)


if __name__=='__main__':
    raise SystemExit(main())
