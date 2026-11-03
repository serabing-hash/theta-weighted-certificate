"""Portable invocation of the original conservative a2048 gate construction.

Same exact formula as certify_conservative_gate.py. The unchanged
exact_congruence.py only proposes a floating witness; sign uses exact integers.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time


def main(args):
    started = time.time()
    sys.path.insert(0, str(Path(args.source_dir).resolve()))
    from target import A, NU
    from verify_final_gate import load_matrix
    out = Path(args.output)
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('Refusing to overwrite nonempty output directory')
    frozen = Path(args.candidate)
    digest = hashlib.sha256((frozen/'candidate.json').read_bytes()).hexdigest()
    if digest != 'a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d':
        raise ValueError('Unexpected frozen candidate identity')
    source = json.loads((frozen/'verified_components.json').read_text())
    assert source['status'] == 'CERT' and source['candidate_sha256'] == digest
    paths = [Path(args.T),Path(args.G),Path(args.K)]
    (_,T),(_,G),(_,K) = [load_matrix(p,digest) for p in paths]
    f = F(source['coordinates']['F_trial_scalar_lower'])
    nu0 = 4*A/5
    penalty = 4/nu0+5*A/nu0**2
    assert penalty == 26240 and NU > nu0 and f > 0
    M = [[4*T[i][j]-5*A*G[i][j]/4+(A*f/4 if i==j else 0)-penalty*K[i][j] for j in range(256)] for i in range(256)]
    den = math.lcm(*(v.denominator for row in M for v in row))
    packet = {'candidate_sha256':digest,'a':str(A),'penalty':str(penalty),'nu_used':str(nu0),'common_denominator':str(den),'matrix_numerators':[[str(v.numerator*(den//v.denominator)) for v in row] for row in M]}
    out.mkdir(parents=True,exist_ok=True)
    path = out/'sufficient_gate_exact.json'
    path.write_text(json.dumps(packet,indent=2)+'\n')
    checker = Path(args.exact_checker)
    spec = importlib.util.spec_from_file_location('exact_sign_checker',checker)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.A = out
    gap = F(1,2000)
    module.run(path,gap)
    cert = json.loads((out/'independent_congruence_certificate.json').read_text())
    assert cert['status'] == 'EXACT_INTEGER_POSITIVE_DEFINITE'
    step = A*nu0/(A+4*nu0)
    b = A-step
    report = {'status':'CERT_EXACT_INTEGER_SIGN','scope':'same frozen sufficient gate with conservative26240 penalty; shifted by1/2000 before the exact congruence','a':str(A),'B':'log(8)/2','k':256,'nu_used':str(nu0),'penalty':str(penalty),'gap':str(gap),'step':str(step),'b':str(b),'conditional_coefficient':str(F(1,2)-b),'coefficient_float_DIAG':float(F(1,2)-b),'candidate_sha256':digest,'sufficient_matrix_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'inputs_sha256':{name:hashlib.sha256(p.read_bytes()).hexdigest() for name,p in zip(('T','G','K'),paths)},'elapsed_seconds':time.time()-started,'unseen_parent_epsilon_identity_required':False,'half':'NOT_PROVED','RH':'NOT_PROVED'}
    (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['source-dir','exact-checker','candidate','T','G','K','output']:
        parser.add_argument('--'+name,required=True)
    main(parser.parse_args())
