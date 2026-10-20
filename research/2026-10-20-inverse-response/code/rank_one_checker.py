"""Frozen rank-one scalar reuse only. No work on import; conditional physical premises."""
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from fractions import Fraction as Q
from math import isqrt

SCOPE = 'DELTA128_FIXED_C_RANK_ONE_SCALAR_SCREEN_ONCE_V1'
PREVIOUS_SCOPE = 'DELTA128_FIXED_C_SHARED_ERROR_DIRECTION_SCREEN_ONCE_V1'
SCALAR_DIGITS = 100000
SCALAR_BITS = 332193
ROOT_BITS = 128
ROOT_NAMES = ('m_U', 'rho2_U', 'N2_U', 'J_U', 'W2', 'R_U')
_guard = lambda: None

class Hold(RuntimeError):
    pass

def need(ok, label):
    if not ok:
        raise Hold(label)

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
        need(sha(self.manifest_path) == os.environ['SHIFT_INPUT_SHA256'], 'manifest admission')
        self.m = load(self.manifest_path)
        need(self.m['format'] == 'RANK_ONE_SCALAR_SAVED_INPUTS_V1' and self.m['scope'] == SCOPE,
             'scalar-only manifest scope')
        need(self.m['science_roles'] == ['accepted_report', 'nu_scalar'] and
             self.m['dense_inputs_allowed'] is False and self.m['accepted_run_review'] == 'GO',
             'only two admitted mathematical artifacts')
        self.rows = self.m['bindings']; self.paths = {}
        need(set(self.rows) == set(self.m['allowed_binding_roles']), 'exact metadata allowlist')
        for role, row in self.rows.items():
            p = Path(row['path'])
            need(p.is_absolute() and p.resolve() == p and not p.is_symlink(), 'canonical bound path '+role)
            self.paths[role] = p
        self.verify()

    def verify(self):
        for role, row in self.rows.items():
            p = self.paths[role]; _guard()
            need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'],
                 'immutable admitted file '+role)

    def read(self, role):
        return load(self.paths[role])

    def h(self, role):
        return self.rows[role]['sha256']


