"""Corrected-producer Gamma with disk storage and atomic independent-phase restart.

Fixed preparation always reruns. Only an exact, source/input/config/environment
bound complete prefix may be copied into fresh output buffers; the original
remaining phase bodies and final archive serialization execute unchanged.
"""
import argparse,builtins,gc,hashlib,inspect,json,mmap,re,sys
from pathlib import Path
import numpy as np
from producer_guard import verify_source
from disk_backed_storage import sha256_file,evict
from gamma_phase_checkpoint import GammaPhaseStore
from run_K_checkpointed import arithmetic_environment
PHASE_COUNT=33;CELLS=5120;K=256
CANDIDATE='a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d'

def raw_digest(array):
 h=hashlib.sha256();v=memoryview(array).cast('B')
 for start in range(0,len(v),1024*1024):h.update(v[start:start+1024*1024])
 return h.hexdigest()

def preparation_record(local,producer):
 return {'n':local['n'],'k':local['k'],'h':str(local['h']),'cells':local['cells'],'degree':local['degree'],'NTT_length':local['size'],'CRT_product':str(local['product']),'primes':producer.PRIMES,'H_bits':producer.H_BITS,'J_bits':producer.J_BITS,'phases':[p.record() for p in local['phases']],'H0':local['H0'].record(),'hradius':str(local['hradius']),'jradius':str(local['jradius']),'column_error_bounds_before_float':[str(v) for v in local['error']],'source_ffts':[{'shape':list(a.shape),'dtype':a.dtype.str,'raw_sha256':raw_digest(a)} for a in local['source_ffts']]}

