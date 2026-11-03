"""Freeze a DIAG candidate as exact dyadics; verify its actual source coordinates.

This verifies neither its primal form matrices nor its residual head integral.
The original input NPZ is DIAG. Each finite stored float is here DECLARED to be
the exact dyadic value defining a new spline/witness, not an enclosure of a solve.
"""
import argparse
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy import linalg
from interval_bounds import IV,pi_interval,spatial_residual_tail,gamma_label_bounds


def exact(x):return IV(Decimal.from_float(float(x)))
def rational_pair(x):return list(float(x).as_integer_ratio())
def abs_upper(x):return max(x.lo.copy_abs(),x.hi.copy_abs())


def cosine_table(nb):
    pi=pi_interval();table=[]
    for index in range(2*nb):
        r=index if index<=nb else 2*nb-index
        sign=1
        if 2*r>nb:r=nb-r;sign=-1
        z=pi*IV.rational(r,nb)
        z2=z*z
        val=IV(0)
        # Degree 78 Taylor polynomial; absolute remainder <= |z|^80/80!.
        for j in reversed(range(40)):
            val=val*z2+IV.rational((-1)**j,math.factorial(2*j))
        tail=z**80/IV(math.factorial(80))
        val+=IV(tail.hi.copy_negate(),tail.hi)
        table.append(sign*val)
    return table


def aligned_moments_for_fixture(nodes,h,nb,k=64):
    n=len(nodes);table=cosine_table(nb);B=h*nb
    hh=IV.rational(h.numerator,h.denominator)
    hquarter=hh/4
    sinh=(hquarter.exp()-(-hquarter).exp())/2
    base=16*sinh**2/hh
    means=[]
    for j in range(n):
        means.append(base*(hh*j/2).cosh()*(1 if j==0 else 2))
    m=[sum((means[j]*nodes[j][col] for j in range(n)),IV(0)) for col in range(k)]
    raw=[]
    for mode in range(k):
        norm=(IV.rational(2*B.numerator,B.denominator) if mode==0 else IV.rational(B.numerator,B.denominator)).sqrt().reciprocal()
        if mode==0:sinc2=IV(1)
        else:
            kh=pi_interval()*IV.rational(mode,nb)
            sinc2=2*(1-table[mode])/kh**2
        factor=hh*norm*sinc2
        row=[]
        for col in range(k):
            value=nodes[0][col]+((-1)**mode)*nodes[nb][col]
            value+=sum((2*nodes[j][col]*table[(mode*j)%(2*nb)] for j in range(1,nb)),IV(0))
            rawval=factor*value
            # J=raw-2m*int_I kappa*e. |int_I kappa e|<=norm/2,
            # since mu(R)=1 and c>=1. Bound the exact centering correction.
            rad=IV(abs_upper(m[col]))*norm
            row.append(rawval+IV(rad.hi.copy_negate(),rad.hi))
        raw.append(row)
        if mode%16==0:print(f'coordinate interval rows: {mode+1}/{k}',flush=True)
    return m,raw


def actual_moments(nodes,h,nb=None,k=None,return_geometry=False):
    if nb is not None:return aligned_moments_for_fixture(nodes,h,nb,k=len(nodes[0]) if k is None else k)
    from source_geometry import geometry,moment_coefficients,ball_to_intervals
    from ball_array import Ball,pairs_ball,iv_pair
    k=len(nodes[0]) if k is None else k;n=len(nodes)
    geom=geometry(h,k);B,q,cutoff,displacement,cb,sb,norms=geom
    N=pairs_ball([[iv_pair(v) for v in row] for row in nodes])
    hh=IV.rational(h.numerator,h.denominator);quarter=hh/4
    sinh=(quarter.exp()-(-quarter).exp())/2;base=16*sinh**2/hh
    mean=pairs_ball([iv_pair(base*(hh*j/2).cosh()*(1 if j==0 else 2)) for j in range(n)]).reshape(1,n)
    m=ball_to_intervals(mean@N)[0]
    raw=ball_to_intervals(moment_coefficients(n,h,k,geom)@N)
    J=[]
    for mode,row in enumerate(raw):
        out=[]
        for col,value in enumerate(row):
            rad=IV(abs_upper(m[col]))*norms[mode]
            out.append(value+IV(rad.hi.copy_negate(),rad.hi))
        J.append(out)
    return (m,J,geom) if return_geometry else (m,J)


