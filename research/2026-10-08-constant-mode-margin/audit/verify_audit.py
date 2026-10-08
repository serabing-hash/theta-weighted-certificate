#!/usr/bin/env python3
"""CC BY-NC 4.0. Independent rational replay of saved constant-mode inputs.

No source, phase, H, FFT, physical integral, or eigensolver evaluation.
The physical inclusion premises are inherited, not regenerated here.
"""
from fractions import Fraction as Q
from pathlib import Path
import csv, hashlib, io, json, zipfile

SOURCE = Path('/workspace/shared/constant_mode_margin_20261008')
OUT = Path(__file__).resolve().parent

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def ball(record):
    midpoint, radius = map(int, record)
    assert radius >= 0
    return Q(midpoint-radius, 2**140), Q(midpoint+radius, 2**140)

def product(a, b):
    values = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
    return min(values), max(values)

def arctan_reciprocal(q, terms):
    lower = Q(0)
    upper = Q(0)
    # Each pair of adjacent partial sums brackets the alternating series.
    partial = Q(0)
    for j in range(terms+1):
        partial += Q((-1)**j, (2*j+1)*q**(2*j+1))
        if j == terms-1:
            first = partial
    return min(first, partial), max(first, partial)

def main():
    d = json.loads((SOURCE/'sources/constant_mode_inputs.json').read_text())
    assert d['column_zero_based'] == 0
    assert d['T_denominator_power_of_two'] == 30
    assert d['pole_denominator_power_of_two'] == d['phase_bits'] == 140
    archive = Path(d['source_archive']).read_bytes()
    assert digest(archive) == d['source_archive_sha256']
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        nested = z.read(d['nested_archive_member'])
    assert digest(nested) == d['nested_archive_sha256']
    prefix = 'SERABI_RH_FIXED_RANK32_ACTION_2026-10-07/'
    with zipfile.ZipFile(io.BytesIO(nested)) as z:
        for name, expected in d['member_sha256'].items():
            assert digest(z.read(name)) == expected
        old_t = list(csv.reader(io.StringIO(z.read(prefix+'sources/fixed_inputs/T32_dyadic_numerators.csv').decode())))
        assert [int(row[0]) for row in old_t] == d['T0_numerators']
        phase = json.loads(z.read(prefix+'outputs/PHASE_COEFFICIENT_ENCLOSURES.json'))
        assert phase['bits'] == 140 and phase['K'] == 8192
        assert phase['columns'][0] == d['phase_column0']
        assert phase['shifts'] == d['phase_shifts']
        assert len(phase['shifts']) == 124
        assert all(len(row) == 124 for row in d['phase_column0'])
        assert len(d['phase_column0']) == 3
        pole = json.loads(z.read(prefix+'outputs/FRAME_AND_POLE_ENCLOSURES.json'))
        assert pole['denominator_power_of_two'] == 140
        assert pole['pole_integrals'][0] == d['saved_pole_record']
        for r in range(3):
            base = json.loads(z.read(prefix+f'outputs/BASE_kappa_{r}.json'))
            assert {k:v for k,v in base.items() if k!='values'} == d['base_headers'][str(r)]
            for k, value in d['base_kappa_selected'][str(r)].items():
                assert base['values'][int(k)] == value
        inherited_audit = json.loads(z.read(prefix+'logs/CACHED_ALGEBRA_REPLAY.json'))
        assert inherited_audit['phase_inputs_exactly_checked'] == 32*124*3
        assert inherited_audit['verdict'] == 'PASS-CACHED-INTEGER-COEFFICIENT-ALGEBRA'
    t64_bytes = Path(d['T64_path']).read_bytes()
    assert digest(t64_bytes) == d['T64_sha256']
    new_t = list(csv.reader(io.StringIO(t64_bytes.decode())))
    assert len(new_t) == len(old_t) == 372
    assert all(len(row)==32 for row in old_t)
    assert all(len(row)==64 for row in new_t)
    assert all(a == b[:32] for a,b in zip(old_t,new_t))
    n,r = map(int,d['saved_pole_record'])
    coefficient_square_sum = sum(int(t)**2 for t in d['T0_numerators'])
    assert coefficient_square_sum == 574870339585334557
    norm_squared = Q(coefficient_square_sum,2**60)
    # Independently clear denominators for the saved-pole comparison.
    positive_comparison_integer = 64*(n-r)**2 - 127*coefficient_square_sum*2**220
    assert n-r > 0 and positive_comparison_integer > 0
    saved_c_lower = ball(d['saved_pole_record'])[0]**2/norm_squared
    total = (Q(0),Q(0))
    saved_count = tail_count = 0
    for r in range(3):
        for s,m in enumerate(d['phase_shifts']):
            assert m > 0 and isinstance(m,int)
            if m <= 8192:
                moment = ball(d['base_kappa_selected'][str(r)][str(m)])
                saved_count += 1
            else:
                radius = Q(2**20,2**(m//128))
                moment = (-radius,radius)
                tail_count += 1
            term = product(ball(d['phase_column0'][r][s]),moment)
            total = (total[0]+term[0],total[1]+term[1])
    a = arctan_reciprocal(5,16)
    b = arctan_reciprocal(239,8)
    pi = (16*a[0]-4*b[1],16*a[1]-4*b[0])
    assert Q(333,106)<pi[0]<pi[1]<Q(355,113)
    overlap = product((64*pi[0],64*pi[1]),total)
    recombined_c_lower = overlap[0]**2/norm_squared
    assert overlap[0]>0 and recombined_c_lower > Q(127,64)
    saved_pole = ball(d['saved_pole_record'])
    assert overlap[0] <= saved_pole[1] and saved_pole[0] <= overlap[1]
    original_result = json.loads((SOURCE/'outputs/EXACT_RESULT.json').read_text())
    assert str(saved_c_lower) == original_result['saved_pole_c_lower_exact']
    assert str(recombined_c_lower) == original_result['recombined_pole_c_lower_exact']
    assert list(map(str,overlap)) == original_result['recombined_pole_interval_exact']
    assert (saved_count,tail_count)==(315,57)
    delta=Q(1,64)
    lambda_barrier=saved_c_lower/(saved_c_lower+delta)
    assert lambda_barrier>Q(127,128)>Q(99,100)
    eps=Q(14194233101692862490101543299783481485,3284055810247577849424937639623597936869376)
    dsharp=Q(960589,4389760000000)
    rho=eps+dsharp
    assert str(rho)==original_result['fixed_cover_floor_exact']
    assert delta-rho>0
    status={
        'status':'PASS_CONDITIONAL_SAVED_DATA_ADVISORY',
        'license':'CC-BY-NC-4.0',
        'new_physical_evaluations':0,
        'archive_and_member_bindings_checked':True,
        'T32_T64_prefix_checked':True,
        'norm_squared_exact':str(norm_squared),
        'saved_pole_c_lower_exact':str(saved_c_lower),
        'cleared_denominator_comparison_positive':True,
        'recombined_pole_c_lower_exact':str(recombined_c_lower),
        'recombination_matches_original_exact_result':True,
        'saved_moments_read':saved_count,
        'analytic_tail_balls':tail_count,
        'lambda_delta64_lower_barrier_exact':str(lambda_barrier),
        'strict_simple_barrier':'lambda_max(B_1/64) > 127/128 > 99/100',
        'delta64_cover_eta_exact':str(delta-rho),
        'B_delta64_le_099I':'RULED_OUT_UNDER_STATED_PREMISES',
        'B_delta64_lt_I':'NOT_ESTABLISHED_OR_RULED_OUT_BY_THIS_AUDIT',
        'physical_source_inclusion_regenerated':False,
        'source_hashes':{str(p.relative_to(SOURCE)):digest(p.read_bytes()) for p in [SOURCE/'ADVISORY.md',SOURCE/'code/verify_constant_mode.py',SOURCE/'sources/constant_mode_inputs.json',SOURCE/'outputs/EXACT_RESULT.json']}
    }
    (OUT/'STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
    print(json.dumps(status,indent=2))

if __name__=='__main__':
    main()
