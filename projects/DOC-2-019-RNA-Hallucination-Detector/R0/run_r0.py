#!/usr/bin/env python3
"""DOC-2-019 locked R0 pilot. Stdlib + numpy/scipy only."""
import argparse,gzip,hashlib,json,math,random,sys
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

BASES='ACGU'
def clean(s):
 s=s.upper().replace('T','U'); return ''.join(c for c in s if c in BASES)
def parse_stockholm(path,min_len=40,max_len=500,min_family_n=5,cap=8):
 fam=None; d=defaultdict(list)
 with gzip.open(path,'rt',errors='replace') as f:
  for line in f:
   if line.startswith('#=GF AC'): fam=line.split()[2]
   elif fam and line.strip() and not line.startswith('#') and line.strip()!='//':
    z=line.split();
    if len(z)>=2:
     s=clean(z[1])
     if min_len<=len(s)<=max_len: d[fam].append(s)
 # deterministic diversity-neutral cap, deduplicate within family
 out={k:sorted(set(v),key=lambda x:hashlib.sha256(x.encode()).hexdigest())[:cap] for k,v in d.items()}
 return {k:v for k,v in out.items() if len(v)>=min_family_n}
def surrogate(s,rng):
 # Per-sequence first-order Markov generator, same length. Add-0.5 smoothing.
 cnt=np.full((4,4),.5); idx={b:i for i,b in enumerate(BASES)}
 for a,b in zip(s[:-1],s[1:]): cnt[idx[a],idx[b]]+=1
 p=cnt/cnt.sum(1,keepdims=True); comp=np.array([s.count(b) for b in BASES],float)+.5; comp/=comp.sum()
 cur=int(rng.choice(4,p=comp)); out=[BASES[cur]]
 for _ in range(len(s)-1): cur=int(rng.choice(4,p=p[cur])); out.append(BASES[cur])
 return ''.join(out)
KMERS=[ ''.join(p) for k in (2,3,4) for p in __import__('itertools').product(BASES,repeat=k)]
def feat(s):
 v=[]
 for k in (2,3,4):
  c=Counter(s[i:i+k] for i in range(len(s)-k+1)); den=max(1,len(s)-k+1)
  v += [c[x]/den for x in KMERS if len(x)==k]
 # global complexity descriptors
 comp=np.array([s.count(b)/len(s) for b in BASES]); ent=-sum(x*math.log(x+1e-12) for x in comp)/math.log(4)
 runs=[]; r=1
 for a,b in zip(s[:-1],s[1:]):
  if a==b:r+=1
  else:runs.append(r);r=1
 runs.append(r)
 v += [ent,max(runs)/len(s),sum(x>=4 for x in runs)/len(s)]
 return v
def basefeat(s):
 return [math.log(len(s)),(s.count('G')+s.count('C'))/len(s)]
def fit_lr(X,y,l2=1.0):
 X=np.asarray(X,float); y=np.asarray(y,float); mu=X.mean(0); sd=X.std(0); sd[sd<1e-8]=1; Z=(X-mu)/sd
 def fun(w):
  q=Z@w[:-1]+w[-1]; loss=np.logaddexp(0,q).sum()-(y*q).sum()+.5*l2*np.dot(w[:-1],w[:-1]);
  p=1/(1+np.exp(-np.clip(q,-40,40))); g=np.r_[Z.T@(p-y)+l2*w[:-1],(p-y).sum()]; return loss,g
 w=minimize(lambda w:fun(w),np.zeros(Z.shape[1]+1),jac=True,method='L-BFGS-B',options={'maxiter':500}).x
 return lambda A: 1/(1+np.exp(-np.clip(((np.asarray(A)-mu)/sd)@w[:-1]+w[-1],-40,40)))
