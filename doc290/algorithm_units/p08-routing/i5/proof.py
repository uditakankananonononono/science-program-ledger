"""Independent raw arcs, iterative original-state traversal and envelope audit."""
import importlib.util,json
from fractions import Fraction as F
from pathlib import Path
from model import model,i3,Failure,Domain,text,SPEC_PATH
spec=importlib.util.spec_from_file_location('i5_original_i4_proof',Path(__file__).resolve().parent.parent/'i4'/'proof.py');cert=importlib.util.module_from_spec(spec);spec.loader.exec_module(cert)
# Exports required by the unchanged imported I4 generator. Not the expected schedule.
audit=cert.audit;guarded_potential=cert.guarded_potential;reconcile=cert.reconcile

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def fraction(x):return f'{x.numerator}/{x.denominator}'

def raw_topology(s):
    G=s['graph'];ids=[(a,j) for a in sorted(G) for j in range(len(G[a]))];pos={e:k+1 for k,e in enumerate(ids)};sink=len(ids)+1
    states=[{'kind':'source','vertex':s['start'],'incoming':None}]+[{'kind':'edge','vertex':G[a][j]['target'],'incoming':[a,j]} for a,j in ids]+[{'kind':'goal','vertex':s['goal'],'incoming':None}]
    f={(tuple(r[0]),tuple(r[1])) for r in s['forbidden']};pen={(tuple(p['incoming']),tuple(p['outgoing'])):p['delay'] for p in s['penalties']};arcs=[]
    for j,e in enumerate(G[s['start']]):arcs.append((0,pos[(s['start'],j)],[s['start'],j],0))
    if s['start']==s['goal']:arcs.append((0,sink,None,0))
    for inc in ids:
        a,j=inc;v=G[a][j]['target']
        for k,e in enumerate(G[v]):
            out=(v,k)
            if (inc,out) not in f:arcs.append((pos[inc],pos[out],[v,k],pen.get((inc,out),0)))
        if v==s['goal']:arcs.append((pos[inc],sink,None,0))
    if len({(a,b) for a,b,e,d in arcs})!=len(arcs):raise Failure('parent unique state arc assumption')
    return states,arcs

def raw_paths(s,n):
    states,arcs=raw_topology(s);G=s['graph'];stack=[(0,(0,),(),0,(0,)*n)];found=[];sink=len(states)-1
    while stack:
        v,seen,indices,r,totals=stack.pop()
        if v==sink:
            found.append({'arcs':list(indices),'exposure':r,'scenario_totals':list(totals)})
            if len(found)==65:return found,True
            continue
        following=[]
        for k,(a,b,e,delay) in enumerate(arcs):
            if a!=v or b in seen:continue
            edge=None if e is None else G[e[0]][e[1]];x=0 if edge is None else edge['exposure'];ss=[0]*n if edge is None else [c+delay for c in edge['scenario_times']]
            following.append((b,seen+(b,),indices+(k,),r+x,tuple(c+d for c,d in zip(totals,ss))))
        stack.extend(reversed(following))
    return found,False

def parametric(raw,w,budget):
    affine=[(sum(w[k]*p['scenario_totals'][k] for k in range(len(w))),F(p['exposure']-budget)) for p in raw]
    if not affine or min(slope for _,slope in affine)>0:raise Failure('parent feasible ray')
    xs=[F(0)]
    for j in range(len(affine)):
        for k in range(j):
            intercept,slope=affine[j];other,oslope=affine[k]
            if slope!=oslope:
                x=(other-intercept)/(slope-oslope)
                if x>=0:xs.append(x)
    rows=[];highest=None;selected=None
    for x in sorted(set(xs)):
        ys=[b+x*m for b,m in affine];low=min(ys);rows.append({'lambda':fraction(x),'lower_bound':fraction(low),'active_paths':[k for k,y in enumerate(ys) if y==low]})
        if highest is None or low>highest:highest=low;selected=x
    return affine,rows,selected,highest

