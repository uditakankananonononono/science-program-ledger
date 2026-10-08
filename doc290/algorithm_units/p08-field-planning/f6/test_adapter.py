import unittest,os
from unittest.mock import patch
from fractions import Fraction as F
from adapter import check,assemble,Invalid
class Development(unittest.TestCase):
    def test_every_prefix_row(self):
        m={'x':[3,-2],'target':[1,4],'dt':['1/2','3/2'],'B':[[2,-3],[-1,4]],'lower':[[-4,-3],[0,-2],[-1,1]],'upper':[[4,3],[7,9],[8,9]],'limit':[2,3],'slew':[1,2],'previous':['1/2','-1/2']}
        A,b,L=assemble(m);u=[F(2,3),F(-1,4),F(3,2),F(-2,5)];controls=[u[:2],u[2:]];old=[F(1,2),F(-1,2)];want=[];times=[F(1,2),F(3,2)]
        for row in controls:
            for v,c in zip(row,[2,3]):want.extend([v-c,-v-c])
        path=[m['x'][:]]
        for t,row in zip(times,controls):
            for v,p,r in zip(row,old,[1,2]):want.extend([v-p-r*t,-v+p-r*t])
            old=row;path.append([v+t*sum(a*c for a,c in zip(br,row)) for v,br in zip(path[-1],m['B'])])
        for row,lo,hi in zip(path,m['lower'],m['upper']):
            for v,l,h in zip(row,lo,hi):want.extend([v-h,l-v])
        for v,t in zip(path[-1],m['target']):want.extend([v-t,t-v])
        got=[sum(c*v for c,v in zip(row,u))-rhs for row,rhs in zip(A,b)]
        self.assertEqual(len(got),32);self.assertEqual(got,want)
    def test_zero_row_and_boundary(self):
        m={'x':[0],'target':[0],'dt':[1],'B':[[1]],'lower':[[1],[0]],'upper':[[1],[0]],'limit':[1],'slew':[1],'previous':[0]}
        A,b,L=assemble(m);lam=[0]*len(A);i=L.index('node:0:0:lower');lam[i]=1
        self.assertEqual(A[i],[0]);self.assertEqual(b[i],-1);self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'INFEASIBLE')
        m['lower'][0]=[0];self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'UNAVAILABLE')
        lam[i]=-1;self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'INVALID')
        lam[i]=1;lam[0]=1;self.assertEqual(check(m,{'kind':'farkas','multipliers':lam})['status'],'INVALID')
    def test_intermediate_only_violation(self):
        m={'x':[0],'target':[0],'dt':[1,1],'B':[[1]],'lower':[[0],[1],[0]],'upper':[[0],[1],[0]],'limit':[1],'slew':[2],'previous':[0]}
        self.assertEqual(check(m,{'kind':'primal','controls':[0,0]})['status'],'INVALID')
        r=check(m,{'kind':'primal','controls':[1,-1]});self.assertEqual(r['status'],'FEASIBLE');self.assertEqual(r['path'],[['0/1'],['1/1'],['0/1']])
    def test_model_keys_and_missing(self):
        self.assertEqual(check({},None)['status'],'INVALID')
        m={'x':[0],'target':[0],'dt':[1],'B':[[1]],'lower':[[0],[0]],'upper':[[0],[0]],'limit':[1],'slew':[1],'previous':[0]}
        self.assertEqual(check(m,None)['status'],'UNAVAILABLE')
        for w in ({'kind':'other'},{'kind':'primal','controls':[0],'extra':0},{'kind':'primal','controls':['-0/1']},{'kind':'farkas','multipliers':[0]}):self.assertEqual(check(m,w)['status'],'INVALID')
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('FEASIBLE',{'status':'INVALID'}))
    def test_gate_thread(self):
        from compare import gate
        with patch.dict(os.environ,{'OPENBLAS_NUM_THREADS':'2'}):
            with self.assertRaises(Invalid):gate()
if __name__=='__main__':unittest.main()
