"""Established exact Frechet endpoint bounds and finite-menu maximin selection."""
from fractions import Fraction as F
from payload import rational

def interval(p, w, required):
    p=list(map(rational,p));w=list(map(rational,w));required=rational(required)
    if len(p) not in (1,2) or len(w)!=len(p):raise ValueError('one or two agents only')
    if any(not 0<=a<=1 for a in p) or any(a<=0 for a in w) or not 0<required<=sum(w):raise ValueError('probability/payload/threshold')
    if len(p)==1:
        return {'minimum':p[0],'maximum':p[0],'independent':p[0],'endpoint_probabilities':(p[0],p[0]),'joint_target_interval':None}
    a,b=p;lo=max(F(0),a+b-1);hi=min(a,b)
    # state order lost/lost, lost/target, target/lost, target/target
    event=[F(0),F(w[1]>=required),F(w[0]>=required),F(1)]
    def probability(t):
        mass=(1-a-b+t,b-t,a-t,t)
        if min(mass)<0 or sum(mass)!=1:raise RuntimeError('exact mass failure')
        return sum(x*y for x,y in zip(mass,event))
    endpoints=(probability(lo),probability(hi))
    return {'minimum':min(endpoints),'maximum':max(endpoints),'independent':probability(a*b),'endpoint_probabilities':endpoints,'joint_target_interval':(lo,hi)}

def select(menu,total_payload,required):
    total=rational(total_payload);required=rational(required)
    if total<=0 or not 0<required<=total:raise ValueError('budget/threshold')
    menu=list(menu)
    if not menu:raise ValueError('empty menu')
    results=[];seen=set()
    for name,p,w in menu:
        if not isinstance(name,str) or not name.strip() or name in seen:raise ValueError('unique nonempty labels required')
        seen.add(name);w=list(map(rational,w))
        if sum(w)!=total:raise ValueError('unequal payload budget')
        results.append({'name':name,**interval(p,w,required)})
    best=max(row['minimum'] for row in results)
    return {'results':results,'best_guaranteed_probability':best,'maximin_ties':[row['name'] for row in results if row['minimum']==best],
            'scope':'exact target-only one/two-agent supplied-marginal finite-menu maximin; payload budget only, no physical or novelty claim'}
