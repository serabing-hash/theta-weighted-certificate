from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
m=json.loads((R/'MANIFEST_SHA256.json').read_text())
for n,h in m.items():
 p=R/n
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise SystemExit('FAIL: '+n)
print('PASS: all published research bytes match; not a proof or a full producer replay')
