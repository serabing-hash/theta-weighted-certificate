"""Validated analytic-plus-log model of the fixed optimized residual.

This constructs a model and its weighted L2 row-error budget. It does NOT yet
integrate the model Gram; that is a separate, mandatory verification stage.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
import interval_bounds as ib
from interval_bounds import IV
from freeze_candidate import cosine_table
from validated_phi import tlog
from ntt_gamma_rows import exact_jumps
from ball_array import Ball,iv_pair,fraction_pair,pairs_ball,up,ua,um,usum,norm_upper
import weighted64 as w
from target import A,radius_interval


def cos_small(angle):
    z=IV(angle);z2=z*z;v=IV(0)
    for j in reversed(range(32)):v=v*z2+IV.rational((-1)**j,math.factorial(2*j))
    tail=z**64/IV(math.factorial(64))
    return v+IV(tail.hi.copy_negate(),tail.hi)


def sin_small(angle):
    z=IV(angle);z2=z*z;v=IV(0)
    for j in reversed(range(32)):v=v*z2+IV.rational((-1)**j,math.factorial(2*j+1))
    v*=z;tail=absolute(z)**65/IV(math.factorial(65))
    return v+IV(tail.hi.copy_negate(),tail.hi)


def absolute(x):
    if x.lo>=0:return x
    if x.hi<=0:return -x
    return IV(0,max(x.lo.copy_abs(),x.hi.copy_abs()))


def cgamma_interval():
    N=16384
    harmonic=sum((IV.rational(1,j) for j in range(1,N+1)),IV(0))
    b=harmonic-IV(N).log()-IV.rational(1,2*N)
    # b_N increases to Euler gamma. Its increments are the trapezoid errors
    # for integral_k^(k+1) 1/x, <=1/(6k^3); sum <=1/(8N^2) for N>=4.
    gamma=b+IV(0,IV.rational(1,8*N*N).hi)
    return gamma+ib.pi_interval()/2+3*IV(2).log()+ib.pi_interval().log()


def gram_trace(record):
    den=int(record['common_denominator'])
    return sum(Fraction(int(record['matrix_numerators'][i][i]),den) for i in range(len(record['matrix_numerators'])))


def float_iv(x):return IV.rational(*float(x).as_integer_ratio())


def main(args):
    start=time.time();folder=Path(args.candidate);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    p=json.loads((folder/'candidate.json').read_text());digest=hashlib.sha256((folder/'candidate.json').read_bytes()).hexdigest()
    assert p['a']==str(A)
    gr=json.loads((Path(args.gamma)/'result.json').read_text());assert gr['candidate_sha256']==digest
    assert hashlib.sha256((Path(args.gamma)/'gamma_nodes.npz').read_bytes()).hexdigest()==gr['raw_nodes_sha256']
    gd=np.load(Path(args.gamma)/'gamma_nodes.npz');degree=gr['degree'];cells=gr['cells'];n=p['n'];k=p['k'];h=Fraction(p['h']);hh=IV.rational(h.numerator,h.denominator)
    ib.pi_interval=lru_cache(maxsize=1)(ib.pi_interval)
    assert (2*hh).exp().hi<IV.rational(101,100).lo
    assert ((-2*hh).exp()*cos_small(2*hh)).lo>IV.rational(99,100).hi
    assert (1+hh.exp()).hi<IV.rational(201,100).lo
    first=IV.rational(16,5)*16*(-IV.rational(177,20)).exp()
    ratio=IV.rational(81,16)*(-IV.rational(297,20)).exp()
    assert (first/(1-ratio)).hi<IV.rational(1,100).lo
    # Immutable Gamma arrays are decompressed once, with unchanged arithmetic.
    gamma_mid=gd['mid'];gamma_rad=gd['rad']
    phasecos=cosine_table(degree);phases=[(1+phasecos[j])/2 for j in range(degree+1)]
    rows=[[Fraction(*v) for v in row] for row in p['node_dyadics']]
    raw=pairs_ball([[fraction_pair(v) for v in row] for row in rows]+[[(0.,0.)]*k]*(cells-n+1))
    assert all(Fraction(*v)==Fraction(float(Fraction(*v))) for v in p['alpha_dyadics'])
    assert all(Fraction(*v)==Fraction(float(Fraction(*v))) for row in p['beta_dyadics'] for v in row)
    alpha=Ball(np.array([float(Fraction(*v)) for v in p['alpha_dyadics']]))
    beta=Ball(np.array([[float(Fraction(*v)) for v in row] for row in p['beta_dyadics']]))
    jumps=exact_jumps(p)
    for col in range(k):
        assert sum(row[col] for row in jumps)==0
        assert sum(Fraction(j-n)*h*row[col] for j,row in enumerate(jumps))==0
    jump_norms=[sum((IV.rational(v.numerator,v.denominator)**2 for v in row),IV(0)).sqrt() for row in jumps]
    Jsum=sum(jump_norms,IV(0));Jmax=max(v.hi for v in jump_norms)
    assert Jsum.lo>0 and Jmax>0  # Fresh candidate norms, not checkpoint3 constants.
    U=[];V=[]
    for cell in range(cells):
        left=jumps[n+cell] if cell<=n else [Fraction(0)]*k
        right=jumps[n+cell+1] if cell+1<=n else [Fraction(0)]*k
        U.append([fraction_pair(-h*v/2) for v in left]);V.append([fraction_pair(-h*v/2) for v in right])
    U=pairs_ball(U);V=pairs_ball(V)
    # Trigonometric addition on exact coarse phases; small fractional phases
    # are enclosed by Taylor with an explicit remainder.
    geometry_record=json.loads((folder/'geometry.json').read_text())
    assert geometry_record['k']==k and geometry_record['h']==str(h) and geometry_record['B_exact']=='log(8)/2'
    assert hashlib.sha256((folder/'source_geometry.npz').read_bytes()).hexdigest()==geometry_record['geometry_npz_sha256']
    geo=np.load(folder/'source_geometry.npz');q=geometry_record['q'];B=radius_interval()
    cosbase=Ball(geo['cos_mid'][:q+1],geo['cos_rad'][:q+1])
    sinbase=Ball(geo['sin_mid'][:q+1],geo['sin_rad'][:q+1])
    normball=pairs_ball(geo['norm_pairs'])
    boundary_mid=np.empty((degree+1,k));boundary_rad=np.empty_like(boundary_mid)
    cg=cgamma_interval();cgpoint=Fraction(float(w.CGAMMA))
    cgerror=max(abs(cgpoint-Fraction(cg.lo)),abs(cgpoint-Fraction(cg.hi)))
    if not Fraction(cg.lo)<=cgpoint<=Fraction(cg.hi):raise ArithmeticError('Diagnostic cGamma not in verified enclosure')
    midpoint=np.empty((degree+1,cells,k));radius=np.empty_like(midpoint)
    weight_cell_upper=[];Ucomplex=[]
    for cell in range(cells):
        xx=IV((hh*cell).lo,(hh*(cell+1)).hi)
        weight_cell_upper.append(ib.weight_interval(xx).hi)
    for phase_index,phase in enumerate(phases):
        gamma=Ball(gamma_mid[phase_index],gamma_rad[phase_index])
        ph=Ball.iv(phase)
        g=raw[:cells]*(1-ph)+raw[1:cells+1]*ph
        source=gamma-float(cgpoint)*g
        cvals=[];Wvals=[]
        for cell in range(cells):
            xx=(IV(cell)+phase)*hh
            cvals.append(iv_pair((xx/2).cosh()))
            if cell<n:Wvals.append(iv_pair(ib.weight_interval(xx)))
        source=source-pairs_ball(cvals).reshape(cells,1)*alpha.reshape(1,k)
        interior=Ball.fraction(A)*g[:n]/pairs_ball(Wvals).reshape(n,1)
        source=Ball(np.vstack([(source[:n]+interior).mid,source[n:].mid]),np.vstack([(source[:n]+interior).rad,source[n:].rad]))
        cp=pairs_ball([iv_pair(cos_small(ib.pi_interval()*phase*m*hh/B)) for m in range(k)])
        sp=pairs_ball([iv_pair(sin_small(ib.pi_interval()*phase*m*hh/B)) for m in range(k)])
        E=(cosbase*cp-sinbase*sp)*normball
        moments=E@beta
        inside=source[:q]-moments[:q]
        source=Ball(np.vstack([inside.mid,source[q:].mid]),np.vstack([inside.rad,source[q:].rad]))
        boundary_mid[phase_index]=moments.mid[q];boundary_rad[phase_index]=moments.rad[q]
        source=source-U*Ball.iv(tlog(phase))-V*Ball.iv(tlog(1-phase))
        midpoint[phase_index]=source.mid;radius[phase_index]=source.rad
        print(f'validated analytic model phase {phase_index+1}/{degree+1}',flush=True)
    # Exact Chebyshev-Lobatto coefficient transform, itself enclosed.
    transform=[]
    for mode in range(degree+1):
        row=[]
        for j in range(degree+1):
            factor=Fraction(2,degree)*(Fraction(1,2) if j in [0,degree] else 1)*(Fraction(1,2) if mode in [0,degree] else 1)
            row.append(iv_pair(phasecos[(mode*j)%(2*degree)]*IV.rational(factor.numerator,factor.denominator)))
        transform.append(row)
    coefficients=pairs_ball(transform)@Ball(midpoint.reshape(degree+1,-1),radius.reshape(degree+1,-1))
    cm=coefficients.mid.reshape(degree+1,cells,k).transpose(1,0,2)
    cr=coefficients.rad.reshape(degree+1,cells,k).transpose(1,0,2)
    boundary_coeff=pairs_ball(transform)@Ball(boundary_mid,boundary_rad)
    node_error=usum(norm_upper(cr,axis=2),axis=1)
    node_error[q]=ua(node_error[q],usum(norm_upper(boundary_coeff.rad,axis=1)))
    # Cauchy applied to the SECOND derivative of the log-regular Gamma row.
    rho_half=(-hh/4).exp()/(1-(-hh).exp())
    M2=(rho_half+3)*Jsum
    gamma_remainder=(2*degree+2)*M2*hh**2*IV.rational(1,1<<degree)/(degree*(degree+1))
    # Real Taylor errors for cosines and cosh, multiplied by 1+Lebesgue <=2p+2.
    bnorm=float_iv(norm_upper(beta.mid))
    cosine_error=(2*degree+2)*bnorm*(IV(k)/B).sqrt()*(ib.pi_interval()*(k-1)*hh/(2*B))**(degree+1)/math.factorial(degree+1)
    anorm=float_iv(norm_upper(alpha.mid))
    cosh_error=(2*degree+2)*anorm*IV(1).cosh()*(hh/4)**(degree+1)/math.factorial(degree+1)
    common=gamma_remainder+cosine_error+cosh_error
    # Analytic reciprocal-W bound on |z-cell_mid|<=h. The first theta term
    # dominates the rest by >99/100 for h<=1/640; the three explicit guards above verify the needed caps.
    analytic=[]
    for cell in range(cells):
        error=common
        if cell<n:
            mid=hh*IV.rational(2*cell+1,2);tau=ib.pi_interval()*(2*mid).exp()
            invW=IV.rational(201,100)*(IV.rational(101,100)*tau).exp()/(IV.rational(99,100)**2*tau*(IV.rational(396,100)*tau-6))
            left=ua(norm_upper(raw.mid[cell]),norm_upper(raw.rad[cell]));right=ua(norm_upper(raw.mid[cell+1]),norm_upper(raw.rad[cell+1]))
            difference=raw[cell+1]-raw[cell]
            diff=ua(norm_upper(difference.mid),norm_upper(difference.rad))
            ubound=float_iv(ua(um(ua(left,right),.5),diff))
            error+=(2*degree+2)*IV.rational(A.numerator,A.denominator)*ubound*invW*IV.rational(1,1<<degree)
        analytic.append(error.hi)
    epsilon_squared=IV(0);cell_ledger=[]
    for cell in range(cells):
        err=IV(float(node_error[cell]).as_integer_ratio()[0])/IV(float(node_error[cell]).as_integer_ratio()[1])+IV(analytic[cell])
        # Replacing exact singular coefficients by the saved midpoint costs
        # <=(||delta U||+||delta V||)/e <= (norm radii sum)/2.
        singerr=up((norm_upper(U.rad[cell])+norm_upper(V.rad[cell]))/2)
        err+=float_iv(singerr)
        debit=2*hh*IV(weight_cell_upper[cell])*err**2
        epsilon_squared+=debit
        cell_ledger.append({'cell':cell,'whole_cell_W_upper':str(weight_cell_upper[cell]),
                            'coefficient_row_error_upper_exact_dyadic':list(float(node_error[cell]).as_integer_ratio()),
                            'analytic_interpolation_row_error_upper':str(analytic[cell]),
                            'singular_coefficient_row_error_upper_exact_dyadic':list(float(singerr).as_integer_ratio()),
                            'combined_row_error_upper':str(err.hi),'weighted_squared_error_upper':str(debit.hi)})
    # cGamma midpoint error is a separately bounded source error (not multiplied
    # by an interpolation Lebesgue bound, since its raw P1 term is linear).
    from verify_gram_upper import gram_trace_exact
    l2trace=gram_trace_exact(p['node_dyadics'],h)
    cg_epsilon=IV.rational(cgerror.numerator,cgerror.denominator)*(2*IV.rational(l2trace.numerator,l2trace.denominator)).sqrt()
    displacement=Fraction(geometry_record['B_model_displacement_upper'])
    # Even full line and W<2: squared sliver norm <=4*width*sup||e beta||^2.
    boundary_epsilon=(4*IV.rational(displacement.numerator,displacement.denominator)).sqrt()*bnorm*(IV(k)/B).sqrt()
    epsilon=epsilon_squared.sqrt()+cg_epsilon+boundary_epsilon
    np.savez_compressed(out/'model.npz',coefficients=cm,boundary_cosine_coefficients=boundary_coeff.mid,U=U.mid,V=V.mid,weight_cell_upper=np.array([float(v) for v in weight_cell_upper]))
    # These extra audit artifacts do not change the frozen model or its bounds.
    np.savez_compressed(out/'coefficient_radii.npz',coefficients=cr,boundary_cosine_coefficients=boundary_coeff.rad,U=U.rad,V=V.rad)
    (out/'cell_error_ledger.json').write_text(json.dumps(cell_ledger,indent=2)+'\n')
    result={'status':'CERT','scope':'analytic-plus-log residual model EXCLUDING prime term; weighted row error only',
            'candidate_sha256':digest,'degree':degree,'cells':cells,'k':k,'h':str(h),'boundary_cell':q,'B_exact':'log(8)/2','B_model_cutoff':geometry_record['B_model_cutoff'],'boundary_sliver_weighted_error_upper':str(boundary_epsilon.hi),'sum_jump_norm_upper':str(Jsum.hi),'max_jump_norm_upper':str(Jmax),
            'exact_jump_sum_zero':True,'exact_jump_first_moment_zero':True,
            'Gamma_interpolation_uniform_row_error_upper':str(gamma_remainder.hi),
            'point_and_analytic_interpolation_weighted_error_squared_upper':str(epsilon_squared.hi),
            'cGamma_interval':cg.record(),'cGamma_midpoint_exact_dyadic':list(float(cgpoint).as_integer_ratio()),
            'cGamma_source_error_weighted_upper':str(cg_epsilon.hi),'weighted_row_error_before_prime_upper':str(epsilon.hi),
            'model_sha256':hashlib.sha256((out/'model.npz').read_bytes()).hexdigest(),
            'actual_global256_gate':'NOT_RUN','elapsed_seconds':time.time()-start}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',required=True);ap.add_argument('--gamma',required=True);ap.add_argument('--output',required=True);main(ap.parse_args())
