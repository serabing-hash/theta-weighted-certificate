"""Source-free independent audit: only generic rational unit roots, no Work production import."""
import ast, hashlib, importlib.util, json, pathlib, sys
from fractions import Fraction as F
BASE=pathlib.Path('/workspace/shared/phase_gate_audit_20261008')
ART=BASE/'work_artifacts/v2_j2_local_20261008'
OUT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ART/'runtime_deps'))
import flint
from flint import arb,acb,fmpq,ctx
ctx.prec=160;ctx.threads=1

def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
# Extract only side-effect-free support helper definitions, without importing Work modules.
src=ART/'code/v2_support.py';tree=ast.parse(src.read_text())
names={'aa','exact','upper','pad','quantize','rec','restore'}
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
assert {n.name for n in funcs}==names
ns={'arb':arb,'fmpq':fmpq,'F':F}
exec(compile(ast.Module(body=funcs,type_ignores=[]),str(src),'exec'),ns)
exact,rec,restore=ns['exact'],ns['rec'],ns['restore']
candidate=BASE/'centered_disc_candidate.py'
spec=importlib.util.spec_from_file_location('review_candidate',candidate);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def endpoints(x):
 assert x.is_finite()
 m,r=exact(x.mid()),exact(x.rad())
 return m-r,m+r

def check_record(x,bits=140):
 c,r=map(int,rec(x,bits));lo,hi=endpoints(x)
 assert F(c-r,1<<bits)<=lo and hi<=F(c+r,1<<bits)
 rehydrated=restore([c,r],bits);rlo,rhi=endpoints(rehydrated)
 assert rlo<=lo and hi<=rhi
 return [str(c),str(r)]

records=[]
for c,r in [(0,0),(1,0),(-1,0),(0,3),(7,2),(-7,2),(1,7),(-1,7)]:
 x=arb((c,-142),(r,-139));records.append({'input_center':c,'input_radius':r,'record':check_record(x)})
for sign in (-1,1):
 x=arb(fmpq(sign,3));records.append({'rational':str(F(sign,3)),'record':check_record(x)})

roots=[(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1)),(F(3,5),F(4,5)),(F(3,5),F(-4,5)),(F(-3,5),F(4,5)),(F(-3,5),F(-4,5))]
runs=[]
for a,b in roots:
 assert a*a+b*b==1
 R=acb(arb(fmpq(a.numerator,a.denominator)),arb(fmpq(b.numerator,b.denominator)))
 for rr,target in [(R.real,a),(R.imag,b)]:
  lo,hi=endpoints(rr);assert lo<=target<=hi
 q,E=module.initial_state();real,imag=F(1),F(0);assert q.is_exact() and q==1 and E==0
 for k in range(1,130):
  oldq,oldE=q,E;P=oldq*R
  q,E,cosine,local=module.step_exact_unit_phase(q,E,R,rec)
  cr,rr,ci,ri=local
  assert E==oldE+rr+ri and E>=oldE
  assert exact(q.real)==F(cr,1<<140) and exact(q.imag)==F(ci,1<<140)
  for coord,c,r in [(P.real,cr,rr),(P.imag,ci,ri)]:
   lo,hi=endpoints(coord);assert F(c-r,1<<140)<=lo and hi<=F(c+r,1<<140)
  real,imag=real*a-imag*b,real*b+imag*a
  assert (real-exact(q.real))**2+(imag-exact(q.imag))**2 <= F(E,1<<140)**2
  lo,hi=endpoints(cosine);assert lo<=real<=hi
  assert lo<=F(cr-E,1<<140) and F(cr+E,1<<140)<=hi
  check_record(cosine)
  assert q.is_exact() and q.is_finite() and ctx.prec==160
 runs.append({'root':[str(a),str(b)],'steps':129,'terminal_E_numerator':E,'all_exact_euclidean_checks':True,'all_cosine_and_serialized_full_enclosures':True})

# Full-ball bounds for strict absolute gate, including negative and straddling cases.
gate_cases=[]
for value,expected in [(arb(-41),True),(arb(41),True),(arb(-42),False),(arb(42),False),(arb(0,42),False),(arb(-41,2),False)]:
 accepted=bool(value.is_finite() and ns['upper'](value)<42)
 assert accepted==expected;gate_cases.append({'input':str(value),'expected':expected,'observed':accepted})

# Interval weights: two arbitrary rational roots/weights and signed DC constant.
weighted=[]
for k in range(0,17):
 D=arb(fmpq(-7,3));target=F(-7,3)
 for (a,b),w in [(roots[4],F(5,7)),(roots[6],F(2,9))]:
  q,E=module.initial_state();cosine=arb(1);real,imag=F(1),F(0)
  R=acb(arb(fmpq(a.numerator,a.denominator)),arb(fmpq(b.numerator,b.denominator)))
  W=arb(fmpq(w.numerator,w.denominator))
  for _ in range(k):
   q,E,cosine,_=module.step_exact_unit_phase(q,E,R,rec)
   real,imag=real*a-imag*b,real*b+imag*a
  D+=2*W*cosine;target+=2*w*real
 lo,hi=endpoints(D);assert lo<=target<=hi
 weighted.append({'k':k,'target':str(target),'record':check_record(D)})

result={'status':'PASS-GENERIC-NATIVE-ONLY','runtime':'copied Work runtime binary, local audit executor; Work-native preflight still required','python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,'precision_bits':ctx.prec,'threads':ctx.threads,'support_sha256':sha(src),'candidate_sha256':sha(candidate),'helper_functions':sorted(names),'unit_root_runs':runs,'serialization_cases':records,'strict_abs_gate':gate_cases,'weighted_sum_fixtures':weighted,'actual_prime_phase_evaluations':0,'new_Gamma_evaluations':0,'H_actions':0,'DFTs':0,'physical_integrals':0}
(OUT/'NATIVE_GENERIC_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['unit_root_runs','serialization_cases','strict_abs_gate','weighted_sum_fixtures']},indent=2))
