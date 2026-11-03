#!/usr/bin/env python3
"""Compare regenerated complete frozen-source outputs to scientific reference digests.

No original source enclosures are loaded. All moments, source-coordinate fields,
tail fields and raw geometry arrays are checked through their canonical digests.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frozen', required=True, type=Path)
    args = parser.parse_args()
    reference = json.loads((Path(__file__).resolve().parent / 'inputs/FROZEN_SOURCE_REFERENCE.json').read_text())
    if reference['format'] != 'a2048-frozen-source-scientific-reference-v1':
        raise ValueError('Unsupported reference format')
    checks = []
    for name, record in reference['json_outputs'].items():
        raw = (args.frozen / name).read_bytes()
        value = json.loads(raw)
        if name == 'candidate.json' and sha(raw) != reference['candidate_sha256']:
            raise ValueError('Candidate byte identity differs')
        excluded = record['excluded_non_scientific_fields']
        if excluded:
            value = {key: item for key, item in value.items() if key not in excluded}
        if sha(canonical(value)) != record['canonical_scientific_sha256']:
            raise ValueError(f'Scientific field digest mismatch: {name}')
        checks.append({'file': name, 'all_scientific_fields_equal': True,
                       'excluded_non_scientific_fields': excluded})
    with np.load(args.frozen / 'source_geometry.npz', allow_pickle=False) as data:
        records = reference['source_geometry_arrays']
        if set(data.files) != set(records):
            raise ValueError('Source geometry array set differs')
        for name, record in records.items():
            a = data[name]
            if (str(a.dtype) != record['dtype'] or list(a.shape) != record['shape']
                    or sha(a.tobytes(order='C')) != record['raw_C_order_sha256']):
                raise ValueError(f'Raw source geometry array differs: {name}')
        geometry = json.loads((args.frozen / 'geometry.json').read_text())
        if sha((args.frozen / 'source_geometry.npz').read_bytes()) != geometry['geometry_npz_sha256']:
            raise ValueError('Generated geometry archive is not bound by its metadata')
    print(json.dumps({'status': 'PASS', 'json_output_checks': checks,
                      'raw_geometry_arrays_checked': len(records),
                      'candidate_bytes_unchanged': True,
                      'scope': 'Complete frozen-source scientific-output comparison only; downstream T/G/Gamma/model/K/gates are separate stages.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
