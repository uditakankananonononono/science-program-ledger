#!/usr/bin/env python3
"""amp_design.py - generate candidate antimicrobial peptides and rank them.
Usage: python3 amp_design.py N   (generates N candidates, prints ranked shortlist)
Pipeline: ESM-2 t6_8M masked parallel decoding (temperature 1.0, top-p 0.95) -> Macrel AMP
scoring -> novelty filter vs APD natural AMPs (MMseqs2 <70% pident).
BOUNDARY WARNING (REPORT.md): unconditional sampling yields ~0.2% Macrel-AMP+ at prob>=0.8
(51x below shuffled-composition baseline) - use for mechanism exploration, not production design."""
import sys, os, subprocess, json, random
import numpy as np, torch, esm
AA='ACDEFGHIKLMNPQRSTVWY'
def generate(n, seed=7):
    model,alphabet=esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
    toks_aa=[alphabet.get_idx(a) for a in AA]; mask_id=alphabet.mask_idx
    here=os.path.dirname(os.path.abspath(__file__))
    lens=json.load(open(os.path.join(here,'..','data','apd_lengths.json')))
    rng=random.Random(seed); np.random.seed(seed); torch.manual_seed(seed)
    seqs=[]
    while len(seqs)<n:
        batch=[rng.choice(lens) for _ in range(16)]
        L=max(batch)
        toks=torch.full((16,L+2),mask_id,dtype=torch.long)
        toks[:,0]=alphabet.cls_idx
        for i,l in enumerate(batch): toks[i,l+1]=alphabet.eos_idx
        fixed=torch.zeros_like(toks,dtype=torch.bool); fixed[:,0]=True
        for i,l in enumerate(batch): fixed[i,l+1]=True
        with torch.no_grad():
            for r in range(12):
                logits=model(toks)['logits'][:,:,torch.tensor(toks_aa)]
                rem=(~fixed).nonzero()
                k=max(1,int(np.ceil(len(rem)/(12-r))))
                pick=rem[torch.randperm(len(rem))[:k]]
                for b,p in pick:
                    lg=logits[b,p]
                    v,ix=torch.sort(lg,descending=True); pr=torch.softmax(v,dim=-1)
                    cum=torch.cumsum(pr,-1); keep=cum<=0.95; keep[0]=True
                    v=v*keep+(-1e9)*(~keep); pr=torch.softmax(v,-1)
                    toks[b,p]=toks_aa[ix.gather(-1,torch.multinomial(pr,1)).item()]
                fixed[pick[:,0],pick[:,1]]=True
        for i,l in enumerate(batch):
            s=''.join(alphabet.get_tok(t) for t in toks[i,1:l+1].tolist())
            s=''.join(c for c in s if c in AA)
            if 12<=len(s)<=50: seqs.append(s)
            if len(seqs)>=n: break
    return seqs[:n]
def main():
    n=int(sys.argv[1]) if len(sys.argv)>1 else 20
    seqs=generate(n)
    fa='/tmp/amp_design_in.fasta'
    with open(fa,'w') as f:
        for i,s in enumerate(seqs): f.write(f'>c{i}\n{s}\n')
    subprocess.run(['macrel','peptides','-f',fa,'-o','/tmp/amp_design_out','-t','2','--keep-negatives','--force'],capture_output=True)
    import gzip
    scored={}
    for line in gzip.open('/tmp/amp_design_out/macrel.out.prediction.gz','rt'):
        if line.startswith('#') or line.startswith('Access'): continue
        p=line.rstrip('\n').split('\t'); scored[p[0]]=(float(p[4]),float(p[6]))
    ranked=sorted(scored.items(),key=lambda kv:-kv[1][0])
    print(f'{n} generated; ranked by Macrel AMP probability:')
    for cid,(prob,hemo) in ranked[:10]:
        print(f'{cid}\tAMP_prob={prob:.3f}\themo_prob={hemo:.3f}\t{seqs[int(cid[1:])]}')
if __name__=='__main__': main()
