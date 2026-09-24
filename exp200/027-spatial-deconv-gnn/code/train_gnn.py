import numpy as np, json, sys, torch
import torch.nn as nn
torch.set_num_threads(2)
OUT='results/local'
mode=sys.argv[1] if len(sys.argv)>1 else 'gnn'  # 'gnn' or 'mlp'
k=int(sys.argv[2]) if len(sys.argv)>2 else 6
HID=int(sys.argv[3]) if len(sys.argv)>3 else 128
tag=sys.argv[4] if len(sys.argv)>4 else mode
S=np.load(f'{OUT}/spots_dev.npy'); P=np.load(f'{OUT}/props_dev.npy'); C=np.load(f'{OUT}/coords_dev.npy')
N=len(S)
# kNN k=6 graph
from scipy.spatial import cKDTree
dist,idx=cKDTree(C).query(C, k+1)
src=np.repeat(np.arange(N), k); dst=idx[:,1:].ravel()
# symmetric normalized adjacency with self loops
import scipy.sparse as sp
A=sp.coo_matrix((np.ones(len(src)),(src,dst)), shape=(N,N))
A=((A+A.T)>0).astype(np.float32)+sp.eye(N)
D=np.asarray(A.sum(1)).ravel()**-0.5
A=sp.coo_matrix(A); A.data*=D[A.row]*D[A.col]
At=torch.tensor(np.stack([A.row, A.col])).long(); Av=torch.tensor(A.data.astype(np.float32))
X=torch.tensor(S); Y=torch.tensor(P).clamp_min(1e-8); Y=Y/Y.sum(1,keepdim=True)
perm=torch.randperm(N, generator=torch.Generator().manual_seed(5))
tr, va=perm[:1600], perm[1600:]
def agg(x): return torch.sparse.mm(torch.sparse_coo_tensor(At, Av, (N,N)), x)
class Net(nn.Module):
    def __init__(s, gnn):
        super().__init__(); s.gnn=gnn
        s.l1=nn.Linear(2000,HID); s.l2=nn.Linear(HID,10); s.d=nn.Dropout(0.1)
    def forward(s,x):
        h = agg(x) if s.gnn else x
        h=torch.relu(s.l1(h)); h=s.d(h)
        if s.gnn: h=agg(h)
        return s.l2(h)
net=Net(mode=='gnn'); opt=torch.optim.Adam(net.parameters(), lr=1e-3)
best=1e9; best_state=None; patience=0
for ep in range(60):
    net.train(); opt.zero_grad()
    logits=net(X)[tr]
    loss=-(Y[tr]*torch.log_softmax(logits,1)).sum(1).mean()
    loss.backward(); opt.step()
    net.eval()
    with torch.no_grad():
        vlog=net(X)[va]
        vloss=-(Y[va]*torch.log_softmax(vlog,1)).sum(1).mean().item()
    if vloss<best-1e-4: best=vloss; best_state={k:v.clone() for k,v in net.state_dict().items()}; patience=0
    else:
        patience+=1
        if patience>=8: break
net.load_state_dict(best_state); net.eval()
res={'mode':mode,'k':k,'hidden':HID,'epochs':ep+1,'best_val':round(best,5)}
with torch.no_grad():
    for which in ['dev','frozen']:
        Sw=np.load(f'{OUT}/spots_{which}.npy'); Pw=np.load(f'{OUT}/props_{which}.npy')
        if which=='dev': logits=net(X)
        else:
            Cw=np.load(f'{OUT}/coords_frozen.npy')
            _,iw=cKDTree(Cw).query(Cw, k+1)
            srcw=np.repeat(np.arange(len(Sw)), k); dstw=iw[:,1:].ravel()
            Aw=sp.coo_matrix((np.ones(len(srcw)),(srcw,dstw)), shape=(len(Sw),)*2)
            Aw=((Aw+Aw.T)>0).astype(np.float32)+sp.eye(len(Sw))
            Dw=np.asarray(Aw.sum(1)).ravel()**-0.5
            Aw=sp.coo_matrix(Aw); Aw.data*=Dw[Aw.row]*Dw[Aw.col]
            old=(At,Av,N)
            Nw=len(Sw)
            Atw=torch.tensor(np.stack([Aw.row, Aw.col])).long(); Avw=torch.tensor(Aw.data.astype(np.float32))
            def agg_w(x): return torch.sparse.mm(torch.sparse_coo_tensor(Atw, Avw, (Nw,Nw)), x)
            # forward with swapped aggregator
            def fwd(x):
                h = agg_w(x) if net.gnn else x
                h=torch.relu(net.l1(h))
                if net.gnn: h=agg_w(h)
                return net.l2(h)
            logits=fwd(torch.tensor(Sw))
        pr=torch.softmax(logits,1).numpy()
        rs=[float(np.corrcoef(pr[:,t],Pw[:,t])[0,1]) if pr[:,t].std()>1e-8 and Pw[:,t].std()>1e-8 else float('nan') for t in range(10)]
        res[which]={'per_type_r':[round(r,4) for r in rs], 'mean_r':round(float(np.nanmean(rs)),4)}
        np.save(f'{OUT}/{tag}_pred_{which}.npy', pr)
json.dump(res, open(f'results/{tag}_scores.json','w'), indent=1)
print(json.dumps(res))
