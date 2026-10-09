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

spec=importlib.util.spec_from_file_location('t16_immutable_t15',Path(__file__).resolve().parent.parent/'t15/proof.py');t14=importlib.util.module_from_spec(spec);spec.loader.exec_module(t14)
PREFIX_FIELDS={'semantics','scenario_count','remaining_scenario_indices','terminal_reason','selected_index','selected_W','original_L','combined_L','bound_kind'}
def candidate_prefix_expected(s,limit=None):
    original_route=prior.incumbent_expected(s);n=len(original_route['scenario_totals']);ds=scenario_distances_raw(s);oldL=max(row[0] for row in ds);_,charged=prior.charged_distances(s);L=max(oldL,max(row[0] for row in charged)-s['budget']);rows=[];selected=0;equal=False
    for k in range(n+1):
        if k==0:route=original_route;stop=None
        else:route,stop=scenario_candidate_expected(s,k-1)
        validation_only=copy.deepcopy(s);validation_only['budget']=MAX;checked=witness(validation_only,route);eligible=route['exposure']<=s['budget']
        audit={'validation_scope':'validation-only MAX budget copy; original input unchanged','validation_budget':MAX,'checked':checked,'eligible':eligible,'eligibility_budget':s['budget'],'state':'valid_eligible' if eligible else 'valid_but_ineligible_over_budget'}
        rows.append({'index':k,'objective':'exposure' if k==0 else 'scenario','scenario_index':None if k==0 else k-1,'route':route,'stop_ledger':stop,'audit':audit})
        if eligible and route['worst_time']<rows[selected]['route']['worst_time']:selected=k
        equal=rows[selected]['route']['worst_time']==L
        if k and (equal or k==limit):break
    count=len(rows)-1
    prefix={'semantics':'ordered produced PREFIX, omitted candidates NOT constructed/audited','scenario_count':count,'remaining_scenario_indices':list(range(count,n)),'terminal_reason':'bound_equality' if equal else 'all_candidates' if count==n else 'continuing','selected_index':selected,'selected_W':rows[selected]['route']['worst_time'],'original_L':oldL,'combined_L':L,'bound_kind':'combined_fixed_lambda1'}
    witness(s,rows[selected]['route']);return rows,selected,prefix

def prefix_check(s,rows,selected):
    expected,index,_=candidate_prefix_expected(s)
    if type(selected) is not int or selected!=index or canonical(rows)!=canonical(expected):raise Invalid('earliest eligible prefix raw ledger/firsttie')

def candidates_check(s,rows,selected,prefix,allow_continuing=False):
    if type(prefix) is not dict or set(prefix)!=PREFIX_FIELDS:raise Invalid('exact prefix fields')
    for k in ('scenario_count','selected_index','selected_W','original_L','combined_L'):integer(prefix[k])
    if type(prefix['remaining_scenario_indices']) is not list:raise Invalid('remaining list type')
    for v in prefix['remaining_scenario_indices']:integer(v)
    if type(prefix['terminal_reason']) is not str or type(prefix['semantics']) is not str or type(prefix['bound_kind']) is not str:raise Invalid('prefix string type')
    limit=prefix['scenario_count'] if allow_continuing else None
    expected,index,meta=candidate_prefix_expected(s,limit)
    if type(selected) is not int or selected!=index or canonical(rows)!=canonical(expected) or canonical(prefix)!=canonical(meta) or (not allow_continuing and prefix['terminal_reason']=='continuing'):raise Invalid('earliest exact prefix/typed index/count/remaining/reason/W/L')

