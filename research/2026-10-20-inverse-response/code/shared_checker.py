"""One charged fixed-C/fixed-v shared-error cap screen. No mathematical work on import.

Reuses the accepted exact c=Cv and n=v*v, without recomputing either.
Seven declared direction contractions plus one68-term error radius; no source/native/solver imports.
The inherited physical inclusions remain conditional. Pending code review.
"""
import gc
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from fractions import Fraction as Q

SCOPE = 'DELTA128_FIXED_C_SHARED_ERROR_DIRECTION_SCREEN_ONCE_V1'
CACHE_SCOPE = 'DELTA128_SAME_DIRECTION_COEFFICIENT_GAP_EXACT_ONCE_V1'
PRODUCTION_SCOPE = 'DELTA128_PUP68_NEW_C_FULL372_ONCE_V1'
WITNESS_SCOPE = 'DELTA128_PIVOT210_SAME_DIRECTION_DIAGNOSTIC_ONCE_V1'
RANK, WIDTH, FULL = 68, 211, 372
BITS, WBITS, CBITS, MAXBITS = 160, 80, 160, 1024
SCALAR_DIGITS = 100000
# Additional conservative operation gate, within the existing scalar parser cap.
# Dense matrix/vector arithmetic NEVER enters this separate scalar path.
SCALAR_BITS = 332193
MODEL = 'alpha*M-B^*C-C^*B+C^*S*C; B=alpha*K-p*D; S=alpha*N-q*F+k*P_up+beta*I'
_guard = lambda: None


class Hold(RuntimeError):
    """Admission/model/arithmetic failure, never a scientific conclusion."""


def need(ok, label):
    if not ok:
        raise Hold(label)


def gate(x):
    need(type(x) is int and x.bit_length() <= MAXBITS, 'dense1024-bit ceiling')
    return x


def integer(s):
    need(type(s) is str and len(s) <= 310 and
         re.fullmatch(r'0|-?[1-9][0-9]*', s) is not None,
         'canonical bounded dense integer')
    return gate(int(s))


def add(a, b):
    gate(a); gate(b)
    if not a: return b
    if not b: return a
    need(max(a.bit_length(), b.bit_length()) + 1 <= MAXBITS,
         'dense addition pre-operation ceiling')
    return gate(a + b)


def mul(a, b):
    gate(a); gate(b)
    if not a or not b: return 0
    need(a.bit_length() + b.bit_length() <= MAXBITS,
         'dense product pre-operation ceiling')
    return gate(a * b)


def isigsum(values):
    total = 0
    for value in values:
        total = add(total, value)
    return total


def sg(q):
    need(type(q) is Q and q.denominator > 0 and
         q.numerator.bit_length() <= SCALAR_BITS and
         q.denominator.bit_length() <= SCALAR_BITS, 'scalar rational ceiling')
    return q


def sint_product(a, b):
    need(type(a) is int and type(b) is int and
         a.bit_length() <= SCALAR_BITS and b.bit_length() <= SCALAR_BITS,
         'bounded scalar operands')
    if not a or not b: return 0
    need(a.bit_length() + b.bit_length() <= SCALAR_BITS,
         'scalar product pre-operation ceiling')
    _guard()
    return a * b


def sint_add(a, b):
    need(type(a) is int and type(b) is int and
         a.bit_length() <= SCALAR_BITS and b.bit_length() <= SCALAR_BITS,
         'bounded scalar addends')
    if not a: return b
    if not b: return a
    need(max(a.bit_length(), b.bit_length()) + 1 <= SCALAR_BITS,
         'scalar addition pre-operation ceiling')
    return a + b


def sadd(a, b):
    sg(a); sg(b)
    n = sint_add(sint_product(a.numerator, b.denominator),
                 sint_product(b.numerator, a.denominator))
    d = sint_product(a.denominator, b.denominator)
    _guard(); result = sg(Q(n, d)); _guard()
    return result


def ssub(a, b):
    return sadd(a, -sg(b))


def smul(a, b):
    sg(a); sg(b)
    n = sint_product(a.numerator, b.numerator)
    d = sint_product(a.denominator, b.denominator)
    _guard(); result = sg(Q(n, d)); _guard()
    return result


def sdiv(a, b):
    sg(a); sg(b); need(b.numerator != 0, 'nonzero scalar divisor')
    return smul(a, Q(b.denominator, b.numerator))


def scmp(a, b):
    delta = ssub(a, b)
    return (delta.numerator > 0) - (delta.numerator < 0)


def ssum(values):
    total = Q(0)
    for value in values: total = sadd(total, value)
    return total


