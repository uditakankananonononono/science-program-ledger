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
    rng=random.Random(264575);out=[]
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
