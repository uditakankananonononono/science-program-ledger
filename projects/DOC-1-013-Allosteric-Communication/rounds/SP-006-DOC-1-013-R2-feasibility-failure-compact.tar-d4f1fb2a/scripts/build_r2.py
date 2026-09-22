import pandas as pd,numpy as np,requests,pathlib,ast,re,csv,json,hashlib,datetime,time,resource
from Bio.PDB import MMCIFParser
from Bio.PDB.Polypeptide import is_aa
import networkx as nx
B=pathlib.Path(__file__).resolve().parents[1];raw=B/'data/raw';res=B/'results';proc=B/'data/processed';t0=time.time()
r0p=set('1C50 1FRZ 1H78 1H79 1H7A 1LLC 1LTH 1PZO 1PZP 1XJF 1XJG 1XJJ 1XJK 1XJM 1XJN'.split());r0u=set('P00489 P0A759 P07071 P00343 E8ME30 P62593 O33839'.split())
d=pd.read_csv(raw/'AlloBench.csv').sort_values(['target_id','allosteric_pdb']);rows=[];labs=[];seen=set();accepted=0
AA={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
def fetch(pid):
 p=raw/f'{pid}.cif';u=f'https://files.rcsb.org/download/{pid}.cif'
 if not p.exists():
  r=requests.get(u,timeout=60);b=r.content
  with (B/'provenance/http_ledger.jsonl').open('a') as f:f.write(json.dumps({'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':u,'status':r.status_code,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})+'\n')
  if not r.ok:return None
  p.write_bytes(b)
 return p
for tid,g in d.groupby('target_id',sort=True):
 if accepted>=40:break
 if tid in seen:continue
 for _,z in g.iterrows():
  pid=str(z.allosteric_pdb).upper();uni=str(z.pdb_uniprot)
  if pid in r0p or uni in r0u:rows.append({'target_id':tid,'pdb_id':pid,'decision':'reject','reason':'R0_overlap'});continue
  try:
   aset=ast.literal_eval(str(z.allosteric_site_residue));act=ast.literal_eval(str(z.active_site_residue));rawsites=[str(x) for x in aset]; prefixes=[x.split('-')[0] for x in rawsites if '-' in x]; chain=max(set(prefixes),key=prefixes.count) if prefixes else str(z.modulator_chain).strip()
   asetn={int(re.search(r'(-?\d+)$',str(x)).group(1)) for x in aset if str(x).startswith(chain+'-') and re.search(r'(-?\d+)$',str(x))}
   actn={int(x) for x in act};p=(raw/f'{pid}.cif') if (raw/f'{pid}.cif').exists() else None
   if not p:raise ValueError('fetch')
   st=MMCIFParser(QUIET=True).get_structure(pid,str(p));model=next(st.get_models());ch=model[chain];aa=[x for x in ch if is_aa(x,standard=True) and x.resname in AA]
   amap={x.id[1]:x for x in aa};pos=set(amap)&asetn;active=set(amap)&actn
   if len(active)<3:
    active=set(list(amap)[max(0,i-1)] for i in actn if 1<=i<=len(amap))
   if not 60<=len(aa)<=1200 or len(pos)<3 or len(active)<3:raise ValueError('gate')
   G=nx.Graph();coords=[]
   for i,x in enumerate(aa):G.add_node(i);coords.append(x['CA'].coord if 'CA' in x else np.mean([a.coord for a in x],0))
   C=np.array(coords);D=((C[:,None]-C[None])**2).sum(2);ii,jj=np.where((D<=64)&(D>0));G.add_edges_from(zip(ii.tolist(),jj.tolist()))
   idx={x.id[1]:i for i,x in enumerate(aa)};pidx={idx[x] for x in pos};aidx={idx[x] for x in active};buffer=set(pidx)
   for x in list(pidx):buffer|=set(nx.single_source_shortest_path_length(G,x,cutoff=2))
   neg=[i for i in range(len(aa)) if i not in buffer and i not in aidx]
   if len(neg)<30:raise ValueError('negatives')
   corridor=set()
   for a in pidx:
    for b in aidx:
     try:corridor|=set(nx.shortest_path(G,a,b)[1:-1])
     except:pass
   cen=nx.betweenness_centrality(G,k=min(5,len(G)),seed=130132);close=nx.closeness_centrality(G);clust=nx.clustering(G);cent=C.mean(0)
   seq=''.join(AA[x.resname] for x in aa)
   for i,x in enumerate(aa):
    if i not in pidx and i not in neg:continue
    labs.append({'target_id':tid,'pdb_id':pid,'uniprot':uni,'chain':chain,'i':i,'resseq':x.id[1],'aa':AA[x.resname],'label':int(i in pidx),'corridor':int(i in corridor),'active':int(i in aidx),'degree':G.degree(i),'closeness':close[i],'betweenness':cen[i],'clustering':clust[i],'centroid_distance':float(np.linalg.norm(C[i]-cent)),'relative_position':i/max(1,len(aa)-1),'sequence':seq})
   rows.append({'target_id':tid,'pdb_id':pid,'uniprot':uni,'decision':'accept','n':len(aa),'positives':len(pos),'active':len(active),'corridor':len(corridor)});accepted+=1;seen.add(tid);print('A',accepted,tid,pid,len(aa),len(pos));break
  except Exception as e:rows.append({'target_id':tid,'pdb_id':pid,'decision':'reject','reason':str(e)[:100]})
pd.DataFrame(rows).to_csv(res/'screening_log.csv',index=False);pd.DataFrame(labs).to_csv(proc/'residues.csv',index=False)
with (B/'provenance/compute_ledger.jsonl').open('a') as f:f.write(json.dumps({'stage':'build_r2','wall_seconds':time.time()-t0,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'accepted':accepted,'residue_rows':len(labs)})+'\n')
print('DONE',accepted,len(labs))
if accepted<30:raise SystemExit('FEASIBILITY FAILURE')
