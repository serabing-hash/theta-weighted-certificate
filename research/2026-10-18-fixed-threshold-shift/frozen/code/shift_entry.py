"""One scientific worker, invoked only by the explicit timed launcher.

This file has no CLI that directly runs a consumer without inherited admission.
"""
import gc
import os
from pathlib import Path
import resource
import sys
import time


def main():
    admission=getattr(sys,'_shift_source_admission',None)
    if not admission or admission['role']!='entry' or admission['source_only'] is not True:
        raise RuntimeError('verified source-only bootstrap required before local imports')
    from shift_exact import require,read,sha,save
    import shift_lifecycle as life
    require(len(sys.argv)==1 and sys.flags.isolated and sys.flags.no_site and not sys.flags.optimize, 'isolated entry invocation')
    require(os.environ.get('SHIFT_RELEASED')==os.environ.get('SHIFT_LAUNCH_ID') and
            os.environ.get('SHIFT_RELEASED'), 'parent release is absent')
    epoch=int(os.environ['SHIFT_EPOCH_NS']); controller=int(os.environ['SHIFT_CONTROLLER_PID'])
    cpu=int(os.environ['SHIFT_CPU']); plan_path=Path(os.environ['SHIFT_PLAN'])
    require(sha(plan_path)==os.environ['SHIFT_PLAN_SHA256'], 'plan admission bytes')
    plan=read(plan_path); attempt=Path(plan['attempt_root'])
    require(plan['tree_protocol']==life.PROTOCOL,'registered tree protocol')
    life.prepare_parent(cpu)
    require(plan['limits']=={'wall_seconds':60,'tree_cpu_seconds':60,'worker_as_bytes':402653184,
            'worker_rss_kib':327680,'threads':1,'scientific_workers':1,'poll_seconds':0.01}, 'frozen resource contract')
    require(resource.getrlimit(resource.RLIMIT_AS)==(402653184,402653184), '384MiB AS hard cap')
    require(resource.getrlimit(resource.RLIMIT_CPU)==(60,60), 'worker CPU fallback cap')
    require(resource.getrlimit(resource.RLIMIT_NPROC)==(0,0), 'no worker descendant/thread creation')
    require(os.getuid()!=0, 'NPROC root bypass is excluded')
    status=dict(line.split(':',1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
    caps=int(status['CapEff'].strip(),16)
    require(caps & ((1<<21)|(1<<24))==0, 'NPROC privilege bypass is excluded')
    def guard():
        require(0<time.monotonic_ns()-epoch<60_000_000_000, 'shared60second wall')
        require(os.getppid()==controller, 'controller disappeared')
        require(os.sched_getaffinity(0)=={cpu}, 'worker affinity changed')
        require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<=327680, '320MiB worker RSS/HWM')
        require(resource.getrlimit(resource.RLIMIT_AS)==(402653184,402653184), 'AS cap changed')
        require(resource.getrlimit(resource.RLIMIT_NPROC)==(0,0), 'NPROC cap changed')
        require(len(list(Path('/proc/self/task').iterdir()))==1, 'single worker thread')
        life.require_sealed(os.getpid()); life.assert_no_children()
    guard()
    code=Path(plan['code_root'])
    for name,h in plan['code_sha256'].items():
        require(sha(code/name)==h, 'code admission '+name); guard()
    require(Path(__file__).resolve()==code/'shift_entry.py', 'bound entry path')
    require(sha(plan['input_manifest'])==plan['input_manifest_sha256']==os.environ['SHIFT_INPUT_SHA256'],
            'input manifest admission')
    def audit(event,args):
        if event in {'os.fork','os.forkpty','os.exec','os.posix_spawn','subprocess.Popen',
                     'socket.__new__','socket.connect'}:
            raise RuntimeError('forbidden worker process/network event '+event)
    sys.addaudithook(audit)
    try:
        from shift_runtime import import_runtime
        import_runtime(plan,attempt/'RUNTIME_IDENTITY.json',guard)
        from shift_driver import run as produce
        produce(plan['source_root'],plan['input_manifest'],attempt/'math',guard)
        gc.collect(); guard()
        # Independent implementation: imports no producer/helper/native modules.
        # Existing native mappings remain in this same worker process.
        from shift_checker import run as check
        report=check(plan['source_root'],plan['input_manifest'],attempt/'math',guard)
        guard()
        for name,h in plan['code_sha256'].items(): require(sha(code/name)==h,'code unchanged '+name)
        require(sha(plan_path)==os.environ['SHIFT_PLAN_SHA256'],'plan unchanged')
        save(attempt/'WORKER_RESULT.json',{'status':'MATH-COMPLETE-RESOURCE-GATE-PENDING',
             'scope':plan['scope'],'plan_sha256':sha(plan_path),'input_manifest_sha256':plan['input_manifest_sha256'],
             'checker_sha256':sha(code/'shift_checker.py'),
             'check_report_sha256':sha(attempt/'math/INDEPENDENT_CHECK.json'),
             'report_status':report['status'],'worker_pid':os.getpid(),'controller_pid':controller,
             'native_import_timed':True,'physical_producer_calls':0,'coefficient_solves':0,
             'independent_checker_passes':1,'source_only_import_events':admission['events'],
             'RH_PROOF':'NOT-OBTAINED'})
        guard(); return 0
    except Exception as exc:
        # Audit only. Partial mathematical files are retained, with no restart.
        try: save(attempt/'WORKER_FAILURE.json',{'status':'HOLD','reason':str(exc),
                  'exception_type':type(exc).__name__,'automatic_retry':False})
        except Exception: pass
        return 2


if __name__=='__main__':
    raise SystemExit(main())
