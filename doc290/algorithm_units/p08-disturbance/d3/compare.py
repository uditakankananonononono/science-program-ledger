"""D3 pin-before-import admission and frozen factorial scoring."""
from pathlib import Path
import json,hashlib,importlib.util,sys
from pins import PINS

def typed_equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def admit(root,manifest):
    root=Path(root)
    for name,sha in PINS.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=sha:raise ValueError('pin mismatch '+name)
    frozen=json.loads((root/'d3/manifest.json').read_text())
    if not typed_equal(manifest,frozen):raise ValueError('typed frozen manifest mismatch')
    d1=json.loads((root/'d1/manifest.json').read_text());d2=json.loads((root/'d2/manifest.json').read_text())
    for key in ('initial','target','dt','bound','lower','upper','tolerance','policy_reset_and_action_wall_seconds'):
        if not typed_equal(manifest[key],d1[key]) or not typed_equal(manifest[key],d2[key]):raise ValueError('plant constant')
    if not typed_equal(manifest['policies'],d2['policies']):raise ValueError('policy list')
    expected=[]
    for name in ('reference','alternating_drift','reduced_actuation','immobilization_block'):
        original=next(c['sequence'] for c in d1['cases'] if c['name']==name)
        for obs in ('all','block'):
            seq=json.loads(json.dumps(original));seq['observed']=next(c['sequence']['observed'] for c in d1['cases'] if c['name']==('reference' if obs=='all' else 'observation_block'))
            expected.append({'name':name+'__'+obs,'sequence':seq})
    if not typed_equal(manifest['cases'],expected):raise ValueError('factorial identity')
    return frozen

def load_runtime(root):
    # Called only after admission, no dependency import executes before pin check.
    def load(name,path):
        spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
    h=load('d3_pinned_d2_harness',Path(root)/'d2/harness.py')
    old=sys.modules.get('harness');sys.modules['harness']=h
    try:c=load('d3_pinned_d2_compare',Path(root)/'d2/compare.py')
    finally:
        if old is None:sys.modules.pop('harness',None)
        else:sys.modules['harness']=old
    return h,c

def score(manifest,root=None):
    root=Path(root) if root is not None else Path(__file__).resolve().parent.parent
    m=admit(root,manifest);h,c=load_runtime(root)
    from fractions import Fraction as F
    policies={'hold_p':h.HoldP,'predict_p':h.PredictP,'hold_sign':h.HoldSign,'predict_sign':h.PredictSign}
    plant={k:F(m[k]) for k in ('initial','target','dt','bound','lower','upper','tolerance')};rows=[]
    for name in m['policies']:
        for entry in m['cases']:
            seq={k:[F(x) for x in v] if k in ('gain','drift') else v for k,v in entry['sequence'].items()}
            rows.append({'policy':name,'case':entry['name'],**h.run(policies[name],seq,**plant)})
    pairs=[]
    for rule in ('p','sign'):
        for entry in m['cases']:
            get=lambda name:next(r for r in rows if r['case']==entry['name'] and r['policy']==name)
            pairs.append({'rule':rule,'case':entry['name'],**c.pair(get('hold_'+rule),get('predict_'+rule),len(entry['sequence']['gain']))})
    return {'rows':rows,'pairs':pairs}
if __name__=='__main__':
    print(json.dumps(score(json.loads(Path(__file__).with_name('manifest.json').read_text())),default=str,indent=2))
