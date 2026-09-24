import numpy as np, json, torch, torch.nn as nn
torch.set_num_threads(2)
L='results/local'
Xtr=torch.tensor(np.load(f'{L}/Xtr.npy')); Ytr=np.load(f'{L}/Ytr.npy')
Xte=torch.tensor(np.load(f'{L}/Xte.npy')); Yte=np.load(f'{L}/Yte.npy')
Xfz=torch.tensor(np.load(f'{L}/Xfz.npy')); Yfz=np.load(f'{L}/Yfz.npy')
torch.manual_seed(7)
enc=nn.Sequential(nn.Linear(2000,256), nn.ReLU())
dec=nn.Sequential(nn.Linear(256,256), nn.ReLU(), nn.Linear(256,2000))
model=nn.ModuleDict({'enc':enc,'dec':dec})
opt=torch.optim.Adam(model.parameters(), lr=1e-3)
N=Xtr.shape[0]
for ep in range(40):
    model.train(); opt.zero_grad()
    mask=(torch.rand(N,2000)>0.25).float()
    xin=Xtr*mask
    z=enc(xin); rec=dec(z)
    loss=(((rec-Xtr)*(1-mask))**2).sum(1).mean()  # reconstruct masked entries
    loss.backward(); opt.step()
model.eval()
with torch.no_grad():
    Ztr=enc(Xtr).numpy(); Zte=enc(Xte).numpy(); Zfz=enc(Xfz).numpy()
np.save(f'{L}/Ztr.npy', Ztr); np.save(f'{L}/Zte.npy', Zte); np.save(f'{L}/Zfz.npy', Zfz)
torch.save(model.state_dict(), f'{L}/fm_encoder.pt')
from sklearn.linear_model import Ridge
probe=Ridge(alpha=1.0).fit(Ztr, Ytr)
def score(Z, Y):
    P=probe.predict(Z)
    rs=[float(np.corrcoef(P[:,i],Y[:,i])[0,1]) for i in range(Y.shape[1])]
    return {'per_protein_r':[round(r,4) for r in rs], 'mean_r':round(float(np.mean(rs)),4)}
res={'pretrain_final_loss':round(float(loss.item()),4),'dev_test':score(Zte,Yte),'frozen':score(Zfz,Yfz)}
json.dump(res, open('results/fm_scores.json','w'), indent=1)
print(json.dumps(res))
