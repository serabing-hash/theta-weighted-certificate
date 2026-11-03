#!/usr/bin/env python3
"""Exact retained-margin replay using the original a2048 matrices and witness.

This verifies a fixed beta, not a parameter search or a new source regeneration.
The coefficient extraction retains all full-domain and enclosure premises of
the manuscript's margin-gain theorem. It does not establish the half bound/RH.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip
import json

import replay_saved_gates as base


def replay():
    folder = Path(base.__file__).resolve().parent / 'inputs'
    provenance = json.loads((folder / 'a2048_PROVENANCE.json').read_text())
    compressed = (folder / 'a2048_saved_matrices.json.gz').read_bytes()
    assert base.sha(compressed) == provenance['gzip_sha256']
    raw = gzip.decompress(compressed)
    assert base.sha(raw) == provenance['curated_json_sha256']
    x = json.loads(raw)
    assert x['format'] == 'theta-exact-triangular-extract-v2'
    assert x['source_sha256'] == provenance['source_sha256']
    assert x['candidate_sha256'] == provenance['candidate_sha256'] == 'a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d'
    assert x['source_sha256']['exact_witness'] == '8b86ae6a10de105df265e33b93698bd0614fb976549bb528acd493e5ad34ee2f'
    n = x['dimension']; assert n == 256
    a, nu, fl = F(x['a']), F(x['nu']), F(x['F_lower'])
    assert a == F(1, 2048) and nu == F(101891603714446529085721, 250172086796502324840759296) and fl > 0
    matrices = {}
    for name in ['G', 'K', 'T']:
        entry = x['matrices'][name]
        upper = entry['upper_triangle_rows']; assert len(upper) == n
        rows = [[0] * n for _ in range(n)]
        for i, row in enumerate(upper):
            assert len(row) == n-i
            for j, value in enumerate(row, i):
                rows[i][j] = rows[j][i] = int(value)
        den = int(entry['common_denominator']); assert den > 0
        assert base.sha(base.canonical(base.matrix_view(rows, den))) == entry['canonical_matrix_sha256']
        matrices[name] = rows, den
    G, gd = matrices['G']; K, kd = matrices['K']; T, td = matrices['T']
    gate = x['gates']['exact']; penalty = F(gate['penalty'])
    assert penalty == 4/nu + 5*a/nu**2 and F(gate['gap']) == F(1, 2000)
    M, md = base.exact_linear_combination([(F(4), T, td), (-5*a/4, G, gd), (-penalty, K, kd)], a*fl/4)
    original_den = int(gate['common_denominator']); assert original_den > 0
    normalized = []
    for row in M:
        current = []
        for value in row:
            quotient, remainder = divmod(value*original_den, md)
            assert remainder == 0
            current.append(quotient)
        normalized.append(current)
    assert base.sha(base.canonical(base.matrix_view(normalized, original_den))) == gate['canonical_matrix_sha256']
    U, ud = base.exact_linear_combination([(F(5, 4), G, gd), (5/nu**2, K, kd)], -fl/4)
    beta, m, g = F(10508819, 40000000000), F(1, 2000), 4060
    A, ad = base.exact_linear_combination([(F(1), M, md), (-beta, U, ud)], -m)
    # The original integer witness is used unchanged: no fit, rescaling or solve.
    sign = base.congruence_sign(A, ad, gate['witness_integer_rows'])
    upper_rows = [F(row[i]+sum(abs(v) for j, v in enumerate(row) if j != i), ud)
                  for i, row in enumerate(U)]
    upper = max(upper_rows)
    assert all(bound < g for bound in upper_rows)
    assert -(-upper.numerator // upper.denominator) == g
    alpha = (a+beta+m/g)/4
    h = alpha*nu/(alpha+nu)
    coefficient = F(1, 2)-a+h
    old = F(1, 2)-a+(a/4)*nu/(a/4+nu)
    rounded = F(499640243163, 10**12)
    ceiling = F(1, 2)-a+nu
    assert alpha == F(6099134007, 32480000000000)
    assert coefficient == F(2415896663121887366359985794094352519, 4835272370827926282795053961934979072)
    assert old == F(542006223062224701317434549, 1084868104425248291110985728)
    assert old < rounded < coefficient < ceiling < F(1, 2)
    # Coefficients of the exact Hilbert-space square completion; no H-orthogonality is assumed.
    assert alpha-h == alpha**2/(alpha+nu) and nu-h == nu**2/(alpha+nu)
    assert h == alpha*nu/(alpha+nu)
    return {
        'status': 'PASS', 'candidate_sha256': x['candidate_sha256'],
        'original_witness_sha256': x['source_sha256']['exact_witness'],
        'unchanged_original_witness': True, 'reconstructed_M_entries': n*n,
        'retained_matrix': 'M - m I - beta U', 'beta': str(beta), 'm': str(m),
        'retained_matrix_sign': sign, 'g': g, 'positive_U_row_gaps': n,
        'maximum_exact_U_row_bound': str(upper), 'alpha': str(alpha),
        'conditional_coefficient': str(coefficient), 'rounded_down_coefficient': str(rounded),
        'old_coefficient': str(old), 'positive_gain': str(coefficient-old),
        'fixed_complement_method_ceiling': str(ceiling),
        'scope': 'Exact stored-matrix retained margin and conditional scalar extraction only. Same frozen input and original witness; no source regeneration, new parameter search, global half bound or RH proof.'}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without Python -O: assertions are verification gates.')
    print(json.dumps(replay(), indent=2, sort_keys=True))
