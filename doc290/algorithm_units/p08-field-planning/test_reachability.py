import unittest,numpy as np
from reachability import projection_bounds
from scipy.optimize import linprog
class ReachabilityTests(unittest.TestCase):
    def test_scalar_ramp(self):
        r=projection_bounds([0],[1,1],[[1]],[2],[.5],[0],[1])
        self.assertEqual(r['projection_max'],1.5);self.assertEqual(r['projection_min'],-1.5)
        np.testing.assert_array_equal(r['maximizing_controls'],[[.5],[1.]])
    def test_negative_weight_and_previous(self):
        r=projection_bounds([2],[1],[[2]],[2],[.5],[1],[-1])
        self.assertEqual(r['projection_max'],-3);self.assertEqual(r['projection_min'],-5)
    def test_coordinate_bounds_not_joint_feasibility(self):
        for v in ([1,0],[0,1]):
            r=projection_bounds([0,0],[1],[[1],[1]],[1],[1],[0],v)
            self.assertEqual((r['projection_min'],r['projection_max']),(-1,1))
        r=projection_bounds([0,0],[1],[[1],[1]],[1],[1],[0],[1,-1])
        self.assertEqual((r['projection_min'],r['projection_max']),(0,0)) # target [1,-1] projection 2 impossible
    def test_support_controls_feasible_and_match_dense_lp(self):
        times=np.array([.2,.4,.3]);B=np.array([[1.,-2.],[3.,1.]]);v=np.array([.7,-.2]);limit=np.array([1.,2.]);slew=np.array([.8,.5]);prev=np.array([.2,-.3])
        r=projection_bounds([0,0],times,B,limit,slew,prev,v)
        rows=[];rhs=[]
        for k in range(3):
            for j in range(2):
                row=np.zeros(6);row[2*k+j]=1
                if k:row[2*(k-1)+j]=-1
                offset=prev[j] if k==0 else 0
                rows.extend([row,-row]);rhs.extend([slew[j]*times[k]+offset,slew[j]*times[k]-offset])
        c=(times[:,None]*(v@B)).ravel()
        result=linprog(-c,A_ub=rows,b_ub=rhs,bounds=[(-limit[j],limit[j]) for k in range(3) for j in range(2)],method='highs')
        self.assertTrue(result.success);self.assertAlmostEqual(-result.fun,r['projection_max'])
        for name in ('minimizing_controls','maximizing_controls'):
            u=np.array(r[name]);self.assertTrue((abs(u)<=limit+1e-12).all());self.assertTrue((abs(np.diff(np.vstack([prev,u]),axis=0))<=times[:,None]*slew+1e-12).all())
if __name__=='__main__':unittest.main()