def admit_previous(inp):
    report = inp.read('accepted_report'); worker = inp.read('accepted_worker')
    plan = inp.read('accepted_plan'); manifest = inp.read('accepted_inputs')
    host = inp.read('accepted_host'); tool = inp.read('accepted_tool')
    final = inp.read('accepted_final_manifest'); audit = inp.read('accepted_final_result')
    need(inp.h('accepted_report') == '1d8335c6f041d561f26d021663620d17e98e54f10854c5f9368c1f92617567b1' and
         inp.h('accepted_plan') == 'adf09382423ae26bec6d944990e12c7d26b89fd94795ab7375212ccfd013811b',
         'exact accepted single run')
    need(report['format'] == 'FIXED_C_SHARED_ERROR_DIRECTION_SCREEN_V1' and
         report['scope'] == plan['scope'] == worker['scope'] == PREVIOUS_SCOPE and
         report['status'] == 'EXACT-SHARED-ERROR-SCREEN-COMPLETE' and report['stage'] == 'complete',
         'completed scalar-producing run')
    need(worker['status'] == 'MATH-COMPLETE-RESOURCE-GATE-PENDING' and
         worker['report_status'] == report['status'] and
         worker['check_report_sha256'] == inp.h('accepted_report') and
         worker['checker_sha256'] == plan['code_sha256']['shift_checker.py'] == inp.h('previous_shift_checker') and
         worker['plan_sha256'] == host['plan_sha256'] == final['plan_sha256'] == inp.h('accepted_plan'),
         'executed source/report/plan chain')
    need(report['input_manifest_sha256'] == worker['input_manifest_sha256'] ==
         plan['input_manifest_sha256'] == inp.h('accepted_inputs'), 'input manifest chain')
    need(report['input_sha256'] == {k: row['sha256'] for k, row in manifest['bindings'].items()},
         'complete inherited original-input references; not reopened')
    for name, expected in plan['code_sha256'].items():
        role = 'previous_'+Path(name).stem
        need(inp.h(role) == expected and inp.paths[role] == Path(plan['code_root'])/name,
             'previous executed code '+name)
    need(inp.h('previous_host') == plan['host_wrapper_sha256'] and
         inp.paths['previous_host'] == Path(plan['host_wrapper']), 'previous host source')
    need(host['status'] == 'EXTERNAL-RESOURCE-WITNESS-VERIFIED' and host['resource_acceptance'] is True and
         host['actual_wait4_completed'] is True and host['no_remaining_descendants'] is True and
         host['observer_exit_code'] == 0 and host['closure_evidence'] == 'wait4(-1,WNOHANG|__WALL) -> ECHILD' and
         0 < host['complete_wall_ns'] == host['tree_cpu_capacity_upper_ns'] < 60_000_000_000 and
         host['CPU_affinity'] == [0], 'actual accepted resource/reap')
    need(tool['actual_tool_exit_code'] == 0 and tool['retries'] == 0 and
         tool['final_stdout']['status'] == host['status'] and
         tool['final_stdout']['plan_sha256'] == inp.h('accepted_plan') and
         tool['final_stdout']['external_receipt_sha256'] == inp.h('accepted_host'), 'actual terminal evidence')
    need(host['final_artifact_manifest_sha256'] == inp.h('accepted_final_manifest') and
         final['format'] == 'SHIFT372_FINAL_BYTES_V1', 'final artifact linkage')
    root = inp.paths['accepted_final_manifest'].parent
    by_path = {str(p): role for role, p in inp.paths.items()}
    seen = set()
    for row in final['files']:
        rel = Path(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen, 'safe finalized path')
        seen.add(str(rel)); p = root/rel
        need(str(p) in by_path, 'no unbound finalized file read')
        role = by_path[str(p)]
        need(inp.rows[role]['bytes'] == row['bytes'] and inp.h(role) == row['sha256'], 'finalized byte identity')
    need(len(seen) == 13 and 'math/INDEPENDENT_CHECK.json' in seen, 'complete13 artifact metadata')
    need(inp.paths['accepted_report'] == root/'math/INDEPENDENT_CHECK.json' and
         inp.paths['accepted_worker'] == root/'WORKER_RESULT.json', 'actual finalized report/worker paths')
    resource = inp.read('previous_resource')
    need(resource['worker_exit_code'] == 0 and resource['worker_reaped'] is True and
         resource['worker_wait4']['maxrss_kib'] <= 327680 and resource['observed_worker_peak_kib'] <= 327680 and
         resource['checker_report_sha256'] == inp.h('accepted_report'), 'prior worker resource/report')
    need(audit['status'] == 'FINAL-RESOURCE-ACCEPTED-FIXED-MAJORANT-EXCLUDED' and
         audit['resource_acceptance'] is True and audit['candidate_executions'] == 1 and audit['retries'] == 0 and
         audit['actual_tool_exit_code'] == 0, 'accepted final audit')
    for name, role in (('check_report_sha256','accepted_report'), ('plan_sha256','accepted_plan'),
                       ('checker_sha256','previous_shift_checker'), ('input_manifest_sha256','accepted_inputs'),
                       ('external_receipt_sha256','accepted_host'),
                       ('final_artifact_manifest_sha256','accepted_final_manifest'),
                       ('independent_review_sha256','accepted_code_review')):
        need(audit['bindings'][name] == inp.h(role), 'external audit binding '+name)
    need(report['decisions'] == worker['mathematical_decisions'] and
         report['numerical_status'] == audit['mathematical_status'] ==
         'CONDITIONAL-FIXED-SHARED-ERROR-MAJORANT-EXCLUDED', 'prior exclusion scope retained')
    need(report['P_up_representation'] == 'EXACT-RATIONAL-NO-SWITCH' and
         report['physical_P_radius_or_UCERT_pad_added'] is False and
         report['eta_is_exact_columnwise_e'] is True and report['unknown_slack_contracted'] is False and
         report['repeated_coefficients_collected_before_radii'] is True, 'prior physical padding conventions')
    need(report['cache_reuse']['c_Cv_and_n_vv'] == 'ACCEPTED-EXACT-CACHE-NOT-RECOMPUTED' and
         report['cache_reuse']['coefficient_report_sha256'] == manifest['bindings']['coefficient_report']['sha256'],
         'inherited c/n cache binding; no coefficient array opened')
    order = report['column_bound_admission']
    need(order['terms'] == 68 and order['sum_of_squares_identity_verified'] is True and
         order['sigma_bar_square_dominates_sigma2'] is True and
         order['column_order']['old_coefficient_indices'] == list(range(64)) and
         order['column_order']['new_coefficient_indices'] == [64,65,66,67] and
         order['column_order']['new_source_columns'] == [0,1,2,3] and
         order['column_order']['action_arrays'] == ['old_B','new_B'], 'accepted64+4 e derivation')
    need(manifest['bindings']['saved_SHIFT_SCALARS'] == inp.rows['nu_scalar'], 'nu scalar original binding')
    scalar = inp.read('nu_scalar')
    need(scalar['model_id'] == 'DELTA128_PUP68_NEW_C_V1' and
         scalar['trial_gram_majorant'] == 'P<=P_up<=nu68^2 I' and
         scalar['physical_errors_unchanged'] is True, 'same admitted nu convention')
    return report, scalar['values'], {
        'status':'ACCEPTED-SCALAR-REUSE', 'accepted_report_sha256':inp.h('accepted_report'),
        'accepted_plan_sha256':inp.h('accepted_plan'), 'accepted_checker_sha256':inp.h('previous_shift_checker'),
        'accepted_final_audit_sha256':inp.h('accepted_final_result'),
        'accepted_external_host_sha256':inp.h('accepted_host'), 'accepted_tool_sha256':inp.h('accepted_tool'),
        'nu_scalar_sha256':inp.h('nu_scalar'), 'coefficient_report_sha256':report['cache_reuse']['coefficient_report_sha256'],
        'frozen_C_sha256':manifest['bindings']['saved_C']['sha256'],
        'frozen_v_sha256':manifest['bindings']['witness_vector']['sha256'],
        'physical_P_UP_EXACT_sha256':manifest['bindings']['saved_P_UP_EXACT']['sha256'],
        'inherited_physical_input_references':report['input_sha256'],
        'coordinates':'211 coordinates appended with161 exact zeros; inherited from accepted source/cache admission',
        'column_order':order['column_order'], 'original_arrays_reopened':False,
        'physical_inclusions_reproved':False}


