"""Exact rational certificate replay. Run without -O; see README.md."""
import json,hashlib,sys,argparse
from fractions import Fraction as Q
from pathlib import Path
if not __debug__: raise RuntimeError('Do not run with Python -O: assertions are proof checks.')
sys.set_int_max_str_digits(100000)
ap=argparse.ArgumentParser()
ap.add_argument('--data-dir',type=Path,default=Path('data'))
ap.add_argument('--output',type=Path,default=Path('result.json'))
args=ap.parse_args()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
EXPECTED_INPUT_HASHES={'original.json': 'be35a1bfedcbe49e775c4855fe740a846a0d85173a9630c505b60de1f4d0e4b3', 'two_term.json': 'a4bb77f154d8e385f456e53703bba53bc02b639a504e187a469875fab7341f7c', 'success.json': '44db810221f4693d4807f9f3c54f3e746b0bb44ead44f5a9f85a9faba04970db'}
for name,expected in EXPECTED_INPUT_HASHES.items():
 assert sha(args.data_dir/name)==expected
s=json.loads((args.data_dir/'success.json').read_text())
d=json.loads((args.data_dir/'two_term.json').read_text())
o=json.loads((args.data_dir/'original.json').read_text())
assert s['status']=='PASS_INTERVAL_SAVED_TWO_TERM_TAIL_SCHUR_CERTIFICATE'
assert s['saved_gate_sha256']==d['saved_gate_sha256']=='845d571fd58ea4e4d950b481d8f98ce134ba3f7dc1bdc7b12ca7e7280dbb918a'
assert s['input_sha256']==d['input_sha256']==EXPECTED_INPUT_HASHES['original.json']
assert d['original_producer_sha256']==o['verifier_sha256']=='f7288fe5eb238d2e1350fad683c0c4290ba9f4c6fdfb5c891e6457e2c834b00e'
def iv(x):
 a,b=Q(x['lower_rational']),Q(x['upper_rational']);assert a<=b;return a,b
def const(x):return Q(x),Q(x)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def sub(x,y):return add(x,neg(y))
def mul(x,y):
 t=[a*b for a in x for b in y];return min(t),max(t)
def div(x,y):
 assert y[0]>0 or y[1]<0
 return mul(x,(1/y[1],1/y[0]))
def sq(x):return (0 if x[0]<=0<=x[1] else min(x[0]**2,x[1]**2),max(x[0]**2,x[1]**2))
def mid(x):return (x[0]+x[1])/2
def hull(x,y):return min(x[0],y[0]),max(x[1],y[1])
e={k:iv(v) for k,v in d['elementary_enclosures'].items()}
assert e['b0'][0]>0 and e['bpos'][0]>0
assert sq(e['b0'])[0]<=Q(4,3)<=sq(e['b0'])[1]
assert sq(e['bpos'])[0]<=Q(8,3)<=sq(e['bpos'])[1]
E=div(e['exp_minus_3_over_4'],sub(const(1),e['exp_minus_3']))
A=o['witness_matrices']['A'];F=o['witness_matrices']['Ffull'];scalar=iv(o['low_tail_scalar']);n=32
assert d['matrix_size']==n and len(s['LDL_pivots'])==n
w=[]
for m in range(n):
 saved_a=iv(d['saved_actual_A_first_row'][m]); original_a=iv(A[0][m])
 assert saved_a[0]<=original_a[0]<=original_a[1]<=saved_a[1]
 v=mul(e['b0'] if m==0 else e['bpos'],const((-1)**m))
 km=mul(e['pi'],const(Q(4*m,3)))
 wi=sub(mul(v,sub(mul(const(4),sq(e['sinh_3_over_8'])),E)),div(mul(sq(km),iv(A[0][m])),e['b0']))
 w.append(hull(wi,iv(d['signed_tail_vector_w'][m])))
a=Q(d['tail_rank_w_coefficient']);dd=Q(d['tail_diagonal_coefficient'])
assert a==Q(5,12347453440914696) and dd==Q(1225,138087071076825292750731)
Fi=[]
for i in range(n):
 row=[]
 for j in range(n):
  v=sub(iv(F[i][j]),mul(const(a),sq(w[i]) if i==j else mul(w[i],w[j])))
  if i==j:v=add(v,sub(scalar,const(dd*(i+1)**4)))
  row.append(hull(v,iv(d['F_two_term'][i][j])))
 Fi.append(row)
for i in range(n):
 for j in range(i):Fi[i][j]=Fi[j][i]=hull(Fi[i][j],Fi[j][i])
L=[[mid(iv(v)) for v in row] for row in s['L']]
D=[mid(iv(v)) for v in s['LDL_pivots']]
assert all(iv(v)[0]>0 for v in s['LDL_pivots'])
assert all(L[i][i]==1 for i in range(n)) and all(L[i][j]==0 for i in range(n) for j in range(i+1,n))
delta=Q(0)
for i in range(n):
 rowerr=Q(0)
 for j in range(n):
  r=sum((L[i][k]*D[k]*L[j][k] for k in range(min(i,j)+1)),Q(0))
  lo,hi=Fi[i][j];rowerr+=abs((lo+hi)/2-r)+(hi-lo)/2
 delta=max(delta,rowerr)
Li=[[Q(int(i==j)) for j in range(n)] for i in range(n)]
for i in range(n):
 for j in range(i):Li[i][j]=-sum((L[i][k]*Li[k][j] for k in range(j,i)),Q(0))
assert all(sum((L[i][k]*Li[k][j] for k in range(n)),Q(0))==int(i==j) for i in range(n) for j in range(n))
norm=sum((x*x for row in Li for x in row),Q(0))
mu=min(D)/norm-delta
assert mu>0
oldtrace=iv(o['uncorrected_complete_coupling_bound_trace'])[1]
tau_needed=oldtrace+a*sum((sq(x)[1] for x in w),Q(0))+dd*sum((i+1)**4 for i in range(n))
tau_saved=Q(s['safe_complete_coupling_trace_upper_bound']);tau=max(tau_saved,tau_needed)
k=Q(8,5);assert Q(s['high_block_floor'])==k
gap=min(mu*k/(k+2*tau),k/2)
assert gap>=Q(1,10**20)
assert Q(s['q_lower_bound_L2'])>=Q(1,10**20)
result={'status':'PASS_EXACT_FRACTION_INDEPENDENT_CERTIFICATE','dimension':n,'positive_pivots':32,'independently_enclosed_matrix':True,'exact_residual_row_bound':str(delta),'exact_inverse_frobenius_squared':str(norm),'exact_mu':str(mu),'exact_safe_trace':str(tau),'exact_gap':str(gap),'clean_certified_bound':'1/100000000000000000000','mu_approx':float(mu),'gap_approx':float(gap),'tau_saved_suffices_for_independent_w':tau_saved>=tau_needed,'hashes':EXPECTED_INPUT_HASHES,'trust_boundary':'Saved elementary transcendental and original matrix interval enclosures inherited; algebra, interval operations, inverse, residual and coercivity checked independently using Fraction. Analytic dependency audit separate.','RH_proved':False}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','positive_pivots','mu_approx','gap_approx','clean_certified_bound','tau_saved_suffices_for_independent_w']}))
