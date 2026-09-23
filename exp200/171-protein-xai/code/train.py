import sys,re,json,random,numpy as np,torch,torch.nn as nn,torch.nn.functional as F
from sklearn.metrics import f1_score,roc_auc_score
from scipy.stats import wilcoxon
torch.set_num_threads(2);SHUF=len(sys.argv)>1 and sys.argv[1]=='shuffle'
random.seed(0);np.random.seed(0);torch.manual_seed(0)
AA='ACDEFGHIKLMNPQRSTVWY';IDX={a:i for i,a in enumerate(AA)};L=600
rows=[]
for c in range(1,7):
    r=[l.rstrip('\n').split('\t') for l in open(f'data/ec{c}.tsv')][1:]
    ok=[]
    for acc,ec,fam,act,seq in r:
        tops={e.strip().split('.')[0] for e in ec.split(';') if e.strip()}
        if tops!={str(c)}: continue
        sites=[int(m) for m in re.findall(r'ACT_SITE (\d+)(?!\.\.)',act)]
        sites=[s for s in sites if 1<=s<=len(seq)]
        if not sites: continue
        ok.append((acc,c-1,fam or acc,sites,seq))
    random.shuffle(ok);rows+=ok[:1200]
fams=sorted({r[2] for r in rows});random.shuffle(fams)
n=len(fams);split={f:('train' if i<.7*n else 'val' if i<.8*n else 'test') for i,f in enumerate(fams)}
def enc(s):
    x=np.zeros((20,L),np.float32)
    for i,a in enumerate(s[:L]):
        if a in IDX:x[IDX[a],i]=1
    return x
D={k:[r for r in rows if split[r[2]]==k] for k in('train','val','test')}
print({k:len(v) for k,v in D.items()},flush=True)
X={k:torch.tensor(np.stack([enc(r[4]) for r in v])) for k,v in D.items()}
Y={k:torch.tensor([r[1] for r in v]) for k,v in D.items()}
if SHUF: Y['train']=Y['train'][torch.randperm(len(Y['train']))]
class Net(nn.Module):
    def __init__(s):
        super().__init__();s.c1=nn.Conv1d(20,96,9,padding=4)
        s.c2=nn.Conv1d(96,96,5,padding=4,dilation=2);s.c3=nn.Conv1d(96,96,5,padding=8,dilation=4)
        s.fc=nn.Linear(96,6);s.dp=nn.Dropout(0.3)
    def forward(s,x):
        h=F.relu(s.c1(x));h=F.relu(s.c2(h))+h;h=F.relu(s.c3(h))+h
        return s.fc(s.dp(h.max(-1).values))
m=Net();opt=torch.optim.AdamW(m.parameters(),2e-3,weight_decay=1e-4)
best=(-1,None)
for ep in range(12):
    m.train();p=torch.randperm(len(Y['train']))
    for i in range(0,len(p),64):
        b=p[i:i+64];opt.zero_grad();F.cross_entropy(m(X['train'][b]),Y['train'][b]).backward();opt.step()
    m.eval()
    with torch.no_grad(): pv=torch.cat([m(X['val'][i:i+256]) for i in range(0,len(Y['val']),256)]).argmax(1)
    f=f1_score(Y['val'],pv,average='macro');print(ep,round(f,3),flush=True)
    if f>best[0]: best=(f,{k:v.clone() for k,v in m.state_dict().items()})
m.load_state_dict(best[1]);m.eval()
with torch.no_grad(): pt=torch.cat([m(X['test'][i:i+256]) for i in range(0,len(Y['test']),256)]).argmax(1)
f1t=f1_score(Y['test'],pt,average='macro')
g2=[];g3=[];cat=set('HSDCEKRYT')
for j,r in enumerate(D['test']):
    x=X['test'][j:j+1];y=r[1];ln=min(len(r[4]),L)
    al=torch.linspace(1/32,1,32).view(-1,1,1);xs=(al*x).requires_grad_(True)
    out=m(xs)[:,y].sum();g,=torch.autograd.grad(out,xs)
    ig=(x[0]*g.mean(0)).sum(0).abs().numpy()[:ln]
    lab=np.zeros(ln);site=[s-1 for s in r[3] if s<=ln]
    if not site or len(site)==ln: continue
    lab[site]=1;g2.append(roc_auc_score(lab,ig))
    types={r[4][s] for s in site};mask=np.array([a in types for a in r[4][:ln]])
    if mask.sum()>lab[mask].sum()>0: g3.append(roc_auc_score(lab[mask],ig[mask]))
res=dict(shuffled=SHUF,n=({k:len(v) for k,v in D.items()}),val_f1=best[0],test_macroF1=f1t,
 n_g2=len(g2),G2_median_auroc=float(np.median(g2)),n_g3=len(g3),G3_mean_auroc=float(np.mean(g3)),G3_median=float(np.median(g3)),
 G3_wilcoxon_p=float(wilcoxon(np.array(g3)-0.5,alternative='greater').pvalue))
print(json.dumps(res,indent=1));json.dump(res,open(f"results/{'shuffled' if SHUF else 'main'}.json",'w'),indent=1)
if not SHUF: torch.save(best[1],'results/model.pt')
