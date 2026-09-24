import h5py, numpy as np, json
f=h5py.File('results/local/scib_pancreas.h5ad','r')
tcats=[c.decode() for c in f[f['obs/tech'].attrs['categories']][:]]
si=tcats.index('smartseq2')
codes=f['obs/tech'][:]
rows=np.where(codes==si)[0]
ctcats=[c.decode() for c in f[f['obs/celltype'].attrs['categories']][:]]
ct=f['obs/celltype'][:][rows]
y=np.array([ctcats[c] for c in ct])
X=f['X'][rows,:].astype(np.float32)
np.save('results/local/frozen_X.npy', X); np.save('results/local/frozen_y.npy', y)
rng=np.random.default_rng(7)
gm=np.where(y=='gamma')[0]; bg=np.where(y!='gamma')[0]
order=rng.permutation(gm).tolist()
grid={'0.005':order[:11],'0.01':order[:22],'0.02':order[:44],'0.05':order[:115]}
json.dump({'background_count':int(len(bg)),'gamma_total':int(len(gm)),'grid':grid,'seed':7,
           'study':'smartseq2 (Segerstolpe, human)'}, open('results/rarity_grid_frozen.json','w'), indent=1)
print('frozen', X.shape, 'gamma', len(gm), 'bg', len(bg))
