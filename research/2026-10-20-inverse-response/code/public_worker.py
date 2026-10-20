#!/usr/bin/env python3
"""Derivative reader arithmetic worker; not the historical launch/resource chain.

Publication validation is static only. Run only through the package's bounded
one-shot supervisor. This worker never fetches files. Original checker sources
remain byte-identical; only filesystem and historical admission are replaced.
The original run/evaluate and all scientific arithmetic statements are retained.
"""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import types

FORMAT = 'INVERSE_RESPONSE_PUBLIC_INPUTS_V1'
SOURCES = {
    'shared': ('code/shared_checker.py', 33411, 'c00ff1771829543fadb1ba6e2d1a902a541ae1f2bee2132c91c70e5560d2a692'),
    'rank-one': ('code/rank_one_checker.py', 24884, 'feb274cd51d46897f75ed3872c32e6ea161486f6942c435cf3180f7b47e8a27e'),
}
REFERENCES = {
    'shared': ('results/shared_error.json', 129711, '1d8335c6f041d561f26d021663620d17e98e54f10854c5f9368c1f92617567b1'),
    'rank-one': ('results/rank_one.json', 178084, '176d95a7ae6297cd444488bf2c90613ce34a6806d2729589f60dcd1c22dddbf7'),
}
ORDER_SOURCE_HASHES = {
    'saved68_order_worker_source': '981d2894e9fbea5f5d7964962c39be83c79566dbcecf6b6568bfc22558a91e7e',
    'saved68_order_checker_source': '0129a808a19611048d89cab92c9f5ecdd3abf47cd3dc58d13b5d27041684c622',
}
COLUMN_ORDER = {
    'old_coefficient_indices': list(range(64)),
    'new_coefficient_indices': [64, 65, 66, 67],
    'new_source_columns': [0, 1, 2, 3],
    'action_arrays': ['old_B', 'new_B'],
}
# SHA-256 and byte sizes copied from the accepted original input manifest.
DEPENDENCY_PINS = {'saved_A160': {'bytes': 5942796, 'sha256': '58dbcee3c0650984f0cc946d4ed6db08e9551b582fc3a97198d87d6e1bd44300'}, 'saved_SHIFT_SCALARS': {'bytes': 23704, 'sha256': '3d13e17b7a03fdb976e1467bf33eda0e5360b4a35d9c1d21329d690555ccb377'}, 'saved_P_UP_EXACT': {'bytes': 447716, 'sha256': 'acab1e0af409919a3346663ad2c75d6df0f1f632443d1f06c0a9a24dc3ce4a29'}, 'saved_N160': {'bytes': 308806, 'sha256': '4ab4461ade2a35e6e074d16397bf28c261b50a3a0240f20c9858d7803410927d'}, 'saved_F160': {'bytes': 297034, 'sha256': '5bf84d32de849f7c66aee70c9b9d80a2d6c15c79b68d168c6d9569f5767db967'}, 'saved_D160': {'bytes': 1252355, 'sha256': '43795512abcc3666d539b941d74ab23bbc1e1dc00756c6823f411e1171f2ab84'}, 'saved_K160': {'bytes': 1498926, 'sha256': '662533a397a7b52aafd48cb7c8b9218a7b4fcaded9cc698ec9bd08d218b2f2c9'}, 'original_norm': {'bytes': 239044, 'sha256': '3fbd0d8a8b289f73e6d854b2192d248e436b5e8154de79441e4c56f4408dfac3'}, 'witness_vector': {'bytes': 6568, 'sha256': '9f659a0426dcf7f1e25f9602daae30bdf5d7d16c766fc082c296bf676d996fcb'}, 'coefficient_report': {'bytes': 54413, 'sha256': 'ffc27e0dc16e5d3f4e1cb2a1cdedd67c2f9e91dc98d641ea7b46ad8f4b57c692'}}
PUBLIC_BASE = ('https://raw.githubusercontent.com/serabing-hash/theta-weighted-certificate/'
               'f61c7af23c7e4027cc3cb768faa40273f1146ffd/'
               'research/2026-10-18-coefficient-obstruction/')
