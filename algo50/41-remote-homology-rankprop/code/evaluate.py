import numpy as np,json
M=np.load('../data/sw.npy').astype(np.float64); ids=[l.split('\t') for l in open('../data/ids.tsv').read().splitlines()]
cls=[x[1] for x in ids]; L=np.array([int(x[2]) for x in ids],float); n=len(ids)
sf=np.array(['.'.join(c.split('.')[:3]) for c in cls]); fo=np.array(['.'.join(c.split('.')[:2]) for c in cls]); fa=np.array(cls)
E=0.041*np.outer(L,L)*n*np.exp(-0.267*M); np.fill_diagonal(E,np.inf)
K=np.exp(-E/100.0); np.fill_diagonal(K,0); Kn=K/np.maximum(K.sum(0,keepdims=True),1e-300)
def auc(s,y):
    from scipy.stats import rankdata
    r=rankdata(s); p=y.sum(); q=len(y)-p; return (r[y].sum()-p*(p+1)/2)/(p*q)
def roc50(s,y):
    o=np.argsort(-s,kind='stable'); yy=y[o]; p=yy.sum(); fp=0; tp=0; a=0
    for v in yy:
        if v: tp+=1
        else:
            fp+=1; a+=tp
            if fp==50: break
    return a/(50*p)
Q=[q for q in range(n) if (((sf==sf[q])&(fa!=fa[q])).sum()-0)>=2]
Y0=np.exp(-E[:,Q]/100.0); Y0[Q,np.arange(len(Q))]=0; V=Y0.copy()
for _ in range(20): V=Y0+0.95*(Kn@V)
Vcol={q:V[:,k] for k,q in enumerate(Q)}
rows=[]
for q in Q:
    pos=(sf==sf[q])&(fa!=fa[q]); pos[q]=False
    if pos.sum()<2: continue
    neg=fo!=fo[q]; keep=pos|neg; y=pos[keep]
    v=Vcol[q]
    sc={'RAW':M[q],'EVAL':-E[q],'RP':v}
    rows.append([auc(sc[k][keep],y) for k in ('RAW','EVAL','RP')]+[roc50(sc[k][keep],y) for k in ('RAW','EVAL','RP')])
A=np.array(rows); np.savetxt('../results/per_query.tsv',A,delimiter='\t',header='auc_raw\tauc_eval\tauc_rp\troc50_raw\troc50_eval\troc50_rp',comments='')
m=A.mean(0); rng=np.random.default_rng(41); B=[]
for _ in range(2000):
    ii=rng.integers(0,len(A),len(A)); mm=A[ii].mean(0); B.append([mm[2]-mm[1],mm[5]-mm[4]])
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]
res={'n_query':len(A),'auc':{'RAW':m[0],'EVAL':m[1],'RP':m[2]},'roc50':{'RAW':m[3],'EVAL':m[4],'RP':m[5]},
 'd1':m[2]-m[1],'ci1':ci(B[:,0]),'d2':m[5]-m[4],'ci2':ci(B[:,1]),'frac_rp_ge':float((A[:,2]>=A[:,1]).mean())}
res['gates']={'G1':bool(res['d1']>=0.03 and res['ci1'][0]>0),'G2':bool(res['ci2'][0]>0),'G3':bool(res['frac_rp_ge']>=0.6)}
json.dump(res,open('../results/metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
