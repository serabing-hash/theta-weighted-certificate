"""Document/text/byte checks only; no mathematical target evaluation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import resource
import signal
from pypdf import PdfReader

resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(30,30));signal.alarm(60)
parser=argparse.ArgumentParser();parser.add_argument('--source-ref',required=True)
args=parser.parse_args()
assert re.fullmatch('[0-9a-f]{40}',args.source_ref)
ROOT=Path(__file__).resolve().parent
tex=ROOT/'direct_m_residual_enclosure.tex';pdf=ROOT/'output/pdf/direct_m_residual_enclosure.pdf'
text=tex.read_text();source=json.loads((ROOT/'source_definitions.json').read_bytes())
reader=PdfReader(pdf);pages=[p.extract_text() for p in reader.pages]
assert pages and all(len(x)>100 for x in pages)
assert reader.metadata.author=='Jongmin Choi'
joined='\n'.join(pages)
for token in ['Jongmin Choi','Independent Researcher','24ping@naver.com','0009-0008-7448-514X','Zero-start limitation','References']:
    assert token in joined,token
assert r'\begin{thebibliography}' in text
assert not re.search(r'\\(?:input|include|includegraphics|bibliography|addbibresource)\b',text)
assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
assert 'No sign certification' in text and 'Within the files identified' in text
literal=re.search(r'a=\\frac\{(\d+)\}\{(\d+)\}>0',text)
assert literal and '/'.join(literal.groups())==source['a']
assert len(source['F49_b_m_exact_strings'])==49 and len(source['alpha16_exact_strings'])==16
assert hashlib.sha256(json.dumps(source['alpha16_exact_strings'],separators=(',',':')).encode()).hexdigest()==source['alpha16_canonical_vector_sha256']
isolated=PdfReader(ROOT/'tmp/pdfs/standalone/direct_m_residual_enclosure.pdf')
assert [p.extract_text() for p in isolated.pages]==pages
log=(ROOT/'tmp/pdfs/build/direct_m_residual_enclosure.log').read_text()
assert 'Overfull' not in log and 'undefined' not in log and 'Missing $' not in log
expected=f'https://github.com/serabing-hash/theta-weighted-certificate/tree/{args.source_ref}/research/2026-10-13-direct-m-residual-enclosure-paper/'
urls=[]
for page in reader.pages:
    for ref in page.get('/Annots',[]):
        obj=ref.get_object();action=obj.get('/A')
        if action and action.get('/URI'):urls.append(str(action['/URI']))
assert expected in urls
assert expected in re.sub(r'\s+','',joined)
result={'status':'DOCUMENT_CHECKS_PASS','page_count':len(pages),
        'single_tex_isolated_build_pass':True,'isolated_build_page_text_matches_final_pdf':True,
        'internal_bibliography_only':True,'external_figure_or_data_build_inputs':False,
        'source_data_commit':args.source_ref,'source_data_URL':expected,
        'immutable_URL_in_PDF_annotations_and_extracted_text':True,
        'author_metadata_matches_requested':True,'a_F49_alpha16_static_identity_checks_pass':True,
        'undefined_references_or_overfull_boxes':False,'research_numerical_evaluations':0,
        'numerical_M_certificate':'OPEN in inspected scientific input scope',
        'original_whole_line_operator_transfer':'outside established results',
        'tex_sha256':hashlib.sha256(tex.read_bytes()).hexdigest(),
        'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}
(ROOT/'VALIDATION_REPORT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'pages':len(pages),'source_ref':args.source_ref,'research_numerical_evaluations':0}))
