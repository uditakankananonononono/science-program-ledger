import json,hashlib,sys
from pathlib import Path
from core import gate,ROOT,launch
from model import load_bytes

def run(output):
    identity=gate();cases=load_bytes((ROOT/'cases.json').read_bytes());rows=[]
    for k,c in enumerate(cases):
        receipt=launch(['subject',k]);rows.append({'name':c['name'],'expected':c['expected'],'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'receipt':receipt,'agreement':receipt['status']=='PASS'})
    Path(output).write_text(json.dumps({'identity':identity,'rows':rows,'row_count':len(rows),'agreement_count':sum(r['agreement'] for r in rows),'scope':'bounded finite certificate generation, incomplete/not invention'},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
