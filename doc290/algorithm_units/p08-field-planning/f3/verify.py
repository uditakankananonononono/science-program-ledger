"""Exact rational minimax witness check, independent of floating solver assembly."""
import json
import re
from fractions import Fraction

class Invalid(ValueError):
    pass

def rational(v):
    if type(v) is int:
        if len(str(v))>80: raise Invalid('scalar length')
        return Fraction(v)
    if type(v) is not str or len(v)>80 or not re.fullmatch(r'(0|-?[1-9][0-9]*)/[1-9][0-9]*',v):
        raise Invalid('canonical rational scalar')
    a,b=map(int,v.split('/')); f=Fraction(a,b)
    if f'{f.numerator}/{f.denominator}'!=v: raise Invalid('unreduced rational')
    return f

def vector(v,n=None,cap=8):
    if type(v) is not list or not 1<=len(v)<=cap or (n is not None and len(v)!=n): raise Invalid('vector dimension')
    return [rational(x) for x in v]

def keys(o,expected):
    if type(o) is not dict or set(o)!=set(expected): raise Invalid('object keys')

def assemble(model):
    keys(model,('x','dt','maps','targets','limit','slew','previous'))
    x=vector(model['x'],cap=4); d=len(x)
    dt=vector(model['dt']); n=len(dt)
    lim=vector(model['limit'],cap=4); m=len(lim)
    slew=vector(model['slew'],m,4); prev=vector(model['previous'],m,4)
    if any(v<=0 for v in dt+lim) or any(v<0 for v in slew) or any(abs(p)>l for p,l in zip(prev,lim)): raise Invalid('model bounds')
    Bs=model['maps'];ys=model['targets']
    if type(Bs) is not list or not 1<=len(Bs)<=8 or type(ys) is not list or len(ys)!=len(Bs): raise Invalid('scenario dimension')
    matrices=[]; targets=[]
    for B,y in zip(Bs,ys):
        if type(B) is not list or len(B)!=d: raise Invalid('map dimension')
        matrices.append([vector(row,m,4) for row in B]);targets.append(vector(y,d,4))
    size=n*m+1; A=[];b=[]; labels=[]
    def add(row,rhs,label): A.append(row);b.append(rhs);labels.append(label)
    def empty():return [Fraction(0)]*size
    for k in range(n):
        for j in range(m):
            for sign,name in ((1,'upper'),(-1,'lower')):
                row=empty();row[k*m+j]=sign
                add(row,lim[j],f'actuator:{k}:{j}:{name}')
    for k in range(n):
        for j in range(m):
            for sign,name in ((1,'upper'),(-1,'lower')):
                row=empty();row[k*m+j]=sign
                if k:row[(k-1)*m+j]=-sign
                offset=prev[j] if k==0 else 0
                add(row,slew[j]*dt[k]+sign*offset,f'slew:{k}:{j}:{name}')
    for s,(B,y) in enumerate(zip(matrices,targets)):
        for i in range(d):
            for sign,name in ((1,'upper'),(-1,'lower')):
                row=empty()
                for k in range(n):
                    for j in range(m):row[k*m+j]=sign*dt[k]*B[i][j]
                row[-1]=-1
                add(row,sign*(y[i]-x[i]),f'terminal:{s}:{i}:{name}')
    row=empty();row[-1]=-1;add(row,Fraction(0),'epigraph:lower')
    c=empty();c[-1]=1
    return A,b,c,labels

def scalar_text(x):return f'{x.numerator}/{x.denominator}'

def verify(model,witness):
    try:
        A,b,c,labels=assemble(model)
        if witness is None:return {'status':'UNAVAILABLE','reason':'missing witness'}
        keys(witness,('z','lambda'))
        z=vector(witness['z'],len(c),33); lam=vector(witness['lambda'],len(A),400)
        if any(l<0 for l in lam):raise Invalid('negative multiplier')
        slack=[rhs-sum(a*v for a,v in zip(row,z)) for row,rhs in zip(A,b)]
        if any(v<0 for v in slack):raise Invalid('primal infeasible')
        station=[cj+sum(row[j]*l for row,l in zip(A,lam)) for j,cj in enumerate(c)]
        if any(station):raise Invalid('stationarity')
        primal=sum(v*w for v,w in zip(c,z));dual=-sum(rhs*l for rhs,l in zip(b,lam))
        if primal!=dual:raise Invalid('objective gap')
        return {'status':'VERIFIED','reason':'exact matching feasible bounds','primal':scalar_text(primal),'dual':scalar_text(dual),'row_count':len(A),'variable_count':len(c),'complementarity':[scalar_text(s*l) for s,l in zip(slack,lam)]}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}

# Admission: 128KiB, JSON nesting<=10, exact keys subsequently, duplicate/NaN refused.
def load_bytes(data):
    if type(data) is not bytes or len(data)>131072:raise Invalid('JSON byte cap')
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise Invalid('duplicate key')
            out[k]=v
        return out
    try:
        obj=json.loads(data.decode('utf-8'),object_pairs_hook=pairs,parse_int=lambda s:int(s) if len(s)<=80 else (_ for _ in ()).throw(Invalid('integer token length')),parse_constant=lambda s:(_ for _ in ()).throw(Invalid('JSON nonfinite')))
    except (UnicodeError,ValueError,RecursionError) as e:raise Invalid('JSON encoding/syntax') from e
    def depth(v,k=0):
        if k>10:raise Invalid('JSON depth')
        if type(v) is list:
            for a in v:depth(a,k+1)
        if type(v) is dict:
            for a in v.values():depth(a,k+1)
    depth(obj);return obj
