import os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=str(ROOT/'src')
if SRC not in sys.path:
    sys.path.insert(0,SRC)
existing=os.environ.get('PYTHONPATH','')
os.environ['PYTHONPATH']=SRC+(os.pathsep+existing if existing else '')
