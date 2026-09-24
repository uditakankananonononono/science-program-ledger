import numpy as np, json, sys
BASE='/home/sandbox/ledger/exp200/022-cross-tissue-embedding/results/local'
OUT='results/local'
which=sys.argv[1]  # 'dev' or 'frozen'
spec={'dev':   dict(half='halfA', seed=11, alpha=2.0),
      'frozen':dict(half='halfB', seed=23, alpha=0.5)}[which]
sp=json.load(open(f'{OUT}/split.json'))
cells=np.array(sp[spec['half']]); KEEP=sp['keep_types']
X=np.load(f'{BASE}/Lung_X.npy', mmap_mode='r')
y=np.load(f'{BASE}/Lung_y.npy', allow_pickle=True)
hv=np.load(f'{OUT}/hvg.npy')
rng=np.random.default_rng(spec['seed'])
N=2000
# GRF via coarse-grid random field + bilinear interp
g=8; grid=rng.standard_normal((g+1,g+1))
coords=rng.random((N,2))
fx,fy=coords[:,0]*g, coords[:,1]*g
ix,iy=fx.astype(int), fy.astype(int); dx,dy=fx-ix, fy-iy
field=(grid[ix,iy]*(1-dx)*(1-dy)+grid[ix+1,iy]*dx*(1-dy)+
       grid[ix,iy+1]*(1-dx)*dy+grid[ix+1,iy+1]*dx*dy)
order=np.argsort(field); bands=np.empty(N,int); bands[order]=np.arange(N)//(N//10)
dominant=bands % len(KEEP)
# mixture: dominant weight 0.45, rest spread over other types
base_prof=np.full((len(KEEP),), 0.55/(len(KEEP)-1)); base_prof[0]=0.45
props=np.zeros((N,len(KEEP)), np.float32)
member_types=np.zeros((N,10), int)-1  # up to 10 cells per spot
ncells=rng.integers(5,11,N)
for i in range(N):
    prof=np.roll(base_prof, dominant[i])
    p=rng.dirichlet(prof*spec['alpha']*20); props[i]=p
    ts=rng.choice(len(KEEP), size=ncells[i], p=p/p.sum())
    member_types[i,:ncells[i]]=ts
# sample cells of each type from the half pool
pools={t: cells[y[cells]==KEEP[t]] for t in range(len(KEEP))}
type_names=np.array(KEEP)
spots=np.zeros((N,len(hv)), np.float32)
# vectorized per type: assign each member occurrence a random cell from pool
counts_sum=np.zeros((N,), np.float32)
for t in range(len(KEEP)):
    rows, cols=np.where(member_types==t)
    if len(rows)==0: continue
    pool=pools[t]
    chosen=pool[rng.integers(0,len(pool),len(rows))]
    block=np.asarray(X[chosen][:,hv], dtype=np.float32)
    np.add.at(spots, rows, block)
# normalize spot to log1p/1e4 for model input; also store raw sums? store log1p-normalized (what arms use)
lib=spots.sum(1, keepdims=True); lib[lib==0]=1
spots_log=np.log1p(spots/lib*1e4)
np.save(f'{OUT}/spots_{which}.npy', spots_log.astype(np.float32))
np.save(f'{OUT}/props_{which}.npy', props)
np.save(f'{OUT}/coords_{which}.npy', coords.astype(np.float32))
print(which, 'spots', spots_log.shape, 'props mean', props.mean(0).round(3))
