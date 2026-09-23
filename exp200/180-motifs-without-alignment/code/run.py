import json, random, numpy as np
from collections import Counter
from scipy.stats import binomtest
random.seed(0)
fams="PF00089 PF00069 PF00106 PF00561 PF00067 PF00071 PF00128 PF00085 PF00112 PF00026 PF00501 PF00378 PF00300 PF00248 PF00107 PF00144 PF00155 PF00202 PF00255 PF00462".split()
dev=set(fams[:5]); K=4
def load(f):
    R=json.load(open(f'data/{f}.json'))['results']; seen=set(); out=[]
    for r in R:
        s=r['sequence']['value']
        if s in seen: continue
        seen.add(s); sites=set()
        for ft in r.get('features',[]):
            if ft['type'] in ('Active site','Binding site'):
                a=ft['location']['start']['value']; b=ft['location']['end']['value']
                if a and b and b-a<5: sites.update(range(a-1,b))
        out.append((s,sites))
    return out
def df(seqs):
    c=Counter()
    for s in seqs: c.update({s[i:i+K] for i in range(len(s)-K+1)})
    return c
res={}
for f in fams:
    M=load(f); seqs=[s for s,_ in M]; n=len(seqs)
    obs=df(seqs); exp=Counter()
    for r in range(3):
        sh=[''.join(random.sample(s,len(s))) for s in seqs]; e=df(sh)
        for k,v in e.items(): exp[k]+=v/3
    sc={k:np.log2((v+1)/(exp.get(k,0)+1)) for k,v in obs.items() if v>=0.2*n}
    top=sorted(sc,key=sc.get,reverse=True)[:5]
    tot=cov=site=sitecov=0
    for s,st in M:
        mask=np.zeros(len(s),bool)
        for m in top:
            i=s.find(m)
            while i!=-1: mask[i:i+K]=True; i=s.find(m,i+1)
        tot+=len(s); cov+=mask.sum(); site+=len(st); sitecov+=sum(mask[p] for p in st if p<len(s))
    fs=sitecov/site if site else float('nan'); fp=cov/tot
    res[f]={'n':n,'motifs':top,'n_site_res':site,'frac_sites_cov':fs,'frac_pos_cov':fp,'enrich':fs/fp if fp and site else float('nan'),'split':'dev' if f in dev else 'test'}
    print(f,res[f]['split'],n,top,site,round(fs,3),round(fp,4),round(res[f]['enrich'],2))
T=[v for k,v in res.items() if v['split']=='test' and v['n_site_res']>0]
e=np.array([v['enrich'] for v in T]); fc=np.array([v['frac_sites_cov'] for v in T])
summ={'n_test_with_sites':len(T),'median_enrich':float(np.median(e)),'n_enrich_gt1':int((e>1).sum()),
 'sign_p':float(binomtest(int((e>1).sum()),len(e),0.5,alternative='greater').pvalue),'median_frac_sites_cov':float(np.median(fc))}
print(json.dumps(summ,indent=1)); json.dump({'families':res,'test_summary':summ},open('results/primary.json','w'),indent=1)
