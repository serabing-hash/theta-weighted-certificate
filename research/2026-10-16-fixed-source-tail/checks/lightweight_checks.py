#!/usr/bin/env python3
"""Read-only scalar, primitive, and saved-output checks. Does NOT run source-tail main."""
from pathlib import Path
from fractions import Fraction as Q
import ast, hashlib, json, math
B=Path(__file__).resolve().parents[1]/'source_tail_M128'
R=json.loads((B/'run/result.json').read_text()); D=json.loads((B/'input.json').read_text())
S=10**120
checks=[]
def ok(name,cond):
    assert cond,name
    checks.append(name)
def cd(a,b): return -((-a)//b)
def rec(x):
    a,b=Q(x['lower'])*S,Q(x['upper'])*S
    assert a.denominator==b.denominator==1
    assert a<=b and Q(x['width'])*S==b-a
    return int(a),int(b)
def add(a,b): return a[0]+b[0],a[1]+b[1]
def sub(a,b): return a[0]-b[1],a[1]-b[0]
def mul(a,b):
    p=[x*y for x in a for y in b]
    return min(p)//S,cd(max(p),S)
def square(a):
    l=0 if a[0]<=0<=a[1] else min(x*x for x in a)
    return l//S,cd(max(x*x for x in a),S)
def root(a):
    l,h=math.isqrt(a[0]*S),math.isqrt(a[1]*S)
    return l,h+(h*h<a[1]*S)
def div(a,b):
    assert not b[0]<=0<=b[1]
    p=[Q(x*S,y) for x in a for y in b]
    l,h=min(p),max(p)
    return l.numerator//l.denominator,cd(h.numerator,h.denominator)
def rational(x): return x.numerator*S//x.denominator,cd(x.numerator*S,x.denominator)
def point_upper(a): return a[1],a[1]
# Exact request and source-data binding only.
req=(B/'request.txt').read_text(); raw=req[req.index('{\n  "B"'):]
ok('input JSON is byte-exact requested JSON',raw==(B/'input.json').read_text())
source=Path(__file__).resolve().parents[1]/'sources'
design=json.loads((source/'DESIGN.extract.json').read_text()); witness=json.loads((source/'EXACT_FIXED_DIRECTION.extract.json').read_text())
ok('all 16 frozen witness numerators match published source extract',D['hA_grid_numerators']==witness['witness_integer_numerators_grid40'])
ok('frozen H_A matches published source extract',Q(D['H_A'])==Q(witness['norm_squared']))
ok('all inherited constant boxes match DESIGN extract',all(D['constant_intervals'][n]==design['reference_box'][n] for n in D['constant_intervals']) and D['pi_interval']==design['pi_interval'])
ok('Ek and th match original DESIGN',Q(D['Ek'])==Q(design['kernel_error']) and Q(D['th'])==Q(design['pole_high_tail']))
# Independent H_A identity directly in the (1-t^2)^r basis: E0[(1-t^2)^j] = 2^(2j) (j!)^2/(2j+1)!.
z=[Q(n,int(D['hA_grid_denominator'])) for n in D['hA_grid_numerators']]
h=sum((z[i]*z[j]*Q(2**(2*(i+j))*math.factorial(i+j)**2,math.factorial(2*(i+j)+1)) for i in range(16) for j in range(16)),Q(0))
ok('H_A exact alternate beta-moment identity',h==Q(D['H_A']))
# Scalar remainders, not source-tail integration.
u=v=None
U,V=[Q(1)],[Q(1)]
for n in range(1,49):
    U.append(-sum((U[n-j]/math.factorial(2*j+1) for j in range(1,n+1)),Q(0)))
    V.append(-sum((V[n-j]/math.factorial(2*j) for j in range(1,n+1)),Q(0)))
q=Q(3,4)
def tail(j,e): return q**(2*j)/math.factorial(2*j+e)/(1-q*q/((2*j+e+1)*(2*j+e+2)))
ek=sum((q**(2*n)*(abs(U[n])*tail(49-n,1)/q+abs(V[n])*tail(49-n,0))/4 for n in range(49)),Q(0))
th=Q(3,8)**32/math.factorial(32)/(1-Q(3,8)**2/(33*34))
ok('Ek exact recurrence scalar identity',ek==Q(D['Ek']))
ok('th exact complete factorial-tail scalar identity',th==Q(D['th']))
# Execute ONLY isolated arithmetic class/functions from AST. No imports, cap setup, main, moments, integration, or tail evaluation from source.
tree=ast.parse((B/'certify_tail.py').read_text())
keep=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in {'ceildiv','I','ArithmeticHold'}]
ns={'SCALE':S,'STATS':{'interval_operations':0},'math':math}
exec(compile(ast.Module(body=keep,type_ignores=[]),'<isolated interval primitives>','exec'),ns)
I=ns['I']
cases=[(-3*S,-2*S),(-3*S,2*S),(-S,-S),(-1,1),(0,0),(0,1),(1,2),(S,S),(S,2*S),(3*S+1,4*S+7)]
for a in cases:
    ia=I(*a)
    ok('primitive square %s'%(a,), (ia.square().lo,ia.square().hi)==square(a))
    if a[0]>=0:
        rt=ia.sqrt()
        ok('primitive sqrt %s'%(a,),rt.lo*rt.lo<=a[0]*S and rt.hi*rt.hi>=a[1]*S and (rt.lo+1)**2>a[0]*S and (rt.hi==0 or (rt.hi-1)**2<a[1]*S))
    for b in cases:
        ib=I(*b); im=ia*ib
        ok('primitive multiply %s %s'%(a,b),(im.lo,im.hi)==mul(a,b))
        if not b[0]<=0<=b[1]:
            ix=ia/ib
            ok('primitive divide %s %s'%(a,b),(ix.lo,ix.hi)==div(a,b))
