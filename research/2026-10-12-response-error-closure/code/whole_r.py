"""Whole-R replay with same-buffer two-pass binding and a complete error ledger.

Pure math/serialization definitions. Actual center replay requires separate
admission and a frozen source model stream; this stage runs fixtures only.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from shared_jet import I,Jet,Coordinate,prefix_taylor,physical_affine,EDGES,DIMS
from center_replay import replay_prefix_taylor

class Reject(ValueError):pass
REQUIRED_TERMS=('coefficient_and_rounding','geometry_parameter','fhat_taylor',
    'low_taylor','Gamma_saved_box','parameter_input','product_truncation',
    'remainder_cross','response_central_residual','global_chi_all_errors',
    'endpoint_form','endpoint_response','whole_pole_cross','midpoint_drift')
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canon(x)).hexdigest()
def merge(a,b):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}
def scaled(a,s):return {k:v*abs(F(s)) for k,v in a.items() if v*abs(F(s))}
def box_data(b):return [str(b.lo),str(b.hi)]

@dataclass(frozen=True)
class Scalar:
    center:F
    errors:dict
    def __post_init__(self):
        object.__setattr__(self,'center',F(self.center))
        object.__setattr__(self,'errors',{k:F(v) for k,v in self.errors.items() if F(v)})
        if any(x<0 for x in self.errors.values()):raise Reject('negative error payment')
    @classmethod
    def box(cls,b,tag):
        b=I.of(b);return cls(b.mid(),{tag:b.rad()})
    @property
    def radius(self):return sum(self.errors.values(),F(0))
    @property
    def interval(self):return I(self.center-self.radius,self.center+self.radius)
    def __add__(self,x):
        if not isinstance(x,Scalar):x=Scalar(x,{})
        return Scalar(self.center+x.center,merge(self.errors,x.errors))
    __radd__=__add__
    def __neg__(self):return Scalar(-self.center,self.errors)
    def __sub__(self,x):return self+-x
    def scale(self,s):return Scalar(self.center*F(s),scaled(self.errors,s))
    def __mul__(self,x):
        if not isinstance(x,Scalar):return self.scale(x)
        errors=merge(scaled(self.errors,x.center),scaled(x.errors,self.center))
        errors=merge(errors,{'remainder_cross':self.radius*x.radius})
        return Scalar(self.center*x.center,errors)
    def data(self):
        return {'interval':box_data(self.interval),'center':str(self.center),
            'radius':str(self.radius),'error_ledger':{k:str(v) for k,v in sorted(self.errors.items())}}

@dataclass(frozen=True)
class TJet:
    coordinate:Coordinate
    coefficients:tuple
    errors:dict
    def __post_init__(self):
        object.__setattr__(self,'coefficients',tuple(map(F,self.coefficients)))
        object.__setattr__(self,'errors',{k:F(v) for k,v in self.errors.items() if F(v)})
        if not self.coefficients or any(x<0 for x in self.errors.values()):raise Reject('invalid tracked jet')
    @property
    def order(self):return len(self.coefficients)-1
    @property
    def radius(self):return sum(self.errors.values(),F(0))
    @property
    def polynomial_mag(self):return sum(map(abs,self.coefficients),F(0))
    @classmethod
    def constant(cls,c,d,s):
        if not isinstance(s,Scalar):s=Scalar(s,{})
        return cls(c,(s.center,)+(F(0),)*d,s.errors)
    @classmethod
    def model(cls,j,tail_tag):
        # Fixed coefficient intervals and source geometry are conservatively
        # paid as uniform error. Their central polynomial keeps the same t.
        errors={'coefficient_and_rounding':sum((x.rad() for x in j.coefficients),F(0)),tail_tag:j.remainder}
        return cls(j.coordinate,tuple(x.mid() for x in j.coefficients),errors)
    def other(self,x):
        if not isinstance(x,TJet):x=TJet.constant(self.coordinate,self.order,x)
        if x.coordinate!=self.coordinate or x.order!=self.order:raise Reject('cross-cell/source/order mixture')
        return x
    def __add__(self,x):
        x=self.other(x);return TJet(self.coordinate,tuple(a+b for a,b in zip(self.coefficients,x.coefficients)),merge(self.errors,x.errors))
    __radd__=__add__
    def __neg__(self):return TJet(self.coordinate,tuple(-x for x in self.coefficients),self.errors)
    def __sub__(self,x):return self+-self.other(x)
    def __mul__(self,x):
        x=self.other(x);d=self.order;conv=[F(0)]*(2*d+1)
        for k,a in enumerate(self.coefficients):
            if not a:continue
            for l,b in enumerate(x.coefficients):
                if b:conv[k+l]+=a*b
        errors=merge(scaled(self.errors,x.polynomial_mag),scaled(x.errors,self.polynomial_mag))
        errors=merge(errors,{'product_truncation':sum(map(abs,conv[d+1:]))})
        for a,av in self.errors.items():
            for b,bv in x.errors.items():
                tag='chi:remainder_cross' if a.startswith('chi:') or b.startswith('chi:') else 'remainder_cross'
                errors=merge(errors,{tag:av*bv})
        return TJet(self.coordinate,tuple(conv[:d+1]),errors)
    __rmul__=__mul__
    def polynomial_range(self):
        result=I.of(self.coefficients[0])
        for k,a in enumerate(self.coefficients[1:],1):result=result+a*(I(-1,1) if k%2 else I(0,1))
        return result
    def interval(self):return self.polynomial_range()+I(-self.radius,self.radius)
    def integral(self,length):
        length=I.of(length)
        if length.lo<=0:raise Reject('positive Jacobian required')
        width=self.coordinate.right-self.coordinate.left
        avg=sum((a/F(k+1) for k,a in enumerate(self.coefficients) if k%2==0),F(0))
        errors=scaled(self.errors,length.mid()*width)
        errors=merge(errors,{'geometry_parameter':length.rad()*width*abs(avg),
                            'remainder_cross':length.rad()*width*self.radius})
        return Scalar(avg*length.mid()*width,errors)

def dot(x,y):
    if not x or len(x)!=len(y):raise Reject('complete dot shape')
    return sum((a*b for a,b in zip(x,y)),TJet.constant(x[0].coordinate,x[0].order,0))
def unpack_model(x,c,d):
    if set(x)!= {'coefficients','remainder'}:raise Reject('model schema')
    if len(x['coefficients'])!=d+1:raise Reject('missing center-jet coefficient')
    return Jet(c,tuple(I.of(v) for v in x['coefficients']),F(x['remainder']))
def pack_model(j):return {'coefficients':[box_data(x) for x in j.coefficients],'remainder':str(j.remainder)}
def pack_model_outward(j,places=240):
    """Bounded decimal serialization without converting huge integers to str.

    Exact rational source formulas may have >4300 digit denominators. Keep
    Python's inherited integer conversion policy unchanged. Flooring and
    ceiling in integer arithmetic prove every serialized inclusion; the
    coefficient widths and enlarged remainder are paid by TJet.model.
    """
    if not 1<=places<=240:raise Reject('bounded decimal serialization places')
    scale=10**places
    def bound(x,up):
        x=F(x);z=x.numerator*scale
        k=-((-z)//x.denominator) if up else z//x.denominator
        sign='-' if k<0 else '';digits=str(abs(k)).zfill(places+1)
        return sign+digits[:-places]+'.'+digits[-places:]
    return {'coefficients':[[bound(x.lo,False),bound(x.hi,True)] for x in j.coefficients],
            'remainder':bound(j.remainder,True)}
def verify_model(got,expected):
    if got.coordinate!=expected.coordinate or got.order!=expected.order:raise Reject('jet coordinate binding')
    if got.remainder<expected.remainder:raise Reject('unpaid strict Taylor remainder')
    for a,b in zip(got.coefficients,expected.coefficients):
        if not a.lo<=b.lo<=b.hi<=a.hi:raise Reject('center coefficient inclusion failure')

def bind_and_replay(row,source,header,allow_actual_centers=False,replay_centers=True):
    if row['source_binding_sha256']!=digest(source):raise Reject('geometry/M/c0/F/E buffer hash mismatch')
    if source['source_context']!=header['source_context']:raise Reject('source context mismatch')
    c=Coordinate(source['source_context'],source['component'],source['cell'],*map(F,source['normalized']))
    d=header['order'];n=DIMS[c.component]
    if source['Gamma_quantity']!='V_full_complete_Rtail':raise Reject('complete Gamma missing')
    if source['prime_edges']!=[list(x) for x in EDGES[c.component]]:raise Reject('prime edge missing')
    if len(source['Gamma_plus'])!=n or len(source['Gamma_minus'])!=n or len(source['saved_c0'])!=n:
        raise Reject('complete vertex or c0 missing')
    if len(source['offsets'])!=n or len(source['slopes'])!=n:raise Reject('shared geometry missing')
    if header['source_kind']=='actual' and not allow_actual_centers:
        raise Reject('ACTUAL_CENTER_REPLAY_REQUIRES_NEW_SOURCE_ADMISSION')
    f=[];E=[]
    if len(row['fhat'])!=n or len(row['E'])!=n:raise Reject('all source vertices')
    for v in range(n):
        jf=unpack_model(row['fhat'][v],c,d)
        if replay_centers:
            ef=replay_prefix_taylor(c,d,header['physical_fhat_coefficients'],I.of(source['offsets'][v]),I.of(source['slopes'][v]))
            verify_model(jf,ef)
        f.append(TJet.model(jf,'fhat_taylor'))
        if len(row['E'][v])!=16:raise Reject('complete low16')
        low=[]
        for j in range(16):
            je=unpack_model(row['E'][v][j],c,d)
            if replay_centers:
                ee=replay_prefix_taylor(c,d,{2*j:I.of(header['physical_low_factors'][j])},I.of(source['offsets'][v]),I.of(source['slopes'][v]))
                verify_model(je,ee)
            low.append(TJet.model(je,'low_taylor'))
        E.append(low)
    q=header['parameters'];a=I.of(q['a']);const=lambda x,tag='parameter_input':TJet.constant(c,d,Scalar.box(x,tag))
    if a.lo<=0:raise Reject('coercivity lower absent')
    M=[[const(0) for _ in range(n)] for _ in range(n)]
    for v in range(n):
        # Entire saved Gamma uncertainty is variable, so no odd cancellation.
        gamma=const(source['Gamma_plus'][v],'Gamma_saved_box')+const(source['Gamma_minus'][v],'Gamma_saved_box')
        M[v][v]=const(q['a'])+const(q['kappa'])+const(q['omega'])*gamma
    for u,v,key in EDGES[c.component]:M[u][v]=M[v][u]=-const(q[key])
    if header['source_kind']=='synthetic':
        lower=min(M[v][v].interval().lo-sum((M[v][w].interval().mag() for w in range(n) if w!=v),F(0)) for v in range(n))
        if lower<a.lo:raise Reject('synthetic coercivity failure')
    elif header.get('coercivity_premise_sha256')!=source.get('coercivity_premise_sha256'):
        raise Reject('original conditional coercivity binding missing')
    g=[const(q['a'])*f[v]-dot(E[v],[const(x) for x in q['alpha']]) for v in range(n)]
    centers=[TJet.constant(c,d,F(x)) for x in source['saved_c0']]
    residual=[g[v]-dot(M[v],centers) for v in range(n)]
    paid={'response_central_residual':sum((x.polynomial_range().mag() for x in residual),F(0))/a.lo}
    for x in residual:
        paid=merge(paid,{'response:'+tag:value/a.lo for tag,value in x.errors.items()})
    response=[TJet(c,x.coefficients,paid) for x in centers]
    Mf=[dot(r,f) for r in M]
    return {'coordinate':c,'length':source['length'],'fhat':f,'E':E,'M':M,'g':g,
        'residual':residual,'response':response,'response_error_ledger':paid,
        'chi':[dot([r[j] for r in E],Mf) for j in range(16)],'Ag':dot(f,Mf)}

def category_ledger(s,drift):
    ledger={tag:F(0) for tag in REQUIRED_TERMS}
    for tag,value in s.errors.items():
        if tag.startswith('chi:'):ledger['global_chi_all_errors']+=value
        else:
            base=tag.removeprefix('response:')
            if base in ledger:ledger[base]+=value
            else:raise Reject('unclassified error term '+tag)
    ledger['whole_pole_cross']=sum((v for tag,v in s.errors.items() if tag.startswith('pole:')),F(0)) if any(x.startswith('pole:') for x in s.errors) else ledger['whole_pole_cross']
    ledger['midpoint_drift']=F(drift) # audit-only, not counted twice in radius.
    return {tag:str(value) for tag,value in ledger.items()}

def whole_r(header,stream_factory,reference_center,reported=None,allow_actual_centers=False):
    header_sha=digest(header)
    if set(header['covered_error_terms'])!=set(REQUIRED_TERMS):raise Reject('whole-R residual error categories omitted')
    if not 0<=header['order']<=128 or len(header['physical_low_factors'])!=16:raise Reject('source degree/low factors')
    if len(header['parameters']['alpha'])!=16:raise Reject('fixed alpha16')
    expected=header['counts'];counts={c:0 for c in expected};last={c:F(header['cutoff']) for c in expected}
    for key in ('endpoint_form','endpoint_response_source'):
        endpoints=header[key]
        if len(endpoints)!=len(expected) or {e['component'] for e in endpoints}!=set(expected):
            raise Reject('complete endpoint component coverage missing')
    form_eps={e['component']:e for e in header['endpoint_form']}
    for ep in header['endpoint_form']:
        if (len(ep['chi'])!=16 or len(ep['E0'])!=16 or ep['source_context']!=header['source_context']
            or ep.get('strips')!=2 or ep.get('all_vertices') is not True
            or ep.get('Gamma_integral')!='complete_Rtail_log_integral_upper'):
            raise Reject('full endpoint/source inclusion certificate missing')
    for ep in header['endpoint_response_source']:
        form=form_eps[ep['component']]
        if any(ep[k]!=form[k] for k in ('epsilon','G0','E0')):
            raise Reject('endpoint response/form source mismatch')
        if I.of(ep['epsilon']).lo<=0 or len(ep['E0'])!=16:raise Reject('endpoint norm domain')
    chi=[Scalar(0,{}) for _ in range(16)];Ag=Scalar(0,{});beta=[Scalar(0,{}) for _ in range(16)]
    first=hashlib.sha256();second=hashlib.sha256();cell_reports=[]
    for row,source in stream_factory():
        first.update(canon([row,source]));model=bind_and_replay(row,source,header,allow_actual_centers)
        c=model['coordinate'];name=c.component
        if name not in counts or c.cell!=counts[name] or c.left!=last[name]:raise Reject('whole native partition gap/duplicate')
        last[name]=c.right;counts[name]+=1
        for j in range(16):chi[j]=chi[j]+model['chi'][j].integral(model['length'])
        Ag=Ag+model['Ag'].integral(model['length'])
        cell_reports.append({'component':name,'cell':c.cell,
            'response_error_ledger':{k:str(v) for k,v in model['response_error_ledger'].items()}})
    if counts!=expected or any(x!=1-F(header['cutoff']) for x in last.values()):raise Reject('incomplete whole source coverage')
    for ep in header['endpoint_form']:
        for j,x in enumerate(ep['chi']):chi[j]=chi[j]+Scalar.box(x,'endpoint_form')
        Ag=Ag+Scalar.box(ep['Ag'],'endpoint_form')
    chi_sha=digest([x.data() for x in chi]);weighted=Scalar(0,{})
    for row,source in stream_factory():
        second.update(canon([row,source]));model=bind_and_replay(row,source,header,allow_actual_centers,replay_centers=False)
        c=model['coordinate'];d=header['order']
        # Only the newly accumulated full chi participates; every chi error
        # tag is carried into the single weighted target before integration.
        chi_jets=[TJet.constant(c,d,Scalar(x.center,{'chi:'+tag:value for tag,value in x.errors.items()})) for x in chi]
        Echi=[dot(r,chi_jets) for r in model['E']]
        w=dot(model['response'],Echi)
        weighted=weighted+w.integral(model['length'])
        for j in range(16):beta[j]=beta[j]+dot([r[j] for r in model['E']],model['response']).integral(model['length'])
    if first.hexdigest()!=second.hexdigest():raise Reject('source/model stream changed between chi and R pass')
    if digest(header)!=header_sha:raise Reject('parameters or endpoint header changed between passes')
    for ep in header['endpoint_response_source']:
        eps=I.of(ep['epsilon']);G0=I.of(ep['G0']);a=I.of(header['parameters']['a']);E0=list(map(I.of,ep['E0']))
        for j,x in enumerate(E0):
            b=(2*eps*G0/a*x).hi;beta[j]=beta[j]+Scalar(0,{'endpoint_response':b})
        b=(2*eps*G0/a*sum((x*y.interval.mag() for x,y in zip(E0,chi)),I.of(0))).hi
        weighted=weighted+Scalar(0,{'endpoint_response':b})
    sigma=Scalar.box(header['sigma'],'whole_pole_cross');ell=Scalar.box(header['ell'],'whole_pole_cross')
    pole=sigma*ell
    # Keep every signed whole-pole uncertainty, including its mixed product,
    # in its own paid category even when both central values happen to be 0.
    pole=Scalar(pole.center,{'whole_pole_cross':pole.radius})
    R=weighted-pole.scale(2)
    Hraw=Ag.interval+2*I.of(header['ell']).square();H=I(max(F(header['H_lower']),Hraw.lo),Hraw.hi)
    if H.lo<=0:raise Reject('full H/coercivity not positive')
    drift=abs(R.center-F(reference_center));ledger=category_ledger(R,drift)
    # All categories except midpoint audit sum exactly to the certified R radius.
    if sum((F(v) for k,v in ledger.items() if k!='midpoint_drift'),F(0))!=R.radius:raise Reject('unpaid full radius')
    out={'status':'PASS_WHOLE_R_INCLUSION_CONDITIONAL_SOURCE','source_kind':header['source_kind'],
        'counts':counts,'same_buffer_two_pass_sha256':first.hexdigest(),'full_chi_sha256':chi_sha,
        'chi':[x.data() for x in chi],'Ag':Ag.data(),'beta':[x.data() for x in beta],
        'weighted_R':weighted.data(),'R':R.data(),'H':box_data(H),
        'all_error_term_upper_bounds':ledger,'reference_center':str(reference_center),
        'midpoint_drift_exact':str(drift),'reference_center_displacement_upper':str(drift+R.radius),
        'direct_sign_separated':not R.interval.lo<=0<=R.interval.hi,
        'scientific_status':'HOLD_RESIDUAL_ZERO_AMBIGUITY' if R.interval.lo<=0<=R.interval.hi else 'SOURCE_PACKET_SIGN_SEPARATED_ONLY',
        'global_pole_square_count':1,'whole_signed_pole_cross_count':1,
        'Jacobian_count_per_cell':1,'new_coefficient_s0':False,'new_Psi':False,
        'numeric_count':11,'production_admission':False,'cell_residual_error_bounds':cell_reports}
    if reported is not None:
        if set(reported['all_error_term_upper_bounds'])!=set(REQUIRED_TERMS):raise Reject('reported residual error term missing')
        for k,value in ledger.items():
            if F(reported['all_error_term_upper_bounds'][k])<F(value):raise Reject('underpaid whole-R term '+k)
        rr=F(reported['R']['radius']);rc=F(reported['R']['center'])
        if rr<R.radius:raise Reject('reported full R radius underpaid')
        if rc!=R.center:raise Reject('reported midpoint differs from coupled whole-R replay')
        total=sum((F(v) for k,v in reported['all_error_term_upper_bounds'].items() if k!='midpoint_drift'),F(0))
        if total!=rr:raise Reject('reported whole-R ledger sum differs from reported radius')
        rep=I.of(reported['R']['interval'])
        if not rep.lo<=R.interval.lo<=R.interval.hi<=rep.hi:raise Reject('partial budget promoted to full R radius')
        if not rep.lo<=rc-rr<=rc+rr<=rep.hi:raise Reject('reported R interval and midpoint/radius disagree')
        if reported['full_chi_sha256']!=chi_sha:raise Reject('residual used stale chi packet')
    return out
