import torch, esm, pandas as pd, numpy as np
torch.set_num_threads(2)
model, alph = esm.pretrained.esm2_t6_8M_UR50D(); model.eval()
bc=alph.get_batch_converter()
s=pd.read_csv('data/eval_seqs_R2.tsv',sep='\t'); e=pd.read_csv('data/eval_set_R2.tsv',sep='\t')
res=[]
for g,sq in zip(s.gene,s.seq):
    _,_,t=bc([(g,sq)])
    with torch.no_grad(): lp=torch.log_softmax(model(t)['logits'][0],-1).numpy()
    ent=-(np.exp(lp)*lp).sum(-1)
    for i,r in e[e.gene==g].iterrows():
        p=int(r.pos)
        res.append((i, lp[p,alph.get_idx(r.mut)]-lp[p,alph.get_idx(r.wt)], ent[p]))
r=pd.DataFrame(res,columns=['idx','s_esm','site_entropy']).set_index('idx')
e=e.join(r); e.to_csv('results/scores_R2.tsv',sep='\t',index=False); print(e.s_esm.isna().sum(), len(e))
