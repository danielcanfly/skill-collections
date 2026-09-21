#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,datetime
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--json-output');ap.add_argument('--allow-pre-manifest',action='store_true');a=ap.parse_args();root=Path(a.root).resolve();errors=[];p=root/'qa/seal_state.json';d={}
 if not p.exists():errors.append('qa/seal_state.json missing')
 else:d=json.loads(p.read_text(encoding='utf-8'))
 allowed={'MANIFEST_FROZEN','SEALED'} if a.allow_pre_manifest else {'SEALED'}
 if d.get('state') not in allowed:errors.append('invalid state')
 if (root/'qa/SEAL_STATE.json').exists():errors.append('legacy uppercase qa/SEAL_STATE.json must not exist')
 if d.get('state')=='SEALED' and not d.get('sealed_at'):errors.append('sealed_at missing')
 if int(d.get('post_manifest_mutations',1))!=0:errors.append('post_manifest_mutations must equal 0')
 if d.get('manifest_generated_after_all_receipts') is not True:errors.append('manifest chronology flag missing')
 if not a.allow_pre_manifest and d.get('fresh_extraction_verified') is not True:errors.append('fresh extraction not verified')
 if any(v is not True for v in d.get('completed',{}).values()):errors.append('one or more completed receipts false')
 o={'status':'PASS' if not errors else 'FAIL','errors':errors,'seal_state':d};txt=json.dumps(o,ensure_ascii=False,indent=2);print(txt);out=Path(a.json_output) if a.json_output else root/'qa/seal_state_validation.json';out.write_text(txt+'\n',encoding='utf-8');sys.exit(0 if not errors else 1)
if __name__=='__main__':main()
