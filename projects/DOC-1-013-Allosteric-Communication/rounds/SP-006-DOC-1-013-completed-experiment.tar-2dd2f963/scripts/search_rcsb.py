import requests,json,datetime,hashlib,pathlib
base=pathlib.Path(__file__).resolve().parents[1]
out=base/'data/raw'; out.mkdir(parents=True,exist_ok=True)
ledger=base/'provenance/http_ledger.jsonl'; ledger.parent.mkdir(exist_ok=True)
q={"query":{"type":"terminal","service":"full_text","parameters":{"value":"allosteric"}},"return_type":"entry","request_options":{"paginate":{"start":0,"rows":100}}}
u='https://search.rcsb.org/rcsbsearch/v2/query'
r=requests.post(u,json=q,timeout=60); b=r.content
rec={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'POST','url':u,'status':r.status_code,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'request_sha256':hashlib.sha256(json.dumps(q,sort_keys=True).encode()).hexdigest()}
with ledger.open('a') as f:f.write(json.dumps(rec)+'\n')
r.raise_for_status(); (out/'rcsb_search_allosteric.json').write_bytes(b)
ids=sorted(x['identifier'] for x in r.json().get('result_set',[]))
(out/'candidate_ids.txt').write_text('\n'.join(ids)+'\n')
print(len(ids),ids[:20])
