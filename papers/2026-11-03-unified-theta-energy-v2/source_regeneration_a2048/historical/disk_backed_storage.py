"""Storage-only numerical helpers: full-shape operations, no reassociation.

Each helper matches the exact operation sequence of ball_array.py. The only
changes are output-buffer allocation/lifetime and flushed file-backed storage.
All dense BLAS products keep the original full dimensions and input values.
"""
import hashlib,json,mmap,zipfile
from pathlib import Path
import numpy as np


def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def evict(a):
    seen=set()
    while a is not None and id(a) not in seen:
        seen.add(id(a))
        if isinstance(a,np.memmap):
            a.flush()
            if hasattr(a._mmap,'madvise'):a._mmap.madvise(mmap.MADV_DONTNEED)
            return
        a=getattr(a,'base',None)


class ArchiveMappings:
    """Read-only NPY views extracted by streaming from a hash-bound NPZ."""
    def __init__(self,archive,scratch,expected_sha256=None):
        self.path=Path(archive);self.scratch=Path(scratch)
        self.sha256=sha256_file(self.path)
        if expected_sha256 is not None and self.sha256!=expected_sha256:raise ValueError('NPZ identity mismatch')
        if self.scratch.exists() and any(self.scratch.iterdir()):raise FileExistsError('Refusing nonempty extraction scratch')
        self.scratch.mkdir(parents=True,exist_ok=True);self.files=[];self.arrays={};records=[]
        with zipfile.ZipFile(self.path) as z:
            for info in z.infolist():
                if '/' in info.filename or not info.filename.endswith('.npy'):raise ValueError('Unexpected NPZ member')
                key=info.filename[:-4];destination=self.scratch/info.filename
                with z.open(info) as src,destination.open('wb') as dst:
                    for chunk in iter(lambda:src.read(1024*1024),b''):dst.write(chunk)
                a=np.lib.format.open_memmap(destination,mode='r')
                self.files.append(key);self.arrays[key]=a
                records.append({'key':key,'shape':list(a.shape),'dtype':str(a.dtype),'npy_sha256':sha256_file(destination)})
        (self.scratch/'mapping_identity.json').write_text(json.dumps({'archive_sha256':self.sha256,'arrays':records,'read_only':True,'streamed_extraction':True},indent=2)+'\n')
    def __getitem__(self,k):return self.arrays[k]
    def close(self):pass


class FullShapeDiskArithmetic:
    def __init__(self,scratch):
        self.scratch=Path(scratch)
        if self.scratch.exists() and any(self.scratch.iterdir()):raise FileExistsError('Refusing nonempty arithmetic scratch')
        self.scratch.mkdir(parents=True,exist_ok=True);self.arrays=[];self.operations=[]
    def empty(self,shape,label):
        p=self.scratch/f'{len(self.arrays):02d}_{label}.npy'
        a=np.lib.format.open_memmap(p,mode='w+',dtype='float64',shape=shape,fortran_order=False)
        self.arrays.append(a);return a
    def matmul(self,a,b,label):
        out=self.empty((a.shape[0],b.shape[1]),label)
        np.matmul(a,b,out=out)
        if not np.isfinite(out).all():raise ArithmeticError('Nonfinite dot product')
        self.operations.append({'operation':'full_shape_matmul','left':list(a.shape),'right':list(b.shape),'out':list(out.shape)})
        evict(a);evict(b);evict(out);return out
    def abs(self,a,label):
        out=self.empty(a.shape,label);np.absolute(a,out=out);evict(a);evict(out);return out
    def empty_like_layout(self,a,label):
        # Match the original dense-permutation tensor strides, not merely shape.
        order=tuple(sorted(range(a.ndim),key=lambda i:a.strides[i],reverse=True))
        base=self.empty(tuple(a.shape[i] for i in order),label)
        inverse=tuple(order.index(i) for i in range(a.ndim))
        out=base.transpose(inverse)
        if out.strides!=a.strides:raise ValueError('Unsupported non-dense tensor layout')
        return out
    def norm_upper(self,a,axis):
        from ball_array import usum,up
        a=np.asarray(a)
        square=self.empty_like_layout(a,'absolute_square')
        np.absolute(a,out=square)
        # abs(a)*abs(a), followed by the same one outward nextafter as um.
        np.multiply(square,square,out=square)
        np.nextafter(square,np.inf,out=square)
        evict(a);evict(square)
        result=up(np.sqrt(usum(square,axis)))
        self.operations.append({'operation':'norm_upper','shape':list(a.shape),'strides':list(a.strides),'axis':axis,'same_full_shape_reduction':True})
        (self.scratch/'norm_identity.json').write_text(json.dumps(self.operations,indent=2)+'\n')
        evict(square)
        return result
    def um_inplace(self,a,b):
        np.multiply(a,b,out=a);np.nextafter(a,np.inf,out=a);evict(a);evict(b);return a
    def ua_inplace(self,a,b):
        np.add(a,b,out=a);np.nextafter(a,np.inf,out=a);evict(a);evict(b);return a
    def positive_dot_upper(self,a,b,label):
        from ball_array import EPS,TINY,up
        k=a.shape[-1];v=self.matmul(a,b,label)
        factor=up(1/(1-(2*k+2)*EPS))
        return self.ua_inplace(self.um_inplace(v,factor),TINY*(2*k+2))
    def ball_matmul(self,left,right):
        from ball_array import Ball,EPS,TINY,up
        right=right if isinstance(right,Ball) else Ball(right)
        k=left.mid.shape[-1]
        mid=self.matmul(left.mid,right.mid,'mid')
        absleft=np.abs(left.mid);absright=self.abs(right.mid,'abs_right_mid')
        mag=self.positive_dot_upper(absleft,absright,'magnitude')
        roundoff=self.ua_inplace(self.um_inplace(mag,up((2*k+2)*EPS/(1-(2*k+2)*EPS))),TINY*(2*k+2))
        p1=self.positive_dot_upper(left.rad,absright,'radius_term1')
        p2=self.positive_dot_upper(absleft,right.rad,'radius_term2')
        rad=self.ua_inplace(p1,p2)
        p3=self.positive_dot_upper(left.rad,right.rad,'radius_term3')
        rad=self.ua_inplace(rad,p3)
        result=Ball(mid,self.ua_inplace(rad,roundoff))
        (self.scratch/'arithmetic_identity.json').write_text(json.dumps({'operation_sequence':'ball_array.Ball.__matmul__ with full-shape outputs stored on disk','elementwise_rounding_sequence_unchanged':True,'no_block_or_cell_split':True,'operations':self.operations},indent=2)+'\n')
        return result
