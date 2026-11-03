"""Run original full K integration with read-only mapped model-array storage.

No cells, phase operations, matrix accumulation order or weights are changed.
"""
import argparse,builtins,hashlib,json,re,sys
from pathlib import Path
import numpy as np
from disk_backed_storage import ArchiveMappings,evict


def progress_evictor(mapped,base_print,expected_cells=5120,stride=64):
    """Preserve progress output and discard only clean file-backed pages."""
    completed=[]
    def emit(*values,**kwargs):
        base_print(*values,**kwargs)
        if len(values)!=1 or not isinstance(values[0],str):return
        match=re.fullmatch(r'validated residual integration (\d+)/(\d+)',values[0])
        if match is None:return
        cell,total=map(int,match.groups())
        previous=completed[-1] if completed else 0
        if total!=expected_cells or cell!=previous+stride or cell>total:
            raise RuntimeError('Unexpected residual integration progress sequence')
        for array in mapped.arrays.values():evict(array)
        completed.append(cell)
    return emit,completed


def main(args):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    source=Path(args.source_dir).resolve()
    from producer_guard import verify_source
    verify_source(source)
    sys.path.insert(0,str(source))
    import verify_residual_gram as producer
    out=Path(args.output);scratch=Path(args.scratch)
    if out.exists() and any(out.iterdir()):raise FileExistsError('Refusing nonempty output')
    model_path=(Path(args.model)/'model.npz').resolve()
    mr=json.loads((Path(args.model)/'result.json').read_text())
    mapped=ArchiveMappings(model_path,scratch,mr['model_sha256'])
    old_load=np.load
    def load(file,*args_,**kwargs):
        if Path(file).resolve()==model_path:
            if args_ or kwargs:raise ValueError('Unexpected load signature')
            return mapped
        return old_load(file,*args_,**kwargs)
    np.load=load
    had_print='print' in producer.__dict__
    old_print=producer.__dict__.get('print',builtins.print)
    producer.print,evicted_cells=progress_evictor(mapped,old_print)
    try:producer.main(argparse.Namespace(candidate=args.candidate,model=args.model,output=args.output,weight_refinement=args.weight_refinement))
    finally:
        np.load=old_load
        if had_print:producer.print=old_print
        else:del producer.print
    if evicted_cells!=list(range(64,5121,64)):
        raise RuntimeError('Incomplete residual integration progress sequence')
    (out/'storage_adapter_identity.json').write_text(json.dumps({'storage_only_adapter':True,'source_bytes_modified':False,'source_producer_sha256':hashlib.sha256((source/'verify_residual_gram.py').read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'model_npz_sha256':mapped.sha256,'all_5120_cells_in_original_order':True,'arithmetic_unchanged':True,'clean_mapped_pages_evicted_after_cells':evicted_cells,'original_progress_print_preserved':True},indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['source-dir','candidate','model','output','scratch']:p.add_argument('--'+k,required=True)
    p.add_argument('--weight-refinement',type=int,default=16)
    main(p.parse_args())
