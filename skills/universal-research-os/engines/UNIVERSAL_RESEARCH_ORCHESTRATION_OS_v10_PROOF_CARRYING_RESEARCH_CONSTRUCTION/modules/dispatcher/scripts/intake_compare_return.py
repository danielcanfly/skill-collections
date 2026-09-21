#!/usr/bin/env python3
"""Deprecated compatibility wrapper. v7 requires control_plane/intake_admission_gate.py."""
from pathlib import Path
import subprocess,sys
script=Path(__file__).resolve().parents[2]/'control_plane/scripts/intake_admission_gate.py'
raise SystemExit(subprocess.call([sys.executable,str(script),*sys.argv[1:]]))
