import numpy as np
MURPHY10={c:i for i,g in enumerate(["LVIM","C","A","G","ST","P","FYW","EDNQ","KR","H"]) for c in g}
PLAIN={c:i for i,c in enumerate("ACDEFGHIKLMNPQRSTVWY")}
M64=np.uint64(0xFFFFFFFFFFFFFFFF)
def mix(x):
    x=x.astype(np.uint64)
    x^=x>>np.uint64(33); x*=np.uint64(0xff51afd7ed558ccd); x^=x>>np.uint64(33)
    x*=np.uint64(0xc4ceb9fe1a85ec53); x^=x>>np.uint64(33); return x
def kmers(seq,alpha,pattern,seedid=0):
    a=np.array([alpha[c] for c in seq],dtype=np.uint64); B=np.uint64(len(set(alpha.values())))
    pos=[i for i,ch in enumerate(pattern) if ch=='1']; L=len(pattern)
    if len(a)<L: return np.zeros(0,np.uint64)
    m=len(a)-L+1; code=np.zeros(m,np.uint64)
    for p in pos: code=code*B+a[p:p+m]
    return np.unique(mix(code+np.uint64(seedid)*np.uint64(1<<40)))
def featset(seq,alpha,patterns):
    return np.unique(np.concatenate([kmers(seq,alpha,p,k) for k,p in enumerate(patterns)]))
def bottom(h,s): return h[:s]  # h already sorted unique
def mash_jaccard(a,b,s):
    u=np.union1d(a,b)[:s]
    inter=np.intersect1d(np.intersect1d(a,b,assume_unique=True),u,assume_unique=True)
    return len(inter)/len(u) if len(u) else 0.0
def exact_jaccard(a,b):
    i=len(np.intersect1d(a,b,assume_unique=True)); return i/(len(a)+len(b)-i)
