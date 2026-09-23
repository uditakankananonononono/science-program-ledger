import torch
torch.set_num_threads(1)
import json,numpy as np,torch,torch.nn as nn
VOC={'A':0,'C':1,'G':2,'T':3,'N':4}
def encode(s,maxlen=256):
    x=np.full(maxlen,4,dtype=np.int64)
    for i,c in enumerate(s[:maxlen]): x[i]=VOC.get(c,4)
    return x
class GPT(nn.Module):
    def __init__(s,d=128,nl=4,nh=4,ctx=256):
        super().__init__()
        s.emb=nn.Embedding(5,d); s.pos=nn.Embedding(ctx,d)
        enc=nn.TransformerEncoderLayer(d,nh,4*d,dropout=0.1,batch_first=True,activation='gelu')
        s.tr=nn.TransformerEncoder(enc,nl)
        s.ctx=ctx; s.head=nn.Linear(d,4)
        s.register_buffer('mask',torch.triu(torch.ones(ctx,ctx),1).bool())
    def forward(s,x):
        from torch.utils.checkpoint import checkpoint
        B,T=x.shape
        h=s.emb(x)+s.pos(torch.arange(T,device=x.device))
        m=s.mask[:T,:T]
        for layer in s.tr.layers:
            if s.training:
                h=checkpoint(lambda h,l=layer,m=m: l(h,src_mask=m),h,use_reentrant=False)
            else:
                h=layer(h,src_mask=m)
        h=s.tr.norm(h) if s.tr.norm is not None else h
        return s.head(h)  # logits for 4 bases (N never predicted)
def batches(path,max_nt=30_000_000,bs=64,ctx=256,seed=20260924):
    rng=np.random.default_rng(seed); rows=[];nt=0
    for line in open(path):
        r=json.loads(line); rows.append(r['seq']); nt+=len(r['seq'])
        if nt>=max_nt: break
    print('train corpus:',len(rows),'transcripts',nt,'nt')
    X=torch.tensor(np.stack([encode(s) for s in rows]))
    while True:
        i=rng.integers(0,len(X),bs)
        yield X[i]
