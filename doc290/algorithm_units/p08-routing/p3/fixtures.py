"""Corpus and independently exhaustive simple-path/analytic frozen oracle."""
import random
from model import model

def edge(t,ss):return {'target':t,'time':1,'exposure':0,'scenario_times':ss}
def exhaustive(s):
    G,ns=model(s);values=[]
    def visit(v,seen,totals):
        if v==s['goal']:values.append(max(totals));return
        for e in G[v]:
            if e['target'] not in seen:visit(e['target'],seen|{e['target']},[x+y for x,y in zip(totals,e['scenario_times'])])
    visit(s['start'],{s['start']},[0]*ns)
    return min(values) if values else None

def cases():
    rng=random.Random(314159);out=[]
    for n in range(100):
        G={v:[] for v in 'abcd'}
        for a in G:
            for b in G:
                if a!=b and rng.random()<.35:G[a].append(edge(b,[rng.randint(0,9),rng.randint(0,9)]))
        if not any(G.values()):G['d'].append(edge('d',[0,0]))
        s={'graph':G,'start':'a','goal':'d'};out.append({'name':f'random{n:03}','statement':s,'oracle':exhaustive(s),'oracle_kind':'independent simple-path enumeration'})
    curated=[('parallel',{'a':[edge('g',[1,5]),edge('g',[5,1])],'g':[]},'a','g'),('identity',{'a':[edge('g',[2,3])],'g':[]},'a','a'),('correlated',{'a':[edge('b',[1,5])],'b':[edge('g',[5,1])],'g':[]},'a','g'),('unreachable',{'a':[edge('b',[1,1])],'b':[],'g':[]},'a','g')]
    for name,G,a,b in curated:
        s={'graph':G,'start':a,'goal':b};out.append({'name':name,'statement':s,'oracle':exhaustive(s),'oracle_kind':'independent simple-path enumeration'})
    for n in (8,10):
        G={f'v{i}':[edge(f'v{i+1}',[2**i,0]),edge(f'v{i+1}',[0,2**i])] for i in range(n)};G[f'v{n}']=[];s={'graph':G,'start':'v0','goal':f'v{n}'};out.append({'name':f'tradeoff{n}','statement':s,'oracle':2**(n-1),'oracle_kind':'analytic subset-sum bijection'})
    return out
