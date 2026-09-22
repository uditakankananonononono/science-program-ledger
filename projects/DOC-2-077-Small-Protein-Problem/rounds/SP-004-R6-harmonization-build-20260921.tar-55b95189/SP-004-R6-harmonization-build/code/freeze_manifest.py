from pathlib import Path
import pandas as pd,re,hashlib,json
R=Path(__file__).resolve().parents[1];p=pd.read_csv(R/'data/raw/project_feasibility.csv');f=pd.read_csv(R/'data/raw/file_inventory.csv')
rows=[];rank=[]
for d in ['human','mouse','yeast']:
 for proj,g in f[(f.domain==d)&f.processed_candidate].groupby('project'):
  meta=p[p.project==proj].iloc[0]; names=' '.join(g.file_name.astype(str)); std=bool(re.search(r'\.mz(id|identml)|mztab',names,re.I)); pep=bool(re.search(r'psm|peptide',names,re.I)); small=g[g.bytes<=200_000_000]
  if meta.explicit_1pct_fdr_metadata and len(small):rank.append({'domain':d,'project':proj,'standard_id':std,'peptide_token':pep,'candidate_bytes':int(small.bytes.sum())})
r=pd.DataFrame(rank).sort_values(['domain','standard_id','peptide_token','candidate_bytes','project'],ascending=[True,False,False,True,True]);sel=r.groupby('domain').head(2);sel.to_csv(R/'results/frozen_projects.csv',index=False)
for _,x in sel.iterrows():
 g=f[(f.project==x.project)&f.processed_candidate&(f.bytes<=200_000_000)].copy();g['selected_project']=True;rows.append(g)
m=pd.concat(rows);m.to_csv(R/'results/frozen_file_manifest.csv',index=False)
print(sel.to_string(index=False));print('bytes',m.bytes.sum())
