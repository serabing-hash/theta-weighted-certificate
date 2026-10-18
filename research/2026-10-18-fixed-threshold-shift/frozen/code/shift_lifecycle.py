"""Registered single-fork lifecycle; trusted control code, not a native sandbox.

No procfs task/children enumeration. Every production birth is the return value
of our sole fork; the parent seals NPROC before releasing its blocked child.
All syscalls and identity reads fail closed. This module performs no work on
import beyond definitions and stdlib imports. Preparation never executes it.
"""
import errno
import json
import os
from pathlib import Path
import resource
import select
import signal
import time

PROTOCOL='REGISTERED_FORK_NPROC_PIDFD_ECHILD_V1'
WALL=0x40000000  # Linux __WALL: include clone and ordinary child processes.
RELEASE=b'BOUND-CHILD-RELEASE\n'


def need(ok,message):
    if not ok: raise RuntimeError(message)


def fields(pid):
    return dict(line.split(':',1) for line in Path('/proc',str(pid),'status').read_text().splitlines() if ':' in line)


def unprivileged(pid):
    row=fields(pid)
    uid=list(map(int,row['Uid'].split()))
    need(uid==[os.getuid()]*4 and uid[0]!=0,'unchanged nonroot credentials required')
    for key in ('CapEff','CapPrm','CapInh','CapAmb','CapBnd'):
        need(int(row[key],16)==0,'capability-free control identity required: '+key)
    need(int(row['NoNewPrivs'])==1,'inherited NoNewPrivs required; no environment repair')
    return row


def seal():
    unprivileged(os.getpid())
    resource.setrlimit(resource.RLIMIT_NPROC,(0,0))
    require_sealed(os.getpid())


def require_sealed(pid):
    unprivileged(pid)
    limits=resource.getrlimit(resource.RLIMIT_NPROC) if pid==os.getpid() else resource.prlimit(pid,resource.RLIMIT_NPROC)
    need(limits==(0,0),'NPROC soft/hard zero required')


def prctl(option,value):
    import ctypes
    libc=ctypes.CDLL(None,use_errno=True)
    libc.prctl.argtypes=[ctypes.c_int,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_ulong]
    libc.prctl.restype=ctypes.c_int
    if libc.prctl(option,value,0,0,0)!=0:
        err=ctypes.get_errno(); raise OSError(err,os.strerror(err),'prctl')
    # Both settings used here have a get operation with an int* argument.
    get_option={1:2,36:37}[option]
    result=ctypes.c_int()
    if libc.prctl(get_option,ctypes.addressof(result),0,0,0)!=0:
        err=ctypes.get_errno(); raise OSError(err,os.strerror(err),'prctl get')
    need(result.value==value,'prctl readback mismatch')


def assert_no_children():
    """ECHILD only. A zero return means a child exists, not an empty tree.

    Requires SIGCHLD DFL, no SA_NOCLDWAIT, no competing waiter, and a sealed
    trusted single-thread caller. Unexpected waitable children are reaped but
    still force HOLD; this function never quietly drains them to success.
    """
    try:
        pid,status,usage=os.wait4(-1,os.WNOHANG|WALL)
    except ChildProcessError as exc:
        need(exc.errno==errno.ECHILD,'unexpected wait4 error')
        return
    raise RuntimeError('unexpected child remains: '+str(pid)+' (zero means live/nonwaitable)')


def prepare_parent(cpu,subreaper=False):
    need(hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal') and hasattr(resource,'prlimit'),
         'pidfd/prlimit required')
    need(os.readlink('/proc/self')==str(os.getpid()),'flat procfs required')
    unprivileged(os.getpid())
    need(len(list(Path('/proc/self/task').iterdir()))==1,'single-thread parent required')
    need(os.sched_getaffinity(0)=={cpu},'single shared CPU required')
    # CPython signal.signal installs a new disposition with no SA_NOCLDWAIT.
    # No library or signal handler is allowed to reap behind this owner.
    signal.signal(signal.SIGCHLD,signal.SIG_DFL)
    if subreaper: prctl(36,1)
    assert_no_children()


