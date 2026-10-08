"""CC BY-NC 4.0. Single j=2 worker. Only external supervisor may launch it."""
import gc, json, os, pathlib, resource, signal, sys, time, traceback
import v2_support as s
class StopSignal(BaseException):pass
def stop(signum,frame):raise StopSignal('external SIGTERM at soft deadline')
def main():
    assert 'V2_SUPERVISOR_START' in os.environ and (s.ROOT/'PILOT_SINGLE_USE.json').exists()
    assert resource.getrlimit(resource.RLIMIT_AS)==(512*1024*1024,512*1024*1024)
    assert resource.getrlimit(resource.RLIMIT_CPU)==(600,600)
    s.START=float(os.environ['V2_SUPERVISOR_START']);signal.signal(signal.SIGTERM,stop)
    s.OUT.mkdir(parents=True,exist_ok=False)
    try:
        s.phase('guarded-backend-import')
        s.backend();import flint
        import v2_action as action, v2_nodes as nodes
        action.get_backend();nodes.get_backend()
        s.save(s.OUT/'RUNTIME_IDENTITY.json',{'python':sys.version,'python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,'precision_bits':s.ctx.prec,'threads':s.ctx.threads,'RLIMIT_AS':resource.getrlimit(resource.RLIMIT_AS),'RLIMIT_CPU':resource.getrlimit(resource.RLIMIT_CPU),'dependency_identity_sha256':s.sha(s.ROOT/'DEPENDENCY_IDENTITY.json')})
        s.phase('fixed-input-and-old-cache-preparation');fixed=s.load_fixed();facts=action.old_facts(fixed)
        frame_nums,frame_error=action.frame(fixed,facts)
        D,mult,terms=action.shared()
        desc,cert=action.produce(fixed,D,mult,frame_nums,frame_error)
        del D,mult,frame_nums;gc.collect();s.phase('producer-multiplier-polynomial-lifetimes-ended')
        nodes.polynomial_nodes(desc)
        nodes.integrate(fixed,facts,desc,cert,terms)
        s.save(s.OUT/'PILOT_STATUS.json',{'status':'PASS-PILOT-PENDING-INDEPENDENT-SAVED-CHECK','column_zero_based':2,'attempts':1,'B2':cert['B2'],'kernels':437,'other_residual_columns':0,'positivity_consumers':0,'counts':s.COUNTS,'last_completed_stage':s.PHASE,'wall_seconds':time.monotonic()-s.START,'CPU_seconds':time.process_time(),'memory':s.proc_memory(),'RH_or_delta64_proof':False})
    except BaseException as exc:
        status={'status':'HOLD','failure_stage':s.PHASE,'exception_type':type(exc).__name__,'reason':str(exc),'counts':s.COUNTS,'pilot_attempts':1,'retries':0,'other_residual_columns':0,'positivity_consumers':0,'wall_seconds':time.monotonic()-s.START,'CPU_seconds':time.process_time(),'memory':s.proc_memory(),'traceback':traceback.format_exc()}
        try:s.save(s.OUT/'PILOT_STATUS.json',status);print(json.dumps(status),flush=True)
        except BaseException:pass
        raise
if __name__=='__main__':main()
