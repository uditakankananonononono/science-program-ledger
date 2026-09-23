import json,glob,numpy as np,sys
import torch,torch.nn as nn
torch.manual_seed(20260924);np.random.seed(20260924)
torch.set_num_threads(1)
AA='ACDEFGHIKLMNPQRSTVWY'; AAI={a:i for i,a in enumerate(AA)}
def load(fj):
    d=json.load(open(fj))
    F=np.array(d['F'],dtype=np.float32); y=np.array(d['truth'],dtype=np.int64)
    ai=np.array([AAI.get(a,19) for a in d['seq']],dtype=np.int64)
    return d,F,ai,y
def windows(F,ai,w=4):
    n=len(ai)
    idx=np.arange(n)
    W=np.zeros((n,2*w+1,F.shape[1]),dtype=np.float32); WA=np.zeros((n,2*w+1),dtype=np.int64)
    for i in range(n):
        lo,hi=max(0,i-w),min(n,i+w+1)
        k=hi-lo; off=max(0,w-i)
        W[i,off:off+k]=F[lo:hi]; WA[i,off:off+k]=ai[lo:hi]
        if off>0: W[i,:off]=F[lo]; WA[i,:off]=ai[lo]
        if off+k<2*w+1: W[i,off+k:]=F[hi-1]; WA[i,off+k:]=ai[hi-1]
    return W,WA
class Net(nn.Module):
    def __init__(s,nbase=7,nextra=10):
        super().__init__()
        s.emb=nn.Embedding(20,8)
        s.c1=nn.Conv1d(8+nbase,64,3,padding=1); s.c2=nn.Conv1d(64,64,3,padding=1)
        s.h1=nn.Linear(64+nextra,32); s.h2=nn.Linear(32,1); s.drop=nn.Dropout(0.3)
        s.act=nn.GELU()
    def forward(s,wa,wb,extra):
        e=s.emb(wa).permute(0,2,1)          # B,8,9
        x=torch.cat([e,wb.permute(0,2,1)],1) # B,15,9
        x=s.act(s.c1(x)); x=s.act(s.c2(x))
        c=x[:,:,4]                           # center position
        z=torch.cat([c,extra],1)
        z=s.drop(s.act(s.h1(z)))
        return s.h2(z).squeeze(-1)
def prep(ds):
    Ws,WAs,Es,Ys=[],[],[],[]
    for d,F,ai,y in ds:
        W,WA=windows(F,ai)
        Ws.append(W[:,:,:7]); WAs.append(WA); Es.append(F[:,7:]); Ys.append(y)
    return (torch.tensor(np.concatenate(Ws)),torch.tensor(np.concatenate(WAs)),
            torch.tensor(np.concatenate(Es)),torch.tensor(np.concatenate(Ys)))
def train_model(ds,seed=0,epochs=30):
    torch.manual_seed(seed)
    W,WA,E,Y=prep(ds)
    net=Net(); opt=torch.optim.Adam(net.parameters(),lr=1e-3,weight_decay=1e-4)
    pw=torch.tensor([(Y==0).sum().item()/max((Y==1).sum().item(),1)])
    lossf=nn.BCEWithLogitsLoss(pos_weight=pw)
    n=len(Y); bs=256
    net.train()
    for ep in range(epochs):
        perm=torch.randperm(n)
        for i in range(0,n,bs):
            b=perm[i:i+bs]
            opt.zero_grad()
            loss=lossf(net(WA[b],W[b],E[b]),Y[b].float())
            loss.backward(); opt.step()
    return net
def score(net,ds):
    W,WA,E,Y=prep(ds)
    net.eval()
    with torch.no_grad():
        return torch.sigmoid(net(WA,W,E)).numpy(),Y.numpy()
if __name__=='__main__':
    mode=sys.argv[1]
    files=sorted(glob.glob('data/*.feat.json'))
    files=[f for f in files if '6AL5' not in f]
    dss={f.split('/')[-1].split('.')[0]:load(f) for f in files}
    ids=sorted(dss)
    from sklearn.metrics import roc_auc_score
    if mode=='loco':
        preds=np.zeros(sum(len(dss[i][3]) for i in ids)); ys=np.zeros_like(preds); o=0
        per={}
        for hid in ids:
            tr=[dss[i] for i in ids if i!=hid]
            net=train_model(tr)
            p,y=score(net,[dss[hid]])
            per[hid]=roc_auc_score(y,p)
            preds[o:o+len(y)]=p; ys[o:o+len(y)]=y; o+=len(y)
        out={'loco_pooled':float(roc_auc_score(ys,preds)),'loco_mean':float(np.mean(list(per.values()))),'per_complex':per}
        json.dump(out,open('results/g1_loco.json','w'),indent=1); print(json.dumps(out,indent=1))
    elif mode=='fixed':
        tr_ids=ids[:13]; te_ids=ids[13:]
        net=train_model([dss[i] for i in tr_ids])
        p,y=score(net,[dss[i] for i in te_ids])
        out={'train':tr_ids,'test':te_ids,'fixed_split_auroc':float(roc_auc_score(y,p))}
        json.dump(out,open('results/g1_fixed.json','w'),indent=1); print(json.dumps(out,indent=1))
    elif mode=='perms':
        a,b=int(sys.argv[2]),int(sys.argv[3])
        tr_ids=ids[:13]; te_ids=ids[13:]
        out={}
        for i in range(a,b):
            tr=[]
            rng=np.random.default_rng(1000+i)
            for cid in tr_ids:
                d,F,ai,y=dss[cid]
                yp=rng.permutation(y)
                tr.append((d,F,ai,yp))
            net=train_model(tr,seed=i)
            p,y=score(net,[dss[i2] for i2 in te_ids])
            out[f'perm_{i}']=float(roc_auc_score(y,p))
        json.dump(out,open(f'/tmp/006c_perms_{a}_{b}.json','w')); print('done',a,b)
    elif mode=='final6al5':
        net=train_model([dss[i] for i in ids])
        torch.save(net.state_dict(),'results/final_model.pt')
        d=json.load(open('data/6AL5.feat.json'))
        F=np.array(d['F'],dtype=np.float32); y=np.array(d['truth'])
        ai=np.array([AAI.get(a2,19) for a2 in d['seq']],dtype=np.int64)
        p,yy=score(net,[(d,F,ai,y)])
        seq=d['seq']; n=len(seq)
        PARKER={'A':2.1,'R':10.0,'N':7.0,'D':2.1,'C':1.4,'E':5.7,'Q':2.1,'G':-5.7,'H':4.2,'I':-8.0,'L':9.2,'K':-4.2,'M':7.1,'F':-2.1,'P':2.1,'S':6.5,'T':5.2,'W':1.9,'Y':-1.9,'V':-8.2}
        bep=np.array([np.mean([PARKER.get(seq[j],0) for j in range(max(0,i-3),min(n,i+4))]) for i in range(n)])
        sasa=F[:,4]
        out={'n':int(n),'epitope':int(y.sum()),
             'dl_auroc':float(roc_auc_score(y,p)),
             'bepipred1_auroc':float(roc_auc_score(y,bep)),
             'sasa_auroc':float(roc_auc_score(y,sasa)),
             'dl_scores':p.tolist(),'res_ids':d['ids']}
        json.dump(out,open('results/g2_6al5.json','w'),indent=1)
        print(json.dumps({k:v for k,v in out.items() if k not in('dl_scores','res_ids')},indent=1))
