"""Durable ordered execution. POSIX flock covers recovery, calls and synthesis."""
import os,json,time,fcntl,hashlib
from pathlib import Path
class LockedFailure(RuntimeError):pass
class Busy(RuntimeError):pass

def encoded(x):return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
def digest(x):return hashlib.sha256(encoded(x)).hexdigest()
def atomic(path,data,immutable=False):
    path=Path(path);raw=encoded(data)
    if path.exists():
        if immutable:
            if path.read_bytes()!=raw:raise LockedFailure('immutable conflict '+path.name)
            return
    tmp=path.with_name('.'+path.name+'.tmp')
    with open(tmp,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
    fd=os.open(path.parent,os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def read(path):return json.loads(Path(path).read_text())

def transact(run,plan,identity,validate,execute,limit=40,ceiling=60,headroom=7,hook=None,finish=None,finalize_only=False,started=None):
    begin=time.monotonic() if started is None else started;run=Path(run);run.mkdir(parents=True,exist_ok=True)
    lock=open(run/'LOCK','a+b')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:lock.close();raise Busy('run busy')
    call=lambda point:hook(point) if hook else None
    try:
        if (run/'FAIL.json').exists():raise LockedFailure('durable FAIL sentinel')
        if len(plan)%2 or any(type(e) is not dict for e in plan):raise LockedFailure('plan structure')
        expected={'identity':identity,'plan_sha256':digest(plan),'slots':len(plan)}
        allowed={'LOCK','run.json','ledger.json','inflight.json','DONE.json','report.json','chunk-history.json','FAIL.json'}
        for path in run.iterdir():
            if path.name not in allowed and not (path.name.startswith('receipt-') or path.name.startswith('pair-') or (path.name.startswith('.') and path.name.endswith('.tmp'))):raise LockedFailure('foreign run file')
        # An interrupted atomic replacement temp is never promoted or trusted.
        # Allowed only for exact known mutable/receipt names, and ignored as uncommitted bytes.
        for path in run.glob('.*.tmp'):
            target=path.name[1:-4]
            if target not in allowed and not (target.startswith('receipt-') and target.endswith('.json')) and not (target.startswith('pair-') and target.endswith('.json')):raise LockedFailure('foreign temp file')
        if not (run/'run.json').exists():
            if any(p.name!='LOCK' for p in run.iterdir()):raise LockedFailure('uninitialized foreign run')
            atomic(run/'run.json',expected,True);atomic(run/'ledger.json',{'next':0})
        if encoded(read(run/'run.json'))!=encoded(expected):raise LockedFailure('run/source/plan mismatch')
        ledger=read(run/'ledger.json')
        if type(ledger) is not dict or set(ledger)!={'next'} or type(ledger['next']) is not int or not 0<=ledger['next']<=len(plan):raise LockedFailure('ledger schema')
        index=ledger['next'];stored={}
        for path in sorted(run.glob('receipt-*.json')):
            receipt=read(path)
            if type(receipt) is not dict or set(receipt)!={'slot','entry','identity','result'} or type(receipt['slot']) is not int:raise LockedFailure('receipt schema')
            slot=receipt['slot']
            if not 0<=slot<len(plan) or path.name!=f'receipt-{slot:04}.json' or slot in stored or encoded(receipt['entry'])!=encoded(plan[slot]) or encoded(receipt['identity'])!=encoded(identity):raise LockedFailure('receipt slot/order/input/source')
            validate(plan[slot],receipt['result']);stored[slot]=receipt
        prefix=len(stored)
        if set(stored)!=set(range(prefix)):raise LockedFailure('receipt gap')
        inflight=read(run/'inflight.json') if (run/'inflight.json').exists() else None
        if inflight is not None:
            if type(inflight) is not dict or set(inflight)!={'slot','entry','identity'} or type(inflight['slot']) is not int:raise LockedFailure('inflight schema')
            slot=inflight['slot']
            if not 0<=slot<len(plan) or encoded(inflight['entry'])!=encoded(plan[slot]) or encoded(inflight['identity'])!=encoded(identity):raise LockedFailure('inflight binding')
            if slot not in stored:raise LockedFailure('inflight unreceipted subject uncertainty')
            if slot!=prefix-1 or index not in (slot,slot+1):raise LockedFailure('inflight/ledger transition')
        elif index!=prefix:raise LockedFailure('ledger/receipt mismatch without inflight')
        if inflight is not None:
            atomic(run/'ledger.json',{'next':prefix});atomic(run/'inflight.json',None);index=prefix
        # Pair markers reconstructed only from both complete, validated immutable receipts.
        for path in run.glob('pair-*.json'):
            marker=read(path);pair=marker.get('pair') if type(marker) is dict else None
            if type(pair) is not int or path.name!=f'pair-{pair:04}.json' or 2*pair+1>=prefix:raise LockedFailure('pair marker missing subjects')
            expected_marker={'pair':pair,'receipt_sha256':[digest(stored[2*pair]),digest(stored[2*pair+1])]}
            if marker!=expected_marker:raise LockedFailure('pair marker binding')
        for pair in range(prefix//2):atomic(run/f'pair-{pair:04}.json',{'pair':pair,'receipt_sha256':[digest(stored[2*pair]),digest(stored[2*pair+1])]},True)
        if (run/'DONE.json').exists():
            if index!=len(plan) or read(run/'DONE.json')!={'slots':len(plan),'plan_sha256':digest(plan)}:raise LockedFailure('false completion')
            if finish:finish(run,[stored[k] for k in range(prefix)])
            return {'state':'DONE','next':index,'launched':0,'elapsed':time.monotonic()-begin}
        if finalize_only:
            if index!=len(plan):raise LockedFailure('finalize incomplete')
            if finish is None:raise LockedFailure('missing final synthesizer')
            finish(run,[stored[k] for k in range(prefix)])
            atomic(run/'DONE.json',{'slots':len(plan),'plan_sha256':digest(plan)},True)
            return {'state':'DONE','next':index,'launched':0,'elapsed':time.monotonic()-begin}
        # Budget includes setup/reconciliation; no fresh timer after validation.
        initial=index
        while index<len(plan) and index-initial<limit:
            if ceiling-(time.monotonic()-begin)<headroom:break
            entry=plan[index];atomic(run/'inflight.json',{'slot':index,'entry':entry,'identity':identity});call('inflight')
            result=execute(entry);validate(entry,result)
            receipt={'slot':index,'entry':entry,'identity':identity,'result':result};atomic(run/f'receipt-{index:04}.json',receipt,True);stored[index]=receipt;call('receipt')
            index+=1;atomic(run/'ledger.json',{'next':index});call('ledger');atomic(run/'inflight.json',None);call('clear')
            if index%2==0:
                pair=index//2-1;atomic(run/f'pair-{pair:04}.json',{'pair':pair,'receipt_sha256':[digest(stored[index-2]),digest(stored[index-1])]},True);call('pair')
        # Synthesis has a separate invocation, never squeezed into launch budget.
        elapsed=time.monotonic()-begin;history=read(run/'chunk-history.json') if (run/'chunk-history.json').exists() else []
        history.append({'from':initial,'next':index,'launched':index-initial,'elapsed':elapsed,'ceiling':ceiling,'headroom':headroom});atomic(run/'chunk-history.json',history)
        return {'state':'READY_FINAL' if index==len(plan) else 'OPEN','next':index,'launched':index-initial,'elapsed':elapsed}
    except Busy:raise
    except Exception as e:
        if not (run/'FAIL.json').exists():atomic(run/'FAIL.json',{'status':'LOCKED_CONTROLLER_FAILURE','exception_type':type(e).__name__,'reason':str(e)})
        raise
    finally:lock.close()

def finalize(run,plan,identity,validate,finish,started=None):
    return transact(run,plan,identity,validate,lambda e:None,limit=0,finish=finish,finalize_only=True,started=started)
