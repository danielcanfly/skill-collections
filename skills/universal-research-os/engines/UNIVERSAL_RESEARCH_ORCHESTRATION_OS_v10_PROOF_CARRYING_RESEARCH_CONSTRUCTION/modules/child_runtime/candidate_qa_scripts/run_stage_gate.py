#!/usr/bin/env python3
from pathlib import Path
import argparse,subprocess,sys
def main():
 a=argparse.ArgumentParser();a.add_argument('root');a.add_argument('--stage',choices=['sources','review','passages','clauses','claims','all'],required=True);x=a.parse_args();h=Path(__file__).parent;py=sys.executable
 m={'sources':['validate_source_snapshots.py'],'review':['validate_source_snapshots.py','validate_external_stage_review.py'],'passages':['validate_source_snapshots.py','validate_external_stage_review.py','validate_passage_stage.py'],'clauses':['validate_source_snapshots.py','validate_external_stage_review.py','validate_passage_stage.py','validate_clause_stage.py'],'claims':['validate_source_snapshots.py','validate_external_stage_review.py','validate_passage_stage.py','validate_clause_stage.py','compile_direct_support_claims.py','validate_proof_chain.py'],'all':['validate_source_snapshots.py','validate_external_stage_review.py','validate_passage_stage.py','validate_clause_stage.py','compile_direct_support_claims.py','validate_proof_chain.py']}
 for n in m[x.stage]:subprocess.run([py,str(h/n),x.root],check=True)
if __name__=='__main__':main()
