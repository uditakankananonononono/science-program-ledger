"""Exact parametric lambda search for fixed weights in a capped state domain."""
from fractions import Fraction as F
import importlib.util
from pathlib import Path
from model import model,i3,Invalid,Failure,Domain,text
spec=importlib.util.spec_from_file_location('i5_i4_generator',Path(__file__).resolve().parent.parent/'i4'/'generator.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
spec=importlib.util.spec_from_file_location('i5_i4_proof',Path(__file__).resolve().parent.parent/'i4'/'proof.py');certificate=importlib.util.module_from_spec(spec);spec.loader.exec_module(certificate)

def weights(n):
    rows=[tuple(F(int(j==k)) for j in range(n)) for k in range(n)];u=tuple(F(1,n) for _ in range(n))
    if u not in rows:rows.append(u)
    return rows

def paths(G,n,states,arcs):
    pairs=[(a['source'],a['target']) for a in arcs]
    if len(pairs)!=len(set(pairs)):raise Failure('unique state arc assumption')
    out=[[] for _ in states]
    for k,a in enumerate(arcs):out[a['source']].append((k,a))
    found=[];sink=len(states)-1;overflow=False
    def visit(v,seen,ids,exposure,totals):
        nonlocal overflow
        if overflow:return
        if v==sink:
            found.append({'arcs':ids,'exposure':exposure,'scenario_totals':totals})
            if len(found)>64:overflow=True
            return
        for k,a in out[v]:
            b=a['target']
            if b in seen:continue
            e=None if a['edge'] is None else G[a['edge'][0]][a['edge'][1]]
            x=0 if e is None else e['exposure'];ss=[0]*n if e is None else [v+a['delay'] for v in e['scenario_times']]
            visit(b,seen|{b},ids+[k],exposure+x,[x+y for x,y in zip(totals,ss)])
    visit(0,{0},[],0,[0]*n)
    return found,overflow

def envelope(raw,w,budget):
    lines=[(sum(a*b for a,b in zip(w,p['scenario_totals'])),p['exposure']-budget) for p in raw]
    if not lines or min(b for a,b in lines)>0:raise Failure('feasible primal/ray contradiction')
    points={F(0)}
    for k,(a,b) in enumerate(lines):
        for c,d in lines[k+1:]:
            if b!=d:
                v=(c-a)/(b-d)
                if v>=0:points.add(v)
    rows=[];best=None;selected=None
    for lam in sorted(points):
        values=[a+lam*b for a,b in lines];LB=min(values);rows.append({'lambda':fraction(lam),'lower_bound':fraction(LB),'active_paths':[k for k,v in enumerate(values) if v==LB]})
        if best is None or LB>best:best=LB;selected=lam
    return lines,rows,selected,best

def fraction(v):return f'{v.numerator}/{v.denominator}'

def generate(s):
    try:G,n,states,arcs,primal=model(s)
    except (Invalid,KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':str(e),'paths':[],'weights':[]}
    if s['route'] is None:return {'status':'UNAVAILABLE','reason':'missing route after model','paths':[],'weights':[]}
    if sum(map(len,G.values()))>6:return {'status':'UNAVAILABLE_DOMAIN','reason':'six original edge research cap','paths':[],'weights':[]}
    raw,overflow=paths(G,n,states,arcs)
    if overflow:return {'status':'UNAVAILABLE_ENUMERATION','reason':'65th path; no prefix envelope','paths':raw,'weights':[]}
    if not raw or min(p['exposure'] for p in raw)>s['budget']:raise Failure('valid primal but no simple feasible state path')
    rows=[];best=None;selected=None
    for k,w in enumerate(weights(n)):
        lines,points,lam,LB=envelope(raw,w,s['budget']);row={'index':k,'weights':[fraction(x) for x in w],'lines':[{'intercept':fraction(a),'slope':b} for a,b in lines],'points':points,'selected_lambda':fraction(lam),'optimal_lower':fraction(LB),'minimum_slope':min(b for a,b in lines)}
        try:
            text(lam)
            d=old.reverse(states,arcs,G,w,lam);aa=certificate.audit(s,w,lam,states,d)
            row.update(states=states,distances=[None if x is None else text(x) for x in d])
            hM=certificate.guarded_potential(d,aa)
            if hM is None:row.update(status='UNAVAILABLE_TOPOLOGY',reason='audited None-to-finite; no emission');rows.append(row);continue
            h,M=hM;row.update(clamp=text(M),potential=[text(x) for x in h])
            for v in (sum(a*b for a,b in zip(w,primal['scenario_totals'])),sum(a*b for a,b in zip(w,primal['scenario_totals']))+lam*primal['exposure'],lam*s['budget'],h[-1]-lam*s['budget']):text(v)
            result=old.invoke_i3(dict(s,weights=[text(v) for v in w],multiplier=text(lam),potential=[text(x) for x in h]));actual=certificate.reconcile(s,w,lam,h,aa,primal,result)
            if actual!=LB:raise Failure('path envelope/reverse certificate disagreement')
            row.update(status=result['status'],checker=result)
            if best is None or LB>best:best=LB;selected=k
        except Domain as e:row.update(status='UNAVAILABLE_DOMAIN',reason=str(e))
        rows.append(row)
    return {'status':'UNAVAILABLE_DOMAIN' if best is None else 'CERTIFIED_INTEGRATED' if best==primal['worst_time'] else 'UNAVAILABLE','reason':'exact lambda for fixed weights in small enumerated domain','primal':primal,'paths':raw,'weights':rows,'selected_weight':selected,'best_lower':None if best is None else text(best),'gap':None if best is None else text(F(primal['worst_time'])-best)}
