"""Focused equivalence/lifetime tests for storage adapters, not a full certificate."""
import argparse,hashlib,json,sys,tempfile,unittest
from pathlib import Path
import numpy as np

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source-dir',required=True)
a,remaining=p.parse_known_args()
sys.path.insert(0,str(Path(a.source_dir).resolve()))
from ball_array import Ball,norm_upper
from disk_backed_storage import ArchiveMappings,FullShapeDiskArithmetic
import run_gamma_disk_backed as gamma_adapter
import ntt_gamma_rows as gamma_producer

class StorageEquivalenceTests(unittest.TestCase):
    def test_full_shape_ball_and_npz(self):
        rng=np.random.default_rng(2048)
        for shape in [(3,3,7),(33,33,512),(7,33,256),(33,33,20000)]:
            with self.subTest(shape=shape),tempfile.TemporaryDirectory() as td:
                d=Path(td)
                left=Ball(rng.normal(size=shape[:2]),np.abs(rng.normal(size=shape[:2]))*1e-14)
                right=Ball(rng.normal(size=shape[1:]),np.abs(rng.normal(size=shape[1:]))*1e-13)
                expected=left@right
                actual=FullShapeDiskArithmetic(d/'arith').ball_matmul(left,right)
                self.assertTrue(np.array_equal(expected.mid,actual.mid))
                self.assertTrue(np.array_equal(expected.rad,actual.rad))
                np.savez_compressed(d/'expected.npz',mid=expected.mid,rad=expected.rad)
                np.savez_compressed(d/'actual.npz',mid=actual.mid,rad=actual.rad)
                self.assertEqual((d/'expected.npz').read_bytes(),(d/'actual.npz').read_bytes())
                mapped=ArchiveMappings(d/'actual.npz',d/'mapped',hashlib.sha256((d/'actual.npz').read_bytes()).hexdigest())
                for k,v in [('mid',expected.mid),('rad',expected.rad)]:
                    self.assertTrue(np.array_equal(mapped[k],v));self.assertFalse(mapped[k].flags.writeable)
    def test_same_layout_norm(self):
        rng=np.random.default_rng(2048)
        for shape in [(33,31,256),(7,12,256)]:
            with self.subTest(shape=shape),tempfile.TemporaryDirectory() as td:
                values=np.abs(rng.normal(size=shape)).transpose(1,0,2)
                actual=FullShapeDiskArithmetic(Path(td)/'norm').norm_upper(values,2)
                self.assertTrue(np.array_equal(norm_upper(values,2),actual))
    def test_gamma_allocation_and_dead_buffer_lifetime(self):
        original=gamma_producer.main
        with tempfile.TemporaryDirectory() as td:
            d=Path(td);(d/'out').mkdir()
            def fixture(args):
                packet={'fixture':[1,2,3]};jumps=[[1,2,3]]
                small=np.empty(8,dtype=np.int64)
                self.assertEqual(small.shape,(8,));self.assertNotIsInstance(small,np.memmap)
                mid=np.empty((3,5120,256));rad=np.empty_like(mid)
                self.assertEqual(packet,{});self.assertEqual(jumps,[])
                self.assertIsInstance(mid,np.memmap);self.assertIsInstance(rad,np.memmap)
                for phase_index in range(3):
                    exact=np.array([[2**100,-2**120]],dtype=object);residues=[np.array([1,2,3])]
                    mid[phase_index]=phase_index;rad[phase_index]=-phase_index
                    self.assertTrue(np.array_equal(mid[phase_index],-rad[phase_index]))
                    self.assertFalse(np.any(exact));self.assertEqual(residues,[])
            gamma_producer.main=fixture
            try:
                gamma_adapter.main(argparse.Namespace(source_dir=a.source_dir,output=str(d/'out'),scratch=str(d/'scratch'),candidate='unused_fixture',degree=2))
            finally:gamma_producer.main=original
            identity=json.loads((d/'out/storage_adapter_identity.json').read_text())
            self.assertEqual(identity['consumed_CRT_buffers_released_after_phases'],[0,1,2])

if __name__=='__main__':unittest.main(argv=[sys.argv[0],*remaining])
