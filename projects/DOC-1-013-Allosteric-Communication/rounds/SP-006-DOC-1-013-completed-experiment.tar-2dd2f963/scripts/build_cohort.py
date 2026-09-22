import requests,json,datetime,hashlib,pathlib,csv,time,re
from Bio.PDB import MMCIFParser
from Bio.PDB.Polypeptide import is_aa
B=pathlib.Path(__file__).resolve().parents[1]; raw=B/'data/raw'; led=B/'provenance/http_ledger.jsonl'; res=B/'results'; res.mkdir(exist_ok=True)
S=requests.Session()
def get(url,path):
 for attempt in range(2):
  r=S.get(url,timeout=60); b=r.content
  with led.open('a') as f:f.write(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'GET','url':url,'status':r.status_code,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'attempt':attempt+1})+'\n')
  if r.ok:path.write_bytes(b);return r
  time.sleep(1)
 return r
exclude={'HOH','DMS','EDO','GOL','PEG','SO4','PO4','ACT','FMT','TRS','MES','HEP','MPD','IOD','CL','NA','K','MG','CA','ZN','MN','CO','NI','CD','CU','ATP','ADP','AMP','GDP','GTP','NAD','NAP','FAD','FMN','SAM','SAH','COA'}
rows=[]; labels=[]; accepted=0
for pid in [x.strip() for x in (raw/'candidate_ids.txt').read_text().splitlines()]:
 if accepted>=15:break
 row={'pdb_id':pid,'decision':'reject','reason':''}
 try:
  jp=raw/f'{pid}.entry.json'; r=get(f'https://data.rcsb.org/rest/v1/core/entry/{pid}',jp)
  if not r.ok: row['reason']=f'entry_http_{r.status_code}';rows.append(row);continue
  j=r.json(); title=j.get('struct',{}).get('title',''); row['title']=title
  if not re.search(r'\ballosteric\b',title,re.I):row['reason']='title_not_allosteric';rows.append(row);continue
  methods=';'.join(x.get('method','') for x in j.get('exptl',[])); row['method']=methods
  if methods and not any(x in methods for x in ['X-RAY DIFFRACTION','ELECTRON MICROSCOPY']):row['reason']='method';rows.append(row);continue
  rr=j.get('rcsb_entry_info',{}).get('resolution_combined') or []; resolution=min(rr) if rr else 99; row['resolution']=resolution
  if resolution>3.5:row['reason']='resolution';rows.append(row);continue
  cp=raw/f'{pid}.cif'; r=get(f'https://files.rcsb.org/download/{pid}.cif',cp)
  if not r.ok:row['reason']=f'cif_http_{r.status_code}';rows.append(row);continue
  st=MMCIFParser(QUIET=True).get_structure(pid,str(cp)); model=next(st.get_models())
  chains=[]
  for ch in model:
   aa=[x for x in ch if is_aa(x,standard=True)]
   if 60<=len(aa)<=1200: chains.append((len(aa),ch,aa))
  if not chains:row['reason']='no_chain_length_gate';rows.append(row);continue
  chains.sort(key=lambda x:(-x[0],x[1].id)); _,ch,aa=chains[0]; row['chain']=ch.id;row['resolved_residues']=len(aa)
  ligs=[]
  for c in model:
   for q in c:
    if q.id[0]==' ' or is_aa(q,standard=True) or q.resname.strip() in exclude:continue
    atoms=[a for a in q.get_atoms() if a.element!='H']
    if len(atoms)<6:continue
    near=[]
    for x in aa:
     d=min((a-b) for a in x.get_atoms() if a.element!='H' for b in atoms)
     if d<=5.0:near.append((x,d))
    if len(near)>=3:ligs.append((len(atoms),len(near),q,near,c.id))
  if not ligs:row['reason']='no_eligible_ligand';rows.append(row);continue
  ligs.sort(key=lambda z:(-z[0],-z[1],z[2].resname)); ha,np,q,near,lch=ligs[0]
  row.update({'decision':'accept','reason':'','ligand':q.resname.strip(),'ligand_chain':lch,'ligand_seq':q.id[1],'ligand_heavy_atoms':ha,'positive_residues':np})
  # UniProt mapping: entry graphql API, source URL retained; mapping absence rejects.
  gu=f'https://data.rcsb.org/rest/v1/core/polymer_entity/{pid}/1'; gp=raw/f'{pid}.polymer1.json'; gr=get(gu,gp)
  uj=gr.json() if gr.ok else {}; refs=uj.get('rcsb_polymer_entity_container_identifiers',{}).get('reference_sequence_identifiers') or []
  unis=[x.get('database_accession') for x in refs if x.get('database_name')=='UniProt']
  row['uniprot']=';'.join(x for x in unis if x)
  if not row['uniprot']:row['decision']='reject';row['reason']='no_uniprot_mapping';rows.append(row);continue
  amap={x.id[1]:x for x in aa}
  pos={x.id[1] for x,d in near}
  for i,x in enumerate(aa):labels.append({'pdb_id':pid,'chain':ch.id,'seq_index':i,'pdb_resseq':x.id[1],'aa3':x.resname,'label':int(x.id[1] in pos),'ligand':q.resname.strip()})
  accepted+=1;rows.append(row);print('ACCEPT',pid,title[:50],q.resname,np,len(aa))
 except Exception as e:row['reason']='exception:'+type(e).__name__+':'+str(e)[:160];rows.append(row)
fields=sorted({k for r in rows for k in r})
with (res/'screening_log.csv').open('w',newline='') as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
with (B/'data/processed/residue_labels.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(labels[0]) if labels else ['pdb_id']);w.writeheader();w.writerows(labels)
print('accepted',accepted,'screened',len(rows),'labels',len(labels))
if accepted<8:raise SystemExit('LOCKED FEASIBILITY FAILURE')
