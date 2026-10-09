import importlib.util
from pathlib import Path
SPEC_PATH=Path(__file__).resolve().parent.parent/'i3'/'certificate.py'
spec=importlib.util.spec_from_file_location('i4_pinned_i3',SPEC_PATH);i3=importlib.util.module_from_spec(spec);spec.loader.exec_module(i3)
Invalid,keys,integer,rational,capped,scalar_text,load_bytes=(getattr(i3,k) for k in ('Invalid','keys','integer','rational','capped','scalar_text','load_bytes'))
class Failure(RuntimeError):pass
class Domain(Exception):pass

def model(s):
    keys(s,('graph','start','goal','budget','forbidden','penalties','route'))
    temp={k:s[k] for k in ('graph','start','goal','forbidden','penalties','route')}|{'potential':None}
    G,f,p,states,arcs=i3.b3.t2.model(temp);integer(s['budget']);n=next((len(e['scenario_times']) for es in G.values() for e in es),0)
    if not 1<=n<=4:raise Invalid('positive edge-established dimension')
    primal=i3.b3.t2.helper.checked(s)
    return G,n,states,arcs,primal

def text(x):
    # I3 accepts reduced canonical rational strings and exact integer, not floats.
    value=scalar_text(x)
    if len(value)>80 or abs(x)>i3.b3.MAX:raise Domain('candidate rational representation/cap')
    rational(value)
    return value

def component(x):
    if type(x) is not int or not 0<=x<=i3.b3.MAX:raise Domain('candidate scenario+delay cap')
    return x