def shape(pid,cpu,parent,start=None,sealed=False):
    base=Path('/proc',str(pid))
    stat=(base/'stat').read_text().rsplit(')',1)[1].split()
    row=unprivileged(pid)
    need(int(row['Pid'])==int(row['Tgid'])==pid and list(map(int,row['NSpid'].split()))==[pid],
         'PID/TID/namespace identity changed')
    need(int(stat[1])==int(row['PPid'])==parent,'unexpected reparenting')
    ticks=int(stat[19])
    if start is not None: need(ticks==start,'process starttime changed')
    if stat[0]!='Z':
        need(len(list((base/'task').iterdir()))==1 and int(row['Threads'])==1,'extra thread')
        need(os.sched_getaffinity(pid)=={cpu},'CPU affinity changed')
        if sealed: require_sealed(pid)
    return {'pid':pid,'parent_pid':parent,'start_ticks':ticks,'state':stat[0],
            'cpu_ticks':int(stat[11])+int(stat[12]),
            'rss_kib':int(row.get('VmRSS','0 kB').split()[0]),
            'hwm_kib':int(row.get('VmHWM','0 kB').split()[0])}


def ready(fd):
    return bool(select.select([fd],[],[],0)[0])


def read_line(fd,deadline):
    data=b''
    while not data.endswith(b'\n'):
        remaining=(deadline-time.monotonic_ns())/1_000_000_000
        need(remaining>0,'handshake deadline')
        if select.select([fd],[],[],min(0.01,remaining))[0]:
            part=os.read(fd,4096); need(part,'child/parent exited during handshake')
            data+=part; need(len(data)<=4096,'handshake length')
    need(data.count(b'\n')==1,'multiple handshake packets')
    return data


class Child:
    """One direct, unreaped child. Keep PID ownership until wait4 returns it."""
    def __init__(self,pid,cpu,parent):
        self.pid=pid; self.cpu=cpu; self.parent=parent
        self.fd=None; self.start=None; self.release_fd=None
        self.reaped=False; self.status=None; self.usage=None; self.sealed=False
    def bind(self,sealed=False):
        need(not self.reaped and self.fd is None,'duplicate/dead child binding')
        self.fd=os.pidfd_open(self.pid,0)
        row=shape(self.pid,self.cpu,self.parent)
        self.start=row['start_ticks']; self.sealed=sealed
        return row
    def sample(self):
        need(not self.reaped,'no numeric PID reads after reap')
        return shape(self.pid,self.cpu,self.parent,self.start,self.sealed)
    def release(self):
        need(self.release_fd is not None and not self.reaped and not ready(self.fd),'dead/already released child')
        row=self.sample(); need(row['state']!='Z','zombie child cannot be released')
        need(os.write(self.release_fd,RELEASE)==len(RELEASE),'release pipe write')
        os.close(self.release_fd); self.release_fd=None
    def poll(self):
        need(not self.reaped,'duplicate wait4')
        done,st,usage=os.wait4(self.pid,os.WNOHANG)
        if done:
            need(done==self.pid,'wrong wait4 child')
            self.reaped=True; self.status=st; self.usage=usage
            return done,st,usage
        return 0,0,None
    def kill(self):
        if self.reaped: return
        try:
            if self.fd is not None: signal.pidfd_send_signal(self.fd,signal.SIGKILL)
            else: os.kill(self.pid,signal.SIGKILL)  # Our own unreaped child only.
        except ProcessLookupError: pass
    def reap_until(self,deadline):
        while not self.reaped and time.monotonic_ns()<deadline:
            if self.poll()[0]: break
            select.select([self.fd] if self.fd is not None else [],[],[],0.001)
        return self.reaped
    def record(self):
        return {'pid':self.pid,'parent_pid':self.parent,'start_ticks':self.start,
                'pidfd_bound':self.fd is not None,'reaped':self.reaped,
                'sealed_child_before_release':self.sealed}


