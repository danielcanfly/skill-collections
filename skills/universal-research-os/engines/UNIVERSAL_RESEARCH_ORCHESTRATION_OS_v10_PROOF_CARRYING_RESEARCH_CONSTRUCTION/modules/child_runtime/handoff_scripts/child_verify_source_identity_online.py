#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,re,urllib.request,urllib.parse,xml.etree.ElementTree as ET,html

def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'ResearchAudit/1.0'}); return urllib.request.urlopen(req,timeout=20).read().decode('utf-8','replace')
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--output'); a=ap.parse_args(); root=Path(a.root).resolve(); rows=list(csv.DictReader((root/'research/source_identity_verification.csv').open(encoding='utf-8-sig',newline=''))); results=[]
 for r in rows:
  sid=r.get('source_id'); url=r.get('canonical_url',''); typ=r.get('identifier_type','').lower(); status='MANUAL_REQUIRED'; observed=''; error=''
  try:
   if typ=='arxiv':
    ident=r.get('observed_identifier') or r.get('declared_identifier'); ident=ident.replace('arXiv:',''); xml=fetch('https://export.arxiv.org/api/query?id_list='+urllib.parse.quote(ident)); ns={'a':'http://www.w3.org/2005/Atom'}; rootx=ET.fromstring(xml); observed=' '.join((rootx.find('.//a:entry/a:title',ns).text or '').split()); status='PASS' if norm(observed)==norm(r.get('observed_title')) else 'FAIL'
   elif typ=='doi':
    doi=r.get('observed_identifier') or r.get('declared_identifier'); data=json.loads(fetch('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''))); observed=' '.join(data['message'].get('title',[''])); status='PASS' if norm(observed)==norm(r.get('observed_title')) else 'FAIL'
   elif url.startswith('http'):
    text=fetch(url)[:500000]; cand=[]
    for pat in [r'<meta[^>]+(?:name|property)=["\'](?:citation_title|og:title|twitter:title)["\'][^>]+content=["\']([^"\']+)',r'<title[^>]*>(.*?)</title>']:
     m=re.search(pat,text,re.I|re.S)
     if m: cand.append(html.unescape(re.sub(r'<[^>]+>',' ',m.group(1))).strip())
    observed=cand[0] if cand else ''
    if observed: status='PASS' if difflib.SequenceMatcher(None,norm(observed),norm(r.get('observed_title'))).ratio()>=.72 else 'FAIL'
  except Exception as e: error=str(e); status='MANUAL_REQUIRED'
  results.append({'source_id':sid,'status':status,'online_observed_title':observed,'error':error})
 out={'status':'PASS' if all(x['status']!='FAIL' for x in results) else 'FAIL','results':results}; p=Path(a.output) if a.output else root/'qa/source_identity_online_validation.json'; p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
if __name__=='__main__':
 import difflib
 main()
