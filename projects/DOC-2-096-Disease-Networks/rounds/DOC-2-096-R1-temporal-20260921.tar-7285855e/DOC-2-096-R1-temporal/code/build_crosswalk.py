from pathlib import Path
import pandas as pd,re,collections,hashlib,json
R=Path(__file__).resolve().parents[1];raw=R/'data/raw/variant_summary.txt.gz';pat=re.compile(r'(MedGen:C\d+|OMIM:\d+|Orphanet:\d+|MONDO:MONDO:\d+)'); parent={}
def find(x):
 parent.setdefault(x,x)
 if parent[x]!=x:parent[x]=find(parent[x])
 return parent[x]
def union(a,b):
 a=find(a);b=find(b)
 if a!=b:parent[b]=a
for ch in pd.read_csv(raw,sep='\t',usecols=['PhenotypeIDS'],dtype=str,chunksize=250000):
 for s in ch.PhenotypeIDS.dropna():
  # split phenotype slots; only co-link within comma-delimited same slot, never ||
  for slot in s.split('||'):
   ids=pat.findall(slot)
   for x in ids[1:]:union(ids[0],x)
comps=collections.defaultdict(set)
for x in parent:comps[find(x)].add(x)
rows=[];amb=0
for root,ids in comps.items():
 cnt=collections.Counter(x.split(':')[0] for x in ids); ambiguous=any(v>1 for v in cnt.values());amb+=ambiguous
 canon=sorted(ids)[0] if not ambiguous else ''
 for x in ids:rows.append({'identifier':x,'component':root,'canonical':canon,'ambiguous':ambiguous,'component_size':len(ids)})
x=pd.DataFrame(rows);x.to_csv(R/'data/processed/condition_crosswalk.csv',index=False)
a={'identifiers':len(x),'components':len(comps),'ambiguous_components':amb,'mapped_identifiers':int(x.canonical.ne('').sum())};(R/'results/crosswalk_audit.json').write_text(json.dumps(a,indent=2));print(a)
