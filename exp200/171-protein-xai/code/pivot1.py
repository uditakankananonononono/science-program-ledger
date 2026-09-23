import re,json,random,numpy as np,torch,torch.nn as nn,torch.nn.functional as F,urllib.request,urllib.parse,os,sys
from sklearn.metrics import roc_auc_score,average_precision_score
from scipy.stats import wilcoxon
from transformers import AutoTokenizer,AutoModelForMaskedLM
torch.set_num_threads(2);random.seed(0);np.random.seed(0);torch.manual_seed(0)
AA='ACDEFGHIKLMNPQRSTVWY'
# ---- M-CSA external
R=json.load(open('data/mcsa_residues.json'));mc={}
for r in R:
    roles={x['function_type'] for x in r.get('roles',[])}
    for s in r['residue_sequences']:
        if s.get('is_reference') and s.get('uniprot_id') and s.get('resid'):
            mc.setdefault(s['uniprot_id'],{})[int(s['resid'])]=(s['code'],'reactant' in roles)
accs=sorted(mc);print('mcsa accs',len(accs),flush=True)
if not os.path.exists('data/mcsa_uniprot.tsv'):
    out=['Entry\tProtein families\tSequence']
    for i in range(0,len(accs),100):
        q=urllib.parse.quote(' OR '.join('accession:'+a for a in accs[i:i+100]))
        t=urllib.request.urlopen(f'https://rest.uniprot.org/uniprotkb/stream?format=tsv&fields=accession,protein_families,sequence&query={q}',timeout=60).read().decode().split('\n')
        out+= [l for l in t[1:] if l]
    open('data/mcsa_uniprot.tsv','w').write('\n'.join(out))
three={'Ala':'A','Arg':'R','Asn':'N','Asp':'D','Cys':'C','Gln':'Q','Glu':'E','Gly':'G','His':'H','Ile':'I','Leu':'L','Lys':'K','Met':'M','Phe':'F','Pro':'P','Ser':'S','Thr':'T','Trp':'W','Tyr':'Y','Val':'V'}
ext=[];mfam=set()
for l in open('data/mcsa_uniprot.tsv').read().split('\n')[1:]:
    a,fam,seq=l.split('\t');mfam|={fam} if fam else set()
    if not 50<=len(seq)<=1000 or a not in mc: continue
    s=mc[a];ok=all(1<=p<=len(seq) and three.get(c)==seq[p-1] for p,(c,_) in s.items())
    if ok and s: ext.append((a,seq,s))
print('external proteins',len(ext),flush=True)
# ---- training set
mset=set(mc);rows=[]
for c in range(1,7):
    for l in open(f'data/ec{c}.tsv').read().split('\n')[1:]:
        if not l: continue
        acc,ec,fam,act,seq=l.split('\t')
        if acc in mset or (fam and fam in mfam): continue
        sites=[int(m) for m in re.findall(r'ACT_SITE (\d+)(?!\.\.)',act)];sites=[x for x in sites if 1<=x<=len(seq)]
        if sites: rows.append((acc,fam or acc,sites,seq))
