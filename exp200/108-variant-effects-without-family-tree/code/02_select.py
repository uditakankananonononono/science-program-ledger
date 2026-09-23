import pandas as pd, numpy as np
d=pd.read_csv('data/missense_2star.tsv',sep='\t')
u=pd.read_csv('data/uniprot_human_sp.tsv.gz',sep='\t')
u.columns=['acc','gene','length','seq']
u=u.dropna(subset=['gene']).drop_duplicates('gene',keep=False)  # ambiguous gene symbols dropped
seq=dict(zip(u.gene,u.seq))
d=d[d.gene.isin(seq)]
ok=[len(seq[g])>=p and seq[g][p-1]==w for g,p,w in zip(d.gene,d.pos,d.wt)]
print('ref-match',sum(ok),'of',len(d)); d=d[ok]
d=d[[len(seq[g])<=1022 for g in d.gene]]
g=d.groupby('gene').label.agg(['sum','count']); el=g[(g['sum']>=1)&(g['count']-g['sum']>=1)].index
print('eligible<=1022aa',len(el))
rng=np.random.default_rng(20260923)
pick=sorted(rng.choice(sorted(el),size=min(150,len(el)),replace=False))
e=d[d.gene.isin(pick)].copy()
e['seq_len']=[len(seq[x]) for x in e.gene]
e.to_csv('data/eval_set.tsv',sep='\t',index=False)
pd.DataFrame({'gene':pick,'seq':[seq[x] for x in pick]}).to_csv('data/eval_seqs.tsv',sep='\t',index=False)
print('eval genes',len(pick),'variants',len(e),e.label.value_counts().to_dict())
