import pandas as pd,requests,pathlib,hashlib,json,datetime
B=pathlib.Path(__file__).resolve().parents[1]; x=pd.read_csv(B/'results/screening_log.csv'); acc=sorted(set(';'.join(x[x.decision=='accept'].uniprot.dropna()).split(';')))
for a in acc:
 u=f'https://rest.uniprot.org/uniprotkb/{a}.json';r=requests.get(u,timeout=60);b=r.content
 with (B/'provenance/http_ledger.jsonl').open('a') as f:f.write(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'GET','url':u,'status':r.status_code,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})+'\n')
 r.raise_for_status();(B/f'data/raw/uniprot_{a}.json').write_bytes(b)
print(acc)
