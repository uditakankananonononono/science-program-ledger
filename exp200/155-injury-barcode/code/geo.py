import gzip,numpy as np,pandas as pd
def load(g):
    ch=[];rows=[];inT=False
    for l in gzip.open(f'data/{g}.txt.gz','rt'):
        if l.startswith('!Sample_characteristics_ch1') or l.startswith('!Sample_source_name_ch1'): ch.append([x.strip('"') for x in l.rstrip('\n').split('\t')[1:]])
        if l.startswith('!series_matrix_table_begin'): inT=True;continue
        if l.startswith('!series_matrix_table_end'): break
        if inT: rows.append(l.rstrip('\n').split('\t'))
    df=pd.DataFrame([r[1:] for r in rows[1:]],index=[r[0].strip('"') for r in rows[1:]],columns=[c.strip('"') for c in rows[0][1:]]).apply(pd.to_numeric,errors='coerce')
    meta=[' | '.join(c[i] for c in ch) for i in range(df.shape[1])];return df,meta
def annot(p):
    m={};h=None
    for l in gzip.open(f'data/{p}.annot.gz','rt'):
        f=l.rstrip('\n').split('\t')
        if h is None:
            if f[0]=='ID': h=f.index('Gene symbol')
            continue
        if len(f)>h and f[h]: m[f[0]]=f[h]
    return m
def genes(df,p):
    m=annot(p);df=df.copy();df['g']=[m.get(i) for i in df.index];df=df[df['g'].notna()&~df['g'].astype(str).str.contains('///')]
    if df.drop(columns='g').max().max()>100: df.iloc[:,:-1]=np.log2(df.iloc[:,:-1].clip(lower=1))
    df['mm']=df.drop(columns='g').mean(1);df=df.sort_values('mm',ascending=False).drop_duplicates('g');return df.set_index('g').drop(columns='mm')
