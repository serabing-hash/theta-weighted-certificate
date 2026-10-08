#!/usr/bin/env python3
"""CC BY-NC 4.0. Exact cached interval algebra; no numerical operators.

Both results are conditional on the explicitly identified saved whole-line
source and phase enclosure inclusions. This does not regenerate those inputs.
"""
import argparse, csv, hashlib, io, json, resource, time, zipfile
from fractions import Fraction as F
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def interval(pair, bits=140):
    n, r = map(int, pair)
    assert r >= 0
    return F(n-r, 1<<bits), F(n+r, 1<<bits)


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def mul(a, b):
    q = [x*y for x in a for y in b]
    return min(q), max(q)


def atan(q, n):
    s = sum((F((-1)**j, (2*j+1)*q**(2*j+1)) for j in range(n)), F(0))
    e = F(1, (2*n+1)*q**(2*n+1))
    return (s-e, s) if n % 2 else (s, s+e)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source_bindings(d):
    """Optional byte checks against already existing release; no extraction run."""
    raw = Path(d['source_archive']).read_bytes()
    assert sha(raw) == d['source_archive_sha256']
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        ar = outer.read(d['nested_archive_member'])
    assert sha(ar) == d['nested_archive_sha256']
    prefix = 'SERABI_RH_FIXED_RANK32_ACTION_2026-10-07/'
    with zipfile.ZipFile(io.BytesIO(ar)) as z:
        for name, digest in d['member_sha256'].items():
            assert sha(z.read(name)) == digest
        phases = json.loads(z.read(prefix+'outputs/PHASE_COEFFICIENT_ENCLOSURES.json'))
        assert phases['columns'][0] == d['phase_column0']
        assert phases['shifts'] == d['phase_shifts']
        poles = json.loads(z.read(prefix+'outputs/FRAME_AND_POLE_ENCLOSURES.json'))
        assert poles['pole_integrals'][0] == d['saved_pole_record']
        oldT = list(csv.reader(io.StringIO(z.read(prefix+'sources/fixed_inputs/T32_dyadic_numerators.csv').decode())))
        assert [int(row[0]) for row in oldT] == d['T0_numerators']
        for r in range(3):
            base = json.loads(z.read(prefix+f'outputs/BASE_kappa_{r}.json'))
            for k, pair in d['base_kappa_selected'][str(r)].items():
                assert pair == base['values'][int(k)]
    traw = Path(d['T64_path']).read_bytes()
    assert sha(traw) == d['T64_sha256']
    newT = list(csv.reader(io.StringIO(traw.decode())))
    assert len(newT) == len(oldT) == 372
    assert all(a == b[:32] for a, b in zip(oldT, newT))


def verify(bind_sources=False):
    start = time.monotonic()
    d = json.loads((ROOT/'sources/constant_mode_inputs.json').read_text())
    assert d['column_zero_based'] == 0
    assert d['T_denominator_power_of_two'] == 30
    assert d['pole_denominator_power_of_two'] == d['phase_bits'] == 140
    if bind_sources:
        source_bindings(d)
    t = [F(n, 1<<30) for n in d['T0_numerators']]
    assert len(t) == 372
    norm2 = sum((x*x for x in t), F(0))
    assert norm2 > 0
    saved = interval(d['saved_pole_record'])
    assert saved[0] > 0
    c_saved = saved[0]**2/norm2
    assert c_saved > F(127,64) > F(99,64)

    # Read and combine EXISTING phase enclosures. No new phase/source array.
    # Stored positive Fourier coefficients of P_0 are p_r at m_s; the
    # negative coefficients are p_r for even r and -p_r for odd r. With
    # odd components imaginary, the zero-frequency product is +2 p_r d_r
    # for all r. Thus integral kappa P_0 = 64*pi * sum_{r,s} p_rs d_rs.
    a, b = atan(5, 16), atan(239, 8)
    pi = (16*a[0]-4*b[1], 16*a[1]-4*b[0])
    assert F(333,106) < pi[0] < pi[1] < F(355,113)
    total = (F(0), F(0))
    used = tail = 0
    for r in range(3):
        h = d['base_headers'][str(r)]
        assert h['kind'] == 'kappa' and h['source_power'] == r
        assert h['K'] == 8192 and h['denominator_power_of_two'] == 140
        assert h['component'] == ('imag' if r%2 else 'real')
        for s, m in enumerate(d['phase_shifts']):
            phase = interval(d['phase_column0'][r][s])
            if m <= 8192:
                base = interval(d['base_kappa_selected'][str(r)][str(m)])
                used += 1
            else:
                # Inherited analytic |d_r,m| <= 2^20 exp(-m/128).
                # e > 2 gives the deliberately coarser exact dyadic ball.
                n = m//128
                e = F(1<<20, 1<<n)
                base = (-e, e)
                tail += 1
            total = add(total, mul(phase, base))
    recombined = mul((64*pi[0], 64*pi[1]), total)
    assert recombined[0] > 0
    assert recombined[0] <= saved[1] and saved[0] <= recombined[1]
    c_cache = recombined[0]**2/norm2
    assert c_cache > F(127,64) > F(99,64)
    assert F(127,64)/(F(127,64)+F(1,64)) == F(127,128) > F(99,100)
    eta32 = F(2893974301919559083402996479244366770223445381007,
              92620636523388719034562694367509285563269120000000)
    cover_floor = F(1,32)-eta32
    dsharp = F(960589,4389760000000)
    eps = F(14194233101692862490101543299783481485,
            3284055810247577849424937639623597936869376)
    assert cover_floor == dsharp+eps > 0
    return {
        'status': 'PASS_EXACT_ALGEBRA_CONDITIONAL_ON_IDENTIFIED_INPUT_INCLUSIONS',
        'license': 'CC-BY-NC-4.0',
        'source_bindings_checked': bind_sources,
        't0_norm_squared_exact': str(norm2),
        'saved_pole_interval_exact': list(map(str, saved)),
        'saved_pole_c_lower_exact': str(c_saved),
        'recombined_pole_interval_exact': list(map(str, recombined)),
        'recombined_pole_c_lower_exact': str(c_cache),
        'certified_simple_statement': 'c > 127/64; hence lambda_max(B_1/64) > 127/128 > 99/100',
        'fixed_cover_floor_exact': str(cover_floor),
        'epsilon_cover_exact': str(eps), 'dsharp_exact': str(dsharp),
        'counts': {'saved_phase_records_read': used+tail,
                   'saved_moment_records_read': used, 'tail_balls': tail,
                   'new_H_actions': 0, 'new_phase_arrays': 0,
                   'new_source_evaluations': 0, 'new_FFT': 0,
                   'new_physical_Gram_integrals': 0, 'eigensolves': 0},
        'resources': {'wall_seconds': time.monotonic()-start,
                      'peak_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--bind-sources', action='store_true')
    p.add_argument('--emit', action='store_true')
    args = p.parse_args()
    result = verify(args.bind_sources)
    if args.emit:
        (ROOT/'outputs/EXACT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
