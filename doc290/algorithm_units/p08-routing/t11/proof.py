"""Independent raw charged BF, original incumbent and each bound-event audit."""
import importlib.util,json,heapq
from pathlib import Path
from model import model,witness,Invalid,integer,MAX
spec=importlib.util.spec_from_file_location('t11_original_t9_proof',Path(__file__).resolve().parent.parent/'t9/proof.py');baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
original=baseline.original;original_t7_proof=baseline.original_t7_proof
scenario_check=baseline.scenario_check;incumbent_check=baseline.incumbent_check
BASE_COUNTERS={'reverse_relaxations','candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue','scenario_reverse_inspections','incumbent_inspections','objective_bound_pruned'}
NEW_COUNTERS={'charged_reverse_inspections','charged_bound_stronger','charged_strict_exclusions'}
PHASE={'candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue','objective_bound_pruned'}
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def topology(s):
    G=s['graph'];ids=[(a,j) for a in sorted(G) for j in range(len(G[a]))];pos={e:k+1 for k,e in enumerate(ids)};sink=len(ids)+1;n=next(len(e['scenario_times']) for es in G.values() for e in es)
    states=[{'kind':'source','vertex':s['start'],'incoming':None}]+[{'kind':'edge','vertex':G[a][j]['target'],'incoming':[a,j]} for a,j in ids]+[{'kind':'goal','vertex':s['goal'],'incoming':None}]
    ban={(tuple(x),tuple(y)) for x,y in s['forbidden']};delays={(tuple(x['incoming']),tuple(x['outgoing'])):x['delay'] for x in s['penalties']};aa=[]
    def add(u,v,identity,delay):
        e=None if identity is None else G[identity[0]][identity[1]];risk=0 if e is None else e['exposure'];ss=[0]*n if e is None else [x+delay for x in e['scenario_times']];aa.append({'source':u,'target':v,'edge':identity,'delay':delay,'risk':risk,'scenarios':ss})
    for j in range(len(G[s['start']])):add(0,pos[(s['start'],j)],[s['start'],j],0)
    if s['start']==s['goal']:add(0,sink,None,0)
    for a,j in ids:
        inc=(a,j);v=G[a][j]['target']
        for k in range(len(G[v])):
            out=(v,k)
            if (inc,out) not in ban:add(pos[inc],pos[out],[v,k],delays.get((inc,out),0))
        if v==s['goal']:add(pos[inc],sink,None,0)
    return states,aa

def charged_distances(s):
    model(s);st,aa=topology(s);n=next(len(e['scenario_times']) for es in s['graph'].values() for e in es);allrows=[]
    for k in range(n):
        d=[None]*len(st);d[-1]=0
        for _ in range(len(st)-1):
            old=d;d=d[:]
            for a in aa:
                if old[a['target']] is not None:
                    v=old[a['target']]+a['scenarios'][k]+a['risk'];u=a['source']
                    if d[u] is None or v<d[u]:d[u]=v
        allrows.append(d)
    return st,allrows

def charged_check(s,p):
    states,dd=charged_distances(s)
    if type(p) is not dict or set(p)!={'states','distances','lambda'} or type(p['lambda']) is not int or p['lambda']!=1 or canonical(p)!=canonical({'states':states,'distances':dd,'lambda':1}):raise Invalid('charged full typed raw BF proof')

def incumbent_expected(s):
    st,aa=topology(s);out=[[] for _ in st]
    for a in aa:out[a['source']].append(a)
    d=[None]*len(st);d[0]=0;pred={};q=[(0,0,0)];serial=0
    while q:
        value,_,u=heapq.heappop(q)
        if value!=d[u]:continue
        if u==len(st)-1:break
        for a in out[u]:
            v=a['target'];x=value+a['risk']
            if d[v] is None or x<d[v]:d[v]=x;pred[v]=a;serial+=1;heapq.heappush(q,(x,serial,v))
    if d[-1] is None or d[-1]>s['budget']:raise Invalid('independent incumbent feasibility')
    chosen=[];v=len(st)-1;seen=set()
    while v:
        if v in seen or v not in pred:raise Invalid('independent incumbent chain')
        seen.add(v);a=pred[v];chosen.append(a);v=a['source']
    path=[s['start']];edges=[];ss=[0]*len(aa[0]['scenarios']);r=turn=0
    for a in reversed(chosen):
        if a['edge'] is None:continue
        source,j=a['edge'];target=s['graph'][source][j]['target'];path.append(target);edges.append({'source':source,'edge_index':j,'target':target});r+=a['risk'];turn+=a['delay'];ss=[x+y for x,y in zip(ss,a['scenarios'])]
    return {'path':path,'edges':edges,'exposure':r,'scenario_totals':ss,'worst_time':max(ss),'turn_penalty':turn}

