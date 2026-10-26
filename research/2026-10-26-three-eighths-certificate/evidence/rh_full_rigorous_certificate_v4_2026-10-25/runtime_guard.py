"""Bind actually loaded runtime binaries and package implementation files; no numerical test."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,json,hashlib,ctypes,subprocess,signal,resource,argparse,zipfile,lzma,bz2,zlib,sysconfig
import inertia_check
from pathlib import Path
import numpy,scipy.linalg,threadpoolctl

def snapshot():
 ctypes.CDLL(str(Path('h_point.so').resolve()))
 # Loading, not calling, the point library binds MPFR/GMP/libm/libc dependencies.
 paths={Path(sys.executable).resolve(),Path('h_point.so').resolve()}
 for line in Path('/proc/self/maps').read_text().splitlines():
  parts=line.split(maxsplit=5)
  if len(parts)==6 and parts[5].startswith('/'):
   f=Path(parts[5]);
   if f.is_file():paths.add(f.resolve())
 for root in [Path(numpy.__file__).parent,Path(scipy.__file__).parent]:
  paths.update(f.resolve() for f in root.rglob('*') if f.is_file() and (f.suffix=='.py' or '.so' in f.name))
 paths.add(Path(threadpoolctl.__file__).resolve())
 paths.update(f.resolve() for f in Path(sysconfig.get_path('stdlib')).joinpath('lib-dynload').glob('*.so'))
 return {str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(paths)}
def verify(label):
 actual=snapshot();expected=json.loads(Path('RUNTIME_EXPECTED.json').read_text())
 if actual!=expected:raise RuntimeError('runtime fingerprint mismatch at '+label)
 Path('runtime_'+label+'.json').write_text(json.dumps({'status':'MATCH','files':len(actual),'fingerprints':actual},indent=2))
if __name__=='__main__':
 if sys.argv[1]=='prepare':Path('RUNTIME_EXPECTED.json').write_text(json.dumps(snapshot(),indent=2))
 else:verify(sys.argv[1])
