"""Enclose the complete compact residual Gram of the fixed 64-column model.

All shifted-prime knots are retained as exact dyadic model breakpoints, with
their source displacement paid in a global translation bound. Positive step
weight upper envelopes, polynomial-exact verified Gauss rules and enclosed
logarithmic moments integrate the model. This file does not change the trial.
"""
from fractions import Fraction
from functools import lru_cache
from decimal import Decimal
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np

import interval_bounds as ib
from interval_bounds import IV
from ball_array import Ball,pairs_ball,fraction_pair,up,ua,um,usum,norm_upper
from validated_quadrature import prime_geometry,logarithmic_moments,gauss_verified,cheb_vandermonde_ball
from verify_gram_upper import upper_dyadic,gram_integer_matrix


def exact_float_iv(x):return IV.rational(*float(x).as_integer_ratio())


def prime_coefficients(cell,points,records,nodes,h=Fraction(1,640)):
    segments=len(points)-1;k=nodes.shape[1];n=len(nodes)-2
    C0=Ball(np.zeros((segments,k)));C1=Ball(np.zeros((segments,k)))
    mids=[(a+b)/2 for a,b in zip(points,points[1:])]
    for record in records:
        shift=record['shift']/h
        for direction in [-1,1]:
            ids=[];offsets=[];signs=[]
            s=direction*shift
            for mid in mids:
                q=Fraction(cell)+mid+s;sign=1 if q>=0 else -1
                j=(sign*q).__floor__()
                ids.append(min(j,n));signs.append(sign)
                offset=sign*(Fraction(cell)+s)-j
                offsets.append(fraction_pair(offset))
            ids=np.array(ids)
            left=Ball(nodes[ids]);right=Ball(nodes[np.minimum(ids+1,n+1)])
            diff=right-left
            offset=pairs_ball(offsets).reshape(segments,1)
            weight=Ball.fraction(record['weight'])
            C0=C0+weight*(left+offset*diff)
            C1=C1+weight*(diff*np.array(signs)[:,None])
    return C0,C1


def sum_rows(ball):
    # A positive exact row of ones supplies a fully bounded dot product.
    return Ball(np.ones((1,len(ball.mid))))@ball


