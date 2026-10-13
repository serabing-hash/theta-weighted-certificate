"""Static file identities, disclosure scan, and anonymous public readback.

No research module is imported; no mathematical target is evaluated.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import resource
import signal
import urllib.parse
import urllib.request

resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(30,30));signal.alarm(180)
ROOT=Path(__file__).resolve().parent
REPO='serabing-hash/theta-weighted-certificate'
DIRECTORY='research/2026-10-13-direct-m-residual-enclosure-paper'
ALLOWED_HOSTS={'github.com','raw.githubusercontent.com','doi.org','dlmf.nist.gov','www.cambridge.org','orcid.org'}
parser=argparse.ArgumentParser()
parser.add_argument('--manifest',default='SHA256SUMS')
parser.add_argument('--remote-ref')
parser.add_argument('--receipt',type=Path)
args=parser.parse_args()
if args.remote_ref and not re.fullmatch('[0-9a-f]{40}',args.remote_ref):
    raise ValueError('remote ref must be an explicit immutable SHA')
rules={
 'internal_absolute_path':r'/(?:workspace|root|home)/[A-Za-z0-9]',
 'Library_identifier':r'\blibfile_[a-z0-9]+\b',
 'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'credential_token':r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})',
 'private_transfer_field':r'"(?:download_url|upload_url|access_token)"\s*:',
 'signed_url_parameter':r'[?&](?:sig|access_token|token)=',
}
entries=[]
manifest_path=ROOT/args.manifest
manifest_receipt={'file':args.manifest,'bytes':manifest_path.stat().st_size,
                  'sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest()}
if args.remote_ref:
    manifest_url=f'https://raw.githubusercontent.com/{REPO}/{args.remote_ref}/{DIRECTORY}/'+urllib.parse.quote(args.manifest,safe='/')
    with urllib.request.urlopen(manifest_url,timeout=20) as response:
        remote_manifest=response.read();status=response.status
    if remote_manifest!=manifest_path.read_bytes():raise ValueError('remote manifest mismatch')
    manifest_receipt.update(public_url=manifest_url,HTTP_status=status,remote_bytes_equal_local=True)
for line in (ROOT/args.manifest).read_text().splitlines():
    expected,name=line.split('  ',1)
    path=Path(name)
    if path.is_absolute() or '..' in path.parts:raise ValueError('nonrelative manifest path')
    local=(ROOT/path).read_bytes()
    actual=hashlib.sha256(local).hexdigest()
    if actual!=expected:raise ValueError(f'local hash mismatch: {name}')
    if path.suffix in {'.json','.md','.py','.tex'} or name=='.gitignore':
        text=local.decode('utf-8')
        for rule,pattern in rules.items():
            if re.search(pattern,text):raise ValueError(f'disclosure scan: {name}: {rule}')
        for url in re.findall(r'https?://[^\s<>"\)\}]+',text):
            host=urllib.parse.urlparse(url).hostname
            if host not in ALLOWED_HOSTS:raise ValueError(f'nonpublic source host in {name}')
        emails=set(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',text))
        if emails-{'24ping@naver.com'}:raise ValueError(f'unapproved contact in {name}')
    item={'file':name,'bytes':len(local),'sha256':actual,'local_hash_match':True}
    if args.remote_ref:
        url=f'https://raw.githubusercontent.com/{REPO}/{args.remote_ref}/{DIRECTORY}/'+urllib.parse.quote(name,safe='/')
        with urllib.request.urlopen(url,timeout=20) as response:
            remote=response.read();status=response.status
        if remote!=local:raise ValueError(f'remote byte mismatch: {name}')
        item.update(public_url=url,HTTP_status=status,remote_bytes_equal_local=True)
    entries.append(item)
result={'mode':'STATIC_PUBLIC_BYTE_CHECK','research_numerical_evaluations':0,
        'disclosure_scan':'PASS','remote_ref':args.remote_ref,'manifest':manifest_receipt,'files':entries}
if args.receipt:
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','files':len(entries),'remote_ref':args.remote_ref,
                  'anonymous_public_readback':bool(args.remote_ref),'research_numerical_evaluations':0}))
