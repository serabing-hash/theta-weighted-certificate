"""Independent stdlib exact checker for one fixed shifted full372 certificate.
No producer/runtime/helper imports. Arithmetic only in run(), inside timed entry.
Adapted endpoint/factor utilities retain original CC BY-NC 4.0 provenance.
"""
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import sys
import time
from fractions import Fraction as Q

SCOPE = 'SHIFT372_H2_DELTA_STAR_FIXED_C_ONCE_V1'
RANK, N = 68, 372
P, CBITS, UBITS, MAXBITS = 160, 80, 100, 1024
ETA_TEXT = '1446776856241610348487954379752034183297365381007/92620636523388719034562694367509285563269120000000'
C_SHA = 'c459b5c283020808e6d52ac60e3749137c11cd9db21e98fa5178ff0698ade513'
_guard = lambda: None

class Hold(RuntimeError):
    """Unmet certificate obligation; never an impossibility theorem."""


def must(ok, label):
    if not ok:
        raise Hold(label)


def integer(v):
    must(type(v) is str and re.fullmatch(r'0|-?[1-9][0-9]*', v) is not None,
         'noncanonical integer text')
    return int(v)


def rational(v):
    must(type(v) is str and re.fullmatch(r'(0|-?[1-9][0-9]*)(/[1-9][0-9]*)?', v) is not None,
         'noncanonical rational text')
    return Q(v)


def bound(v):
    must(type(v) is int and v.bit_length() <= MAXBITS, 'dense 1024-bit ceiling')
    return v


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as fd:
        while block := fd.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def load(path):
    def pairs(items):
        d = {}
        for key, value in items:
            must(key not in d, 'duplicate JSON key ' + key)
            d[key] = value
        return d
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs)


