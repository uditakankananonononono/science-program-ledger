import numpy as np, json
from sklearn.metrics import roc_auc_score, roc_curve
rng=np.random.default_rng(1)
BASEP=np.array([0.275,0.225,0.225,0.275])  # A C G T, GC 0.45
CONS='CACGTGCA'; cons_idx=np.array([1,0,1,2,3,2,1,0])
MP=np.array([0.62,0.80,0.95,0.98,0.98,0.95,0.80,0.62])
def make(scale=1.0):
    mp=np.minimum(MP*scale,1.0)
    seqs=rng.choice(4,(400,500),p=BASEP)
    y=np.array([1]*200+[0]*200)
    for i in range(200):
        inst=np.zeros(8,int)
        for p in range(8):
            if rng.random()<mp[p]: inst[p]=cons_idx[p]
            else: inst[p]=rng.choice([b for b in range(4) if b!=cons_idx[p]])
        s=rng.integers(0,493)
        seqs[i,s:s+8]=inst
    return seqs,y
def scores(seqs):
    n=len(seqs)
    # build all 8-mers as codes
    codes=np.zeros((n,493),dtype=np.int64)
    v=np.zeros(n,dtype=np.int64)
    for i in range(500):
        v=((v<<2)|seqs[:,i])&0xFFFF
        if i>=7: codes[:,i-7]=v
    # consensus match count
    conscode=0
    for b in cons_idx: conscode=(conscode<<2)|b
    match=(codes==conscode)
    # mismatch counts: decode per position
    dec=(codes[:,:,None]>>np.array([2*(7-p) for p in range(8)]))&3  # n x 493 x 8
    mism=(dec!=cons_idx[None,None,:]).sum(2)  # n x 493
    cons_best=(8-mism).max(1)
    # PWM log-odds
    pwm=np.full((8,4),np.log(( (1-MP)[:,None]/3 +1e-4)))
    for p in range(8): pwm[p,cons_idx[p]]=np.log(MP[p]+1e-4)
    pwm-=np.log(BASEP)[None,:]
    lo=np.take_along_axis(pwm[None,None,:,:].repeat(1,0), dec[...,None], axis=3).squeeze(-1).sum(2)
    pwm_best=lo.max(1)
    return cons_best,pwm_best
def tpr_at_fpr(y,s,fpr=0.01):
    f,t,_=roc_curve(y,s)
    return float(np.interp(fpr,f,t))
out={}
for name,scale in (('standard',1.0),('weak',0.85)):
    seqs,y=make(scale)
    cs,ps=scores(seqs)
    out[name]=dict(CONS_AUROC=float(roc_auc_score(y,cs)),PWM_AUROC=float(roc_auc_score(y,ps)),
                   CONS_TPR1=tpr_at_fpr(y,cs),PWM_TPR1=tpr_at_fpr(y,ps))
    print(name,out[name],flush=True)
json.dump(out,open('results/results.json','w'),indent=1)
s,w=out['standard'],out['weak']
print('G1',s['PWM_AUROC']>=s['CONS_AUROC']+0.03)
print('G2',s['PWM_TPR1']>=s['CONS_TPR1']+0.10)
print('G3',w['PWM_AUROC']>=w['CONS_AUROC']+0.05)
print('G4',s['PWM_AUROC']>=0.85)
