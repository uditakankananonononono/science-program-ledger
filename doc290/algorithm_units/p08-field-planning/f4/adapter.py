"""Exact supplied-model rectangular reachability certificate check, no solver."""
import sys
from pathlib import Path
from fractions import Fraction as F
sys.path.append(str(Path(__file__).resolve().parent.parent/'f3'))
from verify import Invalid,rational,vector,keys,load_bytes,scalar_text

def model_data(m):
    keys(m,('x','target','dt','B','limit','slew','previous'))
    x=vector(m['x'],cap=4);d=len(x);y=vector(m['target'],d,4)
    dt=vector(m['dt']);cap=vector(m['limit'],cap=4);a=len(cap)
    rate=vector(m['slew'],a,4);prev=vector(m['previous'],a,4)
    if type(m['B']) is not list or len(m['B'])!=d:raise Invalid('map dimension')
    B=[vector(row,a,4) for row in m['B']]
    if any(t<=0 for t in dt) or any(c<=0 for c in cap) or any(r<0 for r in rate) or any(abs(p)>c for p,c in zip(prev,cap)):raise Invalid('model bounds')
    return x,y,dt,B,cap,rate,prev

def ramps(dt,cap,rate,prev):
    lo=[];hi=[];elapsed=F(0)
    for t in dt:
        elapsed+=t
        lo.append([max(-c,p-r*elapsed) for c,p,r in zip(cap,prev,rate)])
        hi.append([min(c,p+r*elapsed) for c,p,r in zip(cap,prev,rate)])
    L=[sum(t*row[j] for t,row in zip(dt,lo)) for j in range(len(cap))]
    U=[sum(t*row[j] for t,row in zip(dt,hi)) for j in range(len(cap))]
    return lo,hi,L,U

def texts(obj):
    if type(obj) is list:return [texts(v) for v in obj]
    return scalar_text(obj)

def check(model,witness):
    try:
        x,y,dt,B,cap,rate,prev=model_data(model)
        lo,hi,L,U=ramps(dt,cap,rate,prev)
        if witness is None:return {'status':'UNAVAILABLE','reason':'missing witness'}
        if type(witness) is not dict or witness.get('kind') not in ('feasible','separator'):raise Invalid('witness kind')
        if witness['kind']=='separator':
            keys(witness,('kind','direction'));v=vector(witness['direction'],len(x),4)
            if not any(v):raise Invalid('zero direction')
            q=[sum(v[i]*B[i][j] for i in range(len(x))) for j in range(len(cap))]
            h=sum(max(qj*l,qj*u) for qj,l,u in zip(q,L,U));p=sum(vv*(yy-xx) for vv,yy,xx in zip(v,y,x))
            return {'status':'UNREACHABLE' if p>h else 'UNAVAILABLE','reason':'strict oriented separation' if p>h else 'nonseparating direction','support':scalar_text(h),'projection':scalar_text(p),'margin':scalar_text(p-h),'lower':texts(L),'upper':texts(U)}
        keys(witness,('kind','integrals'));z=vector(witness['integrals'],len(cap),4)
        if any(a<l or a>u for a,l,u in zip(z,L,U)):raise Invalid('integral outside box')
        if any(sum(b*a for b,a in zip(row,z))!=yy-xx for row,xx,yy in zip(B,x,y)):raise Invalid('terminal integral mismatch')
        mix=[F(0) if u==l else (a-l)/(u-l) for a,l,u in zip(z,L,U)]
        controls=[[(1-w)*l+w*u for w,l,u in zip(mix,low,high)] for low,high in zip(lo,hi)]
        old=prev
        for t,row in zip(dt,controls):
            if any(abs(v)>c or abs(v-p)>r*t for v,c,p,r in zip(row,cap,old,rate)):raise Invalid('lift actuator/slew')
            old=row
        integral=[sum(t*row[j] for t,row in zip(dt,controls)) for j in range(len(cap))]
        terminal=[xx+sum(b*a for b,a in zip(row,integral)) for xx,row in zip(x,B)]
        if integral!=z or terminal!=y:raise Invalid('lift replay')
        return {'status':'REACHABLE','reason':'exact feasible integral and schedule','lower':texts(L),'upper':texts(U),'integrals':texts(integral),'controls':texts(controls),'terminal':texts(terminal),'mix':texts(mix)}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}
