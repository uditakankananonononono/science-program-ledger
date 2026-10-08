import unittest
from fractions import Fraction as F
from itertools import product
from two_agent_allocation import interval
from uncertain_allocation import uncertain_interval,select_uncertain
class Tests(unittest.TestCase):
    def test_point_intervals(self):
        for p in ([F(1,3)],[F(1,3),F(2,3)]):
            w=[F(1,len(p))]*len(p)
            a=interval(p,w,F(1));b=uncertain_interval([(x,x) for x in p],w,F(1))
            self.assertEqual((a['minimum'],a['maximum']),(b['minimum'],b['maximum']))
    def test_iterable_payloads(self):
        u=uncertain_interval([(F(1,4),F(3,4))],(x for x in [F(1)]),F(1))
        self.assertEqual((u['minimum'],u['maximum']),(F(1,4),F(3,4)))
    def test_all_unconstrained(self):
        a=uncertain_interval([(F(0),F(1))]*2,[F(1,2)]*2,F(1))
        self.assertEqual((a['minimum'],a['maximum']),(0,1))
    def test_grid_rectangle_extrema(self):
        pairs=[(F(a,4),F(b,4)) for a in range(5) for b in range(a,5)]
        for r1,r2 in product(pairs,repeat=2):
            for w,k in (([F(1,2)]*2,F(1,2)),([F(1,2)]*2,F(1)),([F(3,4),F(1,4)],F(1,2))):
                vals=[]
                for a,b in product(range(5),repeat=2):
                    if r1[0]<=F(a,4)<=r1[1] and r2[0]<=F(b,4)<=r2[1]:
                        v=interval([F(a,4),F(b,4)],w,k);vals.extend([v['minimum'],v['maximum']])
                u=uncertain_interval([r1,r2],w,k)
                self.assertEqual((u['minimum'],u['maximum']),(min(vals),max(vals)))
    def test_ranking_uncertainty(self):
        u=select_uncertain([('single',[(F(3,5),F(4,5))],[F(1)]),('split',[(F(7,10),F(9,10))]*2,[F(1,2)]*2)],F(1),F(1,2))
        self.assertEqual(u['maximin_ties'],['split'])
        self.assertEqual(u['best_guaranteed_probability'],F(7,10))
    def test_invalid(self):
        for r in ([],[(F(3,4),F(1,4))],[(F(-1),F(1))],[(0.5,F(1))],[(F(0),)],[(F(0),F(1),F(1))]):
            with self.assertRaises(ValueError):uncertain_interval(r,[F(1)],F(1))
        with self.assertRaises(ValueError):select_uncertain([],F(1),F(1))
        with self.assertRaises(ValueError):select_uncertain([('a',[(F(0),F(1))],[F(2)])],F(1),F(1))
if __name__=='__main__':unittest.main()
