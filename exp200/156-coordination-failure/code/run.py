import gzip, io, json, numpy as np, pandas as pd, sys
rng=np.random.default_rng(0)
def annot(gpl):
    lines=gzip.open(f'data/{gpl}.annot.gz','rt',errors='replace').read().split('\n')
    i=[k for k,l in enumerate(lines) if l.startswith('!platform_table_begin')][0]
    t=pd.read_csv(io.StringIO('\n'.join(lines[i+1:])),sep='\t',usecols=['ID','Gene symbol'],dtype=str).dropna()
    t=t[~t['Gene symbol'].str.contains('///')]; return dict(zip(t.ID,t['Gene symbol']))
def load(gse,gpl,field):
    L=gzip.open(f'data/{gse}_series_matrix.txt.gz','rt').read().split('\n')
    lab=None
    for l in L:
        if l.startswith(field) and (lab is None):
            v=[x.strip('"') for x in l.split('\t')[1:]]
            if field!='!Sample_characteristics_ch1' or any('disease:' in x or 'ntrol' in x for x in v): lab=v
    b=[k for k,l in enumerate(L) if l.startswith('!series_matrix_table_begin')][0]; e=[k for k,l in enumerate(L) if l.startswith('!series_matrix_table_end')][0]
    X=pd.read_csv(io.StringIO('\n'.join(L[b+1:e])),sep='\t',index_col=0)
    m=annot(gpl); X=X[X.index.isin(m)]; X['g']=X.index.map(m)
    X['mu']=X.drop(columns='g').mean(1); X=X.sort_values('mu',ascending=False).drop_duplicates('g').set_index('g').drop(columns='mu')
    return X,np.array(lab)
gmt={}
for l in open('data/ReactomePathways.gmt'):
    p=l.rstrip('\n').split('\t'); gmt[p[0]]=set(p[2:])
def coord(X,idx,paths):
    return np.array([np.nanmean(np.corrcoef(X[np.ix_(g,idx)])[np.triu_indices(len(g),1)]) for g in paths])
def analyse(X,ctrl,case,nperm=200,paths_named=None):
    genes={g:i for i,g in enumerate(X.index)}; A=X.values.astype(float)
    names=[];P=[]
    for n,s in gmt.items():
        g=[genes[x] for x in s if x in genes]
        if 15<=len(g)<=100 and (paths_named is None or n in paths_named): names.append(n); P.append(g)
    obs=coord(A,case,P)-coord(A,ctrl,P)
    allidx=np.r_[ctrl,case]; nulls=[]
    for _ in range(nperm):
        pm=rng.permutation(allidx); nulls.append(coord(A,pm[len(ctrl):],P)-coord(A,pm[:len(ctrl)],P))
    N=np.array(nulls)
    p=(1+(np.abs(N)>=np.abs(obs)).sum(0))/(nperm+1)
    # expression shift: mean |t| of members
    from scipy.stats import ttest_ind
    t=ttest_ind(A[:,case],A[:,ctrl],axis=1).statistic
    et=np.array([np.nanmean(np.abs(t[g])) for g in P])
    return pd.DataFrame({'pathway':names,'delta':obs,'p':p,'mean_abs_t':et}),N,names