def main(args):
 if not __debug__:raise RuntimeError('Assertions required')
 source=Path(args.source_dir).resolve();source_hashes=verify_source(source);sys.path.insert(0,str(source));import ntt_gamma_rows as producer
 candidate=Path(args.candidate)/'candidate.json'
 if sha256_file(candidate)!=CANDIDATE or args.degree!=PHASE_COUNT-1:raise ValueError('Unexpected candidate/configuration')
 out=Path(args.output);scratch=Path(args.scratch)
 for path in [out,scratch]:
  if path.exists() and any(path.iterdir()):raise FileExistsError('Refusing nonempty output/scratch')
 scratch.mkdir(parents=True,exist_ok=True)
 helpers={name:Path(__file__).with_name(name) for name in ['run_gamma_checkpointed.py','gamma_phase_checkpoint.py','k_prefix_checkpoint.py','producer_guard.py','disk_backed_storage.py','run_K_checkpointed.py']}
 binding={'arithmetic_profile':'directed_integer_power_repair_v1','candidate_sha256':CANDIDATE,'source_sha256':source_hashes,'adapter_helper_sha256':{k:sha256_file(p) for k,p in helpers.items()},'arithmetic_environment':arithmetic_environment()}
 shape=(PHASE_COUNT,CELLS,K);outputs=[];released_initial=[];released_phases=[];printed=[];store=None;prefix=[];start=0;enumerations=0
 class Output(np.memmap):
  def __setitem__(self,key,value):
   super().__setitem__(key,value);evict(self)
   if getattr(self,'role',None)=='rad':
    caller=inspect.currentframe().f_back
    if caller.f_code is not producer.main.__code__:raise RuntimeError('Unexpected Gamma phase writer')
    phase=caller.f_locals['phase_index']
    if phase!=start+len(released_phases):raise RuntimeError('Unexpected phase lifetime sequence')
    exact=caller.f_locals['exact'];residues=caller.f_locals['residues']
    if exact.dtype!=object or not isinstance(residues,list):raise TypeError('Unexpected consumed CRT state')
    exact.fill(0);residues.clear();gc.collect();released_phases.append(phase)
 old_empty,old_empty_like=np.empty,np.empty_like
 had_enumerate='enumerate' in producer.__dict__;old_enumerate=producer.__dict__.get('enumerate',builtins.enumerate)
 had_print='print' in producer.__dict__;old_print=producer.__dict__.get('print',builtins.print)
 def allocate(dimensions,dtype=float,order='C',**kwargs):
  nonlocal store,prefix,start
  if (tuple(dimensions) if not isinstance(dimensions,int) else (dimensions,))==shape:
   if np.dtype(dtype)!=np.dtype('float64') or order!='C' or kwargs or len(outputs)>=2:raise ValueError('Unexpected Gamma allocation')
   if not outputs:
    caller=inspect.currentframe().f_back
    if caller.f_code is not producer.main.__code__:raise RuntimeError('Unexpected Gamma allocation caller')
    binding['preparation']=preparation_record(caller.f_locals,producer)
    # JSON normalizes the immutable tuples before comparison on resumed runs.
    normalized=json.loads(json.dumps(binding));store=GammaPhaseStore(args.checkpoints,normalized,phase_count=PHASE_COUNT,row_shape=(CELLS,K))
    prefix=store.validate_prefix(required=args.resume)
    if prefix and not args.resume:raise FileExistsError('Committed phases exist; explicit --resume required')
    start=len(prefix)
    for name,kind in [('packet',dict),('jumps',list)]:
     value=caller.f_locals[name]
     if not isinstance(value,kind):raise TypeError('Unexpected completed source container')
     value.clear();released_initial.append(name)
    gc.collect()
   key='mid' if not outputs else 'rad';a=np.lib.format.open_memmap(scratch/(key+'.npy'),mode='w+',dtype='float64',shape=shape,fortran_order=False).view(Output);a.role=key;outputs.append(a);return a
  return old_empty(dimensions,dtype=dtype,order=order,**kwargs)
 def empty_like(a,*argv,**kwargs):
  if isinstance(a,Output) and a.shape==shape:
   if argv or kwargs:raise ValueError('Unexpected Gamma empty_like')
   return allocate(shape,dtype=a.dtype)
  return old_empty_like(a,*argv,**kwargs)
 def phases(values,*argv):
  nonlocal enumerations
  caller=inspect.currentframe().f_back
  if caller.f_code is producer.main.__code__ and values is caller.f_locals.get('phases'):
   if argv or enumerations or len(outputs)!=2:raise RuntimeError('Unexpected Gamma outer enumeration')
   enumerations+=1
   if store.restore(*outputs)!=start:raise ValueError('Wrong restored phase prefix')
   return builtins.enumerate(values[start:],start)
  return old_enumerate(values,*argv)
 def emit(*values,**kwargs):
  old_print(*values,**kwargs)
  if len(values)!=1 or not isinstance(values[0],str):return
  match=re.fullmatch(r'validated Gamma phase (\d+)/(\d+)',values[0])
  if match is None:return
  completed,total=map(int,match.groups());caller=inspect.currentframe().f_back;phase=completed-1
  if caller.f_code is not producer.main.__code__ or caller.f_locals['phase_index']!=phase or total!=PHASE_COUNT or phase!=start+len(printed) or released_phases[-1]!=phase:raise RuntimeError('Gamma progress/state mismatch')
  store.save(phase,outputs[0][phase],outputs[1][phase]);printed.append(phase)
  for a in outputs:evict(a)
 np.empty,np.empty_like=allocate,empty_like;producer.enumerate=phases;producer.print=emit
 try:producer.main(argparse.Namespace(candidate=args.candidate,output=args.output,degree=PHASE_COUNT-1))
 finally:
  np.empty,np.empty_like=old_empty,old_empty_like
  if had_enumerate:producer.enumerate=old_enumerate
  else:del producer.enumerate
  if had_print:producer.print=old_print
  else:del producer.print
 if enumerations!=1 or printed!=list(range(start,PHASE_COUNT)) or released_phases!=printed:raise RuntimeError('Incomplete ordered Gamma execution')
 if verify_source(source)!=source_hashes or sha256_file(candidate)!=CANDIDATE or any(sha256_file(p)!=binding['adapter_helper_sha256'][k] for k,p in helpers.items()) or arithmetic_environment()!=binding['arithmetic_environment']:raise RuntimeError('Bound identity changed during Gamma')
 record={'status':'COMPLETED','arithmetic_profile':'directed_integer_power_repair_v1','binding_sha256':store.binding_sha256,'binding':binding,'resumed_from_completed_phases':start,'new_committed_phases':printed,'last_manifest_sha256':store.committed[-1]['manifest_sha256'],'original_phase_body_unchanged':True,'old_logs_used_as_state':False,'storage_and_checkpoint_adaptation':True,'source_bytes_modified_during_execution':False,'unused_initial_containers_released':released_initial}
 (out/'checkpoint_adapter_identity.json').write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['source-dir','candidate','output','scratch','checkpoints']:p.add_argument('--'+name,required=True)
 p.add_argument('--degree',type=int,default=32);p.add_argument('--resume',action='store_true');main(p.parse_args())