def main(args):
    start=time.time();folder=Path(args.candidate);modeldir=Path(args.model);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    packet=json.loads((folder/'candidate.json').read_text());digest=hashlib.sha256((folder/'candidate.json').read_bytes()).hexdigest()
    mr=json.loads((modeldir/'result.json').read_text());assert mr['candidate_sha256']==digest
    assert hashlib.sha256((modeldir/'model.npz').read_bytes()).hexdigest()==mr['model_sha256']
    data=np.load(modeldir/'model.npz');degree=mr['degree'];cells=mr['cells'];h=Fraction(packet['h']);n=packet['n'];k=packet['k']
    assert cells*h==2 and k==256 and packet['B']=='log(8)/2' and packet['a']=='1/2048'
    boundary_cell=mr['boundary_cell'];B0=Fraction(mr['B_model_cutoff']);boundary_phase=B0/h-boundary_cell
    assert 0<boundary_phase<1
    ib.pi_interval=lru_cache(maxsize=1)(ib.pi_interval)
    assert IV(25).log().lo>IV.rational(16,5).hi
    records,points=prime_geometry(args.weight_refinement,h,[boundary_phase])
    segments=len(points)-1
    print(f'fixed partition: {segments} segments per physical cell; degree {degree}',flush=True)
    IL,IR,IUU,IVV,IUV=logarithmic_moments(points,degree)
    gx,gw=gauss_verified(degree+1)
    lower=pairs_ball([fraction_pair(x) for x in points[:-1]]).reshape(segments,1)
    upper=pairs_ball([fraction_pair(x) for x in points[1:]]).reshape(segments,1)
    t=(lower+upper)/2+(upper-lower)*gx.reshape(1,degree+1)/2
    X=2*t-1
    vandermonde=cheb_vandermonde_ball(X,degree).reshape(segments*(degree+1),degree+1)
    lengths=upper-lower
    # Full-line factor 2 cancels the Gauss mapping factor 1/2.
    measure=Ball.fraction(h)*lengths*gw.reshape(1,degree+1)
    assert all(Fraction(*v)==Fraction(float(Fraction(*v))) for row in packet['node_dyadics'] for v in row)
    nodes=np.array([[float(Fraction(*v)) for v in row] for row in packet['node_dyadics']]+[[0.]*k,[0.]*k])
    boundary_mask=np.array([1 if (a+b)/2<boundary_phase else 0 for a,b in zip(points,points[1:])])
    boundary_coeff=Ball(data['boundary_cosine_coefficients'])
    # NpzFile indexing decompresses a complete array: load immutable arrays once.
    coefficient_array=data['coefficients'];U_array=data['U'];V_array=data['V']
    weight_indices=np.array([((a+b)*args.weight_refinement/2).__floor__() for a,b in zip(points,points[1:])])
    weights_saved=[]
    K=Ball(np.zeros((k,k)))
    cell_trace=[]
    for cell in range(cells):
        # Uniform weight panels are also in the exact prime partition. No
        # monotonicity of theta is assumed: enclose the entire panel.
        weights=[]
        for panel in range(args.weight_refinement):
            a=h*(cell+Fraction(panel,args.weight_refinement));b=h*(cell+Fraction(panel+1,args.weight_refinement))
            aa=IV.rational(a.numerator,a.denominator);bb=IV.rational(b.numerator,b.denominator)
            W=ib.weight_interval(IV(aa.lo,bb.hi))
            weights.append(upper_dyadic(W.hi))
        weights_saved.append(weights)
        segment_weights=Ball(np.array([float(Fraction(*weights[j])) for j in weight_indices]))
        coeff=Ball(coefficient_array[cell])
        C0,C1=prime_coefficients(cell,points,records,nodes,h)
        P= (vandermonde@coeff).reshape(segments,degree+1,k)-C0.reshape(segments,1,k)-t.reshape(segments,degree+1,1)*C1.reshape(segments,1,k)
        if cell==boundary_cell:
            boundary_values=(vandermonde@boundary_coeff).reshape(segments,degree+1,k)
            P=P-boundary_mask[:,None,None]*boundary_values
        ww=(segment_weights.reshape(segments,1)*measure).reshape(-1,1)
        values=P.reshape(-1,k)
        Kcell=values.T@(ww*values)
        # Prime affine parts in Chebyshev coordinates on the ORIGINAL cell.
        prime0=C0+C1/2;prime1=C1/2
        left=(IL@coeff)-IL[:,0].reshape(segments,1)*prime0-IL[:,1].reshape(segments,1)*prime1
        right=(IR@coeff)-IR[:,0].reshape(segments,1)*prime0-IR[:,1].reshape(segments,1)*prime1
        if cell==boundary_cell:
            left=left-boundary_mask[:,None]*(IL@boundary_coeff)
            right=right-boundary_mask[:,None]*(IR@boundary_coeff)
        qU=Ball.fraction(2*h)*sum_rows(segment_weights.reshape(segments,1)*left)
        qV=Ball.fraction(2*h)*sum_rows(segment_weights.reshape(segments,1)*right)
        U=Ball(U_array[cell].reshape(1,k));V=Ball(V_array[cell].reshape(1,k))
        Kcell=Kcell+U.T@qU+qU.T@U+V.T@qV+qV.T@V
        sUU=Ball.fraction(2*h)*sum_rows((segment_weights*IUU).reshape(segments,1))
        sVV=Ball.fraction(2*h)*sum_rows((segment_weights*IVV).reshape(segments,1))
        sUV=Ball.fraction(2*h)*sum_rows((segment_weights*IUV).reshape(segments,1))
        Kcell=Kcell+sUU*(U.T@U)+sVV*(V.T@V)+sUV*(U.T@V+V.T@U)
        K=K+Kcell
        cell_trace.append(float(np.trace(Kcell.mid)))
        if (cell+1)%64==0:print(f'validated residual integration {cell+1}/{cells}',flush=True)
    K=(K+K.T)/2
    radius=float(np.max(usum(K.rad,axis=1)))
    radius_fraction=Fraction(radius)
    trace_upper=sum(Fraction(float(K.mid[j,j]))+Fraction(float(K.rad[j,j])) for j in range(k))
    if trace_upper<0:raise ArithmeticError('Impossible negative upper trace for model Gram')
    # Fresh positive-model trace at the actual rank, no inherited U.
    root=IV.rational(trace_upper.numerator,trace_upper.denominator).sqrt()
    model_norm=Fraction(*upper_dyadic(root.hi))
    components=json.loads((folder/'verified_components.json').read_text())
    derivative=IV(components['derivative_gram_trace_upper']).sqrt()
    from verify_gram_upper import gram_trace_exact
    l2trace=gram_trace_exact(packet['node_dyadics'],h)
    l2norm=IV.rational(l2trace.numerator,l2trace.denominator).sqrt()
    prime_error=IV(0)
    for record in records:
        ea=record['weight_error'];es=record['shift_error'];aw=abs(record['weight'])
        prime_error+=2*IV(2).sqrt()*(IV.rational(ea.numerator,ea.denominator)*l2norm+IV.rational(aw.numerator,aw.denominator)*IV.rational(es.numerator,es.denominator)*derivative)
    epsilon=IV(mr['weighted_row_error_before_prime_upper'])+prime_error
    eps_upper=Fraction(epsilon.hi)
    inflation=2*model_norm*eps_upper+eps_upper**2
    tail=Fraction(components['full_spatial_and_unenumerated_prime_residual_tail']['upper'])
    total_debit=radius_fraction+inflation+tail
    center=[[Fraction(float(v)) for v in row] for row in K.mid]
    for i in range(k):center[i][i]+=total_debit
    den=math.lcm(*(x.denominator for row in center for x in row))
    exact={'status':'CERT','scope':'full weighted residual Gram upper bound for the exact frozen candidate, conditional on documented analytic model bounds',
            'candidate_sha256':digest,'model_result_sha256':hashlib.sha256((modeldir/'result.json').read_bytes()).hexdigest(),'model_npz_sha256':mr['model_sha256'],'a':packet['a'],'B_exact':packet['B'],'k':k,'h':str(h),'boundary_cell':boundary_cell,'B_model_cutoff':str(B0),'boundary_phase':str(boundary_phase),'boundary_sliver_already_in_model_error':mr['boundary_sliver_weighted_error_upper'],'matrix_numerators':[[str(v.numerator*(den//v.denominator)) for v in row] for row in center],
            'common_denominator':str(den),'Gram_arithmetic_radius_upper':str(radius_fraction),
            'positive_model_trace_upper':str(trace_upper),'positive_model_norm_upper':str(model_norm),
            'model_row_error_upper':str(eps_upper),'row_error_Gram_inflation':str(inflation),
            'outer_tail_once':str(tail),'total_scalar_Gram_debit':str(total_debit),
            'all_prime_powers_on_compact_interval':[r['n'] for r in records],
            'shifted_prime_source_error_upper':str(prime_error.hi),
            'prime_model_constants':[{name:str(value) for name,value in r.items()} for r in records],
            'exact_normalized_breakpoints':[str(v) for v in points],
            'weight_refinement':args.weight_refinement,'model_degree':degree,'Gauss_order':degree+1,
            'Gauss_use':'polynomial part is degree <=2*degree, integrated exactly by the enclosed rule; logs use separate enclosed analytic moments',
            'elapsed_seconds':time.time()-start,'actual_global256_gate':'NOT_RUN'}
    (out/'K_upper_exact.json').write_text(json.dumps(exact,indent=2)+'\n')
    np.savez_compressed(out/'gram_evidence.npz',model_center=K.mid,model_radius=K.rad,cell_trace_DIAG=np.array(cell_trace))
    (out/'weight_upper_dyadics.json').write_text(json.dumps(weights_saved,separators=(',',':'))+'\n')
    result={name:exact[name] for name in ['status','scope','candidate_sha256','positive_model_trace_upper','positive_model_norm_upper','Gram_arithmetic_radius_upper','model_row_error_upper','row_error_Gram_inflation','elapsed_seconds','actual_global256_gate']}
    result['K_upper_sha256']=hashlib.sha256((out/'K_upper_exact.json').read_bytes()).hexdigest()
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',required=True);ap.add_argument('--model',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--weight-refinement',type=int,default=16);main(ap.parse_args())
