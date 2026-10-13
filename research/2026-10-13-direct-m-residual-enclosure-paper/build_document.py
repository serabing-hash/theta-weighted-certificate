"""Bounded document compilation/rendering only; no research arithmetic."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parent
# The parent never raises its soft limits. The larger inherited hard limit
# lets the single child set its own enforced soft/hard cap in preexec_fn.
resource.setrlimit(resource.RLIMIT_AS, (128*1024**2, 320*1024**2))
resource.setrlimit(resource.RLIMIT_CPU, (45, 150))
signal.alarm(240)

def child_limits():
    os.setsid()
    resource.setrlimit(resource.RLIMIT_AS, (320*1024**2, 320*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU, (150, 150))

def command(args, logfile, timeout=90, cwd=ROOT):
    with logfile.open('wb') as out:
        p = subprocess.Popen(args, cwd=cwd, stdout=out, stderr=subprocess.STDOUT,
                             preexec_fn=child_limits)
        try:
            code = p.wait(timeout=timeout)
        except BaseException:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            raise
    if code:
        raise RuntimeError(f'document command exit {code}; see {logfile}')

parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=['compile', 'render', 'standalone'])
args = parser.parse_args()
start = time.monotonic()
build = ROOT/'tmp/pdfs/build'
build.mkdir(parents=True, exist_ok=True)
pdf = ROOT/'output/pdf/direct_m_residual_enclosure.pdf'
tex = ROOT/'direct_m_residual_enclosure.tex'
if args.mode == 'standalone':
    isolated=ROOT/'tmp/pdfs/standalone'
    isolated.mkdir(parents=True,exist_ok=True)
    isolated_tex=isolated/tex.name
    shutil.copyfile(tex,isolated_tex)
    assert isolated_tex.read_bytes()==tex.read_bytes()
    for i in range(2):
        command(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                 '-no-shell-escape', '-file-line-error', tex.name],
                 build/f'standalone_pass_{i+1}.stdout.log',cwd=isolated)
    pdf=isolated/'direct_m_residual_enclosure.pdf'
elif args.mode == 'compile':
    for i in range(2):
        command(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                 '-no-shell-escape', '-file-line-error', f'-output-directory={build}',
                 str(tex)], build/f'compile_pass_{i+1}.stdout.log')
    pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(build/'direct_m_residual_enclosure.pdf', pdf)
else:
    renders = ROOT/'tmp/pdfs/rendered'
    renders.mkdir(parents=True, exist_ok=True)
    command(['pdftoppm', '-r', '120', '-png', str(pdf), str(renders/'page')],
            build/'render.stdout.log', timeout=180)

receipt = {
    'operation': f'document_{args.mode}', 'research_numerical_evaluations': 0,
    'tex_sha256': hashlib.sha256(tex.read_bytes()).hexdigest(),
    'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
    'wall_seconds': time.monotonic()-start,
    'children_CPU_seconds': resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
                            + resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,
    'parent_AS_soft_MiB': 128, 'parent_AS_hard_MiB': 320,
    'child_AS_soft_and_hard_MiB': 320,
    'aggregate_enforced_AS_limit_sum_MiB': 448,
    'aggregate_enforced_CPU_limit_sum_max_seconds': 345 if args.mode in ('compile','standalone') else 195,
    'wall_alarm_seconds': 240, 'shell_escape': False,
}
(ROOT/f'{args.mode.upper()}_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
