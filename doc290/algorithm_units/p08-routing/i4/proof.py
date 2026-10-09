"""Raw-original topology/Fraction synchronous BF, independent of generator arcs."""
from fractions import Fraction
from model import model,Failure,Domain,integer,text,i3,component

def topology(s,w,lam):
    G=s['graph'];ids=[(a,j) for a in sorted(G) for j in range(len(G[a]))];pos={e:k+1 for k,e in enumerate(ids)};sink=len(ids)+1
    states=[{'kind':'source','vertex':s['start'],'incoming':None}]+[{'kind':'edge','vertex':G[a][j]['target'],'incoming':[a,j]} for a,j in ids]+[{'kind':'goal','vertex':s['goal'],'incoming':None}]
    forbidden={(tuple(r[0]),tuple(r[1])) for r in s['forbidden']};penalties={(tuple(p['incoming']),tuple(p['outgoing'])):p['delay'] for p in s['penalties']};arcs=[]
    def cost(e,delay):
        ss=[component(x+delay) for x in e['scenario_times']];c=sum(a*b for a,b in zip(w,ss))+lam*e['exposure'];text(c);return c
    for j,e in enumerate(G[s['start']]):arcs.append((0,pos[(s['start'],j)],cost(e,0),[s['start'],j],0))
    if s['start']==s['goal']:arcs.append((0,sink,Fraction(0),None,0))
    for a,j in ids:
        v=G[a][j]['target'];inc=(a,j)
        for k,e in enumerate(G[v]):
            out=(v,k)
            if (inc,out) not in forbidden:
                delay=penalties.get((inc,out),0);arcs.append((pos[inc],pos[out],cost(e,delay),[v,k],delay))
        if v==s['goal']:arcs.append((pos[inc],sink,Fraction(0),None,0))
    return states,arcs

def distances(s,w,lam):
    states,arcs=topology(s,w,lam);d=[None]*len(states);d[-1]=Fraction(0)
    for _ in range(len(states)-1):
        old=d;d=old[:]
        for a,b,c,_,_ in arcs:
            if old[b] is not None:
                v=c+old[b]
                if d[a] is None or v<d[a]:d[a]=v
    return states,arcs,d

def audit(s,w,lam,states,d):
    actual,arcs,expected=distances(s,w,lam)
    import json
    if json.dumps(states,sort_keys=True)!=json.dumps(actual,sort_keys=True) or len(d)!=len(expected) or any(x is not None and type(x) is not Fraction for x in d) or d!=expected:raise Failure('independent original weighted distances mismatch')
    return arcs

def guarded_potential(d,arcs):
    if d[0] is None:raise Failure('finite primal but source distance None')
    if any(d[a] is None and d[b] is not None for a,b,*_ in arcs):return None
    M=max(x for x in d if x is not None);D=d[0];h=[D-(x if x is not None else M) for x in d]
    for v in h:text(v)
    if h[0]!=0 or h[-1]!=D or any(c+h[a]-h[b]<0 for a,b,c,*_ in arcs):raise Failure('full-state potential construction/slack')
    return h,M

def reconcile(s,w,lam,h,arcs,primal,result):
    W=primal['worst_time'];weighted=sum(x*y for x,y in zip(w,primal['scenario_totals']));weightedpath=weighted+lam*primal['exposure'];charge=lam*s['budget'];LB=h[-1]-charge
    for v in (weighted,weightedpath,charge,LB):text(v)
    if LB>W:raise Failure('lower above feasible worst')
    expected='CERTIFIED_INTEGRATED' if LB==W else 'UNAVAILABLE'
    if result['status']!=expected:raise Failure('unchanged checker disagreement/INVALID')
    if result['lower_bound']!=text(LB) or result['gap']!=text(Fraction(W)-LB) or result['weighted_scenario_sum']!=text(weighted) or result['weighted_route_cost']!=text(weightedpath) or result['budget_charge']!=text(charge):raise Failure('checker algebra reconciliation')
    # Exact decoded ledgers, not Python bool/float value equality.
    import json
    ledger=[{'source':a,'target':b,'edge':e,'delay':delay,'weighted_cost':text(c),'slack':text(c+h[a]-h[b])} for a,b,c,e,delay in arcs]
    if json.dumps(result['transition_ledger'],sort_keys=True)!=json.dumps(ledger,sort_keys=True):raise Failure('checker original transition ledger')
    if json.dumps(result['primal'],sort_keys=True)!=json.dumps(primal,sort_keys=True):raise Failure('checker primal disagreement')
    return LB

