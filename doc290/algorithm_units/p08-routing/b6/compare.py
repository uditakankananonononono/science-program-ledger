import json,sys,hashlib
from pathlib import Path
from core import gate,launch,ROOT

def run(output):
    try:identity=gate()
    except Exception as e:
        Path(output).write_text(json.dumps({'status':'GATE_FAIL','exception_type':type(e).__name__,'exception':str(e)},sort_keys=True,indent=2)+'\n');return
    cases=json.loads((ROOT/'cases.json').read_text());rows=[]
    for i,c in enumerate(cases):
        r={'name':c['name'],'oracle':c['oracle'],'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'subjects':{m:launch(['subject',i,m]) for m in ('variant','b5')}};r['agreement']=all(v['status']=='PASS' for v in r['subjects'].values());rows.append(r)
    Path(output).write_text(json.dumps({'identity':identity,'rows':rows,'pair_count':len(rows),'agreement_count':sum(r['agreement'] for r in rows),'attempt_count':2*len(rows),'pass_count':sum(v['status']=='PASS' for r in rows for v in r['subjects'].values()),'scope':'standard admissible pruning synthetic comparator, no invention/superiority'},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
