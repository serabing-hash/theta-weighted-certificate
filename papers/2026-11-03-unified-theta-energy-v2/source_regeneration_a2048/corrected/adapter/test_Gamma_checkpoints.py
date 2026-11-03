"""Small exact phase interruption fixtures for the production adapter path."""
import argparse,hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--source-dir',required=True);args,remaining=p.parse_known_args();sys.path.insert(0,str(Path(args.source_dir).resolve()))
from interval_bounds import IV
from fractions import Fraction
from gamma_phase_checkpoint import GammaPhaseStore
import gamma_phase_checkpoint as cp
import run_gamma_checkpointed as adapter
import ntt_gamma_rows as producer
class Interrupted(Exception):pass
class GammaCheckpointTests(unittest.TestCase):
 def test_adapter_interruption_resume_and_complete_prefix(self):
  for stop in [2,5]:
   with self.subTest(stop=stop),tempfile.TemporaryDirectory() as td:
    root=Path(td);frozen=root/'frozen';frozen.mkdir();(frozen/'candidate.json').write_text('{}')
    candidate=hashlib.sha256(b'{}').hexdigest();visited=[]
    def fixture(a):
     out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
     packet={'fixture':True};jumps=[[1,2,3]];n=2;k=3;h=Fraction(1,2);cells=4;degree=4;size=16;product=17
     phases=[IV.rational(i,8) for i in range(5)];H0=IV(1);hradius=Fraction(1,16);jradius=Fraction(1,32);error=[Fraction(1,64)]*3
     source_ffts=[np.arange(12,dtype=np.int64).reshape(4,3)]
     gamma=np.empty((degree+1,cells,k));radii=np.empty_like(gamma)
     for phase_index,phase in producer.enumerate(phases) if 'enumerate' in producer.__dict__ else enumerate(phases):
      visited.append(phase_index);exact=np.array([[2**80+phase_index]],dtype=object);residues=[np.array([1,2])]
      midpoint=np.arange(12,dtype=float).reshape(4,3)*(phase_index+1)/7;rad=np.nextafter(abs(midpoint)*1e-16,np.inf)
      gamma[phase_index]=midpoint;radii[phase_index]=rad
      if 'print' in producer.__dict__:producer.print(f'validated Gamma phase {phase_index+1}/{degree+1}',flush=True)
     np.savez_compressed(out/'gamma_nodes.npz',mid=gamma,rad=radii)
    # The test replaces only producer.main and fixed-size constants in memory;
    # the production adapter code, checkpoint commit, restore and guards run.
    with patch.object(producer,'main',fixture),patch.object(adapter,'PHASE_COUNT',5),patch.object(adapter,'CELLS',4),patch.object(adapter,'K',3),patch.object(adapter,'CANDIDATE',candidate):
     fixture(argparse.Namespace(output=str(root/'expected')));visited.clear()
     common=dict(source_dir=args.source_dir,candidate=str(frozen),degree=4,checkpoints=str(root/'checkpoint'))
     original=GammaPhaseStore.save
     def interrupted(store,index,mid,rad):
      result=original(store,index,mid,rad)
      if index+1==stop:raise Interrupted()
      return result
     with patch.object(GammaPhaseStore,'save',interrupted),self.assertRaises(Interrupted):
      adapter.main(argparse.Namespace(**common,output=str(root/'first'),scratch=str(root/'firstscratch'),resume=False))
     first=list(visited);visited.clear()
     adapter.main(argparse.Namespace(**common,output=str(root/'resumed'),scratch=str(root/'secondscratch'),resume=True))
     self.assertEqual(first+visited,list(range(5)))
     self.assertEqual((root/'expected/gamma_nodes.npz').read_bytes(),(root/'resumed/gamma_nodes.npz').read_bytes())
     record=json.loads((root/'resumed/checkpoint_adapter_identity.json').read_text());self.assertEqual(record['resumed_from_completed_phases'],stop)
 def test_identity_change_and_damage_refused(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);s=GammaPhaseStore(root,{'candidate':'one','error':['1/64']},3,(2,3));s.validate_prefix();s.save(0,np.ones((2,3)),np.zeros((2,3)))
   with self.assertRaises(ValueError):GammaPhaseStore(root,{'candidate':'two','error':['1/64']},3,(2,3))
   with (root/'phase_000/mid.npy').open('ab') as f:f.write(b'corruption')
   with self.assertRaises(ValueError):s.validate_prefix()
 def test_missing_middle_and_partial_log_not_state(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);s=GammaPhaseStore(root,{},3,(2,3));(root/'old.log').write_text('validated Gamma phase 33/33');(root/'.staging_partial').mkdir()
   with self.assertRaises(FileNotFoundError):s.validate_prefix(required=True)
   s.save(0,np.ones((2,3)),np.zeros((2,3)));(root/'phase_000').rename(root/'phase_001')
   with self.assertRaises(ValueError):s.validate_prefix()
 def test_nonfinite_negative_radius_and_wrong_phase_refused(self):
  with tempfile.TemporaryDirectory() as td:
   s=GammaPhaseStore(td,{},3,(2,3));a=np.ones((2,3))
   for index,mid,rad in [(1,a,a),(0,a,-a),(0,a*np.inf,a)]:
    with self.assertRaises(ValueError):s.save(index,mid,rad)
 def test_failed_atomic_commit_is_not_prefix(self):
  with tempfile.TemporaryDirectory() as td:
   s=GammaPhaseStore(td,{},3,(2,3));a=np.ones((2,3))
   with patch.object(cp.os,'replace',side_effect=OSError('interrupted before atomic rename')),self.assertRaises(OSError):s.save(0,a,a)
   self.assertEqual(s.validate_prefix(),[])
 def test_original_phase_loop_is_single(self):
  source=(Path(args.source_dir)/'ntt_gamma_rows.py').read_text();self.assertEqual(source.count('for phase_index,phase in enumerate(phases):'),1)
if __name__=='__main__':unittest.main(argv=[sys.argv[0],*remaining])
