import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('p3_model',Path(__file__).resolve().parent.parent/'p3'/'model.py');p3=importlib.util.module_from_spec(spec);spec.loader.exec_module(p3)
Invalid,integer,MAX,EDGE_MAX=(getattr(p3,k) for k in ('Invalid','integer','MAX','EDGE_MAX'))
def model(s):
    if type(s) is not dict or set(s)!={'graph','start','goal','budget'}:raise Invalid('statement fields')
    integer(s['budget']);return p3.model({k:s[k] for k in ('graph','start','goal')})
def witness(s,r):
    G,ns=model(s)
    if type(r) is not dict or set(r)!={'path','edges','exposure','scenario_totals','worst_time'}:raise Invalid('route fields')
    result=p3.witness({k:s[k] for k in ('graph','start','goal')},{k:r[k] for k in ('path','edges','scenario_totals','worst_time')})
    exposure=0;ledger=[]
    for e in r['edges']:
        exposure=integer(exposure+G[e['source']][e['edge_index']]['exposure']);ledger.append(exposure)
    if integer(r['exposure'])!=exposure or exposure>s['budget']:raise Invalid('indexed exposure/budget')
    return dict(result,exposure=exposure,exposure_ledger=ledger)
