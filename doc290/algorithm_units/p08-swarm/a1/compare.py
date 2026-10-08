"""Frozen exact synthetic comparison. No import-time scoring."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
from itertools import product
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from uncertain_allocation import uncertain_interval
from two_agent_allocation import interval

def evaluate(menu,required):
    rows=[]
    for name,ranges,w in menu:
        u=uncertain_interval(ranges,w,required)
        mid=[(a+b)/2 for a,b in ranges]
        rows.append({'name':name,'guarantee':u['minimum'],'nominal':interval(mid,w,required)['independent']})
    # max keeps first index on ties, fixed menu order.
    ri=max(range(len(rows)),key=lambda i:rows[i]['guarantee'])
    ni=max(range(len(rows)),key=lambda i:rows[i]['nominal'])
    return {'choices':rows,'robust_choice':rows[ri]['name'],'nominal_choice':rows[ni]['name'],
            'guarantee_difference':rows[ri]['guarantee']-rows[ni]['guarantee'],
            'nominal_difference':rows[ri]['nominal']-rows[ni]['nominal']}

def run(protocol):
    rows=[]
    for i,(single,split,k) in enumerate(product(protocol['single_ranges'],protocol['split_ranges'],protocol['thresholds'])):
        menu=[('single',[(F(single[0]),F(single[1]))],[F(x) for x in protocol['payload_single']]),
              ('split',[(F(a),F(b)) for a,b in split],[F(x) for x in protocol['payload_split']])]
        rows.append({'case':i+1,'single_range':single,'split_ranges':split,'threshold':k,**evaluate(menu,F(k))})
    return rows
if __name__=='__main__':
    p=Path(__file__).with_name('protocol.json')
    print(json.dumps(run(json.loads(p.read_text())),default=str,indent=2))
