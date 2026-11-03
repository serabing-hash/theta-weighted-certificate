"""Bind storage/lifetime assumptions to the immutable reviewed producer modules."""
from pathlib import Path
import hashlib

EXPECTED = {'ball_array.py': '1b8b6ac09a84d7d72d20fe66e6ee638b341242cf1a76bb131f2f3766777fe598', 'check_preflight.py': 'eb782c0ad97c38c5373ac34228cf04ef44074c7ee8525c4d03b7747f783b4d6e', 'check_reference_closure.py': 'e9ec857744a244bd212618cd1885c595076a348eb28532ea1f3e1d0f8368fc6c', 'evaluate_frozen_diag.py': 'd6d8c37343ce9f44453ae62a8c6b280365d106e1cf9cfe25dab4399f29002b52', 'freeze_candidate.py': '92225da0b21c9c6ef6197ba52270e8a7a3a0f79f6be028b9481526fe9c63ac6b', 'integer_convolution.py': '399cab228bcff60e4219581449094104c769d2cf0f78f27fdb825b4efb5aa9d6', 'interval_bounds.py': '95f90cb8ac6e1d73ea7639c0e44140a4df4a9ed96923945d16ebde80d0a6a05b', 'ntt_gamma_rows.py': 'fbe83fa8217c118a75291b144637933d46c3c1ddb2d2a15497c7234014a107ee', 'run_gate400.py': '80e97f83157637c43f8e3938f94b133d841d56c02affa2677567d7ea81f1099f', 'source_geometry.py': '8f0c65a48b4d83d6526fe0965629cadb8bc76780ad8ac15f55b1f2c22a030600', 'target.py': '7f3231e1a14d606945519140351a093278757acc0231a89e114eb8d2303844b3', 'validated_phi.py': '6b4f74d27d61d0b9cb3f186be9333ca1008bfdb97d5e7055dab8c5368eb6ad56', 'validated_quadrature.py': 'b4bd30653de32e0478005b56da78832710bd89dad49a3eb83547b9f63f493c0d', 'validated_residual_model.py': '68a616960f4b370072ccefe07794c14b3a854410c8d7965a4a0e0c93874295df', 'verify_energy_lower.py': 'c6f3a8ff5274afa38fa98e2d674593b8651dcfed3aeb0c7a4b9817786f1d3b3e', 'verify_final_gate.py': 'f5058d416c2d9b2ec0012c255e6fc3009c62762d3aec095c307fa87fffbc52f5', 'verify_gram_upper.py': '1037b04990d6cfa42a70424579991c9ec4ed4567195a5b27bd87144d1d0081c4', 'verify_residual_gram.py': '9f85e794fe004e56cf3ea33d7ee9c11a423153155eafe6046f5b089614cceaf5', 'weighted64.py': '8943e3afa414ae412b4d89c493e35f1c8d701590e1162bce318d949220ff1b8b'}

def verify_source(source_dir):
    source=Path(source_dir)
    for name,expected in EXPECTED.items():
        path=source/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValueError('Producer source identity mismatch: '+name)
    return dict(EXPECTED)
