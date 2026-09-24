#!/usr/bin/env python3
"""refine.py - 014F score-guided iterative refinement (locked mechanics, GATES.md).
Per iteration: re-mask uniform-random 15% of positions, resample with 014's exact
ESM-2 t6_8M masked decoding (top-p 0.95, temp 1.0), greedy-accept iff Macrel prob
does not decrease. 30 iterations, rng seed 7. Checkpointed per iteration."""
import os, sys, json, random, subprocess
import numpy as np, torch, esm
AA='ACDEFGHIKLMNPQRSTVWY'
import os as _os
ITERS=int(_os.environ.get('REFINE_ITERS','30')); MASKFRAC=0.15
rng=random.Random(7); np.random.seed(7); torch.manual_seed(7)
model,alphabet=esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
bc=alphabet.get_batch_converter()
toks_aa=[alphabet.get_idx(a) for a in AA]
mask_id=alphabet.mask_idx
def top_p_sample(logits,p=0.95,temp=1.0):
    logits=logits/temp
    v,ix=torch.sort(logits,descending=True)
    probs=torch.softmax(v,dim=-1); cum=torch.cumsum(probs,dim=-1)
    keep=cum<=p; keep[...,0]=True
    v=v*keep+(-1e9)*(~keep)
    pr=torch.softmax(v,dim=-1)
    return ix.gather(-1,torch.multinomial(pr,1))
def read_fasta(p):
    recs=[]
    for blk in open(p).read().split('>'):
        blk=blk.strip()
        if not blk or '\n' not in blk: continue
        hdr,seq=blk.split('\n',1)
        recs.append((hdr.split()[0],seq.replace('\n','')))
    return recs
def macrel_probs(recs):
    import gzip, shutil
    with open('tmp_refine.fasta','w') as f:
        for i,s in recs: f.write(f'>{i}\n{s}\n')
    if os.path.exists('tmp_refine_out'): shutil.rmtree('tmp_refine_out')
    subprocess.run(['macrel','peptides','--fasta','tmp_refine.fasta','--output','tmp_refine_out','--keep-negatives'],
                   check=True, capture_output=True)
    probs={}
    with gzip.open('tmp_refine_out/macrel.out.prediction.gz','rt') as fh:
        for line in fh:
            if line.startswith('#') or line.startswith('Access'): continue
            parts=line.split('\t')
            if len(parts)>=5:
                try: probs[parts[0]]=float(parts[4])
                except: pass
    return probs
def propose(recs):
    """one masked-resample pass over all seqs, batched by 16; 3 progressive unmask rounds"""
    L=max(len(s) for _,s in recs)
    out={}
    for j in range(0,len(recs),16):
        batch=recs[j:j+16]
        bl=max(len(s) for _,s in batch)
        toks=torch.full((len(batch),bl+2),mask_id,dtype=torch.long)
        toks[:,0]=alphabet.cls_idx
        fixed=torch.zeros_like(toks,dtype=torch.bool); fixed[:,0]=True
        for i,(rid,s) in enumerate(batch):
            toks[i,len(s)+1]=alphabet.eos_idx; fixed[i,len(s)+1]=True
            n_mask=max(1,int(round(len(s)*MASKFRAC)))
            mpos=set(rng.sample(range(len(s)),n_mask))
            for p in range(len(s)):
                if p in mpos: toks[i,p+1]=mask_id
                else: toks[i,p+1]=alphabet.get_idx(s[p]); fixed[i,p+1]=True
        with torch.no_grad():
            for r in range(3):
                logits=model(toks)['logits'][:,:,torch.tensor(toks_aa)]
                remaining=(~fixed)
                if remaining.sum()==0: break
                n_unmask=max(1,int(np.ceil(remaining.sum().item()/(3-r))))
                cand=remaining.nonzero()
                pick=cand[torch.randperm(len(cand))[:n_unmask]]
                new=toks.clone()
                for b,p in pick:
                    new[b,p]=toks_aa[top_p_sample(logits[b,p],0.95,1.0).item()]
                toks=new; fixed[pick[:,0],pick[:,1]]=True
        for i,(rid,s) in enumerate(batch):
            seq=''.join(alphabet.get_tok(t) for t in toks[i,1:len(s)+1].tolist())
            out[rid]=''.join(c for c in seq if c in AA)
    return out
if __name__=='__main__':
    smoke='--smoke' in sys.argv
    seeds=read_fasta('seeds.fasta')
    if smoke: seeds=seeds[:2]
    state_file='refine_state.json'
    if os.path.exists(state_file) and not smoke:
        st=json.load(open(state_file))
    else:
        st={'iter':0,'cur':{i:s for i,s in seeds},'prob':{},'traj':{i:[] for i,_ in seeds}}
    if st['iter']==0:
        st['prob']=macrel_probs(list(st['cur'].items()))
    maxit=1 if smoke else ITERS
    while st['iter']<maxit:
        prop=propose(list(st['cur'].items()))
        pprob=macrel_probs(list(prop.items()))
        for rid in st['cur']:
            old=st['prob'].get(rid,0.0); new=pprob.get(rid,old)
            if new>=old:
                st['cur'][rid]=prop[rid]; st['prob'][rid]=new
            st['traj'][rid].append(st['prob'][rid])
        st['iter']+=1
        json.dump(st,open(state_file+'.tmp','w')); os.replace(state_file+'.tmp',state_file)
        print('iter',st['iter'],'median prob',round(float(np.median(list(st['prob'].values()))),3),flush=True)
    if not smoke:
        with open('final.fasta','w') as f:
            for i,s in st['cur'].items(): f.write(f'>{i}\n{s}\n')
        json.dump(st['traj'],open('trajectories.json','w'))
        print('DONE: final.fasta + trajectories.json')