def interval_pair(obj, name, nonnegative=False):
    need(set(obj) == {'lower','upper'}, 'endpoint schema '+name)
    lo, hi = rational(obj['lower']), rational(obj['upper'])
    need(scmp(lo,hi) <= 0, 'reversed interval '+name)
    if nonnegative:
        need(lo.numerator >= 0 and hi.numerator >= 0, 'negative admitted norm interval '+name)
    return lo,hi


def linear_ball(balls, coefficients, constant=Q(0)):
    need(len(coefficients) == 5, 'five primitive coefficients')
    center=constant; radius=Q(0)
    for name, coefficient in zip(('m','x','u','b','y'),coefficients):
        c,r=balls[name]
        center=sadd(center,smul(coefficient,c))
        radius=sadd(radius,smul(abs(coefficient),r))
    return ssub(center,radius),sadd(center,radius)


def sint_shift(value,bits):
    need(type(value) is int and value >= 0 and type(bits) is int and bits >= 0 and
         value.bit_length()+bits <= SCALAR_BITS, 'scalar shift pre-operation ceiling')
    _guard(); return value << bits


def sqrt_up(value,name,certificates):
    sg(value); need(value.numerator >= 0 and name in ROOT_NAMES and name not in certificates,
                    'named nonnegative root, one evaluation')
    _guard(); scale=sint_shift(1,ROOT_BITS)
    scaled=sint_shift(value.numerator,2*ROOT_BITS)
    den=value.denominator
    need(den > 0 and scaled.bit_length() <= SCALAR_BITS and den.bit_length() <= SCALAR_BITS,
         'root integer division pre-operation ceiling')
    floor=scaled//den; _guard()
    need(floor.bit_length() <= SCALAR_BITS, 'isqrt operand ceiling')
    k=isqrt(floor); _guard()
    k2=sint_product(k,k); exact=sint_product(k2,den)==scaled
    upnum=k if exact else sint_add(k,1)
    lower=sg(Q(k,scale)); upper=sg(Q(upnum,scale)); _guard()
    need(scmp(smul(lower,lower),value) <= 0 and scmp(smul(upper,upper),value) >= 0,
         'root rational-square certificate')
    need(value.numerator != 0 or upper.numerator == 0, 'exact zero root')
    certificates[name]={'radicand':st(value),'fractional_binary_bits':ROOT_BITS,
        'scaled_floor':st(Q(floor)), 'integer_root':st(Q(k)), 'lower':st(lower),'upper':st(upper),
        'exact_zero':value.numerator==0,'perfect_scaled_square':exact,
        'upper_square_verified':True,'lower_square_verified':True}
    return upper


