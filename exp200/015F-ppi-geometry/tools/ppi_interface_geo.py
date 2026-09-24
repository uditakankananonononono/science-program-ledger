#!/usr/bin/env python3
"""ppi_interface_geo.py - DOC-1-015F: per-residue PPI-interface predictor
(ESM-2-8M 320d + PSSM 20d + 4d intra-chain contact-graph geometry, logistic C=1.0).
Usage: python3 ppi_interface_geo.py protein.fasta structure.cif out.tsv
NOTE (locked boundary, 2026-09-24): geometry adds +0.027/+0.059 frozen AUROC over the
015 multimodal arm but MISSES the locked +0.03-on-both-sets bar (dset72 +0.0268) -
documented boundary; geometry alone beats the classical PSSM baseline on both frozen
sets. Treat rankings as hypothesis-generating. See REPORT.md."""
import sys, difflib, pickle, os
import numpy as np

def read1(p):
    for blk in open(p).read().split('\n>'):
        blk = blk.lstrip('>')
        if blk and '\n' in blk:
            h, s = blk.split('\n', 1)
            return h.split()[0], ''.join(c for c in s if c in 'ACDEFGHIKLMNPQRSTVWY')[:512]

def geo_from_cif(cifpath, dseq):
    import gemmi
    from scipy.spatial import cKDTree
    st = gemmi.read_structure(cifpath)
    model = st[0]
    cas = {}
    for chain in model:
        for res in chain:
            ca = res.find_atom('CA', '\0')
            if ca is not None and res.label_seq and res.label_seq > 0:
                cas[int(res.label_seq)] = (ca.pos.x, ca.pos.y, ca.pos.z)
        break
    keys = sorted(cas)
    eseq_len = max(keys) if keys else 0
    doc = gemmi.cif.read_file(cifpath)
    eseq = None
    try:
        for row in doc.sole_block().find('_entity_poly.', ['pdbx_seq_one_letter_code']):
            eseq = str(row[0]).replace('\n', '').replace(';', '').strip(); break
    except Exception:
        eseq = 'X' * eseq_len
    sm = difflib.SequenceMatcher(None, dseq, eseq, autojunk=False)
    amap = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): amap[blk.a + k] = blk.b + k + 1
    xyz = np.array([cas[k] for k in keys])
    n = len(dseq)
    if not len(xyz): return np.zeros((n, 4), np.float32)
    tree = cKDTree(xyz)
    nb = tree.query_ball_tree(tree, 10.0)
    adj = [set(q) - {i} for i, q in enumerate(nb)]
    deg = np.array([len(a) for a in adj], np.float32)
    twohop = np.zeros(len(keys), np.float32)
    for i, q in enumerate(adj):
        s = set(q)
        for j in q: s |= adj[j]
        twohop[i] = len(s - {i})
    mx = deg.max() if deg.max() > 0 else 1.0
    pos_of = {k: i for i, k in enumerate(keys)}
    G = np.zeros((n, 4), np.float32)
    for i in range(n):
        ls = amap.get(i, -1)
        if ls in pos_of:
            p = pos_of[ls]
            G[i] = [deg[p], twohop[p], deg[p] + 1.0, 1.0 - deg[p] / mx]
    return G

def main():
    fasta, cif, out = sys.argv[1], sys.argv[2], sys.argv[3]
    name, seq = read1(fasta)
    import esm, torch
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
    bc = alphabet.get_batch_converter()
    _, _, toks = bc([(name, seq)])
    with torch.no_grad():
        r = model(toks, repr_layers=[6])['representations'][6][0, 1:len(seq)+1].numpy()
    G = geo_from_cif(cif, seq)
    P = np.zeros((len(seq), 20), np.float32)  # flat PSSM in single-sequence mode (as 015 CLI)
    X = np.hstack([r.astype(np.float32), P, G])
    clf = pickle.load(open(os.path.join(os.path.dirname(__file__), '..', 'results', 'models015F.pkl'), 'rb'))['clfE']
    p = 1 / (1 + np.exp(-clf.decision_function(X)))
    thr = np.quantile(p, 0.9)
    with open(out, 'w') as o:
        o.write('residue\tposition\tinterface_probability\ttop_decile\n')
        for i, c in enumerate(seq):
            o.write(f'{c}\t{i+1}\t{p[i]:.4f}\t{int(p[i] >= thr)}\n')
    print('wrote', out)

if __name__ == '__main__': main()