def rational(s):
    need(type(s) is str and
         re.fullmatch(r'(0|-?[1-9][0-9]*)(/[1-9][0-9]*)?', s) is not None,
         'canonical scalar rational')
    need(all(len(part.lstrip('-')) <= SCALAR_DIGITS for part in s.split('/')),
         'unchanged scalar input digit ceiling')
    _guard(); result = sg(Q(s)); _guard()
    return result


def st(q):
    sg(q); _guard(); result = str(q); _guard()
    need(all(len(part.lstrip('-')) <= SCALAR_DIGITS for part in result.split('/')),
         'bounded scalar output encoding')
    return result


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while block := f.read(1 << 20):
            h.update(block); _guard()
    return h.hexdigest()


def load(path):
    def unique(items):
        out = {}
        for key, value in items:
            need(key not in out, 'duplicate JSON key'); out[key] = value
        return out
    _guard(); result = json.loads(Path(path).read_bytes(), object_pairs_hook=unique); _guard()
    return result


def save(path, obj):
    _guard(); raw = (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()
    with Path(path).open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    need(Path(path).read_bytes() == raw, 'durable report byte readback')
    fd = os.open(Path(path).parent, os.O_RDONLY | os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)
    _guard()


class Inputs:
    def __init__(self, manifest_path):
        self.manifest_path = Path(manifest_path)
        need(sha(self.manifest_path) == os.environ['SHIFT_INPUT_SHA256'],
             'input manifest admission')
        self.m = load(self.manifest_path)
        need(self.m['format'] == 'SHARED_ERROR_SAVED_INPUTS_V1' and self.m['scope'] == SCOPE and
             self.m['upstream_coefficient_cache_review'] == 'GO' and
             self.m['P_up_representation'] == 'EXACT-RATIONAL-NO-SWITCH', 'fixed scope/cache admission')
        self.rows = self.m['bindings']; self.paths = {}
        for role, row in self.rows.items():
            p = Path(row['path'])
            need(p.is_absolute() and p.resolve() == p and not p.is_symlink(),
                 'canonical input path ' + role)
            self.paths[role] = p
        self.verify()

    def verify(self):
        for role, row in self.rows.items():
            p = self.paths[role]; _guard()
            need(p.is_file() and p.stat().st_size == row['bytes'] and
                 sha(p) == row['sha256'], 'immutable input bytes ' + role)

    def read(self, role):
        return load(self.paths[role])

    def h(self, role):
        return self.rows[role]['sha256']


def selected_rows(raw, shape, selected):
    nr, nc = shape; sr, sc = selected
    need(type(raw) is list and len(raw) == nr and
         all(type(row) is list and len(row) == nc for row in raw), 'full stored shape')
    need(0 < sr <= nr and 0 < sc <= nc, 'selected shape')
    result = []
    for i in range(sr):
        _guard(); result.append([integer(raw[i][j]) for j in range(sc)])
    return result


def symmetric(a):
    for i in range(len(a)):
        _guard()
        if any(a[i][j] != a[j][i] for j in range(i)): return False
    return True


def interval(inp, role, shape, selected, sym):
    o = inp.read(role)
    need(o['format'] == 'DYADIC_INTERVAL_MATRIX_V1' and o['shape'] == list(shape) and
         type(o['bits']) is int and o['bits'] == BITS and o['symmetric'] is sym,
         'primitive enclosure schema ' + role)
    c = selected_rows(o['center'], shape, selected)
    r = selected_rows(o['radius'], shape, selected)
    need(all(x >= 0 for row in r for x in row), 'nonnegative primitive radii')
    if sym: need(symmetric(c) and symmetric(r), 'primitive transpose symmetry')
    return c, r


def cache_dyadic(obj, bits):
    need(set(obj) == {'numerator', 'denominator_power_of_two'} and
         type(obj['denominator_power_of_two']) is int and obj['denominator_power_of_two'] == bits,
         'cached dyadic scalar scale')
    return sg(Q(integer(obj['numerator']), gate(1 << bits)))


def admit_cache(inp):
    old = inp.read('coefficient_report'); manifest = inp.read('coefficient_input_manifest')
    plan = inp.read('coefficient_launch_plan'); worker = inp.read('coefficient_worker')
    host = inp.read('coefficient_host'); tool = inp.read('coefficient_actual_tool')
    final = inp.read('coefficient_final_manifest')
    need(manifest['format'] == 'COEFFICIENT_GAP_SAVED_INPUTS_V1' and
         manifest['scope'] == plan['scope'] == worker['scope'] == CACHE_SCOPE and
         len(manifest['bindings']) == 42, 'accepted predecessor scope')
    for role, row in manifest['bindings'].items():
        need(inp.rows[role] == row and old['input_sha256'][role] == row['sha256'],
             'unchanged predecessor input ' + role)
    need(old['format'] == 'SAME_DIRECTION_COEFFICIENT_GAP_CHECK_V1' and
         old['scope'] == CACHE_SCOPE and old['status'] == 'EXACT-CHECK-COMPLETE' and
         old['stage'] == 'complete' and old['same_direction_residual_and_rounding_links'] is True and
         old['primitive_error_owners_charged_once'] is True and
         old['normal_bounds']['raw_enclosure_bridge_validated'] is True,
         'accepted exact cached identities and primitive enclosure bridge')
    need(old['input_manifest_sha256'] == worker['input_manifest_sha256'] ==
         plan['input_manifest_sha256'] == inp.h('coefficient_input_manifest'), 'cached input linkage')
    need(worker['status'] == 'MATH-COMPLETE-RESOURCE-GATE-PENDING' and
         worker['report_status'] == old['status'] and worker['check_report_sha256'] == inp.h('coefficient_report') and
         worker['checker_sha256'] == plan['code_sha256']['shift_checker.py'] == inp.h('coefficient_checker_source') and
         worker['plan_sha256'] == host['plan_sha256'] == inp.h('coefficient_launch_plan'),
         'cached actual executed checker binding')
    need(host['status'] == 'EXTERNAL-RESOURCE-WITNESS-VERIFIED' and host['resource_acceptance'] is True and
         host['actual_wait4_completed'] is True and host['no_remaining_descendants'] is True and
         host['observer_exit_code'] == 0 and tool['dispatch_count'] == 1 and
         tool['actual_tool_exit_code'] == tool['actual_terminal_result']['exit_code'] == 0,
         'cached actual exit and complete resource acceptance')
    terminal = json.loads(tool['actual_terminal_result']['output'])
    need(terminal['status'] == host['status'] and terminal['external_receipt_sha256'] == inp.h('coefficient_host') and
         terminal['plan_sha256'] == inp.h('coefficient_launch_plan'), 'actual tool host receipt chain')
    need(host['final_artifact_manifest_sha256'] == inp.h('coefficient_final_manifest') and
         final['format'] == 'SHIFT372_FINAL_BYTES_V1' and final['plan_sha256'] == inp.h('coefficient_launch_plan'),
         'cached finalized artifact manifest')
    root = inp.paths['coefficient_final_manifest'].parent
    seen = set()
    for row in final['files']:
        rel = Path(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen, 'final cache artifact path')
        seen.add(str(rel)); p = root / rel
        need(not p.is_symlink() and p.resolve().is_relative_to(root.resolve()) and
             p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'final cache artifact bytes')
    need(len(seen) == 13 and 'math/INDEPENDENT_CHECK.json' in seen, 'complete predecessor artifact manifest')
    need(sha(root / 'math/INDEPENDENT_CHECK.json') == inp.h('coefficient_report'), 'manifest to cached report')
    # The separately bound parent final audit accepts this chain and its math.
    # No status word by itself is a replacement for that external review.
    need(inp.h('upstream_coefficient_final_audit') == inp.m['upstream_final_audit_sha256'],
         'accepted external audit record binding')
    v = inp.read('witness_vector')
    need(v['format'] == 'PIVOT210_EXACT_DYADIC_VECTOR_V1' and v['scope'] == WITNESS_SCOPE and
         v['length'] == WIDTH and type(v['bits']) is int and v['bits'] == WBITS and
         v['selected_indices_zero_based'] == list(range(WIDTH)) and
         v['embedding'] == 'append 161 exact zero coordinates to length372' and
         type(v['numerators']) is list and len(v['numerators']) == WIDTH, 'same witness schema')
    w = [integer(x) for x in v['numerators']]
    need(w[-1] == 1 << WBITS and v['last_coordinate'] == '1', 'fixed witness last coordinate')
    x = old['exact_values']; cc = x['c']
    need(set(cc) == {'numerators', 'denominator_power_of_two'} and
         type(cc['denominator_power_of_two']) is int and cc['denominator_power_of_two'] == CBITS and
         type(cc['numerators']) is list and len(cc['numerators']) == RANK, 'cached exact c scale/dimension')
    c = [integer(s) for s in cc['numerators']]
    n = cache_dyadic(x['n'], 160); q0 = cache_dyadic(x['q0'], 480); eps = cache_dyadic(x['eps_q'], 480)
    need(n.numerator > 0 and eps.numerator >= 0, 'cached norm/error signs')
    # Deliberately no C-vector product and no v-vector norm recomputation.
    return w, c, n, q0, eps


def admit_scalars(inp):
    cert = inp.read('saved_SHIFT_SCALARS'); v = cert['values']
    need(cert['scope'] == PRODUCTION_SCOPE and cert['model'] == MODEL and
         cert['model_id'] == 'DELTA128_PUP68_NEW_C_V1' and
         cert['physical_errors_unchanged'] is True and
         cert['trial_gram_majorant'] == 'P<=P_up<=nu68^2 I', 'same physical scalar model')
    norm = inp.read('original_norm'); act = norm['action']; trial = norm['trial']
    need(v['nu68'] == trial['nu68'] and v['sigma2'] == act['sigma68_squared'] and
         v['sigma_bar'] == act['sigma_bar68'] and v['tau'] == act['tau'],
         'exact original scalar strings; accepted scalar identities reused')
    out = {key: rational(v[key]) for key in ('h', 'delta1', 'delta0', 'eta1', 'Fw',
                                           'tau', 'nu68', 'sigma_bar', 'sigma2')}
    need(out['h'] == out['delta1'] == Q(1, 128) and out['delta0'] == Q(1, 64) and
         out['tau'] == Q(1, 100) and out['eta1'].numerator > 0 and
         scmp(out['eta1'], ssub(out['delta1'], out['Fw'])) == 0, 'fixed shift/a/tau0')
    need(out['nu68'].numerator > 0 and out['sigma_bar'].numerator >= 0 and
         out['sigma2'].numerator >= 0, 'nonnegative exact budgets')
    return out


def bilinear_ball(matrix, left, right, scale):
    c, r = matrix
    need(len(c) == len(left) and len(r) == len(left) and
         all(len(row) == len(right) for row in c + r), 'direction contraction dimensions')
    center = radius = 0
    for i, li in enumerate(left):
        _guard()
        cv = isigsum(mul(x, y) for x, y in zip(c[i], right))
        rv = isigsum(mul(x, abs(y)) for x, y in zip(r[i], right))
        center = add(center, mul(li, cv)); radius = add(radius, mul(abs(li), rv))
    need(radius >= 0, 'contracted primitive radius')
    den = gate(1 << scale)
    return sg(Q(center, den)), sg(Q(radius, den))


def exact_p_contraction(inp, c):
    o = inp.read('saved_P_UP_EXACT')
    need(set(o) == {'format', 'shape', 'symmetric', 'denominator', 'numerators'} and
         o['format'] == 'RATIONAL_EXACT_MATRIX_V1' and o['shape'] == [RANK, RANK] and
         o['symmetric'] is True, 'predeclared exact P_up representation')
    den = integer(o['denominator']); need(den > 0, 'positive exact P_up denominator')
    nums = selected_rows(o['numerators'], (RANK, RANK), (RANK, RANK))
    need(symmetric(nums), 'exact P_up symmetry')
    total = 0
    for i, ci in enumerate(c):
        _guard(); row = isigsum(mul(x, y) for x, y in zip(nums[i], c))
        total = add(total, mul(ci, row))
    need(total >= 0, 'P_up nonnegative directional value under physical premises')
    return sg(Q(total, mul(den, gate(1 << 320))))


def endpoint_text(lower, upper):
    need(scmp(lower, upper) <= 0, 'ordered finite rational endpoints')
    return {'lower': st(lower), 'upper': st(upper)}


def tau_value(d, aa, bb, a, tau):
    need(a.numerator > 0 and tau.numerator > 0, 'positive a/tau')
    return sadd(d, sdiv(ssum((aa, bb, smul(tau, aa), sdiv(bb, tau))), a))


def admit_column_bounds(inp, scalar, c):
    """Same64+4 order; original scalar identities, then exact e. No source calls."""
    tau_manifest = inp.read('tau54_input_manifest')
    need(tau_manifest['format'] == 'TAU_ONLY_SAVED_INPUTS_V1' and
         tau_manifest['scope'] == 'DELTA128_FIXED_C_TAU_ONLY_DIRECTION_SCREEN_ONCE_V1' and
         len(tau_manifest['bindings']) == 54, 'unchanged unexecuted tau preparation')
    for role, row in tau_manifest['bindings'].items():
        need(inp.rows[role] == row, 'same previous input/cache chain ' + role)
    order = inp.m['column_order']
    need(order == {'old_coefficient_indices': list(range(64)),
                   'new_coefficient_indices': list(range(64, 68)),
                   'new_source_columns': [0, 1, 2, 3],
                   'action_arrays': ['old_B', 'new_B']}, 'fixed coefficient-to-error-column order')
    origin = inp.read('saved68_order_manifest')
    checked = inp.read('saved68_order_check')
    output = inp.read('saved68_order_outputs')
    need(origin['format'] == 'SAVED68_FIXED_INPUT_MANIFEST_V1' and
         origin['constants']['old_columns'] == 64 and
         origin['constants']['new_columns'] == [0, 1, 2, 3] and
         origin['constants']['observations'] == FULL, 'original68 column order')
    need(checked['checker_sha256'] == inp.h('saved68_order_checker_source') and
         checked['input_manifest_sha256'] == output['manifest_sha256'] == inp.h('saved68_order_manifest') and
         checked['original_mixed_gram_block_identities'] is True and
         checked['fresh_norm_and_all68_action_errors'] is True and
         checked['output_hashes']['OUTPUT_MANIFEST.json'] == inp.h('saved68_order_outputs'),
         'archived order source/report/manifest linkage; inherited physical premises')
    for name, role in [('NORM_ERROR_CERTIFICATE.json', 'original_norm'), ('P68.json', 'original_P68'),
                       ('D68.json', 'original_D68'), ('K68.json', 'original_K68'),
                       ('N68.json', 'original_N68'), ('E68.json', 'original_E68')]:
        need(output['outputs'][name]['sha256'] == checked['output_hashes'][name] == inp.h(role),
             'same ordered primitive output ' + name)
    norm = inp.read('original_norm'); action = norm['action']
    need(norm['counts']['trial_columns'] == RANK and
         norm['ownership']['physical_B'] ==
         'all 64 exact old B_i plus four exact measured Bnew_j; only deterministic action correction',
         'original action-error owners')
    need(type(action['old_B']) is list and len(action['old_B']) == 64 and
         type(action['new_B']) is list and len(action['new_B']) == 4 and len(c) == RANK,
         'exact64+4 action bound sequence')
    bounds = [rational(s) for s in action['old_B'] + action['new_B']]
    need(all(b.numerator >= 0 for b in bounds), 'nonnegative columnwise bounds')
    squared_sum = Q(0); e = Q(0)
    for bi, ci in zip(bounds, c):
        _guard()
        squared_sum = sadd(squared_sum, smul(bi, bi))
        e = sadd(e, smul(bi, Q(abs(gate(ci)), gate(1 << CBITS))))
    need(scmp(squared_sum, scalar['sigma2']) == 0 and
         scmp(smul(scalar['sigma_bar'], scalar['sigma_bar']), squared_sum) >= 0,
         'exact sum B_i^2=sigma2 and sigma_bar^2>=sigma2')
    need(e.numerator >= 0, 'nonnegative exact columnwise error radius')
    return e, {'column_order': order, 'terms': 68, 'sum_of_squares_identity_verified': True,
               'sigma_bar_square_dominates_sigma2': True,
               'eta_equals_e_basis': 'triangle inequality then Cauchy-Schwarz; same ordered c and error columns',
               'archived_order_source_sha256': inp.h('saved68_order_worker_source'),
               'archived_order_checker_sha256': inp.h('saved68_order_checker_source')}


def linear_ball(contracts, coefficients, constant):
    """Combine coefficients BEFORE taking primitive absolute radii."""
    names = ('m_v', 'd_v', 'k_v', 'n_c', 'f_c')
    need(len(coefficients) == len(names), 'five primitive scalar coefficients')
    center = constant; radius = Q(0)
    for name, coefficient in zip(names, coefficients):
        cc, rr = contracts[name]
        need(rr.numerator >= 0, 'primitive radius sign')
        center = sadd(center, smul(coefficient, cc))
        radius = sadd(radius, smul(abs(coefficient), rr))
    return center, radius


def nonnegative_interval(center, radius, name):
    need(radius.numerator >= 0, 'model HOLD: negative radius ' + name)
    raw_lower, upper = ssub(center, radius), sadd(center, radius)
    need(scmp(raw_lower, upper) <= 0, 'model HOLD: unordered raw ' + name)
    need(upper.numerator >= 0, 'model HOLD: negative upper ' + name)
    lower = Q(0) if raw_lower.numerator < 0 else raw_lower
    need(scmp(lower, upper) <= 0, 'model HOLD: clipped lower exceeds upper ' + name)
    return lower, upper, raw_lower


def single_root_predicate(aa, zz, n, relation):
    need(zz.numerator >= 0 and relation in ('lt', 'gt'), 'single-root predicate inputs')
    d0 = ssub(n, aa)
    result = {'relation': relation, 'D0': st(d0), 'strict': False, 'squares_evaluated': False}
    if relation == 'lt' and d0.numerator <= 0:
        return result
    if relation == 'gt' and d0.numerator < 0:
        result['strict'] = True
        return result
    # lt has D0>0; gt has D0>=0. Equality of squared values never passes.
    d02 = smul(d0, d0); signed = ssub(d02, zz)
    result.update(squares_evaluated=True, D0_squared_minus_Z=st(signed),
                  strict=signed.numerator > 0 if relation == 'lt' else signed.numerator < 0)
    return result


def two_root_predicate(aa, xx, yy, n, relation):
    need(xx.numerator >= 0 and yy.numerator >= 0 and relation in ('lt', 'gt'),
         'two-root predicate inputs')
    d0 = ssub(n, aa)
    result = {'relation': relation, 'D0': st(d0), 'strict': False,
              'D0_square_evaluated': False, 'K_square_evaluated': False}
    if relation == 'lt' and d0.numerator <= 0:
        return result
    if relation == 'gt' and d0.numerator < 0:
        result['strict'] = True
        return result
    kval = ssub(ssub(smul(d0, d0), xx), yy)
    result.update(D0_square_evaluated=True, K=st(kval))
    if relation == 'lt' and kval.numerator <= 0:
        return result
    if relation == 'gt' and kval.numerator < 0:
        result['strict'] = True
        return result
    # lt has K>0; gt has K>=0. These sign gates precede the second squaring.
    signed = ssub(smul(kval, kval), smul(Q(4), smul(xx, yy)))
    result.update(K_square_evaluated=True, K_squared_minus_4XY=st(signed),
                  strict=signed.numerator > 0 if relation == 'lt' else signed.numerator < 0)
    return result


def shared_error_decision(aminus, aplus, xx, yminus, yplus, zminus, zplus, n):
    need(n.numerator > 0 and scmp(aminus, aplus) <= 0 and xx.numerator >= 0 and
         yminus.numerator >= 0 and zminus.numerator >= 0 and
         scmp(yminus, yplus) <= 0 and scmp(zminus, zplus) <= 0,
         'model HOLD: ordered symbolic endpoints and exact positive target')
    upper_single = single_root_predicate(aplus, zplus, n, 'lt')
    upper_two = two_root_predicate(aplus, xx, yplus, n, 'lt')
    lower_single = single_root_predicate(aminus, zminus, n, 'gt')
    lower_two = two_root_predicate(aminus, xx, yminus, n, 'gt')
    passed = upper_single['strict'] or upper_two['strict']
    excluded = lower_single['strict'] and lower_two['strict']
    need(not (passed and excluded), 'model HOLD: contradictory shared-error decisions')
    status = 'INCONCLUSIVE'
    if passed: status = 'CONDITIONAL-SHARED-ERROR-DIRECTION-PASS'
    elif excluded: status = 'CONDITIONAL-FIXED-SHARED-ERROR-MAJORANT-EXCLUDED'
    return {'status': status, 'target': 'Q_cap<n; exact cached n=v*v; no extra1-delta factor',
            'upper_pass_uses_OR': passed, 'lower_exclusion_uses_AND': excluded,
            'branch_checks': {'upper_single': upper_single, 'upper_two': upper_two,
                              'lower_single': lower_single, 'lower_two': lower_two},
            'physical_premises_inherited': True, 'only_same_fixed_C_v_majorant': True,
            'exclusion_does_not_lower_bound_true_response': True,
            'no_true_L_negativity_RH_falsity_or_all_choices_exclusion': True,
            'one_direction_is_not_full372_positivity': True,
            'equality_or_failed_sufficient_test_means': 'INCONCLUSIVE'}


def run(source_root, manifest_path, output_path, guard):
    global _guard
    _guard = guard; sys.set_int_max_str_digits(SCALAR_DIGITS)
    need(os.environ.get('SHIFT_CHARGED_EXACT_CHECK') == '1', 'charged exact-check entry required')
    need(not any(name.split('.')[0] in {'flint', 'numpy', 'scipy', 'mpmath'} for name in sys.modules),
         'no scientific runtime imports')
    out = Path(output_path); out.mkdir(exist_ok=False)
    report = {'format': 'FIXED_C_SHARED_ERROR_DIRECTION_SCREEN_V1', 'scope': SCOPE,
              'status': 'HOLD', 'stage': 'input_admission', 'RH_PROOF': 'NOT-OBTAINED',
              'resource_acceptance': False, 'provisional_until_actual_exit_and_resource_acceptance': True,
              'physical_inclusions_reproved': False, 'decisions': {'shared_error': {'status': 'HOLD'}},
              'counts': {'exact_check_calls': 1, 'directions': 1, 'declared_contractions_started': [],
                         'column_radius_terms_started': 0, 'action_budget_identity_terms_started': 0,
                         'native_imports': 0, 'linear_solves': 0, 'C_solves': 0, 'factorizations': 0,
                         'matrix_inverses': 0, 'full372_consumers': 0, 'C_times_v_recomputations': 0,
                         'v_norm_recomputations': 0, 'old_checker_replays': 0, 'tau_screen_executions': 0,
                         'source_actions_FFT_integrals': 0, 'root_approximations': 0,
                         'parameter_grid_points': 0, 'alternate_candidates': 0, 'retries': 0}}
    try:
        inp = Inputs(manifest_path)
        need(str(source_root) == inp.m['source_root'], 'same saved execution environment source root')
        report['input_manifest_sha256'] = sha(manifest_path)
        report['input_sha256'] = {key: row['sha256'] for key, row in inp.rows.items()}
        report['stage'] = 'accepted_cache_and_exact_error_order'
        w, c, n, q0, eps = admit_cache(inp)
        scalar = admit_scalars(inp)
        h, a, tau0 = scalar['h'], scalar['eta1'], scalar['tau']
        report['counts']['column_radius_terms_started'] = 68
        report['counts']['action_budget_identity_terms_started'] = 68
        e, order_evidence = admit_column_bounds(inp, scalar, c)
        report['column_bound_admission'] = order_evidence
        report['cache_reuse'] = {'c_Cv_and_n_vv': 'ACCEPTED-EXACT-CACHE-NOT-RECOMPUTED',
                                'raw_to160_bridge': 'ACCEPTED-PRIOR-CHECK-SAME-INPUT-HASHES',
                                'coefficient_report_sha256': inp.h('coefficient_report')}
        report['stage'] = 'seven_fixed_direction_contractions'
        contracts = {}
        for name, role, shape, selected, sym, left, right, scale in (
            ('m_v', 'saved_A160', (FULL, FULL), (WIDTH, WIDTH), True, w, w, 320),
            ('d_v', 'saved_D160', (RANK, FULL), (RANK, WIDTH), False, c, w, 400),
            ('k_v', 'saved_K160', (RANK, FULL), (RANK, WIDTH), False, c, w, 400),
            ('n_c', 'saved_N160', (RANK, RANK), (RANK, RANK), True, c, c, 480),
            ('f_c', 'saved_F160', (RANK, RANK), (RANK, RANK), True, c, c, 480)):
            report['counts']['declared_contractions_started'].append(name)
            matrix = interval(inp, role, shape, selected, sym)
            contracts[name] = bilinear_ball(matrix, left, right, scale)
            del matrix; gc.collect(); _guard()
        report['counts']['declared_contractions_started'].append('P0')
        p_up_value = exact_p_contraction(inp, c)
        report['counts']['declared_contractions_started'].append('t')
        t = sg(Q(isigsum(mul(x, x) for x in c), gate(1 << 320)))
        need(p_up_value.numerator >= 0 and t.numerator >= 0 and e.numerator >= 0,
             'model HOLD: P0/t/e must be nonnegative')
        ia = sdiv(Q(1), a); ia2 = smul(ia, ia); ha = smul(h, ia)
        oneha = sadd(Q(1), ha); twoha = sadd(Q(1), smul(Q(2), ha))
        h2 = smul(h, h); twoh = smul(Q(2), h)
        rc, rr = linear_ball(contracts, (Q(1), twoh, Q(-2), Q(1), -twoh), smul(h2, p_up_value))
        dc, dr = linear_ball(contracts, (Q(0), Q(2), Q(0), Q(0), Q(-1)), smul(h, p_up_value))
        lc, lr = linear_ball(contracts,
            (ia, smul(Q(2), oneha), smul(Q(-2), ia), ia, -twoha), smul(smul(h, oneha), p_up_value))
        fouria = smul(Q(4), ia); fouria2 = smul(Q(4), ia2)
        jc, jr = linear_ball(contracts,
            (fouria2, smul(fouria, twoha), smul(Q(-8), ia2), fouria2, -smul(fouria, twoha)),
            smul(smul(twoha, twoha), p_up_value))
        rl, ru, raw_rl = nonnegative_interval(rc, rr, 'R')
        jl, ju, raw_jl = nonnegative_interval(jc, jr, 'J')
        ll, lu = ssub(lc, lr), sadd(lc, lr)
        need(scmp(ll, lu) <= 0, 'model HOLD: unordered L interval')
        nu2t = smul(smul(scalar['nu68'], scalar['nu68']), t)
        w2 = nu2t if scmp(nu2t, p_up_value) <= 0 else p_up_value
        need(w2.numerator >= 0, 'model HOLD: negative W2')
        e2 = smul(e, e); budget_t = smul(scalar['sigma2'], t)
        need(scmp(e2, budget_t) <= 0, 'model HOLD: column-radius Cauchy consistency')
        report['stage'] = 'tau0_consistency_only'
        old_allowance = smul(smul(scalar['nu68'], scalar['sigma_bar']), t)
        old_dl, old_du = sadd(ssub(dc, dr), old_allowance), sadd(sadd(dc, dr), old_allowance)
        new_lo = tau_value(old_dl, rl, budget_t, a, tau0)
        new_hi = tau_value(old_du, ru, budget_t, a, tau0)
        old_lo, old_hi = ssub(q0, eps), sadd(q0, eps)
        need(scmp(new_lo, old_hi) <= 0 and scmp(old_lo, new_hi) <= 0,
             'model HOLD: disjoint tau0 consistency intervals')
        report['tau0_link'] = {'primitive': endpoint_text(new_lo, new_hi),
                              'accepted_q0_eps_q': endpoint_text(old_lo, old_hi),
                              'nonempty_intersection': True,
                              'consistency_only_not_physical_inclusion_or_Q_proof': True}
        report['stage'] = 'symbolic_shared_error_endpoints'
        e2a = smul(e2, ia)
        aminus, aplus = sadd(ll, e2a), sadd(lu, e2a)
        xx = smul(e2, w2)
        four_e2_a2 = smul(Q(4), smul(e2, ia2))
        yminus, yplus = smul(four_e2_a2, rl), smul(four_e2_a2, ru)
        zminus, zplus = smul(e2, jl), smul(e2, ju)
        report['primitive_contractions'] = {name: {'center': st(v[0]), 'absolute_radius': st(v[1])}
                                            for name, v in contracts.items()}
        report['exact_scalars'] = {'P0': st(p_up_value), 't': st(t), 'e': st(e), 'W2': st(w2),
                                   'a': st(a), 'h': st(h), 'n_cached_exact': st(n)}
        report['collected_enclosures'] = {'L': endpoint_text(ll, lu), 'R': endpoint_text(rl, ru),
                                          'J': endpoint_text(jl, ju), 'R_raw_lower': st(raw_rl),
                                          'J_raw_lower': st(raw_jl), 'L_intersection_tightening': False,
                                          'R_J_clip_basis': 'nonnegative physical norm plus nonnegative exact-P_up slack'}
        report['Q_symbolic_endpoints'] = {
            'expression': 'min(A+sqrt(Z), A+sqrt(X)+sqrt(Y))',
            'lower': {'A': st(aminus), 'X': st(xx), 'Y': st(yminus), 'Z': st(zminus)},
            'upper': {'A': st(aplus), 'X': st(xx), 'Y': st(yplus), 'Z': st(zplus)},
            'numerical_roots_computed': False, 'target': 'exact cached n'}
        decision = shared_error_decision(aminus, aplus, xx, yminus, yplus, zminus, zplus, n)
        report['decisions'] = {'shared_error': decision}
        report.update(status='EXACT-SHARED-ERROR-SCREEN-COMPLETE', stage='complete',
                      numerical_status=decision['status'], eta_is_exact_columnwise_e=True,
                      P_up_representation='EXACT-RATIONAL-NO-SWITCH',
                      repeated_coefficients_collected_before_radii=True,
                      physical_P_radius_or_UCERT_pad_added=False, unknown_slack_contracted=False,
                      no_matrix_lambda_theta_halfspace_branch=True,
                      no_global_certificate_or_true_response_lower_bound=True,
                      no_all_coefficient_parameter_choices_exclusion=True,
                      automatic_follow_on_compute=False, new_lower_edge=None)
        inp.verify()
        need(sha(manifest_path) == report['input_manifest_sha256'], 'input manifest unchanged')
        save(out / 'INDEPENDENT_CHECK.json', report)
        return report
    except Exception as exc:
        report.update(status='HOLD', failed_obligation=str(exc), exception_type=type(exc).__name__, automatic_retry=False)
        report['decisions'] = {'shared_error': {'status': 'HOLD', 'reason': str(exc)}}
        try:
            target = out / 'INDEPENDENT_CHECK.json'
            if target.exists():
                report['invalidates_provisional_report'] = 'INDEPENDENT_CHECK.json'
                target = out / 'CHECK_HOLD.json'
            save(target, report)
        except Exception: pass
        raise

