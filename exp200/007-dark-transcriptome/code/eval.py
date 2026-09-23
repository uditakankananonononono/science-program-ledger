import torch; torch.set_num_threads(1)
import sys,json,numpy as np,torch.nn as nn
sys.path.insert(0,'code')
from model import GPT,encode
net=GPT(); net.load_state_dict(torch.load('results/ckpt.pt',weights_only=True)['model']); net.eval()
lossf=nn.CrossEntropyLoss(reduction='none')
def score_seqs(seqs,bs=32):
    out=[]
    with torch.no_grad():
        for i in range(0,len(seqs),bs):
            x=torch.tensor(np.stack([encode(s) for s in seqs[i:i+bs]]))
            inp,tgt=x[:,:-1],x[:,1:]
            logits=net(inp); mask=tgt<4
            ll=-lossf(logits.reshape(-1,4),tgt.clamp(max=3).reshape(-1)).reshape(inp.shape)
            ll=(ll*mask).sum(1)/mask.sum(1)
            out+=ll.tolist()
    return np.array(out)
def masked_acc(seqs,frac=0.15,seed=7,bs=32):
    rng=np.random.default_rng(seed); correct=[];total=[]
    with torch.no_grad():
        for i in range(0,len(seqs),bs):
            X=np.stack([encode(s) for s in seqs[i:i+bs]])
            for j in range(len(X)):
                m=rng.random(256)<frac
                m &= X[j]<4
                if m.sum()<5: continue
                xm=X[j].copy(); xm[m]=4
                x=torch.tensor(xm[None]); logits=net(x[:,:])
                pred=logits[0].argmax(-1).numpy()
                tm=(X[j]<4)&m
                correct.append((pred[tm]==X[j][tm]).sum()); total.append(tm.sum())
    return sum(correct)/sum(total)
mode=sys.argv[1]
if mode=='g1':
    rows=[json.loads(l) for l in open('/tmp/007_dev_eval.jsonl')]
    rng=np.random.default_rng(0); idx=rng.permutation(len(rows))[:300]
    real=[rows[i]['seq'] for i in idx]; shuf=[rows[i]['shuf'] for i in idx]
    a_real=masked_acc(real); a_shuf=masked_acc(shuf,seed=8)
    # paired permutation on per-transcript mean-loglik diff
    l_real=score_seqs(real); l_shuf=score_seqs(shuf)
    d=l_real-l_shuf; obs=d.mean()
    cnt=0
    for _ in range(1000):
        signs=rng.choice([-1,1],len(d))
        if (d*signs).mean()>=obs: cnt+=1
    out={'masked_acc_real':a_real,'masked_acc_shuf':a_shuf,'diff_points':(a_real-a_shuf)*100,
         'mean_ll_real':float(l_real.mean()),'mean_ll_shuf':float(l_shuf.mean()),
         'paired_perm_p':(cnt+1)/1001,'n_pairs':len(d)}
    json.dump(out,open('results/g1.json','w'),indent=1); print(json.dumps(out,indent=1))
if mode=='g2':
    rows=[json.loads(l) for l in open('/tmp/007_noncode.jsonl')]
    rng=np.random.default_rng(1); idx=rng.permutation(len(rows))[:500]
    real=[rows[i]['seq'] for i in idx]; shuf=[rows[i]['shuf'] for i in idx]
    l_real=score_seqs(real); l_shuf=score_seqs(shuf)
    from sklearn.metrics import roc_auc_score
    y=np.r_[np.ones(len(l_real)),np.zeros(len(l_shuf))]
    s=np.r_[l_real,l_shuf]
    auc=roc_auc_score(y,s)
    out={'n_pairs':len(real),'gen_loglik_auroc':float(auc)}
    json.dump(out,open('results/g2_gen.json','w'),indent=1); print(json.dumps(out,indent=1))
