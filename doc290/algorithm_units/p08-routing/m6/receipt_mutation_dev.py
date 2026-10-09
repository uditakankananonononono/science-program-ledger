"""Real persisted checked-receipt mutations using non-corpus worker only."""
import json,tempfile,copy
from pathlib import Path
import controller
from controller import validate
from core import launch,gate,validate_record
from durable import transact,read,atomic,encoded

def run():
    identity=gate();controller.VALIDATED_IDENTITY=identity
    base=launch(['devsubject',0,'variant']);assert base['status']=='PASS'
    # Stored dev receipt validation follows original parser with dev input,
    # canonical result binding is identical to production controller.validate.
    def checked(e,r):
        expected=validate_record(['devsubject',0,e['method']],r,validated_identity=identity)
        if encoded(expected)!=encoded(r):raise ValueError('canonical checked receipt mismatch')
    results=[]
    for target in ('counter_bool','rss_float','check_float','check_bool'):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'run';plan=[{'method':'variant','slot':k} for k in range(4)];launches=[]
            def execute(e):launches.append(e['slot']);return copy.deepcopy(base)
            transact(path,plan,identity,checked,execute,limit=2)
            receipt=read(path/'receipt-0000.json');stdout=receipt['result']['stdout'];r=receipt['result']
            if target=='counter_bool':
                for k,v in r['worker']['counters'].items():
                    if v==0:r['worker']['counters'][k]=False;break
            elif target=='rss_float':r['worker']['rss_kib']=float(r['worker']['rss_kib'])
            elif target=='check_float':r['check']['worst_time']=float(r['check']['worst_time'])
            elif target=='check_bool':r['check']['exposure']=False
            assert r['stdout']==stdout
            atomic(path/'receipt-0000.json',receipt)
            failed=False
            try:transact(path,plan,identity,checked,execute)
            except Exception:failed=True
            assert failed and (path/'FAIL.json').exists() and launches==[0,1]
            try:transact(path,plan,identity,checked,execute)
            except Exception:pass
            assert launches==[0,1]
            results.append({'mutation':target,'stdout_unchanged':True,'durable_FAIL':True,'no_new_launches':True})
    return results
if __name__=='__main__':
    Path('/tmp/m6-persisted-mutations.json').write_text(json.dumps(run(),indent=2)+'\n')
