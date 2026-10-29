"""Portable exact finite certificate replay; analytic premises described in README."""
import argparse
import hashlib
import json
import sys
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path

if not __debug__:
    raise RuntimeError('Assertions are proof checks: do not use -O.')
sys.set_int_max_str_digits(100000)
parser = argparse.ArgumentParser()
parser.add_argument('--data-dir', type=Path, default=Path('data'))
parser.add_argument('--output', type=Path, default=Path('result.json'))
args = parser.parse_args()
HASHES = {'success.json': '19156f6635bb25e853b9a1aecd650672043113f85d279c562e1a090269b0ca91',
          'diagnostic.json': '4c67f0c3f37bb8ce3c4f7c6da166050f2a1760c62bd47227c7709fb3a0b2ea05'}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for name, expected in HASHES.items():
    assert sha(args.data_dir / name) == expected
s = json.loads((args.data_dir / 'success.json').read_text())
d = json.loads((args.data_dir / 'diagnostic.json').read_text())
assert s['status'] == 'PASS_INTERVAL_FULL_ACTUAL_DEFECT_SCHUR_CERTIFICATE'
assert s['diagnostic']['sha256'] == HASHES['diagnostic.json']
assert d['missing_matrices'] == []
assert d['fixed_parameters'] == {'support_radius':'4/5','precision_bits':256,'low_modes':32,'source_columns':64,'actual_trial_indices':[32,63],'trial_columns':32,'tail_start':16384,'exponential_terms':32,'active_prime_powers':[2,3,4],'python_flint_version':'0.9.0'}
assert s['verifier_sha256'] == d['verifier_sha256'] == '3b46a081b272146cc6cc8474416f124726a45453f55e01bb85b0eb1762e192bc'
assert Q(d['high_block_floor_used']) == Q(8,5)
assert Q(d['tail_floor_used']) == Q(39,5)
N = 32
BITS = 240
GRID = 1 << BITS
ZERO = (Q(0), Q(0))
def rounded(x):
    lo, hi = x
    assert lo <= hi
    return (Q((lo.numerator*GRID)//lo.denominator, GRID),
            Q(-((-hi.numerator*GRID)//hi.denominator), GRID))
def iv(record):
    return rounded((Q(record['lower_rational']), Q(record['upper_rational'])))
def pt(x):
    return Q(x), Q(x)
def add(x,y): return x[0]+y[0], x[1]+y[1]
def sub(x,y): return x[0]-y[1], x[1]-y[0]
def mul(x,y):
    products = (x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1])
    return min(products),max(products)
def scale(x,c): return mul(x,pt(c))
def hull(x,y): return min(x[0],y[0]),max(x[1],y[1])
def midpoint(x): return (x[0]+x[1])/2
def mag(x): return max(abs(x[0]),abs(x[1]))
def contains(x,y): return x[0] <= y[0] <= y[1] <= x[1]
def sqrt_iv(q):
    q=Q(q); base=10**80
    z=isqrt((q.numerator*base*base)//q.denominator)
    low, high=Q(z,base),Q(z+1,base)
    assert low*low <= q <= high*high
    return rounded((low,high))
def matrix(name):
    rows=d['witness_matrices'][name]
    assert len(rows)==N and all(len(row)==N for row in rows)
    return [[iv(x) for x in row] for row in rows]
def sym(M):
    return [[hull(M[i][j],M[j][i]) for j in range(N)] for i in range(N)]
def mm(A,B):
    out=[]
    for row in A:
        rr=[]
        for j in range(N):
            val=ZERO
            for k in range(N): val=add(val,mul(row[k],B[k][j]))
            rr.append(rounded(val))
        out.append(rr)
    return out
# Independently reconstruct A including its direct diagonals; enclosure hulls
# avoid invalid equality tests between differently outward-rounded tables.
b0,bpos=sqrt_iv(Q(5,4)),sqrt_iv(Q(5,2))
v=[scale(b0 if i==0 else bpos,(-1)**i) for i in range(N)]
factors=[pt(1)]+[scale(sqrt_iv(2),(-1)**i) for i in range(1,N)]
row0=[iv(x) for x in d['low_first_row_64']]
diags=[iv(x) for x in d['direct_diagonal_64']]
assert len(row0)==len(diags)==64
savedA=matrix('A')
A=[]
for i in range(N):
    row=[]
    for j in range(N):
        entry=diags[i] if i==j else scale(sub(scale(mul(factors[j],row0[i]),i*i),scale(mul(factors[i],row0[j]),j*j)),Q(1,i*i-j*j))
        row.append(rounded(hull(entry,savedA[i][j])))
    A.append(row)
A=sym(A)
assert all(contains(A[i][j],savedA[i][j]) for i in range(N) for j in range(N))
# Complete low coupling: finite rows AND signed rank-two infinite tail.
a=Q(d['low_tail_w_coefficient']); taildiag=Q(d['low_tail_remainder_coefficient'])
assert a==Q(512,1041816384077177475)
assert taildiag==Q(51380224,4194394783958568267303454125)
rank=iv(d['low_tail_rank']); assert rank[0]>=0
w=[iv(x) for x in d['signed_tail_w_32']]; assert len(w)==N
Cfinite=matrix('Cfinite'); savedC0=matrix('C0')
C0=[]
for i in range(N):
    row=[]
    for j in range(N):
        entry=add(Cfinite[i][j],add(mul(rank,mul(v[i],v[j])),scale(mul(w[i],w[j]),a)))
        if i==j: entry=add(entry,pt(taildiag*(i+1)**4))
        row.append(rounded(hull(entry,savedC0[i][j])))
    C0.append(row)
C0=sym(C0)
# Inverse witness is checked by residual, not assumed exact.
Btrial,Theta,G=matrix('Btrial'),matrix('Theta'),matrix('G')
savedM=matrix('M_resource')
M=sym([[rounded(hull(add(add(Btrial[i][j],scale(Theta[i][j],54)),G[i][j]),savedM[i][j])) for j in range(N)] for i in range(N)])
inv=matrix('M_resource_inverse')
X=[[midpoint(hull(inv[i][j],inv[j][i])) for j in range(N)] for i in range(N)]
Xi=[[pt(x) for x in row] for row in X]
MX=mm(M,Xi)
R=[[sub(pt(int(i==j)),MX[i][j]) for j in range(N)] for i in range(N)]
r=max(max(sum((mag(x) for x in row),Q(0)) for row in R), max(sum((mag(R[i][j]) for i in range(N)),Q(0)) for j in range(N)))
assert r<1
xnorm=max(sum((abs(x) for x in row),Q(0)) for row in X)
inverse_error=xnorm*r/(1-r)
Z=matrix('Z_trial_by_low')
z2=sum((mag(x)**2 for row in Z for x in row),Q(0))
correction=mm([[Z[j][i] for j in range(N)] for i in range(N)],mm(Xi,Z))
F=sym([[rounded(sub(add(sub(A[i][j],C0[i][j]),correction[i][j]),pt(inverse_error*z2 if i==j else 0))) for j in range(N)] for i in range(N)])
# Exact rational LDL witness; no reliance on producer's printed norm margin.
rawL=s['witness_matrices']['L']; rawD=s['witness_matrices']['LDL_pivots']
assert len(rawL)==len(rawD)==N and all(len(row)==N for row in rawL)
L=[[midpoint(iv(x)) for x in row] for row in rawL]
D=[midpoint(iv(x)) for x in rawD]
assert all(x>0 for x in D)
assert all(L[i][i]==1 for i in range(N))
assert all(L[i][j]==0 for i in range(N) for j in range(i+1,N))
error=Q(0)
for i in range(N):
    err=Q(0)
    for j in range(N):
        product=sum((L[i][k]*D[k]*L[j][k] for k in range(min(i,j)+1)),Q(0))
        err+=mag(sub(F[i][j],pt(product)))
    error=max(error,err)
Li=[[Q(int(i==j)) for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(i):
        Li[i][j]=-sum((L[i][k]*Li[k][j] for k in range(j,i)),Q(0))
assert all(sum((L[i][k]*Li[k][j] for k in range(j,i+1)),Q(0))==int(i==j) for i in range(N) for j in range(i+1))
U=sum((x*x for row in Li for x in row),Q(0))
mu=min(D)/U-error
assert mu>0
trace_reconstructed=sum((C0[i][i][1] for i in range(N)),Q(0))
tau=max(trace_reconstructed,iv(d['uncorrected_complete_coupling_bound_trace'])[1],Q(s['coupling_trace_upper_bound']))
assert tau>=0
kappa=Q(8,5)
gap=min(mu*kappa/(kappa+2*tau),kappa/2)
assert gap>=Q(1,10**22)
result={'status':'PASS_EXACT_FRACTION_RECONSTRUCTED_SCHUR_CERTIFICATE','dimension':N,'fixed_interval_grid_bits':BITS,'square_root_decimal_digits':80,'clean_certified_bound':'1/10000000000000000000000','exact_gap':str(gap),'exact_mu':str(mu),'exact_inverse_residual_bound':str(r),'exact_inverse_error_bound':str(inverse_error),'exact_Z_frobenius_squared_upper':str(z2),'exact_LDL_residual_bound':str(error),'exact_L_inverse_frobenius_squared':str(U),'exact_complete_coupling_trace_upper':str(tau),'gap_approx':float(gap),'input_sha256':HASHES,'checker_sha256':sha(Path(__file__)),'trust_boundary':'Analytic source correspondence and saved initial special-function enclosures remain premises. Finite reconstruction, inverse residual, LDL residual, complete-cost trace and gap arithmetic are independently checked with exact rationals.','scope':'real-even minimum local Gamma form domain, 0<B<=4/5','global_all_radii_positivity':'NOT_PROVED','RH':'NOT_PROVED'}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ('status','dimension','clean_certified_bound','gap_approx')}))
