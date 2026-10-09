import json,sys,hashlib
from pathlib import Path
from core import gate,launch,ROOT
from analysis import order,summarize

def run(output):
    try:identity=gate()
    except Exception as e:
        Path(output).write_text(json.dumps({'status':'GATE_FAIL','exception_type':type(e).__name__,'exception':str(e)},sort_keys=True,indent=2)+'\n');return
    cases=json.loads((ROOT/'cases.json').read_text());rows=[]
    for i,c in enumerate(cases):
        for repeat in range(3):
            ord=order(i,repeat);subjects={m:launch(['subject',i,m]) for m in ord};cpu_equal=all(v['status']=='PASS' for v in subjects.values()) and subjects['variant']['worker']['affinity']==subjects['p3']['worker']['affinity'];r={'name':c['name'],'case_index':i,'repeat':repeat,'order':ord,'oracle':c['oracle'],'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'subjects':subjects,'cpu_equal':cpu_equal,'agreement':all(v['status']=='PASS' for v in subjects.values()) and cpu_equal};rows.append(r)
    result={'identity':identity,'rows':rows,'pair_count':len(rows),'agreement_count':sum(r['agreement'] for r in rows),'attempt_count':2*len(rows),'pass_count':sum(v['status']=='PASS' for r in rows for v in r['subjects'].values()),'analysis':summarize(rows,len(cases)),'scope':'matched boundary descriptive observations, reused corpus, no inferential speedwin'}
    Path(output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
