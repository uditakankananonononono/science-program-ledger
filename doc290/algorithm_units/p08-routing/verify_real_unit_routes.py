"""Recheck recorded unit-cost queries against coordinate BFS; artifact folder required."""
import hashlib,json,sys
from pathlib import Path
from collections import deque
import numpy as np
from PIL import Image
from mask_graph import mask_to_graph
from anchor_route import route_integer_anchors

root=Path(sys.argv[1]);records=json.loads((Path(__file__).parent/'data_audit/three_first_mask_unit_cost_routes.json').read_text())
for row in records:
 mask=np.asarray(Image.open(root/(row['dataset']+'_full_skeleton.png')))==255
 assert hashlib.sha256(mask.tobytes()).hexdigest()==row['skeleton_sha256']
 start,goal=row['start'],row['goal'];dist={start:0};queue=deque([start])
 while queue:
  current=queue.popleft();y,x=map(int,current.split(','))
  for dy in (-1,0,1):
   for dx in (-1,0,1):
    a,b=y+dy,x+dx
    if not (dy or dx) or not 0<=a<mask.shape[0] or not 0<=b<mask.shape[1] or not mask[a,b]:continue
    key=f'{a},{b}'
    if key not in dist:dist[key]=dist[current]+1;queue.append(key)
 assert dist[goal]==row['bfs_steps']
 graph=mask_to_graph(mask.astype(int).tolist(),8,1,0,(1,2))
 for method,budget in [('budget',0),('scenario',None),('budget-scenario',0)]:
  result=route_integer_anchors(graph,start,goal,method,budget)
  path=result['expanded_pixel_path'];out=result['compressed_result']
  assert len(path)-1==dist[goal]
  for a,b in zip(path,path[1:]):
   y,x=map(int,a.split(','));u,v=map(int,b.split(','))
   assert mask[y,x] and mask[u,v] and max(abs(y-u),abs(x-v))==1
  if method=='budget':assert out['time']==dist[goal]
  else:assert out['scenario_totals']==[dist[goal],2*dist[goal]]
 print(row['dataset'],dist[goal],'all three objectives match coordinate BFS')