def nonsingularity(J):
    k=len(J)
    mid=np.array([[float((Fraction(x.lo)+Fraction(x.hi))/2) for x in row] for row in J])
    inverse=linalg.inv(mid)
    from ball_array import Ball,pairs_ball,iv_pair,ua,usum,norm_upper
    JJ=pairs_ball([[iv_pair(x) for x in row] for row in J])
    residual=Ball(np.eye(k))-Ball(inverse)@JJ
    err=ua(np.abs(residual.mid),residual.rad)
    delta=Decimal.from_float(float(np.max(usum(err,axis=1))))
    yy=norm_upper(inverse)
    yfrobsq=exact(yy)**2
    if delta>=1:raise ArithmeticError('Moment matrix interval nonsingularity failed')
    # R=I-YJ, ||R||_infinity<=delta. For a Euclidean lower singular bound,
    # ||R||_2<=sqrt(k)*delta; do NOT silently identify the two matrix norms.
    euclidean_delta=IV(k).sqrt()*IV(delta)
    if euclidean_delta.hi>=1:raise ArithmeticError('Euclidean inverse bound too wide')
    sigma_lower=(1-euclidean_delta)/yfrobsq.sqrt()
    # F<=2I by the theta envelope, so J^T F^-1 J >= (sigma_lower^2/2)I.
    source_lower=sigma_lower**2/2
    return {'status':'CERT','scope':'nonsingularity of ACTUAL centered spline moment map J; same V',
            'neumann_residual_infinity_upper':str(delta),
            'neumann_residual_two_norm_upper':str(euclidean_delta.hi),
            'J_smallest_singular_value_lower':str(sigma_lower.lo),
            'F_trial_scalar_lower':str(source_lower.lo),
            'inverse_witness_dyadics':[[rational_pair(x) for x in row] for row in inverse]}