def verify(s,result):
    from model import Invalid,rational
    G,n,states,arcs,primal=model(s)
    import json
    canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    if type(result) is not dict:raise Failure('result dict schema')
    if s['route'] is None:
        if set(result)!={'status','reason','candidates'} or type(result['reason']) is not str or result['status']!='UNAVAILABLE' or result['candidates']!=[]:raise Failure('missing route result')
        return
    if set(result)!={'status','reason','selected_index','best_lower','gap','primal','candidates'} or type(result['reason']) is not str:raise Failure('result exact schema')
    if canonical(result['primal'])!=canonical(primal):raise Failure('top-level primal binding')
    if result['selected_index'] is not None and type(result['selected_index']) is not int:raise Failure('selected index strict type')
    rows=result['candidates']
    # Parent reconstructs the prereg schedule without generator imports.
    weight_rows=[tuple(Fraction(1 if j==k else 0,1) for j in range(n)) for k in range(n)]
    uniform=tuple(Fraction(1,n) for _ in range(n))
    if uniform not in weight_rows:weight_rows.append(uniform)
    expected=[(w,lam) for w in weight_rows for lam in (Fraction(0,1),Fraction(1,2),Fraction(1,1),Fraction(2,1))]
    if type(rows) is not list:raise Failure('candidate list schema')
    if len(rows)!=len(expected):raise Failure('complete finite candidate coverage')
    best=None;selected=None
    for k,(row,(w,lam)) in enumerate(zip(rows,expected)):
        if type(row) is not dict or type(row.get('index')) is not int:raise Failure('candidate index strict type')
        basekeys={'index','weights','multiplier'}
        status=row.get('status')
        if status in ('CERTIFIED_INTEGRATED','UNAVAILABLE'):
            if set(row)!=basekeys|{'states','distances','clamp','potential','status','checker','lower_bound','gap'}:raise Failure('emitted row exact schema')
        elif status=='UNAVAILABLE_TOPOLOGY':
            if set(row)!=basekeys|{'states','distances','status','reason'} or type(row['reason']) is not str:raise Failure('topology row exact schema')
        elif status=='UNAVAILABLE_DOMAIN':
            permitted=basekeys|{'states','distances','clamp','potential','status','reason'}
            if not basekeys|{'status','reason'}<=set(row) or set(row)-permitted or type(row['reason']) is not str:raise Failure('domain row schema')
            if ('states' in row)!=('distances' in row) or ('clamp' in row)!=('potential' in row):raise Failure('domain stage fields')
        else:raise Failure('candidate status schema')
        if row['index']!=k or row['weights']!=[text(v) for v in w] or row['multiplier']!=text(lam):raise Failure('candidate order/parameters')
        try:
            st,aa,dd=distances(s,w,lam)
            import json
            if json.dumps(row.get('states'),sort_keys=True)!=json.dumps(st,sort_keys=True) or row.get('distances')!=[None if v is None else text(v) for v in dd]:raise Failure('receipt original distance ledger')
            constructed=guarded_potential(dd,aa)
            if constructed is None:
                if row['status']!='UNAVAILABLE_TOPOLOGY' or 'checker' in row:raise Failure('topology no-emission')
                continue
            h,M=constructed
            if row['clamp']!=text(M) or row['potential']!=[text(v) for v in h]:raise Failure('receipt clamp/potential')
            for v in (sum(x*y for x,y in zip(w,primal['scenario_totals'])),sum(x*y for x,y in zip(w,primal['scenario_totals']))+lam*primal['exposure'],lam*s['budget'],h[-1]-lam*s['budget']):text(v)
            from model import SPEC_PATH
            from pathlib import Path
            if Path(i3.__file__).resolve()!=SPEC_PATH.resolve():raise Failure('receipt original I3 loaded path')
            check=i3.check(dict(s,weights=[text(v) for v in w],multiplier=text(lam),potential=[text(v) for v in h]));LB=reconcile(s,w,lam,h,aa,primal,check)
            import json
            if json.dumps(check,sort_keys=True)!=json.dumps(row['checker'],sort_keys=True) or row['status']!=check['status'] or row['lower_bound']!=text(LB) or row['gap']!=text(Fraction(primal['worst_time'])-LB):raise Failure('receipt emitted checker/algebra')
            if best is None or LB>best:best=LB;selected=k
        except Domain:
            if row['status']!='UNAVAILABLE_DOMAIN' or 'checker' in row:raise Failure('candidate domain category')
    status='UNAVAILABLE_DOMAIN' if best is None else 'CERTIFIED_INTEGRATED' if best==primal['worst_time'] else 'UNAVAILABLE'
    expectedgap=None if best is None else text(Fraction(primal['worst_time'])-best)
    if result['status']!=status or result['selected_index']!=selected or result['best_lower']!=(None if best is None else text(best)) or result['gap']!=expectedgap:raise Failure('selection/classification')
