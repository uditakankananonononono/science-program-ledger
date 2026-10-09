import unittest,itertools,copy,json
from pathlib import Path
from core import family,oracle,witness,Invalid,launch,gate,ROOT
class Development(unittest.TestCase):
    def route(self,n,choices,method):
        X=sum(2**i for i,c in enumerate(choices) if c==0);S=2**n-1
        r={'path':[f'v{i}' for i in range(n+1)],'edges':[{'source':f'v{i}','edge_index':c,'target':f'v{i+1}'} for i,c in enumerate(choices)],'scenario_totals':[X,S-X],'worst_time':max(X,S-X)}
        if method=='budget-scenario':r['exposure']=X
        return r
    def test_bijection_frontier_and_oracle(self):
        for n in (1,2,3):
            rows=[self.route(n,c,'scenario') for c in itertools.product((0,1),repeat=n)];X=[r['scenario_totals'][0] for r in rows];self.assertEqual(sorted(X),list(range(2**n)))
            for a,b in itertools.combinations(rows,2):self.assertFalse(all(x<=y for x,y in zip(a['scenario_totals'],b['scenario_totals'])))
            self.assertEqual(min(r['worst_time'] for r in rows),oracle(n,'scenario')['worst'])
            for r in rows:
                if r['worst_time']==oracle(n,'scenario')['worst']:self.assertEqual(witness(n,'scenario',r)['status'],'PASS')
            if n>=2:
                O=oracle(n,'budget-scenario');rs=[self.route(n,c,'budget-scenario') for c in itertools.product((0,1),repeat=n)];self.assertEqual(min(r['worst_time'] for r in rs if r['exposure']<=O['budget']),O['worst'])
    def test_witness_mutations_and_disagreement(self):
        r=self.route(3,[0,0,1],'scenario');self.assertEqual(witness(3,'scenario',r)['status'],'PASS')
        for key,value in (('worst_time',True),('worst_time',0),('scenario_totals',[True,4]),('scenario_totals',[4,3]),('path',['v0','v3'])):
            rr=copy.deepcopy(r);rr[key]=value
            with self.assertRaises(Invalid):witness(3,'scenario',rr)
        rr=copy.deepcopy(r);rr['edges'][0]['edge_index']=True
        with self.assertRaises(Invalid):witness(3,'scenario',rr)
        rr=copy.deepcopy(r);rr['exposure']=3
        with self.assertRaises(Invalid):witness(3,'scenario',rr)
        rr=self.route(3,[0,0,1],'budget-scenario')
        with self.assertRaises(Invalid):witness(3,'budget-scenario',rr)
    def test_input_domain(self):
        for n in (True,1.0,0,11):
            with self.assertRaises(Invalid):family(n)
        with self.assertRaises(Invalid):oracle(3,'other')
    def test_real_sleep_kill_reap(self):
        r=launch(['sleep'],timeout=.3);self.assertEqual(r['status'],'FAIL');self.assertTrue(r['timed_out']);self.assertTrue(r['kill_sent']);self.assertTrue(r['reaped']);self.assertEqual(r['returncode'],-9);self.assertEqual(r['stdout'],'sleep-ready\n');(ROOT/'sleep-control.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    def test_actual_cap_gate_and_parse_failures(self):
        rows={m:launch([m]) for m in ('memory','gatefail','badjson')}
        for r in rows.values():self.assertEqual(r['status'],'FAIL');self.assertTrue(r['reaped']);self.assertFalse(r['timed_out'])
        self.assertIn('MemoryError',rows['memory']['stdout']);self.assertIn('intentional gate refusal',rows['gatefail']['stdout']);self.assertEqual(rows['badjson']['returncode'],0);self.assertIn('JSONDecodeError',rows['badjson']['reason']);(ROOT/'failure-controls.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
    def test_source_gate_disagree(self):
        self.assertEqual(set(gate()),{'manifest_sha256','runtime_sha256'})
        import unittest.mock
        with unittest.mock.patch('core.hashlib.sha256') as h:
            h.return_value.hexdigest.return_value='bad'
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