def distance_from_zero(lo,hi,name):
    need(scmp(lo,hi) <= 0, 'reversed real overlap '+name)
    if lo.numerator > 0: return lo
    if hi.numerator < 0: return -hi
    return Q(0)


def ep(lo,hi):
    return {'lower':st(lo),'upper':st(hi)}


def evaluate(saved,nu_values,report):
    balls={}
    for label,key in (('m','m_v'),('x','d_v'),('u','k_v'),('b','n_c'),('y','f_c')):
        obj=saved['primitive_contractions'][key]
        need(set(obj)=={'center','absolute_radius'}, 'primitive scalar ball schema '+label)
        center,radius=rational(obj['center']),rational(obj['absolute_radius'])
        need(radius.numerator >= 0, 'negative primitive radius '+label)
        balls[label]=(center,radius)
    scalars=saved['exact_scalars']
    p0,t,e,a,h,n=(rational(scalars[key]) for key in ('P0','t','e','a','h','n_cached_exact'))
    nu=rational(nu_values['nu68'])
    need(a.numerator > 0 and n.numerator > 0 and h==Q(1,128), 'a/n positive and fixed h')
    need(all(v.numerator >= 0 for v in (p0,t,e,nu)), 'nonnegative P0/t/e/nu')
    need(h==rational(nu_values['h']) and a==rational(nu_values['eta1']) and
         a==ssub(rational(nu_values['delta1']),rational(nu_values['Fw'])),
         'independently admitted a; never infer a=h')
    ll,lu=interval_pair(saved['collected_enclosures']['L'],'L')
    rl,ru=interval_pair(saved['collected_enclosures']['R'],'R',True)
    jl,ju=interval_pair(saved['collected_enclosures']['J'],'J',True)
    need(saved['collected_enclosures']['L_intersection_tightening'] is False, 'same saved L enclosure')
    e2=smul(e,e); e2a=sdiv(e2,a)
    aminus=rational(saved['Q_symbolic_endpoints']['lower']['A'])
    need(aminus==sadd(ll,e2a), 'prior A_minus identity')
    prior_d0=ssub(n,aminus)
    old=saved['decisions']['shared_error']['branch_checks']
    need(prior_d0.numerator < 0 and
         all(old[key]['strict'] is True and old[key]['relation']=='gt' and
             rational(old[key]['D0'])==prior_d0 for key in ('lower_single','lower_two')),
         'retain exact old exclusion without skipping new bounds')
    nu2t=smul(smul(nu,nu),t)
    w2=nu2t if scmp(nu2t,p0)<=0 else p0
    need(w2.numerator >= 0 and w2==rational(scalars['W2']), 'same exact saved W2 cap')
    d=sadd(a,h); q=sadd(a,smul(Q(2),h)); hd=smul(h,d); q2=smul(q,q)
    beta_l,beta_u=linear_ball(balls,(Q(0),-d,Q(1),Q(0),Q(0)))
    mu0_l,mu0_u=linear_ball(balls,(Q(0),-d,Q(1),Q(-1),q))
    mu_l=ssub(mu0_l,smul(hd,p0)); mu_u=mu0_u
    need(scmp(mu_l,mu_u)<=0, 'mu endpoints with p_L=0')
    _,rho2_u=linear_ball(balls,(Q(1),smul(Q(2),q),Q(-4),Q(4),smul(Q(-4),q)),smul(q2,p0))
    _,n2_u=linear_ball(balls,(Q(0),Q(0),Q(0),Q(4),smul(Q(-4),q)),smul(q2,p0))
    _,s0_u=linear_ball(balls,(Q(0),Q(0),Q(0),Q(1),-q),smul(hd,p0))
    m_u=sadd(balls['m'][0],balls['m'][1])
    need(all(v.numerator>=0 for v in (m_u,rho2_u,n2_u,ju,w2,ru)), 'negative norm/radical upper; no clipping')
    roots={}; report['root_certificates']=roots
    for name,value in zip(ROOT_NAMES,(m_u,rho2_u,n2_u,ju,w2,ru)):
        report['counts']['root_evaluations_started'].append(name)
        sqrt_up(value,name,roots)
    mroot,rhoroot,nroot,jroot,wroot,rroot=(rational(roots[name]['upper']) for name in ROOT_NAMES)
    du=smul(a,ssum((s0_u,smul(e,nroot),e2)))
    need(du.numerator>=0, 'negative combined denominator upper; s0_U not clipped')
    j_l=ssub(beta_l,smul(e,mroot)); j_u=sadd(beta_u,smul(e,mroot))
    z_direct=distance_from_zero(j_l,j_u,'direct')
    if scmp(smul(Q(2),e),rhoroot)<=0:
        psi=ssub(smul(e,rhoroot),e2); psi_branch='2e<=Rho_U'
    else:
        psi=sdiv(smul(rhoroot,rhoroot),Q(4)); psi_branch='2e>Rho_U'
    q_l=ssub(ssub(mu_l,smul(e,rhoroot)),e2); q_u=sadd(mu_u,psi)
    z_residual=distance_from_zero(q_l,q_u,'residual')
    if du.numerator==0:
        need(z_direct.numerator==0 and z_residual.numerator==0, 'zero denominator with positive certified overlap')
        delta_direct=delta_residual=Q(0)
    else:
        delta_direct=sdiv(smul(z_direct,z_direct),du)
        delta_residual=sdiv(smul(z_residual,z_residual),du)
    capped_second=sadd(wroot,sdiv(smul(Q(2),rroot),a))
    cap=jroot if scmp(jroot,capped_second)<=0 else capped_second
    bq=ssum((lu,e2a,smul(e,cap)))
    direct_baseline=sdiv(m_u,a)
    u_direct=ssub(direct_baseline,delta_direct); u_residual=ssub(bq,delta_residual)
    need(u_direct.numerator>=0 and u_residual.numerator>=0, 'negative certified inverse upper bound')
    upper=u_direct if scmp(u_direct,u_residual)<=0 else u_residual
    margin_direct=ssub(n,u_direct); margin_residual=ssub(n,u_residual)
    pass_direct=margin_direct.numerator>0; pass_residual=margin_residual.numerator>0
    verdict='CONDITIONAL-RANK-ONE-DIRECTION-PASS' if (pass_direct or pass_residual) else 'INCONCLUSIVE'
    report.update(fixed_root_precision=ROOT_BITS, primitive_field_mapping={
        'm':'primitive_contractions.m_v','x':'primitive_contractions.d_v','u':'primitive_contractions.k_v',
        'b':'primitive_contractions.n_c','y':'primitive_contractions.f_c'},
        prior_result={'A_minus':st(aminus),'n_minus_A_minus':st(prior_d0),
                      'scope':'unchanged old fixed majorant excluded; new bounds still both evaluated'},
        beta_interval=ep(beta_l,beta_u),mu_interval=ep(mu_l,mu_u),
        exact_inputs={key:st(value) for key,value in [('a',a),('h',h),('n',n),('e',e),('P0',p0),('t',t),('nu',nu)]},
        scalar_lifts={key:st(value) for key,value in [('d',d),('q',q),('m_U',m_u),('rho2_U',rho2_u),
            ('N2_U',n2_u),('s0_U',s0_u),('D_U',du),('W2',w2),('psi',psi)]},
        psi_branch=psi_branch,direct_real_interval=ep(j_l,j_u),residual_real_interval=ep(q_l,q_u),
        zetas={'direct':st(z_direct),'residual':st(z_residual),
            'direct_positive':z_direct.numerator>0,'residual_positive':z_residual.numerator>0},
        lower_corrections={'direct':st(delta_direct),'residual':st(delta_residual),'summed':False},
        baselines={'direct_m_U_over_a':st(direct_baseline),'residual_B_Q':st(bq)},
        baseline_gaps={'direct':st(ssub(direct_baseline,n)),'residual':st(ssub(bq,n))},
        upper_bounds={'direct':st(u_direct),'residual':st(u_residual),'minimum':st(upper)},
        margins={'direct_n_minus_U':st(margin_direct),'residual_n_minus_U':st(margin_residual)},
        degeneracy={'D_U_zero':du.numerator==0,'zero_error':e.numerator==0,
                    'direct_zero_lower_correction':z_direct.numerator==0,
                    'residual_zero_lower_correction':z_residual.numerator==0},
        validity={'norm_upper_signs_checked':True,'s0_upper_not_clipped':True,'p_lower_fixed_zero':True,
                  'P0_padding_added_again':False,'final_nonnegative_bounds_checked':True},
        decisions={'rank_one':{'status':verdict,'target':'min(U_direct,U_residual)<exact n',
            'direct_strict_pass':pass_direct,'residual_strict_pass':pass_residual,
            'direct_equality':margin_direct.numerator==0,'residual_equality':margin_residual.numerator==0,
            'failure_is_not_exclusion':True,'physical_premises_inherited':True}},numerical_status=verdict)


