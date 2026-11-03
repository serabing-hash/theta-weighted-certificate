#!/usr/bin/env python3
"""Tie regenerated a2048 enclosure/gate matrices to the public exact-sign packet.

This comparison does not by itself prove that files were regenerated rather than
copied. Run the source pipeline first, retain its execution evidence, then run
this comparison and the separate exact integer sign checker.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import gzip
import hashlib
import json


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['frozen', 'T', 'G', 'K', 'exact-gate', 'conservative-gate']:
        parser.add_argument('--' + key, required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent.parent / 'reproducibility/inputs'
    provenance = json.loads((source / 'a2048_PROVENANCE.json').read_text())
    compressed = (source / 'a2048_saved_matrices.json.gz').read_bytes()
    if sha(compressed) != provenance['gzip_sha256']:
        raise ValueError('Public comparison input identity mismatch')
    raw = gzip.decompress(compressed)
    if sha(raw) != provenance['curated_json_sha256']:
        raise ValueError('Public mathematical-field identity mismatch')
    expected = json.loads(raw)
    candidate = expected['candidate_sha256']
    if sha((args.frozen / 'candidate.json').read_bytes()) != candidate:
        raise ValueError('Frozen candidate identity differs')
    source_record = json.loads((args.frozen / 'verified_components.json').read_text())
    if (source_record['status'] != 'CERT' or source_record['candidate_sha256'] != candidate
            or F(source_record['coordinates']['F_trial_scalar_lower']) != F(expected['F_lower'])):
        raise ValueError('Fresh source scalar differs from the exact-sign packet')
    reports = []
    for key in ['G', 'K', 'T']:
        record = json.loads(getattr(args, key).read_text())
        if record['status'] != 'CERT' or record['candidate_sha256'] != candidate:
            raise ValueError(f'{key} does not certify the same candidate')
        rows = record['matrix_numerators']; denominator = int(record['common_denominator'])
        entry = expected['matrices'][key]; target_den = int(entry['common_denominator'])
        if denominator <= 0 or len(rows) != 256 or any(len(row) != 256 for row in rows):
            raise ValueError(f'{key} has an invalid matrix shape/denominator')
        upper = entry['upper_triangle_rows']
        for i in range(256):
            for j in range(256):
                target = int(upper[i][j-i] if j >= i else upper[j][i-j])
                if int(rows[i][j]) * target_den != target * denominator:
                    raise ValueError(f'{key} entry ({i},{j}) differs')
        reports.append({'matrix': key, 'exact_entries_equal': 65536})
    for key, gate_path, status in [('exact', args.exact_gate, 'CERT'),
                                  ('conservative', args.conservative_gate, 'CERT_EXACT_INTEGER_SIGN')]:
        record = json.loads(gate_path.read_text())
        result = json.loads((gate_path.parent / 'result.json').read_text())
        target = expected['gates'][key]
        if (record['candidate_sha256'] != candidate or F(record['a']) != F(1, 2048)
                or F(record['penalty']) != F(target['penalty']) or result['status'] != status
                or F(result['gap']) != F(1, 2000)):
            raise ValueError(f'{key} gate identity, parameters or status differ')
        rows = record['matrix_numerators']; denominator = int(record['common_denominator'])
        target_den = int(target['common_denominator'])
        if denominator <= 0 or len(rows) != 256 or any(len(row) != 256 for row in rows):
            raise ValueError(f'{key} gate shape/denominator invalid')
        normalized = []
        for row in rows:
            converted = []
            for value in row:
                quotient, remainder = divmod(int(value) * target_den, denominator)
                if remainder: raise ValueError(f'{key} gate cannot match its saved denominator')
                converted.append(str(quotient))
            normalized.append(converted)
        view = {'common_denominator': str(target_den), 'matrix_numerators': normalized}
        if sha(canonical(view)) != target['canonical_matrix_sha256']:
            raise ValueError(f'{key} sufficient matrix differs')
        if key == 'exact':
            proof = result['interval_LDL_of_M_minus_gap_I']
            if (not proof['positive'] or len(proof['pivots']) != 256
                    or not all(0 < F(p['lower']) <= F(p['upper']) for p in proof['pivots'])):
                raise ValueError('Exact gate did not report 256 positive shifted pivots')
        reports.append({'gate': key, 'exact_entries_equal': 65536, 'reported_status': status})
    print(json.dumps({'status': 'PASS', 'candidate_sha256': candidate,
                      'source_scalar_equal': True, 'matrices': reports,
                      'scope': 'Equality of regenerated-file matrices to the public exact-sign inputs; source execution and exact sign replay are distinct checks.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
