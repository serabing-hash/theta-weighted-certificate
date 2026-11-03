#!/usr/bin/env python3
"""Small synthetic comparator-contract tests, not numerical regeneration tests.

Tests inject tiny independent fixture references into the helper function;
they never edit or replace the production reference used by the command line.
"""
from pathlib import Path
import copy
import hashlib
import json
import tempfile
import unittest

from verify_production_archives import digest, verify_stage


class ProductionArchiveContract(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.folder = Path(self.directory.name)
        self.raw = bytes(range(256)) * 9000
        (self.folder / 'array.bin').write_bytes(self.raw)
        self.result = {'status': 'CERT', 'candidate_sha256': 'fixture-identity',
                       'scientific_bound': '3/7', 'elapsed_seconds': 0.5}
        scientific = {k: v for k, v in self.result.items() if k != 'elapsed_seconds'}
        canonical = json.dumps(scientific, sort_keys=True, separators=(',', ':')).encode()
        self.reference = {
            'candidate_sha256': 'fixture-identity',
            'records': [{'stage': 'gamma', 'filename': 'array.bin',
                         'bytes': len(self.raw), 'sha256': hashlib.sha256(self.raw).hexdigest()}],
            'stage_results': {'gamma': {'scientific_canonical_sha256': hashlib.sha256(canonical).hexdigest(),
                                         'excluded_fields': ['elapsed_seconds']}}}
        self.save_result()

    def save_result(self):
        (self.folder / 'result.json').write_text(json.dumps(self.result))

    def test_streaming_hash_and_exact_fixture(self):
        self.assertEqual(digest(self.folder / 'array.bin'), hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(len(verify_stage(self.folder, 'gamma', self.reference)), 2)

    def test_same_size_changed_archive_rejected(self):
        (self.folder / 'array.bin').write_bytes(b'x' + self.raw[1:])
        with self.assertRaises(ValueError):
            verify_stage(self.folder, 'gamma', self.reference)

    def test_timing_only_ignored_but_scientific_change_rejected(self):
        self.result['elapsed_seconds'] = 123.5
        self.save_result()
        self.assertEqual(len(verify_stage(self.folder, 'gamma', self.reference)), 2)
        self.result['scientific_bound'] = '4/7'
        self.save_result()
        with self.assertRaises(ValueError):
            verify_stage(self.folder, 'gamma', self.reference)

    def test_fail_status_and_wrong_identity_rejected(self):
        for key, value in [('status', 'FAIL'), ('candidate_sha256', 'wrong')]:
            with self.subTest(key=key):
                old = self.result[key]
                self.result[key] = value
                self.save_result()
                with self.assertRaises(ValueError):
                    verify_stage(self.folder, 'gamma', self.reference)
                self.result[key] = old

    def test_unexpected_exclusions_rejected(self):
        changed = copy.deepcopy(self.reference)
        changed['stage_results']['gamma']['excluded_fields'].append('scientific_bound')
        with self.assertRaises(ValueError):
            verify_stage(self.folder, 'gamma', changed)


if __name__ == '__main__':
    unittest.main()
