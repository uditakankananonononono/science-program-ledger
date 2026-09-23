import json, numpy as np, pandas as pd
from scipy.stats import binomtest
exec(open('code/run.py').read())
out={}
X,lab=load('GSE87466','GPL13158','!Sample_characteristics_ch1')
ctrl=np.where(np.char.find(lab,'Normal')>=0)[0]; case=np.where(np.char.find(lab,'Ulcerative')>=0)[0]
D,N,names=analyse(X,ctrl,case,nperm=2000)
from statsmodels.stats.multitest import multipletests
D['fdr']=multipletests(D.p,method='fdr_bh')[1]; D.to_csv('results/pivot1_discovery_GSE87466.csv',index=False)
S=D[D.fdr<0.10]; out['G1_n_sig']=int(len(S)); out['G1_n_tested']=int(len(D)); out['G1_frac_loss']=float((S.delta<0).mean()) if len(S) else None
print('G1',out,flush=True)
sign=dict(zip(S.pathway,np.sign(S.delta)))
def settest(X,ctrl,case,tag):
    R,Nr,nm=analyse(X,ctrl,case,paths_named=set(sign))
    s=np.array([sign[n] for n in nm]); stat=(R.delta.values*s).mean(); null=(Nr*s).mean(1)
    conc=float((np.sign(R.delta.values)==s).mean())
    r={'n':len(nm),'concordant_frac':conc,'binom_p':float(binomtest(int(conc*len(nm)),len(nm),0.5,alternative='greater').pvalue),
       'set_stat':float(stat),'set_p':float((1+(null>=stat).sum())/(len(null)+1)),'mean_abs_t':float(R.mean_abs_t.mean())}
    R.to_csv(f'results/pivot1_{tag}.csv',index=False); print(tag,r,flush=True); return r
X2,lab2=load('GSE38713','GPL570','!Sample_source_name_ch1')
c2=np.where(np.char.find(lab2,'non-inflammatory control')>=0)[0]
act=np.where(np.char.find(lab2,'active disease (involved')>=0)[0]
rem=np.where(np.char.find(lab2,'remission')>=0)[0]; noninv=np.where(np.char.find(lab2,'non-involved')>=0)[0]
if len(S):
    out['G2_GSE38713_active']=settest(X2,c2,act,'rep_GSE38713_active')
    out['G3_GSE38713_noninflamed']=settest(X2,c2,np.r_[rem,noninv],'rep_GSE38713_noninflamed')
    out['GSE38713_remission_only']=settest(X2,c2,rem,'rep_GSE38713_remission')
    out['GSE38713_noninvolved_only']=settest(X2,c2,noninv,'rep_GSE38713_noninvolved')
    X3,lab3=load('GSE9452','GPL570','!Sample_characteristics_ch1')
    c3=np.where(np.char.find(lab3,'Control')>=0)[0]; ni=np.where((np.char.find(lab3,'Ulcerative')>=0)&(np.char.find(lab3,'no macroscopic')>=0))[0]
    inf=np.where(np.char.find(lab3,'inflammation vissible')>=0)[0]
    out['G3_GSE9452_noninflamed']=settest(X3,c3,ni,'rep_GSE9452_noninflamed')
    out['GSE9452_inflamed']=settest(X3,c3,inf,'rep_GSE9452_inflamed')
json.dump(out,open('results/pivot1.json','w'),indent=1); print(json.dumps(out,indent=1))
