import hashlib,json,os,sys,re,fractions,_hashlib,_json,_sre
from pathlib import Path
from fractions import Fraction as F
import numpy,scipy
import scipy.optimize._linprog,scipy.optimize._highspy._highs_wrapper
from adapter import load_bytes,check,Invalid
ROOT=Path(__file__).resolve().parent

def gate():
    pins=json.loads((ROOT/'manifest.json').read_text())
    for name,digest in pins['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise Invalid('identity mismatch '+name)
    env=json.loads((ROOT/'environment.json').read_text())
    if sys.version!=env['python'] or numpy.__version__!=env['numpy'] or scipy.__version__!=env['scipy'] or any(os.environ.get(k)!='1' for k in env['thread_keys']):raise Invalid('environment mismatch')
    for name,identity in env['runtime_sources'].items():
        path=Path(identity['path'])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=identity['sha256']:raise Invalid('runtime source mismatch '+name)
    for name in env['module_names']:
        module=sys.modules.get(name)
        if module is None or (str(Path(module.__file__).resolve()) if getattr(module,'__file__',None) else str(Path(sys.executable).resolve()))!=env['runtime_sources'][name]['path']:raise Invalid('loaded module mismatch '+name)
    if str(Path(sys.executable).resolve())!=env['runtime_sources']['python_executable']['path']:raise Invalid('executable path mismatch')

def agreed(expected,result):return expected==result['status']

def run(output):
    gate();cases=load_bytes((ROOT/'cases.json').read_bytes());rows=[]
    for c in cases:
        result=check(c['model'],c['witness']);rows.append({'name':c['name'],'expected':c['expected'],'result':result,'agreement':agreed(c['expected'],result),'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
    sys.path.insert(0,str(ROOT.parent));from scenarios import solve_scenarios
    baseline=[]
    for c in cases:
        if ':' in c['name']:continue
        def floats(v):return [floats(a) if type(a) is list else float(F(a)) for a in v]
        m=c['model']
        try:entry={'name':c['name'],'result':solve_scenarios(*(floats(m[k]) for k in ('x','dt','maps','limit','slew','previous','lower','upper')))}
        except Exception as e:entry={'name':c['name'],'exception_type':type(e).__name__,'exception':str(e)}
        baseline.append(entry)
    Path(output).write_text(json.dumps({'rows':rows,'agreement_count':sum(r['agreement'] for r in rows),'row_count':len(rows),'baseline':baseline,'scope':'supplied rational models, external certificates; descriptive floating status not proof'},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
