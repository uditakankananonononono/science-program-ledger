import os, sys, time, json
import numpy as np, torch, esm
FILES=[('dev_all','dev_all.fasta'),('frozen_pos','frozen_pos.fasta'),('frozen_decoys','frozen_decoys.fasta')]
os.makedirs('emb',exist_ok=True)
def read_fasta(p):
    recs=[]
    for blk in open(p).read().split('>'):
        blk=blk.strip()
        if not blk or '\n' not in blk: continue
        hdr,seq=blk.split('\n',1)
        recs.append((hdr.split('|')[1] if '|' in hdr else hdr.split()[0], seq.replace('\n','')[:512]))
    return recs
model,alphabet=esm.pretrained.esm2_t6_8M_UR50D()
model.eval()
bc=alphabet.get_batch_converter()
BUDGET=float(sys.argv[1]) if len(sys.argv)>1 else 480.0
t0=time.time()
for tag,path in FILES:
    out=f'emb/{tag}.npz'
    done={}
    if os.path.exists(out):
        z=np.load(out,allow_pickle=True)
        done={i:e for i,e in zip(z['ids'],z['emb'])}
    recs=read_fasta(path)
    todo=[(i,s) for i,s in recs if i not in done]
    print(tag, 'todo:', len(todo), 'done:', len(done), flush=True)
    if not todo: continue
    with torch.no_grad():
        for j in range(0,len(todo),16):
            if time.time()-t0>BUDGET: break
            batch=todo[j:j+16]
            _,_,toks=bc([(i,s) for i,s in batch])
            r=model(toks,repr_layers=[6])['representations'][6]
            for k,(i,s) in enumerate(batch):
                done[i]=r[k,1:len(s)+1].mean(0).numpy().astype(np.float32)
            if j%160==0:
                np.savez(out+'.tmp.npz',ids=list(done.keys()),emb=np.stack(list(done.values())))
                os.replace(out+'.tmp.npz',out)
            if time.time()-t0>BUDGET: break
    np.savez(out+'.tmp.npz',ids=list(done.keys()),emb=np.stack(list(done.values())))
    os.replace(out+'.tmp.npz',out)
    if time.time()-t0>BUDGET: break
print('checkpoint saved, elapsed', round(time.time()-t0,1))