OMIT_FROM_REPORT_COMPARISON = frozenset({'input_manifest_sha256', 'input_sha256', 'admission'})


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    def unique(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def safe_file(root, relative):
    need(type(relative) is str, 'non-string relative path')
    rel = Path(relative)
    need(relative and not rel.is_absolute() and '..' not in rel.parts and
         str(rel) == relative and '\\' not in relative, 'unsafe/noncanonical package path')
    current = root
    for part in rel.parts:
        current = current / part
        need(not current.is_symlink(), 'symlink in package path')
    need(current.resolve().is_relative_to(root) and current.is_file(), 'missing/escaped package file')
    return current


def bound_bytes(root, relative, size, expected):
    need(type(size) is int and size >= 0 and type(expected) is str and
         re.fullmatch('[0-9a-f]{64}', expected), 'invalid byte binding')
    path = safe_file(root, relative)
    need(path.stat().st_size == size, 'size mismatch: ' + relative)
    data = path.read_bytes()
    need(digest(data) == expected, 'hash mismatch: ' + relative)
    return data


def package_admission(root):
    manifest_path = safe_file(root, 'PACKAGE_MANIFEST.json')
    package = decode(manifest_path.read_bytes())
    need(type(package.get('files')) is list, 'package manifest files required')
    seen = set()
    for row in package['files']:
        need(type(row) is dict and {'path', 'bytes', 'sha256'} <= set(row), 'package manifest row')
        need(row['path'] not in seen and row['path'] != 'PACKAGE_MANIFEST.json', 'duplicate/self manifest path')
        seen.add(row['path'])
        bound_bytes(root, row['path'], row['bytes'], row['sha256'])
    required = {'INPUTS.json', 'code/public_worker.py'}
    required.update(row[0] for row in SOURCES.values())
    required.update(row[0] for row in REFERENCES.values())
    need(required <= seen, 'missing core package bindings')
    inputs_path = safe_file(root, 'INPUTS.json')
    inputs_bytes = inputs_path.read_bytes()
    spec = decode(inputs_bytes)
    need(spec.get('format') == FORMAT and set(spec.get('dependencies', {})) == set(DEPENDENCY_PINS),
         'exact public dependency role allowlist')
    need(spec.get('original_source_hashes') == ORDER_SOURCE_HASHES and
         spec.get('column_order') == COLUMN_ORDER, 'fixed public source/order metadata')
    for role, pin in DEPENDENCY_PINS.items():
        row = spec['dependencies'][role]
        expected_path = 'dependencies/' + role + '.json'
        public_path = 'results/coefficient_check.json' if role == 'coefficient_report' else 'inputs/' + role + '.json'
        need(row.get('path') == expected_path and row.get('bytes') == pin['bytes'] and
             row.get('sha256') == pin['sha256'] and row.get('url') == PUBLIC_BASE + public_path,
             'pinned original scientific input: ' + role)
        bound_bytes(root, expected_path, pin['bytes'], pin['sha256'])
    for relative, size, expected in list(SOURCES.values()) + list(REFERENCES.values()):
        bound_bytes(root, relative, size, expected)
    return inputs_path, inputs_bytes, spec


def verified_module(root, kind):
    relative, size, expected = SOURCES[kind]
    data = bound_bytes(root, relative, size, expected)
    module = types.ModuleType('public_bound_' + kind.replace('-', '_'))
    module.__file__ = str(root / relative)
    module.__cached__ = None
    # Runtime only: this function is not called by static publication validation.
    exec(compile(data, module.__file__, 'exec', dont_inherit=True, optimize=0), module.__dict__)
    return module, data


def replace_shared_admission_bodies(module, source):
    """Extract unchanged original statement blocks; no arithmetic reimplementation.

    admit_cache: keep original witness/cache parsing tail, starting at v=read.
    admit_column_bounds: keep exact order assignment/assertion and norm-to-return
    tail; discard only prior path/host/output provenance admission statements.
    """
    tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}

    def assignment_index(body, target):
        hits = [i for i, node in enumerate(body) if isinstance(node, ast.Assign) and
                any(isinstance(t, ast.Name) and t.id == target for t in node.targets)]
        need(len(hits) == 1, 'unique original admission boundary: ' + target)
        return hits[0]

    cache = copy.deepcopy(functions['admit_cache'])
    scientific_cache_gates = [node for node in cache.body if isinstance(node, ast.Expr) and
        isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and
        node.value.func.id == 'need' and any(
            isinstance(part, ast.Subscript) and isinstance(part.value, ast.Name) and
            part.value.id == 'old' and isinstance(part.slice, ast.Constant) and
            part.slice.value == 'format' for part in ast.walk(node))]
    need(len(scientific_cache_gates) == 1, 'original scientific cache admission gate')
    start = assignment_index(cache.body, 'v')
    cache.body = cache.body[start:]
    # The retained cache tail refers to old; public admission supplies only the
    # byte-pinned predecessor mathematical report, not invented process records.
    prefix = ast.parse("old = inp.read('coefficient_report')").body
    cache.body = prefix + scientific_cache_gates + cache.body
    column = copy.deepcopy(functions['admit_column_bounds'])
    order_start = assignment_index(column.body, 'order')
    norm_start = assignment_index(column.body, 'norm')
    need(isinstance(column.body[order_start + 1], ast.Expr), 'original order assertion boundary')
    column.body = column.body[order_start:order_start + 2] + column.body[norm_start:]
    selected = ast.fix_missing_locations(ast.Module(body=[cache, column], type_ignores=[]))
    exec(compile(selected, module.__file__ + ':public-admission-selection', 'exec',
                 dont_inherit=True, optimize=0), module.__dict__)


