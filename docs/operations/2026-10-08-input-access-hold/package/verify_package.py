"""Offline byte-integrity checks only; never execute acquisition code."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parent
sha = lambda data: hashlib.sha256(data).hexdigest()
outer = []
for line in (root / 'MANIFEST.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    target = (root / name).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise ValueError('Unsafe or missing path: ' + name)
    if sha(target.read_bytes()) != expected:
        raise ValueError('Outer hash mismatch: ' + name)
    outer.append(name)
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name != 'MANIFEST.sha256'}
if set(outer) != actual or len(outer) != len(set(outer)):
    raise ValueError('Outer manifest coverage mismatch')
archive = root / 'evidence/SERABI_RH_V2_J2_HOLD_20261008_INPUT_403.zip'
prefix = 'SERABI_RH_V2_J2_HOLD_20261008/'
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:
        raise ValueError('ZIP CRC failure')
    if len(z.namelist()) != len(set(z.namelist())):
        raise ValueError('Duplicate ZIP member')
    inner = []
    for line in z.read(prefix + 'MANIFEST.sha256').decode().splitlines():
        expected, name = line.split('  ', 1)
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name:
            raise ValueError('Unsafe inner path')
        if sha(z.read(prefix + name)) != expected:
            raise ValueError('Inner hash mismatch: ' + name)
        inner.append(prefix + name)
    if len(inner) != 12 or set(z.namelist()) != set(inner) | {prefix + 'MANIFEST.sha256'}:
        raise ValueError('Original manifest coverage mismatch')
    for row in json.loads(z.read(prefix + 'FILE_SIZES.json')):
        data = z.read(prefix + row['path'])
        if len(data) != row['bytes'] or sha(data) != row['sha256']:
            raise ValueError('Original size table mismatch: ' + row['path'])
    if z.read(prefix + 'REPORT_KO.md') != (root / 'evidence/SERABI_RH_V2_J2_HOLD_REPORT_20261008.md').read_bytes():
        raise ValueError('Report comparison mismatch')
print(json.dumps({'outer_manifest_checked': len(outer), 'original_manifest_checked': len(inner), 'crc': 'PASS', 'result': 'PASS'}, indent=2))
