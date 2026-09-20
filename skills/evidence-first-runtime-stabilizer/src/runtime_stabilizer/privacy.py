from __future__ import annotations
import re
from pathlib import Path

PATTERNS=[
    (re.compile(r'(?i)(authorization:\s*bearer\s+)[^\s]+'),r'\1<REDACTED>'),
    (re.compile(r'(?i)((?:password|passwd|secret|token|api[_-]?key|cookie)\s*[=:]\s*)[^\s,;]+'),r'\1<REDACTED>'),
    (re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}'),'<REDACTED_GITHUB_TOKEN>'),
    (re.compile(r'AKIA[0-9A-Z]{16}'),'<REDACTED_AWS_KEY>'),
    (re.compile(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'),'<REDACTED_JWT>'),
    (re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),'<REDACTED_PRIVATE_KEY>'),
]

def redact(s:str)->str:
    for p,r in PATTERNS:
        s=p.sub(r,s)
    return s

def read_text_strict(path:Path)->str|None:
    b=path.read_bytes()
    if b'\x00' in b:
        return None
    try:
        return b.decode('utf-8')
    except UnicodeDecodeError:
        return None
