import pandas as pd, numpy as np, hashlib, json, os, sys, re
from Bio.Align import substitution_matrices
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score, average_precision_score
assert hashlib.sha256(open('cv.tsv','rb').read()).hexdigest()=='c04713fd7a23d8816034a3e550753d0682298e307fce7ea0460f00615b1d1f24'
B=substitution_matrices.load('BLOSUM62')
T3={'Ala':'A','Arg':'R','Asn':'N','Asp':'D','Cys':'C','Gln':'Q','Glu':'E','Gly':'G','His':'H','Ile':'I','Leu':'L','Lys':'K','Met':'M','Phe':'F','Pro':'P','Ser':'S','Thr':'T','Trp':'W','Tyr':'Y','Val':'V'}
G={'S':(1.42,9.2,32),'R':(.65,10.5,124),'L':(0,4.9,111),'P':(.39,8.0,32.5),'T':(.71,8.6,61),'A':(0,8.1,31),'V':(0,5.9,84),'G':(.74,9.0,3),'I':(0,5.2,111),'F':(0,5.2,132),'Y':(.20,6.2,136),'C':(2.75,5.5,55),'H':(.58,10.4,96),'Q':(.89,10.5,85),'N':(1.33,11.6,56),'K':(.33,11.3,119),'D':(1.38,13.0,54),'E':(.92,12.3,83),'M':(0,5.7,105),'W':(.13,5.4,170)}
KD={'A':1.8,'R':-4.5,'N':-3.5,'D':-3.5,'C':2.5,'Q':-3.5,'E':-3.5,'G':-0.4,'H':-3.2,'I':4.5,'L':3.8,'K':-3.9,'M':1.9,'F':2.8,'P':-1.6,'S':-0.8,'T':-0.7,'W':-0.9,'Y':-1.3,'V':4.2}
def gr(a,b): return 50.723*np.sqrt(1.833*(G[a][0]-G[b][0])**2+0.1018*(G[a][1]-G[b][1])**2+0.000399*(G[a][2]-G[b][2])**2)
assert abs(gr('C','W')-215)<=2 and abs(gr('S','R')-110)<=2 and abs(gr('L','I')-5)<=1 and B['A']['A']==4 and B['W']['W']==11,'equiv'
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
AA=sorted(G); CLS={}
for s,i in (('AVLIM',0),('FWY',1),('STNQ',2),('KRH',3),('DE',4),('G',5),('PC',6)):
    for a in s: CLS[a]=i
d=pd.read_csv('cv.tsv',sep='\t'); d=d[d.protein_change!='p.Arg652Ter'].reset_index(drop=True); m=d.protein_change.str.extract(r'^p\.([A-Za-z]{3})(\d+)([A-Za-z]{3})$'); d['ref']=m[0].map(T3); d['alt']=m[2].map(T3); assert d.ref.notna().all() and d.alt.notna().all()
y=(d.binary_class=='positive').astype(int).values
bl=np.array([-B[a][b] for a,b in zip(d.ref,d.alt)],float); gm=np.array([gr(a,b) for a,b in zip(d.ref,d.alt)])
def feats_lr2(): return np.c_[bl,gm/100]
def feats_sub():
    X=[bl,gm/100,[KD[b]-KD[a] for a,b in zip(d.ref,d.alt)],[(G[b][2]-G[a][2])/100 for a,b in zip(d.ref,d.alt)]]
    X=list(map(np.asarray,X)); Xr=np.array([[a==x for x in AA] for a in d.ref],float); Xa=np.array([[a==x for x in AA] for a in d.alt],float)
    Cr=np.array([[CLS[a]==k for k in range(7)] for a in d.ref],float); Ca=np.array([[CLS[a]==k for k in range(7)] for a in d.alt],float); same=np.array([CLS[a]==CLS[b] for a,b in zip(d.ref,d.alt)],float)
    return np.c_[np.array(X).T,Xr,Xa,Cr,Ca,same]
genes=np.array(sorted(d.gene.unique())); perm=np.random.RandomState(5).permutation(len(genes)); dev_g=set(genes[perm[:len(genes)//2]])
isdev=d.gene.isin(dev_g).values; print('dev',isdev.sum(),'test',(~isdev).sum(),flush=True)
Xl=feats_lr2(); Xs=feats_sub(); grp=d.gene.values
def cv_auc(X,C,idx):
    oof=np.zeros(len(idx)); gk=GroupKFold(5)
    for tr,te in gk.split(X[idx],y[idx],grp[idx]):
        mu=X[idx][tr].mean(0); sd=X[idx][tr].std(0)+1e-9
        mdl=LogisticRegression(C=C,max_iter=2000).fit((X[idx][tr]-mu)/sd,y[idx][tr]); oof[te]=mdl.decision_function((X[idx][te]-mu)/sd)
    return roc_auc_score(y[idx],oof)
di=np.where(isdev)[0]; ti=np.where(~isdev)[0]
dev_base={'BLOSUM62':roc_auc_score(y[di],bl[di]),'Grantham':roc_auc_score(y[di],gm[di]),'LR2':cv_auc(Xl,1.0,di)}
head=max(dev_base,key=dev_base.get)
Cs=(0.03,0.1,0.3,1,3); dev_sub={C:cv_auc(Xs,C,di) for C in Cs}; Cb=max(Cs,key=lambda c:(dev_sub[c],-c)); print('DEV',dev_base,head,dev_sub,Cb,flush=True)
def fit_pred(X,C):
    mu=X[di].mean(0); sd=X[di].std(0)+1e-9; mdl=LogisticRegression(C=C,max_iter=2000).fit((X[di]-mu)/sd,y[di]); return mdl.decision_function((X[ti]-mu)/sd)
sc={'BLOSUM62':bl[ti],'Grantham':gm[ti],'LR2':fit_pred(Xl,1.0),'SUB-LR':fit_pred(Xs,Cb)}
yt=y[ti]; auc={k:roc_auc_score(yt,v) for k,v in sc.items()}; ap={k:average_precision_score(yt,v) for k,v in sc.items()}
gt=grp[ti]; ug=np.unique(gt); ix={g:np.where(gt==g)[0] for g in ug}; rs=np.random.RandomState(7); ds=[]
for _ in range(5000):
    s=np.concatenate([ix[g] for g in ug[rs.randint(0,len(ug),len(ug))]])
    if len(set(yt[s]))<2: continue
    ds.append(roc_auc_score(yt[s],sc['SUB-LR'][s])-roc_auc_score(yt[s],sc[head][s]))
lo,hi=np.percentile(ds,[2.5,97.5]); diff=auc['SUB-LR']-auc[head]
v='WIN' if diff>=0.03 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
res=dict(n_test=int(len(ti)),test_pos_frac=float(yt.mean()),dev_baselines=dev_base,head=head,dev_sub=dev_sub,C=Cb,C_at_edge=Cb in (0.03,3),test_auc=auc,test_ap=ap,diff=float(diff),ci=[float(lo),float(hi)],verdict=v)
json.dump(res,open('results.json','w'),indent=1,default=float); print(json.dumps(res,default=float))
