import numpy as np, json, sys
sys.path.insert(0,'code')
from score import hvg_standardize, contrastive_embed, leiden_labels
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
X=np.load('results/local/dev_X.npy'); y=np.load('results/local/dev_y.npy', allow_pickle=True)
genes=np.load('results/local/dev_genes.npy', allow_pickle=True)
g=json.load(open('results/rarity_grid.json'))
bg=np.array([i for i in range(len(y)) if y[i]!='pancreatic PP cell'])
target='pancreatic PP cell'
out={}
for r in ['0.01','0.05']:
    idx=np.array(sorted(bg.tolist()+g['grid'][r]))
    Xs=X[idx].astype(np.float32); yy=y[idx]
    lib=Xs.sum(1,keepdims=True); lib[lib==0]=1
    Xs/=lib; Xs*=1e4; np.log1p(Xs,out=Xs)
    Z=hvg_standardize(Xs)
    P=TruncatedSVD(n_components=50, random_state=7).fit_transform(Z)
    E=contrastive_embed(Z)
    ispp=(yy==target)
    def purity(M):
        nn=NearestNeighbors(n_neighbors=16).fit(M)
        _,I=nn.kneighbors(M)
        return float(ispp[I[ispp,1:]].mean())
    out[r]={'n_pp':int(ispp.sum()),'purity_pca':purity(P),'purity_contrastive':purity(E)}
    # marker: Ppy expression PP vs background (log-norm space)
    gi=[i for i,g2 in enumerate(genes) if g2 in ('Ppy','Sst','Ins1','Gcg')]
    mk={genes[i]:{'pp_mean':float(Xs[ispp,i].mean()),'bg_mean':float(Xs[~ispp,i].mean())} for i in gi}
    out[r]['markers']=mk
# augmentation ablation at r=1% (locked): dropout-only vs noise-only
import torch, os
def embed_custom(Z, use_mask, use_noise, epochs=30, proj=64, bs=128, seed=7):
    torch.manual_seed(seed); np.random.seed(seed)
    enc=torch.nn.Sequential(torch.nn.Linear(Z.shape[1],256), torch.nn.ReLU(), torch.nn.Linear(256,proj))
    opt=torch.optim.Adam(enc.parameters(), lr=1e-3)
    Xt=torch.from_numpy(Z); n=len(Xt)
    def aug(x):
        x=x.clone()
        if use_mask: x=x*(torch.rand_like(x)>0.1).float()
        if use_noise: x=x+0.1*torch.randn_like(x)
        return x
    for ep in range(epochs):
        perm=torch.randperm(n)
        for i in range(0,n,bs):
            xb=Xt[perm[i:i+bs]]
            z1=torch.nn.functional.normalize(enc(aug(xb)),dim=1)
            z2=torch.nn.functional.normalize(enc(aug(xb)),dim=1)
            logits=z1@z2.T/0.5
            lab=torch.arange(len(xb))
            loss=(torch.nn.functional.cross_entropy(logits,lab)+torch.nn.functional.cross_entropy(logits.T,lab))/2
            opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad(): return enc(Xt).numpy().astype(np.float32)
idx=np.array(sorted(bg.tolist()+g['grid']['0.01']))
Xs=X[idx].astype(np.float32); yy=y[idx]
lib=Xs.sum(1,keepdims=True); lib[lib==0]=1
Xs/=lib; Xs*=1e4; np.log1p(Xs,out=Xs)
Z=hvg_standardize(Xs)
abl={}
for name,(m,no) in {'dropout_only':(True,False),'noise_only':(False,True)}.items():
    E=embed_custom(Z,m,no)
    f1,rec,nc=leiden_labels(E, yy, target)
    abl[name]={'f1':f1,'recall':rec,'n_clusters':nc}
out['augmentation_ablation_r0.01']=abl
json.dump(out, open('results/g4_mechanism.json','w'), indent=1)
print(json.dumps(out, indent=1))
