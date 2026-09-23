import json, subprocess, time
def get(u):
    for t in range(4):
        r=subprocess.run(['curl','-s','--max-time','90',u],capture_output=True,text=True).stdout
        try: return json.loads(r)
        except Exception: time.sleep(3)
    raise SystemExit('fail '+u)
B='https://www.ebi.ac.uk'
def pages(path,key):
    out=[];u=B+path
    while u:
        d=get(u); out+=d[key]; n=d['page_meta']['next']; u=B+n if n else None
    return out
mech=pages('/chembl/api/data/mechanism.json?max_phase=4&limit=1000','mechanisms')
json.dump(mech,open('data/mechanisms.json','w')); print('mech',len(mech))
tids=sorted({m['target_chembl_id'] for m in mech if m['target_chembl_id']})
tg=[]
for i in range(0,len(tids),50):
    tg+=get(B+'/chembl/api/data/target.json?limit=50&target_chembl_id__in='+','.join(tids[i:i+50]))['targets']
json.dump(tg,open('data/targets.json','w')); print('targets',len(tg))
mids=sorted({m['parent_molecule_chembl_id'] for m in mech if m['parent_molecule_chembl_id']})
mo=[]
for i in range(0,len(mids),50):
    mo+=[{'id':x['molecule_chembl_id'],'atc':x.get('atc_classifications') or [],'name':x.get('pref_name')} for x in get(B+'/chembl/api/data/molecule.json?limit=50&molecule_chembl_id__in='+','.join(mids[i:i+50]))['molecules']]
json.dump(mo,open('data/molecules.json','w')); print('mols',len(mo))
