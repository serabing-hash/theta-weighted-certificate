"""Exact a=1/2048 sufficient matrix and directed shifted-LDL certificate."""
import argparse,hashlib,json,math,time
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.linalg import eigvalsh
from interval_bounds import IV,interval_ldl
from target import A,B_EXACT,EPSILON,NU,PENALTY,K as DIM

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def load_matrix(path,candidate):
    record=json.loads(path.read_text())
    assert record['status']=='CERT' and record['candidate_sha256']==candidate
    den=int(record['common_denominator'])
    matrix=[[Fraction(int(v),den) for v in row] for row in record['matrix_numerators']]
    assert len(matrix)==DIM and all(len(row)==DIM for row in matrix)
    assert all(matrix[i][j]==matrix[j][i] for i in range(DIM) for j in range(i))
    return record,matrix

def main(args):
    started=time.time();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    frozen=Path(args.candidate);identity=json.loads(Path('inputs/frozen_identity.json').read_text())
    candidate=digest(frozen/'candidate.json');assert candidate==identity['candidate_sha256']
    packet=json.loads((frozen/'candidate.json').read_text())
    assert (packet['a'],packet['B'],packet['k'],packet['n'],packet['h'])==('1/2048','log(8)/2',256,3072,'1/2560')
    source=json.loads((frozen/'verified_components.json').read_text())
    assert source['status']=='CERT' and source['candidate_sha256']==candidate and source['coordinates']['status']=='CERT'
    paths=[Path(args.T),Path(args.G),Path(args.K)]
    tm,T=load_matrix(paths[0],candidate);gm,G=load_matrix(paths[1],candidate);km,K=load_matrix(paths[2],candidate)
    assert tm['a']==str(A) and km['a']==str(A) and km['B_exact']==B_EXACT and km['k']==DIM and km['h']==packet['h']
    geometry=json.loads((frozen/'geometry.json').read_text())
    assert km['B_model_cutoff']==geometry['B_model_cutoff'] and km['boundary_cell']==geometry['q']
    assert Fraction(km['boundary_phase'])==Fraction(km['B_model_cutoff'])/Fraction(packet['h'])-km['boundary_cell']
    assert km['all_prime_powers_on_compact_interval']==[2,3,4,5,7,8,9,11,13,16,17,19,23]
    assert Fraction(km['outer_tail_once'])==Fraction(source['full_spatial_and_unenumerated_prime_residual_tail']['upper'])
    assert NU==A-EPSILON and 4*A/5<NU<A and PENALTY==4/NU+5*A/NU**2
    F=Fraction(source['coordinates']['F_trial_scalar_lower']);assert F>0
    M=[[4*T[i][j]-5*A*G[i][j]/4+(A*F/4 if i==j else 0)-PENALTY*K[i][j] for j in range(DIM)] for i in range(DIM)]
    gap=Fraction(args.gap);assert gap>=0
    shifted=[[v-(gap if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(M)]
    proof=interval_ldl([[IV.rational(v.numerator,v.denominator) for v in row] for row in shifted])
    den=math.lcm(*(v.denominator for row in M for v in row))
    exact={'candidate_sha256':candidate,'a':str(A),'penalty':str(PENALTY),
           'scope':'sufficient matrix in exact induced-source coordinates',
           'common_denominator':str(den),'matrix_numerators':[[str(v.numerator*(den//v.denominator)) for v in row] for row in M]}
    (out/'sufficient_gate_exact.json').write_text(json.dumps(exact,indent=2)+'\n')
    h=A*NU/(A+4*NU);b=A-h
    report={'status':'CERT' if proof['positive'] else 'FAIL',
            'scope':'internal a=1/2048 full weighted256 sufficient-gate certificate, conditional on analytic premises and independent review',
            'a':str(A),'B':B_EXACT,'k':DIM,'nu':str(NU),'epsilon256_new_radius':str(EPSILON),'residual_penalty':str(PENALTY),
            'complement_floor_used':'fresh a2048 epsilon, nu>4a/5','old_penalty_4968_used':False,
            'candidate_sha256':candidate,'F_lower_scalar':str(F),'gap':str(gap),'interval_LDL_of_M_minus_gap_I':proof,
            'minimum_eigenvalue_DIAG':float(eigvalsh(np.array([[float(v) for v in row] for row in M]))[0]),
            'inputs_sha256':{str(p):digest(p) for p in paths+[frozen/'candidate.json',frozen/'verified_components.json',frozen/'geometry.json']},
            'sufficient_matrix_sha256':digest(out/'sufficient_gate_exact.json'),
            'actual_gate':'CONDITIONAL_IMPLICATION_FROM_SUPPLIED_SCHUR_THEOREM' if proof['positive'] else 'UNRESOLVED',
            'conditional_h':str(h),'conditional_b':str(b),'conditional_coefficient':str(Fraction(1,2)-b),
            'independent_review':'PENDING','public_coefficient_claim':False,'half':'NOT_PROVED','RH':'NOT_PROVED',
            'automatic_next_parameter_step':False,'elapsed_seconds':time.time()-started}
    (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='interval_LDL_of_M_minus_gap_I'},indent=2))
    print('Positive shifted pivots:',len(proof['pivots']) if proof['positive'] else 'FAIL',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate',default='results/frozen256_n3072');p.add_argument('--T',default='results/T256_n3072/T_lower_exact.json')
    p.add_argument('--G',default='results/G256_n3072/G_upper_exact.json');p.add_argument('--K',default='results/K256_n3072/K_upper_exact.json')
    p.add_argument('--gap',default='1/2000');p.add_argument('--output',required=True);main(p.parse_args())
