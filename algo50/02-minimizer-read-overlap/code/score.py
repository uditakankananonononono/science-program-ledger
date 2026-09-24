import json, time, itertools
import numpy as np
K=15; W=10; MASK=(1<<(2*K))-1
def parse_reads(path):
    reads={}; name=None; chunks=[]
    for line in open(path):
        if line.startswith('>'):
            if name: reads[name]=''.join(chunks)
            name=line[1:].split()[0]; chunks=[]
        else: chunks.append(line.strip())
    if name: reads[name]=''.join(chunks)
    return reads
def canon_codes(seq):
    # canonical 2-bit codes, skip k-mers with non-ACGT (none expected)
    fwd=0; rev=0; n=len(seq); out=[]
    val={'A':0,'C':1,'G':2,'T':3}
    for i,ch in enumerate(seq):
        v=val[ch]
        fwd=((fwd<<2)|v)&MASK
        rev=(rev>>2)|((3-v)<<(2*(K-1)))
        if i>=K-1: out.append(min(fwd,rev))
    return out
def splitmix64(x):
    x=(x+0x9E3779B97F4A7C15)&0xFFFFFFFFFFFFFFFF
    x=(x^(x>>30))*0xBF58476D1CE4E5B9&0xFFFFFFFFFFFFFFFF
    x=(x^(x>>27))*0x94D049BB133111EB&0xFFFFFFFFFFFFFFFF
    return x^(x>>31)
def minimizers(codes):
    if len(codes)<W: return set(splitmix64(c) for c in codes)
    hs=[splitmix64(c) for c in codes]
    return set(min(hs[i:i+W]) for i in range(len(hs)-W+1))
def pair_scores(sets):
    # inverted index -> shared distinct counts
    inv={}
    for rid,s in enumerate(sets):
        for x in s: inv.setdefault(x,[]).append(rid)
    scores={}
    for rids in inv.values():
        if len(rids)<2: continue
        rids=sorted(set(rids))
        for i in range(len(rids)):
            a=rids[i]
            for b in rids[i+1:]:
                key=(a,b); scores[key]=scores.get(key,0)+1
    return scores
from sklearn.metrics import roc_auc_score, average_precision_score
def auroc_auprc(y,s):
    return roc_auc_score(y,s), average_precision_score(y,s)
def main():
    meta=json.load(open('data/manifest.json'))
    reads=parse_reads('data/reads.fa')
    ids=[m['id'] for m in meta]; n=len(ids)
    assert len(reads)==n
    # ground truth
    starts=np.array([m['start'] for m in meta]); ends=starts+np.array([m['len'] for m in meta])
    truth={}
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    for (i,j) in pairs:
        truth[(i,j)]=1 if min(ends[i],ends[j])-max(starts[i],starts[j])>=1000 else 0
    ntrue=sum(truth.values())
    # featurize
    codes=[canon_codes(reads[r]) for r in ids]
    t0=time.time(); ek=[set(c) for c in codes]; t_ek_feat=time.time()-t0
    t0=time.time(); mn=[minimizers(c) for c in codes]; t_mn_feat=time.time()-t0
    ek_sizes=[len(s) for s in ek]; mn_sizes=[len(s) for s in mn]
    # score
    t0=time.time(); ek_sc=pair_scores(ek); t_ek=time.time()-t0+t_ek_feat
    t0=time.time(); mn_sc=pair_scores(mn); t_mn=time.time()-t0+t_mn_feat
    def evalset(sc, pair_subset=None):
        P=pair_subset or pairs
        y=np.array([truth[p] for p in P]); s=np.array([sc.get(p,0) for p in P],float)
        return y,s
    out={'n_reads':n,'n_pairs':len(pairs),'n_true':ntrue,
         'ek_set_median':float(np.median(ek_sizes)),'mn_set_median':float(np.median(mn_sizes)),
         't_ek':t_ek,'t_mn':t_mn}
    for name,sc in (('EK',ek_sc),('MIN',mn_sc)):
        y,s=evalset(sc)
        au,ap=auroc_auprc(y,s)
        budget=int(0.02*len(pairs))
        top=np.argsort(-s,kind='mergesort')[:budget]
        recall=y[top].sum()/ntrue
        out[name]=dict(auroc=au,auprc=ap,recall_at_2pct=recall)
        # stratum: both eps=0.15
        hi=[m['id'] for m in meta if m['eps']==0.15]
        idx={m['id']:k for k,m in enumerate(meta)}
        hset=set(idx[r] for r in hi)
        hp=[p for p in pairs if p[0] in hset and p[1] in hset]
        y2,s2=evalset(sc,hp)
        nt2=y2.sum()
        b2=int(0.02*len(hp))
        top2=np.argsort(-s2,kind='mergesort')[:b2]
        out[name]['hi_recall_at_2pct']=float(y2[top2].sum()/nt2) if nt2 else None
        out[name]['hi_pairs']=len(hp)
    json.dump(out,open('results/results.json','w'),indent=1)
    print(json.dumps(out,indent=1))
    print('G1 MIN recall@2%% >=0.95:',out['MIN']['recall_at_2pct'])
    print('G2 AUPRC ratio:',out['MIN']['auprc']/out['EK']['auprc'])
    print('G3 time ratio:',out['t_mn']/out['t_ek'])
    print('G4 hi recall@2%%:',out['MIN']['hi_recall_at_2pct'])
main()
