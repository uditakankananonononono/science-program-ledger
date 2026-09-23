import itertools,numpy as np,json
exec(open('evaluate.py').read().split("res={}")[0])
def consS(det,S,k):
    pts=sorted((int(p),m) for m in S for p in det[m]); out=[]; cl=[]
    for p,m in pts:
        if cl and p-cl[0][0]>W:
            if len({x[1] for x in cl})>=k: out.append(int(np.median([x[0] for x in cl])))
            cl=[]
        cl.append((p,m))
    if cl and len({x[1] for x in cl})>=k: out.append(int(np.median([x[0] for x in cl])))
    return np.array(out)
grid=[]
for n in (3,4,5):
    for S in itertools.combinations(M,n):
        for k in range(2,n+1): grid.append((F1(tab(DS1,lambda r:consS(D[r]['det'],S,k)).sum(0)),-n,k,S))
grid.sort(reverse=True); f,_,k,S=grid[0]
res={'chosen_S':S,'chosen_k':k,'DS1_F1':f,'top5_DS1':[(g[0],g[3],g[2]) for g in grid[:5]]}
Tp=tab(DS2,lambda r:consS(D[r]['det'],S,k)); Tb=tab(DS2,lambda r:D[r]['det']['pantompkins1985'])
res['F1_pivot']=F1(Tp.sum(0)); res['F1_PT']=F1(Tb.sum(0)); res['TP_FP_FN_pivot']=Tp.sum(0).tolist(); res['TP_FP_FN_PT']=Tb.sum(0).tolist()
rng=np.random.default_rng(33); B=[]
for _ in range(2000):
    ii=rng.integers(0,len(DS2),len(DS2)); B.append(F1(Tp[ii].sum(0))-F1(Tb[ii].sum(0)))
res['d']=res['F1_pivot']-res['F1_PT']; res['ci']=[float(x) for x in np.percentile(B,[2.5,97.5])]
res['n_low_pivot']=int(sum(F1(t)<0.99 for t in Tp)); res['n_low_PT']=int(sum(F1(t)<0.99 for t in Tb))
res['pivot_gates']={'P1':bool(res['d']>0 and res['ci'][0]>0),'P2':bool(res['n_low_pivot']<=res['n_low_PT'])}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
