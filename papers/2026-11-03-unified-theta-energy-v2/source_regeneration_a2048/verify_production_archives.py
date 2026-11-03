#!/usr/bin/env python3
"""Stream-check an explicitly recorded Gamma/model profile; no numerical inference."""
from pathlib import Path
import argparse
import hashlib
import json


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def verify_stage(folder, stage, reference):
    """Verify one stage against an explicitly supplied identity record."""
    checks = []
    records = [r for r in reference['records'] if r['stage'] == stage]
    if not records:
        raise ValueError('Stage has no expected production files')
    for record in records:
        path = folder / record['filename']
        if path.stat().st_size != record['bytes'] or digest(path) != record['sha256']:
            raise ValueError(f"Replay discrepancy in {stage}/{record['filename']}; do not replace the expected hash")
        checks.append({'stage': stage, 'file': record['filename'],
                       'bytes': record['bytes'], 'sha256': record['sha256'], 'match': True})
    result = json.loads((folder / 'result.json').read_text())
    if result['status'] != 'CERT' or result['candidate_sha256'] != reference['candidate_sha256']:
        raise ValueError(f'{stage} status/candidate mismatch')
    expected = reference['stage_results'][stage]
    if expected['excluded_fields'] != ['elapsed_seconds']:
        raise ValueError('Unexpected scientific-field exclusions')
    result.pop('elapsed_seconds')
    canonical = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    if hashlib.sha256(canonical).hexdigest() != expected['scientific_canonical_sha256']:
        raise ValueError(f'{stage} scientific result fields differ; do not replace the expected hash')
    checks.append({'stage': stage, 'file': 'result.json',
                   'scientific_canonical_sha256': expected['scientific_canonical_sha256'],
                   'excluded_fields': ['elapsed_seconds'], 'match': True})
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma', type=Path)
    parser.add_argument('--model', type=Path)
    parser.add_argument('--reference', type=Path,
                        help='Distinct recorded profile; default is the unchanged historical reference')
    args = parser.parse_args()
    if args.gamma is None and args.model is None:
        parser.error('Provide --gamma, --model, or both')
    reference_path = args.reference or (Path(__file__).resolve().parent / 'inputs/PRODUCTION_ARCHIVE_REFERENCE.json')
    reference = json.loads(reference_path.read_text())
    if reference['format'] not in ['a2048-original-production-array-identities-v1', 'a2048-corrected-production-array-identities-v1']:
        raise ValueError('Unsupported production reference')
    if reference['format'] == 'a2048-corrected-production-array-identities-v1':
        if reference.get('arithmetic_profile') != 'directed_integer_power_repair_v1':
            raise ValueError('Missing corrected arithmetic profile')
    checks = []
    for stage in ['gamma', 'model']:
        folder = getattr(args, stage)
        if folder is None: continue
        checks.extend(verify_stage(folder, stage, reference))
    print(json.dumps({'status': 'PASS', 'checks': checks,
                      'reference_format': reference['format'],
                      'reference_sha256': digest(reference_path),
                      'scope': 'Reference-identical production files and scientific stage-result fields, excluding only elapsed_seconds; not an independent numerical implementation or RH proof.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
