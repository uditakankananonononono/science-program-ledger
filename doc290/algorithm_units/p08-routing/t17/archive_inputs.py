"""Input/oracle preparation only. No method imports or worker launch."""
import json,hashlib,random
from pathlib import Path
from fixtures import cases
ROOT=Path(__file__).resolve().parent

def independent_statements():
 r=random.Random(316227);out=[]
 for _ in range(200):
  graph={v:[] for v in 'abcd'}
  for source in 'abcd':
   for target in 'abcd':
    if source!=target and r.random()<.25:
     times=[r.randrange(7) for _ in range(3)];risk=r.randrange(5)
     graph[source].append(dict(target=target,time=1,exposure=risk,scenario_times=times))
  for vertex in 'abcd':
   if r.random()<.10:graph[vertex].append(dict(target=vertex,time=1,exposure=0,scenario_times=[0,0,0]))
  if not any(graph.values()):graph['d'].append(dict(target='d',time=1,exposure=0,scenario_times=[0,0,0]))
  forbidden=[];penalties=[]
  for source in sorted(graph):
   for index,arc in enumerate(graph[source]):
    for following in range(len(graph[arc['target']])):
     first=[source,index];second=[arc['target'],following]
     if r.random()<.15:forbidden.append([first,second])
     if r.random()<.25:penalties.append(dict(incoming=first,outgoing=second,delay=r.randrange(4)))
  budget=r.randrange(13)
  out.append(dict(graph=graph,start='a',goal='d',budget=budget,forbidden=forbidden,penalties=penalties))
 return out

def independent_oracle(s):
 # Direct raw graph/turn identities, not model/model witness or method helpers.
 graph=s['graph'];ban={(tuple(a),tuple(b)) for a,b in s['forbidden']};delay={(tuple(p['incoming']),tuple(p['outgoing'])):p['delay'] for p in s['penalties']}
 stack=[('a',None,frozenset({('a',None)}),0,(0,0,0))];best=None
 while stack:
  node,incoming,seen,risk,cost=stack.pop()
  if node=='d':
   value=max(cost);best=value if best is None else min(best,value);continue
  for index,arc in enumerate(graph[node]):
   edge=(node,index);state=(arc['target'],edge)
   if state in seen or (incoming,edge) in ban:continue
   nr=risk+arc['exposure']
   if nr>s['budget']:continue
   penalty=delay.get((incoming,edge),0)
   stack.append((arc['target'],edge,seen|{state},nr,tuple(cost[j]+arc['scenario_times'][j]+penalty for j in range(3))))
 return best

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(canonical(x)).hexdigest()
rows=cases();raw=independent_statements()
assert len(rows)==len(raw)==200
for case,statement in zip(rows,raw):
 assert case['statement']==statement
 assert case['oracle']==independent_oracle(statement)
(ROOT/'cases.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
plan=[]
for i,c in enumerate(rows):
 order=['variant','t16'] if i%2==0 else ['t16','variant']
 for method in order:plan.append(dict(case_index=i,method=method,order=order,name=c['name'],input_sha256=sha(c),oracle=c['oracle']))
(ROOT/'plan.json').write_text(json.dumps(plan,sort_keys=True,indent=2)+'\n')
ledger=dict(seed=316227,listed_retired=[223606,244949,264575,282843,300007],distinct_from_list=True,list_completeness='UNVERIFIED',literal_count=200,planned_attempts=400,canonical_cases_sha256=sha(rows),file_cases_sha256=hashlib.sha256((ROOT/'cases.json').read_bytes()).hexdigest(),file_plan_sha256=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest(),original_state_dfs_agreements=200,scope='input-only preparation; no method/worker/corpus evaluation executed',inputs=[dict(name=c['name'],sha256=sha(c),oracle=c['oracle']) for c in rows])
(ROOT/'CORPUS-ARCHIVE.json').write_text(json.dumps(ledger,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in ledger.items() if k!='inputs'},indent=2))
