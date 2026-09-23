import pandas as pd, numpy as np, json, re, os
from collections import Counter, defaultdict
rng=np.random.default_rng(0)
F={'lysine':['M00016','M00525','M00526','M00527','M00030','M00433'],'isoprenoid':['M00096','M00095','M00849'],
   'glycolysis':['M00001','M00008','M00633'],'heme':['M00121','M00926','M00847'],'menaquinone':['M00116','M00930','M00931']}
S=pd.read_csv('data/sample.tsv',sep='\t',header=None,names=['t','code','lin'])
def phylum(l):
    f=[x.strip() for x in l.split(';')]
    for x in f[1:]:
        if x.endswith('ota'): return x
    return f[2] if len(f)>2 else f[-1]
S['phylum']=S.lin.map(phylum)
mods={}
for c in S.code:
    p=f'data/modules/{c}.tsv'
    txt=open(p).read() if os.path.exists(p) else ''
    mods[c]={m.split('_')[-1] for m in re.findall(r'md:\S+',txt)}
S=S[S.code.map(lambda c: len(mods[c])>0)].reset_index(drop=True)
def cramers(x,y):
    t=pd.crosstab(x,y).values; n=t.sum(); e=np.outer(t.sum(1),t.sum(0))/n
    chi=((t-e)**2/np.where(e>0,e,1)).sum(); k=min(t.shape)-1
    return np.sqrt(chi/(n*k)) if k>0 else np.nan
out={'n_genomes':int(len(S)),'phyla':S.phylum.value_counts().to_dict()}
g3=0
for fn,ms in F.items():
    r=S.code.map(lambda c:'+'.join(sorted(m for m in ms if m in mods[c])))
    d=S.assign(route=r)[r!='']
    vc=d.route.value_counts(); d['route']=d.route.where(d.route.map(vc)>=5,'other')
    V=cramers(d.route,d.phylum)
    null=[cramers(pd.Series(rng.permutation(d.route.values)),d.phylum.reset_index(drop=True)) for _ in range(1000)]
    p=(1+sum(n>=V for n in null))/1001
    rp=d.groupby('route').phylum.nunique().to_dict()
    # convergence: a route used in >=3 phyla, where in those phyla a different route also occurs
    conv=[]
    for rt,npy in rp.items():
        if rt=='other' or npy<3: continue
        ph=set(d.phylum[d.route==rt]); other=set(d.phylum[(d.route!=rt)&(d.route!='other')])
        if len(ph&other)>=1: conv.append(rt)
    g3+=bool(conv)
    out[fn]={'n':int(len(d)),'routes':d.route.value_counts().to_dict(),'cramers_V':float(V),'perm_p':float(p),'route_n_phyla':rp,'convergent_routes':conv,
      'route_by_phylum':pd.crosstab(d.phylum,d.route).to_dict()}
    print(fn,len(d),d.route.value_counts().to_dict(),'V=%.3f p=%.4f'%(V,p),rp,conv)
Vs=[out[f]['cramers_V'] for f in F]; ps=[out[f]['perm_p'] for f in F]
out['summary']={'median_V':float(np.median(Vs)),'n_p_lt_0.01':int(sum(p<0.01 for p in ps)),'n_functions_convergent':g3}
print(json.dumps(out['summary'])); print(out['phyla'])
json.dump(out,open('results/primary.json','w'),indent=1,default=str)