def trace_check(s,trace,ds,charged,W,c):
    if type(trace) is not list:raise Invalid('bound trace list')
    G=s['graph'];n=len(ds);st,aa=topology(s);pos={(a,j):k+1 for k,(a,j) in enumerate((a,j) for a in sorted(G) for j in range(len(G[a])))};ban={(tuple(x),tuple(y)) for x,y in s['forbidden']};pen={(tuple(x['incoming']),tuple(x['outgoing'])):x['delay'] for x in s['penalties']};strong=extra=pruned=0
    for row in trace:
        if type(row) is not dict or set(row)!={'path','indices','state','exposure','totals','old_bound','new_bound','stronger','extra_exclusion','pruned'}:raise Invalid('bound event schema')
        path=row['path'];idx=row['indices']
        if type(path) is not list or len(path)<2 or path[0]!=s['start'] or type(idx) is not list or len(idx)!=len(path)-1:raise Invalid('bound prefix shape')
        totals=[0]*n;r=0;previous=None
        for source,target,j in zip(path,path[1:],idx):
            if type(source) is not str or type(target) is not str or type(j) is not int or source not in G or not 0<=j<len(G[source]) or G[source][j]['target']!=target:raise Invalid('bound original prefix index')
            outgoing=(source,j);pair=(previous,outgoing)
            if previous is not None and pair in ban:raise Invalid('bound forbidden prefix')
            delay=pen.get(pair,0) if previous is not None else 0;edge=G[source][j];r+=edge['exposure'];totals=[x+y+delay for x,y in zip(totals,edge['scenario_times'])];previous=outgoing
        state=pos[previous];suffix=[a[state] for a in ds];ch=[a[state] for a in charged]
        if r>s['budget'] or any(x is None for x in suffix+ch):raise Invalid('bound feasible suffix')
        old=max(x+y for x,y in zip(totals,suffix));new=max(totals[k]+max(suffix[k],ch[k]-(s['budget']-r)) for k in range(n));expected={'state':state,'exposure':r,'totals':totals,'old_bound':old,'new_bound':new,'stronger':new>old,'extra_exclusion':new>W and old<=W,'pruned':new>W}
        if any(canonical(row[k])!=canonical(v) for k,v in expected.items()):raise Invalid('bound budgetcharge/strict/event type binding')
        strong+=int(new>old);extra+=int(new>W and old<=W);pruned+=int(new>W)
    if c['charged_bound_stronger']!=strong or c['charged_strict_exclusions']!=extra or c['objective_bound_pruned']!=pruned:raise Invalid('bound trace counters')

def check(s,payload,certificate=True):
    required={'route','counters','proof','certificate','scenario_proof','incumbent','charged_proof','bound_trace'}
    if type(payload) is not dict or not required<=set(payload):raise Invalid('all top proof stages present')
    original_t7_proof.check(s,payload,certificate=False)
    c=payload.get('counters');names=BASE_COUNTERS|NEW_COUNTERS
    if type(c) is not dict or set(c)!=names:raise Invalid('full counter schema')
    for v in c.values():integer(v)
    cert=payload.get('certificate');fields={'early_exit','equality_exit','reason','budget','lower','upper','old_lower','charged_lambda','source_bound_stronger'}
    if type(cert) is not dict or set(cert)!=fields or type(cert['reason']) is not str or any(type(cert[k]) is not bool for k in ('early_exit','equality_exit','source_bound_stronger')) or type(cert['charged_lambda']) is not int or cert['charged_lambda']!=1 or type(cert['budget']) is not int or cert['budget']!=s['budget']:raise Invalid('T11 typed certificate schema')
    minimum=payload['proof']['start_minimum'];early=minimum is None or minimum>s['budget']
    if cert['early_exit']!=early:raise Invalid('T11 exposure classification')
    if early:
        reason='no_allowed_turn_path' if minimum is None else 'budget_infeasible'
        if cert['reason']!=reason or cert['equality_exit'] or cert['source_bound_stronger'] or any(cert[k] is not None for k in ('lower','upper','old_lower')) or any(payload.get(k) is not None for k in ('route','scenario_proof','incumbent','charged_proof')) or payload.get('bound_trace')!=[]:raise Invalid('early exact metadata')
        if any(c[k]!=0 for k in PHASE|NEW_COUNTERS|{'scenario_reverse_inspections','incumbent_inspections'}):raise Invalid('early zero work')
        return
    scenario_check(s,payload['scenario_proof']);charged_check(s,payload['charged_proof']);W=incumbent_check(s,payload['incumbent'])
    if canonical(payload['incumbent'])!=canonical(incumbent_expected(s)):raise Invalid('identical original exposure-min incumbent')
    ds=payload['scenario_proof']['distances'];charged=payload['charged_proof']['distances']
    if any(row[0] is None for row in ds+charged):raise Invalid('feasible source None')
    oldL=max(row[0] for row in ds);L=max(oldL,max(row[0] for row in charged)-s['budget']);equal=L==W
    if L>W or any(type(cert[k]) is not int for k in ('lower','upper','old_lower')) or cert['lower']!=L or cert['old_lower']!=oldL or cert['upper']!=W or cert['source_bound_stronger']!=(L>oldL) or cert['equality_exit']!=equal or cert['reason']!=('equality_exit' if equal else 'strict_gap_search'):raise Invalid('charged exact source L/W classification')
    incumbent_check(s,payload['route']);trace_check(s,payload['bound_trace'],ds,charged,W,c)
    if equal:
        if canonical(payload['route'])!=canonical(payload['incumbent']) or any(c[k]!=0 for k in PHASE|{'charged_bound_stronger','charged_strict_exclusions'}) or payload['bound_trace']!=[]:raise Invalid('matching bound identical incumbent/zero phase')

