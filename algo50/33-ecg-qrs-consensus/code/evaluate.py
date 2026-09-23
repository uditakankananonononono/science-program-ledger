import pickle,numpy as np,json
D=pickle.load(open('../data/detections.pkl','rb'))
DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]; DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
M=['pantompkins1985','hamilton2002','elgendi2010','christov2004','neurokit']; TOL=54; W=27
def match(ref,det):
    ref=np.sort(ref); det=np.sort(det); i=j=tp=0
    while i<len(ref) and j<len(det):
        d=det[j]-ref[i]
        if abs(d)<=TOL: tp+=1; i+=1; j+=1
        elif d<0: j+=1
        else: i+=1
    return tp,len(det)-tp,len(ref)-tp
def cons(det,k):
    pts=sorted((int(p),m) for m in M for p in det[m])
    out=[]; cl=[]
    for p,m in pts:
        if cl and p-cl[0][0]>W:
            if len({x[1] for x in cl})>=k: out.append(int(np.median([x[0] for x in cl])))
            cl=[]
        cl.append((p,m))
    if cl and len({x[1] for x in cl})>=k: out.append(int(np.median([x[0] for x in cl])))
    return np.array(out)
def tab(recs,f): return np.array([match(D[r]['ref'],f(r)) for r in recs])
F1=lambda t:2*t[0]/(2*t[0]+t[1]+t[2])
res={}
ds1={('k%d'%k):F1(tab(DS1,lambda r,k=k:cons(D[r]['det'],k)).sum(0)) for k in range(1,6)}
ds1.update({m:F1(tab(DS1,lambda r,m=m:D[r]['det'][m]).sum(0)) for m in M})
res['DS1_F1']=ds1; k=max(range(1,6),key=lambda k:ds1['k%d'%k]); best=max(M,key=lambda m:ds1[m]); res['k']=k; res['best_single_DS1']=best
T={'CONS':tab(DS2,lambda r:cons(D[r]['det'],k))}; T.update({m:tab(DS2,lambda r,m=m:D[r]['det'][m]) for m in M})
res['DS2']={n:{'sens':float(t[:,0].sum()/(t[:,0].sum()+t[:,2].sum())),'ppv':float(t[:,0].sum()/(t[:,0].sum()+t[:,1].sum())),'F1':float(F1(t.sum(0))),'TP':int(t[:,0].sum()),'FP':int(t[:,1].sum()),'FN':int(t[:,2].sum())} for n,t in T.items()}
rf=lambda t:[float(F1(x)) for x in t]; res['per_record_F1']={n:dict(zip(map(str,DS2),rf(t))) for n,t in T.items()}
rng=np.random.default_rng(33); B=[]
for _ in range(2000):
    ii=rng.integers(0,len(DS2),len(DS2)); c=F1(T['CONS'][ii].sum(0))
    B.append([c-F1(T['pantompkins1985'][ii].sum(0)),c-F1(T[best][ii].sum(0))])
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]; d=res['DS2']
res['d1']=d['CONS']['F1']-d['pantompkins1985']['F1']; res['ci1']=ci(B[:,0])
res['d2']=d['CONS']['F1']-d[best]['F1']; res['ci2']=ci(B[:,1])
low=lambda n:sum(v<0.99 for v in res['per_record_F1'][n].values()); res['n_low_CONS']=low('CONS'); res['n_low_PT']=low('pantompkins1985')
res['gates']={'G1':bool(res['d1']>=0.003 and res['ci1'][0]>0),'G2':bool(res['ci2'][0]>0),'G3':bool(res['n_low_CONS']<res['n_low_PT'])}
json.dump(res,open('../results/metrics.json','w'),indent=1); print(json.dumps({k:v for k,v in res.items() if k!='per_record_F1'},indent=1))
