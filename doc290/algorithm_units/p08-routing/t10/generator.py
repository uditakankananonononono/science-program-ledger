"""Standard all-state reverse integer exposure Dijkstra, unchanged T5 proof."""
import copy,heapq
from model import model,t5,Invalid,Failure
def minima(states,arcs):
    incoming=[[] for _ in states]
    for a in arcs:incoming[a['target']].append((a['source'],a['exposure']))
    d=[None]*len(states);d[-1]=0;heap=[(0,len(states)-1)]
    while heap:
        value,v=heapq.heappop(heap)
        if d[v]!=value:continue
        for u,cost in incoming[v]:
            candidate=value+cost
            if d[u] is None or candidate<d[u]:d[u]=candidate;heapq.heappush(heap,(candidate,u))
    return d

def generate(s):
    base={'status':None,'reason':'','original':copy.deepcopy(s)}
    try:G,states,arcs,budget=model(s)
    except (Invalid,KeyError,TypeError,IndexError,AttributeError) as e:return dict(base,status='INVALID',reason=str(e))
    if s['distances'] is not None:
        checked=t5.check(s)
        if checked['status']=='INVALID':return dict(base,status='INVALID',reason='invalid supplied proof',downstream=checked)
        return dict(base,status='PRESERVED',reason='supplied proof checked and preserved',proof_source='supplied',completed_statement=copy.deepcopy(s),downstream=checked)
    d=minima(states,arcs)
    if any(v is not None and (type(v) is not int or not 0<=v<=t5.MAX*129) for v in d):raise Failure('synthesis distance bound/type')
    completed=copy.deepcopy(s);completed['distances']=d;checked=t5.check(completed)
    status='CERTIFIED_NO_TURN_PATH' if d[0] is None else 'CERTIFIED_BUDGET_INFEASIBLE' if d[0]>budget else 'UNAVAILABLE'
    if checked['status']!=status or checked['states']!=states or checked['exposure_arcs']!=arcs or checked['distances']!=d or checked['source_minimum']!=d[0]:raise Failure('synthesized checker/source/fullledger mismatch')
    return dict(base,status='COMPLETED',reason='full exact exposure proof completed, downstream status separate',proof_source='completed',completed_statement=completed,states=states,exposure_arcs=arcs,distances=d,source_minimum=d[0],downstream=checked)
