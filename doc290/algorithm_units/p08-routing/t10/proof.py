"""Raw original indexed topology + exact all-pairs exposure Floyd sink column."""
import json,copy
from model import model,t5,Invalid,Failure

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def raw(s):
    G=s['graph'];ids=[(a,j) for a in sorted(G) for j in range(len(G[a]))];pos={a:k+1 for k,a in enumerate(ids)};sink=len(ids)+1
    st=[{'kind':'source','vertex':s['start'],'incoming':None}]+[{'kind':'edge','vertex':G[a][j]['target'],'incoming':[a,j]} for a,j in ids]+[{'kind':'goal','vertex':s['goal'],'incoming':None}]
    banned={(tuple(x),tuple(y)) for x,y in s['forbidden']};delays={(tuple(x['incoming']),tuple(x['outgoing'])):x['delay'] for x in s['penalties']};aa=[]
    def add(a,b,e,delay):aa.append({'source':a,'target':b,'edge':e,'exposure':0 if e is None else G[e[0]][e[1]]['exposure'],'delay_ignored':delay})
    for j in range(len(G[s['start']])):add(0,pos[(s['start'],j)],[s['start'],j],0)
    if s['start']==s['goal']:add(0,sink,None,0)
    for inc in ids:
        a,j=inc;v=G[a][j]['target']
        for k in range(len(G[v])):
            out=(v,k)
            if (inc,out) not in banned:add(pos[inc],pos[out],[v,k],delays.get((inc,out),0))
        if v==s['goal']:add(pos[inc],sink,None,0)
    return st,aa

def floyd(states,arcs):
    n=len(states);m=[[None]*n for _ in range(n)]
    for k in range(n):m[k][k]=0
    for a in arcs:
        u,v,c=a['source'],a['target'],a['exposure']
        if m[u][v] is None or c<m[u][v]:m[u][v]=c
    for k in range(n):
        for i in range(n):
            if m[i][k] is None:continue
            for j in range(n):
                if m[k][j] is None:continue
                v=m[i][k]+m[k][j]
                if m[i][j] is None or v<m[i][j]:m[i][j]=v
    return [row[-1] for row in m]

def verify(s,result):
    base={'status','reason','original'}
    if type(result) is not dict or not base<=set(result) or type(result['reason']) is not str or canonical(result['original'])!=canonical(s):raise Failure('typed original/reason schema')
    try:G,states,arcs,budget=model(s)
    except (Invalid,KeyError,TypeError,IndexError,AttributeError):
        if set(result)!=base or result['status']!='INVALID':raise Failure('model invalid precedence/schema')
        return
    st,aa=raw(s);d=floyd(st,aa)
    if canonical(st)!=canonical(states) or canonical(aa)!=canonical(arcs):raise Failure('parent raw topology')
    # Reconstruct EXACT T5 result independently; do not trust checker metadata.
    def expected(supplied):
        if type(supplied) is not list or len(supplied)!=len(st) or any(v is not None and (type(v) is not int or not 0<=v<=t5.MAX*129) for v in supplied) or canonical(supplied)!=canonical(d):return None
        status='CERTIFIED_NO_TURN_PATH' if d[0] is None else 'CERTIFIED_BUDGET_INFEASIBLE' if d[0]>budget else 'UNAVAILABLE'
        reason='no allowed turn path' if d[0] is None else 'all allowed paths over exposure budget' if d[0]>budget else 'minimum exposure feasible, no optimal scenario claim'
        return {'status':status,'reason':reason,'states':st,'exposure_arcs':aa,'distances':d,'source_minimum':d[0],'budget':budget}
    if s['distances'] is not None:
        e=expected(s['distances']);checked=t5.check(s)
        if e is None:
            if set(result)!=base|{'downstream'} or result['status']!='INVALID' or checked['status']!='INVALID' or canonical(result['downstream'])!=canonical(checked):raise Failure('supplied corrupted proof not repaired/schema')
            return
        values={'proof_source':'supplied','completed_statement':copy.deepcopy(s),'downstream':e};status='PRESERVED'
    else:
        if any(v is not None and not 0<=v<=t5.MAX*129 for v in d):raise Failure('parent129MAX proof cap')
        completed=copy.deepcopy(s);completed['distances']=d;values={'proof_source':'completed','completed_statement':completed,'states':st,'exposure_arcs':aa,'distances':d,'source_minimum':d[0],'downstream':expected(d)};status='COMPLETED';checked=t5.check(completed)
    if canonical(checked)!=canonical(values['downstream']):raise Failure('unchanged checker/Floyd reconciliation')
    if set(result)!=base|set(values) or result['status']!=status or any(canonical(result[k])!=canonical(v) for k,v in values.items()):raise Failure('full exact typed preservation/Floyd/result schema')
