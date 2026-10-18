"""Verified-source bootstrap. Only stdlib imports precede local admission.

Invoke through the frozen inline trampoline in START_COMMAND.json. The trampoline
hashes the exact bytes it compiles; it never invokes normal local-module import.
No bytecode cache is read or written for the bound local modules below.
"""
import hashlib
import importlib.abc
import importlib.util
import json
import os
from pathlib import Path
import resource
import signal
import sys
import time
import types

TRAMPOLINE = "import hashlib,pathlib,sys\np=pathlib.Path(sys.argv[1])\nb=p.read_bytes()\nif hashlib.sha256(b).hexdigest()!=sys.argv[2]: raise RuntimeError('bootstrap source hash mismatch')\nsys.argv=[str(p),*sys.argv[3:]]\nexec(compile(b,str(p),'exec',dont_inherit=True,optimize=0),{'__name__':'__main__','__file__':str(p)})"


def need(ok,label):
    if not ok: raise RuntimeError(label)


def load_json_bytes(data):
    def unique(items):
        result={}
        for k,v in items: need(k not in result,'duplicate JSON key'); result[k]=v
        return result
    return json.loads(data,object_pairs_hook=unique)


def persist_epoch(attempt,record):
    # Directory existence is the authoritative one-use mark, even if this
    # record is incomplete. No error path removes the mark or permits retry.
    data=(json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
    parent_fd=os.open(attempt.parent,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(parent_fd)
    finally: os.close(parent_fd)
    with (attempt/'OBSERVER_EPOCH.json').open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    need((attempt/'OBSERVER_EPOCH.json').read_bytes()==data,'bootstrap epoch readback')
    directory_fd=os.open(attempt,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(directory_fd)
    finally: os.close(directory_fd)


class BoundSource(importlib.abc.MetaPathFinder,importlib.abc.Loader):
    def __init__(self,root,sources,hashes,events):
        self.root=root; self.sources=sources; self.hashes=hashes; self.events=events
    def find_spec(self,fullname,path=None,target=None):
        if fullname.startswith('shift_') or fullname=='source_bootstrap':
            need(fullname in self.sources,'unbound local module rejected: '+fullname)
            return importlib.util.spec_from_loader(fullname,self,origin=str(self.root/(fullname+'.py')))
        return None
    def create_module(self,spec): return None
    def exec_module(self,module):
        name=module.__spec__.name; data=self.sources[name]
        need(hashlib.sha256(data).hexdigest()==self.hashes[name+'.py'],'snapshot hash')
        module.__file__=str(self.root/(name+'.py')); module.__cached__=None
        module.__package__=''
        self.events.append({'module':name,'sha256':self.hashes[name+'.py'],'mechanism':'verified-bytes-compile-exec'})
        exec(compile(data,module.__file__,'exec',dont_inherit=True,optimize=0),module.__dict__)


def main():
    need(len(sys.argv)==4,'bootstrap role, plan and plan hash required')
    role,plan_name,expected=sys.argv[1:]
    need(role in {'observer','launcher','entry'},'unbound main role')
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and not sys.flags.optimize,
         'require -I -S -B without optimization')
    need(not any(os.environ.get(k) for k in ('LD_PRELOAD','LD_LIBRARY_PATH','PYTHONPATH')),'injected path')
    plan_path=Path(plan_name).resolve(); plan_bytes=plan_path.read_bytes()
    need(hashlib.sha256(plan_bytes).hexdigest()==expected,'plan hash')
    plan=load_json_bytes(plan_bytes); root=Path(plan['code_root']).resolve()
    need(Path(__file__).resolve()==root/'source_bootstrap.py','bootstrap path binding')
    need(not any(n.startswith('shift_') or n=='source_bootstrap' for n in sys.modules),'local module preloaded')
    cpu=plan['cpu_affinity']; need(cpu in os.sched_getaffinity(0),'CPU unavailable')
    os.sched_setaffinity(0,{cpu})
    if role=='observer':
        attempt=Path(plan['attempt_root'])
        need(not attempt.exists(),'single attempt already consumed')
        print(json.dumps({'status':'READY-NO-SCIENCE','plan_sha256':expected,
                          'required_stdin':'BEGIN '+expected}),flush=True)
        need(sys.stdin.readline().strip()=='BEGIN '+expected,'explicit BEGIN absent')
        epoch=time.monotonic_ns()
        # FIRST filesystem operation after accepting BEGIN. Atomic exclusive
        # mkdir consumes the attempt before limits, hashing or local loading.
        # Even an empty/partial directory permanently blocks the same command.
        attempt.mkdir(mode=0o700,exist_ok=False)
        baseline=time.process_time_ns()
        os.environ.update(SHIFT_EPOCH_NS=str(epoch),SHIFT_OBSERVER_CPU_BASELINE_NS=str(baseline),
                          SHIFT_OBSERVER_PID=str(os.getpid()),SHIFT_PLAN_SHA256=expected)
    else:
        epoch=int(os.environ['SHIFT_EPOCH_NS'])
        need(os.environ.get('SHIFT_PLAN_SHA256')==expected,'inherited plan admission')
        need(os.environ.get('SHIFT_OBSERVER_PID'),'external observer absent')
    remaining=epoch+60_000_000_000-time.monotonic_ns()
    need(remaining>0,'expired epoch before local admission')
    # Remains armed until this process exits. Observer/controller replace the
    # handler with tree-aware killing, but never move the absolute deadline.
    signal.signal(signal.SIGALRM,signal.SIG_DFL)
    signal.setitimer(signal.ITIMER_REAL,remaining/1_000_000_000)
    resource.setrlimit(resource.RLIMIT_AS,(402653184,402653184))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    def guard():
        need(time.monotonic_ns()<epoch+60_000_000_000,'source admission deadline')
        need(os.sched_getaffinity(0)=={cpu},'source admission affinity')
    if role=='observer':
        persist_epoch(attempt,{'t0_ns':epoch,'plan_sha256':expected,
                'launch_id':plan['launch_id'],'observer_pid':os.getpid(),
                'whole_attempt_seconds':60,'automatic_retry':False,
                'created_by':'source_bootstrap','consumed_before_source_admission':True,
                'consumption_authority':'exclusive_attempt_directory'})
    guard()
    need(hashlib.sha256(Path(sys.executable).resolve().read_bytes()).hexdigest()==plan['python_sha256'],
         'interpreter bytes')
    sources={}
    for filename,digest in plan['code_sha256'].items():
        need(Path(filename).name==filename and filename.endswith('.py') and filename[:-3].isidentifier(),
             'flat source-only manifest')
        p=root/filename; need(not p.is_symlink() and p.resolve().is_relative_to(root),'source path escape')
        data=p.read_bytes(); need(hashlib.sha256(data).hexdigest()==digest,'source bytes '+filename)
        sources[filename[:-3]]=data; guard()
    need('source_bootstrap' in sources and
         hashlib.sha256(sources['source_bootstrap']).hexdigest()==plan['code_sha256']['source_bootstrap.py'],
         'bootstrap included in source manifest')
    # No SourceFileLoader/get_code/set_data/cache fallback is used.
    events=[]; finder=BoundSource(root,sources,plan['code_sha256'],events)
    sys.meta_path.insert(0,finder); sys.dont_write_bytecode=True
    sys.path[:]=[p for p in sys.path if p and Path(p).resolve()!=root and Path(p).resolve()!=Path.cwd()]
    def argv_for(child_role):
        need(child_role in {'launcher','entry'},'unsupported child role')
        return [sys.executable,'-I','-S','-B','-c',TRAMPOLINE,str(root/'source_bootstrap.py'),
                plan['code_sha256']['source_bootstrap.py'],child_role,str(plan_path),expected]
    sys._shift_source_admission={'role':role,'plan_sha256':expected,'hashes':dict(plan['code_sha256']),
                                'events':events,'argv_for':argv_for,'finder':finder,
                                'source_only':True,'epoch_ns':epoch}
    main_name='shift_'+role
    need(main_name in sources,'main role source absent')
    module=types.ModuleType('__main__'); module.__file__=str(root/(main_name+'.py'))
    module.__package__=''; module.__cached__=None
    sys.modules['__main__']=module
    sys.argv=[module.__file__] if role=='entry' else [module.__file__,'--execute-once','--plan',str(plan_path),
                                                  '--expected-plan-sha256',expected]
    events.append({'module':'__main__:'+main_name,'sha256':plan['code_sha256'][main_name+'.py'],
                   'mechanism':'verified-bytes-compile-exec'})
    guard()
    exec(compile(sources[main_name],module.__file__,'exec',dont_inherit=True,optimize=0),module.__dict__)


if __name__=='__main__': main()
