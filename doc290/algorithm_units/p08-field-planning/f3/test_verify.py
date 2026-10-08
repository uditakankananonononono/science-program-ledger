import unittest
from fractions import Fraction as F
from verify import assemble,verify,rational,Invalid,load_bytes
class Development(unittest.TestCase):
    def test_grammar(self):
        for v in (True,1.0,'1','-0/1','0/2','2/4','+1/2','01/2','1/-2','1/0',None):
            with self.assertRaises(Invalid):rational(v)
        self.assertEqual(rational('-3/2'),F(-3,2));self.assertEqual(rational(2),F(2))
    def test_multidimensional_assembly(self):
        m={'x':[3,-2],'dt':['1/2',2],'maps':[[[2,-1],[3,4]],[[-1,5],[2,0]]],'targets':[[7,1],[-3,8]],'limit':[2,3],'slew':[1,'1/2'],'previous':[1,-1]}
        A,b,c,L=assemble(m)
        self.assertEqual(len(A),25);self.assertEqual(len(c),5)
        wanted={
          'slew:0:0:upper':([1,0,0,0,0],F(3,2)),
          'slew:0:0:lower':([-1,0,0,0,0],F(-1,2)),
          'slew:0:1:upper':([0,1,0,0,0],F(-3,4)),
          'slew:1:1:lower':([0,1,0,-1,0],1),
          'terminal:0:0:upper':([1,F(-1,2),4,-2,-1],4),
          'terminal:0:1:lower':([F(-3,2),-2,-6,-8,-1],-3),
          'terminal:1:0:upper':([F(-1,2),F(5,2),-2,10,-1],-6),
          'terminal:1:1:upper':([1,0,4,0,-1],10)}
        for label,(row,rhs) in wanted.items():
            i=L.index(label);self.assertEqual(A[i],row);self.assertEqual(b[i],rhs)
    def test_slew_tight_certificate(self):
        m={'x':[3],'dt':['1/2'],'maps':[[[2]]],'targets':[[5]],'limit':[2],'slew':[1],'previous':['1/2']}
        # u=1 hits slew upper, terminal=4, exact error1.
        self.assertEqual(verify(m,{'z':[1,1],'lambda':[0,0,1,0,0,1,0]})['status'],'VERIFIED')
        self.assertEqual(verify(m,{'z':[1,2],'lambda':[0,0,1,0,0,1,0]})['reason'],'objective gap')
    def test_json(self):
        for data in (b'{"a":0,"a":1}',b'{"a":NaN}',b'['*12+b'0'+b']'*12,b'x'*131073):
            with self.assertRaises(Invalid):load_bytes(data)
    def test_invalid_dimensions(self):
        self.assertEqual(verify({},None)['status'],'INVALID')
    def test_missing(self):
        m={'x':[0],'dt':[1],'maps':[[[1]]],'targets':[[0]],'limit':[1],'slew':[0],'previous':[0]}
        self.assertEqual(verify(m,None)['status'],'UNAVAILABLE')
if __name__=='__main__':unittest.main()

class ComparatorControl(unittest.TestCase):
    def test_disagreement(self):
        from compare import agreed
        self.assertFalse(agreed('VERIFIED',{'status':'INVALID'}))
        self.assertTrue(agreed('UNAVAILABLE',{'status':'UNAVAILABLE'}))
