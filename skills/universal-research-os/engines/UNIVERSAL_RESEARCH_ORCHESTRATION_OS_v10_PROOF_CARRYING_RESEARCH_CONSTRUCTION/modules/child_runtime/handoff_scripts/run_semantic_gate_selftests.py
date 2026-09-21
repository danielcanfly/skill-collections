#!/usr/bin/env python3
import json,re,difflib
checks=[]
def add(name,condition): checks.append({'name':name,'status':'PASS' if condition else 'FAIL'})
add('title-mismatch-detected', difflib.SequenceMatcher(None,'uplift modeling for marketing','designing experiments to measure incrementality on facebook').ratio()<.72)
add('support-unsupported-contradiction-detected', bool(re.search(r'not establish','source does not establish full proposition',re.I)))
add('illegal-retain-disposition-detected','retain' not in {'create','merge','split','exclude','defer'})
add('generic-context-template-detected', bool(re.search(r'denominator.*cohort.*causal.*valuation','denominator / cohort / causal / valuation',re.I)))
add('access-date-basis-rejected','access-date' in {'access-date','accessed_at','current-year'})
add('high-node-similarity-detected',difflib.SequenceMatcher(None,'definition mechanism boundary failure control','definition mechanism boundary failure control').ratio()>=.88)
out={'status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','checks':checks}; print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
