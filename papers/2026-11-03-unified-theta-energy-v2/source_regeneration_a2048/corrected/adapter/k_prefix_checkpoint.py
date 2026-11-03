"""Atomic, hash-bound exact binary64 prefix state; never infer state from logs."""
import hashlib,json,os,shutil,uuid
from pathlib import Path
import numpy as np


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def durable_bytes(path,data):
    with Path(path).open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
def sync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)


class PrefixStore:
    def __init__(self,root,binding,cells=5120,k=256,stride=64):
        self.root=Path(root);self.binding=binding;self.cells=cells;self.k=k;self.stride=stride
        self.binding_sha256=hashlib.sha256(canonical(binding)).hexdigest()
        self.root.mkdir(parents=True,exist_ok=True)
        identity=self.root/'INPUT_IDENTITY.json'
        record={'schema':'a2048_K_prefix_identity_v1','binding':binding,'binding_sha256':self.binding_sha256,'cells':cells,'k':k,'stride':stride}
        if identity.exists():
            if json.loads(identity.read_text())!=record:raise ValueError('Checkpoint identity/config mismatch')
        else:
            durable_bytes(identity,canonical(record)+b'\n');sync_dir(self.root)
    def _validate(self,folder):
        manifest=json.loads((folder/'manifest.json').read_text())
        if manifest.get('schema')!='a2048_K_prefix_v1' or manifest.get('binding_sha256')!=self.binding_sha256:
            raise ValueError('Checkpoint manifest binding mismatch')
        c=manifest['completed_cells']
        if not isinstance(c,int) or c<=0 or c>self.cells or c%self.stride or folder.name!=f'cell_{c:06d}':
            raise ValueError('Invalid exact prefix length')
        if manifest['array_file']!='state.npz' or manifest['weights_file']!='weights.json':raise ValueError('Unexpected checkpoint files')
        if digest(folder/'state.npz')!=manifest['array_sha256'] or digest(folder/'weights.json')!=manifest['weights_sha256']:
            raise ValueError('Checkpoint payload hash mismatch')
        with np.load(folder/'state.npz',allow_pickle=False) as data:
            if data.files!=['mid','rad','trace']:raise ValueError('Unexpected checkpoint arrays')
            mid=data['mid'];rad=data['rad'];trace=data['trace']
        if mid.shape!=(self.k,self.k) or rad.shape!=mid.shape or trace.shape!=(c,):raise ValueError('Checkpoint shape mismatch')
        if any(x.dtype!=np.dtype('float64') for x in [mid,rad,trace]):raise ValueError('Checkpoint dtype mismatch')
        if not all(np.isfinite(x).all() for x in [mid,rad,trace]) or np.any(rad<0):raise ValueError('Invalid checkpoint ball')
        weights=json.loads((folder/'weights.json').read_text())
        if len(weights)!=c:raise ValueError('Checkpoint weight-prefix length mismatch')
        refinement=self.binding['weight_refinement']
        if any(len(row)!=refinement or any(not isinstance(v,list) or len(v)!=2 or not all(isinstance(x,int) for x in v) or v[1]<=0 for v in row) for row in weights):
            raise ValueError('Invalid exact weight dyadics')
        return {'completed_cells':c,'mid':mid,'rad':rad,'trace':trace.tolist(),'weights':weights,'manifest_sha256':digest(folder/'manifest.json'),'folder':folder.name}
    def latest(self,required=False):
        folders=sorted(self.root.glob('cell_[0-9]*'))
        if not folders:
            if required:raise FileNotFoundError('No complete checkpoint; logs/temporary buffers are not resumable state')
            return None
        # Atomic directory rename commits a generation, even if pointer update
        # was interrupted. Refuse a damaged latest generation; do not guess.
        return self._validate(folders[-1])
    def save(self,completed,ball,weights,trace):
        if completed<=0 or completed>self.cells or completed%self.stride or len(weights)!=completed or len(trace)!=completed:
            raise ValueError('Progress does not match exact prefix state')
        mid=np.asarray(ball.mid);rad=np.asarray(ball.rad)
        if mid.shape!=(self.k,self.k) or rad.shape!=mid.shape or not np.isfinite(mid).all() or not np.isfinite(rad).all() or np.any(rad<0):raise ValueError('Invalid prefix ball')
        final=self.root/f'cell_{completed:06d}'
        if final.exists():raise FileExistsError('Refusing to overwrite committed checkpoint')
        staging=self.root/('.staging_'+uuid.uuid4().hex);staging.mkdir()
        try:
            with (staging/'state.npz').open('wb') as f:
                np.savez_compressed(f,mid=mid,rad=rad,trace=np.asarray(trace,dtype='float64'))
                f.flush();os.fsync(f.fileno())
            durable_bytes(staging/'weights.json',canonical(weights)+b'\n')
            record={'schema':'a2048_K_prefix_v1','binding_sha256':self.binding_sha256,'completed_cells':completed,'array_file':'state.npz','weights_file':'weights.json','array_sha256':digest(staging/'state.npz'),'weights_sha256':digest(staging/'weights.json'),'state_scope':'K immediately after cell completed_cells-1; before final symmetrization/inflation'}
            durable_bytes(staging/'manifest.json',canonical(record)+b'\n');sync_dir(staging)
            os.replace(staging,final);sync_dir(self.root)
            pointer={'folder':final.name,'manifest_sha256':digest(final/'manifest.json')}
            temporary=self.root/('.latest_'+uuid.uuid4().hex)
            durable_bytes(temporary,canonical(pointer)+b'\n');os.replace(temporary,self.root/'LATEST.json');sync_dir(self.root)
        except BaseException:
            if staging.exists():shutil.rmtree(staging)
            raise
        return record


def restore_objects(local,checkpoint,k):
    """Keep the original K/list variable bindings; restore their exact contents."""
    from ball_array import Ball
    K=local['K'];weights=local['weights_saved'];trace=local['cell_trace']
    if not isinstance(K,Ball) or K.mid.shape!=(k,k) or weights or trace or np.any(K.mid) or np.any(K.rad):
        raise ValueError('Not the original zero-state loop boundary')
    if checkpoint is None:return 0
    restored=Ball(checkpoint['mid'].copy(),checkpoint['rad'].copy())
    K.mid=restored.mid;K.rad=restored.rad
    weights.extend(checkpoint['weights']);trace.extend(checkpoint['trace'])
    return checkpoint['completed_cells']
