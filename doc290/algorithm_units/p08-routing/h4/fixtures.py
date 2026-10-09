"""Fresh corpus; permutation/index-product oracle, NO solver imports."""
import random,itertools
from model import model,integer

def edge(t,ss):return {'target':t,'time':1,'exposure':0,'scenario_times':ss}
def oracle(s):
    G,ns=model(s);values=[];start=s['start'];goal=s['goal']
    if start==goal:return 0
    interior=sorted(v for v in G if v not in (start,goal))
    for length in range(len(interior)+1):
        for middle in itertools.permutations(interior,length):
            path=(start,)+middle+(goal,);choices=[[i for i,e in enumerate(G[a]) if e['target']==b] for a,b in zip(path,path[1:])]
            if not all(choices):continue
            for indices in itertools.product(*choices):
                totals=[0]*ns
                for a,i in zip(path,indices):
                    costs=G[a][i]['scenario_times']
                    # explicit indexing, not zip-coercing dimensions
                    totals=[integer(totals[k]+costs[k]) for k in range(ns)]
                values.append(max(totals))
    return min(values) if values else None

def cases():
    rng=random.Random(271828);out=[]
    for n in range(200):
        G={v:[] for v in 'abcdef'}
        for a in G:
            for b in G:
                if a==b:continue
                if rng.random()<.30:
                    G[a].append(edge(b,[rng.randrange(0,8) for _ in range(3)]))
                    if rng.random()<.20:G[a].append(edge(b,[rng.randrange(0,8) for _ in range(3)]))
        for v in G:
            if rng.random()<.15:G[v].append(edge(v,[0,0,0]))
        if not any(G.values()):G['f'].append(edge('f',[0,0,0]))
        s={'graph':G,'start':'a','goal':'f'};out.append({'name':f'fresh{n:03}','statement':s,'oracle':oracle(s),'oracle_kind':'independent vertex permutations and original adjacency index products'})
    return out
