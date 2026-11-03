"""Exact-state interruption/resume fixtures, not a substitute for full K replay."""
import argparse,builtins,inspect,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--source-dir',required=True);args,remaining=p.parse_known_args();sys.path.insert(0,str(Path(args.source_dir).resolve()))
from ball_array import Ball
from k_prefix_checkpoint import PrefixStore,restore_objects,canonical
import k_prefix_checkpoint as cp

class Interrupted(Exception):pass
class CheckpointTests(unittest.TestCase):
 def fixture(self,stop):
  rng=np.random.default_rng(2048);cells=128;k=7
  mids=rng.normal(size=(cells,k,k))*np.array([1e10,1e-10,1.,-1e10])[np.arange(cells)%4,None,None]
  radii=np.abs(mids)*1e-14+1e-20
  ns={'np':np,'Ball':Ball,'cells':cells,'k':k,'mids':mids,'radii':radii,'visited':[],'print':lambda *a,**k:None}
  exec('''def main():
 weights_saved=[]
 K=Ball(np.zeros((k,k)))
 cell_trace=[]
 for cell in range(cells):
  visited.append(cell)
  Kcell=Ball(mids[cell],radii[cell])
  K=K+Kcell
  weights_saved.append([[cell+1,2],[cell+2,4],[cell+3,8]])
  cell_trace.append(float(np.trace(Kcell.mid)))
  if (cell+1)%64==0:print(f"validated residual integration {cell+1}/{cells}")
 K=(K+K.T)/2
 return K,weights_saved,cell_trace
''',ns)
  main=ns['main'];expected=main();ns['visited']=[]
  with tempfile.TemporaryDirectory() as td:
   store=PrefixStore(td,{'weight_refinement':3,'fixture':'unchanged-source-order'},cells=cells,k=k)
   prefix=None;range_calls=[]
   def ranges(*values):
    caller=inspect.currentframe().f_back
    if caller.f_code is main.__code__ and values==(cells,):
     start=restore_objects(caller.f_locals,prefix,k);range_calls.append(start);return builtins.range(start,cells)
    return builtins.range(*values)
   def emit(value):
    caller=inspect.currentframe().f_back;local=caller.f_locals;completed=local['cell']+1
    store.save(completed,local['K'],local['weights_saved'],local['cell_trace'])
    if completed==stop:raise Interrupted()
   ns['range']=ranges;ns['print']=emit
   with self.assertRaises(Interrupted):main()
   first=list(ns['visited']);prefix=store.latest(required=True);self.assertEqual(prefix['completed_cells'],stop)
   ns['visited']=[];ns['print']=lambda *a,**k:None
   actual=main();self.assertEqual(first+ns['visited'],list(builtins.range(cells)));self.assertEqual(range_calls,[0,stop])
   for field in ['mid','rad']:
    self.assertEqual(getattr(expected[0],field).tobytes(),getattr(actual[0],field).tobytes())
   self.assertEqual(canonical(expected[1]),canonical(actual[1]));self.assertEqual(np.array(expected[2]).tobytes(),np.array(actual[2]).tobytes())
 def test_resume_midway_preserves_bitwise_order(self):self.fixture(64)
 def test_resume_complete_prefix_symmetrizes_once(self):self.fixture(128)
 def test_logs_and_partial_staging_are_not_state(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);store=PrefixStore(root,{'weight_refinement':1},cells=2,k=2,stride=2)
   (root/'old.log').write_text('validated residual integration 2/2\n');(root/'.staging_incomplete').mkdir();(root/'.staging_incomplete/state.npz').write_bytes(b'partial')
   with self.assertRaises(FileNotFoundError):store.latest(required=True)
 def test_config_mismatch_and_payload_corruption_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   store=PrefixStore(td,{'weight_refinement':1,'candidate':'fixed'},cells=2,k=2,stride=2)
   store.save(2,Ball(np.eye(2),np.ones((2,2))*1e-20),[[[1,2]],[[3,4]]],[1.,2.])
   with self.assertRaises(ValueError):PrefixStore(td,{'weight_refinement':1,'candidate':'changed'},cells=2,k=2,stride=2)
   with (Path(td)/'cell_000002/state.npz').open('ab') as f:f.write(b'corruption')
   with self.assertRaises(ValueError):store.latest(required=True)
 def test_committed_generation_survives_pointer_update_failure(self):
  with tempfile.TemporaryDirectory() as td:
   store=PrefixStore(td,{'weight_refinement':1},cells=2,k=2,stride=2);original=cp.os.replace
   def replace(src,dst):
    if Path(dst).name=='LATEST.json':raise OSError('simulated pointer interruption')
    return original(src,dst)
   with patch.object(cp.os,'replace',side_effect=replace),self.assertRaises(OSError):
    store.save(2,Ball(np.eye(2),np.ones((2,2))*1e-20),[[[1,2]],[[3,4]]],[1.,2.])
   self.assertEqual(store.latest(required=True)['completed_cells'],2)
 def test_source_has_one_guarded_outer_loop(self):
  source=(Path(args.source_dir)/'verify_residual_gram.py').read_text()
  self.assertEqual(source.count('for cell in range(cells):'),1)
if __name__=='__main__':unittest.main(argv=[sys.argv[0],*remaining])