if mode=='g2base':
    # CPAT-feature logistic (Wang 2013): ORF len, ORF coverage, Fickett, hexamer bias
    import math
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    COMP={'A':'T','C':'G','G':'C','T':'A','N':'N'}
    STOP={'TAA','TAG','TGA'}
    def orf_stats(s):
        best=0;cov=0
        for fr in range(3):
            i=fr;cur=0
            while i+3<=len(s):
                c=s[i:i+3]
                if c in STOP:
                    best=max(best,cur);cur=0
                else: cur+=3
                i+=3
            best=max(best,cur)
        cov=best/max(len(s),1)
        return best,cov
    def fickett(s):
        # Fickett TESTCODE: position preference * composition, simplified published form
        s=s.replace('N','')
        if len(s)<12: return 0.0
        vals=[]
        for b in 'ACGT':
            pos=[0,0,0]; cnt=s.count(b)
            for i,ch in enumerate(s):
                if ch==b: pos[i%3]+=1
            mx,mn=max(pos),min(pos)
            vals.append((mx/(mn+1))* (cnt/len(s)))
        return sum(vals)
    def hexmer_bias(s,hex_tab):
        sc=0;n=0
        for fr in range(3):
            for i in range(fr,len(s)-5,3):
                hx=s[i:i+6]
                if 'N' in hx: continue
                sc+=hex_tab.get(hx,0); n+=1
        return sc/max(n,1)
    # build hexamer table from train split (coding vs lnc), CPAT method: log ratio
    from collections import Counter
    def hexcount(path,cls,cap=4000):
        c=Counter(); seen=0
        for line in open(path):
            r=json.loads(line)
            if r['cls']!=cls: continue
            seen+=1
            if seen>cap: break
            sq=r['seq']
            for fr in range(3):
                for i in range(fr,len(sq)-5,3):
                    hx=sq[i:i+6]
                    if 'N' not in hx: c[hx]+=1
        return c
    cc=hexcount('/tmp/007_train.jsonl','pc'); cl=hexcount('/tmp/007_train.jsonl','lnc')
    hex_tab={}
    for hx in set(cc)|set(cl):
        hex_tab[hx]=round(np.log((cc[hx]+1)/(cl[hx]+1)),4)
    def feats(s):
        ol,cov=orf_stats(s); return [ol,cov,fickett(s),hexmer_bias(s,hex_tab)]
    dev=[json.loads(l) for l in open('/tmp/007_dev_eval.jsonl')]
    rng=np.random.default_rng(0); didx=rng.permutation(len(dev))[:800]
    Xtr=np.array([feats(dev[i]['seq']) for i in didx]+[feats(dev[i]['shuf']) for i in didx])
    ytr=np.r_[np.ones(800),np.zeros(800)]
    clf=LogisticRegression(max_iter=1000).fit(Xtr,ytr)
    rows=[json.loads(l) for l in open('/tmp/007_noncode.jsonl')]
    nidx=rng.permutation(len(rows))[:800]
    Xte=np.array([feats(rows[i]['seq']) for i in nidx]+[feats(rows[i]['shuf']) for i in nidx])
    yte=np.r_[np.ones(800),np.zeros(800)]
    auc_cpat=roc_auc_score(yte,clf.predict_proba(Xte)[:,1])
    g2=json.load(open('results/g2_gen.json'))
    out={'cpat_feature_auroc':float(auc_cpat),'gen_loglik_auroc':g2['gen_loglik_auroc'],
         'gen_minus_cpat':g2['gen_loglik_auroc']-float(auc_cpat)}
    json.dump(out,open('results/g2_baseline.json','w'),indent=1); print(json.dumps(out,indent=1))
if mode=='g3':
    rows=[json.loads(l) for l in open('/tmp/007_dev_eval.jsonl')]
    pc=[r['seq'] for r in rows if r['cls']=='pc'][:60]
    lnc=[r['seq'] for r in rows if r['cls']=='lnc'][:60]
    def posloss(seqs):
        out=[]
        with torch.no_grad():
            for i in range(0,len(seqs),32):
                x=torch.tensor(np.stack([encode(s) for s in seqs[i:i+32]]))
                inp,tgt=x[:,:-1],x[:,1:]
                logits=net(inp); mask=tgt<4
                ll=-lossf(logits.reshape(-1,4),tgt.clamp(max=3).reshape(-1)).reshape(inp.shape)
                ll=(ll*mask).sum(0)/mask.sum(0).clamp(min=1)
                out.append(ll.numpy())
        return np.mean(np.stack(out),0)
    lp=posloss(pc); ll_=posloss(lnc)
    def lag_profile(v):
        v=v-v.mean()
        return [float(np.corrcoef(v[:-k],v[k:])[0,1]) for k in (1,2,3,4,5,6)]
    out={'pc_lag1to6':lag_profile(lp),'lnc_lag1to6':lag_profile(ll_)}
    json.dump(out,open('results/g3.json','w'),indent=1); print(json.dumps(out,indent=1))
