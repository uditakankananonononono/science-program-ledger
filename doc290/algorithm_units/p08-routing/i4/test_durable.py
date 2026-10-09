import unittest,tempfile,subprocess,sys,time,json,hashlib,os
from pathlib import Path
from durable import read,atomic
ROOT=Path(__file__).resolve().parent
class RealDurability(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def invoke(self,path,point='none',limit=40):
        return subprocess.run([sys.executable,str(ROOT/'dev_driver.py'),str(path),point,str(limit)],capture_output=True,text=True,timeout=15)
    def kill_at(self,path,point,limit=40):
        p=subprocess.Popen([sys.executable,str(ROOT/'dev_driver.py'),str(path),point,str(limit)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        mark=path.with_name(path.name+'-ready');end=time.monotonic()+10
        while not mark.exists() and time.monotonic()<end:time.sleep(.01)
        self.assertTrue(mark.exists());p.kill();p.communicate(timeout=5);self.assertEqual(p.returncode,-9)
    def counts(self,path):return [int(x) for x in path.with_name(path.name+'-launches.txt').read_text().splitlines()]
    def test_real_crash_matrix_reconcile_no_duplicate(self):
        evidence={}
        for point in ('receipt','ledger','clear','pair'):
            path=self.base/point;self.kill_at(path,point);before={p.name:p.read_bytes() for p in path.glob('receipt-*')};r=self.invoke(path);self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(self.counts(path),list(range(4)))
            self.assertTrue(all((path/k).read_bytes()==v for k,v in before.items()));self.assertEqual(self.invoke(path,'finalize').returncode,0);self.assertEqual(self.invoke(path).returncode,0);self.assertEqual(self.invoke(path,'finalize').returncode,0);self.assertEqual(self.counts(path),list(range(4)));evidence[point]={'receipts_unchanged':True,'launches':self.counts(path),'next':read(path/'ledger.json')['next']}
        # Kill with second receipt saved, both receipts but no pair marker.
        path=self.base/'both';self.assertEqual(self.invoke(path,limit=1).returncode,0);self.kill_at(path,'clear');before={p.name:p.read_bytes() for p in path.glob('receipt-*')};self.assertFalse((path/'pair-0000.json').exists());self.assertEqual(self.invoke(path).returncode,0);self.assertTrue(all((path/k).read_bytes()==v for k,v in before.items()));self.assertEqual(self.counts(path),list(range(4)));evidence['both_before_pair']={'launches':self.counts(path),'receipts_unchanged':True}
        Path('/tmp/m6-durability-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    def test_unreceipted_uncertainty_locks_and_death_releases(self):
        path=self.base/'missing';self.kill_at(path,'inflight');self.assertEqual(len(list(path.glob('receipt-*'))),0);r=self.invoke(path);self.assertNotEqual(r.returncode,0);self.assertTrue((path/'FAIL.json').exists());self.assertNotEqual(self.invoke(path).returncode,0);self.assertFalse(path.with_name(path.name+'-launches.txt').exists())
    def test_concurrent_refusal_partial_and_guard(self):
        path=self.base/'concurrent';p=subprocess.Popen([sys.executable,str(ROOT/'dev_driver.py'),str(path),'receipt'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);mark=path.with_name(path.name+'-ready');end=time.monotonic()+10
        while not mark.exists() and time.monotonic()<end:time.sleep(.01)
        self.assertTrue(mark.exists());r=self.invoke(path);self.assertNotEqual(r.returncode,0);self.assertFalse((path/'FAIL.json').exists());p.kill();p.communicate();self.assertEqual(self.invoke(path).returncode,0);self.assertEqual(self.counts(path),list(range(4)))
        path=self.base/'partial';self.assertEqual(self.invoke(path,limit=1).returncode,0);self.assertFalse((path/'pair-0000.json').exists());self.assertEqual(self.invoke(path).returncode,0);self.assertEqual(self.counts(path),list(range(4)))
        path=self.base/'guard';r=self.invoke(path,'guard');self.assertEqual(r.returncode,0);data=json.loads(r.stdout);self.assertEqual(data['launched'],0);self.assertLess(data['elapsed'],1)
    def test_corruption_foreign_identity_plan_coverage(self):
        for what in ('truncated','ledger','identity','entry','gap','pair','foreign','runplan','receiptresult','straytemp','boolentry'):
            path=self.base/what;self.assertEqual(self.invoke(path).returncode,0)
            if what=='truncated':(path/'receipt-0000.json').write_text('{')
            if what=='ledger':atomic(path/'ledger.json',{'next':True})
            if what=='identity':r=read(path/'receipt-0000.json');r['identity']={};atomic(path/'receipt-0000.json',r)
            if what=='entry':r=read(path/'receipt-0000.json');r['entry']['number']=9;atomic(path/'receipt-0000.json',r)
            if what=='gap':(path/'receipt-0000.json').unlink()
            if what=='pair':atomic(path/'pair-0000.json',{'pair':0,'receipt_sha256':[]})
            if what=='foreign':(path/'foreign.json').write_text('{}')
            if what=='runplan':r=read(path/'run.json');r['plan_sha256']='wrong';atomic(path/'run.json',r)
            if what=='receiptresult':r=read(path/'receipt-0000.json');r['result']['value']=999;atomic(path/'receipt-0000.json',r)
            if what=='straytemp':(path/'.foreign.tmp').write_text('{}')
            if what=='boolentry':r=read(path/'receipt-0001.json');r['entry']['number']=True;atomic(path/'receipt-0001.json',r)
            before=self.counts(path);self.assertNotEqual(self.invoke(path).returncode,0);self.assertNotEqual(self.invoke(path).returncode,0);self.assertEqual(self.counts(path),before);self.assertTrue((path/'FAIL.json').exists())

    def test_final_synthesis_interruption_idempotent(self):
        path=self.base/'final';self.assertEqual(self.invoke(path).returncode,0);self.kill_at(path,'finalreport');raw=(path/'report.json').read_bytes();self.assertFalse((path/'DONE.json').exists());self.assertEqual(self.invoke(path,'finalize').returncode,0);self.assertEqual(self.invoke(path,'finalize').returncode,0);self.assertEqual(raw,(path/'report.json').read_bytes());self.assertEqual(self.counts(path),list(range(4)))