# Saved result arithmetic, not recalculation of any integral or source moment.
record_count=0
def walk(x):
    global record_count
    if isinstance(x,dict):
        if {'lower','upper','width'}<=x.keys(): rec(x); record_count+=1
        else:
            for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
walk(R)
ok('all saved interval endpoints and widths are on exact grid',record_count>250)
expected=list(range(0,129,2))
ok('all 65 removed even modes including low16',R['removed_even_modes']==expected)
for letter in 'WS':
    rows=R[letter+'_modes']
    ok(letter+' saved modes complete and ordered',[x['m'] for x in rows]==expected)
    total=(0,0)
    for row in rows:
        a=rec(row['E0_Pm_u'+letter]); sq=square(a)
        c=((2*row['m']+1)*sq[0],(2*row['m']+1)*sq[1])
        ok(letter+' mode %d stored squared coefficient'%row['m'],rec(row['squared_coefficient'])==c)
        total=add(total,c)
    ok(letter+' saved prefix is exact sum of 65 squared intervals',rec(R['P_'+letter])==total)
    diff=sub(rec(R['N_'+letter]),total)
    ok(letter+' tail uses total upper minus prefix lower',rec(R['tail_'+letter+'_squared_enclosure'])==diff and rec(R['U_'+letter])==(diff[1],diff[1]) and diff[1]>=0)
    ok(letter+' y upper is outward sqrt of U',rec(R['y_'+letter+'_upper'])==point_upper(root(rec(R['U_'+letter]))))
pairs=R['shift_pairs']; names=['2-','2+','3-','3+','4-','4+']
expected_pairs=[(names[i],names[j],1 if i==j else 2) for i in range(6) for j in range(i,6)]
ok('all 21 shift pairs with 36 ordered-term multiplicity',[(x['i'],x['j'],x['multiplicity']) for x in pairs]==expected_pairs and sum(x['multiplicity'] for x in pairs)==36)
ok('n=2 overlap recorded nonempty',next(x for x in pairs if (x['i'],x['j'])==('2-','2+'))['nonempty_intersection'])
nsum=(0,0)
for pair in pairs: nsum=add(nsum,rec(pair['contribution']))
ok('N_S equals sum of all stored cross-term enclosures',nsum==rec(R['N_S']))
ok('sqrt H saved interval',rec(R['sqrt_H_A'])==root(rec(R['H_A'])))
epar=4*(Q(23,10**48)+Q(20700,10**96))+Q(26,10**96)
ok('epar saved exact value',rec(R['e_par'])==rational(epar))
eop=add(add(rational(epar),div(mul(rational(ek),(3*S,3*S)),(2*S,2*S))),div(mul(rational(th),(9*S,9*S)),(2*S,2*S)))
ok('eop includes full kernel plus pole exactly once',rec(R['e_op'])==eop)
yrem=point_upper(mul(eop,rec(R['sqrt_H_A'])))
ok('remainder saved upper',rec(R['y_remainder_upper'])==yrem)
ycert=add(add(rec(R['y_W_upper']),rec(R['y_S_upper'])),yrem)
crude=mul(add((28*S,28*S),eop),rec(R['sqrt_H_A']))
ok('y_certificate sum of norm upper constants',rec(R['y_certificate'])==ycert)
ok('Y_crude has norm units and correct saved endpoints',rec(R['Y_crude'])==crude)
ok('saved ratio is outward division of certificate by crude',rec(R['certificate_over_crude'])==div(ycert,crude))
ok('saved gap arithmetic',rec(R['crude_minus_certificate'])==sub(crude,ycert))
ok('strict reduction upper below lower',ycert[1]<crude[0])
ok('complete with Schur explicitly unevaluated',R['arithmetic_status']=='COMPLETE' and R['schur_status']=='NOT EVALUATED / HOLD')
print('PASS:',len(checks),'lightweight checks;',record_count,'stored interval records validated.')
print('No source-tail main, integrals, source moments, response, or quadrature executed.')
print('Exact scalar identities: H_A via alternate beta moments; Ek recurrence; th remainder.')
print('65+65 mode squares and prefix sums, 21 shift-pair norm sum, tails, sqrt bounds, eop, remainder, certificate, crude, ratio all consistent.')
for letter in 'WS':
    rr=R['tail_'+letter+'_squared_enclosure']; width=Q(rr['width']); hi=Q(rr['upper'])
    print(letter+' tail enclosure width = %.8e; relative to upper = %.8e'%(float(width),float(width/hi)))
print('Nonempty shift pairs:',sum(x['nonempty_intersection'] for x in pairs),'of 21')
print('Primitive checks:',ns['STATS']['interval_operations'],'isolated test operations; not a source computation.')
