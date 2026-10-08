import unittest
from fractions import Fraction as F
from harness import run,Proportional,Sign
class Zero:
    def action(self,*args):return F(0)
class Invalid:
    def action(self,*args):return True
class Floating:
    def action(self,*args):return float('nan')
class FiniteFloat:
    def action(self,*args):return 0.0
class ResetHangs:
    def __init__(self):
        while True:pass
class Explodes:
    def action(self,*args):raise RuntimeError('not retained')
class Hangs:
    def action(self,*args):
        while True:pass
class Large:
    def action(self,*args):return F(2)

def case(n,drift=F(0)):
    return {'gain':[F(1)]*n,'drift':[drift]*n,'observed':[True]*n,'immobilized':[False]*n}
class Tests(unittest.TestCase):
    def test_literal_and_reset(self):
        c=case(2);a=run(Proportional,c);b=run(Proportional,c)
        self.assertEqual(a,b);self.assertEqual(a['states'],[F(0),F(1,10),F(19,100)])
        self.assertEqual(a['control_effort'],F(19,100))
    def test_missing_observation(self):
        c=case(2);c['observed'][1]=False
        self.assertEqual(run(Proportional,c)['states'],[0,F(1,10),F(1,5)])
    def test_causal_prefix_hidden_future(self):
        for policy in (Proportional,Sign):
            a=case(4);b=case(4,F(3));a['observed']=b['observed']=[True,False,False,False]
            ra=run(policy,a);rb=run(policy,b)
            self.assertEqual([r['action'] for r in ra['records']],[r['action'] for r in rb['records']])
            a=case(4);b=case(4);b['drift'][3]=F(2)
            self.assertEqual([r['action'] for r in run(policy,a)['records']][:3],[r['action'] for r in run(policy,b)['records']][:3])
    def test_invalid_and_exception_metrics(self):
        for policy,label in ((Invalid,'invalid_action'),(Floating,'invalid_action'),(FiniteFloat,'invalid_action'),(Large,'invalid_action'),(Explodes,'controller_exception')):
            a=run(policy,case(1));self.assertEqual(a['outcome'],label)
            self.assertEqual((a['completed_steps'],a['control_effort'],a['final_error'],a['max_boundary_overshoot']),(0,0,1,0))
    def test_timeout(self):
        for policy in (Hangs,ResetHangs):
            a=run(policy,case(1));self.assertEqual(a['error_identifier'],'PolicyTimeout');self.assertEqual(a['outcome'],'controller_exception')
    def test_boundary_terminal_inclusive_precedence(self):
        a=run(Zero,case(1,F(15)),target=F(3,2));self.assertEqual(a['outcome'],'success')
        a=run(Zero,case(1,F(16)),target=F(8,5));self.assertEqual(a['outcome'],'boundary_exit');self.assertEqual(a['max_boundary_overshoot'],F(1,10))
        a=run(Zero,case(1,F(9)));self.assertEqual(a['outcome'],'success')
    def test_immobilization(self):
        c=case(1,F(5));c['immobilized']=[True];a=run(Sign,c)
        self.assertEqual(a['states'],[0,0]);self.assertEqual(a['control_effort'],F(1,10))
    def test_malformed(self):
        with self.assertRaises(ValueError):run(Sign,case(0))
        c=case(1);c['observed']=[1]
        with self.assertRaises(ValueError):run(Sign,c)
if __name__=='__main__':unittest.main()
