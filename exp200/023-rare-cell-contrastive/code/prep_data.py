import pandas as pd, numpy as np, json
ann=pd.read_csv('../022-cross-tissue-embedding/results/local/annotations_FACS.csv')
ann=ann[ann['tissue']=='Pancreas']
ann=ann[ann['cell_ontology_class'].notna() & (ann['cell_ontology_class']!='')].set_index('cell')
hdr=pd.read_csv('results/local/pancreas_facs.csv', nrows=0).columns.tolist()
cells=[c for c in hdr[1:] if c in ann.index]
labs=ann.loc[cells,'cell_ontology_class'].values
keep={'Unnamed: 0'}|set(cells)
dt={c:np.float32 for c in cells}
chunks=[]
for ch in pd.read_csv('results/local/pancreas_facs.csv', index_col=0, usecols=lambda c:c in keep, dtype=dt, chunksize=3000):
    chunks.append(ch)
df=pd.concat(chunks); df=df[~df.index.duplicated()]
X=df[cells].values.T.astype(np.float32)
genes=np.array(df.index)
np.save('results/local/dev_X.npy', X); np.save('results/local/dev_y.npy', labs); np.save('results/local/dev_genes.npy', genes)
print('dev', X.shape)
# rarity grid: PP cells nested subsets
rng=np.random.default_rng(7)
pp=np.where(labs=='pancreatic PP cell')[0]
bg=np.where(labs!='pancreatic PP cell')[0]
order=rng.permutation(pp)
grid={str(r): sorted(order[:n].tolist()) for r,n in [('0.005',6),('0.01',12),('0.02',25),('0.05',64)]}
# nested: sort subsets by prefix
order2=order.tolist()
grid={'0.005':order2[:6],'0.01':order2[:12],'0.02':order2[:25],'0.05':order2[:64]}
json.dump({'background_count':len(bg),'pp_total':len(pp),'grid':grid,'seed':7}, open('results/rarity_grid.json','w'), indent=1)
print('grid nested sizes', {k:len(v) for k,v in grid.items()}, 'bg', len(bg), 'pp', len(pp))
