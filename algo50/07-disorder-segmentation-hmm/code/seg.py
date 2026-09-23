import numpy as np, numba
@numba.njit(cache=True)
def segment(e, L, pen):
    # e: emission score for disorder state (order state = 0). Returns 0/1 labels.
    n=len(e); S=np.zeros((2,n+1))
    for i in range(n): S[1,i+1]=S[1,i]+e[i]
    V=np.full((2,n),-1e18); B=np.full((2,n),-2,np.int64)  # B=-1 continue, -3 prefix start, j>=0 new segment started at j
    for i in range(n):
        for s in range(2):
            best=S[s,i+1]; arg=-3   # whole prefix in state s
            if i>0 and V[s,i-1]+(e[i] if s==1 else 0.0)>best: best=V[s,i-1]+(e[i] if s==1 else 0.0); arg=-1
            j=i-L+1
            if j>=1:
                c=V[1-s,j-1]-pen+S[s,i+1]-S[s,j]
                if c>best: best=c; arg=j
            V[s,i]=best; B[s,i]=arg
    # terminal: allow short final segment
    bestv=-1e18; bs=0; bj=-1
    for s in range(2):
        if V[s,n-1]>bestv: bestv=V[s,n-1]; bs=s; bj=-1
        for j in range(max(1,n-L+1),n):
            c=V[1-s,j-1]-pen+S[s,n]-S[s,j]
            if c>bestv: bestv=c; bs=s; bj=j
    lab=np.zeros(n,np.int8); i=n-1; s=bs
    if bj>=0:
        lab[bj:]=s; i=bj-1; s=1-s
    while i>=0:
        a=B[s,i]
        if a==-1: lab[i]=s; i-=1
        elif a==-3: lab[:i+1]=s; break
        else: lab[a:i+1]=s; i=a-1; s=1-s
    return lab
def regions(y):
    d=np.diff(np.concatenate([[0],y.astype(int),[0]])); return list(zip(np.where(d==1)[0],np.where(d==-1)[0]))
def region_counts(yt,yp):
    T=regions(yt); P=regions(yp); used=set(); tp=0
    for a,b in P:
        for k,(c,d) in enumerate(T):
            if k in used: continue
            ov=min(b,d)-max(a,c)
            if ov>0 and ov>=0.5*min(b-a,d-c): used.add(k); tp+=1; break
    return tp,len(P),len(T)
