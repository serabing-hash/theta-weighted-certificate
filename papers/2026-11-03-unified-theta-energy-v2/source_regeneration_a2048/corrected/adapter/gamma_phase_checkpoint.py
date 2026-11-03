"""Atomic authenticated independent Gamma rows; logs are never resumable state."""
from pathlib import Path
import hashlib,json,os,shutil,uuid
import numpy as np
from k_prefix_checkpoint import canonical,digest,durable_bytes,sync_dir

class GammaPhaseStore:
 def __init__(self,root,binding,phase_count=33,row_shape=(5120,256)):
  self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True);self.binding=binding;self.phase_count=phase_count;self.row_shape=tuple(row_shape)
  self.binding_sha256=hashlib.sha256(canonical(binding)).hexdigest()
  record={'schema':'gamma_independent_phase_identity_v1','binding':binding,'binding_sha256':self.binding_sha256,'phase_count':phase_count,'row_shape':list(row_shape),'dtype':'float64'}
  path=self.root/'INPUT_IDENTITY.json'
  if path.exists():
   if json.loads(path.read_text())!=record:raise ValueError('Gamma checkpoint identity/config mismatch')
  else:durable_bytes(path,canonical(record)+b'\n');sync_dir(self.root)
  self.committed=[]
 def validate_prefix(self,required=False):
  folders=sorted(self.root.glob('phase_[0-9]*'));records=[];previous=None
  if required and not folders:raise FileNotFoundError('No committed Gamma phase; logs and partial buffers are not state')
  for index,folder in enumerate(folders):
   if index>=self.phase_count or folder.name!=f'phase_{index:03d}':raise ValueError('Gamma phase gap or out-of-order directory')
   manifest=json.loads((folder/'manifest.json').read_text())
   if manifest.get('schema')!='gamma_independent_phase_v1' or manifest.get('binding_sha256')!=self.binding_sha256 or manifest.get('phase_index')!=index or manifest.get('previous_manifest_sha256')!=previous:raise ValueError('Gamma phase binding/order mismatch')
   if set(manifest['arrays'])!={'mid','rad'}:raise ValueError('Gamma row array set mismatch')
   for key in ['mid','rad']:
    record=manifest['arrays'][key];path=folder/(key+'.npy')
    if record['file']!=path.name or digest(path)!=record['file_sha256']:raise ValueError('Gamma row hash mismatch')
    a=np.load(path,mmap_mode='r',allow_pickle=False)
    if a.shape!=self.row_shape or a.dtype!=np.dtype('float64') or not a.flags.c_contiguous or not np.isfinite(a).all() or (key=='rad' and np.any(a<0)):raise ValueError('Invalid committed Gamma row')
    del a
   previous=digest(folder/'manifest.json');records.append({'phase_index':index,'manifest_sha256':previous,'folder':folder})
  self.committed=records
  return list(records)
 def save(self,index,mid,rad):
  if index!=len(self.committed) or index>=self.phase_count:raise ValueError('Not the next independent Gamma phase')
  for key,a in [('mid',mid),('rad',rad)]:
   if a.shape!=self.row_shape or a.dtype!=np.dtype('float64') or not a.flags.c_contiguous or not np.isfinite(a).all() or (key=='rad' and np.any(a<0)):raise ValueError('Invalid new Gamma row')
  final=self.root/f'phase_{index:03d}'
  if final.exists():raise FileExistsError('Refusing committed Gamma overwrite')
  staging=self.root/('.staging_'+uuid.uuid4().hex);staging.mkdir();arrays={}
  try:
   for key,a in [('mid',mid),('rad',rad)]:
    path=staging/(key+'.npy')
    with path.open('wb') as f:np.save(f,np.asarray(a),allow_pickle=False);f.flush();os.fsync(f.fileno())
    arrays[key]={'file':path.name,'file_sha256':digest(path)}
   record={'schema':'gamma_independent_phase_v1','binding_sha256':self.binding_sha256,'phase_index':index,'previous_manifest_sha256':self.committed[-1]['manifest_sha256'] if self.committed else None,'arrays':arrays}
   durable_bytes(staging/'manifest.json',canonical(record)+b'\n');sync_dir(staging);os.replace(staging,final);sync_dir(self.root)
   committed={'phase_index':index,'manifest_sha256':digest(final/'manifest.json'),'folder':final};self.committed.append(committed)
  except BaseException:
   if staging.exists():shutil.rmtree(staging)
   raise
  return committed
 def restore(self,gamma,radii):
  if gamma.shape!=(self.phase_count,*self.row_shape) or radii.shape!=gamma.shape or gamma.dtype!=np.dtype('float64') or radii.dtype!=gamma.dtype:raise ValueError('Gamma restore target mismatch')
  for record in self.committed:
   index=record['phase_index']
   for key,target in [('mid',gamma),('rad',radii)]:
    saved=np.load(record['folder']/(key+'.npy'),mmap_mode='r',allow_pickle=False)
    np.copyto(target[index],saved,casting='no');del saved
    if isinstance(target,np.memmap):
     target.flush()
     if hasattr(target._mmap,'madvise'):
      import mmap
      target._mmap.madvise(mmap.MADV_DONTNEED)
  return len(self.committed)
