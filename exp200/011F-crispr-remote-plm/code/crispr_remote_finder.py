#!/usr/bin/env python3
"""crispr_remote_finder.py - score FASTA sequences for remote CRISPR-Cas effector likelihood
in the sequence-signal-free regime (011F). Max cosine similarity to 011's committed
Cas9/Cas12a/Cas13a seed centroids over ESM-2 t6_8M mean-pooled embeddings (512aa cap).
Frozen temporal validation AUROC 0.821 on post-2023 Cas12f/b/k deposits where MMseqs2 -s 7.5
is at chance (0.487). Use where sequence search has no signal; for alignable families use
MMseqs2 instead (011 boundary).
Usage: python3 crispr_remote_finder.py proteins.fasta"""
import os, sys, json
import numpy as np, torch, esm
def read_fasta(p):
    recs=[]
    for blk in open(p).read().split('>'):
        blk=blk.strip()
        if not blk or '\n' not in blk: continue
        hdr,seq=blk.split('\n',1)
        recs.append((hdr.split('|')[1] if '|' in hdr else hdr.split()[0], seq.replace('\n','')[:512]))
    return recs
if __name__ == '__main__':
    assert len(sys.argv) > 1, 'need a FASTA path'
    here = os.path.dirname(os.path.abspath(__file__))
    cent = json.load(open(os.path.join(here, '..', '..', '011-crispr-plm-discovery', 'results', 'centroids.json')))
    Cn = {k: np.array(v, dtype=np.float32) / (np.linalg.norm(v) + 1e-9) for k, v in cent.items()}
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    model.eval()
    bc = alphabet.get_batch_converter()
    recs = read_fasta(sys.argv[1])
    fams = ['Cas9','Cas12a','Cas13a']
    with torch.no_grad():
        for j in range(0, len(recs), 16):
            batch = recs[j:j+16]
            _,_,toks = bc([(i,s) for i,s in batch])
            r = model(toks, repr_layers=[6])['representations'][6]
            for k,(i,s) in enumerate(batch):
                e = r[k,1:len(s)+1].mean(0).numpy().astype(np.float32)
                e = e / (np.linalg.norm(e) + 1e-9)
                sims = {f: float(e @ Cn[f]) for f in fams}
                best = max(sims, key=sims.get)
                print(f'{i}\tscore={sims[best]:.4f}\tnearest_family={best}\tall={json.dumps({f: round(v,3) for f,v in sims.items()})}')