def public_inputs_class(root, inputs_path, inputs_bytes, spec, kind):
    class PublicInputs:
        def __init__(self, manifest_path):
            need(Path(manifest_path) == inputs_path and inputs_path.read_bytes() == inputs_bytes,
                 'unchanged public input manifest')
            self.manifest_path = inputs_path
            self.m = {'source_root': str(root), 'column_order': spec['column_order']}
            if kind == 'shared':
                self.rows = dict(spec['dependencies'])
            else:
                rel, size, expected = REFERENCES['shared']
                self.rows = {
                    'accepted_report': {'path': rel, 'bytes': size, 'sha256': expected},
                    'nu_scalar': dict(spec['dependencies']['saved_SHIFT_SCALARS']),
                }
            self.paths = {role: safe_file(root, row['path']) for role, row in self.rows.items()}
            self.verify()

        def verify(self):
            need(inputs_path.read_bytes() == inputs_bytes, 'public manifest changed')
            for row in self.rows.values():
                bound_bytes(root, row['path'], row['bytes'], row['sha256'])

        def read(self, role):
            row = self.rows[role]
            return decode(bound_bytes(root, row['path'], row['bytes'], row['sha256']))

        def h(self, role):
            return self.rows[role]['sha256'] if role in self.rows else ORDER_SOURCE_HASHES[role]
    return PublicInputs


def rank_public_admission(inp):
    """Retain scientific cache/convention admission, omit private process claims."""
    report = inp.read('accepted_report')
    need(inp.h('accepted_report') == REFERENCES['shared'][2], 'fixed accepted report')
    need(report['format'] == 'FIXED_C_SHARED_ERROR_DIRECTION_SCREEN_V1' and
         report['scope'] == 'DELTA128_FIXED_C_SHARED_ERROR_DIRECTION_SCREEN_ONCE_V1' and
         report['status'] == 'EXACT-SHARED-ERROR-SCREEN-COMPLETE' and report['stage'] == 'complete',
         'completed shared-error scientific report')
    need(report['numerical_status'] == report['decisions']['shared_error']['status'] ==
         'CONDITIONAL-FIXED-SHARED-ERROR-MAJORANT-EXCLUDED', 'prior exclusion scope')
    need(report['P_up_representation'] == 'EXACT-RATIONAL-NO-SWITCH' and
         report['physical_P_radius_or_UCERT_pad_added'] is False and
         report['eta_is_exact_columnwise_e'] is True and report['unknown_slack_contracted'] is False and
         report['repeated_coefficients_collected_before_radii'] is True, 'physical padding conventions')
    need(report['cache_reuse']['c_Cv_and_n_vv'] == 'ACCEPTED-EXACT-CACHE-NOT-RECOMPUTED' and
         report['cache_reuse']['coefficient_report_sha256'] == DEPENDENCY_PINS['coefficient_report']['sha256'],
         'inherited coefficient cache')
    order = report['column_bound_admission']
    need(order['terms'] == 68 and order['sum_of_squares_identity_verified'] is True and
         order['sigma_bar_square_dominates_sigma2'] is True and order['column_order'] == COLUMN_ORDER,
         'accepted exact 64+4 error order and budgets')
    scalar = inp.read('nu_scalar')
    need(inp.h('nu_scalar') == DEPENDENCY_PINS['saved_SHIFT_SCALARS']['sha256'] and
         report['input_sha256']['saved_SHIFT_SCALARS'] == inp.h('nu_scalar'), 'same original scalar binding')
    need(scalar['model_id'] == 'DELTA128_PUP68_NEW_C_V1' and
         scalar['trial_gram_majorant'] == 'P<=P_up<=nu68^2 I' and
         scalar['physical_errors_unchanged'] is True, 'same admitted nu convention')
    return report, scalar['values'], {
        'status': 'PUBLIC-DERIVATIVE-SCALAR-ADMISSION',
        'accepted_report_sha256': inp.h('accepted_report'),
        'nu_scalar_sha256': inp.h('nu_scalar'),
        'physical_inclusions_reproved': False,
        'historical_host_chain_recreated': False,
    }


