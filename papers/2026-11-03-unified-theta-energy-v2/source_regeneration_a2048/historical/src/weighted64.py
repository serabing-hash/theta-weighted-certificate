"""NEW full-line weighted response prototype. All floating output is DIAG.

No old matrix or dataset is imported. See NUMERICAL_CONTRACT.md for conventions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import linalg, special
from target import PENALTY

B = math.log(8.0) / 2.0
A = 1.0 / 2048.0
CGAMMA = math.log(math.pi) - special.digamma(0.25)


def theta(x, terms=8):
    """Even source series, diagnostic floating evaluation (tail separately bounded)."""
    x = np.abs(np.asarray(x, dtype=float))
    tau = math.pi * np.arange(1, terms + 1, dtype=float) ** 2 * np.exp(2 * x[..., None])
    return np.exp(x / 2) * np.sum((4 * tau**2 - 6 * tau) * np.exp(-tau), axis=-1)


def weight(x):
    x = np.asarray(x, dtype=float)
    return theta(x) / (2 * np.cosh(x / 2))


def cosines(x, k, radius=B):
    x = np.asarray(x)
    out = np.cos(x[..., None] * (np.arange(k) * math.pi / radius)) / math.sqrt(radius)
    out[..., 0] /= math.sqrt(2)
    return out


def prime_powers(nmax):
    """(n,p,Lambda(n)/sqrt(n)); include powers once, never weight p^r by log(p^r)."""
    sieve = np.ones(nmax + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, math.isqrt(nmax) + 1):
        if sieve[p]:
            sieve[p*p::p] = False
    out = []
    for p0 in np.flatnonzero(sieve):
        p = int(p0)
        n = p
        while n <= nmax:
            out.append((n, p, math.log(p) / math.sqrt(n)))
            n *= p
    return sorted(out)


def gamma_potential(d):
    """Complete H(d), not a finite exponential-label sum. DIAG scipy spence."""
    t = np.exp(-np.abs(np.asarray(d)) / 2)
    return special.spence(1-t) - special.spence(1+t) + 2*special.spence(1-1j*t).imag


def gamma_hat(x, h):
    return (2*gamma_potential(x)-gamma_potential(np.asarray(x)-h)
            -gamma_potential(np.asarray(x)+h))/h


def fold_even(kernel, n):
    ix = np.arange(n)
    out = 2*(kernel[np.abs(ix[:, None]-ix)] + kernel[ix[:, None]+ix])
    out[0, :] /= 2
    out[:, 0] /= 2
    return out


def hat_correlation(x, h):
    t = np.abs(np.asarray(x))/h
    return h*(np.maximum(2-t, 0)**3-4*np.maximum(1-t, 0)**3)/6


def gamma_matrix(n, h, order):
    # Integrate the central full-line hat against every translated Gamma row.
    z, w = leggauss(order)
    x = np.r_[h*(z-1)/2, h*(z+1)/2]
    w = np.tile(w*h/2, 2)*(1-np.abs(x)/h)
    lag = np.arange(2*n)*h
    kernel = gamma_hat(x[:, None]-lag, h).T @ w
    return fold_even(kernel, n)


def prime_matrix(n, h, length):
    lag = np.arange(2*n)*h
    kernel = np.zeros(2*n)
    primes = prime_powers(math.floor(math.exp(2*length)))
    for value, _, coeff in primes:
        s = math.log(value)
        kernel += coeff*(hat_correlation(lag+s, h)+hat_correlation(lag-s, h))
    return fold_even(kernel, n), primes


def mesh_quadrature(length, panels, order):
    z, w = leggauss(order)
    h = length/panels
    return (h*(np.arange(panels)[:, None]+(z+1)/2)).ravel(), np.tile(w*h/2, panels)


def hats(x, n, h):
    """Full even hats on x>=0; dense only for small coordinate assembly."""
    return np.maximum(1-np.abs(np.abs(np.asarray(x))[:, None]/h-np.arange(n)), 0)


def values_from_nodes(x, nodes, h):
    """Evaluate compact even piecewise-linear columns without a dense basis matrix."""
    x = np.abs(np.asarray(x))
    n = len(nodes)
    u = x/h
    j = np.floor(u).astype(int)
    t = u-j
    padded = np.vstack([nodes, np.zeros((1, nodes.shape[1]))])
    left = padded[np.minimum(j, n)]
    right = padded[np.minimum(j+1, n)]
    return left*(1-t[:, None])+right*t[:, None]


def moments_and_mass(n, h, k, order):
    length = n*h
    x, w = mesh_quadrature(length, n, order)
    # Local support avoids ill-conditioned dense accumulation of the H mass.
    z, qw = leggauss(order)
    t = (z+1)/2
    W = weight(x).reshape(n, order)
    weighted = (qw*h)/(W)  # full-line factor two cancels the mapped factor 1/2
    diag_left = weighted @ (1-t)**2
    diag_right = weighted @ t**2
    off = weighted @ (t*(1-t))
    diagonal = diag_left.copy()
    diagonal[1:] += diag_right[:-1]
    mass = np.diag(diagonal)+np.diag(off[:-1],1)+np.diag(off[:-1],-1)
    # Exact analytic mean formula for full-line hats, evaluated in binary64 here.
    mean = 32*math.sinh(h/4)**2/h*np.cosh(np.arange(n)*h/2)
    mean[0] /= 2
    moments = physical_hat_moments(n,h,k,B)
    return mass, mean, moments


def physical_hat_moments(n,h,k,radius=B):
    """Analytic P1 moments on the true-boundary floating DIAG approximation."""
    q=math.floor(radius/h);delta=radius-q*h
    if not 1<=q<n-1:raise ValueError('Source boundary must be inside raw support')
    result=np.zeros((k,n));j=np.arange(q)
    for mode in range(k):
        norm=1/math.sqrt(radius*(2 if mode==0 else 1))
        if mode==0:
            result[mode,:q]=h;result[mode,0]=h/2
            result[mode,q]=h/2+delta-delta**2/(2*h)
            result[mode,q+1]=delta**2/(2*h)
        else:
            omega=mode*math.pi/radius;theta=omega*h
            result[mode,:q]=h*np.sinc(theta/(2*math.pi))**2*np.cos(j*theta)
            result[mode,0]/=2
            cq=math.cos(q*theta);cp=math.cos((q-1)*theta);end=(-1)**mode
            result[mode,q]=(2*cq-cp-end)/(h*omega**2)
            result[mode,q+1]=(end-cq)/(h*omega**2)
        result[mode]*=2*norm
    return result


def riesz_gram(k, panels=256, order=16):
    x, w = mesh_quadrature(B, panels, order)
    e = cosines(x,k)
    W = weight(x)
    d = e.T@(2*w*np.cosh(x/2)*W)
    gram = e.T@((2*w*W)[:,None]*e)-4*np.outer(d,d)
    ev, U = linalg.eigh(gram)
    if ev[0] <= 0:
        raise ArithmeticError('DIAG F is not positive; cannot whiten these coordinates')
    sqrt = (U*np.sqrt(ev))@U.T
    invsqrt = (U/np.sqrt(ev))@U.T
    return gram, sqrt, invsqrt, ev, d


def gamma_row(x, nodes, h):
    n = len(nodes)
    centers = np.arange(n)*h
    rows = gamma_hat(x[:,None]-centers,h)+gamma_hat(x[:,None]+centers,h)
    rows[:,0] /= 2
    return rows@nodes


def physical_residual(x, nodes, h, alpha, beta, residual_primes):
    g = values_from_nodes(x,nodes,h)
    row = gamma_row(x,nodes,h)-CGAMMA*g
    for n, _, coeff in residual_primes:
        s = math.log(n)
        row -= coeff*(values_from_nodes(x+s,nodes,h)+values_from_nodes(x-s,nodes,h))
    # Safe where g vanishes: avoid 0/very-small issues beyond its support.
    row += A*g/weight(x)[:,None]
    row -= np.cosh(x/2)[:,None]*alpha
    inside = x < B
    row[inside] -= cosines(x[inside],len(beta))@beta
    return row


def residual_gram(nodes, h, alpha, beta, radius, order, refinement=1):
    n = len(nodes)
    length = n*h
    panels = round(radius/h)*refinement
    if abs(panels*h/refinement-radius)>1e-12:
        raise ValueError('Residual radius must be a trial-mesh multiple')
    x,w = mesh_quadrature(radius,panels,order)
    primes = prime_powers(math.floor(math.exp(radius+length)))
    K = np.zeros((nodes.shape[1],nodes.shape[1]))
    maxrow = 0.0
    for begin in range(0,len(x),256):
        xx=x[begin:begin+256]
        r=physical_residual(xx,nodes,h,alpha,beta,primes)
        K += r.T@((2*w[begin:begin+256]*weight(xx))[:,None]*r)
        maxrow=max(maxrow,float(np.max(np.linalg.norm(r,axis=1))))
    # This scalar uses an analytic formula, but its input coefficients are DIAG.
    D=float(np.max(np.linalg.norm(nodes,axis=1)))
    ca=float(np.linalg.norm(alpha))
    def ip(p):
        return math.exp(p*radius-math.pi*math.exp(2*radius))/(2*math.pi*math.exp(2*radius)-p)
    tail=252*(4*length**2*D**2*math.exp(length)/(1-math.exp(-2*(radius-length)))**2*ip(3)
              +D**2*math.exp(2*length)*ip(6)+ca**2*ip(5))
    return (K+K.T)/2,tail,{'prime_powers':primes,'panels':panels,'nodes':len(x),
                         'D_DIAG':D,'alpha_norm_DIAG':ca,'max_physical_row_DIAG':maxrow}


def run(args):
    started=time.time()
    out=Path(args.output)
    out.mkdir(parents=True,exist_ok=True)
    n=args.cells; k=args.k; length=args.length; h=length/n
    if n<=k+1:
        raise ValueError('Need at least k+2 cells')
    print(f'DIAG assemble k={k} N={n} L={length} h={h}',flush=True)
    F,Fhalf,Finvhalf,Fev,d=riesz_gram(k)
    mass,mean,moments=moments_and_mass(n,h,k,args.order)
    scale=np.sqrt(weight(np.arange(n)*h))
    mass=scale[:,None]*mass*scale
    gamma=gamma_matrix(n,h,args.gamma_order)*scale[:,None]*scale
    primes,prime_head=prime_matrix(n,h,length)
    primes=primes*scale[:,None]*scale
    l2=fold_even(hat_correlation(np.arange(2*n)*h,h),n)*scale[:,None]*scale
    ell=gamma-CGAMMA*l2-primes+A*mass
    C=np.vstack([2*mean*scale,Finvhalf@(moments*scale)])
    rhs=np.vstack([np.zeros((n+1,k)),np.eye(k)])
    saddle=np.block([[ell,C.T],[C,np.zeros((k+1,k+1))]])
    print(f'DIAG constrained solve dimension={len(saddle)}',flush=True)
    sol=linalg.solve(saddle,rhs,assume_a='sym')
    coeff=sol[:n]; multipliers=-sol[n:]
    nodes=scale[:,None]*coeff
    alpha=2*multipliers[0]
    beta=Finvhalf@multipliers[1:]
    T=coeff.T@ell@coeff
    G=coeff.T@mass@coeff
    Fcoord=np.eye(k)
    T=(T+T.T)/2; G=(G+G.T)/2
    finite_gate=4*T-A*G
    trial_gate_no_residual=4*T-5*A*G/4+A*Fcoord/4
    print('DIAG full continuous row integration',flush=True)
    from evaluate_frozen_diag import frozen_residual
    K=frozen_residual(nodes,h,alpha,beta,args.residual_radius,args.residual_order,args.residual_refinement)
    K=(K+K.T)/2
    D=float(np.max(np.linalg.norm(nodes,axis=1)));ca=float(np.linalg.norm(alpha));R=args.residual_radius
    def ip(p):return math.exp(p*R-math.pi*math.exp(2*R))/(2*math.pi*math.exp(2*R)-p)
    tail=252*(4*length**2*D**2*math.exp(length)/(1-math.exp(-2*(R-length)))**2*ip(3)+D**2*math.exp(2*length)*ip(6)+ca**2*ip(5))
    remeta={'method':'full-kernel FFT row DIAG','prime_powers':prime_powers(math.floor(math.exp(R+length))),'D_DIAG':D,'alpha_norm_DIAG':ca}

    gate=trial_gate_no_residual-float(PENALTY)*(K+tail*np.eye(k))
    target=np.vstack([np.zeros((1,k)),np.eye(k)])
    result={
      'status':'DIAG', 'actual_global_gate':'NOT_RUN', 'scope':'NEW256 changed-radius response DIAG' if k==256 else 'small pilot; not target256',
      'parameters':vars(args), 'a':'1/2048','B':'log(8)/2','theta_terms':8,
      'F_eigenvalue_min':float(Fev[0]),'F_eigenvalue_max':float(Fev[-1]),'F_condition':float(Fev[-1]/Fev[0]),
      'constraint_error_max':float(np.max(np.abs(C@coeff-target))),
      'weighted_mean_error_max':float(np.max(np.abs(mean@nodes))),
      'physical_moment_error_max':float(np.max(np.abs(moments@nodes-Fhalf))),
      'KKT_error_max':float(np.max(np.abs(ell@coeff-C.T@multipliers))),
      'T_eigenvalue_min':float(linalg.eigvalsh(T)[0]),'G_eigenvalue_min':float(linalg.eigvalsh(G)[0]),
      'finite_response_gate_min_DIAG':float(linalg.eigvalsh(finite_gate)[0]),
      'trial_gate_without_residual_min_DIAG':float(linalg.eigvalsh(trial_gate_no_residual)[0]),
      'K_eigenvalue_min_DIAG':float(linalg.eigvalsh(K)[0]),'K_eigenvalue_max_DIAG':float(linalg.eigvalsh(K)[-1]),
      'sufficient_gate_min_DIAG':float(linalg.eigvalsh(gate)[0]),
      'spatial_and_prime_tail_scalar_DIAG_inputs':tail,
      'primal_prime_head':prime_head,'residual_metadata':remeta,
      'elapsed_seconds':time.time()-started,
      'not_certified':['F quadrature and whitening','exact mean and moment correction','Gamma/primal quadrature',
                       'H norm quadrature','continuous residual quadrature','interval coefficient/tail bounds','interval final matrix sign'],
      'conditional_target_coefficient':'NOT_ACHIEVED','global_half':'NOT_PROVED','RH':'NOT_PROVED'}
    np.savez_compressed(out/'matrices.npz',F=F,Fhalf=Fhalf,Finvhalf=Finvhalf,d=d,coeff=coeff,nodes=nodes,
                        T=T,G=G,K=K,gate=gate,finite_gate=finite_gate,multipliers=multipliers,
                        alpha=alpha,beta=beta,scale=scale,constraint_matrix=C,trial_ell=ell,
                        moment_matrix=moments,mean_vector=mean,trial_mass=mass)
    result['raw_matrices_sha256']=hashlib.sha256((out/'matrices.npz').read_bytes()).hexdigest()
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--k',type=int,default=256)
    ap.add_argument('--cells',type=int,default=1536)
    ap.add_argument('--length',type=float,default=1.2)
    ap.add_argument('--order',type=int,default=12)
    ap.add_argument('--gamma-order',type=int,default=32)
    ap.add_argument('--residual-radius',type=float,default=2.0)
    ap.add_argument('--residual-order',type=int,default=8)
    ap.add_argument('--residual-refinement',type=int,default=1)
    ap.add_argument('--output',required=True)
    run(ap.parse_args())
