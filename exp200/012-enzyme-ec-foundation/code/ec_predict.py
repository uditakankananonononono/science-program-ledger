#!/usr/bin/env python3
"""ec_predict.py - predict EC top-level class (1-7) from protein sequence.
Usage: python3 ec_predict.py proteins.fasta
Model: ESM-2 t6_8M mean-pooled embedding + logistic regression trained on 3,000 reviewed
pre-2022 UniProt enzymes. Dev macro-F1 0.573; frozen (post-2022) 0.459.
CAVEAT (see REPORT.md boundary): MMseqs2 best-hit EC transfer outperforms this model
(dev 0.789, frozen 0.574, low-identity dev 0.655 vs 0.470). Use sequence search first."""
import sys, os, pickle
import numpy as np, torch, esm
here=os.path.dirname(os.path.abspath(__file__))
def read_fasta(p):
    for blk in open(p).read().split('\n>'):
        blk=blk.lstrip('>')
        if not blk or '\n' not in blk: continue
        h,s=blk.split('\n',1)
        yield h.split()[0], s.replace('\n','')[:512]
def main():
    bundle=pickle.load(open(os.path.join(here,'..','results','ec_model.pkl'),'rb'))
    clf,classes=bundle['clf'],bundle['classes']
    model,alphabet=esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
    bc=alphabet.get_batch_converter()
    recs=list(read_fasta(sys.argv[1]))
    with torch.no_grad():
        for j in range(0,len(recs),16):
            batch=recs[j:j+16]
            _,_,toks=bc([(i,s) for i,s in batch])
            rep=model(toks,repr_layers=[6])['representations'][6]
            E=[]
            for k,(i,s) in enumerate(batch):
                n=min(len(s),512); E.append(rep[k,1:n+1].mean(0).numpy())
            probs=clf.predict_proba(np.stack(E))
            for (i,s),pr in zip(batch,probs):
                top=classes[int(np.argmax(pr))]
                print(f'{i}\tEC_class={top}\tprob={pr.max():.3f}\tall={dict(zip(classes,np.round(pr,3)))}')
if __name__=='__main__': main()