def main(args):
    started=time.time();source=Path(args.source);output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    data=np.load(source/'matrices.npz');meta=json.loads((source/'result.json').read_text())
    if meta['status']!='DIAG' or meta['parameters']['k']!=256 or meta['a']!='1/2048' or meta['B']!='log(8)/2':raise ValueError('Need exact new target256 DIAG input')
    n=meta['parameters']['cells'];length=Fraction(str(meta['parameters']['length']));h=length/n
    k=meta['parameters']['k']
    nodes_float=data['nodes'];alpha_float=data['alpha'];beta_float=data['beta']
    if not all(np.isfinite(x).all() for x in [nodes_float,alpha_float,beta_float]):raise ValueError('Nonfinite candidate')
    packet={'status':'EXACT_FROZEN_DEFINITION_NOT_A_CERTIFICATE','k':k,'n':n,'L':str(length),'h':str(h),'a':'1/2048','B':'log(8)/2',
            'trial':'f_j=C u_j, u_j compact even linear spline with these exact nodal dyadics',
            'source_coordinates':'v_prime_j=P_V f_j; source Gram is F_trial=J^T F^-1 J, NOT identity',
            'node_dyadics':[[rational_pair(x) for x in row] for row in nodes_float],
            'alpha_dyadics':[rational_pair(x) for x in alpha_float],
            'beta_dyadics':[[rational_pair(x) for x in row] for row in beta_float],
            'input_matrix_sha256':hashlib.sha256((source/'matrices.npz').read_bytes()).hexdigest()}
    (output/'candidate.json').write_text(json.dumps(packet,separators=(',',':'))+'\n')
    nodes=[[exact(x) for x in row] for row in nodes_float]
    # All candidate entries are exact frozen binary64 dyadics by construction.
    assert all(Fraction(*v)==Fraction(float(Fraction(*v))) for row in packet['node_dyadics'] for v in row)
    assert all(Fraction(*v)==Fraction(float(Fraction(*v))) for v in packet['alpha_dyadics'])
    assert all(Fraction(*v)==Fraction(float(Fraction(*v))) for row in packet['beta_dyadics'] for v in row)
    m,J,geom=actual_moments(nodes,h,k=k,return_geometry=True)
    B,q,cutoff,displacement,cb,sb,norms=geom
    from ball_array import iv_pair
    np.savez_compressed(output/'source_geometry.npz',cos_mid=cb.mid,cos_rad=cb.rad,sin_mid=sb.mid,sin_rad=sb.rad,norm_pairs=np.array([iv_pair(v) for v in norms]))
    geometry_record={'status':'CERT_GEOMETRY_ONLY','B_exact':'log(8)/2','B_interval':B.record(),'q':q,'h':str(h),'k':k,'B_model_cutoff':str(cutoff),'B_model_displacement_upper':str(displacement),'model_cutoff_bits':120,'coefficient_binary64_representability_checked':True,'geometry_npz_sha256':hashlib.sha256((output/'source_geometry.npz').read_bytes()).hexdigest()}
    (output/'geometry.json').write_text(json.dumps(geometry_record,indent=2)+'\n')
    coord=nonsingularity(J)
    Dsq=max(sum((x*x for x in row),IV(0)).hi for row in nodes)
    asq=sum((exact(x)**2 for x in alpha_float),IV(0))
    Dupper=IV(Dsq).sqrt().hi;aupper=asq.sqrt().hi
    R=Fraction(str(meta['parameters']['residual_radius']))
    tail=spatial_residual_tail(IV.rational(length.numerator,length.denominator),IV.rational(R.numerator,R.denominator),Dupper,aupper)
    dtrace=IV(0)
    for j in range(n):
        for col in range(k):
            nxt=nodes[j+1][col] if j+1<n else IV(0)
            dtrace+=(nxt-nodes[j][col])**2
    dtrace*=IV.rational(2*h.denominator,h.numerator)
    gamma_budgets={}
    for labels in [4096,65536,1048576]:
        b=gamma_label_bounds(labels)
        en=b['energy_derivative_gram_multiplier'];rn=b['row_derivative_norm_multiplier']
        energy=IV.rational(en.numerator,en.denominator)*dtrace
        squared=2*IV.rational(rn.numerator,rn.denominator)**2*dtrace
        gamma_budgets[str(labels)]={'primal_energy_tail_scalar_upper':str(energy.hi),
                                  'weighted_Gamma_row_tail_squared_scalar_upper':str(squared.hi),
                                  'usage':'alternative finite-label assembly only; combine head/tail cross terms; NOT consumed by DIAG full H'}
    Wcap=42*(-pi_interval()).exp()
    if Wcap.hi>=2:raise ArithmeticError('Could not certify sup W<2')
    report={'status':'CERT','scope':'frozen candidate coordinate rank, exact centering formula, scalar whole-row spatial/prime tail and optional Gamma-label tail budgets ONLY',
            'actual_global256_gate':'NOT_RUN','primal_form_enclosures':'NOT_RUN','residual_head_enclosure':'NOT_RUN',
            'candidate_sha256':hashlib.sha256((output/'candidate.json').read_bytes()).hexdigest(),
            'm_u_intervals':[v.record() for v in m],'m_u_absolute_upper':str(max(abs_upper(v) for v in m)),
            'coordinates':coord,'sup_W_analytic_upper':str(Wcap.hi),
            'D_upper':str(Dupper),'alpha_norm_upper':str(aupper),
            'full_spatial_and_unenumerated_prime_residual_tail':tail.record(),
            'derivative_gram_trace_upper':str(dtrace.hi),'optional_Gamma_label_budgets':gamma_budgets,
            'elapsed_seconds':time.time()-started,
            'analytic_inputs':['theta normalization and positive envelope','weak source equation B kappa=-kappa/2',
                               'full complementary coercivity from supplied proof','piecewise linear row-domain proof in contract'],
            'conditional_target_coefficient':'NOT_ACHIEVED','RH':'NOT_PROVED'}
    (output/'moments_intervals.json').write_text(json.dumps([[v.record() for v in row] for row in J],indent=2)+'\n')
    (output/'verified_components.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['m_u_intervals','coordinates']},indent=2),flush=True)
    print('CERT coordinate scope:',{k:v for k,v in coord.items() if k!='inverse_witness_dyadics'},flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    main(ap.parse_args())
