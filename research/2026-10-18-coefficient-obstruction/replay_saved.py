#!/usr/bin/env python3
"""Optional reader replay of saved mathematics. NOT RUN for publication.

The executed checker is unchanged. This adapter replaces only absolute-path
admission and private prior-run admission with a portable manifest and a direct
same-vector quadratic check. It does not reproduce the historical OS/resource
protocol or prove the analytic/physical premises. Python standard library only.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import os
import sys
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True,
                    help='new output directory, which must not exist')
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    manifest_path = root / 'INPUTS.json'
    manifest = json.loads(manifest_path.read_text())
    checker_path = root / 'code/executed_coefficient_checker.py'
    assert hashlib.sha256(checker_path.read_bytes()).hexdigest() == manifest['executed_checker_sha256']
    if args.output.exists():
        raise SystemExit('Output exists; preserve it and do not overwrite.')
    sys.set_int_max_str_digits(100000)
    start = time.monotonic()

    def guard():
        if time.monotonic() - start > 60:
            raise RuntimeError('Reader replay elapsed guard exceeded; stop without retry.')

    spec = importlib.util.spec_from_file_location('executed_checker', checker_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class PortableInputs:
        def __init__(self, path):
            assert Path(path).resolve() == manifest_path
            self.m = {'source_root': str(root)}
            self.rows = manifest['bindings']
            self.paths = {}
            for role, row in self.rows.items():
                rel = Path(row['path'])
                assert not rel.is_absolute() and '..' not in rel.parts
                p = root / rel
                assert p.resolve().is_relative_to(root) and not p.is_symlink()
                self.paths[role] = p
            self.verify()

        def verify(self):
            for role, row in self.rows.items():
                guard()
                p = self.paths[role]
                assert p.stat().st_size == row['bytes']
                assert module.sha(p) == row['sha256'], role

        def read(self, role):
            return module.load(self.paths[role])

        def h(self, role):
            return self.rows[role]['sha256']

    def portable_witness(inp):
        v = inp.read('witness_vector')
        old = inp.read('witness_check')
        module.need(v['bits'] == 80 and v['length'] == 211 and
                    v['selected_indices_zero_based'] == list(range(211)), 'fixed vector metadata')
        w = [module.integer(s) for s in v['numerators']]
        module.need(len(w) == 211 and w[-1] == 1 << 80, 'fixed nonzero same direction')
        module.need(old['vector_sha256'] == inp.h('witness_vector'), 'prior vector identity')
        module.need(v['U_MODEL_sha256'] == inp.h('saved_U_MODEL') and
                    v['UCERT_sha256'] == inp.h('saved_UCERT'), 'same saved output matrices')
        uc, ur = module.interval(inp.paths['saved_U_MODEL'], (372,372), (211,211), 100, True)
        cert = module.exact(inp.paths['saved_UCERT'], (372,372), (211,211), 100)
        n = module.dot(w, w)
        identity = module.shift(n,100)
        center = module.dot(w, module.matvec(uc,w))
        upper = module.dot(w, module.matvec(cert,w))
        av = list(map(abs,w))
        radius = module.dot(av, module.matvec(ur,av))
        values = {'identity':identity, 'U_MODEL_center':center, 'UCERT':upper,
                  'final_diagonal_pad':module.sub(upper,center),
                  'saved_entrywise_radius_bound':radius,
                  'I_minus_U_MODEL_center':module.sub(identity,center),
                  'I_minus_UCERT':module.sub(identity,upper)}
        for key, number in values.items():
            rec = old['quadratic_values_unreduced_exact_rationals'][key]
            module.need(module.integer(rec['denominator']) == 1 << 260 and
                        module.integer(rec['numerator']) == number, 'old directional scalar '+key)
        module.need(identity-center < 0 and identity-upper < 0, 'center and certificate failure')
        return w,n,center

    module.Inputs = PortableInputs
    module.check_cached_witness = portable_witness
    os.environ['SHIFT_CHARGED_EXACT_CHECK'] = '1'  # local admission flag, not a credential
    produced = module.run(str(root), str(manifest_path), str(args.output), guard)
    reference = json.loads((root / manifest['reference_report']).read_text())
    for key in ['scope','status','stage','decisions','normal_bounds','exact_values',
                'same_direction_residual_and_rounding_links','primitive_error_owners_charged_once']:
        if produced[key] != reference[key]:
            raise RuntimeError('Reference mathematical field mismatch: '+key)
    print(json.dumps({'status':'MATCHED-SAVED-MATHEMATICAL-FIELDS-CONDITIONALLY',
                      'historical_resource_protocol_reproduced':False,
                      'physical_premises_reproved':False,
                      'RH_PROOF':'NOT-OBTAINED'}))


if __name__ == '__main__':
    main()
