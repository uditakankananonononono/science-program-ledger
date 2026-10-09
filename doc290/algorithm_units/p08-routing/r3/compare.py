import json,hashlib,sys
from pathlib import Path
from core import gate,launch,ROOT,family

def run(output):
    try:identity=gate()
    except Exception as e:
        Path(output).write_text(json.dumps({'status':'GATE_FAIL','exception_type':type(e).__name__,'exception':str(e)},sort_keys=True,indent=2)+'\n');return
    inputs=json.loads((ROOT/'cases.json').read_text());rows=[]
    for c in inputs:
        r=launch(['subject',c['n'],c['method']]);r.update(c);r['input_sha256']=hashlib.sha256(json.dumps({'case':c,'graph':family(c['n'])},sort_keys=True,separators=(',',':')).encode()).hexdigest();rows.append(r)
    Path(output).write_text(json.dumps({'identity':identity,'rows':rows,'row_count':len(rows),'pass_count':sum(r['status']=='PASS' for r in rows),'scope':'bounded characterization, no invention/performance superiority/observed frontier claim'},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