def exact_trace_expected(s,ds,charged,W,exposure):
    # Separate raw indexed forward state simulation binds complete event sequence
    # and phase counters, not just a prefix or hand-counted metadata.
    G=s['graph'];n=len(ds);st,aa=topology(s);pos={(a,j):k+1 for k,(a,j) in enumerate((a,j) for a in sorted(G) for j in range(len(G[a])))};ban={(tuple(x),tuple(y)) for x,y in s['forbidden']};pen={(tuple(x['incoming']),tuple(x['outgoing'])):x['delay'] for x in s['penalties']};c={k:0 for k in PHASE|{'charged_bound_stronger','charged_strict_exclusions'}};trace=[]
    zero=(0,)*n;labels={(s['start'],None):[(0,*zero)]};queue=[(0,0,0,zero,s['start'],None,(s['start'],),(),0)];serial=0;c['labels_inserted']=c['max_live_queue']=1
    while queue:
        worst,_,risk,totals,v,inc,path,indices,turn=heapq.heappop(queue);c['pops']+=1
        if (risk,*totals) not in labels[(v,inc)]:c['stale_pops']+=1;continue
        if v==s['goal']:
            route={'path':list(path),'edges':[{'source':a,'edge_index':j,'target':b} for a,b,j in zip(path,path[1:],indices)],'exposure':risk,'scenario_totals':list(totals),'worst_time':worst,'turn_penalty':turn};return trace,c,route
        for j,e in enumerate(G[v]):
            c['candidate_edges']+=1;out=(v,j);pair=(inc,out)
            if inc is not None and pair in ban:c['forbidden_skipped']+=1;continue
            delay=pen.get(pair,0) if inc is not None else 0;r=risk+e['exposure'];state=pos[out];suffix=exposure[state]
            if r>s['budget'] or suffix is None or r+suffix>s['budget']:c['feasibility_pruned']+=1;continue
            new=tuple(x+y+delay for x,y in zip(totals,e['scenario_times']));d=[row[state] for row in ds];a=[row[state] for row in charged]
            if any(x is None for x in d+a):raise Invalid('parent exact feasible suffix')
            old=max(x+y for x,y in zip(new,d));bound=max(new[k]+max(d[k],a[k]-(s['budget']-r)) for k in range(n));stronger=bound>old;extra=bound>W and old<=W;c['charged_bound_stronger']+=int(stronger);c['charged_strict_exclusions']+=int(extra)
            trace.append({'path':list(path)+[e['target']],'indices':list(indices)+[j],'state':state,'exposure':r,'totals':list(new),'old_bound':old,'new_bound':bound,'stronger':stronger,'extra_exclusion':extra,'pruned':bound>W})
            if bound>W:c['objective_bound_pruned']+=1;continue
            vector=(r,*new);key=(e['target'],out);oldlabels=labels.setdefault(key,[])
            if any(all(x<=y for x,y in zip(label,vector)) for label in oldlabels):c['dominance_pruned']+=1;continue
            labels[key]=[label for label in oldlabels if not all(x<=y for x,y in zip(vector,label))];labels[key].append(vector);serial+=1;heapq.heappush(queue,(max(new),serial,r,new,e['target'],out,path+(e['target'],),indices+(j,),turn+delay));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(queue))
    raise Invalid('parent feasible exact search returned None')

_original_check=check
def check(s,payload,certificate=True):
    _original_check(s,payload,certificate)
    if not payload['certificate']['early_exit'] and not payload['certificate']['equality_exit']:
        expected,c,r=exact_trace_expected(s,payload['scenario_proof']['distances'],payload['charged_proof']['distances'],payload['certificate']['upper'],payload['proof']['distances'])
        if canonical(payload['bound_trace'])!=canonical(expected) or any(payload['counters'][k]!=v for k,v in c.items()) or canonical(payload['route'])!=canonical(r):raise Invalid('complete original exact event/counter/firstgoal replay')
