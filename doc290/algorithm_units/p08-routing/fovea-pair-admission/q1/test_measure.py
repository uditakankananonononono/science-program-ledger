import unittest
import numpy as np
from measure import endpoints,diagnostic
class Tests(unittest.TestCase):
    def test_indices(self):
        a=np.ones((1,20),bool);m,p=endpoints(a,a)
        self.assertEqual(m,20);self.assertEqual([y for x,y in p],[(j*19)//15 for j in range(16)])
    def test_missing(self):
        a=np.zeros((2,2),bool);r=diagnostic(a,a)
        self.assertEqual(r['status'],'insufficient_shared_endpoints');self.assertEqual(r['query_count'],0)
    def test_split(self):
        a=np.ones((1,5),bool);b=a.copy();b[0,2]=False;r=diagnostic(a,b)
        self.assertEqual(r['counts']['A1_only'],4);self.assertEqual(r['counts']['both_reachable'],2)
        self.assertEqual(r['shared_coverage_A1'],{'numerator':4,'denominator':5})
    def test_neither(self):
        a=np.array([[1,0,1]],bool);r=diagnostic(a,a)
        self.assertEqual(r['counts']['neither'],1)
if __name__=='__main__':unittest.main()
