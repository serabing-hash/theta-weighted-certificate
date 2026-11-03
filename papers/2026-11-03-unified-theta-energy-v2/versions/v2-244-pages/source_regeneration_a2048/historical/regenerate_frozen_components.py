"""Regenerate source enclosures from the exact frozen a2048 candidate.

This adapter replaces only the omitted diagnostic NPZ import. It preserves the
candidate bytes and invokes the unchanged producer primitives. This is a
same-implementation/library replay, not independent validation or an RH proof.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

EXPECTED_SHA256 = 'a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d'


def environment_record():
    import platform
    import numpy
    import scipy
    import mpmath
    actual = {'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__}
    expected = {'python':'3.12.14','numpy':'2.3.5','scipy':'1.17.0','mpmath':'1.3.0'}
    return {'actual_versions':actual,'original_versions':expected,'same_libraries':actual==expected}


def main(args):
    if not __debug__:
        raise RuntimeError('Do not use python -O/-OO: producer validation requires assertions')
    started = time.time()
    environment = environment_record()
    source = Path(args.source_dir).resolve()
    from producer_guard import verify_source
    verify_source(source)
    sys.path.insert(0, str(source))
    import numpy as np
    from freeze_candidate import exact, actual_moments, nonsingularity, abs_upper
    from interval_bounds import IV, pi_interval, spatial_residual_tail, gamma_label_bounds
    from ball_array import iv_pair

    candidate_bytes = Path(args.candidate).read_bytes()
    digest = hashlib.sha256(candidate_bytes).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError('Candidate identity differs from authenticated a2048 input')
    packet = json.loads(candidate_bytes)
    k, n = packet['k'], packet['n']
    length, h = Fraction(packet['L']), Fraction(packet['h'])
    if (k, n, length, h, packet['a'], packet['B']) != (256, 3072, Fraction(6, 5), Fraction(1, 2560), '1/2048', 'log(8)/2'):
        raise ValueError('Unexpected scientific identity')
    if length != n*h:
        raise ValueError('Invalid mesh identity')
    def checked_float(pair):
        value = Fraction(*pair)
        result = float(value)
        if Fraction(result) != value:
            raise ValueError('Candidate coefficient is not exactly binary64 representable')
        return result
    nodes_float = np.array([[checked_float(v) for v in row] for row in packet['node_dyadics']])
    alpha_float = np.array([checked_float(v) for v in packet['alpha_dyadics']])
    beta_float = np.array([[checked_float(v) for v in row] for row in packet['beta_dyadics']])
    if nodes_float.shape != (n, k) or alpha_float.shape != (k,) or beta_float.shape != (k, k):
        raise ValueError('Unexpected coefficient shape')
    if not all(np.isfinite(x).all() for x in (nodes_float, alpha_float, beta_float)):
        raise ValueError('Nonfinite coefficient')
    output = Path(args.output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('Refusing to overwrite nonempty output directory')
    output.mkdir(parents=True, exist_ok=True)
    (output/'candidate.json').write_bytes(candidate_bytes)
    nodes = [[exact(x) for x in row] for row in nodes_float]
    m, J, geom = actual_moments(nodes, h, k=k, return_geometry=True)
    B, q, cutoff, displacement, cb, sb, norms = geom
    np.savez_compressed(output/'source_geometry.npz', cos_mid=cb.mid, cos_rad=cb.rad, sin_mid=sb.mid, sin_rad=sb.rad, norm_pairs=np.array([iv_pair(v) for v in norms]))
    geometry_record = {'status':'CERT_GEOMETRY_ONLY','B_exact':'log(8)/2','B_interval':B.record(),'q':q,'h':str(h),'k':k,'B_model_cutoff':str(cutoff),'B_model_displacement_upper':str(displacement),'model_cutoff_bits':120,'coefficient_binary64_representability_checked':True,'geometry_npz_sha256':hashlib.sha256((output/'source_geometry.npz').read_bytes()).hexdigest()}
    (output/'geometry.json').write_text(json.dumps(geometry_record,indent=2)+'\n')
    coord = nonsingularity(J)
    Dsq = max(sum((x*x for x in row),IV(0)).hi for row in nodes)
    asq = sum((exact(x)**2 for x in alpha_float),IV(0))
    Dupper = IV(Dsq).sqrt().hi
    aupper = asq.sqrt().hi
    # Original DIAG metadata fixes residual_radius=2.0; do not infer it from a result.
    R = Fraction(2)
    tail = spatial_residual_tail(IV.rational(length.numerator,length.denominator),IV.rational(R.numerator,R.denominator),Dupper,aupper)
    dtrace = IV(0)
    for j in range(n):
        for col in range(k):
            nxt = nodes[j+1][col] if j+1<n else IV(0)
            dtrace += (nxt-nodes[j][col])**2
    dtrace *= IV.rational(2*h.denominator,h.numerator)
    gamma_budgets = {}
    for labels in [4096,65536,1048576]:
        b = gamma_label_bounds(labels)
        en, rn = b['energy_derivative_gram_multiplier'], b['row_derivative_norm_multiplier']
        energy = IV.rational(en.numerator,en.denominator)*dtrace
        squared = 2*IV.rational(rn.numerator,rn.denominator)**2*dtrace
        gamma_budgets[str(labels)] = {'primal_energy_tail_scalar_upper':str(energy.hi),'weighted_Gamma_row_tail_squared_scalar_upper':str(squared.hi),'usage':'alternative finite-label assembly only; combine head/tail cross terms; NOT consumed by DIAG full H'}
    Wcap = 42*(-pi_interval()).exp()
    if Wcap.hi >= 2:
        raise ArithmeticError('Could not certify sup W<2')
    report = {'status':'CERT','scope':'frozen candidate coordinate rank, exact centering formula, scalar whole-row spatial/prime tail and optional Gamma-label tail budgets ONLY','actual_global256_gate':'NOT_RUN','primal_form_enclosures':'NOT_RUN','residual_head_enclosure':'NOT_RUN','candidate_sha256':digest,'m_u_intervals':[v.record() for v in m],'m_u_absolute_upper':str(max(abs_upper(v) for v in m)),'coordinates':coord,'sup_W_analytic_upper':str(Wcap.hi),'D_upper':str(Dupper),'alpha_norm_upper':str(aupper),'full_spatial_and_unenumerated_prime_residual_tail':tail.record(),'derivative_gram_trace_upper':str(dtrace.hi),'optional_Gamma_label_budgets':gamma_budgets,'elapsed_seconds':time.time()-started,'analytic_inputs':['theta normalization and positive envelope','weak source equation B kappa=-kappa/2','full complementary coercivity from supplied proof','piecewise linear row-domain proof in contract'],'conditional_target_coefficient':'NOT_ACHIEVED','RH':'NOT_PROVED'}
    (output/'moments_intervals.json').write_text(json.dumps([[v.record() for v in row] for row in J],indent=2)+'\n')
    (output/'verified_components.json').write_text(json.dumps(report,indent=2)+'\n')
    identity = {'status':'REGENERATED','candidate_sha256':digest,'candidate_bytes_unchanged':True,'residual_radius':'2','residual_radius_provenance':'original DIAG parameters.residual_radius=2.0','same_implementation':True,'same_libraries':environment['same_libraries'],'environment':environment,'independent_implementation':False,'copied_verified_components':False,'source_module_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.glob('*.py'))},'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (output/'regeneration_identity.json').write_text(json.dumps(identity,indent=2)+'\n')
    print(json.dumps({'status':'REGENERATED','candidate_sha256':digest,'elapsed_seconds':report['elapsed_seconds'],'F_trial_scalar_lower':coord['F_trial_scalar_lower'],'RH':'NOT_PROVED'},indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',required=True)
    parser.add_argument('--candidate',required=True,help='Authenticated decompressed candidate.json file')
    parser.add_argument('--output',required=True,help='New or empty directory only')
    main(parser.parse_args())
