#!/usr/bin/env python3
"""crispr_finder.py - score FASTA sequences for CRISPR-Cas effector likelihood.
Usage: python3 crispr_finder.py proteins.fasta
Output: per-sequence max cosine similarity to Cas9/Cas12a/Cas13a seed centroids + nearest family.
Model: ESM-2 t6_8M mean-pooled. Frozen cross-temporal validation AUROC 0.981 (post-2022 deposits);
dev AUROC 0.923. Caveat: MMseqs2 sequence search outperforms this PLM score on the same pools
(dev 0.989, frozen 0.995) - see REPORT.md boundary analysis."""
import sys, os, json
import numpy as np, torch, esm
here=os.path.dirname(os.path.abspath(__file__))
def read_fasta(p):
    for blk in open(p).read().split('>'):
        if not blk: continue
        h,s=blk.split('\n',1)
        yield h.split()[0], s.replace('\n','')[:512]
def main():
    cent=json.load(open(os.path.join(here,'..','results','centroids.json')))
    model,alphabet=esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
    bc=alphabet.get_batch_converter()
    recs=list(read_fasta(sys.argv[1]))
    with torch.no_grad():
        for j in range(0,len(recs),16):
            batch=recs[j:j+16]
            _,_,toks=bc([(i,s) for i,s in batch])
            rep=model(toks,repr_layers=[6])['representations'][6]
            for k,(i,s) in enumerate(batch):
                n=min(len(s),512)
                e=rep[k,1:n+1].mean(0).numpy()
                sims={f:float(e@np.array(c)/(np.linalg.norm(e)*np.linalg.norm(c))) for f,c in cent.items()}
                best=max(sims,key=sims.get)
                print(f'{i}\tscore={sims[best]:.4f}\tnearest_family={best}\tall={json.dumps({k:round(v,3) for k,v in sims.items()})}')
if __name__=='__main__': main()
