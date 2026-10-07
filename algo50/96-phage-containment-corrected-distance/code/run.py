import numpy as np, subprocess, json, csv, os, hashlib, warnings
from scipy.stats import spearmanr
warnings.filterwarnings('ignore')
MASH='./mash-Linux64-v2.3/mash'
M=list(csv.DictReader(open('manifest.csv'))); acc=sorted(r['accession'] for r in M); fam={r['accession']:r['family_requested'] for r in M}
for r in M: assert hashlib.sha256(open(f"data/{r['accession']}.fasta",'rb').read()).hexdigest()==r['fasta_sha256'],r['accession']
LUT=np.full(256,255,np.uint8)
for i,c in enumerate('ACGT'): LUT[ord(c)]=i
def read(a):
    s=''.join(l.strip() for l in open(f'data/{a}.fasta') if not l.startswith('>')).upper(); return np.frombuffer(s.encode(),np.uint8)
def canon(a,K):
    x=LUT[a]; ok=(x<4); x=np.where(ok,x,0).astype(np.uint64); n=len(x)-K+1
    f=np.zeros(n,np.uint64); r=np.zeros(n,np.uint64); bad=np.zeros(n,bool)
    for i in range(K):
        f=(f<<np.uint64(2))|x[i:i+n]; r=r|((np.uint64(3)-x[i:i+n])<<np.uint64(2*i)); bad|=~ok[i:i+n]
    return np.unique(np.minimum(f,r)[~bad])
def sm(v,seed):
    with np.errstate(over='ignore'):
        z=(v^np.uint64(seed*0x9E3779B97F4A7C15 & 0xFFFFFFFFFFFFFFFF))+np.uint64(0x9E3779B97F4A7C15)
        z=(z^(z>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9); z=(z^(z>>np.uint64(27)))*np.uint64(0x94D049BB133111EB); return z^(z>>np.uint64(31))
def sketch(k,s,seed): return {a:np.sort(sm(KM[a],seed))[:s] for a in acc}
def mashdist(s,sk,K):
    D=np.ones((len(acc),len(acc))); J=np.zeros_like(D); N=len(acc)
    for i in range(N):
        for j in range(i+1,N):
            u=np.union1d(sk[acc[i]],sk[acc[j]])[:s]; sh=np.isin(u,sk[acc[i]])&np.isin(u,sk[acc[j]]); jj=sh.sum()/len(u)
            J[i,j]=J[j,i]=jj; d=1.0 if jj==0 else min(1.0,-np.log(2*jj/(1+jj))/K); D[i,j]=D[j,i]=d
    return D
def ccd(s,sk,K):
    N=len(acc); D=np.ones((N,N)); T=2.0**64
    for i in range(N):
        for j in range(i+1,N):
            a,b=sk[acc[i]],sk[acc[j]]; u=np.union1d(a,b)[:s]; sh=(np.isin(u,a)&np.isin(u,b)).sum()
            if sh==0: continue
            Jj=sh/len(u); U=(s-1)/(float(u[-1])/T); I=Jj*U
            na=(s-1)/(float(a[-1])/T); nb=(s-1)/(float(b[-1])/T); C=min(1.0,I/min(na,nb)); D[i,j]=D[j,i]=1.0 if C<=0 else min(1.0,-np.log(C)/K)
    return D
def acc1nn(D):
    c=0
    for i in range(len(acc)):
        d=D[i].copy(); d[i]=9; j=int(np.argmin(d)); c+=fam[acc[i]]==fam[acc[j]]
    return c/len(acc)
def binary_D(k,s,seed):
    os.makedirs('tmp',exist_ok=True); fa=[f'data/{a}.fasta' for a in acc]
    subprocess.run([MASH,'sketch','-k',str(k),'-s',str(s),'-S',str(seed),'-o','tmp/sk']+fa,check=True,capture_output=True)
    out=subprocess.run([MASH,'dist','tmp/sk.msh','tmp/sk.msh'],check=True,capture_output=True,text=True).stdout.split('\n')
    idx={f'data/{a}.fasta':i for i,a in enumerate(acc)}; D=np.ones((len(acc),)*2)
    for l in out:
        p=l.split('\t')
        if len(p)>=5: D[idx[p[0]],idx[p[1]]]=float(p[2])
    return D
def exactD(K,KMs):
    N=len(acc); D=np.ones((N,N))
    for i in range(N):
        for j in range(i+1,N):
            inter=len(np.intersect1d(KMs[acc[i]],KMs[acc[j]],assume_unique=True)); un=len(KMs[acc[i]])+len(KMs[acc[j]])-inter; jj=inter/un
            D[i,j]=D[j,i]=1.0 if jj==0 else min(1.0,-np.log(2*jj/(1+jj))/K)
    return D
iu=np.triu_indices(len(acc),1)
out={}
for K,S,tag in ((13,100,'primary'),(21,1000,'sensitivity')):
    KM={a:canon(read(a),K) for a in acc}; ex=exactD(K,KM)
    if K==13:
        sk=sketch(1000,1000,0) if False else {a:np.sort(sm(KM[a],0))[:1000] for a in acc}
        Dp=mashdist(1000,sk,13); Db=binary_D(13,1000,0); m=(Dp[iu]<0.3)&(Db[iu]<0.3)
        eq=spearmanr(Dp[iu][m],Db[iu][m])[0]; print('equivalence spearman',eq,m.sum(),flush=True); assert eq>=0.95
    r=[]
    for seed in range(20):
        sk=sketch(None,S,seed) if False else {a:np.sort(sm(KM[a],seed))[:S] for a in acc}
        Db=binary_D(K,S,seed); Dn=ccd(S,sk,K)
        r.append((acc1nn(Db),acc1nn(Dn),spearmanr(Db[iu],ex[iu])[0],spearmanr(Dn[iu],ex[iu])[0]))
    r=np.array(r); d=r[:,1]-r[:,0]; rs=np.random.RandomState(7); bs=[d[rs.randint(0,20,20)].mean() for _ in range(10000)]
    lo,hi=np.percentile(bs,[2.5,97.5]); v='WIN' if d.mean()>=.02 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
    out[tag]=dict(k=K,s=S,acc_mash=r[:,0].mean(),acc_ccd=r[:,1].mean(),diff=d.mean(),ci=[lo,hi],sp_mash=r[:,2].mean(),sp_ccd=r[:,3].mean(),verdict=v if tag=='primary' else 'sensitivity:'+v)
    print(tag,json.dumps(out[tag],default=float),flush=True)
json.dump(out,open('results.json','w'),indent=1,default=float)