def comparison_tree(report):
    return {key: value for key, value in report.items() if key not in OMIT_FROM_REPORT_COMPARISON}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind', choices=['shared', 'rank-one'], required=True)
    parser.add_argument('--package-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and not sys.flags.optimize,
         'worker requires isolated python -I -S -B without optimization')
    need(args.package_root.is_absolute() and args.package_root == args.package_root.resolve(),
         'canonical absolute package root required')
    root = args.package_root
    out = args.output_dir
    need(out.is_absolute() and not out.exists() and not out.is_symlink() and
         out.parent.is_dir() and out.parent == out.parent.resolve(), 'fresh canonical output directory required')
    need(not out.is_relative_to(root), 'write replay output outside immutable package')
    inputs_path, inputs_bytes, spec = package_admission(root)
    module, source = verified_module(root, args.kind)
    module.Inputs = public_inputs_class(root, inputs_path, inputs_bytes, spec, args.kind)
    if args.kind == 'shared':
        replace_shared_admission_bodies(module, source)
    else:
        module.admit_previous = rank_public_admission
    os.environ['SHIFT_CHARGED_EXACT_CHECK'] = '1'
    os.environ['SHIFT_INPUT_SHA256'] = digest(inputs_bytes)
    report = module.run(str(root), str(inputs_path), str(out), lambda: None)
    expected_status = ('EXACT-SHARED-ERROR-SCREEN-COMPLETE' if args.kind == 'shared'
                       else 'EXACT-RANK-ONE-SCALAR-SCREEN-COMPLETE')
    need(report.get('status') == expected_status and report.get('stage') == 'complete',
         'HOLD or incomplete report is not replay success')
    reference = decode(bound_bytes(root, *REFERENCES[args.kind]))
    need(comparison_tree(report) == comparison_tree(reference), 'saved mathematical report tree mismatch')
    # Recheck all package/dependency bytes after arithmetic before a success record.
    package_admission(root)
    summary = {
        'format': 'PUBLIC_DERIVATIVE_REPLAY_RESULT_V1',
        'status': 'EXACT-MATHEMATICAL-REPORT-MATCH', 'kind': args.kind,
        'numerical_status': report['numerical_status'],
        'report_sha256': digest((out / 'INDEPENDENT_CHECK.json').read_bytes()),
        'reference_report_sha256': REFERENCES[args.kind][2],
        'original_checker_sha256': SOURCES[args.kind][2],
        'public_inputs_sha256': digest(inputs_bytes),
        'comparison': 'full report trees excluding only listed provenance keys; exact strings and values',
        'excluded_provenance_keys': sorted(OMIT_FROM_REPORT_COMPARISON),
        'historical_host_chain_recreated': False, 'resource_acceptance_claimed_by_worker': False,
        'physical_inclusions_reproved': False, 'RH_PROOF': 'NOT-OBTAINED',
    }
    with (out / 'PUBLIC_REPLAY_RESULT.json').open('x') as stream:
        json.dump(summary, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print(json.dumps({'status': summary['status'], 'numerical_status': summary['numerical_status']}, sort_keys=True))


if __name__ == '__main__':
    main()
