from pathlib import Path
import pandas as pd,json
R=Path(__file__).resolve().parents[1];p=pd.read_csv(R/'results/frozen_projects.csv');m=pd.read_csv(R/'results/frozen_file_manifest.csv');d=pd.read_csv(R/'results/download_status.tsv',sep='\t',header=None,names=['domain','project','file','status'])
rows=[]
for dom in ['human','mouse','yeast']:
 x=p[p.domain==dom];ok=d[(d.domain==dom)&d.status.eq('OK')].project.nunique();rows.append({'domain':dom,'projects_frozen':len(x),'representative_files_downloaded':ok,'two_studies_downloadable':ok>=2,'schema_valid_studies':0,'feasibility_pass':False,'blocker':'PRIDE FTP TLS EOF from execution environment; no candidate bytes retrievable, therefore no schema validation'})
out=pd.DataFrame(rows);out.to_csv(R/'results/feasibility_gate.csv',index=False);print(out.to_string(index=False))
