"""No solver call: independent original topology and exposure predecessor witness."""
import heapq,json
from model import model,witness,Invalid
from proof import original_t7_proof,original

def classify(s):
    G,n,_,_,_,_=model(s);states,ed=original_t7_proof.distances(s)
    if ed[0] is None:return 'no_allowed_turn_path'
    if ed[0]>s['budget']:return 'budget_infeasible'
    # Independent synchronous scenario ledger; original topology arc order.
    _,ds=original.distances(s);_,arcs=original_t7_proof.topology(s)
    out=[[] for _ in states]
    for a,b,c in arcs:out[a].append((b,c))
    d=[None]*len(states);d[0]=0;q=[(0,0,0)];serial=0;prev={};sink=len(states)-1
    while q:
        cost,_,v=heapq.heappop(q)
        if cost!=d[v]:continue
        if v==sink:break
        for b,c in out[v]:
            new=cost+c
            if d[b] is None or new<d[b]:d[b]=new;prev[b]=v;serial+=1;heapq.heappush(q,(new,serial,b))
    selected=[];v=sink;seen=set()
    while v!=0:
        if v in seen or v not in prev:raise Invalid('sidecar predecessor')
        seen.add(v)
        if v!=sink:selected.append(states[v]['incoming'])
        v=prev[v]
    selected.reverse();path=[s['start']];edges=[];totals=[0]*n;exposure=turn=0;inc=None
    penalties={(tuple(p['incoming']),tuple(p['outgoing'])):p['delay'] for p in s['penalties']}
    for a,i in selected:
        e=G[a][i];edge=(a,i);delay=penalties.get((inc,edge),0) if inc is not None else 0
        path.append(e['target']);edges.append({'source':a,'edge_index':i,'target':e['target']});totals=[x+y+delay for x,y in zip(totals,e['scenario_times'])];exposure+=e['exposure'];turn+=delay;inc=edge
    r={'path':path,'edges':edges,'scenario_totals':totals,'worst_time':max(totals),'exposure':exposure,'turn_penalty':turn};W=witness(s,r)['worst_time']
    if any(row[0] is None for row in ds):raise Invalid('sidecar scenario None')
    L=max(row[0] for row in ds)
    if L>W:raise Invalid('sidecar lower above upper')
    return 'equality_exit' if L==W else 'strict_gap_search'

if __name__=='__main__':
    from pathlib import Path
    cases=json.loads(Path('cases.json').read_text());Path('classes.json').write_text(json.dumps([classify(c['statement']) for c in cases],indent=2)+'\n')
