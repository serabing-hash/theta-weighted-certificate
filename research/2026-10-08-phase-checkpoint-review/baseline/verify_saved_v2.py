"""CC BY-NC 4.0. Independent integer/rational certificate checks; no numerical backend."""
import json, pathlib
from fractions import Fraction as F
import v2_support as s
def discrepancy(record,midpoint):return F(abs(int(record[0])-int(midpoint)*(1<<40))+int(record[1]),1<<140)
def interval(r):return F(int(r[0])-int(r[1]),1<<140),F(int(r[0])+int(r[1]),1<<140)
def encloses(r,bounds):
    low,high=interval(r);assert low<=bounds[0]<=bounds[1]<=high
def main():
    result={'status':'PASS-PARTIAL-SAVED-ARITHMETIC','new_source_evaluations':0,'new_H_actions':0,'DFTs':0,'physical_integrals':0,'checks':[],'missing':[]}
    def item(name):
        path=s.OUT/name
        if path.exists():return s.small_json(path)
        result['missing'].append(name);return None
    action=item('J2_ACTION_V2.json');cert=item('J2_ACTION_CERTIFICATE.json')
    if action and cert:
        s.validate_descriptor(action);assert s.sha(s.OUT/'J2_ACTION_V2.json')==cert['descriptor_sha256']
        before=s.small_json(s.OUT/'J2_COEFFICIENT_INTERVALS.json')['values'];assert len(before)==len(action['J_cosine_numerators'])==41189
        ej=sum((discrepancy(r,n) for r,n in zip(before,action['J_cosine_numerators'])),F(0));assert ej==F(cert['eJ']) and ej/2<=F(1,1<<30)
        frame=s.small_json(s.OUT/'J2_FRAME_CERTIFICATE.json');ed=[discrepancy(r,n) for r,n in zip(frame['moment_records_bits140'],frame['dyadic_numerators_bits100'])]
        assert [str(x) for x in ed]==frame['errors'];edtotal=2048*sum(ed,F(0));assert edtotal==F(cert['2048_sum_ed']) and edtotal<=F(1,1<<30)
        pole=s.small_json(s.OUT/'J2_POLE_CERTIFICATE.json');em=discrepancy(pole['prequantization_bits140'],pole['numerator_bits100']);assert em==F(cert['em']) and em<=F(1,1<<30)
        assert sum(map(F,cert['errors_L2_upper'].values()),F(0))==F(cert['B2'])<F(1,1<<18)
        assert F(cert['errors_L2_upper']['measured_J_coefficient_error_half'])==ej/2 and F(cert['errors_L2_upper']['measured_frame_error_2048_sum'])==edtotal and F(cert['errors_L2_upper']['measured_pole_error'])==em
        for key,val in action['bindings'].items():assert len(val)==64
        result['checks'].append({'name':'three independent integer discrepancy ledgers and B2 rational sum','B2':cert['B2'],'eJ':str(ej),'2048_sum_ed':str(edtotal),'em':str(em)})
    # Check every completed compact cache/checkpoint byte stream without loading it as a JSON tree.
    packed=[]
    for meta in sorted(s.OUT.rglob('*.bin.json')):
        md=s.small_json(meta);path=pathlib.Path(str(meta)[:-5]);assert path.stat().st_size==md['bytes']==64*md['count'] and s.sha(path)==md['sha256']
        count=0;mx=mr=0
        with path.open('rb') as f:
            while b:=f.read(64):
                assert len(b)==64;n=int.from_bytes(b[:32],'little',signed=True);r=int.from_bytes(b[32:],'little');mx=max(mx,abs(n).bit_length());mr=max(mr,r.bit_length());count+=1
        assert count==md['count'] and mx==md['max_midpoint_bit_length'] and mr==md['max_radius_bit_length'] and mx<=255 and mr<=256
        packed.append({'path':str(path.relative_to(s.OUT)),'bytes':md['bytes'],'sha256':md['sha256'],'records':count,'midpoint_bits':mx,'radius_bits':mr})
    result['checks'].append({'name':'all completed packed records, sizes, hashes and bit-lengths','files':packed})
    kernels=item('J2_437_KERNELS.json')
    if kernels:
        assert len(kernels['KW'])==372 and len(kernels['GF'])==64 and kernels['physical_kernel_count']==437 and kernels['physical_Gram_multiply_adds']==1709544 and kernels['grid_nodes']==3912
        ledger=s.small_json(s.OUT/'J2_437_LEDGER.json');assert len(ledger['KW_pads'])==372 and len(ledger['G0F_pads'])==64
        for pad in ledger['KW_pads']+ledger['G0F_pads']+[ledger['self_pad']]:assert F(pad['quadrature'])+F(pad['analytic_transfer'])==F(pad['total']) and F(pad['total'])>=0
        # Outward ball representation check, all fields are exact signed dyadics.
        for row in kernels['KW']+kernels['GF']+[kernels['self']]:assert len(row)==2 and int(row[1])>=0
        for out,raw,pad in zip(kernels['KW'],ledger['raw_lattice_KW'],ledger['KW_pads']):
            low,high=interval(raw);p=F(pad['total']);encloses(out,(low-p,high+p))
        for out,raw,pad in zip(ledger['padded_G0F_records'],ledger['raw_lattice_G0F'],ledger['G0F_pads']):
            low,high=interval(raw);p=F(pad['total']);encloses(out,(low-p,high+p))
        low,high=interval(ledger['raw_lattice_self']);p=F(ledger['self_pad']['total']);encloses(kernels['self'],(low-p,high+p))
        T=s.integers(s.REL/'inputs/T64_dyadic_numerators.csv')
        for i in range(64):
            low=high=F(0)
            for l in range(372):
                a,b=interval(kernels['KW'][l]);t=F(3*T[l][i],64*(1<<30));v,w=a*t,b*t;low+=min(v,w);high+=max(v,w)
            correction=ledger['affine_correction_records'][i];encloses(correction,(low,high))
            a,b=interval(ledger['padded_G0F_records'][i]);c,d=interval(correction);encloses(kernels['GF'][i],(a-d,b-c))
        result['checks'].append({'name':'437 kernel shape/count, exact pad ledger and nonnegative serialized radii','all_pads_once':kernels['full_line_pads_added_once']})
        result['status']='PASS-INDEPENDENT-SAVED-ARITHMETIC'
    s.save(s.ROOT/'INDEPENDENT_SAVED_VERIFICATION.json',result)
    print(json.dumps({'status':result['status'],'check_groups':len(result['checks']),'packed_files':len(packed),'missing':result['missing']}))
if __name__=='__main__':main()
