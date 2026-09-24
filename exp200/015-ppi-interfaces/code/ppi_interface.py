#!/usr/bin/env python3
"""ppi_interface.py - per-residue PPI interface probabilities for one protein sequence.
Usage: python3 ppi_interface.py seq.fasta
Model: ESM-2 t6_8M residue embeddings + PSSM -> logistic regression (Dset_186, 183 proteins).
Frozen AUROC 0.670 (Dset_72) / 0.631 (Dset_164) - see REPORT.md boundary. PSSM here is a flat
uniform profile when no homolog search is provided (single-sequence mode documented)."""
import sys, os, pickle
import numpy as np, torch, esm
here=os.path.dirname(os.path.abspath(__file__))
def read1(p):
    for blk in open(p).read().split('\n>'):
        blk=blk.lstrip('>')
        if blk and '\n' in blk:
            h,s=blk.split('\n',1)
            return h.split()[0],''.join(c for c in s if c in 'ACDEFGHIKLMNPQRSTVWY')[:512]
def main():
    name,seq=read1(sys.argv[1])
    clf=pickle.load(open(os.path.join(here,'..','results','ppi_model.pkl'),'rb'))['clf']
    model,alphabet=esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
    bc=alphabet.get_batch_converter()
    _,_,toks=bc([(name,seq)])
    with torch.no_grad():
        rep=model(toks,repr_layers=[6])['representations'][6][0,1:len(seq)+1].numpy()
    pssm=np.tile(0.05,(len(seq),20))  # single-sequence mode: flat profile (documented)
    s=clf.predict_proba(np.hstack([rep,pssm]))[:,1]
    print(f'>{name} len={len(seq)}')
    for i,(c,v) in enumerate(zip(seq,s)):
        flag='*' if v>=np.quantile(s,0.9) else ' '
        print(f'{i+1}\t{c}\t{v:.3f}\t{flag}')
if __name__=='__main__': main()
