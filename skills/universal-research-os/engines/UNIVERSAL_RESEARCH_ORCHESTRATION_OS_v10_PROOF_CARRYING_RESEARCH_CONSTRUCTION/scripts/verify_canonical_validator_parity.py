#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,sys
N=['common.py','validate_source_snapshots.py','validate_external_stage_review.py','validate_passage_stage.py','validate_clause_stage.py','validate_proof_chain.py']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('os_root',nargs='?',default=str(Path(__file__).resolve().parents[3]));x=a.parse_args();r=Path(x.os_root);roots=[r/'core/canonical_validators_v10',r/'modules/proof_carrying_construction/scripts',r/'modules/child_runtime/candidate_qa_scripts',r/'modules/audit_os_v6_proof_carrying_construction/scripts'];e=[];matrix={}
 for n in N:
  vals=[]
  for d in roots:
   p=d/n
   if not p.is_file():e.append(str(p.relative_to(r))+' missing');vals.append(None)
   else:vals.append(sha(p))
  matrix[n]=vals
  if len({v for v in vals if v})!=1:e.append(n+' parity mismatch')
 o={'status':'PASS' if not e else 'FAIL','errors':e,'matrix':matrix};print(json.dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
