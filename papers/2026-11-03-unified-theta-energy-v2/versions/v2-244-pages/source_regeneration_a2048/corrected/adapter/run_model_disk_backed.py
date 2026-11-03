"""Storage-adapted execution of the unchanged residual-model producer.

Gamma arrays are hash-checked, streamed to read-only NPY mappings, phase buffers
are disk-backed, and the single huge Ball matrix product uses identical full-
shape arithmetic with disk-backed temporary outputs. No phase/cell splitting,
reassociation, changed quadrature, coefficient change, or widened radius occurs.
"""
import argparse,hashlib,inspect,json,sys
from pathlib import Path
import numpy as np
from disk_backed_storage import ArchiveMappings,FullShapeDiskArithmetic
from run_gamma_disk_backed import FlushedMemmap


def main(args):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    source=Path(args.source_dir).resolve()
    from producer_guard import verify_source
    verify_source(source)
    sys.path.insert(0,str(source))
    import validated_residual_model as producer
    from ball_array import Ball
    out=Path(args.output);scratch=Path(args.scratch)
    if out.exists() and any(out.iterdir()):raise FileExistsError('Refusing nonempty output')
    if scratch.exists() and any(scratch.iterdir()):raise FileExistsError('Refusing nonempty scratch')
    scratch.mkdir(parents=True,exist_ok=True)
    gamma_path=(Path(args.gamma)/'gamma_nodes.npz').resolve()
    gr=json.loads((Path(args.gamma)/'result.json').read_text())
    mapped=ArchiveMappings(gamma_path,scratch/'gamma_readonly',gr['raw_nodes_sha256'])
    shape=(gr['degree']+1,gr['cells'],256)
    assert shape==(33,5120,256)
    count=0;transform_calls=0;norm_calls=0;released=[]
    old_load,old_empty,old_empty_like,old_matmul=np.load,np.empty,np.empty_like,Ball.__matmul__
    old_norm=producer.norm_upper
    def load(file,*args_,**kwargs):
        if Path(file).resolve()==gamma_path:
            if args_ or kwargs:raise ValueError('Unexpected load signature')
            return mapped
        return old_load(file,*args_,**kwargs)
    def empty(request,dtype=float,order='C',**kwargs):
        nonlocal count
        request_shape=tuple(request) if not isinstance(request,int) else (request,)
        if request_shape==shape:
            if np.dtype(dtype)!=np.dtype('float64') or order!='C' or kwargs or count>=2:raise ValueError('Unexpected buffer allocation')
            if count==0:
                caller=inspect.currentframe().f_back
                if caller.f_code is not producer.main.__code__:raise RuntimeError('Unexpected model allocation caller')
                # raw, U/V, Jsum and Jmax have already been constructed. These
                # Fraction lists have no subsequent reads in the original main.
                for name in ['rows','jumps']:
                    values=caller.f_locals[name]
                    if not isinstance(values,list):raise TypeError('Expected completed Fraction list')
                    values.clear();released.append(name)
            p=scratch/('model_midpoint.npy' if count==0 else 'model_radius.npy');count+=1
            return np.lib.format.open_memmap(p,mode='w+',dtype='float64',shape=shape,fortran_order=False).view(FlushedMemmap)
        return old_empty(request,dtype=dtype,order=order,**kwargs)
    def empty_like(a,*args_,**kwargs):
        if tuple(a.shape)==shape and isinstance(a,FlushedMemmap):
            if args_ or kwargs:raise ValueError('Unexpected empty_like signature')
            return empty(shape,dtype=a.dtype)
        return old_empty_like(a,*args_,**kwargs)
    def matmul(left,right):
        nonlocal transform_calls
        if tuple(left.mid.shape)==(33,33) and isinstance(right,Ball) and tuple(right.mid.shape)==(33,5120*256):
            if transform_calls:raise RuntimeError('Unexpected repeated huge transform')
            transform_calls+=1
            disk=FullShapeDiskArithmetic(scratch/'coefficient_transform')
            return disk.ball_matmul(left,right)
        return old_matmul(left,right)
    def norm_upper(a,axis=None):
        nonlocal norm_calls
        if tuple(a.shape)==(5120,33,256) and axis==2:
            if norm_calls:raise RuntimeError('Unexpected repeated huge norm')
            norm_calls+=1
            return FullShapeDiskArithmetic(scratch/'node_error_norm').norm_upper(a,axis)
        return old_norm(a,axis)
    np.load,np.empty,np.empty_like,Ball.__matmul__=load,empty,empty_like,matmul
    producer.norm_upper=norm_upper
    try:producer.main(argparse.Namespace(candidate=args.candidate,gamma=args.gamma,output=args.output))
    finally:
        np.load,np.empty,np.empty_like,Ball.__matmul__=old_load,old_empty,old_empty_like,old_matmul
        producer.norm_upper=old_norm
    assert count==2 and transform_calls==1 and norm_calls==1
    (out/'storage_adapter_identity.json').write_text(json.dumps({'storage_only_adapter':True,'source_bytes_modified':False,'source_producer_sha256':hashlib.sha256((source/'validated_residual_model.py').read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256((Path(__file__).parent/'disk_backed_storage.py').read_bytes()).hexdigest(),'gamma_npz_sha256':mapped.sha256,'phase_output_buffers':'C-order float64 memmaps','full_shape_transform_calls':transform_calls,'same_layout_full_shape_norm_calls':norm_calls,'unused_fraction_lists_released_before_phases':released,'scientific_operation_sequence_and_shapes_unchanged':True,'arithmetic_and_output_identity_requires_external_comparison':True},indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['source-dir','candidate','gamma','output','scratch']:p.add_argument('--'+k,required=True)
    main(p.parse_args())
