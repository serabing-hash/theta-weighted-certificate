"""Archived runtime byte binding. Native import only in import_runtime()."""
import importlib.util
import os
from pathlib import Path
import sys
from shift_exact import require, read, sha, save


def mapped_files():
    result=set()
    for line in Path('/proc/self/maps').read_text().splitlines():
        cols=line.split(None,5)
        if len(cols)==6 and cols[5].startswith('/'):
            result.add(str(Path(cols[5]).resolve()))
    return result


def import_runtime(plan, output, guard):
    guard()
    require('flint' not in sys.modules, 'runtime was imported before charged gate')
    require(not any(os.environ.get(k) for k in ('LD_PRELOAD','LD_LIBRARY_PATH','PYTHONPATH')),
            'injected library/module path')
    rp=Path(plan['runtime_manifest']); rec=read(rp)
    require(sha(rp)==plan['runtime_manifest_sha256'], 'runtime manifest bytes')
    require(rec['format']=='FULL372_REUSED_RUNTIME_V1' and
            rec['status']=='STATIC_BYTES_VERIFIED_NO_NATIVE_IMPORT' and
            rec['fresh_install'] is False and not rec['unresolved_dependencies'], 'archived runtime premise')
    require([rec[k] for k in ('python_flint','FLINT','precision_bits','threads')]==['0.9.0','3.6.0',160,1],
            'fixed runtime versions')
    require(sha(Path(sys.executable).resolve())==rec['python_sha256']==plan['python_sha256'],
            'same interpreter bytes')
    root=Path(plan['runtime_root']).resolve(); oldroot=Path(rec['runtime_root'])
    expected={x['path']:x for x in rec['files']}
    require(len(expected)==len(rec['files'])==115, 'runtime payload count')
    require(all(not p.endswith('.pyc') and '__pycache__' not in Path(p).parts for p in expected),
            'archived runtime cannot admit cached Python bytecode')
    actual=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'runtime symlink')
        if p.is_file(): actual.add(str(p.relative_to(root)))
    require(actual==set(expected), 'runtime tree exactly archived')
    for rel,item in expected.items():
        guard(); p=root/rel
        require(p.stat().st_size==item['bytes'] and sha(p)==item['sha256'], 'runtime bytes '+rel)
    def remap(name):
        p=Path(name)
        return str(root/p.relative_to(oldroot)) if p.is_relative_to(oldroot) else str(p)
    closure={remap(name):item for name,item in rec['resolved_static_dependency_closure'].items()}
    for name,item in closure.items():
        guard(); require(sha(name)==item['sha256'], 'runtime/system dependency bytes '+name)
        require(all(remap(d['resolved']) in closure for d in item['needed']), 'dependency closure')
    require(all(os.environ.get(k)=='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS')), 'single-thread environment')
    before=mapped_files(); sys.dont_write_bytecode=True; sys.path.insert(0,str(root))
    spec=importlib.util.find_spec('flint')
    require(spec is not None and Path(spec.origin).resolve()==root/'flint/__init__.py', 'frozen runtime resolution')
    guard()
    # The only scientific native import in the entry/driver path.
    import flint
    flint.ctx.prec=160; flint.ctx.threads=1
    require(flint.__version__=='0.9.0' and flint.__FLINT_VERSION__=='3.6.0', 'native runtime version')
    require(flint.ctx.prec==160 and flint.ctx.threads==1, 'fixed precision/thread count')
    newly=mapped_files()-before
    require(newly<=set(closure), 'unbound newly mapped native files')
    for name in newly: require(sha(name)==closure[name]['sha256'], 'mapped bytes')
    for name,module in list(sys.modules.items()):
        if name=='flint' or name.startswith('flint.'):
            p=Path(module.__file__).resolve()
            require(p.is_relative_to(root), 'flint module outside archive')
            rel=str(p.relative_to(root)); require(rel in expected and sha(p)==expected[rel]['sha256'], 'imported module bytes')
    guard()
    save(output,{'status':'TIMED-RUNTIME-IDENTITY-PASS','runtime_manifest_sha256':sha(rp),
         'runtime_root':str(root),'payloads':115,'python_flint':flint.__version__,
         'FLINT':flint.__FLINT_VERSION__,'precision_bits':160,'threads':1,
         'new_mappings':sorted(newly),'installation':False,'scientific_arithmetic_fixture':False})
    os.environ['SHIFT_CHARGED_NATIVE_ADMISSION']='1'; guard()

