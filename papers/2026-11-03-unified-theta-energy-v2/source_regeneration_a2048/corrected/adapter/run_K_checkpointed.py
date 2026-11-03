"""Original full K loop with mapped storage and atomic exact-prefix checkpoints.

Fresh runs begin at cell0. Resume is possible only from complete, hash-bound
state produced by this adapter, never from logs. Module-local range interception
restores the original K/list objects at their zero-state initialization boundary;
all subsequent original cell bodies and floating accumulation order are intact.
"""
import argparse,builtins,contextlib,hashlib,inspect,io,json,os,platform,re,sys
from pathlib import Path
import numpy as np
from disk_backed_storage import ArchiveMappings,evict,sha256_file
from k_prefix_checkpoint import PrefixStore,restore_objects
from producer_guard import verify_source


def arithmetic_environment():
    import scipy,mpmath,decimal
    context=decimal.getcontext()
    context_record={k:getattr(context,k) for k in ["prec","rounding","Emin","Emax","capitals","clamp"]}
    context_record["traps"]={signal.__name__:bool(value) for signal,value in context.traps.items()}
    def config_hash(module):
        text=io.StringIO()
        with contextlib.redirect_stdout(text):module.__config__.show()
        return hashlib.sha256(text.getvalue().encode()).hexdigest()
    from numpy._core import _multiarray_umath as cpu
    thread_keys=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS','NPY_DISABLE_CPU_FEATURES']
    threads={k:os.environ.get(k) for k in thread_keys}
    if threads['OPENBLAS_NUM_THREADS']!='1':raise ValueError('OPENBLAS_NUM_THREADS must be exactly 1')
    cpu_records=[]
    cpuinfo=Path('/proc/cpuinfo')
    if cpuinfo.exists():
        wanted={'vendor_id','cpu family','model','model name','stepping','flags'}
        for block in cpuinfo.read_text().split('\n\n'):
            fields={}
            for line in block.splitlines():
                if ':' in line:
                    key,value=line.split(':',1)
                    if key.strip() in wanted:fields[key.strip()]=value.strip()
            if fields and fields not in cpu_records:cpu_records.append(fields)
    record={'numpy_build_blas_config_sha256':config_hash(np),'scipy_build_blas_config_sha256':config_hash(scipy),'numpy_cpu_features':dict(cpu.__cpu_features__),'numpy_cpu_baseline':list(cpu.__cpu_baseline__),'numpy_cpu_dispatch':list(cpu.__cpu_dispatch__),'cpu_static_records_sha256':hashlib.sha256(json.dumps(cpu_records,sort_keys=True).encode()).hexdigest(),'cpu_static_records_available':bool(cpu_records),'thread_environment':threads,'machine':platform.machine(),'byteorder':sys.byteorder}
    record['versions']={'python':platform.python_version(),'implementation':platform.python_implementation(),'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__,'decimal':decimal.__version__,'libmpdec':decimal.__libmpdec_version__}
    record['decimal_context']=context_record
    record['decimal_status_flags_excluded_because_they_are_outputs']=True
    record['numpy_error_policy']=np.geterr()
    record['digest']=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return record

def main(args):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    source=Path(args.source_dir).resolve();source_hashes=verify_source(source);sys.path.insert(0,str(source))
    import scipy,mpmath,verify_residual_gram as producer
    frozen=Path(args.candidate);model=Path(args.model);out=Path(args.output)
    if out.exists() and any(out.iterdir()):raise FileExistsError('Refusing nonempty output')
    packet=json.loads((frozen/'candidate.json').read_text());mr=json.loads((model/'result.json').read_text())
    candidate=sha256_file(frozen/'candidate.json')
    if candidate!='a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d' or mr['candidate_sha256']!=candidate or mr['status']!='CERT':raise ValueError('Unexpected source identity')
    if (packet['k'],packet['h'],packet['a'],packet['B'],mr['cells'],mr['degree'],args.weight_refinement)!=(256,'1/2560','1/2048','log(8)/2',5120,32,16):raise ValueError('Unexpected fixed configuration')
    input_paths={'candidate':frozen/'candidate.json','components':frozen/'verified_components.json','geometry':frozen/'geometry.json','source_geometry':frozen/'source_geometry.npz','model_result':model/'result.json','model_npz':model/'model.npz'}
    binding={'candidate_sha256':candidate,'input_sha256':{k:sha256_file(p) for k,p in input_paths.items()},'source_sha256':source_hashes,'adapter_sha256':sha256_file(__file__),'checkpoint_helper_sha256':sha256_file(Path(__file__).with_name('k_prefix_checkpoint.py')),'storage_helper_sha256':sha256_file(Path(__file__).with_name('disk_backed_storage.py')),'source_guard_sha256':sha256_file(Path(__file__).with_name('producer_guard.py')),'weight_refinement':16,'k':256,'cells':5120,'degree':32,'h':'1/2560','a':'1/2048','B':'log(8)/2','arithmetic_environment':arithmetic_environment(),'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__}}
    store=PrefixStore(args.checkpoints,binding)
    prefix=store.latest(required=args.resume)
    if prefix is not None and not args.resume:raise FileExistsError('Committed prefix exists; use --resume explicitly')
    start=0 if prefix is None else prefix['completed_cells']
    model_path=(model/'model.npz').resolve();mapped=ArchiveMappings(model_path,args.scratch,mr['model_sha256'])
    old_load=np.load;had_range='range' in producer.__dict__;old_range=producer.__dict__.get('range',builtins.range);had_print='print' in producer.__dict__;old_print=producer.__dict__.get('print',builtins.print)
    loop_calls=0;completed=[]
    def load(file,*argv,**kwargs):
        if Path(file).resolve()==model_path:
            if argv or kwargs:raise ValueError('Unexpected load signature')
            return mapped
        return old_load(file,*argv,**kwargs)
    def source_range(*values):
        nonlocal loop_calls
        caller=inspect.currentframe().f_back
        if caller.f_code is producer.main.__code__ and values==(5120,):
            if loop_calls:raise RuntimeError('Unexpected repeated outer cell loop')
            loop_calls+=1
            if restore_objects(caller.f_locals,prefix,256)!=start:raise ValueError('Wrong restored next cell')
            return builtins.range(start,5120)
        return old_range(*values)
    def emit(*values,**kwargs):
        old_print(*values,**kwargs)
        if len(values)!=1 or not isinstance(values[0],str):return
        match=re.fullmatch(r'validated residual integration (\d+)/(\d+)',values[0])
        if match is None:return
        cell,total=map(int,match.groups());previous=completed[-1] if completed else start
        if total!=5120 or cell!=previous+64 or cell>5120:raise RuntimeError('Invalid cell progress sequence')
        caller=inspect.currentframe().f_back
        if caller.f_code is not producer.main.__code__ or caller.f_locals['cell']+1!=cell:raise RuntimeError('Progress not bound to actual loop state')
        local=caller.f_locals
        store.save(cell,local['K'],local['weights_saved'],local['cell_trace'])
        for array in mapped.arrays.values():evict(array)
        completed.append(cell)
    np.load=load;producer.range=source_range;producer.print=emit
    try:producer.main(argparse.Namespace(candidate=args.candidate,model=args.model,output=args.output,weight_refinement=16))
    finally:
        np.load=old_load
        if had_range:producer.range=old_range
        else:del producer.range
        if had_print:producer.print=old_print
        else:del producer.print
    if loop_calls!=1 or completed!=list(builtins.range(start+64,5121,64)):raise RuntimeError('Incomplete ordered K execution')
    final_helpers={'adapter_sha256':Path(__file__),'checkpoint_helper_sha256':Path(__file__).with_name('k_prefix_checkpoint.py'),'storage_helper_sha256':Path(__file__).with_name('disk_backed_storage.py'),'source_guard_sha256':Path(__file__).with_name('producer_guard.py')}
    if any(sha256_file(p)!=binding[k] for k,p in final_helpers.items()):raise RuntimeError('Adapter/helper file changed during execution')
    if any(sha256_file(p)!=binding['input_sha256'][k] for k,p in input_paths.items()):raise RuntimeError('Bound input changed during execution')
    if verify_source(source)!=binding['source_sha256']:raise RuntimeError('Producer source changed during execution')
    if arithmetic_environment()!=binding['arithmetic_environment']:raise RuntimeError('Arithmetic execution environment changed')
    record={'status':'COMPLETED','source_bytes_modified':False,'original_loop_body_and_accumulation_order_unchanged':True,'binding_sha256':store.binding_sha256,'binding':binding,'resumed_from_completed_cells':start,'restored_manifest_sha256':None if prefix is None else prefix['manifest_sha256'],'new_committed_boundaries':completed,'old_log_progress_used_as_state':False,'storage_only_adaptation':True,'final_checkpoint':store.latest(required=True)['manifest_sha256']}
    (out/'checkpoint_adapter_identity.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['source-dir','candidate','model','output','scratch','checkpoints']:p.add_argument('--'+k,required=True)
    p.add_argument('--weight-refinement',type=int,default=16);p.add_argument('--resume',action='store_true');main(p.parse_args())
