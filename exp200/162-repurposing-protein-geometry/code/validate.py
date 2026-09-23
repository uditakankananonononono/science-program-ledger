import json, subprocess, numpy as np, pandas as pd, time
from scipy.stats import fisher_exact
rng=np.random.default_rng(0)
exec(open('code/run.py').read().split("pos=set()")[0])
a2t={}
for t in tg:
    if t.get('organism')=='Homo sapiens' and t.get('target_type')=='SINGLE PROTEIN':
        for c in t['target_components']:
            if c.get('accession'): a2t.setdefault(c['accession'],t['target_chembl_id'])
g2a={v:k for k,v in gene.items() if isinstance(v,str)}
F=pd.read_csv('results/candidate_alternative_targets.csv')
C=F.sample(150,random_state=0)
J=lambda x,y: len(x&y)/len(x|y) if x|y else 0
ctrl=[]
for d in C.drug:
    s=d2a[d]; pool=[c for c in km if c not in s and max(J(ipr[a],ipr[c]) for a in s)<0.1]
    ctrl.append((d,rng.choice(pool)))
def active(mol,acc):
    t=a2t.get(acc)
    if not t: return None
    u=f'https://www.ebi.ac.uk/chembl/api/data/activity.json?molecule_chembl_id={mol}&target_chembl_id={t}&pchembl_value__gte=6&limit=1'
    for k in range(3):
        try: return json.loads(subprocess.run(['curl','-s','--max-time','60',u],capture_output=True,text=True).stdout)['page_meta']['total_count']>0
        except Exception: time.sleep(2)
    return None
ca=[active(d,g2a.get(c,c)) for d,c in zip(C.drug,C.candidate_target)]
co=[active(d,c) for d,c in ctrl]
ca=[x for x in ca if x is not None]; co=[x for x in co if x is not None]
t=[[sum(ca),len(ca)-sum(ca)],[sum(co),len(co)-sum(co)]]
odds,p=fisher_exact(t,alternative='greater')
res={'cand_n':len(ca),'cand_active':int(sum(ca)),'cand_frac':sum(ca)/len(ca),'ctrl_n':len(co),'ctrl_active':int(sum(co)),'ctrl_frac':sum(co)/max(len(co),1),'fisher_p':float(p)}
res['ratio']=res['cand_frac']/res['ctrl_frac'] if res['ctrl_frac'] else float('inf')
C.assign(active=[active(d,g2a.get(c,c)) for d,c in []] or None)
print(json.dumps(res,indent=1)); json.dump(res,open('results/validation_v1.json','w'),indent=1)
