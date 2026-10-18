"""One stdlib exact check of a fixed saved direction. No work on import.

No producer/helper/native imports, solve, factor, inverse or full consumer.
Raw endpoint checks derive from the archived independent checker (CC BY-NC4.0).
The implementation itself is pending independent review and has not been run.
"""
import gc
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from fractions import Fraction as Q

SCOPE = 'DELTA128_SAME_DIRECTION_COEFFICIENT_GAP_EXACT_ONCE_V1'
OLD_SCOPE = 'DELTA128_PUP68_NEW_C_FULL372_ONCE_V1'
WITNESS_SCOPE = 'DELTA128_PIVOT210_SAME_DIRECTION_DIAGNOSTIC_ONCE_V1'
RANK, WIDTH, FULL = 68, 211, 372
BITS, WBITS, UBITS, MAXBITS = 160, 80, 100, 1024
SCALAR_DIGITS = 100000
MODEL = 'alpha*M-B^*C-C^*B+C^*S*C; B=alpha*K-p*D; S=alpha*N-q*F+k*P_up+beta*I'
_guard = lambda: None


class Inconclusive(RuntimeError):
    """Failed proof obligation; never an impossibility conclusion."""


def need(ok, label):
    if not ok:
        raise Inconclusive(label)


def gate(x):
    need(type(x) is int and x.bit_length() <= MAXBITS, 'dense1024-bit ceiling')
    return x


def integer(s):
    need(type(s) is str and len(s) <= 310 and
         re.fullmatch(r'0|-?[1-9][0-9]*', s) is not None,
         'canonical bounded dense integer')
    return gate(int(s))


def rational(s):
    # Existing separate scalar-rational convention, not a dense-integer escape.
    need(type(s) is str and re.fullmatch(r'(0|-?[1-9][0-9]*)(/[1-9][0-9]*)?', s)
         is not None, 'canonical scalar rational')
    need(all(len(part.lstrip('-')) <= SCALAR_DIGITS for part in s.split('/')),
         'unchanged scalar input digit ceiling')
    _guard()
    result = Q(s)
    _guard()
    return result


def add(a, b):
    gate(a); gate(b)
    if not a: return b
    if not b: return a
    need(max(a.bit_length(), b.bit_length()) + 1 <= MAXBITS,
         'addition pre-operation ceiling')
    return gate(a + b)


def sub(a, b):
    return add(a, -gate(b))


def mul(a, b):
    gate(a); gate(b)
    if not a or not b: return 0
    need(a.bit_length() + b.bit_length() <= MAXBITS,
         'product pre-operation ceiling')
    return gate(a * b)


def shift(a, bits):
    gate(a)
    need(type(bits) is int and 0 <= bits <= MAXBITS, 'shift exponent')
    if not a: return 0
    need(a.bit_length() + bits <= MAXBITS, 'shift pre-operation ceiling')
    return gate(a << bits)


def isum(values):
    total = 0
    for x in values: total = add(total, x)
    return total


def dot(a, b):
    need(len(a) == len(b), 'dot dimensions')
    return isum(mul(x, y) for x, y in zip(a, b))


def matvec(a, v):
    out = []
    for row in a:
        _guard(); out.append(dot(row, v))
    return out


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while block := f.read(1 << 20):
            h.update(block)
            _guard()
    return h.hexdigest()


def load(path):
    def unique(items):
        d = {}
        for k, v in items:
            need(k not in d, 'duplicate JSON key'); d[k] = v
        return d
    _guard()
    obj = json.loads(Path(path).read_bytes(), object_pairs_hook=unique)
    _guard()
    return obj


