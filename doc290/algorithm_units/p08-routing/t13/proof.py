"""Independent original topology/scalar candidates/selection/full search audit."""
import importlib.util,copy,heapq
from pathlib import Path
from model import Invalid,integer,witness,MAX,model
spec=importlib.util.spec_from_file_location('t13_original_t12_parent',Path(__file__).resolve().parent.parent/'t12/proof.py');baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
prior=baseline.prior;original=prior.original;original_t7_proof=prior.original_t7_proof
scenario_check=prior.scenario_check;incumbent_check=prior.incumbent_check;charged_check=prior.charged_check
canonical=prior.canonical;BASE_COUNTERS=prior.BASE_COUNTERS;NEW_COUNTERS=prior.NEW_COUNTERS|{'scalar_candidate_inspections'}
METHOD=baseline.METHOD|{'candidate_ledger','incumbent_original_upper','incumbent_selected_upper','selected_candidate'};WRAPPER=baseline.WRAPPER

def scenario_candidate_expected(s,column):
    st,arcs=prior.topology(s);G=s['graph'];n=next(len(e['scenario_times']) for es in G.values() for e in es);out=[[] for _ in st]
    for k,a in enumerate(arcs):out[a['source']].append((k,a))
    tentative=[None]*len(st);tentative[0]=0;prev={};q=[(0,0,0)];serial=0;finished=[];pops=[];count=0;sink=len(st)-1
    while q:
        value,tie,u=heapq.heappop(q);stale=value!=tentative[u];pops.append({'distance':value,'serial':tie,'state':u,'stale':stale})
        if stale:continue
        finished.append(u)
        if u==sink:break
        for k,a in out[u]:
            count+=1;v=a['target'];new=value+a['scenarios'][column]
            if tentative[v] is None or new<tentative[v]:tentative[v]=new;prev[v]=k;serial+=1;heapq.heappush(q,(new,serial,v))
    if sink not in finished:raise Invalid('parent scenario sink absent')
    selected=[];v=sink;seen=set()
    while v:
        if v in seen or v not in prev:raise Invalid('parent scenario predecessor chain')
        seen.add(v);a=arcs[prev[v]];selected.append(a);v=a['source']
    path=[s['start']];edges=[];ss=[0]*n;r=turn=0
    for a in reversed(selected):
        if a['edge'] is None:continue
        origin,j=a['edge'];target=G[origin][j]['target'];path.append(target);edges.append({'source':origin,'edge_index':j,'target':target});r+=a['risk'];turn+=a['delay'];ss=[x+y for x,y in zip(ss,a['scenarios'])]
    route={'path':path,'edges':edges,'scenario_totals':ss,'worst_time':max(ss),'exposure':r,'turn_penalty':turn}
    stop={'semantics':'tentative at first sink pop, NOT complete ALL-state distances','tentative_distances':tentative,'state_status':['settled' if k in finished else 'queued' if tentative[k] is not None else 'unreached' for k in range(len(st))],'settled_order':finished,'predecessor_arc':[prev.get(k) for k in range(len(st))],'pops':pops,'remaining_heap':[list(x) for x in q],'inspections':count}
    return route,stop

def candidate_expected(s):
    original_route=prior.incumbent_expected(s);n=len(original_route['scenario_totals']);rows=[]
    for k in range(n+1):
        if k==0:route=original_route;stop=None
        else:route,stop=scenario_candidate_expected(s,k-1)
        validation_only=copy.deepcopy(s);validation_only['budget']=MAX;checked=witness(validation_only,route);eligible=route['exposure']<=s['budget']
        audit={'validation_scope':'validation-only MAX budget copy; original input unchanged','validation_budget':MAX,'checked':checked,'eligible':eligible,'eligibility_budget':s['budget'],'state':'valid_eligible' if eligible else 'valid_but_ineligible_over_budget'}
        rows.append({'index':k,'objective':'exposure' if k==0 else 'scenario','scenario_index':None if k==0 else k-1,'route':route,'stop_ledger':stop,'audit':audit})
    selected=next(k for k,row in enumerate(rows) if row['audit']['eligible'] and row['route']['worst_time']==min(x['route']['worst_time'] for x in rows if x['audit']['eligible']))
    witness(s,rows[selected]['route'])
    return rows,selected

def candidates_check(s,rows,selected):
    expected,index=candidate_expected(s)
    if type(selected) is not int or selected!=index or canonical(rows)!=canonical(expected):raise Invalid('complete candidate original route/stop/eligibility/firsttie typed ledger')