def verify(s,result):
    G,n,states,arcs,primal=model(s)
    if type(result) is not dict:raise Failure('result dict')
    short={'status','reason','paths','weights'}
    if s['route'] is None:
        if set(result)!=short or type(result['reason']) is not str or result['status']!='UNAVAILABLE' or result['paths']!=[] or result['weights']!=[]:raise Failure('missing route category/schema')
        return
    if sum(map(len,G.values()))>6:
        if set(result)!=short or type(result['reason']) is not str or result['status']!='UNAVAILABLE_DOMAIN' or result['paths']!=[] or result['weights']!=[]:raise Failure('model domain category/schema')
        return
    raw,overflow=raw_paths(s,n)
    if overflow:
        if set(result)!=short or type(result['reason']) is not str or result['status']!='UNAVAILABLE_ENUMERATION' or canonical(result['paths'])!=canonical(raw) or result['weights']!=[]:raise Failure('enumeration no-prefix category')
        return
    if set(result)!={'status','reason','primal','paths','weights','selected_weight','best_lower','gap'} or type(result['reason']) is not str or canonical(result['primal'])!=canonical(primal) or canonical(result['paths'])!=canonical(raw):raise Failure('parent top/path/primal schema')
    if not raw or min(p['exposure'] for p in raw)>s['budget']:raise Failure('parent feasible path contradiction')
    ww=[tuple(F(1 if j==k else 0,1) for j in range(n)) for k in range(n)];u=tuple(F(1,n) for _ in range(n))
    if u not in ww:ww.append(u)
    rows=result['weights']
    if type(rows) is not list or len(rows)!=len(ww):raise Failure('parent complete weights')
    best=None;selected=None
    for k,(row,w) in enumerate(zip(rows,ww)):
        lines,points,lam,LB=parametric(raw,w,s['budget']);base={'index':k,'weights':[fraction(x) for x in w],'lines':[{'intercept':fraction(a),'slope':int(b)} for a,b in lines],'points':points,'selected_lambda':fraction(lam),'optimal_lower':fraction(LB),'minimum_slope':int(min(b for a,b in lines))}
        if type(row) is not dict or type(row.get('index')) is not int or any(key not in row or canonical(row[key])!=canonical(v) for key,v in base.items()):raise Failure('parent whole-path charge/envelope/schedule/type binding')
        stages={};expected_status=None;checker=None
        try:
            text(lam);st,aa,dd=cert.distances(s,w,lam)
            represented=[None if v is None else text(v) for v in dd];stages.update(states=st,distances=represented)
            construction=cert.guarded_potential(dd,aa)
            if construction is None:expected_status='UNAVAILABLE_TOPOLOGY'
            else:
                h,M=construction;stages.update(clamp=text(M),potential=[text(x) for x in h])
                for v in (sum(a*b for a,b in zip(w,primal['scenario_totals'])),sum(a*b for a,b in zip(w,primal['scenario_totals']))+lam*primal['exposure'],lam*s['budget'],h[-1]-lam*s['budget']):text(v)
                if Path(i3.__file__).resolve()!=SPEC_PATH.resolve():raise Failure('parent unchanged I3 path')
                checker=i3.check(dict(s,weights=[text(x) for x in w],multiplier=text(lam),potential=[text(x) for x in h]));actual=cert.reconcile(s,w,lam,h,aa,primal,checker)
                if actual!=LB:raise Failure('parent path vs fullstate dual')
                expected_status=checker['status']
                if best is None or LB>best:best=LB;selected=k
        except Domain:expected_status='UNAVAILABLE_DOMAIN'
        expectedkeys=set(base)|set(stages)|{'status'}|({'checker'} if checker is not None else {'reason'})
        if set(row)!=expectedkeys or row['status']!=expected_status or any(canonical(row[key])!=canonical(v) for key,v in stages.items()):raise Failure('parent candidate exact stage/domain/schema')
        if checker is not None and canonical(row['checker'])!=canonical(checker):raise Failure('parent checker reconciliation')
        if checker is None and type(row['reason']) is not str:raise Failure('refusal reason')
    status='UNAVAILABLE_DOMAIN' if best is None else 'CERTIFIED_INTEGRATED' if best==primal['worst_time'] else 'UNAVAILABLE'
    if result['selected_weight'] is not None and type(result['selected_weight']) is not int:raise Failure('selected strict index')
    if result['status']!=status or result['selected_weight']!=selected or result['best_lower']!=(None if best is None else text(best)) or result['gap']!=(None if best is None else text(F(primal['worst_time'])-best)):raise Failure('parent overall selection/gap')
