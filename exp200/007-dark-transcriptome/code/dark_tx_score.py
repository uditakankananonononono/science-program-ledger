#!/usr/bin/env python3
"""Score FASTA transcripts for dark-transcriptome authenticity (007 frozen char-GPT).
Usage: dark_tx_score.py file.fasta
Prints per-transcript mean log-likelihood and real-vs-shuffle delta (higher = more
transcriptome-like). Validation: frozen NONCODE v6 real-vs-shuffle AUROC 0.908
(beats CPAT-feature baseline 0.739); masked-reconstruction gate G1 failed (+3.1 pts
vs +10 gate) - disclosed. Research use only."""
import sys,json,numpy as np,torch
sys.path.insert(0,'.')
from code.model import GPT,encode
from code.prep import dinuc_shuffle
import torch.nn as nn
net=GPT(); net.load_state_dict(torch.load('results/ckpt.pt',weights_only=True)['model']); net.eval()
lossf=nn.CrossEntropyLoss(reduction='none')
def ll(seqs):
    out=[]
    with torch.no_grad():
        for i in range(0,len(seqs),16):
            x=torch.tensor(np.stack([encode(s) for s in seqs[i:i+16]]))
            inp,tgt=x[:,:-1],x[:,1:]
            lg=net(inp); mask=tgt<4
            l=-lossf(lg.reshape(-1,4),tgt.clamp(max=3).reshape(-1)).reshape(inp.shape)
            out+=((l*mask).sum(1)/mask.sum(1)).tolist()
    return out
name=None;seqs=[];seq=[]
for line in open(sys.argv[1]):
    if line.startswith('>'):
        if name: seqs.append((''.join(seq).upper(),name))
        name=line[1:].strip(); seq=[]
    else: seq.append(line.strip())
if name: seqs.append((''.join(seq).upper(),name))
rng=np.random.default_rng(99)
real=[s for s,_ in seqs]; shuf=[dinuc_shuffle(s,rng) for s,_ in seqs]
lr=ll(real); ls=ll(shuf)
for (s,n),a,b in zip(seqs,lr,ls): print(f'{n}\tll={a:.4f}\tshuffle_ll={b:.4f}\tdelta={a-b:+.4f}')
