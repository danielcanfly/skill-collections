#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
# Compatibility wrapper: canonical finalizer lives inside candidate qa/.
raise SystemExit(subprocess.call([sys.executable,str(Path(sys.argv[1]).resolve()/'qa/finalize_candidate.py'),*sys.argv[1:]]))
