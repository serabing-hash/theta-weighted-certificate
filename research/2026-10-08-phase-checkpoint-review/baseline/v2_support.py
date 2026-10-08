"""CC BY-NC 4.0. Fixed V2 j=2 support; no physical work at import."""
import csv, gc, hashlib, json, math, os, pathlib, re, resource, struct, time
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/'original'
CONTRACT=ORIGINAL/'residual_action_contract_20261008'
ADM=ORIGINAL/'residual_block_admission_20261007'
REL=ORIGINAL/'theta_delta32_release_20261007/replay/restored_full'
OLD=ROOT/'inherited_runtime/A_action/SERABI_RH_FIXED_RANK32_ACTION_2026-10-07'
FULL=ROOT/'inherited_runtime/A/SERABI_RH_FIXED_RANK32_FULL372_2026-10-07'
DIAG=ORIGINAL/'delta64_failure_diagnosis_20261007'
OUT=ROOT/'pilot'; CODE=ROOT/'code'
K=8192; MSTAR=24804; KOLD=32996; KH=41188; M=131072; NODES=3912; CHUNK=128; COLUMN=2; PREC=160
PRIME_PAIRS=((2,2),(3,3),(4,2),(5,5),(7,7),(8,2),(9,3),(11,11),(13,13),(16,2),(17,17),(19,19),(23,23),(25,5),(27,3),(29,29),(31,31),(32,2))
COUNTS={}; START=None; PHASE='not-started'
def sha(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open('rb') as f:
        while b:=f.read(1024*1024): h.update(b)
    return h.hexdigest()
def save(path,obj):
    path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.partial')
    with tmp.open('w') as f:json.dump(obj,f,separators=(',',':'));f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def metadata(path):
    """Scan top-level object without retaining coefficient/record arrays."""
    result={}
    parser=Stream(path)
    parser.take('{')
    while parser.peek()!='}':
        key=parser.value();parser.take(':')
        if parser.peek()=='[' and key not in ('support','shape','column_indices'):
            for _ in parser.array():pass
        else:result[key]=parser.value()
        if parser.peek()==',':parser.take(',')
        else:break
    parser.take('}');parser.close();return result
class Stream:
    def __init__(self,path):self.f=pathlib.Path(path).open();self.buf='';self.eof=False;self.decoder=json.JSONDecoder()
    def fill(self):
        if self.eof:raise ValueError('Unexpected EOF in JSON')
        block=self.f.read(65536);self.eof=not block;self.buf+=block
    def ws(self):
        self.buf=self.buf.lstrip()
        while not self.buf and not self.eof:self.fill();self.buf=self.buf.lstrip()
    def peek(self):self.ws();return self.buf[0] if self.buf else ''
    def take(self,ch):self.ws();assert self.buf.startswith(ch),(ch,self.buf[:20]);self.buf=self.buf[len(ch):]
    def value(self):
        self.ws()
        while True:
            try:
                value,end=self.decoder.raw_decode(self.buf)
                if end==len(self.buf) and not self.eof:self.fill();continue
                # A bare integer at a read boundary may otherwise be silently truncated.
                if isinstance(value,(int,float)) and end<len(self.buf) and self.buf[end] not in ',]} \t\r\n':
                    if self.eof:raise ValueError('invalid numeric token')
                    self.fill();continue
                break
            except json.JSONDecodeError:
                if self.eof:raise
                self.fill()
        self.buf=self.buf[end:];return value
    def array(self):
        self.take('[')
        while self.peek()!=']':
            yield self.value()
            if self.peek()==',':self.take(',')
            else:break
        self.take(']')
    def close(self):self.f.close()
def iter_array(path,key):
    parser=Stream(path);parser.take('{')
    try:
        while parser.peek()!='}':
            name=parser.value();parser.take(':')
            if name==key:yield from parser.array();return
            if parser.peek()=='[':
                for _ in parser.array():pass
            else:parser.value()
            if parser.peek()==',':parser.take(',')
            else:break
        raise KeyError(key)
    finally:parser.close()
def small_json(path):return json.loads(pathlib.Path(path).read_text())
def validate_descriptor(d):
    schema=small_json(CODE/'V2_DESCRIPTOR_SCHEMA.json')
    assert all(k in d for k in schema['required'])
    for name,rules in schema['properties'].items():
        if name not in d:continue
        value=d[name]
        if 'const' in rules:assert value==rules['const'],name
        if rules.get('type')=='array':
            assert isinstance(value,list) and rules['minItems']<=len(value)<=rules['maxItems'],name
            if 'items' in rules:assert all(isinstance(v,str) and re.fullmatch(rules['items']['pattern'],v) for v in value),name
        if rules.get('type')=='string':assert isinstance(value,str) and re.fullmatch(rules['pattern'],value),name
        if rules.get('type')=='object':assert isinstance(value,dict) and len(value)>=rules['minProperties'] and all(re.fullmatch(rules['additionalProperties']['pattern'],v) for v in value.values()),name
    assert d['prime_terms']==[list(p) for p in PRIME_PAIRS]
    return True
def column_array(path,key,column=2):
    for i,row in enumerate(iter_array(path,key)):
        if i==column:return row
    raise IndexError(column)
def integers(path):return [[int(x) for x in r] for r in csv.reader(pathlib.Path(path).open())]
def inc(k,n=1):COUNTS[k]=COUNTS.get(k,0)+n
def proc_memory():
    d={}
    for line in pathlib.Path('/proc/self/status').read_text().splitlines():
        k,_,v=line.partition(':')
        if k in ('VmRSS','VmHWM','VmSize','VmPeak'):d[k+'_KiB']=int(v.split()[0])
    return d
def guard():
    if START is not None and time.monotonic()-START>=590:raise RuntimeError('cooperative 590-second wall stop')
    if proc_memory().get('VmRSS_KiB',0)>=500*1024:raise MemoryError('cooperative 500-MiB RSS stop')
def phase(name,live=None):
    global PHASE
    PHASE=name;guard()
    d={'phase':name,'wall_seconds':time.monotonic()-START if START else 0,'CPU_seconds':time.process_time(),'memory':proc_memory(),'live_native_slots':live,'counts':COUNTS.copy()}
    (OUT/'logs').mkdir(parents=True,exist_ok=True)
    with (OUT/'logs/phases.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
    print(json.dumps(d),flush=True);return d
def backend():
    import sys
    sys.path.insert(0,str(ROOT/'runtime_deps'))
    from flint import arb,acb,acb_poly,arb_mat,fmpq,ctx
    ctx.prec=PREC;ctx.threads=1
    globals().update(arb=arb,acb=acb,acb_poly=acb_poly,arb_mat=arb_mat,fmpq=fmpq,ctx=ctx)
def aa(x):return arb(fmpq(x.numerator,x.denominator)) if isinstance(x,F) else arb(x)
def exact(x):
    n,e=x.man_exp();n,e=int(n),int(e)
    return F(n<<e) if e>=0 else F(n,1<<(-e))
def upper(x):return exact(aa(x).abs_upper())
def pad(x,r):return x+arb(0,aa(r).abs_upper())
def quantize(x,bits=100):
    assert x.is_finite()
    f=exact(x.mid())*(1<<bits);n=f.numerator//f.denominator
    return n,upper(x-arb((n,-bits)))
def rec(x,bits=100):
    n,e=quantize(x,bits);v=e*(1<<bits);r=-(-v.numerator//v.denominator)
    return [str(n),str(r)]
def restore(r,bits=100):
    n,e=map(int,r);assert e>=0
    return pad(arb((n,-bits)),arb((e,-bits)))
def packed_write(path,values,bits,shape,meaning,bindings):
    p=pathlib.Path(path);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix('.partial');count=0;mx=mr=0
    with tmp.open('xb') as f:
        for x in values:
            n,r=map(int,x if isinstance(x,(list,tuple)) else rec(x,bits));assert -(1<<255)<=n<(1<<255) and 0<=r<(1<<256),'256-bit node slot overflow'
            mx=max(mx,abs(n).bit_length());mr=max(mr,r.bit_length());f.write(n.to_bytes(32,'little',signed=True));f.write(r.to_bytes(32,'little'));count+=1
    assert count==math.prod(shape);os.replace(tmp,p)
    md={'format':'DYADIC_INTERVAL_256LE_V2','bits':bits,'shape':shape,'count':count,'record_bytes':64,'signed_midpoint_bits':256,'unsigned_radius_bits':256,'max_midpoint_bit_length':mx,'max_radius_bit_length':mr,'meaning':meaning,'bindings':bindings,'bytes':p.stat().st_size,'sha256':sha(p)}
    save(p.with_suffix(p.suffix+'.json'),md)
    # Validate actual serialized records and their finite ball rehydration.
    assert p.stat().st_size==64*count
    with p.open('rb') as f:
        for _ in range(count):
            b=f.read(64);assert len(b)==64;n=int.from_bytes(b[:32],'little',signed=True);r=int.from_bytes(b[32:],'little');assert restore([n,r],bits).is_finite()
        assert not f.read(1)
    return md
def packed_read(path,bits,offset=0,count=None):
    with pathlib.Path(path).open('rb') as f:
        f.seek(offset*64);i=0
        while count is None or i<count:
            b=f.read(64)
            if not b:break
            assert len(b)==64
            yield restore([int.from_bytes(b[:32],'little',signed=True),int.from_bytes(b[32:],'little')],bits);i+=1
        if count is not None:assert i==count
def action_path(i):return (OLD if i<32 else REL)/'outputs'/f'ACTION_{i:02d}.json'
def gamma_path(i):return (FULL if i<32 else REL)/'outputs'/f'SAVED_GAMMA_NODE_CACHE_{i:02d}.json'
def feature_majorant(v,shift=F(0),d=F(1,8)):
    t=1+abs(shift)+d
    return 2*sum((abs(v[3*s])*(1+t*t/96)+abs(v[3*s+1])*t/4+abs(v[3*s+2])*t*t/48 for s in range(124)),F(0))
def load_fixed():
    T=integers(REL/'inputs/T64_dyadic_numerators.csv');X=integers(ADM/'outputs/X40.csv');Y=integers(ADM/'outputs/Y40.csv')
    rows=list(csv.DictReader((REL/'inputs/retained_cells_exact.csv').open()));assert len(rows)==124
    shifts=[int(16*F(r['centre'])) for r in rows];assert max(shifts)==MSTAR
    alpha=[(aa(F(r['V_upper']))/arb.pi()).sqrt() for r in rows];assert all(a.upper()<2 for a in alpha)
    aggregate=CONTRACT/'outputs/FROZEN_AGGREGATE_COEFFICIENTS.json'
    p=list(map(int,column_array(aggregate,'P_Q_numerators_bits70')));dy=list(map(int,column_array(aggregate,'frame_numerators')));py=int(column_array(aggregate,'pole_numerators'))
    assert p==[sum(T[l][i]*Y[i][2] for i in range(64)) for l in range(372)]
    qc=[X[l][2]*(1<<100)-p[l]*(1<<64)-dy[l] for l in range(372)]
    pc=[F(v,1<<70) for v in p];cc=[F(v,1<<140) for v in qc]
    return {'T':T,'X':X,'Y':Y,'p':pc,'qc':cc,'py':F(py,1<<140),'shifts':shifts,'alpha':alpha,'gamma_aggregate_path':aggregate}
def primitive(r,kind='a'):
    p=OLD/'outputs'/f'BASE_{kind}_{r}.json';md=metadata(p)
    assert md['K']==K and md['denominator_power_of_two']==140 and md['component']==('imag' if r%2 else 'real')
    a=[restore(z,140) for z in iter_array(p,'values')];assert len(a)==K+1
    return a
def signed_primitive(a,r,k):
    z=a[abs(k)]
    return acb(0,z if k>=0 else -z) if r%2 else acb(z)
def moments(a,r,k,trig):
    if (trig=='cos' and r%2) or (trig=='sin' and not r%2) or (k==0 and trig=='sin'):return arb(0)
    P=32*arb.pi()
    if abs(k)<=K:
        z=P*a[abs(k)];return z if trig=='cos' else (-z if k>0 else z)
    return arb(0,(P*(1<<20)*(-aa(F(abs(k),128))).exp()).abs_upper())
