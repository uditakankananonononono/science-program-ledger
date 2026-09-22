import requests,pathlib,hashlib,json,datetime,urllib.parse,time
B=pathlib.Path(__file__).resolve().parents[1]; raw=B/'data/raw'; led=B/'provenance/http_ledger.jsonl'
base='https://rest.uniprot.org/uniprotkb/stream'
phr=['Alzheimer','Parkinson','Huntington','amyotrophic lateral sclerosis','frontotemporal dementia','prion disease','spinocerebellar ataxia','neurodegeneration','neurodegenerative']
common='reviewed:true AND organism_id:9606 AND length:[50 TO 1200]'
pos=common+' AND ('+' OR '.join('cc_disease:"'+p+'"' for p in phr)+')'
neg=common+' NOT cc_disease:*'
fields='accession,id,protein_name,length,sequence,cc_disease'
def get(label,q):
 u=base+'?'+urllib.parse.urlencode({'query':q,'format':'tsv','fields':fields,'compressed':'false'})
 for a in range(2):
  r=requests.get(u,timeout=120);b=r.content
  with led.open('a') as f:f.write(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'GET','url':u,'status':r.status_code,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'attempt':a+1})+'\n')
  if r.ok:break
  time.sleep(2)
 r.raise_for_status();(raw/f'uniprot_{label}.tsv').write_bytes(b);print(label,len(b),len(b.splitlines())-1)
get('positive_candidates',pos);get('negative_candidates',neg)
(B/'provenance/query_definition.json').write_text(json.dumps({'positive':pos,'negative':neg,'phrases':phr,'fields':fields},indent=2)+'\n')
