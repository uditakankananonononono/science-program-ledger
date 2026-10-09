import json,hashlib
from pathlib import Path
from core import ROOT

if not (ROOT/'cases.json').exists():raise RuntimeError('copy frozen I4 inputs')
pins=json.loads((ROOT.parent/'m6'/'manifest.json').read_text())['files'];names={n for n in pins if n.startswith('../')}
for n in ('certificate.py','manifest.json','fixtures.py','results/RESULT.md'):names.add('../i3/'+n)
for n in ('generator.py','proof.py','model.py','cases.json','manifest.json','results/RESULT.md'):names.add('../i4/'+n)
for n in ('generator.py','proof.py','model.py','cases.json','manifest.json','results/RESULT.md'):names.add('../i5/'+n)
for n in ('durable.py','controller.py','results/RESULT.md'):names.add('../m6/'+n)
for n in ('certificate.py','manifest.json','cases.json','results/RESULT.md'):names.add('../t5/'+n)
for n in ('certificate.py',):names.add('../b3/'+n)
for p in ROOT.iterdir():
 if p.is_file() and p.name not in ('manifest.json','freeze-hashes.sha256'):names.add(p.name)
(ROOT/'manifest.json').write_text(json.dumps({'files':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in sorted(names)}},sort_keys=True,indent=2)+'\n')
