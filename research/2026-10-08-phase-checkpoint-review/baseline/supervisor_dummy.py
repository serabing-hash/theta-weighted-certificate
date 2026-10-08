"""Source-free termination fixture only. No math imports."""
import json, os, pathlib, signal, time
signal.signal(signal.SIGTERM,signal.SIG_IGN)
child=os.fork()
if not child:
    (pathlib.Path(__file__).resolve().parents[1]/'static/supervisor_fixture/grandchild_pid.txt').write_text(json.dumps({'namespace_PID':os.getpid(),'procfs_PID':int(os.readlink('/proc/self'))}))
while True:time.sleep(.05)
