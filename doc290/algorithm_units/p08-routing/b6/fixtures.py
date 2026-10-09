import random,itertools
from model import model,integer

def edge(t,ss,x):return {'target':t,'time':1,'exposure':x,'scenario_times':ss}
def oracle(s):
    G,ns=model(s);values=[]
    if s['start']==s['goal']:return 0
    interior=sorted(v for v in G if v not in (s['start'],s['goal']))
    for length in range(len(interior)+1):
        for middle in itertools.permutations(interior,length):
            path=(s['start'],)+middle+(s['goal'],);choices=[[i for i,e in enumerate(G[a]) if e['target']==b] for a,b in zip(path,path[1:])]
            if not all(choices):continue
            for indices in itertools.product(*choices):
                totals=[0]*ns;exposure=0
                for a,i in zip(path,indices):
                    e=G[a][i];exposure=integer(exposure+e['exposure']);totals=[integer(totals[k]+e['scenario_times'][k]) for k in range(ns)]
                if exposure<=s['budget']:values.append(max(totals))
    return min(values) if values else None

def cases():
    rng=random.Random(173205);out=[]
    for n in range(200):
        G={v:[] for v in 'abcdef'}
        for a in G:
            for b in G:
                if a==b:continue
                if rng.random()<.30:
                    ss=[rng.randrange(0,8) for _ in range(3)];x=rng.randrange(0,9);G[a].append(edge(b,ss,x))
                    if rng.random()<.20:
                        ss=[rng.randrange(0,8) for _ in range(3)];x=rng.randrange(0,9);G[a].append(edge(b,ss,x))
        for v in G:
            if rng.random()<.15:G[v].append(edge(v,[0,0,0],0))
        if not any(G.values()):G['f'].append(edge('f',[0,0,0],0))
        s={'graph':G,'start':'a','goal':'f','budget':rng.randrange(0,25)};out.append({'name':f'budget{n:03}','statement':s,'oracle':oracle(s),'oracle_kind':'independent budget-filtered permutations/index products'})
    return out
