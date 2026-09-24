import parasail,numpy as np,time
recs=[]
for l in open('../data/astral-scopedom-seqres-gd-sel-gs-bib-40-2.08.fa'):
    if l[0]=='>': h=l[1:].split(); recs.append([h[0],h[1],''])
    else: recs[-1][2]+=l.strip().upper()
recs=[r for r in recs if r[1][0] in 'abcd']
rng=np.random.default_rng(41); S=[recs[i] for i in rng.choice(len(recs),4000,replace=False)]
seqs=[''.join(c if c in 'ARNDCQEGHILKMFPSTWYVBZX' else 'X' for c in s[2]) for s in S]
n=len(seqs); M=np.zeros((n,n),np.float32); t0=time.time()
for i in range(n):
    p=parasail.profile_create_16(seqs[i],parasail.blosum62)
    for j in range(i+1,n):
        r=parasail.sw_striped_profile_16(p,seqs[j],11,1); M[i,j]=M[j,i]=r.score
    if i%250==0: print(i,round(time.time()-t0),flush=True)
np.save('../data/sw.npy',M); open('../data/ids.tsv','w').write(''.join(f'{s[0]}\t{s[1]}\t{len(q)}\n' for s,q in zip(S,seqs)))
print('done',flush=True)
