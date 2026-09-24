import sys, json, random
import numpy as np, torch, esm
AA='ACDEFGHIKLMNPQRSTVWY'
model,alphabet=esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
bc=alphabet.get_batch_converter()
toks_aa=[alphabet.get_idx(a) for a in AA]
mask_id=alphabet.mask_idx
lens=json.load(open('data/apd_lengths.json'))
import os; SEED=123+int(os.environ.get("SEEDOFF","0")); rng=random.Random(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
N=int(sys.argv[1]); START=int(sys.argv[2]) if len(sys.argv)>2 else 0
def top_p_sample(logits, p=0.95, temp=1.0):
    logits=logits/temp
    v,ix=torch.sort(logits,descending=True)
    probs=torch.softmax(v,dim=-1)
    cum=torch.cumsum(probs,dim=-1)
    keep=cum<=p; keep[...,0]=True
    v=v*keep + (-1e9)*(~keep)
    pr=torch.softmax(v,dim=-1)
    return ix.gather(-1,torch.multinomial(pr,1))
out=open('results/candidates.fasta','a')
made=0; idx=START
while made<N:
    batch_lens=[rng.choice(lens) for _ in range(16)]
    L=max(batch_lens)
    toks=torch.full((16,L+2),mask_id,dtype=torch.long)
    toks[:,0]=alphabet.cls_idx
    for i,l in enumerate(batch_lens): toks[i,l+1]=alphabet.eos_idx
    fixed=torch.zeros_like(toks,dtype=torch.bool); fixed[:,0]=True
    for i,l in enumerate(batch_lens): fixed[i,l+1]=True
    with torch.no_grad():
        for r in range(12):
            logits=model(toks)['logits'][:,:,torch.tensor(toks_aa)]
            remaining=(~fixed)
            n_unmask=max(1,int(np.ceil(remaining.sum().item()/(12-r))))
            cand=remaining.nonzero()
            pick=cand[torch.randperm(len(cand))[:n_unmask]]
            new=toks.clone()
            for b,p in pick:
                new[b,p]=toks_aa[top_p_sample(logits[b,p],0.95,1.0).item()]
            toks=new; fixed[pick[:,0],pick[:,1]]=True
    for i,l in enumerate(batch_lens):
        seq=''.join(alphabet.get_tok(t) for t in toks[i,1:l+1].tolist())
        seq=''.join(c for c in seq if c in AA)
        if 12<=len(seq)<=50:
            out.write(f'>cand{idx}\n{seq}\n'); idx+=1; made+=1
            if made>=N: break
out.close()
print('generated',made,'total now',idx)
