import unittest,itertools,os
from unittest.mock import patch
from fractions import Fraction as F
from adapter import ramps,check,Invalid
class Development(unittest.TestCase):
    def test_all_ramps_and_corners(self):
        dt=[F(1,2),F(3,2),F(1,4)];cap=[F(2),F(1)];rate=[F(1),F(2)];prev=[F(1,2),F(-1,2)]
        lo,hi,L,U=ramps(dt,cap,rate,prev)
        self.assertEqual(lo,[[F(0),F(-1)],[F(-3,2),F(-1)],[F(-7,4),F(-1)]])
        self.assertEqual(hi,[[F(1),F(1,2)],[F(2),F(1)],[F(2),F(1)]])
        self.assertEqual(L,[F(-43,16),F(-9,4)]);self.assertEqual(U,[F(4),F(2)])
        B=[[2,-3],[-1,4]];v=[-2,3];x=[3,-1];y=[5,7]
        m={'x':x,'target':y,'dt':['1/2','3/2','1/4'],'B':B,'limit':[2,1],'slew':[1,2],'previous':['1/2','-1/2']}
        r=check(m,{'kind':'separator','direction':v})
        corners=[]
        for z in itertools.product(*zip(L,U)):
            corners.append(sum(v[i]*sum(B[i][j]*z[j] for j in range(2)) for i in range(2)))
        self.assertEqual(F(r['support']),max(corners));self.assertEqual(F(r['projection']),sum(v[i]*(y[i]-x[i]) for i in range(2)))
    def test_endpoint_and_degenerate_lift(self):
        m={'x':[3,-1],'target':[4,1],'dt':['1/2','3/2'],'B':[[1,0],[0,2]],'limit':[2,1],'slew':[0,0],'previous':['1/2','1/2']}
        r=check(m,{'kind':'feasible','integrals':[1,1]});self.assertEqual(r['status'],'REACHABLE');self.assertEqual(r['mix'],['0/1','0/1']);self.assertEqual(r['controls'],[['1/2','1/2'],['1/2','1/2']])
        m={'x':[0],'target':['3/4'],'dt':['1/2'],'B':[[1]],'limit':[2],'slew':[1],'previous':[1]}
        r=check(m,{'kind':'feasible','integrals':['3/4']});self.assertEqual(r['controls'],[['3/2']]);self.assertEqual(r['mix'],['1/1'])
        m['target']=['1/4'];r=check(m,{'kind':'feasible','integrals':['1/4']});self.assertEqual(r['controls'],[['1/2']]);self.assertEqual(r['mix'],['0/1'])
    def test_exact_keys_and_missing(self):
        self.assertEqual(check({},None)['status'],'INVALID')
        m={'x':[0],'target':[0],'dt':[1],'B':[[1]],'limit':[1],'slew':[1],'previous':[0]}
        self.assertEqual(check(m,None)['status'],'UNAVAILABLE')
        for w in ({'kind':'anything'},{'kind':'feasible','integrals':[0],'extra':0},{'kind':'separator','direction':[0]},{'kind':'separator','direction':[1],'extra':0}):self.assertEqual(check(m,w)['status'],'INVALID')
    def test_strict_boundary(self):
        m={'x':[0],'target':[1],'dt':[1],'B':[[1]],'limit':[1],'slew':[1],'previous':[0]}
        self.assertEqual(check(m,{'kind':'separator','direction':[1]})['status'],'UNAVAILABLE')
        m['target']=['1000000000000000001/1000000000000000000'];self.assertEqual(check(m,{'kind':'separator','direction':[1]})['status'],'UNREACHABLE')
    def test_comparator_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('REACHABLE',{'status':'INVALID'}))
    def test_gate_thread_before_load(self):
        from compare import gate
        with patch.dict(os.environ,{'OPENBLAS_NUM_THREADS':'2'}):
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
