import unittest
from fractions import Fraction as F
from two_agent_allocation import interval,select
class Tests(unittest.TestCase):
    def test_analytic_endpoints(self):
        self.assertEqual(interval([F(1,2)]*2,[F(1,2)]*2,F(1,2))['minimum'],F(1,2))
        self.assertEqual(interval([F(1,2)]*2,[F(1,2)]*2,F(1))['minimum'],0)
        self.assertEqual(interval([F(1,2)]*2,[F(1,2)]*2,F(1))['maximum'],F(1,2))
    def test_independence_ranking_reverses(self):
        r=select([('single',[F(7,10)],[F(1)]),('split',[F(1,2)]*2,[F(1,2)]*2)],F(1),F(1,2))
        self.assertEqual(r['maximin_ties'],['single'])
        self.assertGreater(r['results'][1]['independent'],r['results'][0]['independent'])
    def test_weight_assignment(self):
        p=[F(4,5),F(2,5)]
        self.assertEqual(interval(p,[F(7,10),F(3,10)],F(3,5))['minimum'],F(4,5))
        self.assertEqual(interval(p,[F(3,10),F(7,10)],F(3,5))['minimum'],F(2,5))
    def test_ties_and_deterministic(self):
        r=select([('a',[F(1)],[F(1)]),('b',[F(1),F(1)],[F(1,2)]*2)],F(1),F(1))
        self.assertEqual(r['maximin_ties'],['a','b'])
        self.assertEqual(interval([F(0),F(1)],[F(1,2)]*2,F(1))['maximum'],0)
    def test_exact_joint_grid(self):
        # Enumerate denominator-4 joint distributions and compare literal extrema.
        for a in range(5):
            for b in range(5):
                p=[F(a,4),F(b,4)]
                for required in (F(1,2),F(1)):
                    values=[]
                    for t in range(max(0,a+b-4),min(a,b)+1):
                        masses=[F(4-a-b+t,4),F(b-t,4),F(a-t,4),F(t,4)]
                        values.append(sum(m for m,s in zip(masses,[0,F(1,2),F(1,2),1]) if s>=required))
                    r=interval(p,[F(1,2)]*2,required)
                    self.assertEqual((r['minimum'],r['maximum']),(min(values),max(values)))
    def test_invalid(self):
        for p,w,k in (([],[],F(1)),([.5],[F(1)],F(1)),([F(2)],[F(1)],F(1)),([F(1)],[F(0)],F(1)),([F(1)],[F(1)],F(0))):
            with self.assertRaises(ValueError):interval(p,w,k)
        for menu in ([],[('a',[F(1)],[F(2)])],[('a',[F(1)],[F(1)]),('a',[F(1)],[F(1)])]):
            with self.assertRaises(ValueError):select(menu,F(1),F(1))
if __name__=='__main__':unittest.main()
