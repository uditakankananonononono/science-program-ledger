import pandas as pd,numpy as np,gzip,ast,re,pathlib,json
B=pathlib.Path(__file__).resolve().parents[1]; d=pd.read_csv(B/'data/raw/AlloBench.csv');s=pd.read_csv('/tmp/sifts_subset.csv');s.columns=[x.upper() for x in s.columns];s.PDB=s.PDB.str.upper()
rows=[]
for tid,g in d.groupby('target_id',sort=True):
 ok=False; reasons=[]
 for _,z in g.iterrows():
  pid=str(z.allosteric_pdb).upper();uni=str(z.pdb_uniprot);sites=ast.literal_eval(str(z.allosteric_site_residue));chs=sorted(set(str(x).split('-')[0] for x in sites if '-' in str(x)))
  mod=str(z.modulator_chain).strip(); q=s[(s.PDB==pid)&(s.SP_PRIMARY==uni)&(s.CHAIN.isin(chs))]
  mapped=not q.empty; contradiction=(bool(chs) and mod not in chs)
  reasons.append({'target_id':tid,'pdb_id':pid,'uniprot':uni,'site_chains':';'.join(chs),'modulator_chain':mod,'chain_contradiction':contradiction,'sifts_segment_mapping':mapped,'segments':len(q)})
  if mapped:ok=True
 rows+=reasons
pd.DataFrame(rows).to_csv(B/'results/segment_mapping_audit.csv',index=False)
t=pd.DataFrame(rows);per=t.groupby('target_id').sifts_segment_mapping.any();obj={'targets':int(len(per)),'targets_with_unambiguous_accession_and_site_chain_segment_mapping':int(per.sum()),'fraction':float(per.mean()),'gate_80pct':bool(per.mean()>=.8),'records_with_chain_contradiction':int(t.chain_contradiction.sum()),'4UC5':t[t.pdb_id=='4UC5'].to_dict('records')}
(B/'results/preflight_gate.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps(obj,indent=2))
