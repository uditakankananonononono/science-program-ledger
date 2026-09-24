import os, sys, time, json
import numpy as np, torch, esm
FILES=[('train','data/train.fasta'),('dev','data/dev.fasta'),('frozen','data/frozen.fasta')]
os.makedirs('results/emb',exist_ok=True)
def read_fasta(p):
    recs=[]
    for blk in open(p).read().split('>'):
        if not blk: continue
        hdr,seq=blk.split('\n',1)
        recs.append((hdr.split('|')[1] if '|' in hdr else hdr.split()[0], seq.replace('\n','')[:512]))
    return recs
model,alphabet=esm.pretrained.esm2_t6_8M_UR50D()
model.eval()
bc=alphabet.get_batch_converter()
BUDGET=float(sys.argv[1]) if len(sys.argv)>1 else 95.0
t0=time.time()
for tag,path in FILES:
    out=f'results/emb/{tag}.npz'
    done={}
    if os.path.exists(out):
        z=np.load(out,allow_pickle=True)
        done={i:e for i,e in zip(z['ids'],z['emb'])}
    recs=read_fasta(path)
    todo=[(i,s) for i,s in recs if i not in done]
    if not todo: continue
    with torch.no_grad():
        for j in range(0,len(todo),16):
            if time.time()-t0>BUDGET: break
            batch=todo[j:j+16]
            _,_,toks=bc([(i,s) for i,s in batch])
            r=model(toks,repr_layers=[6],return_contacts=False)
            rep=r['representations'][6]
            for k,(i,s) in enumerate(batch):
                n=min(len(s),512)
                done[i]=rep[k,1:n+1].mean(0).numpy().astype(np.float32)
            print(tag,j+len(batch),'/',len(todo),flush=True)
        if time.time()-t0>BUDGET:
            np.savez(out,ids=list(done.keys()),emb=np.stack(list(done.values())))
            print('checkpoint',tag,len(done),'/',len(recs)); sys.exit(0)
    np.savez(out,ids=list(done.keys()),emb=np.stack(list(done.values())))
    print('DONE',tag,len(done))
print('ALL DONE')
