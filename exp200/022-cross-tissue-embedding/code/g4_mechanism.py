import numpy as np, json, sys, torch, collections
sys.path.insert(0,'code')
from common import dev_mean_acc
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import silhouette_score
torch.set_num_threads(2)
split=json.load(open('results/split.json')); dev=split['dev']; fz=split['frozen'][0]
classes=json.load(open('results/class_list.json'))
ck=torch.load('results/local/ae.pt')
enc=torch.nn.Sequential(torch.nn.Linear(2000,512), torch.nn.GELU(), torch.nn.Linear(512,128))
enc.load_state_dict(ck['enc']); enc.eval()
Z={t: np.load(f'results/local/{t}_Z.npy') for t in dev+[fz]}
y={t: np.load(f'results/local/{t}_y.npy', allow_pickle=True) for t in dev+[fz]}
with torch.no_grad():
    E={t: enc(torch.from_numpy(Z[t])).numpy().astype(np.float32) for t in dev+[fz]}
# per-class accuracy, dev held-out + frozen
perclass={}
for held in dev+[fz]:
    tr=[t for t in dev if t!=held] if held in dev else dev
    Xtr=np.vstack([E[t] for t in tr]); ytr=np.concatenate([y[t] for t in tr])
    m=np.isin(ytr,classes); Xtr,ytr=Xtr[m],ytr[m]
    cnt=collections.Counter(ytr.tolist()); ok={k for k,v in cnt.items() if v>=30}
    m2=np.array([l in ok for l in ytr]); Xtr,ytr=Xtr[m2],ytr[m2]
    Xte=E[held]; yte=y[held]
    m3=np.isin(yte,classes)&np.array([l in ok for l in yte]); Xte,yte=Xte[m3],yte[m3]
    knn=KNeighborsClassifier(5,metric='cosine').fit(Xtr,ytr)
    pred=knn.predict(Xte)
    for c in classes:
        mm=yte==c
        if mm.sum()>0:
            perclass.setdefault(c,[]).append((held,float((pred[mm]==c).mean()),int(mm.sum())))
summary={c:{'mean_acc':round(float(np.mean([a for _,a,_ in v])),3),
            'by_tissue':{h:round(a,3) for h,a,_ in v}} for c,v in perclass.items()}
# silhouette: by cell type vs by tissue on dev subsample (AE latent)
rng=np.random.default_rng(7)
Xs=[]; labs=[]; tiss=[]
for t in dev:
    ii=rng.choice(len(E[t]), min(1300,len(E[t])), replace=False)
    Xs.append(E[t][ii]); labs.append(y[t][ii]); tiss += [t]*len(ii)
Xs=np.vstack(Xs); labs=np.concatenate(labs); tiss=np.array(tiss)
m=np.isin(labs,classes)
sil_type=float(silhouette_score(Xs[m], labs[m], metric='cosine'))
sil_tissue=float(silhouette_score(Xs[m], tiss[m], metric='cosine'))
# marker loadings: encoder W1 rows for literature markers
genes=np.load('results/local/genes.npy', allow_pickle=True)
hv=np.load('results/local/dev_fit.npz')['hv']
hvg_names=genes[hv]
markers={'Ptprc(CD45,immune)':'Ptprc','Pecam1(CD31,endothelial)':'Pecam1','Epcam(epithelial)':'Epcam',
         'Col1a1(fibroblast)':'Col1a1','Cd79a(B cell)':'Cd79a','Cd3d(T cell)':'Cd3d'}
W=enc[0].weight.detach().numpy()  # 512 x 2000
loads={}
for lab,g in markers.items():
    if g in hvg_names:
        j=list(hvg_names).index(g)
        loads[lab]={'in_hvg':True,'W1_abs_mean':round(float(np.abs(W[:,j]).mean()),4),
                    'rank_pct':round(float((np.abs(W).mean(0)<np.abs(W[:,j]).mean()).mean()),3)}
    else:
        loads[lab]={'in_hvg':False}
out={'per_class':summary,'silhouette':{'by_cell_type':round(sil_type,4),'by_tissue':round(sil_tissue,4)},
     'marker_W1_loadings':loads}
json.dump(out, open('results/g4_mechanism.json','w'), indent=1)
print(json.dumps(out, indent=1))
