import copy,json,subprocess,sys,unittest
from mask_runner import solve_mask

BASE={'mask':[[1,1,1]],'connectivity':4,'costs':{'time':1,'exposure':1,'scenario_times':[1,2]},
      'query':{'method':'integrated','start':'0,0','goal':'0,2','budget':2}}

class MaskRunnerTests(unittest.TestCase):
    def invoke(self,text):
        return subprocess.run([sys.executable,'mask_runner.py','-'],input=text,text=True,capture_output=True)
    def assert_error(self,proc):
        self.assertEqual(proc.returncode,2);self.assertEqual(proc.stdout,'')
        self.assertEqual(json.loads(proc.stderr)['status'],'error');self.assertNotIn('Traceback',proc.stderr)
    def test_actual_chain_subprocess(self):
        out=self.invoke(json.dumps(BASE));self.assertEqual(out.returncode,0)
        got=json.loads(out.stdout)
        self.assertEqual(got['result']['scenario_totals'],[2,4])
        self.assertEqual(got['topology']['directed_edges'],4)
        self.assertFalse(got['topology']['diagonal_cost_correction'])
    def test_empty_foreground_boundary(self):
        p=copy.deepcopy(BASE);p['mask']=[[0]]
        self.assert_error(self.invoke(json.dumps(p)))
    def test_isolated_scenario_boundary_and_scalar_identity(self):
        p=copy.deepcopy(BASE);p['mask']=[[1]];p['query']['goal']='0,0'
        self.assert_error(self.invoke(json.dumps(p)))
        p['query']['method']='budget'
        got=solve_mask(p)
        self.assertEqual(got['result']['path'],['0,0'])
        self.assertEqual(got['result']['time'],0)
    def test_diagonal_and_disconnected(self):
        p=copy.deepcopy(BASE);p['mask']=[[1,0],[0,1]];p['query']['goal']='1,1'
        self.assert_error(self.invoke(json.dumps(p))) # all-isolated scenario boundary
        p['query']['method']='budget'
        self.assertEqual(solve_mask(p)['status'],'infeasible')
        p['query']['method']='integrated'
        p['connectivity']=8
        got=solve_mask(p);self.assertEqual(got['result']['scenario_totals'],[1,2])
    def test_schema_decoder_and_bool_failures(self):
        for raw in ('['*1500+'0'+']'*1500,'{"x":NaN}','{"mask":[],"mask":[]}'):
            self.assert_error(self.invoke(raw))
        for mutate in (lambda p:p.update(connectivity=True),lambda p:p.update(extra=1),
                       lambda p:p['costs'].update(scenario_times=1),lambda p:p.update(mask=[[True]]),
                       lambda p:p['query'].update(graph={})):
            p=copy.deepcopy(BASE);mutate(p);self.assert_error(self.invoke(json.dumps(p)))
