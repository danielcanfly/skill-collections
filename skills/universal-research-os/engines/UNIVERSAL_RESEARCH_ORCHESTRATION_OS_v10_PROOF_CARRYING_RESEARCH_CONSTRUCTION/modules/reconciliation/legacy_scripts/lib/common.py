from pathlib import Path
import hashlib, json, csv, zipfile, mimetypes, re, unicodedata

def sha256_file(path, chunk=1024*1024):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(chunk), b''): h.update(b)
    return h.hexdigest()

def stable_json_dump(obj, path):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)+'\n', encoding='utf-8')

def norm_text(s):
    s=unicodedata.normalize('NFC', str(s or '')).casefold()
    return re.sub(r'\s+',' ',s).strip()

def zip_crc(path):
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        return {'pass': bad is None, 'bad_member': bad, 'members': len(z.infolist())}

def read_csv(path):
    with open(path,newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