def check(s,payload,certificate=True):
    fields=METHOD
    if type(payload) is not dict or set(payload) not in (fields,fields|WRAPPER):raise Invalid('exact T16 payload')
    q=dict(payload);schedule=q.pop('candidate_schedule');branch=q['candidate_activation']
    if type(schedule) is not str:raise Invalid('schedule type')
    if branch in ('exposure_exit','original_bound_equality'):
        if schedule!='uncharged_skip':raise Invalid('uncharged skip schedule')
        t14.check(s,q);return
    if type(branch) is not str or branch not in ('charged_original_bound_equality','candidates_activated') or schedule!='charged_before_candidates':raise Invalid('charged schedule/branch')
    c=q['counters']
    if type(c) is not dict or set(c)!=BASE_COUNTERS|NEW_COUNTERS:raise Invalid('exact counters')
    for value in c.values():integer(value)
    original_t7_proof.check(s,q,certificate=False);scenario_check(s,q['scenario_proof']);charged_check(s,q['charged_proof'])
    original_route=prior.incumbent_expected(s);originalW=incumbent_check(s,original_route);ds=q['scenario_proof']['distances'];oldL=max(row[0] for row in ds);charged=q['charged_proof']['distances'];L=max(oldL,max(row[0] for row in charged)-s['budget'])
    if not oldL<originalW or L>originalW:raise Invalid('original strict gap/valid combined')
    actual_counts=prior.preprocessing_expected(s,True)
    if any(c[k]!=v for k,v in actual_counts.items()):raise Invalid('once original plus charged actualcounts')
    if branch=='charged_original_bound_equality':
        if q['candidate_ledger'] is not None or q['selected_candidate'] is not None or q['candidate_prefix'] is not None or L!=originalW or c['scalar_candidate_inspections']!=0:raise Invalid('charged skip absent ledger/index/prefix actualequality')
        route=original_route;W=originalW
    else:
        if not L<originalW:raise Invalid('candidate prefix cannot continue charged original equality')
        candidates_check(s,q['candidate_ledger'],q['selected_candidate'],q['candidate_prefix']);rows=q['candidate_ledger'];route=rows[q['selected_candidate']]['route'];W=incumbent_check(s,route)
        if c['scalar_candidate_inspections']!=sum(row['stop_ledger']['inspections'] for row in rows[1:]):raise Invalid('actual produced scalar count')
    if L>W or W>originalW or type(q['incumbent_original_upper']) is not int or type(q['incumbent_selected_upper']) is not int or q['incumbent_original_upper']!=originalW or q['incumbent_selected_upper']!=W or canonical(q['incumbent'])!=canonical(route):raise Invalid('actual selected original W/route')
    cert=q['certificate'];fields={'early_exit','equality_exit','reason','budget','lower','upper','old_lower','charged_lambda','source_bound_stronger'}
    if type(cert) is not dict or set(cert)!=fields or type(cert['reason']) is not str or any(type(cert[k]) is not bool for k in ('early_exit','equality_exit','source_bound_stronger')) or any(type(cert[k]) is not int for k in ('budget','lower','upper','old_lower','charged_lambda')):raise Invalid('typed cert')
    equal=L==W
    if q['activation']!='charged_bound' or cert!=dict(early_exit=False,equality_exit=equal,reason='equality_exit' if equal else 'strict_gap_search',budget=s['budget'],lower=L,upper=W,old_lower=oldL,charged_lambda=1,source_bound_stronger=L>oldL):raise Invalid('combined exact classification')
    incumbent_check(s,q['route']);prior.trace_check(s,q['bound_trace'],ds,charged,W,c)
    if equal:
        if canonical(q['route'])!=canonical(route) or q['bound_trace']!=[] or any(c[k]!=0 for k in prior.PHASE|{'charged_bound_stronger','charged_strict_exclusions'}):raise Invalid('combined equality same route zero phase')
    else:
        events,counts,answer=prior.exact_trace_expected(s,ds,charged,W,q['proof']['distances'])
        if canonical(events)!=canonical(q['bound_trace']) or canonical(answer)!=canonical(q['route']) or any(c[k]!=v for k,v in counts.items()):raise Invalid('complete combined selectedW phase/event/firstgoal')

def scenario_distances_raw(s):
    st,arcs=prior.topology(s);n=next(len(e['scenario_times']) for es in s['graph'].values() for e in es);rows=[]
    for k in range(n):
        d=[None]*len(st);d[-1]=0
        for _ in range(len(st)-1):
            old=d;d=d[:]
            for a in arcs:
                if old[a['target']] is not None:
                    value=old[a['target']]+a['scenarios'][k];u=a['source']
                    if d[u] is None or value<d[u]:d[u]=value
        rows.append(d)
    return rows

METHOD=t14.METHOD|{'candidate_activation','candidate_prefix','candidate_schedule'}
