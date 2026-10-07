import gzip, hashlib, numpy as np, scipy.sparse as sp, json
from scipy.stats import rankdata
assert hashlib.sha256(open('intact.tsv.gz','rb').read()).hexdigest()=='7e9f6bba8ea0511e510b71a383817dc22b32469e799bb3457c769e331d442a85'
E={}
for i,l in enumerate(gzip.open('intact.tsv.gz','rt')):
    if i==0: continue
    f=l.rstrip('\n').split('\t'); a,b=f[0],f[1]
    if not(a.startswith('uniprotkb:') and b.startswith('uniprotkb:')): continue
    a=a[10:].split('-')[0]; b=b[10:].split('-')[0]
    if a==b: continue
    k=tuple(sorted((a,b))); E[k]=min(E.get(k,'9'),f[9])
def adj(edges,idx):
    r=[idx[a] for a,b in edges]+[idx[b] for a,b in edges]; c=[idx[b] for a,b in edges]+[idx[a] for a,b in edges]
    return sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(len(idx),len(idx)))
def base_scores(A,us,vs):
    k=np.asarray(A.sum(1)).ravel(); inv=np.where(k>0,1/np.maximum(k,1),0); ila=np.where(k>1,1/np.log(np.maximum(k,2)),0); isq=np.where(k>0,1/np.sqrt(np.maximum(k,1)),0)
    out={'CN':[],'AA':[],'RA':[],'L3':[]}
    Au=A[us,:];Av=A[vs,:]
    out['CN']=np.asarray(Au.multiply(Av).sum(1)).ravel()
    out['AA']=np.asarray(Au.multiply(Av).multiply(ila[None,:]).sum(1)).ravel()
    out['RA']=np.asarray(Au.multiply(Av).multiply(inv[None,:]).sum(1)).ravel()
    Ds=sp.diags(isq); W=(Au@Ds)@A  # sum_a A[u,a]/sqrt(k_a) A[a,b]
    out['L3']=np.asarray(W.multiply(Av@Ds).sum(1)).ravel()
    return out
# hand check: path graph 0-1-2-3 plus 1-3 ; pair (0,2): common nb {1}, k1=3 ; L3 paths 0-1-3-2: 1/sqrt(3*2)
T=adj([(('0','1')),('1','2'),('2','3'),('1','3')],{'0':0,'1':1,'2':2,'3':3}); s=base_scores(T,[0],[2])
assert s['CN'][0]==1 and abs(s['AA'][0]-1/np.log(3))<1e-9 and abs(s['RA'][0]-1/3)<1e-9 and abs(s['L3'][0]-1/np.sqrt(6))<1e-9,'hand check'
def dcd_raw(A,alpha,us,vs,chunk=1500):
    k=np.asarray(A.sum(1)).ravel(); d=np.where(k>0,k**-alpha,0); An=sp.diags(d)@A@sp.diags(d); An=An.tocsr()
    o2=[];o3=[];o4=[]
    for s in range(0,len(us),chunk):
        u=us[s:s+chunk]; v=vs[s:s+chunk]; Pu=An[u,:]; Pv=An[v,:]
        Wu=Pu@An; Wv=Pv@An
        o2.append(np.asarray(Pu.multiply(Pv).sum(1)).ravel()); o3.append(np.asarray(Wu.multiply(Pv).sum(1)).ravel()); o4.append(np.asarray(Wu.multiply(Wv).sum(1)).ravel())
    return np.concatenate(o2),np.concatenate(o3),np.concatenate(o4)
def auc(sc,y):
    r=rankdata(sc); n1=y.sum(); n0=len(y)-n1; return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
def ap(sc,y):
    o=np.argsort(-sc,kind='stable'); yy=y[o]; return float((np.cumsum(yy)/np.arange(1,len(yy)+1))[yy==1].mean())
def build(train_end,t0,t1,seed_p=3,seed_n=4):
    tr=[k for k,d in E.items() if d<=train_end]; nodes=sorted({x for k in tr for x in k}); idx={n:i for i,n in enumerate(nodes)}
    pos=sorted(k for k,d in E.items() if t0<=d<=t1 and k[0] in idx and k[1] in idx)
    rs=np.random.RandomState(seed_p); 
    if len(pos)>10000: pos=[pos[i] for i in rs.choice(len(pos),10000,replace=False)]
    rn=np.random.RandomState(seed_n); ends=[x for k in pos for x in k]; neg=[]
    while len(neg)<10000:
        a=ends[rn.randint(len(ends))]; b=ends[rn.randint(len(ends))]
        if a!=b and tuple(sorted((a,b))) not in E: neg.append((a,b))
    pairs=pos+neg; y=np.array([1]*len(pos)+[0]*len(neg))
    us=np.array([idx[a] for a,b in pairs]); vs=np.array([idx[b] for a,b in pairs])
    return adj(tr,idx),us,vs,y,len(pos),len(nodes),len(tr)
import os,sys
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
A,us,vs,y,npos,nn,ne=build('2010/12/31','2011/01/01','2013/12/31'); print('DEV',npos,nn,ne,flush=True)
bs=base_scores(A,us,vs); dev_b={k:auc(v,y) for k,v in bs.items()}
head=max(('AA','RA','L3'),key=lambda k:dev_b[k]); print('DEV base',dev_b,head,flush=True)
best=None; dev_d={}
for al in (0.5,0.75,1.0):
    r2,r3,r4=dcd_raw(A,al,us,vs)
    for w3 in (0,0.5,1):
        for w4 in (0,0.5,1):
            a=auc(r2+w3*r3+w4*r4,y); dev_d[f'{al},{w3},{w4}']=a
            if best is None or a>best[0]+1e-12: best=(a,al,w3,w4)
print('DEV best',best,flush=True)
_,al,w3,w4=best
A,us,vs,y,npos,nn,ne=build('2015/12/31','2016/01/01','2021/12/31'); print('FINAL',npos,nn,ne,flush=True)
bs=base_scores(A,us,vs); r2,r3,r4=dcd_raw(A,al,us,vs); sd=r2+w3*r3+w4*r4
tb={k:auc(v,y) for k,v in bs.items()}; aps={k:ap(v,y) for k,v in bs.items()}; aps['DCD']=ap(sd,y); tb['DCD']=auc(sd,y)
rs=np.random.RandomState(7); ds=[]
for _ in range(2000):
    i=rs.randint(0,len(y),len(y)); ds.append(auc(sd[i],y[i])-auc(bs[head][i],y[i]))
lo,hi=np.percentile(ds,[2.5,97.5]); d=tb['DCD']-tb[head]
v='WIN' if d>=0.02 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
res=dict(dev_baselines=dev_b,head=head,dev_dcd_best=dict(auc=best[0],alpha=al,w3=w3,w4=w4),at_edge=bool(al in (0.5,1.0) or w3 in (0,1) or w4 in (0,1)),test_auc=tb,test_ap=aps,diff=d,ci=[lo,hi],verdict=v,n_pos=npos,n_nodes=nn,n_train_edges=ne,frac_head_zero=float((bs[head]==0).mean()),frac_dcd_zero=float((sd==0).mean()))
json.dump(res,open('results.json','w'),indent=1,default=float); print(json.dumps(res,default=float))
