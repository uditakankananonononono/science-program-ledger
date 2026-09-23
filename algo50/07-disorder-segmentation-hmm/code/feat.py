import numpy as np
AA="ACDEFGHIKLMNPQRSTVWY"; I={a:i for i,a in enumerate(AA)}
TOP=dict(W=-0.884,F=-0.697,Y=-0.510,I=-0.486,M=-0.397,L=-0.326,V=-0.121,N=0.007,C=0.02,T=0.059,A=0.06,G=0.166,R=0.180,D=0.192,H=0.303,Q=0.318,S=0.341,K=0.586,E=0.736,P=0.987)
KD=dict(A=1.8,R=-4.5,N=-3.5,D=-3.5,C=2.5,Q=-3.5,E=-3.5,G=-0.4,H=-3.2,I=4.5,L=3.8,K=-3.9,M=1.9,F=2.8,P=-1.6,S=-0.8,T=-0.7,W=-0.9,Y=-1.3,V=4.2)
def wmean(v,w):
    n=len(v); h=w//2; c=np.concatenate([[0],np.cumsum(v)]); i=np.arange(n); lo=np.maximum(0,i-h); hi=np.minimum(n,i+h+1)
    return (c[hi]-c[lo])/(hi-lo)
def entropy(s,w=12):
    x=np.array([I[a] for a in s]); n=len(x); oh=np.zeros((n,20)); oh[np.arange(n),x]=1
    c=np.vstack([np.zeros(20),np.cumsum(oh,0)]); i=np.arange(n); lo=np.maximum(0,i-w//2); hi=np.minimum(n,i+w//2+1)
    p=(c[hi]-c[lo])/(hi-lo)[:,None]; p=np.where(p>0,p,1); return -(((c[hi]-c[lo])/(hi-lo)[:,None])*np.log2(p)).sum(1)
def foldindex(s):
    h=np.array([(KD[a]+4.5)/9 for a in s]); q=np.array([(a in 'KR')-(a in 'DE') for a in s],float)
    return -(2.785*wmean(h,51)-np.abs(wmean(q,51))-1.151)
def topidp(s): return wmean(np.array([TOP[a] for a in s]),21)
def feats(s):
    t=np.array([TOP[a] for a in s]); h=np.array([(KD[a]+4.5)/9 for a in s]); q=np.array([(a in 'KR')-(a in 'DE') for a in s],float)
    ch=np.array([a in 'KRDE' for a in s],float); p=np.array([a=='P' for a in s],float); gs=np.array([a in 'GS' for a in s],float)
    F=[]
    for w in (11,31,61): F+=[wmean(t,w),wmean(h,w),np.abs(wmean(q,w)),wmean(p,w),wmean(gs,w),wmean(ch,w)]
    n=len(s); i=np.arange(n); F+=[entropy(s),np.log1p(np.minimum(i,n-1-i))]
    return np.vstack(F).T
