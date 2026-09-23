import pandas as pd, numpy as np, re, json
from collections import Counter
rng=np.random.default_rng(1)
PH=re.compile(r'^(C\d+orf\d+|CXorf\d+|CYorf\d+|FAM\d+[A-Z]*\d*|KIAA\d+|TMEM\d+[A-Z]*|CCDC\d+[A-Z]*|LOC\d+|ORF\d+)$')
BAD=re.compile(r'open reading frame|family with sequence similarity|Coiled-coil domain containing|Transmembrane proteins|uncharacterized|KIAA|Long non-coding',re.I)
h=pd.read_csv('data/hgnc.txt',sep='\t',dtype=str,low_memory=False); h=h[h.status=='Approved']
def groups(s):
    if pd.isna(s): return set()
    return {g for g in s.split('|') if not BAD.search(g)}
sym2g={}
for _,r in h.iterrows():
    g=groups(r.gene_group)
    sym2g[r.symbol]=g
    if pd.notna(r.prev_symbol):
        for p in r.prev_symbol.split('|'): sym2g.setdefault(p.strip(),g)
info=pd.read_csv('data/9606.protein.info.v11.0.txt.gz',sep='\t'); info.columns=['pid','name','size','annot']
pid2name=dict(zip(info.pid,info.name))
c=pd.read_csv('results/cohort_features.csv'); pos=c[(c.y==1)&c.pid.notna()].copy()
pos['g']=pos.symbol.map(lambda s: sym2g.get(s,set()))
pos=pos[pos.g.map(len)>0]
pids=set(pos.pid); nb={p:[] for p in pids}
for ch in pd.read_csv('data/9606.protein.links.v11.0.txt.gz',sep=' ',chunksize=2_000_000):
    ch=ch[ch.protein1.isin(pids)&(ch.combined_score>=700)]
    for p,q,s in ch.itertuples(index=False): nb[p].append(q)
def top3(p):
    cnt=Counter(); k=0
    for q in nb[p]:
        g=sym2g.get(pid2name.get(q,''),set())
        if g: k+=1; cnt.update(g)
    return k,[g for g,_ in cnt.most_common(3)]
pos['k'],pos['top3']=zip(*pos.pid.map(top3))
el=pos[pos.k>=3].reset_index(drop=True)
hit=np.array([len(set(t)&g)>0 for t,g in zip(el.top3,el.g)])
null=[]
for i in range(1000):
    perm=rng.permutation(len(el))
    null.append(np.mean([len(set(el.top3[j])&el.g[i2])>0 for i2,j in enumerate(perm)]))
null=np.array(null)
res=dict(n_pos_with_group=int(len(pos)),n_eligible=int(len(el)),hit_rate=float(hit.mean()),null_mean=float(null.mean()),
 fold=float(hit.mean()/max(null.mean(),1e-9)),p_emp=float((1+(null>=hit.mean()).sum())/1001))
print(json.dumps(res,indent=1)); json.dump(res,open('results/pivot1.json','w'),indent=1)
el.assign(hit=hit,g=el.g.map(lambda s:'|'.join(sorted(s))),top3=el.top3.map('|'.join))[['symbol','t0_symbol','k','g','top3','hit']].to_csv('results/pivot1_predictions.csv',index=False)