def auc(y,s):
 y=np.asarray(y); s=np.asarray(s); pos=s[y==1]; neg=s[y==0]
 if not len(pos) or not len(neg): return float('nan')
 return (sum((x>neg).sum()+.5*(x==neg).sum() for x in pos)/(len(pos)*len(neg)))
def family_macro_auc(rows,scores):
 by=defaultdict(list)
 for r,q in zip(rows,scores):by[r['family']].append((r['y'],q))
 vals={k:auc([x[0] for x in v],[x[1] for x in v]) for k,v in by.items()}
 return float(np.nanmean(list(vals.values()))),vals
def split(f): return ['train','validation','test'][int(hashlib.sha256(f.encode()).hexdigest(),16)%10//6 if int(hashlib.sha256(f.encode()).hexdigest(),16)%10<8 else 2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seed',required=True);ap.add_argument('--out',required=True);ap.add_argument('--bootstrap',type=int,default=2000);a=ap.parse_args()
 fams=parse_stockholm(a.seed); rows=[]
 for f,seqs in sorted(fams.items()):
  sp=split(f)
  for j,s in enumerate(seqs):
   rng=np.random.default_rng(int(hashlib.sha256(f'{f}:{j}:DOC-2-019'.encode()).hexdigest()[:16],16)); h=surrogate(s,rng)
   rows += [dict(family=f,split=sp,y=1,seq=s,length=len(s)),dict(family=f,split=sp,y=0,seq=h,length=len(h))]
 counts=Counter(r['split'] for r in rows); fc=Counter((r['split'],r['family']) for r in rows)
 train=[r for r in rows if r['split']=='train']; test=[r for r in rows if r['split']=='test']
 model=fit_lr([feat(r['seq']) for r in train],[r['y'] for r in train]); pred=model([feat(r['seq']) for r in test])
 base=fit_lr([basefeat(r['seq']) for r in train],[r['y'] for r in train]); bpred=base([basefeat(r['seq']) for r in test])
 primary,per=family_macro_auc(test,pred); bauc,_=family_macro_auc(test,bpred)
 tf=sorted(per); rng=np.random.default_rng(2019); boots=[]
 for _ in range(a.bootstrap): boots.append(np.mean([per[x] for x in rng.choice(tf,len(tf),replace=True)]))
 med=np.median([r['length'] for r in test if r['y']==1]); strata={}
 for name,cond in [('short',lambda r:r['length']<=med),('long',lambda r:r['length']>med)]:
  ix=[i for i,r in enumerate(test) if cond(r)]; strata[name]=family_macro_auc([test[i] for i in ix],pred[ix])[0]
 gates={'data_minimum':len(fams)>=100 and len(rows)//2>=1000,'primary_auc':primary>=.75,'bootstrap_lower':bool(np.quantile(boots,.025)>=.70),'negative_control':bauc<=.60,'length_strata':min(strata.values())>=.70}
 result={'protocol_id':'DOC-2-019-R0','seed_sha256':hashlib.sha256(Path(a.seed).read_bytes()).hexdigest(),'eligible_families':len(fams),'authentic_sequences':len(rows)//2,'row_counts':counts,'family_counts':{z:len({r['family'] for r in rows if r['split']==z}) for z in ('train','validation','test')},'test_median_length':med,'primary_family_macro_auc':primary,'family_bootstrap_95_ci':[float(np.quantile(boots,.025)),float(np.quantile(boots,.975))],'length_gc_control_auc':bauc,'stratum_auc':strata,'gates':gates,'all_gates_pass':all(gates.values()),'limitations':['Synthetic class is a controlled first-order Markov surrogate, not output from a named RNA foundation model.','Rfam seed sequences are curated positives; this R0 does not estimate performance on arbitrary genomic background or adversarial generators.','Sequence-only features do not establish structural or functional validity.']}
 Path(a.out).write_text(json.dumps(result,indent=2,default=lambda x:int(x)))
 print(json.dumps(result,indent=2,default=lambda x:int(x)))
if __name__=='__main__':main()
