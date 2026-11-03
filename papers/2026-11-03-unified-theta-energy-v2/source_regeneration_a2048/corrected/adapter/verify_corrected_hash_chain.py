"""Bind every known producer reference to its actual fresh corrected product."""
import argparse,json
from pathlib import Path
from disk_backed_storage import sha256_file
from producer_guard import verify_source
CANDIDATE='a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d'
def main(args):
 root=Path(args.root);results=root/'results';checks=[];failed=[]
 source_hashes=verify_source(root/'src')
 targets={'candidate_sha256':'results/frozen256_n3072/candidate.json','geometry_npz_sha256':'results/frozen256_n3072/source_geometry.npz','T_lower_sha256':'results/T256_n3072/T_lower_exact.json','G_upper_sha256':'results/G256_n3072/G_upper_exact.json','K_upper_sha256':'results/K256_n3072/K_upper_exact.json','raw_nodes_sha256':'results/gamma256_n3072/gamma_nodes.npz','model_sha256':'results/model256_n3072/model.npz','model_npz_sha256':'results/model256_n3072/model.npz','model_result_sha256':'results/model256_n3072/result.json'}
 cache={}
 def digest(path):
  if path not in cache:cache[path]=sha256_file(path)
  return cache[path]
 def check(record,field,target,value):
  ok=target.is_file() and digest(target)==value
  checks.append({'record':str(record.relative_to(root)),'field':field,'target':str(target.relative_to(root)),'match':ok})
  if not ok:failed.append(str(record.relative_to(root))+':'+field)
 if digest(root/targets['candidate_sha256'])!=CANDIDATE:raise ValueError('Frozen identity differs')
 for p in sorted(results.rglob('*.json')):
  data=json.loads(p.read_text())
  if not isinstance(data,dict):continue
  for key,target in targets.items():
   if key in data:check(p,key,root/target,data[key])
  for key in ['sufficient_matrix_sha256','gate_sha256']:
   if key in data:check(p,key,p.parent/'sufficient_gate_exact.json',data[key])
  if data.get('scalar_cache_sha256') is not None:failed.append(str(p.relative_to(root))+':unexpected_external_scalar_cache')
  if 'inputs_sha256' in data:
   referenced=set()
   for key,value in data['inputs_sha256'].items():
    if key in ['T','G','K']:relative='results/'+key+'256_n3072/'+key+('_lower_exact.json' if key=='T' else '_upper_exact.json')
    elif 'results/' in key:relative='results/'+key.split('results/',1)[1]
    else:failed.append(str(p.relative_to(root))+':unrecognized_reference:'+key);continue
    referenced.add(relative);check(p,'inputs_sha256/'+key,root/relative,value)
   required={targets[k+'_lower_sha256' if k=='T' else k+'_upper_sha256'] for k in ['T','G','K']}
   if p.parent.name=='gate256_n3072_p400':required|={'results/frozen256_n3072/'+x for x in ['candidate.json','verified_components.json','geometry.json']}
   if referenced!=required:failed.append(str(p.relative_to(root))+':unexpected_reference_set')
 identity=json.loads((results/'frozen256_n3072/regeneration_identity.json').read_text())
 if identity['arithmetic_profile']!='directed_integer_power_repair_v1' or identity['source_module_sha256']['interval_bounds.py']!=source_hashes['interval_bounds.py']:failed.append('source regeneration profile')
 for name,expected in identity['source_module_sha256'].items():check(results/'frozen256_n3072/regeneration_identity.json','source_module_sha256/'+name,root/'src'/name,expected)
 check(results/'frozen256_n3072/regeneration_identity.json','adapter_sha256',root/'adapter/regenerate_frozen_components.py',identity['adapter_sha256'])
 report={'status':'PASS' if not failed else 'FAIL','arithmetic_profile':'directed_integer_power_repair_v1','candidate_sha256':CANDIDATE,'checks':checks,'failed':failed,'all_listed_reference_fields_checked':True,'legacy_reference_equality_assumed':False,'scope':'Fresh file-reference integrity only; numerical enclosure and analytic hypotheses are separate','RH':'NOT_PROVED'}
 Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'reference_checks':len(checks),'failed':failed},indent=2))
 if failed:raise SystemExit(1)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',required=True);p.add_argument('--output',required=True);main(p.parse_args())
