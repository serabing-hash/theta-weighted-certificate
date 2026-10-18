"""Fixed68/fixed-C shifted full372 driver. No scientific work on import.

Run only by shift_entry after timed native admission. Physical inputs and all
errors are inherited; no coefficient solve, source producer or second action.
"""
import gc
import os
from pathlib import Path
import sys
from fractions import Fraction as Q
from shift_exact import (require, gate, scalar, parse_source, shifted_model,
                         interval_object, exact_object, sha, save, read, integer)
from shift_inputs import accepted

SCOPE = 'SHIFT372_H2_DELTA_STAR_FIXED_C_ONCE_V1'
ETA_TEXT = '1446776856241610348487954379752034183297365381007/92620636523388719034562694367509285563269120000000'
C_SHA = 'c459b5c283020808e6d52ac60e3749137c11cd9db21e98fa5178ff0698ade513'
COUNTS = {'coefficient_solves': 0, 'consumer_372': 0,
          'full372_factorizations': 0, 'finite_triangular_inverses': 0,
          'source_evaluations': 0, 'H_actions': 0, 'DFT_calls': 0,
          'physical_quadrature': 0, 'precision_retries': 0,
          'alternate_candidates': 0}


class Inputs:
    def __init__(self, root, manifest, guard):
        self.root = Path(root).resolve(); self.path = Path(manifest).resolve()
        self.guard = guard
        require(sha(self.path) == os.environ['SHIFT_INPUT_SHA256'], 'input manifest admission')
        self.m = read(self.path)
        require(self.m['format'] == 'SHIFT372_INPUTS_V1' and self.m['scope'] == SCOPE, 'input scope')
        require(self.m['source_root'] == str(self.root), 'source root')
        self.files = self.m['inputs']; self.verify()
        inherited = self.read('old_full_manifest')
        require(all(self.files.get(role) == rec for role,rec in inherited['inputs'].items()),
                'all original59 full372 bindings retained')

    def p(self, role):
        rel = Path(self.files[role]['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'relative input path')
        p = self.root / rel
        require(not p.is_symlink() and p.resolve().is_relative_to(self.root), 'input path escape')
        return p

    def h(self, role): return self.files[role]['sha256']

    def verify(self):
        for role, rec in self.files.items():
            self.guard(); p = self.p(role)
            require(p.is_file() and p.stat().st_size == rec['size'] and sha(p) == rec['sha256'],
                    'input bytes ' + role)

    def read(self, role):
        self.guard(); p = self.p(role)
        require(sha(p) == self.h(role), 'input changed ' + role)
        return read(p)


def scalars(inp, saved):
    norm = inp.read('norm'); a = norm['action']; t = norm['trial']
    eta, tau, nu = Q(a['eta']), Q(a['tau']), Q(t['nu68'])
    sigma2, sigbar = Q(a['sigma68_squared']), Q(a['sigma_bar68'])
    require(eta == Q(ETA_TEXT) and tau == Q(1, 100), 'eta/tau')
    require(nu > 0 and sigma2 > 0 and sigbar >= 0 and sigbar*sigbar >= sigma2,
            'norm/action upper signs')
    require(nu*nu >= Q(t['L68']), 'trial norm upper bound')
    require(len(a['old_B']) == 64 and len(a['new_B']) == 4, 'all68 action bounds')
    errors = [Q(x) for x in a['old_B'] + a['new_B']]
    require(all(x>=0 for x in errors) and sum(x*x for x in errors) == sigma2, 'all68 squared errors')
    for key, value in [('nu68',nu),('sigma68_squared',sigma2),('sigma_bar68',sigbar)]:
        require(Q(saved[key]) == value, 'saved scalar binding ' + key)
    old = inp.read('old_full_verdict'); check = inp.read('old_full_checker')
    require(old['charged_checker_report_sha256'] == inp.h('old_full_checker'), 'old full checker binding')
    require(old['input_manifest_sha256'] == inp.h('old_full_manifest'), 'old full input binding')
    require(check['input_manifest_sha256'] == inp.h('old_full_manifest'), 'checker old manifest')
    require(check['output_hashes']['C.json'] == inp.h('frozen_C') == C_SHA, 'original C identity')
    mu0 = Q(old['exact_values']['mu372'])
    star = Q(old['exact_values']['eta_times_mu372'])
    require(Q(check['exact_check_values']['mu372']) == mu0, 'old exact response margin')
    require(Q(check['eta_times_mu372']) == star == eta*mu0, 'old exact product')
    require(Q(old['exact_values']['form_lower_edge']) == -Q(1,64)+star, 'old true lower edge')
    require(0 < mu0 < Q(1,100), 'inherited margin range')
    h = 2*star; eta1 = eta-h; delta1 = Q(1,64)-h
    require(0 < h < eta and delta1 > 0, 'single shifted candidate admitted')
    alpha = (1+tau)/eta1
    beta = nu*sigbar+(1+1/tau)*sigma2/eta1
    p = 1+alpha*h; q = 1+2*alpha*h
    gamma = beta+(h+alpha*h*h)*nu*nu
    require(h+alpha*h*h > 0, 'positive coefficient for trial norm majorant')
    values = dict(eta=eta,tau=tau,nu68=nu,sigma2=sigma2,sigma_bar=sigbar,
                  mu0=mu0,delta_star=star,h=h,eta1=eta1,delta1=delta1,
                  alpha=alpha,beta=beta,p=p,q=q,gamma=gamma)
    balls = {k: scalar(values[k]) for k in ('alpha','p','q','gamma')}
    return values, balls


def run(source_root, manifest, output, guard):
    sys.set_int_max_str_digits(100000)
    require(os.environ.get('SHIFT_CHARGED_NATIVE_ADMISSION') == '1' and 'flint' in sys.modules,
            'timed native admission required')
    from flint import ctx
    require(ctx.prec == 160 and ctx.threads == 1, 'fixed native settings')
    from shift_native import consumer, factor
    guard(); out = Path(output); out.mkdir(exist_ok=False)
    outputs = {}; counts = dict(COUNTS); stage = 'inputs'

    def emit(name, obj):
        guard(); save(out/name, obj)
        outputs[name] = {'sha256':sha(out/name),'size':(out/name).stat().st_size}

    def imat(name, ball, bits, sym=False):
        emit(name, interval_object(*ball,bits,sym))

    try:
        inp = Inputs(source_root, manifest, guard); old_saved = accepted(inp)
        require(inp.m['candidate'] == {'h':'2*delta_star','delta0':'1/64','rank':68,
                 'observations':372,'C_sha256':C_SHA,'tau':'1/100'}, 'frozen candidate metadata')
        emit('SINGLE_USE.json', {'scope':SCOPE,'launch_id':os.environ['SHIFT_LAUNCH_ID'],
             'epoch_ns':os.environ['SHIFT_EPOCH_NS'],'plan_sha256':os.environ['SHIFT_PLAN_SHA256'],
             'input_manifest_sha256':sha(manifest),'automatic_retry':False})
        stage = 'fixed_shift_scalars'; values, balls = scalars(inp, old_saved)
        emit('SHIFT_SCALARS.json', {'scope':SCOPE,'values':{k:str(v) for k,v in values.items()},
             'scalar_balls160':{k:list(map(str,v)) for k,v in balls.items()},
             'model':'a*M-B^*C-C^*B+C^*Sbar*C; B=a*K-p*D; Sbar=a*N-q*F+gamma*I',
             'model_id':'SHIFT_AFFINE_NORM_MAJORANT_V1',
             'C_sha256':C_SHA,'old_verdict_sha256':inp.h('old_full_verdict'),
             'physical_errors_unchanged':True,'trial_gram_majorant':'P<=nu68^2 I'})
        # Original dyadic coefficients copied byte-for-byte, never reserialized.
        raw = inp.p('frozen_C').read_bytes()
        with (out/'C.json').open('xb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        require((out/'C.json').read_bytes() == raw and sha(out/'C.json') == C_SHA, 'C exact bytes')
        outputs['C.json'] = {'sha256':C_SHA,'size':len(raw)}
        cobj = inp.read('frozen_C')
        require(cobj['format']=='DYADIC_EXACT_MATRIX_V1' and cobj['shape']==[68,372]
                and cobj['bits']==80, 'C format')
        require(len(cobj['numerators'])==68 and all(len(row)==372 for row in cobj['numerators']), 'C rows')
        C = [[gate(integer(v)) for v in row] for row in cobj['numerators']]
        del raw,cobj
        stage = 'shifted_matrices'; arrays = {}
        for role,name,shape,sym in [('D68','D160.json',(68,372),False),
              ('K68','K160.json',(68,372),False),('N68','N160.json',(68,68),True),
              ('E68','F160.json',(68,68),True)]:
            arrays[role] = parse_source(inp.read(role),shape,160,symmetric=sym)
            imat(name,arrays[role],160,sym)
        S,B = shifted_model(balls['alpha'],balls['p'],balls['q'],balls['gamma'],
                    arrays['N68'],arrays['E68'],arrays['K68'],arrays['D68'],guard)
        del arrays
        imat('SBAR160.json',S,160,True); imat('B160.json',B,160)
        A = parse_source(inp.read('A'),(372,372),160,legacy_A=True,symmetric=True)
        imat('A160.json',A,160,True)
        stage = 'one_full_consumer'; counts['consumer_372'] = 1
        Uc,Ur,Ucert,rr = consumer(balls['alpha'],A,S,B,C,guard)
        del A,S,B,C
        imat('U_MODEL.json',(Uc,Ur),100,True); del Uc,Ur
        obj = exact_object(Ucert,100)
        obj.update(row_radius_numerators=list(map(str,rr)),C_sha256=C_SHA,
                   U_MODEL_sha256=outputs['U_MODEL.json']['sha256'],
                   SHIFT_SCALARS_sha256=outputs['SHIFT_SCALARS.json']['sha256'])
        emit('UCERT.json',obj); del obj,rr; gc.collect()
        reh = [[gate(integer(v)) for v in row] for row in read(out/'UCERT.json')['numerators']]
        require(reh == Ucert, 'fresh exact target rehydration'); del Ucert
        stage = 'one_fresh_full_factor'; counts['full372_factorizations'] = 1
        def on_inverse(): counts['finite_triangular_inverses'] = 1
        fac = factor(reh,guard,on_inverse); del reh
        fac.update(matrix_sha256=outputs['UCERT.json']['sha256'],C_sha256=C_SHA,
                   SHIFT_SCALARS_sha256=outputs['SHIFT_SCALARS.json']['sha256'],
                   scope=SCOPE,delta1=str(values['delta1']),h=str(values['h']))
        emit('FACTOR.json',fac); del fac; gc.collect()
        stage = 'input_recheck'; inp.verify()
        emit('INPUT_VERIFICATION.json', {'inputs':inp.files,'input_manifest_sha256':sha(manifest),
             'byte_stability_before_after':True,'scope':SCOPE})
        emit('OUTPUT_MANIFEST.json', {'format':'SHIFT372_OUTPUTS_V1','scope':SCOPE,
             'input_manifest_sha256':sha(manifest),'outputs':dict(outputs)})
        status={'status':'PROVISIONAL-CHECKER-AND-RESOURCE-GATES-PENDING','scope':SCOPE,
                'counts':counts,'stage':'complete','input_manifest_sha256':sha(manifest),
                'output_manifest_sha256':outputs['OUTPUT_MANIFEST.json']['sha256']}
        emit('DRIVER_STATUS.json',status); guard(); return status
    except Exception as exc:
        failure={'status':'HOLD','stage':stage,'scope':SCOPE,'counts':counts,
                 'first_unmet_obligation':str(exc),'exception_type':type(exc).__name__,
                 'automatic_retry':False,'completed_outputs':outputs}
        try: save(out/'DRIVER_FAILURE.json',failure)
        except Exception: pass
        raise
