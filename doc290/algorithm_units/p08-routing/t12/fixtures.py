import random
from model import model

def edge(t,ss,x):return {'target':t,'time':1,'exposure':x,'scenario_times':ss}
def oracle(s):
    G,n,_,_,_,_=model(s);forbidden={(tuple(r[0]),tuple(r[1])) for r in s['forbidden']};penalties={(tuple(p['incoming']),tuple(p['outgoing'])):p['delay'] for p in s['penalties']};best=[]
    def visit(v,inc,seen,exposure,totals):
        if v==s['goal']:best.append(max(totals));return
        for i,e in enumerate(G[v]):
            out=(v,i);state=(e['target'],out);key=(inc,out)
            if state in seen or (inc is not None and key in forbidden):continue
            risk=exposure+e['exposure']
            if risk>s['budget']:continue
            delay=penalties.get(key,0) if inc is not None else 0
            visit(e['target'],out,seen|{state},risk,[totals[k]+e['scenario_times'][k]+delay for k in range(n)])
    visit(s['start'],None,{(s['start'],None)},0,[0]*n)
    return min(best) if best else None

def cases():
    rng=random.Random(223606);out=[]
    for n in range(200):
        G={v:[] for v in 'abcd'}
        for a in G:
            for b in G:
                if a==b:continue
                if rng.random()<.25:
                    ss=[rng.randrange(0,7) for _ in range(3)];x=rng.randrange(0,5);G[a].append(edge(b,ss,x))
        for v in G:
            if rng.random()<.10:G[v].append(edge(v,[0,0,0],0))
        if not any(G.values()):G['d'].append(edge('d',[0,0,0],0))
        forbidden=[];penalties=[]
        for a in sorted(G):
            for i,e in enumerate(G[a]):
                for j,following in enumerate(G[e['target']]):
                    incoming=[a,i];outgoing=[e['target'],j]
                    if rng.random()<.15:forbidden.append([incoming,outgoing])
                    if rng.random()<.25:penalties.append({'incoming':incoming,'outgoing':outgoing,'delay':rng.randrange(0,4)})
        s={'graph':G,'start':'a','goal':'d','budget':rng.randrange(0,13),'forbidden':forbidden,'penalties':penalties};out.append({'name':f'turn{n:03}','statement':s,'oracle':oracle(s),'oracle_kind':'independent original incoming-edge simple-state-path budget DFS'})
    return out

def development():
    base={'graph':{'q':[edge('z',[1,1],0),edge('z',[0,0],2)],'z':[edge('q',[0,0],0)]},'start':'q','goal':'z','budget':0,'forbidden':[[['q',0],['z',0]]],'penalties':[]}
    import copy
    strict=copy.deepcopy(base);strict['graph']['q'][0]['scenario_times']=[3,3]
    negative=copy.deepcopy(base);negative['budget']=9
    no=copy.deepcopy(base);no['graph']['q']=[];no['start']='q';no['goal']='z';no['forbidden']=[]
    identity=copy.deepcopy(base);identity['goal']='q'
    prune={'graph':{'a':[edge('g',[5,5],0),edge('g',[0,0],2),edge('b',[0,0],1)],'b':[edge('g',[0,0],6),edge('g',[6,6],0)],'g':[]},'start':'a','goal':'g','budget':1,'forbidden':[],'penalties':[]}
    budgetloss=copy.deepcopy(base);budgetloss['graph']['q']=[edge('z',[1,1],3)];budgetloss['forbidden']=[]
    oldequal=copy.deepcopy(base);oldequal['graph']['q']=[edge('z',[2,2],0)]
    return [{'name':'dev:'+str(k),'statement':s,'oracle':oracle(s)} for k,s in enumerate([base,strict,negative,no,identity,prune,budgetloss,oldequal])]