def durable(path, data):
    raw = (json.dumps(data, indent=2, sort_keys=True) + '\n').encode()
    with Path(path).open('xb') as fd:
        fd.write(raw); fd.flush(); os.fsync(fd.fileno())
    must(Path(path).read_bytes() == raw, 'checker report durable byte readback')
    fd = os.open(str(Path(path).parent), os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def introws(raw, shape, limit=True):
    nr, nc = shape
    must(type(raw) is list and len(raw) == nr and
         all(type(row) is list and len(row) == nc for row in raw), 'matrix shape')
    out = [[integer(x) for x in row] for row in raw]
    if limit:
        for row in out:
            for v in row: bound(v)
    return out


def same_symmetric(a):
    n = len(a)
    return all(a[i][j] == a[j][i] for i in range(n) for j in range(i))


def interval(path, shape, bits, symmetric):
    obj = load(path)
    must(obj['format'] == 'DYADIC_INTERVAL_MATRIX_V1' and obj['shape'] == list(shape),
         'interval schema ' + str(path))
    must(type(obj['bits']) is int and obj['bits'] == bits and
         obj['symmetric'] is symmetric, 'interval precision/symmetry flag')
    c, r = introws(obj['center'], shape), introws(obj['radius'], shape)
    must(all(v >= 0 for row in r for v in row), 'negative radius')
    if symmetric:
        must(shape[0] == shape[1] and same_symmetric(c) and same_symmetric(r),
             'center and radius symmetry')
    return c, r


def exact(path, shape, bits):
    obj = load(path)
    must(obj['format'] == 'DYADIC_EXACT_MATRIX_V1' and obj['shape'] == list(shape) and
         type(obj['bits']) is int and obj['bits'] == bits, 'exact matrix schema')
    return introws(obj['numerators'], shape)


def accumulation_budget(a, b, inner):
    # A priori absolute bound covers products AND all canceled partial sums.
    # The bound uses only bit lengths; no oversized trial product is allocated.
    must(inner > 0 and a >= 0 and b >= 0,'product budget dimensions/sign')
    if a and b:
        must(a.bit_length()+b.bit_length()+(inner-1).bit_length() <= MAXBITS,
             '1024-bit absolute partial-sum budget')


def maxabs(rows):
    return max((abs(v) for row in rows for v in row), default=0)


def floor_ratio(num, den):
    must(den > 0, 'positive rational denominator')
    return num // den


def ceil_ratio(num, den):
    must(den > 0, 'positive rational denominator')
    return -((-num) // den)


def quantize_endpoints(lo, hi, den, bits):
    """Integer endpoint route, including correct negative floor/ceiling."""
    must(lo <= hi and den > 0, 'ordered rational endpoints')
    scale = 1 << bits
    low = floor_ratio(lo * scale, den)
    high = ceil_ratio(hi * scale, den)
    c = (low + high) // 2
    r = max(c - low, high - c)
    return bound(c), bound(r)


def quantize_scalar(q, bits=P):
    return quantize_endpoints(q.numerator, q.numerator, q.denominator, bits)


def check_input_requant(source, saved, shape, symmetric, aobs=False):
    obj = load(source)
    if aobs:
        must(obj['shape'] == list(shape) and obj['bits'] == 100 and
             obj['scope'] == 'true full-line W*W; source moment tails retained', 'A schema/full-line scope')
        den = 1 << 100
    else:
        must(obj['format'] == 'RATIONAL_MID_RADIUS_MATRIX_V1' and obj['shape'] == list(shape) and
             obj['symmetric'] is symmetric, 'saved68 source matrix schema')
        den = integer(obj['denominator']); must(den > 0, 'source denominator')
    pairs = obj['entries']
    must(len(pairs) == shape[0] and all(len(row) == shape[1] for row in pairs), 'source shape')
    c, r = interval(saved, shape, P, symmetric)
    for i, row in enumerate(pairs):
        for j, pair in enumerate(row):
            must(type(pair) is list and len(pair) == 2, 'source pair')
            sc, sr = map(integer, pair); must(sr >= 0, 'source radius')
            low, high = sc - sr, sc + sr
            if symmetric:
                tc, tr = map(integer, pairs[j][i]); must(tr >= 0, 'transpose source radius')
                # Declared containing symmetric hull; never intersect an interval.
                low, high = min(low, tc - tr), max(high, tc + tr)
            ec, er = quantize_endpoints(low, high, den, P)
            must((c[i][j], r[i][j]) == (ec, er), 'exact 160-bit source requantization')
    return c, r


def scalar_product_ball(ac, ar, xc, xr):
    # Independently derive the symmetric error envelope from the four terms.
    must(ar >= 0 and xr >= 0, 'product nonnegative radii')
    center = bound(ac * xc)
    radius = bound(abs(ac) * xr + ar * abs(xc) + ar * xr)
    return center, radius


def right_endpoints(center, radius, coefficients):
    """Interval-times-exact product, independently using signed endpoints."""
    cols = list(zip(*coefficients))
    magnitude=max((abs(c)+r for cr,rr in zip(center,radius) for c,r in zip(cr,rr)),default=0)
    accumulation_budget(magnitude,maxabs(coefficients),len(coefficients))
    outlow, outhigh = [], []
    for cr, rr in zip(center, radius):
        low = [c-r for c,r in zip(cr,rr)]; high = [c+r for c,r in zip(cr,rr)]
        rl, rh = [], []
        for col in cols:
            sl = sh = 0
            for l,h,c in zip(low,high,col):
                if c >= 0: sl += l*c; sh += h*c
                else: sl += h*c; sh += l*c
            bound(sl); bound(sh); rl.append(sl); rh.append(sh)
        outlow.append(rl); outhigh.append(rh)
    return outlow, outhigh


def consumer_verify(A, alpha, S, B, C, U, Ucert, rows):
    """68-skinny compression, no full product workspace; all 372^2 entries."""
    ac, ar = alpha; Ac, Ar = A; Sc, Sr = S; Bc, Br = B; Uc, Ur = U
    cols = list(zip(*C))
    # First contraction S*C. Its endpoints contain every saved S member.
    SCl, SCh = right_endpoints(Sc, Sr, C)
    Bcols = list(zip(*Bc)); Rcols = list(zip(*Br))
    cmax=maxabs(C)
    bmax=max(abs(c)+r for cr,rr in zip(Bc,Br) for c,r in zip(cr,rr))
    accumulation_budget(cmax,bmax,RANK)
    accumulation_budget(cmax,max(maxabs(SCl),maxabs(SCh)),RANK)
    must(len(rows) == N and all(v >= 0 for v in rows), 'Loewner row shape/sign')
    for i in range(N):
        _guard()
        ci = cols[i]
        must(rows[i] == sum(Ur[i]), 'exact Loewner radius row sum')
        for j in range(i+1):
            # The independently parsed U center/radius and Ucert are symmetric;
            # S is symmetric, so checking one triangle plus symmetry checks all entries.
            cj = cols[j]
            # Xij = C_i^T B_j and Xji, independent signed-endpoint sums.
            xl = xh = tl = th = 0
            for c,bc,br in zip(ci,Bcols[j],Rcols[j]):
                if c >= 0: xl += c*(bc-br); xh += c*(bc+br)
                else: xl += c*(bc+br); xh += c*(bc-br)
            for c,bc,br in zip(cj,Bcols[i],Rcols[i]):
                if c >= 0: tl += c*(bc-br); th += c*(bc+br)
                else: tl += c*(bc+br); th += c*(bc-br)
            yl = yh = 0
            for k,c in enumerate(ci):
                lo, hi = SCl[k][j], SCh[k][j]
                if c >= 0: yl += c*lo; yh += c*hi
                else: yl += c*hi; yh += c*lo
            for v in [xl,xh,tl,th,yl,yh]: bound(v)
            pc, pr = scalar_product_ball(ac, ar, Ac[i][j], Ar[i][j])
            low = bound(pc-pr - ((xh+th) << CBITS) + yl)
            high = bound(pc+pr - ((xl+tl) << CBITS) + yh)
            ec, er = quantize_endpoints(low, high, 1 << (P + 2*CBITS), UBITS)
            must((Uc[i][j],Ur[i][j]) == (ec,er), 'every full372 model endpoint and final100 rounding')
            must(Ucert[i][j] == Uc[i][j] + (rows[i] if i == j else 0), 'diagonal Loewner upper matrix')
    return {'entries': N*N, 'independent_triangle_entries':N*(N+1)//2, 'row_sums': N, 'final_rounding_bits': UBITS,
            'method': 'Independent signed endpoints, two skinny contractions; no producer imports'}


def factor_verify(factor, Ucert):
    n = len(Ucert); scale = 1 << CBITS
    must(factor.get('format') == 'SHIFT372_EXACT_FACTOR_V1' and factor['shape'] == [n,n] and
         factor['bits'] == CBITS and factor['target'] == '1' and factor['accepted_pivots'] == n and
         factor['precision_bits'] == P and factor['block_size'] == 16,
         'direct-I fresh factor schema')
    L = introws(factor['L_numerators'], (n,n))
    M = introws(factor['inverse_factor_numerators'], (n,n))
    D = [bound(integer(v)) for v in factor['D_numerators']]
    must(len(D) == n and all(d > 0 for d in D), 'positive D80')
    must(2*maxabs(L).bit_length()+max(D).bit_length()+(n-1).bit_length() <= MAXBITS,
         'factor triple-product absolute partial-sum ceiling')
    accumulation_budget(maxabs(L),maxabs(M),n)
    must(all(L[i][i] == scale for i in range(n)), 'unit lower factor')
    must(all(L[i][j] == M[i][j] == 0 for i in range(n) for j in range(i+1,n)),
         'factor and inverse exactly triangular')
    pivots = factor['pivot_enclosures_bits160']
    must(len(pivots) == n, 'all372 pivot count')
    for p in pivots:
        must(type(p) is list and len(p) == 2, 'pivot pair')
        c,r = map(integer,p); bound(c); bound(r)
        must(r >= 0 and c-r > 0, 'strict positive outward pivot lower endpoint')
    # LDL residual: symmetry halves entries, each dot ends at min(i,j).
    residual_rows = [0]*n
    for i in range(n):
        _guard()
        li = L[i]
        for j in range(i+1):
            lj = L[j]; product = 0
            for k in range(j+1):
                product += li[k]*D[k]*lj[k]; bound(product)
            v = (1 << (3*CBITS) if i == j else 0) - (Ucert[i][j] << (3*CBITS-UBITS)) - product
            bound(v); av = abs(v); residual_rows[i] += av
            if i != j: residual_rows[j] += av
    rho = Q(max(residual_rows), 1 << (3*CBITS))
    # L*M is lower triangular. Preserve LM orientation of the Neumann proof.
    erows, ecols = [0]*n, [0]*n
    mrows, mcols = [0]*n, [0]*n
    for i in range(n):
        _guard()
        for j in range(i+1):
            v = 0
            for k in range(j,i+1):
                v += L[i][k]*M[k][j]; bound(v)
            if i == j: v -= scale*scale
            av = abs(v); erows[i] += av; ecols[j] += av
            av = abs(M[i][j]); mrows[i] += av; mcols[j] += av
    for row in [erows,ecols,mrows,mcols,residual_rows]:
        for v in row: bound(v)
    e1,einf = Q(max(ecols),scale*scale),Q(max(erows),scale*scale)
    m1,minf = Q(max(mcols),scale),Q(max(mrows),scale)
    d0 = Q(min(D),scale)
    must(e1 < 1 and einf < 1 and m1 > 0 and minf > 0, 'exact inverse-factor norm gates')
    margin = d0*(1-e1)*(1-einf)/(m1*minf)-rho
    must(0 < margin <= 1, 'strict positive fresh direct-I margin')
    vals = {'rho0':rho,'e1':e1,'einf':einf,'m1':m1,'minf':minf,'d0':d0,'mu372':margin}
    must(set(factor['exact_check_values']) == set(vals), 'exact factor scalar keys')
    for k,v in vals.items():
        must(rational(factor['exact_check_values'][k]) == v, 'exact factor scalar '+k)
    return {k:str(v) for k,v in vals.items()}


def source_chain(manifest, paths):
    inp = load(paths['saved_input_manifest']); iv = load(paths['saved_input_verification'])
    sm = load(paths['saved_output_manifest']); ck = load(paths['saved_checker'])
    fm = load(paths['final_math']); fr = load(paths['final_resource']); fv = load(paths['final_verdict'])
    ih = sha(paths['saved_input_manifest'])
    must(inp['format']=='SAVED68_FIXED_INPUT_MANIFEST_V1' and inp['constants']['eta']==ETA_TEXT and
         inp['constants']['tau']=='1/100' and inp['constants']['old_columns']==64 and
         inp['constants']['new_columns']==[0,1,2,3] and inp['constants']['observations']==372,
         'saved68 exact operator and trial-order constants')
    old_manifest={}
    for line in paths['inherited_old_manifest'].read_text().splitlines():
        h,name=line.split(None,1)
        must(name not in old_manifest,'duplicate original source-manifest path')
        old_manifest[name]=h
    must(old_manifest['inputs/OBSERVATION_COORDINATE_ORDER.csv']==sha(paths['observation_order']) and
         old_manifest['certificates/SHARP_TAIL_REPLAY.json']==sha(paths['sharp']),
         'original accepted observation coordinate and sharp-tail byte bindings')
    must(iv['inputs'] == inp['inputs'] and iv['manifest_sha256'] == ih == sm['manifest_sha256'] ==
         ck['input_manifest_sha256'] == fm['input_manifest_sha256'] == fr['input_manifest_sha256'] ==
         fv['input_manifest_sha256'], 'saved68 exact input chain')
    must(all(manifest['inputs'].get('inherited_'+role) == rec for role,rec in inp['inputs'].items()),
         'all inherited domain/order/T/X/Y/physical binding files exact path/size/hash-covered')
    must('saved_outer_receipt' in paths and fr['receipt_sha256'] == sha(paths['saved_outer_receipt']),
         'saved68 authentic outer closure receipt bytes')
    must(sha(paths['A']) == inp['inputs']['A']['sha256'], 'same inherited A')
    bindings = {'D68':'D68.json','K68':'K68.json','N68':'N68.json','E68':'E68.json',
                'norm':'NORM_ERROR_CERTIFICATE.json','saved_input_verification':'INPUT_VERIFICATION.json',
                'saved_status':'SAVED68_STATUS.json','saved_output_manifest':'OUTPUT_MANIFEST.json'}
    for role, name in bindings.items():
        h = sha(paths[role]); must(ck['output_hashes'][name] == h, 'charged saved checker bytes '+name)
        if name in sm['outputs']:
            must(sm['outputs'][name]['sha256'] == h and sm['outputs'][name]['size'] == paths[role].stat().st_size,
                 'saved output manifest bytes '+name)
    must(fm['charged_checker_report_sha256'] == sha(paths['saved_checker']) and
         fm['norm_error_certificate_sha256'] == sha(paths['norm']) and
         fm['producer_status_sha256'] == sha(paths['saved_status']), 'final math authentic dependency binding')
    must(fv['science_report']['sha256'] == sha(paths['final_math']) and
         fv['resource_report']['sha256'] == sha(paths['final_resource']) and
         fv['outer_receipt_sha256'] == fr['receipt_sha256'] and fv['plan_sha256'] == fr['plan_sha256'],
         'final combined acceptance exact report/receipt/plan chain')
    must(ck['status'] == 'PASS' and fm['status'] == 'PASS-FINAL-SAVED68-MATHEMATICAL-GATE-CONDITIONAL-ON-INHERITED-PREMISES'
         and fr['status'] == 'PASS-INDEPENDENT-SAVED68-RESOURCE-CLOSURE-SCOPE-AND-TRANSCRIPT-AUDIT'
         and fv['status'] == 'PASS-SAVED68-SAVED-ENDPOINT-AND-RESOURCE-GATE', 'saved68 final dependency acceptance')
    must(not fr['open_findings'] and fr['production_roles_closed'] and fr['single_attempt_consumed'] and
         fr['original_READY_and_BEGIN_and_stdout_stderr_preserved'] and
         fv['scientific_acceptance_conditional_on_inherited_physical_and_analytic_premises'],
         'saved68 closed scope and conditional premises')
    return ck


def resolve_inputs(root, manifest_path):
    m = load(manifest_path)
    must(m['format']=='SHIFT372_INPUTS_V1' and m['scope']==SCOPE, 'shift input schema')
    must(Path(m['source_root']).resolve()==root.resolve(), 'bound input root')
    must(m['candidate']=={'h':'2*delta_star','delta0':'1/64','rank':68,'observations':372,
                          'C_sha256':C_SHA,'tau':'1/100'}, 'single fixed candidate')
    paths = {}
    for role, rec in m['inputs'].items():
        rel = Path(rec['path'])
        must(not rel.is_absolute() and '..' not in rel.parts, 'relative source path')
        p = root/rel
        must(p.resolve().is_relative_to(root.resolve()) and not p.is_symlink(), 'source path escape')
        must(p.is_file() and p.stat().st_size==rec['size'] and sha(p)==rec['sha256'], 'source bytes '+role)
        paths[role] = p; _guard()
    old = load(paths['old_full_manifest'])
    must(all(m['inputs'].get(role)==rec for role,rec in old['inputs'].items()),
         'original59 full372 roles retained without replacement')
    must(sha(paths['frozen_C'])==C_SHA, 'frozen original68x372 C')
    return m, paths


def shift_scalars(paths, saved, certificate_path):
    """Independent exact derivation; no driver/helper imports or old normal gate."""
    cert = load(certificate_path)
    nr = load(paths['norm']); act = nr['action']; tr = nr['trial']
    tail = load(paths['sharp'])['exact']
    eta = Q(1,64)-rational(tail['new_prime_tail_upper'])-rational(tail['cover_epsilon_upper'])
    must(str(eta)==ETA_TEXT and rational(act['eta'])==eta, 'same coercivity eta')
    tau = rational(act['tau']); must(tau==Q(1,100), 'tau fixed')
    nu = rational(tr['nu68']); sigbar = rational(act['sigma_bar68'])
    must(len(act['old_B'])==64 and len(act['new_B'])==4, 'all physical action errors')
    errors = [rational(x) for x in act['old_B']+act['new_B']]
    must(all(x>=0 for x in errors), 'nonnegative column error bounds')
    sigma2 = sum(x*x for x in errors)
    must(sigma2>0 and sigma2==rational(act['sigma68_squared']) and sigbar>=0 and sigbar*sigbar>=sigma2,
         'deterministic error bounds from all68 columns')
    must(nu>0 and nu*nu>=rational(tr['L68']), 'trial norm majorant')
    for k,v in [('nu68',nu),('sigma68_squared',sigma2),('sigma_bar68',sigbar)]:
        must(rational(saved[k])==v, 'saved independent scalar binding '+k)
    old = load(paths['old_full_verdict']); oldcheck = load(paths['old_full_checker'])
    must(old['charged_checker_report_sha256']==sha(paths['old_full_checker']) and
         old['input_manifest_sha256']==oldcheck['input_manifest_sha256']==sha(paths['old_full_manifest']),
         'last actual full certificate chain')
    must(oldcheck['output_hashes']['C.json']==C_SHA, 'old full coefficients')
    mu0 = rational(old['exact_values']['mu372'])
    star = rational(oldcheck['eta_times_mu372'])
    must(mu0==rational(oldcheck['exact_check_values']['mu372']) and
         star==eta*mu0==rational(old['exact_values']['eta_times_mu372']), 'actual old product')
    must(rational(old['exact_values']['form_lower_edge'])==star-Q(1,64), 'old bound, not filename')
    must(0<mu0<Q(1,100), 'old response margin range')
    h = star+star; eta1 = eta-h; delta1 = Q(1,64)-h
    must(0<h<eta and delta1>0, 'fixed candidate beyond old scalar boundary')
    # Expanded independently: q=2p-1 and gamma=beta+h*nu^2+alpha*(h*nu)^2.
    alpha = Q(101,100)/eta1
    p = (eta1+Q(101,100)*h)/eta1
    q = 2*p-1
    beta = nu*sigbar+101*sigma2/eta1
    gamma = beta+h*nu*nu+alpha*(h*nu)*(h*nu)
    must(h+alpha*h*h>0, 'norm majorant has positive coefficient')
    vals = dict(eta=eta,tau=tau,nu68=nu,sigma2=sigma2,sigma_bar=sigbar,mu0=mu0,
                delta_star=star,h=h,eta1=eta1,delta1=delta1,alpha=alpha,beta=beta,p=p,q=q,gamma=gamma)
    must(set(cert['values'])==set(vals), 'exact shifted scalar keys')
    for k,v in vals.items(): must(rational(cert['values'][k])==v, 'independent shifted scalar '+k)
    balls = {k:quantize_scalar(vals[k]) for k in ('alpha','p','q','gamma')}
    must(set(cert['scalar_balls160'])==set(balls), 'scalar interval keys')
    for k,v in balls.items():
        must(tuple(map(integer,cert['scalar_balls160'][k]))==v, 'outward scalar160 '+k)
    must(cert['scope']==SCOPE and cert['C_sha256']==C_SHA and
         cert['old_verdict_sha256']==sha(paths['old_full_verdict']) and
         cert['physical_errors_unchanged'] is True and cert['trial_gram_majorant']=='P<=nu68^2 I',
         'shift scalar premise and C bindings')
    must(cert['model_id']=='SHIFT_AFFINE_NORM_MAJORANT_V1' and
         cert['model']=='a*M-B^*C-C^*B+C^*Sbar*C; B=a*K-p*D; Sbar=a*N-q*F+gamma*I',
         'dimensionally explicit shifted model')
    return vals, balls


def check_shifted_model(balls, Nb, Fb, Kb, Db, Sb, Bb):
    """Use signed endpoints, especially -(positive scalar)*F and *D."""
    ac,ar = balls['alpha']; gc,gr = balls['gamma']
    for width, X, Y, coefficient, output, diagonal in [
        (RANK,Nb,Fb,balls['q'],Sb,True),(N,Kb,Db,balls['p'],Bb,False)]:
        xc,xr = X; yc,yr = Y; oc,orr = output; mc,mr = coefficient
        for i in range(RANK):
            _guard()
            for j in range(width):
                az,ae = scalar_product_ball(ac,ar,xc[i][j],xr[i][j])
                yz,ye = scalar_product_ball(mc,mr,yc[i][j],yr[i][j])
                lower = bound(az-ae-(yz+ye))
                upper = bound(az+ae-(yz-ye))
                if diagonal and i==j:
                    lower = bound(lower+((gc-gr)<<P))
                    upper = bound(upper+((gc+gr)<<P))
                expected = quantize_endpoints(lower,upper,1<<(2*P),P)
                must((oc[i][j],orr[i][j])==expected, 'shifted signed endpoints Sbar/B')


def run(source_root, manifest_path, output_path, guard):
    global _guard
    _guard = guard; sys.set_int_max_str_digits(100000); guard()
    must(os.environ.get('SHIFT_INPUT_SHA256')==sha(manifest_path) and
         os.environ.get('SHIFT_LAUNCH_ID') and os.environ.get('SHIFT_EPOCH_NS'), 'timed checker admission')
    root,out = Path(source_root),Path(output_path)
    manifest,paths = resolve_inputs(root,Path(manifest_path))
    saved = source_chain(manifest,paths)
    expected={'SINGLE_USE.json','SHIFT_SCALARS.json','C.json','D160.json','K160.json',
              'N160.json','F160.json','SBAR160.json','B160.json','A160.json','U_MODEL.json',
              'UCERT.json','FACTOR.json','INPUT_VERIFICATION.json','OUTPUT_MANIFEST.json','DRIVER_STATUS.json'}
    must(all(p.is_file() and not p.is_symlink() for p in out.iterdir()), 'only regular output files')
    captured={p.name:sha(p) for p in out.iterdir()}
    must(set(captured)==expected,'exact fixed output set, no solve products')
    status=load(out/'DRIVER_STATUS.json'); om=load(out/'OUTPUT_MANIFEST.json')
    counts={'coefficient_solves':0,'consumer_372':1,'full372_factorizations':1,'finite_triangular_inverses':1,
            'source_evaluations':0,'H_actions':0,'DFT_calls':0,'physical_quadrature':0,
            'precision_retries':0,'alternate_candidates':0}
    must(status['status']=='PROVISIONAL-CHECKER-AND-RESOURCE-GATES-PENDING' and
         status['stage']=='complete' and status['scope']==SCOPE and status['counts']==counts,
         'driver scope and operation counts')
    must(status['input_manifest_sha256']==om['input_manifest_sha256']==sha(manifest_path) and
         status['output_manifest_sha256']==sha(out/'OUTPUT_MANIFEST.json') and
         om['format']=='SHIFT372_OUTPUTS_V1' and om['scope']==SCOPE,'driver manifest bindings')
    must(set(om['outputs'])==expected-{'OUTPUT_MANIFEST.json','DRIVER_STATUS.json'},'output manifest completeness')
    for name,rec in om['outputs'].items():
        must(rec['sha256']==captured[name] and rec['size']==(out/name).stat().st_size,'output bytes '+name)
    iv=load(out/'INPUT_VERIFICATION.json'); single=load(out/'SINGLE_USE.json')
    must(iv['inputs']==manifest['inputs'] and iv['scope']==SCOPE and
         iv['input_manifest_sha256']==sha(manifest_path) and iv['byte_stability_before_after'] is True,'driver input check')
    must(single=={'scope':SCOPE,'launch_id':os.environ['SHIFT_LAUNCH_ID'],
         'epoch_ns':os.environ['SHIFT_EPOCH_NS'],'plan_sha256':os.environ['SHIFT_PLAN_SHA256'],
         'input_manifest_sha256':sha(manifest_path),'automatic_retry':False},'single exact launch identity')
    vals,balls=shift_scalars(paths,saved,out/'SHIFT_SCALARS.json')
    S=interval(out/'SBAR160.json',(RANK,RANK),P,True)
    B=interval(out/'B160.json',(RANK,N),P,False)
    Db=check_input_requant(paths['D68'],out/'D160.json',(RANK,N),False)
    Kb=check_input_requant(paths['K68'],out/'K160.json',(RANK,N),False)
    Nb=check_input_requant(paths['N68'],out/'N160.json',(RANK,RANK),True)
    Fb=check_input_requant(paths['E68'],out/'F160.json',(RANK,RANK),True)
    check_shifted_model(balls,Nb,Fb,Kb,Db,S,B)
    del Db,Kb,Nb,Fb; gc.collect()
    must(sha(out/'C.json')==sha(paths['frozen_C'])==C_SHA and
         (out/'C.json').read_bytes()==paths['frozen_C'].read_bytes(),'original C unchanged bytes')
    C=exact(out/'C.json',(RANK,N),CBITS)
    A=check_input_requant(paths['A'],out/'A160.json',(N,N),True,True)
    U=interval(out/'U_MODEL.json',(N,N),UBITS,True)
    uc=load(out/'UCERT.json')
    must(uc['C_sha256']==C_SHA and uc['U_MODEL_sha256']==captured['U_MODEL.json'] and
         uc['SHIFT_SCALARS_sha256']==captured['SHIFT_SCALARS.json'],'shifted target binding')
    rows=[bound(integer(x)) for x in uc['row_radius_numerators']]; del uc
    Ucert=exact(out/'UCERT.json',(N,N),UBITS); must(same_symmetric(Ucert),'target symmetry')
    coverage=consumer_verify(A,balls['alpha'],S,B,C,U,Ucert,rows)
    del A,S,B,C,U,rows; gc.collect()
    fac=load(out/'FACTOR.json')
    must(fac['matrix_sha256']==captured['UCERT.json'] and fac['C_sha256']==C_SHA and
         fac['SHIFT_SCALARS_sha256']==captured['SHIFT_SCALARS.json'] and fac['scope']==SCOPE and
         rational(fac['delta1'])==vals['delta1'] and rational(fac['h'])==vals['h'], 'fresh same-shift factor')
    witness=factor_verify(fac,Ucert); del fac,Ucert; gc.collect()
    mu1=rational(witness['mu372']); old_edge=-Q(1,64)+vals['delta_star']
    new_edge=-vals['delta1']+mu1*vals['eta1']
    improvement=new_edge-old_edge
    must(improvement==vals['delta_star']+mu1*vals['eta1']>0,'genuine strict improvement')
    for name,h in captured.items(): must(sha(out/name)==h,'output remained unchanged '+name)
    for role,p in paths.items(): must(sha(p)==manifest['inputs'][role]['sha256'],'input remained unchanged '+role)
    must(sha(manifest_path)==os.environ['SHIFT_INPUT_SHA256'],'input manifest unchanged')
    report={'status':'PASS-MATH-CONDITIONAL-RESOURCE-GATE-PENDING','scope':SCOPE,
            'checker_sha256':sha(__file__),'input_manifest_sha256':sha(manifest_path),
            'output_hashes':captured,'coverage':coverage,'exact_check_values':witness,
            'delta1':str(vals['delta1']),'eta1':str(vals['eta1']),'h':str(vals['h']),
            'previous_lower_edge':str(old_edge),'new_lower_edge':str(new_edge),
            'strict_improvement':str(improvement),'producer_imports':0,'native_calls':0,
            'native_imports_by_checker':0,'factorizations_by_checker':0,'solves_by_checker':0,
            'physical_inclusions':'A1-A4/N1-N4 inherited, not regenerated',
            'same_worker_native_runtime_remains_mapped':True,'RH_PROOF':'NOT-OBTAINED'}
    guard(); durable(out/'INDEPENDENT_CHECK.json',report); guard(); return report

