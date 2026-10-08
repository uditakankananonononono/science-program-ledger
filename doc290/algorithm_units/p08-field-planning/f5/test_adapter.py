import unittest,os
from unittest.mock import patch
from fractions import Fraction as F
from adapter import check,assemble,Invalid
class Development(unittest.TestCase):
    def test_every_signed_row(self):
        m={'x':[3,-2],'dt':['1/2','3/2'],'maps':[[[2,-3],[-1,4]],[[-2,1],[5,-1]]],'lower':[[-3,2],[4,-5]],'upper':[[7,9],[8,0]],'limit':[2,3],'slew':[1,2],'previous':['1/2','-1/2']}
        A,b,L=assemble(m);u=[F(2,3),F(-1,4),F(3,2),F(-2,5)];controls=[u[:2],u[2:]];old=[F(1,2),F(-1,2)];want=[]
        for row in controls:
            for v,c in zip(row,[2,3]):want.extend([v-c,-v-c])
        for t,row in zip([F(1,2),F(3,2)],controls):
            for v,p,r in zip(row,old,[1,2]):want.extend([v-p-r*t,-v+p-r*t])
            old=row
        for B,lo,hi in zip(m['maps'],m['lower'],m['upper']):
            terminal=m['x'][:]
            for t,row in zip([F(1,2),F(3,2)],controls):terminal=[v+t*sum(a*c for a,c in zip(br,row)) for v,br in zip(terminal,B)]
            for v,l,h in zip(terminal,lo,hi):want.extend([v-h,l-v])
        got=[sum(c*v for c,v in zip(row,u))-rhs for row,rhs in zip(A,b)]
        self.assertEqual(len(got),24);self.assertEqual(got,want)
    def test_farkas_algebra_and_boundary(self):
        m={'x':[0],'dt':[1],'maps':[[[1]],[[1]]],'lower':[[1],[-1]],'upper':[[1],[-1]],'limit':[2],'slew':[2],'previous':[0]}
        A,b,L=assemble(m);lam=[0,0,0,0,0,1,1,0]
        self.assertEqual(sum(row[0]*v for row,v in zip(A,lam)),0);self.assertEqual(sum(c*v for c,v in zip(b,lam)),-2)
        self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'INFEASIBLE')
        m['lower']=[[0],[0]];m['upper']=[[0],[0]];self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'UNAVAILABLE')
        lam[0]=-1;self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'INVALID')
        lam[0]=1;self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'INVALID')
    def test_primal_replay(self):
        m={'x':[2,-1],'dt':['1/2','3/2'],'maps':[[[1,2],[-1,3]],[[2,-1],[3,1]]],'lower':[[5,1],[3,3]],'upper':[[5,1],[3,3]],'limit':[1,1],'slew':[0,0],'previous':['1/2','1/2']}
        r=check(m,{'kind':'primal','controls':['1/2','1/2','1/2','1/2']});self.assertEqual(r['status'],'FEASIBLE');self.assertEqual(r['scenario_paths'][0][-1],['5/1','1/1'])
    def test_model_first_keys(self):
        self.assertEqual(check({},None)['status'],'INVALID')
        m={'x':[0],'dt':[1],'maps':[[[1]]],'lower':[[0]],'upper':[[0]],'limit':[1],'slew':[1],'previous':[0]}
        self.assertEqual(check(m,None)['status'],'UNAVAILABLE')
        for w in ({'kind':'other'},{'kind':'primal','controls':[0],'extra':0},{'kind':'primal','controls':[True]},{'kind':'farkas','multipliers':[0]}):self.assertEqual(check(m,w)['status'],'INVALID')
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('FEASIBLE',{'status':'INVALID'}))
    def test_gate_thread(self):
        from compare import gate
        with patch.dict(os.environ,{'OPENBLAS_NUM_THREADS':'2'}):
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
