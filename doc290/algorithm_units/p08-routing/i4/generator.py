import heapq
from fractions import Fraction
from pathlib import Path
from model import model,i3,Invalid,Failure,Domain,text,SPEC_PATH,component
from proof import audit,guarded_potential,reconcile

def candidates(n):
    weights=[]
    for k in range(n):weights.append(tuple(Fraction(int(j==k)) for j in range(n)))
    uniform=tuple(Fraction(1,n) for _ in range(n))
    if uniform not in weights:weights.append(uniform)
    return [(w,l) for w in weights for l in (Fraction(0),Fraction(1,2),Fraction(1),Fraction(2))]

def reverse(states,arcs,G,w,lam):
    incoming=[[] for _ in states]
    for a in arcs:
        if a['edge'] is None:c=Fraction(0)
        else:
            v,j=a['edge'];e=G[v][j];ss=[component(x+a['delay']) for x in e['scenario_times']];c=sum(x*y for x,y in zip(w,ss))+lam*e['exposure'];text(c)
        incoming[a['target']].append((a['source'],c))
    d=[None]*len(states);d[-1]=Fraction(0);q=[(Fraction(0),len(states)-1)]
    while q:
        c,v=heapq.heappop(q)
        if c!=d[v]:continue
        for a,x in incoming[v]:
            new=c+x
            if d[a] is None or new<d[a]:d[a]=new;heapq.heappush(q,(new,a))
    return d

def invoke_i3(s):
    if Path(i3.__file__).resolve()!=SPEC_PATH.resolve():raise Failure('loaded I3 checker path')
    bindings=[(i3.b3,'b3/certificate.py'),(i3.b3.t2,'t2/certificate.py'),(i3.b3.t2.helper,'t1/validate.py'),(i3.b3.t2.helper.helper,'c1/validate.py')]
    for module,path in bindings:
        if Path(module.__file__).resolve()!=(SPEC_PATH.parent.parent/path).resolve():raise Failure('loaded transitive checker path')
    return i3.check(s)

def generate(s):
    try:G,n,states,arcs,primal=model(s)
    except (Invalid,KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':str(e),'candidates':[]}
    if s['route'] is None:return {'status':'UNAVAILABLE','reason':'missing route after model checks','candidates':[]}
    rows=[];best=None;bestindex=None
    for index,(w,lam) in enumerate(candidates(n)):
        row={'index':index,'weights':[text(x) for x in w],'multiplier':text(lam)}
        try:
            d=reverse(states,arcs,G,w,lam)
            actual_arcs=audit(s,w,lam,states,d) # precedence: audit BEFORE topology guard
            row.update(states=states,distances=[None if v is None else text(v) for v in d])
            construction=guarded_potential(d,actual_arcs)
            if construction is None:row.update(status='UNAVAILABLE_TOPOLOGY',reason='audited None-to-finite arc; no emission');rows.append(row);continue
            h,M=construction;row.update(clamp=text(M),potential=[text(x) for x in h])
            # Numeric-domain check before emission; unchanged I3 still checks every emission.
            for v in (sum(x*y for x,y in zip(w,primal['scenario_totals'])),sum(x*y for x,y in zip(w,primal['scenario_totals']))+lam*primal['exposure'],lam*s['budget'],h[-1]-lam*s['budget']):text(v)
            supplied=dict(s,weights=[text(x) for x in w],multiplier=text(lam),potential=[text(x) for x in h]);result=invoke_i3(supplied)
            LB=reconcile(s,w,lam,h,actual_arcs,primal,result);row.update(status=result['status'],checker=result,lower_bound=text(LB),gap=text(Fraction(primal['worst_time'])-LB))
            if best is None or LB>best:best=LB;bestindex=index
        except Domain as e:row.update(status='UNAVAILABLE_DOMAIN',reason=str(e))
        rows.append(row)
    status='UNAVAILABLE_DOMAIN' if best is None else 'CERTIFIED_INTEGRATED' if best==primal['worst_time'] else 'UNAVAILABLE'
    return {'status':status,'reason':'finite exact candidate search; no completeness','selected_index':bestindex,'best_lower':None if best is None else text(best),'gap':None if best is None else text(Fraction(primal['worst_time'])-best),'primal':primal,'candidates':rows}
