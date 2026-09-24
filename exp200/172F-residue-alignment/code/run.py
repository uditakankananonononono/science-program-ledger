import json,time,numpy as np,torch
from scipy.stats import binomtest
from transformers import AutoTokenizer,AutoModel
torch.set_num_threads(2)
D={};h=None;s=[]
for l in open('../172-protein-grammar/data/scope40.fa'):
    if l.startswith('>'):
        if h: D[h[0]]=(h[1],''.join(s).upper())
        h=l[1:].split()[:2];s=[]
    else: s.append(l.strip())
D[h[0]]=(h[1],''.join(s).upper())
fold=lambda c:'.'.join(c.split('.')[:2])
S={'s1':json.load(open('../../ledger/exp200/172-protein-grammar/results/ids_p1.json')),'s2':json.load(open('results/ids_split2.json'))}
ids=sorted(set(i for v in S.values() for k in 'qr' for i in v[k]))
tok=AutoTokenizer.from_pretrained('facebook/esm2_t6_8M_UR50D');m=AutoModel.from_pretrained('facebook/esm2_t6_8M_UR50D').eval()
E={};t=time.time()
for n,i in enumerate(ids):
    with torch.no_grad(): x=m(**tok(D[i][1],return_tensors='pt')).last_hidden_state[0,1:-1]
    E[i]=torch.nn.functional.normalize(x,dim=1).half()
    if n%500==0: print('emb',n,len(ids),round(time.time()-t),flush=True)
def mp(i):
    v=E[i].float().mean(0);return v/v.norm()
res={}
for sp,v in S.items():
    Q,Rf=v['q'],v['r'];L=max(E[r].shape[0] for r in Rf)
    Rpad=torch.zeros(len(Rf),L,320,dtype=torch.float16);Rm=torch.zeros(len(Rf),L,dtype=torch.bool)
    for j,r in enumerate(Rf): n=E[r].shape[0];Rpad[j,:n]=E[r];Rm[j,:n]=True
    rl=Rm.sum(1).float();MP=torch.stack([mp(r) for r in Rf])
    soft=[];mean=[];t=time.time()
    for a,q in enumerate(Q):
        qe=E[q].float();sc=torch.empty(len(Rf))
        for c in range(0,len(Rf),200):
            Rc=Rpad[c:c+200].float();M=torch.einsum('ld,rkd->rlk',qe,Rc);M.masked_fill_(~Rm[c:c+200,None,:],-2)
            rowmax=M.max(2).values.mean(1);M.masked_fill_(~Rm[c:c+200,None,:],-2)
            colmax=M.max(1).values;colmax=(colmax*Rm[c:c+200]).sum(1)/rl[c:c+200]
            sc[c:c+200]=0.5*(rowmax+colmax)
        soft.append(int(sc.argmax()));mean.append(int((MP@mp(q)).argmax()))
        if a%50==0: print(sp,a,round(time.time()-t),flush=True)
    qf=[fold(D[q][0]) for q in Q];sa=np.array([fold(D[Rf[j]][0])==f for j,f in zip(soft,qf)]);ma=np.array([fold(D[Rf[j]][0])==f for j,f in zip(mean,qf)])
    b=int((sa&~ma).sum());c=int((~sa&ma).sum());p=binomtest(b,b+c,0.5).pvalue if b+c else 1.0
    cls={k:dict(n=int(sum(D[q][0][0]==k for q in Q)),soft=float(np.mean([x for x,q in zip(sa,Q) if D[q][0][0]==k])),mean=float(np.mean([x for x,q in zip(ma,Q) if D[q][0][0]==k]))) for k in 'abcd'}
    res[sp]=dict(soft=float(sa.mean()),mean=float(ma.mean()),b=b,c=c,p=p,by_class=cls,hits=dict(zip(Q,[Rf[j] for j in soft])))
    print(sp,res[sp]['soft'],res[sp]['mean'],p,flush=True)
s1,s2=res['s1'],res['s2']
res['G1']=bool(s1['soft']>=0.40 and s1['soft']-s1['mean']>=0.10 and s1['p']<0.01)
res['G2']=bool(s2['soft']>=0.30 and s2['soft']-s2['mean']>=0.08)
res['G3']=bool(s1['by_class']['c']['soft']-s1['by_class']['c']['mean']>=0.10)
json.dump(res,open('results/results.json','w'),indent=1)
print({k:res[k] for k in ['G1','G2','G3']})
