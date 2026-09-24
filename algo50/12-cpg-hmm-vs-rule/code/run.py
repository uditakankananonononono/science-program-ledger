import gzip, json, hashlib, time
import numpy as np
seq=''.join(l.strip() for l in open('data/chr22_20m-22m.fa') if not l.startswith('>')).upper()
REGION_START=20000001
print('seqlen',len(seq))
isl=[]
with gzip.open('data/cpgIslandExt.txt.gz','rt') as f:
    for line in f:
        p=line.split('\t')
        if p[1]!='chr22': continue
        s,e=int(p[2]),int(p[3])  # 0-based
        # convert to region coords (1-based region start)
        s0=s-REGION_START+1; e0=e-REGION_START+1
        if e0<0 or s0>=len(seq): continue
        isl.append((max(0,s0),min(len(seq),e0)))
print('islands in region',len(isl))
half=len(seq)//2
# dinucleotide index map
B='ACGT'; di={a+b:i for i,(a,b) in enumerate((x+y) for x in B for y in B)}
def dinuc_indices(s):
    out=np.full(len(s)-1,-1,int)
    codes=np.array([B.find(c) for c in s])
    ok=(codes>=0)
    v=codes[:-1]*4+codes[1:]
    okpair=ok[:-1]&ok[1:]
    out[okpair]=v[okpair]
    return out
def train(mask,trseq):
    # mask: boolean array over positions, True = island
    d=dinuc_indices(trseq)
    posmask=mask[:-1]&mask[1:]&(d>=0)
    negmask=(~mask)[:-1]&(~mask)[1:]&(d>=0)
    cp=np.bincount(d[posmask],minlength=16)+1
    cn=np.bincount(d[negmask],minlength=16)+1
    # transitions on train half
    lab=mask.astype(int)
    tr=np.ones((2,2))
    for a in (0,1):
        for b in (0,1):
            tr[a,b]+=np.sum((lab[:-1]==a)&(lab[1:]==b))
    tr/=tr.sum(1,keepdims=True)
    return np.log(cp/cp.sum()),np.log(cn/cn.sum()),np.log(tr)
mask=np.zeros(len(seq),bool)
for s,e in isl: mask[s:e]=True
lp,ln,ltr=train(mask[:half],seq[:half])
# apply to test half
tseq=seq[half:]; d=dinuc_indices(tseq)
emit_p=lp[d]; emit_n=ln[d]
emit_p[d<0]=np.log(0.25); emit_n[d<0]=np.log(0.25)
n=len(d)
# viterbi, 2 states, vectorized
logp=np.zeros((n,2)); ptr=np.zeros((n,2),np.int8)
logp[0]=[emit_n[0],emit_p[0]]  # column 0 = non-island, column 1 = island (matches tr rows)
for i in range(1,n):
    cand=logp[i-1][:,None]+ltr
    ptr[i]=np.argmax(cand,axis=0)
    logp[i]=cand[ptr[i],[0,1]]+[emit_n[i],emit_p[i]]
states=np.zeros(n,int); states[-1]=np.argmax(logp[-1])
for i in range(n-2,-1,-1): states[i]=ptr[i+1][states[i+1]]
print('island fraction decoded',states.mean())
# window eval
W=200; step=100
wins=[]
for s in range(0,len(tseq)-W+1,step):
    a=half+s; b=half+s+W
    lab=mask[a:b].mean()>=0.5
    win_seq=tseq[s:s+W]
    gc=(win_seq.count('G')+win_seq.count('C'))/W
    cpg=win_seq.count('CG'); g=win_seq.count('G'); c=win_seq.count('C')
    oe=(cpg*W)/(g*c) if g*c>0 else 0
    rule=(gc>=0.5) and (oe>=0.6)
    # LLR on window dinucs
    dd=dinuc_indices(win_seq); dd=dd[dd>=0]
    llr=float((lp[dd]-ln[dd]).mean()) if len(dd) else 0.0
    vit=states[max(0,s-1):max(0,s-1)+W-1].mean()>=0.5 if s>0 else False
    wins.append((lab,rule,llr,vit))
y=np.array([w[0] for w in wins])
def f1(pred):
    pred=np.array(pred); tp=np.sum(pred&y)
    p=tp/max(1,pred.sum()); r=tp/max(1,y.sum())
    return 2*p*r/max(1e-9,p+r),p,r
res={}
res['RULE']=f1([w[1] for w in wins])
res['LLR']=f1([w[2]>0 for w in wins])
res['HMM']=f1([w[3] for w in wins])
print(json.dumps(res,indent=1))
# island-level recall (test half)
test_isl=[(max(s,half)-half,min(e,half+len(tseq))-half) for s,e in isl if e>half]
covered=0
for s,e in test_isl:
    if states[s:e].mean()>=0.5: covered+=1
res['island_recall']=covered/max(1,len(test_isl)); print('island recall',res['island_recall'],'of',len(test_isl))
# segment lengths of HMM calls
segs=[]; i=0
while i<len(states):
    if states[i]==1:
        j=i
        while j<len(states) and states[j]==1: j+=1
        segs.append(j-i); i=j
    else: i+=1
res['hmm_seg_median']=float(np.median(segs)) if segs else 0
res['annot_median_len']=float(np.median([e-s for s,e in test_isl])) if test_isl else 0
print('hmm seg median',res['hmm_seg_median'],'annot median',res['annot_median_len'])
json.dump({k:(list(v) if isinstance(v,tuple) else v) for k,v in res.items()},open('results/results.json','w'),indent=1)
print('G1 HMM>=RULE+0.10:',res['HMM'][0],res['RULE'][0])
print('G2 recall>=0.70:',res['island_recall'])
print('G3 LLR>=RULE+0.05:',res['LLR'][0],res['RULE'][0])
with open('data/SHA256_raw.txt','w') as f:
    for fn in ('chr22_20m-22m.fa','cpgIslandExt.txt.gz'):
        f.write(hashlib.sha256(open('data/'+fn,'rb').read()).hexdigest()+'  '+fn+'\n')
open('data/retrieved_at.txt','w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
