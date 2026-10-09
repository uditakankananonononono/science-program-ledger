import json,hashlib
from pathlib import Path
from core import ROOT
from fixtures import cases
if not (ROOT/'cases.json').exists():(ROOT/'cases.json').write_text(json.dumps(cases(),sort_keys=True,indent=2)+'\n')
pins=json.loads((ROOT.parent/'m6'/'manifest.json').read_text())['files'];names={n for n in pins if n.startswith('../')}
for n in ('certificate.py','manifest.json','fixtures.py','results/RESULT.md'):names.add('../i3/'+n)
for n in ('certificate.py',):names.add('../b3/'+n)
for p in ROOT.iterdir():
 if p.is_file() and p.name not in ('manifest.json','freeze-hashes.sha256'):names.add(p.name)
(ROOT/'manifest.json').write_text(json.dumps({'files':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in sorted(names)}},sort_keys=True,indent=2)+'\n')
