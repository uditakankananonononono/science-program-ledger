import json,sys,hashlib
from pathlib import Path
from core import ROOT,gate,launch
from analysis import order,summarize
from classes import classify

def run(output):
    try:
        identity=gate();cases=json.loads((ROOT/'cases.json').read_text());classes=json.loads((ROOT/'classes.json').read_text())
        if classes!=[classify(c['statement']) for c in cases]:raise ValueError('independent sidecar mismatch')
    except Exception as e:Path(output).write_text(json.dumps({'status':'GATE_FAIL','exception':str(e)},indent=2)+'\n');return
    rows=[]
    for i,c in enumerate(cases):
        for repeat in range(3):
            ord=order(i,repeat);subjects={m:launch(['subject',i,m]) for m in ord};rows.append({'case_index':i,'repeat':repeat,'name':c['name'],'class':classes[i],'order':ord,'oracle':c['oracle'],'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'subjects':subjects,'agreement':all(s['status']=='PASS' for s in subjects.values())})
    p={'identity':identity,'rows':rows,'pair_count':len(rows),'attempt_count':2*len(rows),'agreement_count':sum(r['agreement'] for r in rows),'pass_count':sum(s['status']=='PASS' for r in rows for s in r['subjects'].values()),'analysis':summarize(rows,classes),'scope':'one local environment/reused corpus descriptive timing, no general speed claim'}
    Path(output).write_text(json.dumps(p,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
