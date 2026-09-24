import numpy as np, json, torch, torch.nn as nn
torch.set_num_threads(2)
L='results/local'
Xtr=torch.tensor(np.load(f'{L}/Xtr.npy')); Ytr=torch.tensor(np.load(f'{L}/Ytr.npy'))
Xte=torch.tensor(np.load(f'{L}/Xte.npy')); Yte=np.load(f'{L}/Yte.npy')
Xfz=torch.tensor(np.load(f'{L}/Xfz.npy')); Yfz=np.load(f'{L}/Yfz.npy')
sd=torch.load(f'{L}/fm_encoder.pt')
enc=nn.Sequential(nn.Linear(2000,256), nn.ReLU()); enc.load_state_dict({k[4:]:v for k,v in sd.items() if k.startswith('enc.')})
head=nn.Linear(256,14)
torch.manual_seed(9)
opt=torch.optim.Adam(list(enc.parameters())+list(head.parameters()), lr=5e-4)
N=Xtr.shape[0]
best=1e9; best_state=None; pat=0
perm0=torch.arange(N)
for ep in range(40):
    enc.train(); head.train(); opt.zero_grad()
    pred=head(enc(Xtr))
    loss=((pred-Ytr)**2).mean()
    loss.backward(); opt.step()
    if loss.item()<best-1e-5: best=loss.item(); best_state=({k:v.clone() for k,v in enc.state_dict().items()},{k:v.clone() for k,v in head.state_dict().items()}); pat=0
    else:
        pat+=1
        if pat>=8: break
enc.load_state_dict(best_state[0]); head.load_state_dict(best_state[1])
enc.eval(); head.eval()
with torch.no_grad():
    Pte=head(enc(Xte)).numpy(); Pfz=head(enc(Xfz)).numpy()
def score(P, Y):
    rs=[float(np.corrcoef(P[:,i],Y[:,i])[0,1]) for i in range(Y.shape[1])]
    return {'per_protein_r':[round(r,4) for r in rs], 'mean_r':round(float(np.mean(rs)),4)}
res={'epochs':ep+1,'final_train_mse':round(float(best),4),'dev_test':score(Pte,Yte),'frozen':score(Pfz,Yfz)}
json.dump(res, open('results/p1_scores.json','w'), indent=1)
print(json.dumps(res))
