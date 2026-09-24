#!/usr/bin/env python3
"""score_ddpm.py GENE [GENE...] - tiny conditional DDPM per held-out gene (GATES.md arm B). Appends to results/ddpm_scores.json."""
import sys, json, os, numpy as np, torch, torch.nn as nn
from scipy.stats import spearmanr
torch.manual_seed(7); np.random.seed(7)
S=np.load('results/local/spatial.npz',allow_pickle=True)
genes=list(S['genes']); M=S['M'].T.copy()  # cells x 33 (log-normalized)
X=(S['X']-S['X'].mean())/S['X'].std(); Y=(S['Y']-S['Y'].mean())/S['Y'].std()
coord=np.stack([X,Y],1).astype(np.float32)
T=100
beta=torch.linspace(1e-4,0.02,T); alpha=1-beta; abar=torch.cumprod(alpha,0)
class Den(nn.Module):
    def __init__(s,nin):
        super().__init__()
        s.temb=nn.Sequential(nn.Linear(16,64),nn.SiLU())
        s.net=nn.Sequential(nn.Linear(nin+64,256),nn.SiLU(),nn.Linear(256,256),nn.SiLU(),nn.Linear(256,1))
    def forward(s,x,t):
        te= torch.sin(t[:,None]*torch.exp(torch.linspace(0,4,16))[None,:])
        return s.net(torch.cat([x,s.temb(te)],1))
def run(gene):
    gi=genes.index(gene)
    others=[i for i in range(len(genes)) if i!=gi]
    Xc=torch.tensor(np.concatenate([M[:,others],coord],1))
    y=torch.tensor(M[:,gi:gi+1])
    mu,sd=y.mean(),y.std()+1e-6
    yz=(y-mu)/sd
    m=Den(Xc.shape[1]+1)
    opt=torch.optim.Adam(m.parameters(),1e-3)
    n=len(yz)
    for ep in range(3):
        perm=torch.randperm(n)
        for b in range(0,n,256):
            xb=Xc[perm[b:b+256]]; yb=yz[perm[b:b+256]]
            t=torch.randint(0,T,(len(xb),)).float()
            ti=t.long()
            eps=torch.randn_like(yb)
            noised=torch.sqrt(abar[ti])[:,None]*yb+torch.sqrt(1-abar[ti])[:,None]*eps
            pred=m(torch.cat([xb,noised],1),t/T*10)
            loss=((pred-eps)**2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
    # posterior sampling: 16 samples, 50 reverse steps
    torch.set_num_threads(2)
    ns=16; steps=50
    xs=Xc.repeat_interleave(ns,0)
    with torch.no_grad():
        cur=torch.randn(len(xs),1)
        ts=torch.linspace(T-1,0,steps).long()
        for t in ts:
            tb=torch.full((len(xs),),float(t)/T*10)
            eps=m(torch.cat([xs,cur],1),tb)
            a=alpha[t]; ab=abar[t]; ab_prev=abar[t-1] if t>0 else torch.tensor(1.0)
            coef1=1/torch.sqrt(a); coef2=(1-a)/torch.sqrt(1-ab)
            mean=coef1*(cur-coef2*eps)
            var=beta[t]*(1-ab_prev)/(1-ab)
            cur=mean+ (torch.sqrt(var)*torch.randn_like(cur) if t>0 else 0)
    pred=(cur.view(-1,ns).mean(1,keepdim=True))*sd+mu
    rho=float(spearmanr(M[:,gi],pred[:,0].detach().numpy()).statistic)
    return rho
out={}
if os.path.exists('results/ddpm_scores.json'): out=json.load(open('results/ddpm_scores.json'))
for g in sys.argv[1:]:
    if g in out: continue
    rho=run(g); out[g]=rho
    json.dump(out,open('results/ddpm_scores.json','w'),indent=1)
    print(g,round(rho,3),flush=True)
