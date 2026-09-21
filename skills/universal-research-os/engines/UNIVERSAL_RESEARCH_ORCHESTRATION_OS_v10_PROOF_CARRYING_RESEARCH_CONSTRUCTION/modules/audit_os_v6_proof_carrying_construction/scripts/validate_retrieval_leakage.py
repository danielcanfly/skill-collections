#!/usr/bin/env python3
from pathlib import Path
import argparse,re,tokenize,io
from common import result,emit
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);errors=[];warnings=[]
for p in list((root/'qa').glob('*retrieval*.py'))+list((root/'scripts').glob('*retrieval*.py')):
    src=p.read_text(encoding='utf-8',errors='replace')
    try:
        toks=[]
        for tok in tokenize.generate_tokens(io.StringIO(src).readline): toks.append((tok.type,'' if tok.type in {tokenize.STRING,tokenize.COMMENT} else tok.string))
        code=tokenize.untokenize(toks).lower()
    except: code=src.lower()
    if re.search(r'scores?\s*\[.*\]\s*\+=',code) and 'expected' in code: errors.append(f'{p.name}: runner appears to boost expected IDs')
    if ('negative_ids' in code or 'negativeids' in code) and re.search(r'(remove|exclude|filter|-=)',code): errors.append(f'{p.name}: runner appears to use negative IDs for ranking')
    if 'expected_ids' in code and any(x in code for x in ['title bonus','alias bonus','graph expansion']): errors.append(f'{p.name}: answer-aware rank manipulation')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'runner_files':len(list((root/'qa').glob('*retrieval*.py')))}),a.output)
