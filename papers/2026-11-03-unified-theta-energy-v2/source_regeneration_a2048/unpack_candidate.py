#!/usr/bin/env python3
"""Restore the unchanged exact frozen candidate; does not compute enclosures."""
from pathlib import Path
import argparse
import gzip
import hashlib
import io
import json

EXPECTED_GZIP = 'e5a90ee5549cca66d3f28192728ecedf3f31c32fe7c189cb7ad52da0d8182b7c'
EXPECTED_CANDIDATE = 'a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d'
EXPECTED_BYTES = 32902215


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    path = Path(__file__).resolve().parent / 'inputs/candidate.json.gz'
    compressed = path.read_bytes()
    if hashlib.sha256(compressed).hexdigest() != EXPECTED_GZIP:
        raise ValueError('Compressed input identity mismatch')
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
        raw = stream.read(EXPECTED_BYTES + 1)
    if len(raw) != EXPECTED_BYTES or hashlib.sha256(raw).hexdigest() != EXPECTED_CANDIDATE:
        raise ValueError('Exact candidate identity mismatch')
    packet = json.loads(raw)
    if (packet['a'], packet['B'], packet['k'], packet['n'], packet['h']) != (
            '1/2048', 'log(8)/2', 256, 3072, '1/2560'):
        raise ValueError('Unexpected candidate parameters')
    if args.output.exists():
        if args.output.read_bytes() != raw:
            raise FileExistsError('Refusing to overwrite a different existing candidate')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as handle:
            handle.write(raw)
    print(json.dumps({'status': 'PASS', 'candidate_sha256': EXPECTED_CANDIDATE,
                      'bytes': len(raw), 'scope': 'Frozen input restoration only; no source regeneration.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