def save(path, obj):
    _guard()
    raw = (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()
    with Path(path).open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    need(Path(path).read_bytes() == raw, 'report durable byte readback')
    fd = os.open(Path(path).parent, os.O_RDONLY | os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)
    _guard()


def selected_rows(raw, shape, selected):
    nr, nc = shape
    sr, sc = selected
    need(type(raw) is list and len(raw) == nr and
         all(type(row) is list and len(row) == nc for row in raw), 'full stored shape')
    need(0 < sr <= nr and 0 < sc <= nc, 'selected shape')
    return [[integer(raw[i][j]) for j in range(sc)] for i in range(sr)]


def symmetric(a):
    return all(a[i][j] == a[j][i] for i in range(len(a)) for j in range(i))


def interval(path, shape, selected, bits, sym):
    o = load(path)
    need(o['format'] == 'DYADIC_INTERVAL_MATRIX_V1' and o['shape'] == list(shape)
         and type(o['bits']) is int and o['bits'] == bits and o['symmetric'] is sym,
         'interval schema/scale ' + Path(path).name)
    c = selected_rows(o['center'], shape, selected)
    r = selected_rows(o['radius'], shape, selected)
    need(all(x >= 0 for row in r for x in row), 'nonnegative selected radii')
    if sym:
        need(selected[0] == selected[1] and symmetric(c) and symmetric(r),
             'selected center/radius symmetry')
    return c, r


def exact(path, shape, selected, bits):
    o = load(path)
    need(o['format'] == 'DYADIC_EXACT_MATRIX_V1' and o['shape'] == list(shape)
         and type(o['bits']) is int and o['bits'] == bits, 'exact schema/scale')
    return selected_rows(o['numerators'], shape, selected)


def quantize_endpoints(lo, hi, den, bits=BITS):
    gate(lo); gate(hi); gate(den)
    need(lo <= hi and den > 0, 'ordered endpoints/positive denominator')
    low = shift(lo, bits) // den
    high = -((-shift(hi, bits)) // den)
    c = add(low, high) // 2
    return gate(c), max(sub(c, low), sub(high, c))


def scalar_ball(q):
    # Scalar rational arithmetic already had its own100000-digit decoder.
    # The converted160-bit center/radius must re-enter the dense1024-bit gate.
    _guard()
    low = (q.numerator << BITS) // q.denominator
    high = -((-(q.numerator << BITS)) // q.denominator)
    c = (low + high) // 2
    r = max(c - low, high - c)
    _guard()
    return gate(c), gate(r)


def downward_lower(q):
    _guard()
    num = gate((q.numerator << BITS) // q.denominator)
    need(Q(num, 1 << BITS) <= q, 'downward lower-bound encoding')
    _guard()
    return num


class Inputs:
    def __init__(self, manifest_path):
        self.manifest_path = Path(manifest_path)
        need(sha(self.manifest_path) == os.environ['SHIFT_INPUT_SHA256'],
             'input manifest admission')
        self.m = load(self.manifest_path)
        need(self.m['format'] == 'COEFFICIENT_GAP_SAVED_INPUTS_V1' and
             self.m['scope'] == SCOPE and self.m['upstream_diagnostic_review'] == 'GO',
             'fixed input scope/upstream review')
        self.rows = self.m['bindings']
        self.paths = {}
        for role, row in self.rows.items():
            p = Path(row['path'])
            need(p.is_absolute() and p.resolve() == p and not p.is_symlink(),
                 'canonical input path ' + role)
            self.paths[role] = p
        self.verify()

    def verify(self):
        for role, row in self.rows.items():
            _guard(); p = self.paths[role]
            need(p.is_file() and p.stat().st_size == row['bytes'] and
                 sha(p) == row['sha256'], 'input bytes ' + role)

    def read(self, role):
        return load(self.paths[role])

    def h(self, role):
        return self.rows[role]['sha256']


def check_scalars(inp):
    cert = inp.read('saved_SHIFT_SCALARS')
    norm = inp.read('original_norm'); act, trial = norm['action'], norm['trial']
    tail = inp.read('original_sharp')['exact']
    tau = rational(act['tau']); need(tau == Q(1, 100), 'fixed tau')
    nu = rational(trial['nu68']); sigbar = rational(act['sigma_bar68'])
    need(len(act['old_B']) == 64 and len(act['new_B']) == 4, 'all64+4 action errors')
    sigma2 = Q(0)
    for text in act['old_B'] + act['new_B']:
        x = rational(text); need(x >= 0, 'nonnegative action error')
        sigma2 += x * x; _guard()
    need(sigma2 == rational(act['sigma68_squared']) > 0 and sigbar >= 0 and
         sigbar * sigbar >= sigma2 and nu > 0, 'scalar norm/error bounds')
    eps = rational(tail['cover_epsilon_upper'])
    need(eps == Q(14194233101692862490101543299783481485,
                  3284055810247577849424937639623597936869376), 'original cover allowance')
    dw = Q(1989293801, 35118080000000000)
    need(0 < dw < rational(tail['new_prime_tail_upper']), 'weighted tail owner')
    delta0, delta1 = Q(1, 64), Q(1, 128)
    h = delta0 - delta1; fw = dw + eps; a = delta1 - fw
    need(h == Q(1, 128) and a > 0, 'delta128 positive coercive floor')
    alpha = (1 + tau) / a
    p = 1 + alpha * h; q = 2 * p - 1; k = h * p
    beta = nu * sigbar + 101 * sigma2 / a
    mh = nu * sigbar + 76 * sigma2 / a
    need(k > 0 and mh == beta - sigma2 / (4 * tau * a) > 0,
         'fresh actual-S analytic lower expression')
    eta = delta0 - rational(tail['new_prime_tail_upper']) - eps
    need(rational(act['eta']) == eta, 'original unshifted norm anchor')
    values = dict(eta=eta, tau=tau, nu68=nu, sigma2=sigma2, sigma_bar=sigbar,
                  h=h, eta1=a, delta1=delta1, delta0=delta0, d_w=dw,
                  cover_epsilon=eps, Fw=fw, alpha=alpha, beta=beta, p=p, q=q, k=k, m_h=mh)
    # mu0 and delta_star are historical metadata; this check never uses them.
    need(set(cert['values']) == set(values) | {'mu0', 'delta_star'}, 'saved scalar keys')
    for key, value in values.items():
        need(rational(cert['values'][key]) == value, 'scalar recomputation ' + key)
    need(cert['scope'] == OLD_SCOPE and cert['model'] == MODEL and
         cert['model_id'] == 'DELTA128_PUP68_NEW_C_V1' and
         cert['physical_errors_unchanged'] is True and
         cert['trial_gram_majorant'] == 'P<=P_up<=nu68^2 I', 'physical-model scope')
    balls = {name: scalar_ball(values[name]) for name in ('alpha', 'p', 'q', 'k', 'beta')}
    need(set(cert['scalar_balls160']) == set(balls), 'scalar-ball keys')
    for name, pair in balls.items():
        need(tuple(map(integer, cert['scalar_balls160'][name])) == pair,
             'exact scalar center/radius encoding ' + name)
    return values, balls, trial


def check_p_up(inp, trial):
    o = inp.read('original_P68')
    need(o['format'] == 'RATIONAL_MID_RADIUS_MATRIX_V1' and
         o['shape'] == [RANK, RANK] and o['symmetric'] is True, 'raw P68 schema')
    den = integer(o['denominator']); need(den > 0, 'P68 denominator')
    raw = o['entries']
    need(type(raw) is list and len(raw) == RANK and
         all(type(row) is list and len(row) == RANK for row in raw), 'raw P68 shape')
    center, radius = [], []
    for row in raw:
        cc, rr = [], []
        for pair in row:
            need(type(pair) is list and len(pair) == 2, 'P68 pair')
            c, r = map(integer, pair); need(r >= 0, 'P68 nonnegative radius')
            cc.append(c); rr.append(r)
        center.append(cc); radius.append(rr); _guard()
    need(symmetric(center) and symmetric(radius), 'P68 exact transpose equality')
    rho = [isum(row) for row in radius]
    rows = []
    for i in range(RANK):
        total = add(center[i][i], radius[i][i])
        for j in range(RANK):
            if i != j:
                total = add(total, max(abs(sub(center[i][j], radius[i][j])),
                                       abs(add(center[i][j], radius[i][j]))))
        rows.append(Q(total, den)); _guard()
    need(len(trial['row_upper_bounds']) == RANK and
         rows == [rational(x) for x in trial['row_upper_bounds']], 'all68 raw P row witnesses')
    upper = max(rows); nu = rational(trial['nu68']); slack = nu * nu - upper
    need(upper == rational(trial['L68']) and
         slack == rational(trial['nu68_square_slack']) > 0, 'trial norm slack')
    exact_up = inp.read('saved_P_UP_EXACT')
    need(set(exact_up) == {'format', 'shape', 'symmetric', 'denominator', 'numerators'} and
         exact_up['format'] == 'RATIONAL_EXACT_MATRIX_V1' and
         exact_up['shape'] == [RANK, RANK] and exact_up['symmetric'] is True and
         integer(exact_up['denominator']) == den, 'exact fixed P_up schema')
    nums = selected_rows(exact_up['numerators'], (RANK, RANK), (RANK, RANK))
    need(symmetric(nums), 'exact P_up symmetry')
    pc, pr = interval(inp.paths['saved_P_UP160'], (RANK, RANK), (RANK, RANK), BITS, True)
    for i in range(RANK):
        _guard()
        for j in range(RANK):
            expected = add(center[i][j], rho[i] if i == j else 0)
            need(nums[i][j] == expected, 'P_up physical radius charged once')
            need((pc[i][j], pr[i][j]) == quantize_endpoints(expected, expected, den),
                 'P_up encoding-only radius')
    expected_cert = {
        'method': 'Pc+diag(row_sum(R)); physical R charged once',
        'physical_inclusion': 'INHERITED-N3-NOT-REPROVED',
        'rho_rows': [str(Q(x, den)) for x in rho], 'row_upper_bounds': list(map(str, rows)),
        'L68': str(upper), 'nu68': str(nu), 'nu68_square_slack': str(slack),
        'encoding_radius': 'exact P_up encoding loss only',
        'P68_sha256': inp.h('original_P68'), 'P_up_exact_sha256': inp.h('saved_P_UP_EXACT'),
        'norm_sha256': inp.h('original_norm'), 'scope': OLD_SCOPE}
    need(inp.read('saved_P_UP_CERTIFICATE') == expected_cert, 'saved P_up finite witness')
    return pc, pr


def check_source(inp, raw_role, saved_role, shape, selected, sym, aobs=False):
    o = inp.read(raw_role)
    if aobs:
        need(o['shape'] == list(shape) and type(o['bits']) is int and o['bits'] == 100
             and o['scope'] == 'true full-line W*W; source moment tails retained', 'AOBS scope/scale')
        den = 1 << 100
    else:
        need(o['format'] == 'RATIONAL_MID_RADIUS_MATRIX_V1' and
             o['shape'] == list(shape) and o['symmetric'] is sym, 'raw enclosure schema')
        den = integer(o['denominator']); need(den > 0, 'raw enclosure denominator')
    raw = o['entries']
    need(type(raw) is list and len(raw) == shape[0] and
         all(type(row) is list and len(row) == shape[1] for row in raw), 'raw full shape')
    c, r = interval(inp.paths[saved_role], shape, selected, BITS, sym)

    def pair(i, j):
        item = raw[i][j]
        need(type(item) is list and len(item) == 2, 'raw pair')
        x, y = map(integer, item); need(y >= 0, 'raw radius sign')
        return sub(x, y), add(x, y)

    for i in range(selected[0]):
        _guard()
        for j in range(selected[1]):
            lo, hi = pair(i, j)
            if sym:
                tl, th = pair(j, i)
                lo, hi = min(lo, tl), max(hi, th)  # containing hull, not intersection
            need((c[i][j], r[i][j]) == quantize_endpoints(lo, hi, den),
                 'raw-to160 enclosure encoding ' + saved_role)
    return c, r


def product_ball(ac, ar, xc, xr):
    need(ar >= 0 and xr >= 0, 'product radius signs')
    return mul(ac, xc), isum((mul(abs(ac), xr), mul(ar, abs(xc)), mul(ar, xr)))


def check_assembly(balls, pup, n, f, k, d, s, b):
    ac, ar = balls['alpha']; bc, br = balls['beta']; kc, kr = balls['k']
    for width, xx, yy, coefficient, output, normal in (
            (RANK, n, f, balls['q'], s, True),
            (WIDTH, k, d, balls['p'], b, False)):
        xc, xr = xx; yc, yr = yy; oc, rr = output; mc, mr = coefficient
        for i in range(RANK):
            _guard()
            for j in range(width):
                az, ae = product_ball(ac, ar, xc[i][j], xr[i][j])
                yz, ye = product_ball(mc, mr, yc[i][j], yr[i][j])
                lo = sub(sub(az, ae), add(yz, ye))
                hi = sub(add(az, ae), sub(yz, ye))
                if normal:
                    pz, pe = product_ball(kc, kr, pup[0][i][j], pup[1][i][j])
                    lo = add(lo, sub(pz, pe)); hi = add(hi, add(pz, pe))
                    if i == j:
                        lo = add(lo, shift(sub(bc, br), BITS))
                        hi = add(hi, shift(add(bc, br), BITS))
                need((oc[i][j], rr[i][j]) == quantize_endpoints(lo, hi, 1 << 320),
                     'independent signed S/B assembly')


def check_normal(inp, values, s):
    sc, sr = s
    radius_rows = [isum(row) for row in sr]
    rho_num = max(radius_rows); rho = Q(rho_num, 1 << BITS)
    mh = values['m_h']; center_margin = mh - rho
    cert = inp.read('saved_NORMAL_CERTIFICATE')
    need(cert == {
        'scope': OLD_SCOPE, 'm_h': str(mh), 'row_radius_max': str(rho),
        'center_lower_bound': str(center_margin),
        'criterion': 'm_h-rho_S>0; sufficient contract gate, not necessary for actual SPD',
        'normal_lemma_sha256': inp.h('original_normal_lemma'),
        'SHIFT_SCALARS_sha256': inp.h('saved_SHIFT_SCALARS'),
        'P_UP_EXACT_sha256': inp.h('saved_P_UP_EXACT'),
        'SBAR160_sha256': inp.h('saved_SBAR160')}, 'recomputed normal certificate/links')
    g0 = min(sub(sc[i][i], isum(abs(sc[i][j]) for j in range(RANK) if j != i))
             for i in range(RANK))
    l0 = max(isum(abs(x) for x in row) for row in sc)
    # L0 is an EXACT160-bit upper row bound: never rounded downward.
    need(l0 > 0, 'nonzero exact normal row upper bound')
    mu_center = downward_lower(center_margin)
    mu_actual = downward_lower(mh)
    mu_box = downward_lower(mh - 2 * rho)
    # Prefer a premise-free direct finite margin; otherwise use only the
    # freshly checked enclosing bridge and explicitly conditional margin.
    if g0 > 0:
        m0, basis, conditional = g0, 'DIRECT-EXACT-GERSHGORIN', False
    elif mu_center > 0:
        m0, basis, conditional = mu_center, 'VALIDATED-BRIDGE-m_h-minus-rho', True
    else:
        m0, basis, conditional = None, 'NO-VALID-POSITIVE-LOWER', None
    return {'m_h': str(mh), 'rho_S': str(rho), 'm_h_minus_rho_S': str(center_margin),
            'm_h_minus_2rho_S': str(mh - 2 * rho), 'radius_rows_bits160': list(map(str, radius_rows)),
            'g0_bits160': str(g0), 'L0_exact_upper_bits160': str(l0),
            'center_downward_bits160': str(mu_center), 'actual_downward_bits160': str(mu_actual),
            'whole_box_downward_bits160': str(mu_box), 'selected_m0_bits160': None if m0 is None else str(m0),
            'selected_m0_basis': basis, 'selected_m0_uses_physical_premises': conditional,
            'raw_enclosure_bridge_validated': True}, m0, l0, mu_actual


def check_cached_witness(inp):
    v = inp.read('witness_vector'); old = inp.read('witness_check')
    wm = inp.read('witness_input_manifest'); wp = inp.read('witness_launch_plan')
    worker = inp.read('witness_worker_record'); host = inp.read('witness_host_resource')
    tool = inp.read('witness_actual_tool')
    need(v['format'] == 'PIVOT210_EXACT_DYADIC_VECTOR_V1' and v['scope'] == WITNESS_SCOPE
         and v['length'] == WIDTH and type(v['bits']) is int and v['bits'] == WBITS
         and v['selected_indices_zero_based'] == list(range(WIDTH)) and
         v['last_coordinate'] == '1' and
         v['embedding'] == 'append 161 exact zero coordinates to length372', 'fixed witness schema')
    need(type(v['numerators']) is list and len(v['numerators']) == WIDTH, 'fixed witness length')
    w = [integer(x) for x in v['numerators']]
    need(w[-1] == 1 << WBITS, 'same exact last coordinate')
    need(v['input_manifest_sha256'] == old['input_manifest_sha256'] ==
         worker['input_manifest_sha256'] == inp.h('witness_input_manifest'), 'witness input chain')
    need(wm['scope'] == wp['scope'] == WITNESS_SCOPE and
         wm['matrices']['U_MODEL']['sha256'] == inp.h('saved_U_MODEL') and
         wm['matrices']['UCERT']['sha256'] == inp.h('saved_UCERT') and
         wm['provenance']['C']['sha256'] == inp.h('saved_C'), 'same saved model/C')
    need(old['format'] == 'PIVOT210_EXACT_QUADRATIC_CHECK_V1' and
         old['scope'] == WITNESS_SCOPE and old['same_direction_verified'] is True and
         old['negative_witness_verified'] is True and
         old['vector_sha256'] == inp.h('witness_vector') and
         old['selected_indices_zero_based'] == list(range(WIDTH)) and
         old['zero_extension_length'] == FULL and
         old['matrix_scale_bits'] == UBITS and old['vector_scale_bits'] == WBITS and
         old['quadratic_scale_bits'] == 260, 'accepted cached exact witness')
    need(worker['check_report_sha256'] == inp.h('witness_check') and
         worker['checker_sha256'] == wp['code_sha256']['shift_checker.py'] and
         worker['plan_sha256'] == host['plan_sha256'] == inp.h('witness_launch_plan'),
         'cached checker/plan chain')
    need(host['status'] == 'EXTERNAL-RESOURCE-WITNESS-VERIFIED' and
         host['resource_acceptance'] is True and host['actual_wait4_completed'] is True and
         host['no_remaining_descendants'] is True and host['observer_exit_code'] == 0 and
         tool['dispatch_count'] == 1 and tool['actual_tool_exit_code'] == 0 and
         tool['actual_terminal_result']['exit_code'] == 0, 'accepted diagnostic actual termination')
    terminal = json.loads(tool['actual_terminal_result']['output'])
    need(terminal['external_receipt_sha256'] == inp.h('witness_host_resource') and
         terminal['plan_sha256'] == inp.h('witness_launch_plan'), 'actual tool receipt binding')
    for name in ('U_MODEL', 'UCERT'):
        digest = inp.h('saved_' + name)
        need(v[name + '_sha256'] == old['input_sha256'][name] == digest, 'cached input identity')
    stored = inp.read('saved_U_MODEL')
    need(stored['format'] == 'DYADIC_INTERVAL_MATRIX_V1' and stored['shape'] == [FULL, FULL]
         and stored['bits'] == UBITS and stored['symmetric'] is True, 'bound U_MODEL metadata')
    del stored
    cert = inp.read('saved_UCERT')
    need(cert['C_sha256'] == inp.h('saved_C') and cert['U_MODEL_sha256'] == inp.h('saved_U_MODEL')
         and cert['SHIFT_SCALARS_sha256'] == inp.h('saved_SHIFT_SCALARS') and
         cert['NORMAL_CERTIFICATE_sha256'] == inp.h('saved_NORMAL_CERTIFICATE'), 'consumer proposal links')
    norm_num = dot(w, w); need(norm_num > 0, 'nonzero same witness')
    cached = old['quadratic_values_unreduced_exact_rationals']
    for name in ('identity', 'U_MODEL_center'):
        need(integer(cached[name]['denominator']) == 1 << 260, 'cached common quadratic scale')
    need(integer(cached['identity']['numerator']) == shift(norm_num, 100),
         'same-v quadratic normalization')
    need(Q(integer(old['norm_squared']['numerator']), integer(old['norm_squared']['denominator']))
         == Q(norm_num, 1 << 160), 'cached exact norm equality')
    return w, norm_num, integer(cached['U_MODEL_center']['numerator'])


def dyadic(value, bits):
    return {'numerator': str(gate(value)), 'denominator_power_of_two': bits}


def vector(values, bits):
    return {'numerators': [str(gate(x)) for x in values], 'denominator_power_of_two': bits}


def run(source_root, manifest_path, output_path, guard):
    global _guard
    _guard = guard
    sys.set_int_max_str_digits(SCALAR_DIGITS)
    need(os.environ.get('SHIFT_CHARGED_EXACT_CHECK') == '1', 'charged exact-check entry required')
    need(not any(name.split('.')[0] in {'flint', 'numpy', 'scipy', 'mpmath'} for name in sys.modules),
         'no scientific runtime imports')
    out = Path(output_path); out.mkdir(exist_ok=False)
    report = {
        'format': 'SAME_DIRECTION_COEFFICIENT_GAP_CHECK_V1', 'scope': SCOPE,
        'status': 'INCONCLUSIVE', 'stage': 'input_admission', 'RH_PROOF': 'NOT-OBTAINED',
        'resource_acceptance': False, 'physical_inclusions_reproved': False,
        'provisional_until_actual_exit_and_resource_acceptance': True,
        'decisions': {'nominal_center': {'status': 'INCONCLUSIVE'},
                      'physical_majorant': {'status': 'INCONCLUSIVE'},
                      'nominal_direction_existence': {'status': 'INCONCLUSIVE'}},
        'counts': {'exact_check_calls': 1, 'directions': 1, 'native_imports': 0,
                   'linear_solves': 0, 'C_solves': 0, 'factorizations': 0, 'matrix_inverses': 0,
                   'full372_consumers': 0, 'old_diagnostic_replays': 0,
                   'source_actions_FFT_integrals': 0, 'alternate_candidates': 0, 'retries': 0}}
    try:
        inp = Inputs(manifest_path)
        need(str(source_root) == inp.m['source_root'], 'source root identity')
        report['input_manifest_sha256'] = sha(manifest_path)
        report['input_sha256'] = {k: v['sha256'] for k, v in inp.rows.items()}
        report['stage'] = 'same_cached_witness'
        w, norm_num, u_mid_num = check_cached_witness(inp)
        report['stage'] = 'primitive_enclosure_bridge'
        values, balls, trial = check_scalars(inp)
        pup = check_p_up(inp, trial)
        nn = check_source(inp, 'original_N68', 'saved_N160', (RANK, RANK), (RANK, RANK), True)
        ff = check_source(inp, 'original_E68', 'saved_F160', (RANK, RANK), (RANK, RANK), True)
        kk = check_source(inp, 'original_K68', 'saved_K160', (RANK, FULL), (RANK, WIDTH), False)
        dd = check_source(inp, 'original_D68', 'saved_D160', (RANK, FULL), (RANK, WIDTH), False)
        s = interval(inp.paths['saved_SBAR160'], (RANK, RANK), (RANK, RANK), BITS, True)
        b = interval(inp.paths['saved_B160'], (RANK, FULL), (RANK, WIDTH), BITS, False)
        check_assembly(balls, pup, nn, ff, kk, dd, s, b)
        del pup, nn, ff, kk, dd
        m = check_source(inp, 'original_A', 'saved_A160', (FULL, FULL), (WIDTH, WIDTH), True, aobs=True)
        report['stage'] = 'validated_normal_lower_bounds'
        lower, m0, l0, mactual = check_normal(inp, values, s)
        report['normal_bounds'] = lower
        del trial, values
        gc.collect(); _guard()
        report['stage'] = 'same_direction_contractions'
        cmat = exact(inp.paths['saved_C'], (RANK, FULL), (RANK, WIDTH), WBITS)
        c = matvec(cmat, w); del cmat
        bv = matvec(b[0], w)
        sc = matvec(s[0], c)
        residual = [sub(shift(bv[i], 80), sc[i]) for i in range(RANK)]
        saved_residual = exact(inp.paths['saved_NORMAL_RESIDUAL'], (RANK, FULL), (RANK, WIDTH), 240)
        other = matvec(saved_residual, w); del saved_residual
        need(residual == [-x for x in other], 'r0 equals minus saved normal residual times v')
        ac, ar = balls['alpha']
        mq = dot(w, matvec(m[0], w))
        q0 = add(sub(mul(ac, mq), shift(dot(c, bv), 81)), dot(c, sc))
        n480 = shift(norm_num, 320)
        e0 = sub(q0, n480)
        umid480 = shift(u_mid_num, 220)
        d_round = sub(umid480, q0)
        sum_abs_w = isum(abs(x) for x in w)
        round_limit = shift(mul(sum_abs_w, sum_abs_w), 220)
        report['stage'] = 'stored_U_MODEL_exact_directional_link'
        need(abs(d_round) <= round_limit, 'signed consumer-center rounding link')
        residual_squared = dot(residual, residual)
        report['stage'] = 'primitive_error_contractions'
        av, cv = list(map(abs, w)), list(map(abs, c))
        rbv = matvec(b[1], av)
        rsc = matvec(s[1], cv)
        t = [add(shift(rbv[i], 80), rsc[i]) for i in range(RANK)]
        rm_quad = dot(av, matvec(m[1], av))
        abs_m = [[abs(x) for x in row] for row in m[0]]
        abs_m_quad = dot(av, matvec(abs_m, av)); del abs_m
        eps_alpha_m = isum((mul(abs(ac), rm_quad), mul(ar, abs_m_quad), mul(ar, rm_quad)))
        eps_q = isum((eps_alpha_m, shift(dot(cv, rbv), 81), dot(cv, rsc)))
        upper_residual = [add(abs(residual[i]), t[i]) for i in range(RANK)]
        r_plus = dot(upper_residual, upper_residual)
        need(eps_q >= 0 and r_plus >= residual_squared >= 0, 'primitive error signs')
        report['stage'] = 'scoped_strict_comparisons'
        nominal_margin = None if m0 is None else sub(mul(e0, m0), residual_squared)
        existence_margin = sub(residual_squared, mul(e0, l0))
        physical_margin = None if mactual <= 0 else sub(mul(sub(e0, eps_q), mactual), r_plus)
        conditional = lower['selected_m0_uses_physical_premises']
        nominal_status = 'INCONCLUSIVE'
        if nominal_margin is not None and nominal_margin > 0:
            nominal_status = ('CONDITIONAL-' if conditional else '') + 'NOMINAL-COEFFICIENT-REPAIR-EXCLUDED'
        existence_status = 'INCONCLUSIVE'
        if e0 < 0:
            existence_status = 'CURRENT-NOMINAL-DIRECTION-POSITIVE'
        elif m0 is not None and existence_margin > 0:
            existence_status = 'NOMINAL-DIRECTION-REPAIR-EXISTS-UNRESTRICTED-COEFFICIENTS'
        physical_status = 'INCONCLUSIVE'
        if physical_margin is not None and physical_margin > 0:
            physical_status = 'CONDITIONAL-PHYSICAL-MAJORANT-REPAIR-EXCLUDED'
        report['decisions'] = {
            'nominal_center': {'status': nominal_status, 'lower_bound_basis': lower['selected_m0_basis'],
                'uses_inherited_physical_premises': conditional,
                'strict_margin_bits640': None if nominal_margin is None else str(nominal_margin),
                'scope': 'fixed exact alpha0,S0,B0,M0 and the same v only'},
            'nominal_direction_existence': {'status': existence_status,
                'strict_margin_bits640': str(existence_margin), 'L0_is_exact_upper_bound': True,
                'scope': 'one direction, unrestricted coefficients; no80-bit C or full certificate'},
            'physical_majorant': {'status': physical_status, 'uses_inherited_physical_premises': True,
                'strict_margin_bits640': None if physical_margin is None else str(physical_margin),
                'scope': 'fixed physical upper-majorant family, not true-L sign or the entire interval box'}}
        report['exact_values'] = {
            'n': dyadic(norm_num, 160), 'c': vector(c, 160), 'b0': vector(bv, 240),
            'r0': vector(residual, 320), 'q0': dyadic(q0, 480), 'u_mid': dyadic(u_mid_num, 260),
            'd_round': dyadic(d_round, 480), 'rounding_absolute_limit': dyadic(round_limit, 480),
            'e0': dyadic(e0, 480), 'residual_norm_squared': dyadic(residual_squared, 640),
            'eps_q': dyadic(eps_q, 480), 'residual_error_t': vector(t, 320),
            'R_plus': dyadic(r_plus, 640)}
        report.update(status='EXACT-CHECK-COMPLETE', stage='complete',
            same_direction_residual_and_rounding_links=True,
            current_pad_frozen_across_C=False, primitive_error_owners_charged_once=True,
            whole_interval_box_exclusion_claimed=False, new_lower_edge=None,
            sufficient_test_failure_means='INCONCLUSIVE, not repair and not impossibility',
            no_true_L_sign_or_RH_conclusion=True)
        inp.verify()
        need(sha(manifest_path) == report['input_manifest_sha256'], 'unchanged input manifest')
        save(out / 'INDEPENDENT_CHECK.json', report)
        return report
    except Exception as exc:
        report.update(status='INCONCLUSIVE', failed_obligation=str(exc),
                      exception_type=type(exc).__name__, automatic_retry=False)
        # If final input stability or serialization failed, invalidate every
        # formerly provisional result, retaining exact observations as data.
        report['decisions'] = {key: {'status': 'INCONCLUSIVE', 'reason': str(exc)}
                               for key in report['decisions']}
        try:
            target = out / 'INDEPENDENT_CHECK.json'
            if target.exists():
                report['invalidates_provisional_report'] = 'INDEPENDENT_CHECK.json'
                target = out / 'CHECK_HOLD.json'
            save(target, report)
        except Exception: pass
        raise
