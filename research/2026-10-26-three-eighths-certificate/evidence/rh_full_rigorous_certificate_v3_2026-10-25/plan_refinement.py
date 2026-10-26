"""Exact rational allocation from an already certified full-domain remainder ledger.
No new integrals, eigenvalues, matrix assembly or source evaluations.
"""
from pathlib import Path
from fractions import Fraction
import json,hashlib,math
SRC=Path('../rh_full_rigorous_certificate_v2_2026-10-25/H_domain_ledger.json')
TARGET=Fraction(1,128);CAP=256

def upward_float(q):
 x=float(q)
 if Fraction.from_float(x)<q:x=math.nextafter(x,math.inf)
 return x

def main():
 x=json.loads(SRC.read_text());rows=[r for r in x['panels'] if not r.get('analytic_tail_reused',False)]
 q={int(r['template']):Fraction.from_float(float(r['used_upper'])) for r in rows};k={i:1 for i in q}
 total=sum(q.values());cost=len(k)
 while total>TARGET:
  if cost>=CAP:raise RuntimeError('fixed point-template cap cannot meet target')
  allowed=[i for i in q if cost+k[i]<=CAP]
  if not allowed:raise RuntimeError('fixed cap reached')
  i=max(allowed,key=lambda j:(q[j]*Fraction(15,16)/(k[j]**5),-j))
  total-=q[i]*Fraction(15,16)/(k[i]**4);cost+=k[i];k[i]*=2
 out={'status':'exact_rational_plan','source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
      'target_fraction':str(TARGET),'quad_budget_fraction':str(total),'quad_budget_upper':upward_float(total),
      'point_templates':cost,'point_template_cap':CAP,'maximum_split':max(k.values()),
      'panels':[{'template':i,'split':k[i],'old_bound_fraction':str(q[i]),'new_bound_fraction':str(q[i]/k[i]**4)} for i in sorted(k)],
      'proof':'Each old normalized-fourth-derivative supremum covers every child. k equal children produce k*(h/k)^5/80=h^5/(80*k^4).'}
 Path('refinement_plan.json').write_text(json.dumps(out,indent=2));print(json.dumps({key:out[key] for key in ('status','quad_budget_upper','point_templates','maximum_split')}))
if __name__=='__main__':main()