def check(s,payload,certificate=True):
    if type(payload) is not dict or set(payload) not in (METHOD,METHOD|WRAPPER):raise Invalid('exact T13 stage or worker schema')
    activation=payload['activation']
    if type(activation) is not str or activation not in ('exposure_exit','old_bound_equality','charged_bound'):raise Invalid('T13 activation')
    c=payload['counters']
    if type(c) is not dict or set(c)!=BASE_COUNTERS|NEW_COUNTERS:raise Invalid('T13 counters exact')
    for value in c.values():integer(value)
    original_t7_proof.check(s,payload,certificate=False)
    fields={'early_exit','equality_exit','reason','budget','lower','upper','old_lower','charged_lambda','source_bound_stronger'};cert=payload['certificate']
    if type(cert) is not dict or set(cert)!=fields or type(cert['reason']) is not str or any(type(cert[k]) is not bool for k in ('early_exit','equality_exit','source_bound_stronger')) or type(cert['budget']) is not int or cert['budget']!=s['budget'] or type(cert['charged_lambda']) is not int or cert['charged_lambda']!=1:raise Invalid('typed certificate')
    minimum=payload['proof']['start_minimum'];early=minimum is None or minimum>s['budget']
    if cert['early_exit']!=early:raise Invalid('exposure flag')
    additions=('candidate_ledger','incumbent_original_upper','incumbent_selected_upper','selected_candidate')
    if early:
        if activation!='exposure_exit' or any(payload[k] is not None for k in additions) or c['scalar_candidate_inspections']!=0:raise Invalid('early absent candidates')
        q={k:v for k,v in payload.items() if k not in additions};q['counters']={k:v for k,v in c.items() if k!='scalar_candidate_inspections'};baseline.check(s,q);return
    scenario_check(s,payload['scenario_proof']);candidates_check(s,payload['candidate_ledger'],payload['selected_candidate']);rows=payload['candidate_ledger'];selected=payload['selected_candidate'];route=rows[selected]['route'];W=incumbent_check(s,route);oldW=rows[0]['route']['worst_time']
    if W>oldW or type(payload['incumbent_original_upper']) is not int or payload['incumbent_original_upper']!=oldW or type(payload['incumbent_selected_upper']) is not int or payload['incumbent_selected_upper']!=W or canonical(payload['incumbent'])!=canonical(route):raise Invalid('selected W worsens/original/selected/route binding')
    count=sum(row['stop_ledger']['inspections'] for row in rows[1:])
    if c['scalar_candidate_inspections']!=count:raise Invalid('actual scenario candidate count')
    ds=payload['scenario_proof']['distances'];oldL=max(row[0] for row in ds)
    if oldL>W or any(type(cert[k]) is not int for k in ('old_lower','lower','upper')) or cert['old_lower']!=oldL or cert['upper']!=W:raise Invalid('old lower/actual selected W')
    actual_counts=prior.preprocessing_expected(s,False)
    if any(c[k]!=v for k,v in actual_counts.items()):raise Invalid('original exposure/scenario/incumbent counts')
    if activation=='old_bound_equality':
        if oldL!=W or cert['lower']!=W or cert['source_bound_stronger'] or not cert['equality_exit'] or cert['reason']!='equality_exit' or payload['charged_proof'] is not None or payload['bound_trace']!=[] or any(c[k]!=0 for k in prior.PHASE|prior.NEW_COUNTERS) or canonical(payload['route'])!=canonical(route):raise Invalid('old equality no charged exact phase')
        return
    if activation!='charged_bound' or not oldL<W:raise Invalid('charged branch old gap')
    charged_check(s,payload['charged_proof']);charged=payload['charged_proof']['distances'];actual_counts=prior.preprocessing_expected(s,True)
    if any(c[k]!=v for k,v in actual_counts.items()):raise Invalid('original charged preprocess counts')
    L=max(oldL,max(row[0] for row in charged)-s['budget']);equal=L==W
    if L>W or cert['lower']!=L or cert['source_bound_stronger']!=(L>oldL) or cert['equality_exit']!=equal or cert['reason']!=('equality_exit' if equal else 'strict_gap_search'):raise Invalid('charged selectedW classification')
    incumbent_check(s,payload['route']);prior.trace_check(s,payload['bound_trace'],ds,charged,W,c)
    if equal:
        if canonical(payload['route'])!=canonical(route) or any(c[k]!=0 for k in prior.PHASE|{'charged_bound_stronger','charged_strict_exclusions'}) or payload['bound_trace']!=[]:raise Invalid('charged equality route/counters')
    else:
        events,counts,answer=prior.exact_trace_expected(s,ds,charged,W,payload['proof']['distances'])
        if canonical(events)!=canonical(payload['bound_trace']) or canonical(answer)!=canonical(payload['route']) or any(c[k]!=v for k,v in counts.items()):raise Invalid('complete selectedW search/event/phase/firstgoal')
