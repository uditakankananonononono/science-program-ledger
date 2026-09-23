import pandas as pd, numpy as np, json, gzip, io, os
from sklearn.metrics import roc_auc_score
rng=np.random.default_rng(0)
S=pd.read_csv('data/sample.tsv',sep='\t',header=None,names=['acc','gene','len','ncit'])
q1,q2=S.ncit.quantile([1/3,2/3]); S['tier']=np.where(S.ncit<=q1,'low',np.where(S.ncit>q2,'high','mid'))
V=pd.read_csv('data/clinvar_missense_sample.tsv',sep='\t',header=None,names=['gene','pv','y','stars','lasteval','varid'])
rows=[]
for r in S.itertuples():
    am=f'data/af/{r.acc}.am.gz'; pl=f'data/af/{r.acc}.pl.gz'
    if not (os.path.exists(am) and os.path.exists(pl)): continue
    A=pd.read_csv(io.BytesIO(gzip.decompress(open(am,'rb').read())))
    amd=dict(zip(A.protein_variant,A.am_pathogenicity)); amc=dict(zip(A.protein_variant,A.am_class))
    P=json.loads(gzip.decompress(open(pl,'rb').read())); pld=dict(zip(P['residueNumber'],P['confidenceScore']))
    for v in V[V.gene==r.gene].itertuples():
        if v.pv in amd:   # AM file keys are ref+pos+alt on the UniProt canonical sequence -> implicit ref check
            pos=int(v.pv[1:-1]); rows.append((r.gene,r.tier,r.ncit,v.pv,v.y,v.stars,v.lasteval,amd[v.pv],amc[v.pv],pld.get(pos,np.nan)))
D=pd.DataFrame(rows,columns=['gene','tier','ncit','pv','y','stars','lasteval','am','am_class','plddt'])
D.to_csv('results/variants_scored.csv',index=False)
def auc(d): 
    return roc_auc_score(d.y,d.am) if d.y.nunique()==2 else np.nan
def boot_diff(d):
    H=d[d.tier=='high']; L=d[d.tier=='low']; gh=H.gene.unique(); gl=L.gene.unique()
    Hg={g:x for g,x in H.groupby('gene')}; Lg={g:x for g,x in L.groupby('gene')}
    obs=auc(H)-auc(L); bs=[]
    for i in range(1000):
        h=pd.concat([Hg[g] for g in rng.choice(gh,len(gh))]); l=pd.concat([Lg[g] for g in rng.choice(gl,len(gl))])
        bs.append(auc(h)-auc(l))
    return float(obs),[float(np.nanpercentile(bs,2.5)),float(np.nanpercentile(bs,97.5))]
res={'n_genes_scored':int(D.gene.nunique()),'n_var':int(len(D)),'tier_cut':[float(q1),float(q2)]}
for t in ['low','mid','high']:
    d=D[D.tier==t]; res[t]={'genes':int(d.gene.nunique()),'PLP':int(d.y.sum()),'BLB':int((d.y==0).sum()),'auc':float(auc(d)),
      'PLP_frac_plddt_lt70':float((d[d.y==1].plddt<70).mean()),'PLP_frac_AM_pathogenic':float((d[d.y==1].am_class=='LPath').mean()),
      'BLB_frac_AM_pathogenic':float((d[d.y==0].am_class=='LPath').mean())}
res['G1_diff'],res['G1_ci']=boot_diff(D)
res['G2_diff'],res['G2_ci']=boot_diff(D[D.plddt>=70])
print(json.dumps(res,indent=1)); json.dump(res,open('results/primary.json','w'),indent=1)
