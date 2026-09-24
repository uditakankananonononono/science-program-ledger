import numpy as np, json, sys, torch
sys.path.insert(0,'code')
from common import dev_mean_acc
torch.set_num_threads(2)
split=json.load(open('results/split.json')); dev=split['dev']
Zdev={t: np.load(f'results/local/{t}_Z.npy') for t in dev}
y={t: np.load(f'results/local/{t}_y.npy', allow_pickle=True) for t in dev}
classes=json.load(open('results/class_list.json'))
torch.manual_seed(7)
enc=torch.nn.Sequential(torch.nn.Linear(2000,512), torch.nn.GELU(), torch.nn.Linear(512,128))
dec=torch.nn.Sequential(torch.nn.Linear(128,512), torch.nn.GELU(), torch.nn.Linear(512,2000))
params=list(enc.parameters())+list(dec.parameters())
opt=torch.optim.Adam(params, lr=1e-3)
Xall=torch.from_numpy(np.vstack([Zdev[t] for t in dev]))
n=len(Xall); bs=256
for ep in range(15):
    perm=torch.randperm(n)
    tot=0.
    for i in range(0,n,bs):
        xb=Xall[perm[i:i+bs]]
        loss=torch.nn.functional.mse_loss(dec(enc(xb)), xb)
        opt.zero_grad(); loss.backward(); opt.step()
        tot+=loss.item()*len(xb)
    if ep in (0,7,14): print(f'epoch {ep} mse {tot/n:.4f}', flush=True)
with torch.no_grad():
    Edev={t: enc(torch.from_numpy(Zdev[t])).numpy().astype(np.float32) for t in dev}
acc, per = dev_mean_acc(Edev, y, classes, dev)
json.dump({'mean':acc,'per_tissue':per,'arch':'2000-512-128-512-2000 GELU, Adam1e-3, 15ep, batch-blind'},
          open('results/ae_scores.json','w'), indent=1)
torch.save({'enc':enc.state_dict(),'dec':dec.state_dict()}, 'results/local/ae.pt')
print('AE dev mean', round(acc,4), per)
h=json.load(open('results/baseline_scores.json'))['harmony']['mean']
print('G2 check: AE', round(acc,4), '>= Harmony-0.03 =', round(h-0.03,4), '->', 'PASS' if acc>=h-0.03 else 'FAIL')
