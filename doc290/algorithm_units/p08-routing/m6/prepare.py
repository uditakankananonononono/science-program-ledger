"""Development-only manifest and runtime capture; never method scoring."""
import sys,hashlib,json
from pathlib import Path
from core import ROOT

import unittest,unittest.mock,ast,bisect,selectors,signal,math,dataclasses,heapq,resource,subprocess,random

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def environment():
    sources={};modules=[]
    for name,m in sorted(sys.modules.items()):
        path=getattr(m,'__file__',None)
        if path:
            p=Path(path).resolve()
            if p.is_file() and not str(p).startswith(str(ROOT.parent.parent.resolve())):
                sources[name]={'path':str(p),'sha256':digest(p)};modules.append(name)
    p=Path(sys.executable).resolve();sources['python_executable']={'path':str(p),'sha256':digest(p)}
    (ROOT/'environment.json').write_text(json.dumps({'python':sys.version,'modules':modules,'sources':sources},sort_keys=True,indent=2)+'\n')
def manifest():
    pins=json.loads((ROOT.parent/'m5'/'manifest.json').read_text())['files'];names=set()
    for name in pins:
        if name.startswith('../'):names.add(name)
    for name in ('proof.py','model.py','classes.py','analysis.py','bindings.py','manifest.json','results/RESULT.md','results/FAILED-RUN.json'):names.add('../m5/'+name)
    for p in ROOT.iterdir():
        if p.is_file() and p.name not in ('manifest.json','freeze-hashes.sha256'):names.add(p.name)
    (ROOT/'manifest.json').write_text(json.dumps({'files':{n:digest(ROOT/n) for n in sorted(names)}},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    if not (ROOT/'cases.json').exists():raise RuntimeError('copy exact T9 cases first')
    if not (ROOT/'environment.json').exists():environment()
    manifest()
