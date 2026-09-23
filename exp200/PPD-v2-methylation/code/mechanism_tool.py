import json,gzip,numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
Z=np.load('/tmp/ppdv2_beta.npz',allow_pickle=True);B=Z['beta'];probes=Z['probes']
meta=json.load(open('/tmp/ppdv2_meta.json'));y=np.array(meta['ppd'])
M=np.log2(np.clip(B,1e-4,1-1e-4)/np.clip(1-B,1e-4,1-1e-4))
def welch_t(X,y):
    X1=X[:,y==1];X0=X[:,y==0]
    return np.abs((X1.mean(1)-X0.mean(1))/np.sqrt(X1.var(1,ddof=1)/X1.shape[1]+X0.var(1,ddof=1)/X0.shape[1]+1e-12))
idx=np.argsort(welch_t(M,y))[-200:]
sc=StandardScaler().fit(M[idx].T)
clf=LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,C=1.0,tol=1e-2,max_iter=1000,random_state=0)
clf.fit(sc.transform(M[idx].T),y)
sel=probes[idx]; coef=clf.coef_[0]
mani={}
with gzip.open('data/HM450.hg38.manifest.gencode.v22.tsv.gz','rt') as f:
    hdr=f.readline().rstrip('\n').split('\t');i_pid=hdr.index('probeID');i_g=hdr.index('geneNames')
    for line in f:
        p=line.rstrip('\n').split('\t');mani[p[i_pid]]=p[i_g]
nz=[(s,float(c),mani.get(s,'')) for s,c in zip(sel,coef) if abs(c)>1e-6]
nz.sort(key=lambda x:-abs(x[1]))
genes=sorted({g for _,_,gs in nz for g in gs.split(';') if g and g!='NA'})
json.dump({'probes':sel.tolist(),'coef':[float(c) for c in coef],'mean':sc.mean_.tolist(),'scale':sc.scale_.tolist(),
 'nonzero':nz,'panel_genes':genes},open('results/panel_full.json','w'),indent=1)
print('nonzero coefs',len(nz),'panel genes',len(genes))
print('top10:',nz[:10])
lit=[g for g in genes if g in ('HP1BP3','TTC9B','OXTR','ESR1','ESR2','NR3C1','FKBP5','BDNF','SLC6A4','COMT','CRH','CRHR1')]
print('literature-watchlist overlap:',lit)
