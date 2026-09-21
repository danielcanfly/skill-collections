#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import load_json,result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);r=load_json(root/'qa/seal_state.json',{});errors=[]
if (root/'qa/SEAL_STATE.json').exists(): errors.append('legacy uppercase qa/SEAL_STATE.json exists')
if r.get('state')!='SEALED': errors.append('final candidate seal state must equal SEALED')
if int(r.get('post_manifest_mutations',1))!=0: errors.append('post-manifest mutations detected')
if r.get('manifest_generated_after_all_receipts') is not True: errors.append('manifest not generated after all receipts')
if r.get('fresh_extraction_verified') is not True: errors.append('fresh extraction not verified')
if not r.get('sealed_at') and not r.get('fresh_extraction_receipt'): errors.append('seal timestamp/receipt missing')
emit(result('PASS' if not errors else 'FAIL',errors,stats=r),a.output)
