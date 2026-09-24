import sys, json
import numpy as np, torch, esm
model,alphabet=esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
bc=alphabet.get_batch_converter()
R=8; MASKFRAC=0.15
rng=np.random.RandomState(7); torch.manual_seed(7)
def recs(p):
    out=[]
    for blk in open(p).read().split('\n>'):
        blk=blk.lstrip('>')
        if blk and '\n' in blk:
            h,s=blk.split('\n',1); out.append(s.replace('\n',''))
    return out
def pll_batch(seqs):
    # returns per-seq mean logprob of true tokens at masked positions (per masked residue)
    _,_,toks0=bc([(f's{i}',s) for i,s in enumerate(seqs)])
    scores=np.zeros(len(seqs)); counts=np.zeros(len(seqs))
    with torch.no_grad():
        for r in range(R):
            toks=toks0.clone()
            sel=torch.zeros_like(toks,dtype=torch.bool)
            for i,s in enumerate(seqs):
                L=len(s)
                k=max(1,int(round(MASKFRAC*L)))
                pos=torch.randperm(L,generator=None)[:k]+1
                sel[i,pos]=True; toks[i,pos]=alphabet.mask_idx
            logits=model(toks)['logits']
            lp=torch.log_softmax(logits.float(),dim=-1)
            for i,s in enumerate(seqs):
                pos=sel[i].nonzero().squeeze(1)
                true=toks0[i,pos]
                scores[i]+=lp[i,pos,true].sum().item(); counts[i]+=len(pos)
    return scores/counts
def main():
    sets={n:recs(f'results/{f}') for n,f in [('des','designed.fasta'),('base','baseline.fasta'),('nat','natural.fasta')]}
    out={}
    for name,seqs in sets.items():
        vals=[]
        for j in range(0,len(seqs),16):
            vals+=list(pll_batch(seqs[j:j+16]))
        out[name]=vals
        print(name,'done',len(vals),flush=True)
    json.dump(out,open('results/pll_scores.json','w'))
if __name__=='__main__': main()
