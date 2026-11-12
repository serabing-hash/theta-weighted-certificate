from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
m=json.loads((R/'ARCHIVE.json').read_text())
a=[]
for p in m['parts']:
 b=(R/p['path']).read_bytes()
 if len(b)!=p['bytes'] or hashlib.sha256(b).hexdigest()!=p['sha256']:raise SystemExit('Invalid part: '+p['path'])
 a.append(b)
b=b''.join(a)
if len(b)!=m['bytes'] or hashlib.sha256(b).hexdigest()!=m['sha256']:raise SystemExit('Archive checksum mismatch')
out=R/m['archive']
if out.exists() and out.read_bytes()!=b:raise SystemExit('Refusing to overwrite a different archive')
out.write_bytes(b)
with zipfile.ZipFile(out) as z:
 if z.testzip() is not None:raise SystemExit('ZIP CRC failure')
print('PASS: reconstructed and verified',out.name)
print('Extract in a new directory, then run python3 verify_bundle.py there.')
