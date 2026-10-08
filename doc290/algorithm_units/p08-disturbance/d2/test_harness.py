import unittest,sys,importlib.util
from pathlib import Path
from fractions import Fraction as F
from harness import run,HoldP,PredictP,HoldSign,PredictSign
from compare import pair
spec=importlib.util.spec_from_file_location('d1',Path(__file__).resolve().parent.parent/'d1/harness.py');d1=importlib.util.module_from_spec(spec);spec.loader.exec_module(d1)
def case(n):return {'gain':[F(1)]*n,'drift':[F(0)]*n,'observed':[True]*n,'immobilized':[False]*n}
class BadEstimate:
    def action(self,*args):return (True,F(0))
class BadAction:
    def action(self,*args):return (F(0),float('nan'))
class Explodes:
    def action(self,*args):raise RuntimeError('not kept')
class Hangs:
    def action(self,*args):
        while True:pass
class Tests(unittest.TestCase):
    def test_literal_timing(self):
        c=case(2);c['observed'][1]=False
        a=run(HoldP,c);b=run(PredictP,c)
        self.assertEqual([r['estimate'] for r in a['records']],[0,0]);self.assertEqual([r['estimate'] for r in b['records']],[0,F(1,10)])
        self.assertEqual((a['dropout_mae'],b['dropout_mae']),(F(1,10),0))
    def test_d1_equivalence_fixture(self):
        c=case(4);c['observed'][2]=False;c['drift'][1]=F(1,2)
        for old,new in ((d1.Proportional,HoldP),(d1.Sign,HoldSign)):
            a=d1.run(old,c);b=run(new,c)
            for key in ('states','outcome','final_error','control_effort','max_boundary_overshoot'):self.assertEqual(a[key],b[key])
            self.assertEqual([r['action'] for r in a['records']],[r['action'] for r in b['records']])
    def test_causality(self):
        for policy in (HoldP,PredictP,HoldSign,PredictSign):
            a=case(4);b=case(4);a['observed']=b['observed']=[True,False,False,False];b['drift']=[F(1)]*4
            ra=run(policy,a);rb=run(policy,b)
            self.assertEqual([(r['estimate'],r['action']) for r in ra['records']],[(r['estimate'],r['action']) for r in rb['records']])
    def test_misspecification(self):
        for field,value in (('drift',F(1)),('gain',F(1,2)),('immobilized',True)):
            c=case(2);c['observed'][1]=False;c[field][0]=value
            r=run(PredictP,c);self.assertNotEqual(r['records'][1]['estimation_error'],0)
    def test_invalid_none_counts(self):
        a=run(BadEstimate,case(1));self.assertEqual(a['valid_estimate_count'],0);self.assertIsNone(a['estimation_mae'])
        b=run(BadAction,case(1));self.assertEqual(b['valid_estimate_count'],1);self.assertEqual(b['completed_steps'],0)
        self.assertIsNone(pair(a,b,1)['estimation_mae']['predict_minus_hold'])
    def test_no_dropout_not_tie(self):
        a=run(HoldP,case(1));b=run(PredictP,case(1))
        self.assertIsNone(pair(a,b,1)['dropout_mae']['predict_minus_hold']);self.assertFalse(pair(a,b,1)['dropout_mae']['comparable'])
    def test_reset(self):
        c=case(2);self.assertEqual(run(PredictP,c),run(PredictP,c))
    def test_exception_timeout(self):
        for policy in (Explodes,Hangs):
            a=run(policy,case(1));self.assertEqual(a['outcome'],'controller_exception');self.assertIsNone(a['estimation_mae']);self.assertEqual(a['final_error'],1)
if __name__=='__main__':unittest.main()
