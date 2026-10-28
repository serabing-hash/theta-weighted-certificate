#!/usr/bin/env python3
"""Rigorous ball-arithmetic sufficient Schur certificate, B=1/2.
Requires python-flint==0.9.0. No binary64 value is used in an assertion.
All infinite-series and mode tails are enclosed analytically; see accompanying note.
"""
import argparse, hashlib, json, time
from pathlib import Path
from flint import arb, acb, ctx


def verify():
    ctx.prec = 160
    M, N, J = 16, 8192, 24
    pi = arb.pi(); B = arb(1)/2; s = arb(2).log(); a = s/arb(2).sqrt()
    assert s > B and s < 1 and arb(3).log() > 1
    k = [2*pi*n for n in range(N+1)]
    b = [arb(2).sqrt()]+[arb(2)]*M
    v = [b[m]*((-1)**m) for m in range(M)]
    sh = (B/2).sinh()
    c = [v[m]*sh/2/(arb(1)/4+k[m]**2) for m in range(M)]
    psi = [acb(arb(1)/4, k[n]/2).digamma() for n in range(N+1)]
    D = [z.real-pi.log() for z in psi]
    U = [acb(arb(1)/4).polygamma(1).real/4]
    U += [psi[n].imag/(2*k[n]) for n in range(1,N+1)]
    assert D[M]-a > 2 and D[N]-a > 1
    aj = [arb(2*j)+arb(1)/2 for j in range(J)]
    wt = [x*x*(-2*x*B).exp() for x in aj]
    lowV = [[1/(x*x+k[m]*k[m]) for x in aj] for m in range(M)]
    first = arb(2*J)+arb(1)/2
    exp_error = (-2*first*B).exp()/(first*first*(1-(-4*B).exp()))
    Sdiag = [U[0]]+[psi[m].imag/(4*k[m])+acb(arb(1)/4,k[m]/2).polygamma(1).real/8 for m in range(1,M)]
    def row(n):
        bn = arb(2).sqrt() if n==0 else arb(2)
        sn = (-1)**n; kn=k[n]; kn2=kn*kn
        nv = [wt[j]/(aj[j]*aj[j]+kn2) for j in range(J)]
        cn = bn*sn*sh/2/(arb(1)/4+kn2)
        result=[]
        for m in range(M):
            km=k[m]; km2=km*km
            if n==m: val=Sdiag[m]
            else: val=(kn2*U[n]-km2*U[m])/(kn2-km2)
            # A symmetric radius encloses the negative omitted exponential series.
            val -= sum((nv[j]*lowV[m][j] for j in range(J)),arb(0))
            val += arb(0,exp_error.upper())
            boundary=bn*sn*v[m]*val
            if n>=M:
                integral=-(kn*((-1)**m)*(kn*(s-B)).sin()+km*sn*(km*(B-s)).sin())/(kn2-km2)
            else:
                length=2*B-s
                diff=kn-km; total=kn+km
                sd=arb(1) if n==m else (diff*length/2).sin()/(diff*length/2)
                st=arb(1) if n+m==0 else (total*length/2).sin()/(total*length/2)
                integral=length/2*(sd*(total*s/2).cos()+st*(diff*s/2).cos())
            val=boundary+4*cn*c[m]-a*bn*b[m]*integral
            if n==m:val+=D[n]
            result.append(val)
        return result
    A=[row(n) for n in range(M)]
    # Symmetry is exact analytically; use one consistently enclosed triangle.
    for i in range(M):
        for j in range(i):
            assert (A[i][j]-A[j][i]).contains(0)
            A[j][i]=A[i][j]
    C=[[arb(0) for j in range(M)] for i in range(M)]
    start=time.monotonic()
    for n in range(M,N):
        r=row(n); inv=1/(D[n]-a)
        for i in range(M):
            for j in range(i+1): C[i][j]+=r[i]*r[j]*inv
        if n%1024==0:print(f"Enclosed modes through {n}; elapsed {time.monotonic()-start:.1f}s",flush=True)
    E0=(-B).exp()/(1-(-4*B).exp())
    kn=k[N]
    constants=[]
    for m in range(M):
        km=k[m]; den=1-(km/kn)**2
        km2U=arb(0) if m==0 else 1+pi*km/4
        constants.append(b[m]*(km2U/den+E0+a*(km+km*km/kn)/den)+2*sh*abs(c[m]))
    tail_rank=8*(pi/4+a+1/kn)**2/(2*pi)**2/(N-1)
    tail_scalar=8*sum((x*x for x in constants),arb(0))/(2*pi)**4/(3*(N-1)**3)
    for i in range(M):
        for j in range(i+1):
            C[i][j]+=tail_rank*v[i]*v[j]
            if i==j:C[i][j]+=tail_scalar
            C[j][i]=C[i][j]
    trace=sum((C[i][i] for i in range(M)),arb(0))
    assert trace < arb(1)/10
    mu=arb(8)/10**7
    H=[[A[i][j]-C[i][j]-(mu if i==j else arb(0)) for j in range(M)] for i in range(M)]
    L=[[arb(0) for j in range(M)] for i in range(M)]
    pivots=[]
    for i in range(M):
        L[i][i]=arb(1)
        pivot=H[i][i]-sum((L[i][j]**2*pivots[j] for j in range(i)),arb(0))
        assert pivot > 0, f"Unproved positive pivot {i}: {pivot}"
        pivots.append(pivot)
        for n in range(i+1,M):
            L[n][i]=(H[n][i]-sum((L[n][j]*L[i][j]*pivots[j] for j in range(i)),arb(0)))/pivot
    assert (arb(7)/10**7)*(arb(11)/10) < mu
    return {
        "status":"PASS_INTERVAL_SCHUR_CERTIFICATE",
        "scope":"real even minimum compact-support gamma-form domain, B <= 1/2",
        "q_lower_bound_L2":"7/10000000",
        "schur_margin_low_mode_L2":"8/10000000",
        "precision_bits":ctx.prec,"low_modes":M,"tail_start":N,"exponential_terms":J,
        "prime_weight":str(a),"high_block_floor_at_M":str(D[M]-a),
        "high_block_floor_at_N":str(D[N]-a),
        "rank_one_tail_coefficient":str(tail_rank),"scalar_tail_coefficient":str(tail_scalar),
        "coupling_bound_trace":str(trace),"exponential_entry_error":str(exp_error),
        "ldl_pivots_of_F_minus_mu_I":[str(x) for x in pivots],
        "trust_boundary":"Analytic derivation, this source code, python-flint/FLINT, Python and execution environment; not a formal proof-assistant verification.",
        "global_all_radii_positivity":"NOT_PROVED"}

if __name__=="__main__":
    if not __debug__: raise RuntimeError("Run without -O: certificate assertions must remain enabled.")
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path);args=parser.parse_args()
    result=verify()
    result["verifier_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    import flint
    result["python_flint_version"]=flint.__version__
    data=json.dumps(result,indent=2)+"\n"
    if args.output:args.output.write_text(data)
    print(data)
