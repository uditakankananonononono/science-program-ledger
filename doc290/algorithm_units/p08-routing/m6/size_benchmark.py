"""Explicit copied DEV payload storage/revalidation benchmark, not corpus timing."""
import json,copy,sys,time
from pathlib import Path
from core import gate,launch,validate_record
from durable import transact,finalize,encoded
from controller import synthesize,context
RUN=Path('/tmp/m6-repaired-size-benchmark');STATE=Path('/tmp/m6-repaired-benchmark-data.json')
mode=sys.argv[1]
if mode=='init':
    identity=gate();bases={m:launch(['devsubject',0,m]) for m in ('variant','t8')};assert all(r['status']=='PASS' for r in bases.values());data={'identity':identity,'bases':bases,'chunks':[]};STATE.write_text(json.dumps(data))
data=json.loads(STATE.read_text());identity=data['identity'];bases=data['bases'];plan=json.loads(Path('plan.json').read_text());classes=json.loads(Path('classes.json').read_text())
def val(e,r):
    expected=validate_record(['devsubject',0,e['method']],r,validated_identity=identity)
    if encoded(expected)!=encoded(r):raise ValueError('canonical benchmark receipt mismatch')
if mode in ('init','chunks'):
    for _ in range(10):data['chunks'].append(transact(RUN,plan,identity,val,lambda e:copy.deepcopy(bases[e['method']])))
    STATE.write_text(json.dumps(data));print(data['chunks'][-1]);print('max',max(c['elapsed'] for c in data['chunks']))
elif mode=='final':
    a=finalize(RUN,plan,identity,val,lambda p,rs:synthesize(p,rs,classes));before=(RUN/'report.json').read_bytes();b=finalize(RUN,plan,identity,val,lambda p,rs:synthesize(p,rs,classes));assert before==(RUN/'report.json').read_bytes();start=time.monotonic();context();setup=time.monotonic()-start
    result={'scope':'postcanonicalrepair synthetic sizebenchmark/copied real DEV fullpayloads, NOcorpusmethods orspeedobservations','chunks':data['chunks'],'max_chunk_seconds':max(c['elapsed'] for c in data['chunks']),'final_synthesis_seconds':a['elapsed'],'repeat_synthesis_seconds':b['elapsed'],'context_seconds':setup,'report_bytes_unchanged':True,'receipt_policy':'canonical checked/fullpayload typeexact, allstored receipts revalidated; singleinvocation sourcegate only'}
    Path('repaired-size-evidence.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='chunks'})
