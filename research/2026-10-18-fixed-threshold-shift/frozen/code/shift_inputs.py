"""Driver-side saved68 premise-chain checks; not imported by checker."""
import csv
from fractions import Fraction as Q
from shift_exact import require
ETA_TEXT='1446776856241610348487954379752034183297365381007/92620636523388719034562694367509285563269120000000'

def accepted(inp):
    m=inp.read('saved_input_manifest');iv=inp.read('saved_input_verification');om=inp.read('saved_output_manifest');ck=inp.read('saved_checker');st=inp.read('saved_status')
    fm=inp.read('final_math');fr=inp.read('final_resource');fv=inp.read('final_verdict')
    require(m['format']=='SAVED68_FIXED_INPUT_MANIFEST_V1' and m['constants']['eta']==ETA_TEXT and m['constants']['tau']=='1/100' and m['constants']['old_columns']==64 and m['constants']['new_columns']==[0,1,2,3] and m['constants']['observations']==372,'saved68 interface/order')
    require(iv['manifest_sha256']==om['manifest_sha256']==ck['input_manifest_sha256']==fm['input_manifest_sha256']==fr['input_manifest_sha256']==fv['input_manifest_sha256']==inp.h('saved_input_manifest'),'saved68 manifest receipt chain')
    require(iv['byte_stability_before_after'] is True and iv['all_numerical_inclusions_inherited'] is True,'saved68 input acceptance')
    require(ck['status']=='PASS' and ck['verdict']=='PASS-INDEPENDENT-SAVED68-EXACT-ENDPOINT-CHECK','saved68 independent checker acceptance')
    require(st['status']=='PASS-SAVED68-ALGEBRA-PROVISIONAL-EXTERNAL-REVIEW-REQUIRED','saved68 status')
    require(fm['status']=='PASS-FINAL-SAVED68-MATHEMATICAL-GATE-CONDITIONAL-ON-INHERITED-PREMISES','saved68 finalized mathematics')
    require(fr['status']=='PASS-INDEPENDENT-SAVED68-RESOURCE-CLOSURE-SCOPE-AND-TRANSCRIPT-AUDIT' and fr['production_roles_closed'] is True and not fr['open_findings'],'saved68 finalized resource/scope/process closure')
    require(fv['status']=='PASS-SAVED68-SAVED-ENDPOINT-AND-RESOURCE-GATE' and fv['science_report']['sha256']==inp.h('final_math') and fv['resource_report']['sha256']==inp.h('final_resource'),'saved68 final combined acceptance')
    require(fm['charged_checker_report_sha256']==inp.h('saved_checker') and fm['producer_status_sha256']==inp.h('saved_status') and fm['norm_error_certificate_sha256']==inp.h('norm'),'saved68 final math receipt identities')
    require(fr['receipt_sha256']==fv['outer_receipt_sha256']==inp.h('saved_outer_receipt'),'saved68 authentic outer closure receipt')
    for role,entry in m['inputs'].items():
        require(inp.files['inherited_'+role]==entry and iv['inputs'][role]==entry,'inherited original byte binding '+role)
    require(inp.files['A']==m['inputs']['A'],'same A input')
    for role,file in [('D68','D68.json'),('K68','K68.json'),('N68','N68.json'),('E68','E68.json'),('norm','NORM_ERROR_CERTIFICATE.json')]:
        require(om['outputs'][file]['sha256']==ck['output_hashes'][file]==inp.h(role),'saved matrix accepted hash '+role)
    sharp=inp.read('sharp');require(sharp['verdict']=='PASS_EXACT_SCALARS_AND_IMMUTABLE_BINDINGS' and all(v is True for v in sharp['checks'].values()),'sharp scalar/coordinate premises')
    d=Q(sharp['exact']['new_prime_tail_upper']);eps=Q(sharp['exact']['cover_epsilon_upper'])
    require(d==Q(960589,4389760000000) and eps==Q(14194233101692862490101543299783481485,3284055810247577849424937639623597936869376),'frozen sharp scalar identity')
    require(Q(1,64)-d-eps==Q(ETA_TEXT)>0,'eta64 generic coercivity identity')
    paper=inp.p('paper').read_text();require('\\label{eq:genericsharp}' in paper and '\\label{eq:eta64}' in paper,'paper equation bindings')
    old_rows={line.split(None,1)[1]:line.split(None,1)[0] for line in inp.p('inherited_old_manifest').read_text().splitlines()}
    require(old_rows['inputs/OBSERVATION_COORDINATE_ORDER.csv']==inp.h('observation_order') and old_rows['certificates/SHARP_TAIL_REPLAY.json']==inp.h('sharp'),'old accepted observation/sharp manifest binding')
    with inp.p('observation_order').open(newline='') as f:order=list(csv.reader(f))
    require(len(order)==373,'372 observation order records')
    return ck

