#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json
from common import *
def main():
 a=argparse.ArgumentParser();a.add_argument('root');x=a.parse_args();r=Path(x.root);e=[]
 for rel in ['qa/source_snapshot_validation.json','qa/passage_stage_validation.json','qa/clause_stage_validation.json','qa/claim_compilation_receipt.json']:
  j=load(r/rel);
  if j.get('status')!='PASS':e.append(rel+' not PASS')
 compiled=read_csv(r/'research/compiled_direct_support_claims.csv') if (r/'research/compiled_direct_support_claims.csv').exists() else []
 if not compiled:e.append('compiled direct-support population is zero')
 edges=read_csv(r/'research/edge_entailment.csv') if (r/'research/edge_entailment.csv').exists() else []
 direct=[q for q in edges if q.get('support_label')=='support']
 ids={q.get('claim_id') for q in compiled}
 for q in direct:
  if q.get('claim_id') not in ids:e.append(q.get('edge_id','?')+': handwritten/uncompiled direct claim')
 o={'status':'PASS' if not e else 'FAIL','compiled_claim_count':len(compiled),'direct_edge_count':len(direct),'errors':e};dump(r/'qa/proof_chain_validation.json',o);print(json.dumps(o,indent=2));sys.exit(0 if not e else 1)
if __name__=='__main__':main()