fams=sorted({r[1] for r in rows});random.shuffle(fams);vf=set(fams[:len(fams)//8])
random.shuffle(rows);rows=rows[:3000]
print('train pool',len(rows),flush=True)
tok=AutoTokenizer.from_pretrained('facebook/esm2_t6_8M_UR50D');lm=AutoModelForMaskedLM.from_pretrained('facebook/esm2_t6_8M_UR50D').eval()
def emb(seq):
    seq=seq[:1000];x=tok(seq,return_tensors='pt')
    with torch.no_grad(): o=lm(**x,output_hidden_states=True)
    h=o.hidden_states[-1][0,1:-1];lp=o.logits[0,1:-1].log_softmax(-1)
    ids=torch.tensor(tok.convert_tokens_to_ids(list(seq)));wt=lp[torch.arange(len(seq)),ids]
    return h.numpy().astype(np.float32),(-wt).numpy()
Xtr=[];Ytr=[];G=[];B1tr=[];B1y=[]
for k,(acc,fam,sites,seq) in enumerate(rows):
    h,b1=emb(seq);L=len(seq[:1000]);lab=np.zeros(L);lab[[s-1 for s in sites if s<=L]]=1
    neg=np.where(lab==0)[0];neg=np.random.choice(neg,min(40,len(neg)),replace=False);idx=np.concatenate([np.where(lab==1)[0],neg])
    Xtr.append(h[idx]);Ytr.append(lab[idx]);G+=[fam in vf]*len(idx);B1tr.append(b1[idx]);B1y.append(lab[idx])
    if k%500==0: print('emb',k,flush=True)
X=torch.tensor(np.concatenate(Xtr));Y=torch.tensor(np.concatenate(Ytr)).float();V=torch.tensor(G)
b1s=np.concatenate(B1tr);b1y=np.concatenate(B1y);sgn=1 if roc_auc_score(b1y,b1s)>=0.5 else -1
seqs_tr=''.join(r[3][:1000] for r in rows)
# B2 propensity from training labels
cnt={a:[0,0] for a in AA}
for acc,fam,sites,seq in rows:
    ss=set(sites)
    for i,a in enumerate(seq[:1000]):
        if a in cnt: cnt[a][0]+=1;cnt[a][1]+=(i+1) in ss
prop={a:(v[1]+.5)/(v[0]+1) for a,v in cnt.items()}
net=nn.Sequential(nn.Linear(320,128),nn.ReLU(),nn.Dropout(.2),nn.Linear(128,1));opt=torch.optim.AdamW(net.parameters(),1e-3,weight_decay=1e-3)
tr=torch.where(~V)[0];va=torch.where(V)[0];pw=torch.tensor((Y[tr]==0).sum()/(Y[tr]==1).sum());best=(-1,None)
for ep in range(30):
    net.train();p=tr[torch.randperm(len(tr))]
    for i in range(0,len(p),256):
        b=p[i:i+256];opt.zero_grad();F.binary_cross_entropy_with_logits(net(X[b]).squeeze(-1),Y[b],pos_weight=pw).backward();opt.step()
    net.eval()
    with torch.no_grad(): ap=average_precision_score(Y[va],net(X[va]).squeeze(-1))
    if ap>best[0]: best=(ap,{k:v.clone() for k,v in net.state_dict().items()})
net.load_state_dict(best[1]);net.eval();torch.save(best[1],'results/pivot1_head.pt');json.dump({'prop':prop,'b1_sign':sgn},open('results/pivot1_baselines.json','w'))
print('val AP',best[0],'b1 sign',sgn,flush=True)
# ---- external
P=[];cat=set('HDECKRSYTNQ');out=[]
for a,seq,s in ext:
    h,b1=emb(seq);L=len(seq)
    with torch.no_grad(): m=net(torch.tensor(h)).squeeze(-1).numpy()
    lab=np.zeros(L);lab[[p-1 for p in s]]=1;react=np.zeros(L);react[[p-1 for p,(c,r) in s.items() if r]]=1
    P.append(dict(a=a,lab=lab,react=react,m=m,b1=sgn*b1,b2=np.array([prop.get(x,0) for x in seq]),seq=seq))
print('scored ext',flush=True)
def pooled(key,ids): return average_precision_score(np.concatenate([P[i]['lab'] for i in ids]),np.concatenate([P[i][key] for i in ids]))
ids=list(range(len(P)));ap={k:pooled(k,ids) for k in('m','b1','b2')};bb='b1' if ap['b1']>=ap['b2'] else 'b2'
rng=np.random.default_rng(0);diffs=[]
for _ in range(1000):
    s=rng.integers(0,len(P),len(P));diffs.append(pooled('m',s)-pooled(bb,s))
au=[roc_auc_score(p['lab'],p['m']) for p in P if 0<p['lab'].sum()<len(p['lab'])]
g2=[]
for p in P:
    types={p['seq'][i] for i in np.where(p['lab']==1)[0]};mk=np.array([x in types for x in p['seq']])
    if mk.sum()>p['lab'][mk].sum()>0: g2.append(roc_auc_score(p['lab'][mk],p['m'][mk]))
rec={'reactant':[0,0],'spectator':[0,0]}
for p in P:
    top=set(np.argsort(-p['m'])[:5])
    for i in np.where(p['lab']==1)[0]:
        k='reactant' if p['react'][i] else 'spectator';rec[k][0]+=1;rec[k][1]+=i in top
res=dict(n_ext=len(P),n_ext_sites=int(sum(p['lab'].sum() for p in P)),val_AP=best[0],AUPRC_model=ap['m'],AUPRC_B1_wtmarginal=ap['b1'],AUPRC_B2_propensity=ap['b2'],best_baseline=bb,
 diff=ap['m']-ap[bb],diff_CI=[float(np.percentile(diffs,2.5)),float(np.percentile(diffs,97.5))],median_protein_AUROC=float(np.median(au)),
 G2_mean=float(np.mean(g2)),G2_n=len(g2),G2_p=float(wilcoxon(np.array(g2)-.5,alternative='greater').pvalue),
 top5_recall={k:(v[1]/v[0] if v[0] else None,v[0]) for k,v in rec.items()})
res['P1_G1']=bool(res['diff']>=0.05 and res['diff_CI'][0]>0 and res['median_protein_AUROC']>=0.85);res['P1_G2']=bool(res['G2_mean']>=0.70 and res['G2_p']<0.01)
print(json.dumps(res,indent=1));json.dump(res,open('results/pivot1.json','w'),indent=1)
