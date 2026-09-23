import pandas as pd, numpy as np
t=pd.read_csv('../data/tempura.csv'); r=pd.read_csv('../data/refproteomes.tsv',sep='\t'); r.columns=['upid','taxid','org','n']
t=t.dropna(subset=['Topt_ave']); r['sp']=r['org'].str.split().str[:2].str.join(' ')
m=t.merge(r,left_on='genus_and_species',right_on='sp').drop_duplicates('genus_and_species')
rng=np.random.default_rng(17)
m=m.sample(frac=1,random_state=17).drop_duplicates('genus')
hot=m[m['Topt_ave']>=50].sample(120,random_state=17); rest=m[m['Topt_ave']<50].sample(120,random_state=17)
s=pd.concat([hot,rest]); s['family']=s['family'].fillna(s['genus'])
s[['upid','genus_and_species','genus','family','superkingdom','Topt_ave','n']].to_csv('../data/selected.tsv',sep='\t',index=False)
print(len(s),len(hot),'hot',s['superkingdom'].value_counts().to_dict(),s['family'].nunique(),'families')
