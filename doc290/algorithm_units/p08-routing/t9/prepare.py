"""Development-only manifest and runtime capture; never method scoring."""
import sys,hashlib,json
from pathlib import Path
from core import ROOT
from fixtures import cases
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
    pins=json.loads((ROOT.parent/'t8'/'manifest.json').read_text())['files'];names=set()
    for name in pins:
        if name.startswith('../'):names.add(name)
    for name in ('method.py','proof.py','model.py','fixtures.py','manifest.json','results/RESULT.md','results/report.json'):names.add('../t8/'+name)
    for p in ROOT.iterdir():
        if p.is_file() and p.name not in ('manifest.json','freeze-hashes.sha256'):names.add(p.name)
    (ROOT/'manifest.json').write_text(json.dumps({'files':{n:digest(ROOT/n) for n in sorted(names)}},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    if not (ROOT/'cases.json').exists():(ROOT/'cases.json').write_text(json.dumps(cases(),sort_keys=True,indent=2)+'\n')
    if not (ROOT/'environment.json').exists():environment()
    manifest()
