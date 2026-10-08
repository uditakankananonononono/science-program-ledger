import unittest
from fractions import Fraction as F
from compare import evaluate
class Tests(unittest.TestCase):
    def test_fixed_tie_break(self):
        r=evaluate([('first',[(F(1,2),F(1,2))],[F(1)]),('second',[(F(1,2),F(1,2))],[F(1)])],F(1))
        self.assertEqual((r['robust_choice'],r['nominal_choice']),('first','first'))
        self.assertEqual((r['guarantee_difference'],r['nominal_difference']),(0,0))
    def test_disagreement(self):
        r=evaluate([('single',[(F(7,10),F(7,10))],[F(1)]),('split',[(F(1,2),F(1,2))]*2,[F(1,2)]*2)],F(1,2))
        self.assertEqual((r['robust_choice'],r['nominal_choice']),('single','split'))
        self.assertEqual((r['guarantee_difference'],r['nominal_difference']),(F(1,5),-F(1,20)))
if __name__=='__main__':unittest.main()
