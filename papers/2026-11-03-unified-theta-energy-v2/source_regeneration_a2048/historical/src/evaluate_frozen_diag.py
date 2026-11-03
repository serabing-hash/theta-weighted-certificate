"""DIAG reevaluation of a fixed exact-dyadic candidate, without another solve.

Uses a Toeplitz FFT application of the same complete Gamma hat kernel, checked
against the dense evaluator. This acceleration changes no mathematical source.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy import linalg
from numpy.polynomial.legendre import leggauss
import weighted64 as w
from target import PENALTY


def uniform_gamma_rows(nodes,h,radius,order,refinement=1):
    n,k=nodes.shape;count=round(radius/h)
    if abs(count*h-radius)>1e-12:raise ValueError('Radius must be mesh-aligned')
    z,_=leggauss(order)
    fullnodes=np.vstack([nodes[:0:-1],nodes])
    rows=np.empty((count,refinement,order,k))
    for sub in range(refinement):
        for j,zz in enumerate(z):
            frac=(sub+(zz+1)/2)/refinement
            column=w.gamma_hat(h*(np.arange(count)+frac+n-1),h)
            firstrow=w.gamma_hat(h*(frac+n-1-np.arange(2*n-1)),h)
            rows[:,sub,j,:]=linalg.matmul_toeplitz((column,firstrow),fullnodes,check_finite=True)
    return rows.reshape(-1,k)


def frozen_residual(nodes,h,alpha,beta,radius,order,refinement):
    n,k=nodes.shape
    count=round(radius/h)*refinement
    x,q=w.mesh_quadrature(radius,count,order)
    row=uniform_gamma_rows(nodes,h,radius,order,refinement)
    g=w.values_from_nodes(x,nodes,h)
    row-=w.CGAMMA*g
    pp=w.prime_powers(math.floor(math.exp(radius+n*h)))
    for num,_,coeff in pp:
        s=math.log(num)
        row-=coeff*(w.values_from_nodes(x+s,nodes,h)+w.values_from_nodes(x-s,nodes,h))
    row+=w.A*g/w.weight(x)[:,None]
    row-=np.cosh(x/2)[:,None]*alpha
    inside=x<w.B
    row[inside]-=w.cosines(x[inside],k)@beta
    return row.T@((2*q*w.weight(x))[:,None]*row)


def independent_gamma_probe(nodes,h):
    # Completely separate positive exponential-label evaluation of Phi, applied
    # to slope jumps. All float arithmetic in this check remains DIAG.
    n=len(nodes);k=nodes.shape[1];L=n*h
    xx=np.r_[-np.arange(n,0,-1)*h,np.arange(n+1)*h]
    vals=np.vstack([np.zeros((1,k)),nodes[:0:-1],nodes,np.zeros((1,k))])
    slopes=np.diff(vals,axis=0)/h
    jumps=np.vstack([slopes[0],np.diff(slopes,axis=0),-slopes[-1]])
    samples=np.array([h/3,.4+h/3,.8-h/3,1.1+h/3,1.35+h/3,1.8+h/3])
    alt=[];tail=[];maxlabels=0
    for x in samples:
        distances=np.abs(x-xx)
        phi=[];tails=[]
        for d in distances:
            labels=max(32,math.ceil(38/(2*d)))
            maxlabels=max(maxlabels,labels)
            al=2*np.arange(labels)+.5
            phi.append(np.sum(np.exp(-al*d)/al**2))
            aj=2*labels+.5
            tails.append(math.exp(-aj*d)*(1/aj**2+1/(2*aj)))
        alt.append(-np.array(phi)@jumps)
        tail.append(float(np.array(tails)@np.linalg.norm(jumps,axis=1)))
    reference=w.gamma_row(samples,nodes,h)
    diff=np.array(alt)-reference
    return {'status':'DIAG','scope':'independent positive exponential-series Gamma row against dilogarithm hat row',
            'sample_points':samples.tolist(),'max_exponential_labels':maxlabels,
            'max_entry_difference':float(np.max(np.abs(diff))),
            'max_vector_difference':float(np.max(np.linalg.norm(diff,axis=1))),
            'positive_series_tail_vector_majorants_DIAG_arithmetic':tail}


def main(args):
    started=time.time();folder=Path(args.candidate);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    p=json.loads((folder/'candidate.json').read_text());verified=json.loads((folder/'verified_components.json').read_text())
    nodes=np.array([[float(Fraction(*v)) for v in row] for row in p['node_dyadics']])
    alpha=np.array([float(Fraction(*v)) for v in p['alpha_dyadics']]);beta=np.array([[float(Fraction(*v)) for v in row] for row in p['beta_dyadics']])
    n,k=nodes.shape;h=float(Fraction(p['h']));L=float(Fraction(p['L']))
    mass,mean,mom=w.moments_and_mass(n,h,k,args.order)
    Gamma=w.gamma_matrix(n,h,args.gamma_order)
    prime,_=w.prime_matrix(n,h,L)
    l2=w.fold_even(w.hat_correlation(np.arange(2*n)*h,h),n)
    rawell=Gamma-w.CGAMMA*l2-prime+w.A*mass
    mm=mean@nodes
    T=nodes.T@rawell@nodes+(2-4*w.A)*np.outer(mm,mm)
    G=nodes.T@mass@nodes-4*np.outer(mm,mm)
    F,_,_,_,d=w.riesz_gram(k)
    J=mom@nodes-4*np.outer(d,mm)
    Ftrial=J.T@linalg.solve(F,J,assume_a='pos')
    print('DIAG frozen full row via Toeplitz kernel',flush=True)
    K=frozen_residual(nodes,h,alpha,beta,2.,args.residual_order,args.refinement)
    tail=float(verified['full_spatial_and_unenumerated_prime_residual_tail']['upper'])
    flower=float(verified['coordinates']['F_trial_scalar_lower'])
    gate=4*T-5*w.A*G/4+w.A*Ftrial/4-float(PENALTY)*(K+tail*np.eye(k))
    conservative=4*T-5*w.A*G/4+w.A*flower*np.eye(k)/4-float(PENALTY)*(K+tail*np.eye(k))
    probe=independent_gamma_probe(nodes,h)
    result={'status':'DIAG','actual_global256_gate':'NOT_RUN','parameters':vars(args),
            'candidate_sha256':hashlib.sha256((folder/'candidate.json').read_bytes()).hexdigest(),
            'mean_max_DIAG':float(np.max(np.abs(mm))),'F_trial_min_DIAG':float(linalg.eigvalsh(Ftrial)[0]),
            'F_trial_identity_difference_DIAG':float(np.max(np.abs(Ftrial-np.eye(k)))),
            'K_max_DIAG':float(linalg.eigvalsh(K)[-1]),'gate_min_actual_F_trial_DIAG':float(linalg.eigvalsh((gate+gate.T)/2)[0]),
            'gate_min_conservative_certified_F_scalar_DIAG':float(linalg.eigvalsh((conservative+conservative.T)/2)[0]),
            'Gamma_independent_probe':probe,'elapsed_seconds':time.time()-started,
            'remaining':['interval primal T/G matrices','interval residual head','interval final sign'],
            'conditional_target_coefficient':'NOT_ACHIEVED','global_half':'NOT_PROVED','RH':'NOT_PROVED'}
    np.savez_compressed(out/'matrices.npz',T=T,G=G,J=J,Ftrial=Ftrial,K=K,gate=gate,conservative_gate=conservative)
    result['matrices_sha256']=hashlib.sha256((out/'matrices.npz').read_bytes()).hexdigest()
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--order',type=int,default=16);ap.add_argument('--gamma-order',type=int,default=96)
    ap.add_argument('--residual-order',type=int,default=24);ap.add_argument('--refinement',type=int,default=2)
    main(ap.parse_args())
