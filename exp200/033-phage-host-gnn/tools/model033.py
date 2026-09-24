import numpy as np, json, torch, torch.nn as nn, scipy.sparse as sp, sys, time
torch.manual_seed(0); np.random.seed(0)

ids = json.load(open('virus_ids.json'))
vpos = {v:i for i,v in enumerate(ids)}
Xk = np.load('X_kmer.npy')
cand = json.load(open('candidates.json'))
vocab = json.load(open('tax_vocab.json'))
man = json.load(open('manifest033.json'))
NV, NP = len(ids), len(cand)
N = NV + NP
ranks = ['phylum','class','order','family','genus']
offs, pv = {}, []
o = 0
for r in ranks:
    offs[r] = o; o += len(vocab[r])
TAXDIM = o
# prokaryote rank-index matrix (NP x 5)
Pidx = np.zeros((NP, 5), dtype=np.int64)
for i,c in enumerate(cand):
    for k,r in enumerate(ranks):
        Pidx[i,k] = offs[r] + vocab[r][c['tax'][k+1]]

import os
P1 = os.environ.get('P1') == '1'
CE = np.load('crispr_edges.npy') if P1 else np.zeros((0,2), dtype=np.int64)

def build_adj(vp_rows):
    VV = np.load('vv_edges.npy'); PP = np.load('pp_edges.npy')
    rows = np.concatenate([VV[:,0], PP[:,0]+NV, vp_rows[:,0], vp_rows[:,1]+NV, CE[:,0], CE[:,1]+NV])
    cols = np.concatenate([VV[:,1], PP[:,1]+NV, vp_rows[:,1]+NV, vp_rows[:,0], CE[:,1]+NV, CE[:,0]])
    A = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(N,N))
    A = A + sp.eye(N)
    deg = np.asarray(A.sum(1)).ravel()
    dinv = 1.0/np.sqrt(deg); D = sp.diags(dinv)
    An = (D @ A @ D).tocoo()
    ti = torch.tensor(np.vstack([An.row, An.col]), dtype=torch.long)
    tv = torch.tensor(An.data, dtype=torch.float32)
    return torch.sparse_coo_tensor(ti, tv, (N,N)).coalesce()

VP = np.load('vp_edges.npy')
phage_of_pair = [vpos[p['phage'].split('.')[0]] for p in man['train_pairs']]
pair_edge_idx = {}
for k,(v,c) in enumerate(VP):
    pair_edge_idx.setdefault(v, []).append(k)

class GCN(nn.Module):
    def __init__(self, use_graph=True, hid=64):
        super().__init__()
        self.use_graph = use_graph
        self.emb = nn.Embedding(TAXDIM, 16)
        self.wv = nn.Linear(256, hid)
        self.wp = nn.Linear(5*16, hid)
        self.g1 = nn.Linear(hid, hid); self.g2 = nn.Linear(hid, hid)
        self.dec = nn.Sequential(nn.Linear(hid, 64), nn.ReLU(), nn.Linear(64,1))
    def encode(self, A):
        zv = torch.relu(self.wv(Xk_t))
        zp = torch.relu(self.wp(self.emb(Pidx_t).reshape(NP, -1)))
        z = torch.cat([zv, zp], 0)
        if self.use_graph:
            h = torch.relu(self.g1(torch.sparse.mm(A, z)))
            h = self.g2(torch.sparse.mm(A, h))
        else:
            h = self.g2(self.g1(z))
        return z if False else h
    def score(self, h, v, p):
        return self.dec(h[v] * h[p+NV]).squeeze(-1)

def train_model(vp_rows, negs, epochs=40, use_graph=True, lr=0.01, batch=150000):
    A = build_adj(vp_rows)
    m = GCN(use_graph)
    opt = torch.optim.Adam(m.parameters(), lr=lr)
    lossf = nn.BCEWithLogitsLoss()
    rng = np.random.default_rng(0)
    npos = len(vp_rows)
    for ep in range(epochs):
        m.train(); opt.zero_grad()
        h = m.encode(A)
        selp = rng.integers(0, npos, min(batch, npos))
        pv = torch.tensor(vp_rows[selp,0]); pp = torch.tensor(vp_rows[selp,1])
        nv = torch.tensor(vp_rows[selp,0])
        np_ = torch.tensor(rng.integers(0, NP, len(selp)))
        pl = m.score(h, pv, pp); nl = m.score(h, nv, np_)
        loss = lossf(pl, torch.ones_like(pl)) + lossf(nl, torch.zeros_like(nl))
        loss.backward(); opt.step()
    return m, A

