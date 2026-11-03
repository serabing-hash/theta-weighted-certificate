"""Storage-only wrapper for the unchanged Gamma producer on limited-memory hosts.

The two output buffers use C-order float64 memmaps. Completed initial source
containers and consumed CRT/residue buffers are released after their last use.
All arithmetic, phase order, quantization, NTT/CRT and output serialization
remain the reviewed producer; an early source hash guard pins those lifetimes.
Completed output rows are flushed before dropping file-backed resident pages.
"""
import argparse,gc,hashlib,importlib.util,inspect,json,mmap,sys
from pathlib import Path
import numpy as np

class FlushedMemmap(np.memmap):
    def __setitem__(self,key,value):
        super().__setitem__(key,value)
        self.flush()
        if hasattr(self._mmap,'madvise'):
            self._mmap.madvise(mmap.MADV_DONTNEED)

def main(args):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    source=Path(args.source_dir).resolve()
    from producer_guard import verify_source
    verify_source(source)
    sys.path.insert(0,str(source))
    import ntt_gamma_rows as producer
    out=Path(args.output)
    if out.exists() and any(out.iterdir()):raise FileExistsError('Refusing nonempty output')
    scratch=Path(args.scratch)
    if scratch.exists() and any(scratch.iterdir()):raise FileExistsError('Refusing nonempty scratch')
    scratch.mkdir(parents=True,exist_ok=True)
    shape=(args.degree+1,5120,256);count=0;allocations=[];released_initial=[];released_phases=[]
    class GammaOutputMemmap(FlushedMemmap):
        def __setitem__(self,key,value):
            super().__setitem__(key,value)
            if getattr(self,'output_role',None)=='rad':
                caller=inspect.currentframe().f_back
                if caller.f_code is not producer.main.__code__:raise RuntimeError('Unexpected Gamma phase writer')
                phase=caller.f_locals['phase_index']
                if phase!=len(released_phases):raise RuntimeError('Unexpected phase lifetime sequence')
                exact=caller.f_locals['exact'];residues=caller.f_locals['residues']
                if exact.dtype!=object or not isinstance(residues,list):raise TypeError('Unexpected consumed CRT buffers')
                # Both binary64 outputs have been copied and flushed. Neither
                # exact nor residues is read again before the next assignment.
                exact.fill(0);residues.clear();gc.collect()
                released_phases.append(phase)
    old_empty,old_empty_like=np.empty,np.empty_like
    def allocate(shape,dtype=float,order='C',**kwargs):
        nonlocal count
        if (tuple(shape) if not isinstance(shape,int) else (shape,))==(args.degree+1,5120,256):
            if np.dtype(dtype)!=np.dtype('float64') or order!='C' or kwargs:raise ValueError('Unexpected buffer allocation signature')
            if count==0:
                caller=inspect.currentframe().f_back
                if caller.f_code is not producer.main.__code__:raise RuntimeError('Unexpected Gamma allocation caller')
                for name,kind in [('packet',dict),('jumps',list)]:
                    value=caller.f_locals[name]
                    if not isinstance(value,kind):raise TypeError('Unexpected completed source container')
                    value.clear();released_initial.append(name)
                gc.collect()
            path=scratch/('gamma_mid.npy' if count==0 else 'gamma_rad.npy')
            if count>=2:raise RuntimeError('Unexpected third output allocation')
            array=np.lib.format.open_memmap(path,mode='w+',dtype='float64',shape=shape,fortran_order=False).view(GammaOutputMemmap)
            array.output_role='mid' if count==0 else 'rad'
            allocations.append({'file':path.name,'shape':list(shape),'dtype':'float64','order':'C'})
            count+=1
            return array
        return old_empty(shape,dtype=dtype,order=order,**kwargs)
    def empty_like(a,*args_,**kwargs):
        if tuple(a.shape)==shape and isinstance(a,FlushedMemmap):
            if args_ or kwargs:raise ValueError('Unexpected empty_like signature')
            return allocate(shape,dtype=a.dtype)
        return old_empty_like(a,*args_,**kwargs)
    np.empty,np.empty_like=allocate,empty_like
    try:
        producer.main(argparse.Namespace(candidate=args.candidate,output=args.output,degree=args.degree))
    finally:
        np.empty,np.empty_like=old_empty,old_empty_like
    assert count==2 and len(released_phases)==args.degree+1
    (out/'storage_adapter_identity.json').write_text(json.dumps({'storage_only_adapter':True,'source_bytes_modified':False,'source_producer_sha256':hashlib.sha256((source/'ntt_gamma_rows.py').read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'allocations':allocations,'unused_initial_containers_released':released_initial,'consumed_CRT_buffers_released_after_phases':released_phases,'scientific_arithmetic_and_phase_order_unchanged':True},indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['source-dir','candidate','output','scratch']:p.add_argument('--'+k,required=True)
    p.add_argument('--degree',type=int,default=32)
    main(p.parse_args())
