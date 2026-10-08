"""CC BY-NC 4.0. External absolute deadlines; no 602-second grace."""
import argparse, functools, json, os, pathlib, resource, signal, subprocess, sys, time
import v2_support as s
def limits(pidfile):
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU,(600,600))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    pathlib.Path(pidfile).write_text(json.dumps({'namespace_PID':os.getpid(),'procfs_PID':int(os.readlink('/proc/self')),'pid_namespace_inode':os.stat('/proc/self/ns/pid').st_ino}))
def run(command,output,soft=590,hard=600):
    output=pathlib.Path(output);output.mkdir(parents=True,exist_ok=True)
    clock=time.monotonic();events=[];peak={};last={};term=False;killed=False
    with (output/'worker.stdout.log').open('xb') as out,(output/'worker.stderr.log').open('xb') as err:
        proc=subprocess.Popen(command,stdout=out,stderr=err,start_new_session=True,preexec_fn=functools.partial(limits,str(output/'PROCESS_ID_MAP.json')),env={**os.environ,'V2_SUPERVISOR_START':repr(clock),'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
        pidmap=s.small_json(output/'PROCESS_ID_MAP.json');assert pidmap['namespace_PID']==proc.pid
        while True:
            now=time.monotonic();elapsed=now-clock
            try:
                for line in pathlib.Path(f"/proc/{pidmap['procfs_PID']}/status").read_text().splitlines():
                    key,_,value=line.partition(':')
                    if key in ('VmRSS','VmHWM','VmSize','VmPeak'):
                        n=int(value.split()[0]);last[key+'_KiB']=n;peak[key+'_KiB']=max(peak.get(key+'_KiB',0),n)
            except (FileNotFoundError,ProcessLookupError):pass
            if not term and elapsed>=soft:
                term=True
                try:os.killpg(proc.pid,signal.SIGTERM);events.append({'signal':'SIGTERM','wall_seconds':elapsed,'deadline':soft,'overshoot_seconds':max(0,elapsed-soft)})
                except ProcessLookupError:events.append({'signal':'SIGTERM','wall_seconds':elapsed,'group_already_absent':True})
            if not killed and elapsed>=hard:
                killed=True
                try:os.killpg(proc.pid,signal.SIGKILL);events.append({'signal':'SIGKILL','wall_seconds':elapsed,'deadline':hard,'overshoot_seconds':max(0,elapsed-hard)})
                except ProcessLookupError:events.append({'signal':'SIGKILL','wall_seconds':elapsed,'group_already_absent':True})
            pid,status,usage=os.wait4(proc.pid,os.WNOHANG)
            if pid:
                proc.returncode=os.waitstatus_to_exitcode(status);break
            time.sleep(min(0.05,max(0.001,(soft if not term else hard)-elapsed)))
    record={'command':command,'pid':proc.pid,'process_group_id':proc.pid,'procfs_identity':pidmap,'worker_exit_code':proc.returncode,'wall_seconds':time.monotonic()-clock,'worker_user_CPU_seconds':usage.ru_utime,'worker_system_CPU_seconds':usage.ru_stime,'worker_CPU_seconds':usage.ru_utime+usage.ru_stime,'wait4_peak_RSS_KiB':usage.ru_maxrss,'sampled_peak_memory':peak,'last_sample_memory':last,'monotonic_deadlines':{'SIGTERM_seconds':soft,'SIGKILL_seconds':hard},'termination_events':events,'RLIMIT_CPU_seconds':600,'RLIMIT_AS_bytes':512*1024*1024,'internal_RSS_stop_bytes':500*1024*1024,'sampling_interval_seconds':0.05,'OS_limits':'signals issued when supervisor is scheduled; delivery, accounting, and stop time have OS scheduling granularity; AS limit is allocation refusal, not RSS guarantee','completion_not_guaranteed':True}
    s.save(output/'SUPERVISOR_TERMINATION.json',record);return record
def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',action='store_true');args=p.parse_args()
    if args.fixture:
        dummy=s.CODE/'supervisor_dummy.py';output=s.ROOT/'static/supervisor_fixture'
        r=run([sys.executable,str(dummy)],output,.2,.4)
        assert r['worker_exit_code']==-signal.SIGKILL and [v['signal'] for v in r['termination_events']]==['SIGTERM','SIGKILL']
        # A killed grandchild may briefly remain a zombie, but must not remain running.
        child=s.small_json(output/'grandchild_pid.txt');status=pathlib.Path(f"/proc/{child['procfs_PID']}/status")
        until=time.monotonic()+1
        while status.exists() and '\nState:\tZ' not in status.read_text() and time.monotonic()<until:time.sleep(.01)
        if status.exists():assert '\nState:\tZ' in status.read_text()
        s.save(output/'FIXTURE_PASS.json',{'result':'PASS','child_identity':child,'child_not_running':True,'math_source_calls':0,'physical_pilot_attempts':0})
        print(json.dumps(r));return
    gate=s.small_json(s.ROOT/'static/STATIC_GATE.json');assert gate['status']=='PASS-STATIC-ENTRY'
    for path,expected in gate['code_sha256'].items():assert s.sha(s.ROOT/path)==expected,'code changed after static review'
    marker=s.ROOT/'PILOT_SINGLE_USE.json'
    with marker.open('x') as f:json.dump({'column_zero_based':2,'attempt':1,'static_gate_sha256':s.sha(s.ROOT/'static/STATIC_GATE.json'),'no_retry':True,'start_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},f)
    r=run([sys.executable,str(s.CODE/'v2_worker.py')],s.ROOT/'supervisor')
    print(json.dumps(r))
if __name__=='__main__':main()
