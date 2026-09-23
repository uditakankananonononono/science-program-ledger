#!/usr/bin/env python3
"""Score antigen-chain residues for antibody-epitope likelihood (006C frozen DL model).
Usage: cart_epitope_score.py file.pdb ANTIGEN_CHAIN AB_CHAINS(e.g. H,L)
006C validation: LOCO-CV pooled 0.827 over 16 complexes; frozen 6AL5 (B43-CD19)
AUROC 0.685 (field range); fixed-split permutation criterion FAILED (disclosed).
Research use only."""
import sys,json,numpy as np,torch
sys.path.insert(0,'.')
from code.featurize_c import featurize
from code.dl import Net,windows,AAI
pdb,ag,ab=sys.argv[1],sys.argv[2],sys.argv[3].split(',')
r=featurize(pdb,ag,ab)
F=np.array(r['F'],dtype=np.float32); ai=np.array([AAI.get(a,19) for a in r['seq']])
net=Net(); net.load_state_dict(torch.load('results/final_model.pt',weights_only=True)); net.eval()
W,WA=windows(F,ai)
with torch.no_grad():
    p=torch.sigmoid(net(torch.tensor(WA),torch.tensor(W[:,:,:7]),torch.tensor(F[:,7:]))).numpy()
for rid,a,sc in zip(r['ids'],r['seq'],p): print(f'{rid}\t{a}\t{sc:.3f}')
