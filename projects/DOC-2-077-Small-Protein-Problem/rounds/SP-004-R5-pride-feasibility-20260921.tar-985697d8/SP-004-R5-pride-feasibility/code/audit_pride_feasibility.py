#!/usr/bin/env python3
from pathlib import Path
import json,urllib.request,time,re,pandas as pd
R=Path(__file__).resolve().parents[1];rows=[];file_rows=[]
proc_ext=re.compile(r'\.(mzid|mzidentml|pep\.xml|pepxml|idxml|tsv|csv|txt|mztab)(\.gz|\.zip)?$',re.I)
raw_ext=re.compile(r'\.(raw|wiff|d|mzml)(\.gz|\.zip)?$',re.I)
for dom in ['human','mouse','yeast']:
 projects=json.load(open(R/f'data/raw/pride_search_{dom}.json'))
 for p in projects[:25]:
  acc=p['accession'];url=f'https://www.ebi.ac.uk/pride/ws/archive/v3/projects/{acc}/files'
  try:
   with urllib.request.urlopen(url,timeout=30) as h: files=json.loads(h.read())
  except Exception as e:files=[]
  proc=[];raw=[]
  for f in files:
   n=f.get('fileName',''); cat=(f.get('fileCategory') or {}).get('value','')+' '+(f.get('fileCategory') or {}).get('name','')
   if proc_ext.search(n) or re.search(r'(RESULT|SEARCH|PEPTIDE|IDENTIFICATION)',cat,re.I):proc.append(f)
   if raw_ext.search(n) or 'RAW' in cat.upper():raw.append(f)
   file_rows.append({'domain':dom,'project':acc,'file_name':n,'category':cat,'bytes':f.get('fileSizeBytes',0),'processed_candidate':bool(f in proc),'raw_candidate':bool(f in raw)})
  # metadata evidence strings; explicit FDR in project protocols/description
  text=' '.join(str(p.get(k,'')) for k in ['title','projectDescription','dataProcessingProtocol','sampleProcessingProtocol'])
  fdr=bool(re.search(r'(1%|0\.01).{0,30}(FDR|false discovery)|(FDR|false discovery).{0,30}(1%|0\.01)',text,re.I))
  rows.append({'domain':dom,'project':acc,'title':p.get('title',''),'processed_candidates':len(proc),'raw_files':len(raw),'processed_bytes':sum(f.get('fileSizeBytes',0) or 0 for f in proc),'explicit_1pct_fdr_metadata':fdr,'processed_feasible':len(proc)>0 and fdr})
  time.sleep(.01)
pd.DataFrame(rows).to_csv(R/'results/project_feasibility.csv',index=False);pd.DataFrame(file_rows).to_csv(R/'results/file_inventory.csv',index=False)
x=pd.DataFrame(rows);s=x.groupby('domain').agg(projects_audited=('project','size'),projects_with_processed=('processed_candidates',lambda z:(z>0).sum()),projects_with_explicit_fdr=('explicit_1pct_fdr_metadata','sum'),projects_meeting_basic=('processed_feasible','sum'),processed_candidate_gb=('processed_bytes',lambda z:z.sum()/1e9)).reset_index();s.to_csv(R/'results/feasibility_summary.csv',index=False);print(s.to_string(index=False))