def fork_one(cpu,deadline,child_main,child_limits=None):
    """The only production fork. Returns a bound, ready, unreleased Child.

    child_main is a reviewed control stub, invoked only after parent release.
    Parents call once; NPROC(0,0) makes a second birth fail at the kernel.
    For the scientific leaf, AS/CPU/NPROC are set before its READY and exec.
    """
    release_r,release_w=os.pipe(); ready_r,ready_w=os.pipe()
    owner=os.getpid(); pid=os.fork()
    if pid==0:
        try:
            os.close(release_w); os.close(ready_r)
            signal.signal(signal.SIGALRM,signal.SIG_DFL)
            left=(deadline-time.monotonic_ns())/1_000_000_000
            need(left>0,'child inherited deadline expired'); signal.setitimer(signal.ITIMER_REAL,left)
            prctl(1,signal.SIGKILL); need(os.getppid()==owner,'parent died before child registration')
            if child_limits is not None:
                resource.setrlimit(resource.RLIMIT_AS,(child_limits['as_bytes'],)*2)
                resource.setrlimit(resource.RLIMIT_CPU,(child_limits['cpu_seconds'],)*2)
                resource.setrlimit(resource.RLIMIT_CORE,(0,0)); seal()
            row=shape(os.getpid(),cpu,owner,sealed=child_limits is not None)
            packet=json.dumps({'pid':row['pid'],'parent_pid':owner,'start_ticks':row['start_ticks'],
                               'sealed':child_limits is not None},separators=(',',':')).encode()+b'\n'
            need(os.write(ready_w,packet)==len(packet),'child READY write'); os.close(ready_w)
            need(read_line(release_r,deadline)==RELEASE,'child release binding'); os.close(release_r)
            need(os.getppid()==owner,'parent disappeared before child action')
            result=child_main(); os._exit(0 if result is None else result)
        except BaseException: os._exit(127)
    child=Child(pid,cpu,owner); child.release_fd=release_w
    os.close(release_r); os.close(ready_w)
    try:
        seal()  # The child inherited the pre-seal rlimit at fork.
        child.bind(sealed=child_limits is not None)
        packet=json.loads(read_line(ready_r,deadline)); os.close(ready_r); ready_r=None
        need(packet=={'pid':pid,'parent_pid':owner,'start_ticks':child.start,
                      'sealed':child_limits is not None},'child READY identity mismatch')
        need(child.sample()['state']!='Z','child exited before release')
        return child
    except BaseException:
        child.kill(); child.reap_until(deadline)
        if ready_r is not None: os.close(ready_r)
        if child.release_fd is not None: os.close(child.release_fd)
        raise


def remote_sample(pidfd,pid,cpu,parent,start,sealed=False):
    """A non-owner may read a PID only while the pidfd stays nonterminal.

    Discard the entire numeric-PID sample if exit occurs during the reads.
    This avoids accepting another process after the direct parent reaps it.
    """
    if ready(pidfd): return None
    try: row=shape(pid,cpu,parent,start,sealed)
    except (OSError,RuntimeError):
        if ready(pidfd): return None
        raise
    if ready(pidfd): return None
    return row


def cleanup(owned,deadline):
    """Best effort within the same deadline. Never turns a failed run into GO."""
    for child in owned:
        if child is not None: child.kill()
    for child in owned:
        if child is not None: child.reap_until(deadline)
    adopted=[]
    while time.monotonic_ns()<deadline:
        try: pid,st,usage=os.wait4(-1,os.WNOHANG|WALL)
        except ChildProcessError as exc:
            need(exc.errno==errno.ECHILD,'cleanup wait error')
            return {'closed':True,'adopted_reaped':adopted}
        if pid: adopted.append({'pid':pid,'status':st})
        else: select.select([],[],[],0.001)
    return {'closed':False,'adopted_reaped':adopted,'reason':'same deadline exhausted'}