def run(source_root,manifest_path,output_path,guard):
    global _guard
    _guard=guard;sys.set_int_max_str_digits(SCALAR_DIGITS)
    need(os.environ.get('SHIFT_CHARGED_EXACT_CHECK')=='1','charged scalar worker required')
    need(not any(name.split('.')[0] in {'flint','numpy','scipy','mpmath'} for name in sys.modules),
         'stdlib-only scalar checker')
    out=Path(output_path);out.mkdir(exist_ok=False)
    report={'format':'FIXED_C_RANK_ONE_SCALAR_SCREEN_V1','scope':SCOPE,'status':'HOLD','stage':'admission',
        'resource_acceptance':False,'provisional_until_actual_exit_and_resource_acceptance':True,
        'RH_PROOF':'NOT-OBTAINED','physical_inclusions_reproved':False,
        'decisions':{'rank_one':{'status':'HOLD'}},
        'counts':{'exact_check_calls':1,'directions':1,'root_evaluations_started':[],
            'matrix_reads':0,'direction_contractions':0,'column_radius_recomputations':0,
            'C_times_v_recomputations':0,'v_norm_recomputations':0,'source_actions_integrals':0,
            'parameter_searches':0,'full372_consumers':0,'old_checker_replays':0,'retries':0}}
    try:
        inp=Inputs(manifest_path)
        need(str(source_root)==inp.m['source_root'],'bound scalar-only source root')
        report['input_manifest_sha256']=sha(manifest_path)
        report['input_sha256']={k:row['sha256'] for k,row in inp.rows.items()}
        saved,values,admission=admit_previous(inp);report['admission']=admission
        report['stage']='frozen_scalar_only_evaluation'
        evaluate(saved,values,report)
        need(report['counts']['root_evaluations_started']==list(ROOT_NAMES),'exactly six named roots')
        report.update(status='EXACT-RANK-ONE-SCALAR-SCREEN-COMPLETE',stage='complete',
                      automatic_retry=False,automatic_follow_on_compute=False)
        inp.verify();need(sha(manifest_path)==report['input_manifest_sha256'],'manifest unchanged')
        save(out/'INDEPENDENT_CHECK.json',report);return report
    except Exception as exc:
        report.update(status='HOLD',failed_obligation=str(exc),exception_type=type(exc).__name__,automatic_retry=False)
        report['decisions']={'rank_one':{'status':'HOLD','reason':str(exc)}}
        try:
            target=out/'INDEPENDENT_CHECK.json'
            if target.exists():target=out/'CHECK_HOLD.json'
            save(target,report)
        except Exception:pass
        raise