def accuracy(m, A, phage_list, true_species, true_genus, cand_species, cand_genus, chunk=20000):
    m.eval()
    with torch.no_grad():
        h = m.encode(A)
        correct_s = correct_g = 0
        for vi, ts, tg in zip(phage_list, true_species, true_genus):
            scores = torch.empty(NP)
            for s in range(0, NP, chunk):
                e = min(NP, s+chunk)
                scores[s:e] = m.score(h, torch.full((e-s,), vi), torch.arange(s, e))
            top = int(scores.argmax())
            if cand_species[top] == ts: correct_s += 1
            if cand_genus[top] == tg: correct_g += 1
    return correct_s/len(phage_list), correct_g/len(phage_list)

Xk_t = torch.tensor(Xk)
Pidx_t = torch.tensor(Pidx)
cand_species = [c['tax'][6] for c in cand]
cand_genus = [c['tax'][5] for c in cand]

def make_negs(vp_rows, n):
    rng = np.random.default_rng(0)
    return np.stack([np.repeat(vp_rows[:,0], 1), rng.integers(0, NP, len(vp_rows))],1)

mode = sys.argv[1] if len(sys.argv)>1 else 'lib'
if mode == 'dev':
    pairs = man['train_pairs']
    uniq = sorted(set(p['phage'] for p in pairs))
    rng = np.random.default_rng(0); order = rng.permutation(len(uniq))
    folds = np.array_split(order, 10)
    f0, f1 = int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv)>3 else (0,10)
    res = {'graph': [], 'nograph': []}
    for fi, f in enumerate(folds):
        if fi < f0 or fi >= f1: continue
        held = set(uniq[i] for i in f)
        held_v = [vpos[p['phage'].split('.')[0]] for p in pairs if p['phage'] in held]
        held_ts = [p['host_species'] for p in pairs if p['phage'] in held]
        held_tg = [p['host_genus'] for p in pairs if p['phage'] in held]
        drop_e = set()
        for p in pairs:
            if p['phage'] in held:
                drop_e.update(pair_edge_idx[vpos[p['phage'].split('.')[0]]])
        keep = np.array([k for k in range(len(VP)) if k not in drop_e])
        vp_tr = VP[keep]
        negs = make_negs(vp_tr, len(vp_tr))
        for tag, ug in [('graph', True), ('nograph', False)]:
            m, A = train_model(vp_tr, negs, epochs=40, use_graph=ug)
            acc = accuracy(m, A, held_v, held_ts, held_tg, cand_species, cand_genus)
            res[tag].append(acc)
            print("fold", fi, tag, acc, flush=True)
            open('dev033_p1_progress.jsonl' if P1 else 'dev033_progress.jsonl','a').write(json.dumps({'fold': fi, 'tag': tag, 'acc': acc})+'\n')
    json.dump(res, open('dev033_p1.json' if P1 else 'dev033.json','w'))
    g = np.array(res['graph']); ng = np.array(res['nograph'])
    print("DEV graph species %.3f genus %.3f | nograph species %.3f genus %.3f" % (g[:,0].mean(), g[:,1].mean(), ng[:,0].mean(), ng[:,1].mean()))
elif mode == 'frozen':
    arm = sys.argv[2] if len(sys.argv)>2 else 'both'
    negs = make_negs(VP, len(VP))
    te = man['test_pairs']
    tv = [vpos[p['phage'].split('.')[0]] for p in te]
    ts = [p['host_species'] for p in te]; tg = [p['host_genus'] for p in te]
    out = {}
    if arm in ('graph','both'):
        m, A = train_model(VP, negs, epochs=40, use_graph=True)
        acc = accuracy(m, A, tv, ts, tg, cand_species, cand_genus)
        print("FROZEN graph species %.4f genus %.4f" % acc, flush=True)
        out['graph'] = acc
        torch.save(m.state_dict(), 'model033_p1_graph.pt' if P1 else 'model033_graph.pt')
        json.dump(out, open('frozen033_p1_graph.json' if P1 else 'frozen033_graph.json','w'))
    if arm in ('nograph','both'):
        m2, A2 = train_model(VP, negs, epochs=40, use_graph=False)
        acc2 = accuracy(m2, A2, tv, ts, tg, cand_species, cand_genus)
        print("FROZEN nograph species %.4f genus %.4f" % acc2, flush=True)
        json.dump({'nograph': acc2}, open('frozen033_p1_nograph.json' if P1 else 'frozen033_nograph.json','w'))
