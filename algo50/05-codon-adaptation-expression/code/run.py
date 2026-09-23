import gzip,json,re,numpy as np
from Bio import SeqIO
from Bio.Data.CodonTable import standard_dna_table as CT
from scipy.stats import spearmanr
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
rng=np.random.default_rng(0)
fam={}
for c,a in CT.forward_table.items(): fam.setdefault(a,[]).append(c)
SYN={a:cs for a,cs in fam.items() if len(cs)>1}
CODS=sorted(c for cs in SYN.values() for c in cs)  # 59
genes={};names={}
for r in SeqIO.parse(gzip.open('data/yeast_cds.fasta.gz','rt'),'fasta'):
    if 'Verified ORF' not in r.description: continue
    s=str(r.seq).upper()
    if len(s)%3 or not s.startswith('ATG'): continue
    cod=[s[i:i+3] for i in range(0,len(s)-3,3)]
    if len(cod)<100 or any(c in CT.stop_codons for c in cod) or any(set(c)-set('ACGT') for c in cod): continue
    f=r.description.split()
    genes[r.id]=cod; names[r.id]=f[1] if len(f)>1 and not f[1].startswith('SGDID') else r.id
ids=sorted(genes); N=len(ids)
C=np.array([[0]*len(CODS) for _ in ids],float); ix={c:i for i,c in enumerate(CODS)}
for g,i in zip(ids,range(N)):
    for c in genes[g]:
        if c in ix: C[i,ix[c]]+=1
fidx={a:[ix[c] for c in cs] for a,cs in SYN.items()}
def weights(rows):
    tot=C[rows].sum(0)+0.5; w=np.zeros(len(CODS))
    for a,js in fidx.items(): w[js]=tot[js]/tot[js].max()
    return np.log(w)
def cai(lw): return (C@lw)/C.sum(1)
def enc(i):
    F={}
    for a,js in fidx.items():
        n=C[i,js].sum()
        if n>1: p=C[i,js]/n; F[a]=(n*(p**2).sum()-1)/(n-1)
    groups={2:[],3:[],4:[],6:[]}
    for a in F: groups[len(fidx[a])].append(F[a])
    e=2.0  # Met,Trp
    for k,cnt in [(2,9),(3,1),(4,5),(6,3)]:
        v=[x for x in groups[k] if x>0]; e+=cnt/np.mean(v) if v else cnt
    return min(e,61)
gc3=np.array([np.mean([c[2] in 'GC' for c in genes[g]]) for g in ids])
ENC=np.array([enc(i) for i in range(N)])
rp=[i for i,g in enumerate(ids) if re.match(r'RP[LS]\d',names[g])]
caiRP=cai(weights(rp))
ref=list(range(N)); hist=[]
for it in range(20):
    s=cai(weights(ref)); new=list(np.argsort(-s)[:int(0.02*N)])
    hist.append(len(set(new)&set(rp)))
    if set(new)==set(ref): break
    ref=new
scCAI=cai(weights(ref)); ov=len(set(ref)&set(rp))/len(ref)
def load(f):
    d={}
    for l in open('data/'+f):
        if l.startswith('#'): continue
        p=l.split('\t'); v=float(p[2])
        if v>0: d[p[1].split('.',1)[1]]=np.log10(v)
    return d
DS={'Ghaemmaghami':load('4932-Ghaemmaghami_et_al_yeast_data.txt'),'Kulak':load('4932-PXD000270_Kulak_Nat_Methods_2014_S_cerevisiae.txt'),'Mueller':load('4932-PXD014877_Mueller_Nature_2020_Saccharomyces_cerevisiae.txt')}
rel=C/np.maximum(np.concatenate([[C[:,fidx[a]].sum(1)] for a in SYN]).T[:,[list(SYN).index(next(a for a,js in fidx.items() if j in js)) for j in range(len(CODS))]],1)
G=DS['Ghaemmaghami']; gpos=np.array([g in G for g in ids]); gy=np.array([G.get(g,np.nan) for g in ids])
# supervised: gene-level 5-fold CV predictions (train on Ghaemmaghami labels of training-fold genes)
Spred=np.zeros(N)
for tr,te in KFold(5,shuffle=True,random_state=0).split(np.arange(N)):
    t=tr[gpos[tr]]; m=RidgeCV(alphas=np.logspace(-3,3,13)).fit(rel[t],gy[t]); Spred[te]=m.predict(rel[te])
Sfull=RidgeCV(alphas=np.logspace(-3,3,13)).fit(rel[gpos],gy[gpos]).predict(rel)
IDX={'CAI-RP':caiRP,'ENC(neg)':-ENC,'GC3':gc3,'SC-CAI':scCAI,'S(cv)':Spred}
res={'n_genes':N,'n_rp':len(rp),'sc_iterations':len(hist),'sc_ref_size':len(ref),'sc_ref_rp_overlap':ov,'sc_rp_overlap_per_iter':hist,'datasets':{}}
def boot(a,b,y,B=2000):
    n=len(y); out=[]
    for _ in range(B):
        i=rng.integers(0,n,n); out.append(spearmanr(a[i],y[i])[0]-(spearmanr(b[i],y[i])[0] if b is not None else 0))
    return [float(np.percentile(out,2.5)),float(np.percentile(out,97.5))]
for dn,D in DS.items():
    m=np.array([g in D for g in ids]); y=np.array([D[g] for g in ids if g in D]); r={'n':int(m.sum())}
    for k,v in IDX.items(): r[k]=float(spearmanr(v[m],y)[0])
    r['SC-CAI_minus_CAI-RP_CI']=boot(scCAI[m],caiRP[m],y)
    r['S_minus_CAI-RP_CI']=boot(Spred[m],caiRP[m],y)
    if dn!='Ghaemmaghami':
        mm=m&~gpos; yy=np.array([D[g] for g,k in zip(ids,mm) if k]); r['clean_nonG_n']=int(mm.sum())
        r['clean_nonG_S_full']=float(spearmanr(Sfull[mm],yy)[0]); r['clean_nonG_CAI-RP']=float(spearmanr(caiRP[mm],yy)[0])
    res['datasets'][dn]=r
res['sc_ref_genes']=[names[ids[i]] for i in ref]
json.dump(res,open('results/results.json','w'),indent=1)
np.savez('results/indices.npz',ids=np.array(ids),**{k.replace('(','_').replace(')',''):v for k,v in IDX.items()})
print(json.dumps({k:v for k,v in res.items() if k!='sc_ref_genes'},indent=1)); print(res['sc_ref_genes'][:40])
