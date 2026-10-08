import copy,json,subprocess,sys,unittest
from runner import solve

BASE={'method':'integrated','start':'a','goal':'c','budget':2,'graph':{
'a':[{'target':'b','time':1,'exposure':1,'scenario_times':[2,1]}],
'b':[{'target':'c','time':1,'exposure':1,'scenario_times':[1,2]}],'c':[]}}

class RunnerTests(unittest.TestCase):
    def invoke(self,text):
        return subprocess.run([sys.executable,'runner.py','-'],input=text,text=True,capture_output=True)
    def test_five_methods(self):
        for method in ('budget','scenario','budget-scenario','turn','integrated'):
            p=copy.deepcopy(BASE);p['method']=method
            if method in ('scenario','turn'):p.pop('budget')
            got=solve(p)
            self.assertEqual(got['status'],'ok');self.assertEqual(got['result']['path'],['a','b','c'])
    def test_subprocess_result_and_failure(self):
        got=self.invoke(json.dumps(BASE));self.assertEqual(got.returncode,0)
        self.assertEqual(json.loads(got.stdout)['result']['worst_time'],3)
        p=copy.deepcopy(BASE);p['budget']=1
        got=self.invoke(json.dumps(p));self.assertEqual(got.returncode,0)
        self.assertEqual(json.loads(got.stdout)['status'],'infeasible')
    def test_duplicate_keys_and_constants(self):
        for raw in ('{"method":"budget","method":"turn"}','{"x":NaN}','{"x":Infinity}','{'):
            got=self.invoke(raw);self.assertEqual(got.returncode,2);self.assertEqual(got.stdout,'')
            self.assertEqual(json.loads(got.stderr)['status'],'error')
    def test_strict_fields_and_rules(self):
        for mutate in (lambda p:p.update(extra=1),lambda p:p.pop('budget'),
                       lambda p:p.update(forbidden=[[["a",True],["b",0]]]),
                       lambda p:p.update(penalties=[{'incoming':['a',0],'outgoing':['b',0],'delay':-1}]),
                       lambda p:p.update(graph=[])):
            p=copy.deepcopy(BASE);mutate(p)
            with self.assertRaises((ValueError,TypeError)):solve(p)
    def test_turn_delay_and_forbidden(self):
        p=copy.deepcopy(BASE);p['penalties']=[{'incoming':['a',0],'outgoing':['b',0],'delay':4}]
        self.assertEqual(solve(p)['result']['worst_time'],7)
        p['forbidden']=[[['a',0],['b',0]]]
        self.assertEqual(solve(p)['status'],'infeasible')
    def test_no_silent_ignored_parameters(self):
        p=copy.deepcopy(BASE);p['method']='scenario'
        with self.assertRaises(ValueError):solve(p)
        p.pop('budget');p['forbidden']=[]
        with self.assertRaises(ValueError):solve(p)
