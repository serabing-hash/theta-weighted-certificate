"""Static revision: observe the controller's actual exit inside the same epoch.

No self-issued PASS. Final files remain pending a terminal observer-exit witness.
This file and its process protocol have NOT been dynamically exercised.
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
        result={}
        for k,v in items: need(k not in result,'duplicate JSON key'); result[k]=v
        return result
    return json.loads(Path(p).read_bytes(),object_pairs_hook=unique)


def write_new(p,obj):
    data=(json.dumps(obj,sort_keys=True,indent=2)+'\n').encode()
    with Path(p).open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    need(Path(p).read_bytes()==data,'observer receipt readback')
    fd=os.open(Path(p).parent,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)


def fields(pid):
    return dict(line.split(':',1) for line in Path('/proc',str(pid),'status').read_text().splitlines() if ':' in line)


def main():
    admission=getattr(sys,'_shift_source_admission',None)
    need(admission and admission['role']=='observer' and admission['source_only'] is True,'verified source observer')
    need(len(sys.argv)==6 and sys.argv[1:3]==['--execute-once','--plan'] and
         sys.argv[4]=='--expected-plan-sha256','frozen observer invocation')
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and not sys.flags.optimize,
         'isolated interpreter flags')
    plan_path=Path(sys.argv[3]); expected=sys.argv[5]
    need(sha(plan_path)==expected,'plan binding'); plan=read(plan_path)
    need(plan['limits']==LIMITS and plan['scope']=='SHIFT372_H2_DELTA_STAR_FIXED_C_ONCE_V1','frozen scope')
    need(plan['resource_protocol']=='COMMON_EPOCH_FINALIZATION_EXTERNAL_EXIT_PENDING_V2','endpoint protocol')
    need(plan['source_protocol']=='VERIFIED_SOURCE_BYTES_BEFORE_FIRST_LOCAL_IMPORT_V1','source protocol')
    need(plan['tree_protocol']==life.PROTOCOL,'registered tree protocol')
    attempt=Path(plan['attempt_root']); code=Path(plan['code_root']); cpu=plan['cpu_affinity']
    need(Path(__file__).resolve()==code/'shift_observer.py','observer path binding')
    need(os.environ['SHIFT_OBSERVER_PID']==str(os.getpid()),'observer epoch owner')
    t0=int(os.environ['SHIFT_EPOCH_NS']); deadline=t0+60*NS
    need(attempt.is_dir() and not attempt.is_symlink(),'bootstrap attempt mark absent')
    epoch_record=read(attempt/'OBSERVER_EPOCH.json')
    need(epoch_record=={'t0_ns':t0,'plan_sha256':expected,'launch_id':plan['launch_id'],
                       'observer_pid':os.getpid(),'whole_attempt_seconds':60,'automatic_retry':False,
                       'created_by':'source_bootstrap','consumed_before_source_admission':True,
                       'consumption_authority':'exclusive_attempt_directory'},'bootstrap consumption binding')
    baseline=int(os.environ['SHIFT_OBSERVER_CPU_BASELINE_NS'])
    need(os.readlink('/proc/self')==str(os.getpid()),'flat procfs')
    need(os.getuid()!=0 and int(fields(os.getpid())['CapEff'],16)&((1<<21)|(1<<24))==0,
         'unprivileged worker NPROC enforcement')
    need(hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal'),'pidfd required')
    controller=None; controller_fd=None; controller_reaped=False; controller_child=None
    worker=None; worker_fd=None; controller_start=None; worker_start=None
    def kill_tree():
        for fd in (worker_fd,controller_fd):
            if fd is not None:
                try: signal.pidfd_send_signal(fd,signal.SIGKILL)
                except ProcessLookupError: pass
        if controller is not None and controller_fd is None and not controller_reaped:
            try: os.kill(controller,signal.SIGKILL)
            except ProcessLookupError: pass
    def expired(signum,frame):
        kill_tree(); os._exit(124)
    signal.signal(signal.SIGALRM,expired)
    need(time.monotonic_ns()<deadline,'observer admission deadline')
    signal.setitimer(signal.ITIMER_REAL,max(0.000001,(deadline-time.monotonic_ns())/NS))
    resource.setrlimit(resource.RLIMIT_AS,(402653184,402653184))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    fallback=math.ceil(time.process_time())+60
    resource.setrlimit(resource.RLIMIT_CPU,(fallback,fallback))
    def guard():
        need(os.sched_getaffinity(0)=={cpu},'observer affinity')
        need(len(list(Path('/proc/self/task').iterdir()))==1,'one observer thread')
        if controller_child is not None: life.require_sealed(os.getpid())
        now=time.monotonic_ns()
        need(0<=now-t0<60*NS,'common wall and single-CPU capacity gates')
        return now
    try:
        guard(); life.prepare_parent(cpu,subreaper=True)
        # The stdlib bootstrap already consumed this attempt before admission.
        # Validation above cannot create or repair a missing consumption mark.
        for name,digest in plan['code_sha256'].items():
            guard(); need(sha(code/name)==digest,'source admission '+name)
        for path_key,hash_key in [('input_manifest','input_manifest_sha256'),
                                  ('frozen_contract','frozen_contract_sha256'),('shift_proof','shift_proof_sha256')]:
            guard(); need(sha(plan[path_key])==plan[hash_key],'bound '+path_key)
        request_read,request_write=os.pipe(); reply_read,reply_write=os.pipe()
        os.set_inheritable(request_write,True); os.set_inheritable(reply_read,True)
        os.set_blocking(request_read,False)
        logfd=os.open(attempt/'CONTROLLER_STDOUT.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_SYNC,0o600)
        errfd=os.open(attempt/'CONTROLLER_STDERR.log',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_SYNC,0o600)
        env={**os.environ,'SHIFT_OBSERVER_REQUEST_FD':str(request_write),'SHIFT_OBSERVER_REPLY_FD':str(reply_read)}
        owner=os.getpid()
        def controller_exec():
            os.close(request_read); os.close(reply_write)
            os.dup2(logfd,1); os.dup2(errfd,2); os.close(logfd); os.close(errfd)
            os.execve(sys.executable,admission['argv_for']('launcher'),env)
        controller_child=life.fork_one(cpu,deadline,controller_exec)
        controller=controller_child.pid; controller_fd=controller_child.fd; controller_start=controller_child.start
        os.close(request_write); os.close(reply_read); os.close(logfd); os.close(errfd)
        controller_child.release()
        packet=b''; registered=False; polls=0
        while True:
            now=guard(); polls+=1
            ready=select.select([request_read,controller_fd],[],[],min(0.01,max(0,(deadline-now)/NS)))[0]
            if request_read in ready:
                chunk=os.read(request_read,4096)
                if chunk:
                    need(not registered,'duplicate worker registration'); packet+=chunk
                    need(len(packet)<=4096,'worker registration too long')
                    if packet.endswith(b'\n'):
                        reg=json.loads(packet)
                        need(set(reg)=={'op','pid','start_ticks','controller_pid','launch_id'} and reg['op']=='worker'
                             and reg['controller_pid']==controller and reg['launch_id']==plan['launch_id']
                             and type(reg['pid']) is int and reg['pid']>0,'worker registration binding')
                        worker=reg['pid']; worker_fd=os.pidfd_open(worker,0)
                        worker_start=reg['start_ticks']
                        need(type(worker_start) is int and worker_start>0,'registered starttime')
                        need(life.remote_sample(worker_fd,worker,cpu,controller,worker_start,True) is not None,
                             'registered worker already exited')
                        life.shape(controller,cpu,owner,controller_start,True)
                        ack=json.dumps({'release_worker':worker,'start_ticks':worker_start,
                                        'launch_id':plan['launch_id']},separators=(',',':')).encode()+b'\n'
                        guard(); need(os.write(reply_write,ack)==len(ack),'observer acknowledgement')
                        registered=True
                elif not registered: raise RuntimeError('controller exited before worker registration')
            done,st,usage=controller_child.poll()
            if done:
                controller_reaped=True; controller_exit_observed_ns=guard(); break
            controller_child.sample()
            if registered:
                life.remote_sample(worker_fd,worker,cpu,controller,worker_start,True)
        need(os.waitstatus_to_exitcode(st)==0,'controller failed or was killed')
        need(registered and select.select([worker_fd],[],[],0)[0],'worker exit not observed')
        life.assert_no_children()
        # The exited controller can no longer change its receipt or stdout.
        receipt=read(attempt/'RESOURCE_RECEIPT.json')
        final=read(attempt/'CONTROLLER_FINAL_STATUS.json'); worker_result=read(attempt/'WORKER_RESULT.json')
        need(receipt['status']=='CONTROLLER-COMPLETE-EXTERNAL-ACCEPTANCE-PENDING' and
             receipt['plan_sha256']==expected and receipt['worker_reaped'] is True and
             receipt['tree_protocol']==life.PROTOCOL and receipt['controller_NPROC_soft_hard']==[0,0] and
             receipt['registered_worker']['start_ticks']==worker_start and
             receipt['worker_pid']==worker and receipt['worker_exit_code']==0,'controller final binding')
        need(receipt['worker_wait4']['maxrss_kib']<=327680 and receipt['observed_worker_peak_kib']<=327680,
             'complete worker RSS gate')
        need(final['status']=='CONTROLLER-RESULT-SERIALIZED-OBSERVER-PENDING' and final['plan_sha256']==expected
             and final['resource_receipt_sha256']==sha(attempt/'RESOURCE_RECEIPT.json'),'serialized controller status')
        check_hash=sha(attempt/'math/INDEPENDENT_CHECK.json')
        need(final['checker_report_sha256']==receipt['checker_report_sha256']==
             worker_result['check_report_sha256']==check_hash,'final checker byte binding')
        need(worker_result['worker_pid']==worker and worker_result['controller_pid']==controller and
             worker_result['plan_sha256']==expected,'worker identity binding')
        need(sha(plan_path)==expected,'unchanged final plan')
        for name,digest in plan['code_sha256'].items(): guard(); need(sha(code/name)==digest,'unchanged final code')
        # All three roles are confined to one CPU, inherited from before t0.
        # Its elapsed capacity bounds total CPU, including startup/serialization.
        # wait4 numbers below are diagnostics; do not sum them with child usage.
        snapshot=guard()
        write_new(attempt/'OBSERVER_RECEIPT.json',{
            'status':'CONTROLLER-EXIT-OBSERVED-OBSERVER-EXIT-PENDING','plan_sha256':expected,
            'launch_id':plan['launch_id'],'t0_ns':t0,'controller_exit_observed_ns':controller_exit_observed_ns,
            'controller_exit_code':0,'worker_exit_observed':True,'no_unreaped_descendants':True,
            'tree_protocol':life.PROTOCOL,'closure_evidence':'wait4(-1,WNOHANG|__WALL) -> ECHILD',
            'registered_controller':controller_child.record(),'observer_NPROC_soft_hard':[0,0],
            'registered_worker':{'pid':worker,'parent_pid':controller,'start_ticks':worker_start,'pidfd_bound':True},
            'snapshot_ns':snapshot,'snapshot_is_not_endpoint':True,
            'tree_cpu_capacity_snapshot_upper_ns':snapshot-t0,'capacity_basis':'one shared CPU for all prescribed threads',
            'observer_cpu_snapshot_ns':time.process_time_ns()-baseline,
            'controller_wait4_diagnostic':{'user_seconds':usage.ru_utime,'system_seconds':usage.ru_stime,'maxrss_kib':usage.ru_maxrss},
            'control_processes':2,'scientific_workers':1,'threads_per_process':1,'CPU_affinity':[cpu],
            'polls':polls,'source_only_import_events':admission['events'],'RH_PROOF':'NOT-OBTAINED',
            'acceptance':'PENDING: independent observer terminal-exit time and unchanged-file witness required.'})
        write_new(attempt/'OBSERVER_FINAL_STATUS.json',{
            'status':'SERIALIZED-RESULTS-EXTERNAL-TERMINAL-WITNESS-PENDING','plan_sha256':expected,
            'observer_receipt_sha256':sha(attempt/'OBSERVER_RECEIPT.json'),
            'controller_final_status_sha256':sha(attempt/'CONTROLLER_FINAL_STATUS.json'),
            'checker_report_sha256':check_hash,'resource_acceptance':False,'RH_PROOF':'NOT-OBTAINED'})
        files=[]
        for p in sorted(attempt.rglob('*')):
            guard(); need(not p.is_symlink(),'artifact symlink')
            if p.is_file(): files.append({'path':str(p.relative_to(attempt)),'bytes':p.stat().st_size,'sha256':sha(p)})
        write_new(attempt/'FINAL_ARTIFACT_MANIFEST.json',{'format':'SHIFT372_FINAL_BYTES_V1',
                  'plan_sha256':expected,'status':'EXTERNAL-TERMINAL-WITNESS-PENDING','files':files,
                  'excludes':['FINAL_ARTIFACT_MANIFEST.json'],'no_self_endpoint_claim':True})
        manifest_hash=sha(attempt/'FINAL_ARTIFACT_MANIFEST.json')
        # Final stdout serialization/flush is charged too. The transport is not
        # assumed fsync-able. A blocked pipe remains subject to the same timer.
        print(json.dumps({'status':'EXTERNAL-TERMINAL-WITNESS-PENDING','plan_sha256':expected,
                          'final_manifest_sha256':manifest_hash,'resource_acceptance':False}),flush=True)
        for item in files:
            guard(); p=attempt/item['path']
            need(p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'final artifact readback')
        need(sha(attempt/'FINAL_ARTIFACT_MANIFEST.json')==manifest_hash,'final manifest readback')
        life.assert_no_children()
        guard()  # LAST gate, after ALL result serialization and readback.
        # No output after this gate. Timer remains armed. Exit0 is provisional:
        # this process cannot attest the time at which it actually terminates.
        os._exit(0)
    except BaseException as exc:
        kill_tree()
        closure={'closed':False,'reason':'cleanup incomplete'}
        try: closure=life.cleanup([controller_child],deadline)
        except BaseException as cleanup_error: closure={'closed':False,'reason':str(cleanup_error)}
        if time.monotonic_ns()<deadline and attempt.is_dir():
            try: write_new(attempt/'OBSERVER_HOLD.json',{'status':'HOLD','reason':str(exc),
                        'exception_type':type(exc).__name__,'automatic_retry':False,
                        'cleanup':closure,
                        'termination_observation':'not certified by failure path'})
            except BaseException: pass
        os._exit(2 if time.monotonic_ns()<deadline else 124)


if __name__=='__main__': main()
