import re,random,json,numpy as np,torch,time
from collections import defaultdict
from Bio import Align
from Bio.Align import substitution_matrices
from transformers import AutoTokenizer,AutoModel
from scipy.stats import binomtest
random.seed(0);torch.set_num_threads(2)
D=[];h=None;s=[]
for l in open('data/scope40.fa'):
    if l.startswith('>'):
        if h: D.append((h,''.join(s).upper()))
        h=l[1:].split()[:2];s=[]
    else: s.append(l.strip())
D.append((h,''.join(s).upper()))
D=[(i,c,q) for (i,c),q in D if c[0] in 'abcd' and 50<=len(q)<=300 and set(q)<=set('ACDEFGHIKLMNPQRSTVWYX')]
fold=lambda c:'.'.join(c.split('.')[:2]);sf=lambda c:'.'.join(c.split('.')[:3])
F=defaultdict(lambda:defaultdict(list))
for d in D: F[fold(d[1])][sf(d[1])].append(d)
ok=[f for f in F if sum(len(v)>=3 for v in F[f].values())>=2]
qs=[];refs=[]
for f in sorted(ok):
    good=sorted(k for k,v in F[f].items() if len(v)>=3);qsf=random.choice(good)
    qs+=F[f][qsf];refs+=[d for k,v in F[f].items() if k!=qsf for d in v]
random.shuffle(qs);qs=qs[:300]
other=[d for d in D if fold(d[1]) not in ok];random.shuffle(other)
refs=refs+other;refs=refs[:1500] if len(refs)>1500 else refs
print('folds',len(ok),'queries',len(qs),'refs',len(refs),flush=True)
tok=AutoTokenizer.from_pretrained('facebook/esm2_t6_8M_UR50D');m=AutoModel.from_pretrained('facebook/esm2_t6_8M_UR50D').eval()
def E(seqs):
    out=[]
    for q in seqs:
        with torch.no_grad(): out.append(m(**tok(q,return_tensors='pt')).last_hidden_state[0,1:-1].mean(0).numpy())
    x=np.stack(out);return x/np.linalg.norm(x,axis=1,keepdims=True)
t=time.time();Eq=E([d[2] for d in qs]);Er=E([d[2] for d in refs]);print('emb',round(time.time()-t),flush=True)
np.save('results/Eq.npy',Eq);np.save('results/Er.npy',Er)
esm_hit=(Eq@Er.T).argmax(1)
al=Align.PairwiseAligner();al.substitution_matrix=substitution_matrices.load('BLOSUM62');al.open_gap_score=-11;al.extend_gap_score=-1;al.mode='local'
sw_hit=[];t=time.time()
for i,q in enumerate(qs):
    sc=[al.score(q[2],r[2]) for r in refs];sw_hit.append(int(np.argmax(sc)))
    if i%50==0: print('sw',i,round(time.time()-t),flush=True)
qf=[fold(d[1]) for d in qs];e=np.array([fold(refs[j][1])==f for j,f in zip(esm_hit,qf)]);w=np.array([fold(refs[j][1])==f for j,f in zip(sw_hit,qf)])
b=int((e&~w).sum());c=int((~e&w).sum());p=binomtest(b,b+c,0.5).pvalue if b+c else 1.0
cls={k:dict(n=int(sum(1 for d in qs if d[1][0]==k)),esm=float(np.mean([x for x,d in zip(e,qs) if d[1][0]==k])),sw=float(np.mean([x for x,d in zip(w,qs) if d[1][0]==k]))) for k in 'abcd'}
res=dict(n_folds=len(ok),n_q=len(qs),n_ref=len(refs),esm_acc=float(e.mean()),sw_acc=float(w.mean()),diff=float(e.mean()-w.mean()),mcnemar_b=b,mcnemar_c=c,mcnemar_p=p,by_class=cls)
res['G1']=res['esm_acc']>=0.40;res['G2']=bool(res['diff']>=0.10 and p<0.01)
print(json.dumps(res,indent=1));json.dump(res,open('results/main.json','w'),indent=1)
json.dump(dict(q=[d[0] for d in qs],r=[d[0] for d in refs]),open('results/ids.json','w'))
