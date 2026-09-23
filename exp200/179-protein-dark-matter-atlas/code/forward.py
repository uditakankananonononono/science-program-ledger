import pandas as pd, numpy as np, re, json
from collections import Counter
PH=re.compile(r'^(C\d+orf\d+|CXorf\d+|CYorf\d+|FAM\d+[A-Z]*\d*|KIAA\d+|TMEM\d+[A-Z]*|CCDC\d+[A-Z]*|LOC\d+|ORF\d+)$')
BAD=re.compile(r'open reading frame|family with sequence similarity|Coiled-coil domain containing|Transmembrane proteins|uncharacterized|KIAA|Long non-coding',re.I)
h=pd.read_csv('data/hgnc.txt',sep='\t',dtype=str,low_memory=False); h=h[h.status=='Approved']
sym2g={r.symbol:{g for g in str(r.gene_group).split('|') if r.gene_group==r.gene_group and not BAD.search(g)} for r in h.itertuples()}
for r in h.itertuples():
    if isinstance(r.prev_symbol,str):
        for p in r.prev_symbol.split('|'): sym2g.setdefault(p.strip(),sym2g[r.symbol])
dark=h[(h.locus_group=='protein-coding gene')&h.symbol.str.match(PH)][['symbol','name','hgnc_id']]
info=pd.read_csv('data/9606.protein.info.v12.0.txt.gz',sep='\t',usecols=[0,1,3]); info.columns=['pid','n','annot']
p2n=dict(zip(info.pid,info.n)); n2p=dict(zip(info.n,info.pid)); ann=dict(zip(info.n,info.annot))
dark['pid']=dark.symbol.map(n2p); pids=set(dark.pid.dropna()); nb={p:[] for p in pids}
for ch in pd.read_csv('data/9606.protein.links.v12.0.txt.gz',sep=' ',chunksize=3_000_000):
    ch=ch[ch.protein1.isin(pids)&(ch.combined_score>=700)]
    for p,q,s in ch.itertuples(index=False): nb[p].append((p2n.get(q,''),s))
rows=[]
for r in dark.itertuples():
    if not isinstance(r.pid,str): rows.append((r.symbol,r.name,0,0,'','','','not in STRING v12')); continue
    cnt=Counter(); k=0; nbs=[]
    for q,s in sorted(nb[r.pid],key=lambda x:-x[1]):
        g=sym2g.get(q,set())
        if g: k+=1; cnt.update(g)
        nbs.append(q)
    top=cnt.most_common(3)
    status='eligible' if k>=3 else ('too few grouped neighbours' if nb[r.pid] else 'no high-confidence neighbours')
    rows.append((r.symbol,r.name,len(nb[r.pid]),k,' | '.join(f'{g} ({c}/{k})' for g,c in top),';'.join(nbs[:8]),(ann.get(r.symbol,'') or '')[:160],status))
d=pd.DataFrame(rows,columns=['symbol','hgnc_name','n_neighbours_700','n_grouped_neighbours','top3_group_nominations','top_neighbours','string_annotation_excerpt','status'])
d['top1_vote_share']=d.top3_group_nominations.str.extract(r'\((\d+)/(\d+)\)').astype(float).pipe(lambda x:x[0]/x[1])
d=d.sort_values(['status','top1_vote_share','n_grouped_neighbours'],ascending=[True,False,False])
d.to_csv('results/forward_nominations_2026.csv',index=False)
print(d.status.value_counts().to_string()); print(len(d))
print(d[d.status=='eligible'].head(25)[['symbol','n_grouped_neighbours','top3_group_nominations']].to_string(max_colwidth=110))
