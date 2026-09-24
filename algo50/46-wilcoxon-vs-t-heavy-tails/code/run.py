import numpy as np, json
from scipy.stats import ttest_ind, mannwhitneyu
rng=np.random.default_rng(1); n=20; R=4000; out={}
gen={'NORMAL':lambda s:rng.standard_normal(s),'T3':lambda s:rng.standard_t(3,s)}
for name,d in [('NORMAL',0.8),('T3',0.8),('T3_null',0.0)]:
    g=gen[name.split('_')[0]]; a=g((R,n)); b=g((R,n))+d
    pt=ttest_ind(a,b,axis=1,equal_var=False).pvalue; pw=mannwhitneyu(a,b,axis=1).pvalue
    out[name]={'WELCH':float((pt<0.05).mean()),'WRS':float((pw<0.05).mean())}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
