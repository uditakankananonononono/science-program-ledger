import unittest,copy
from fixtures import edge,oracle
from model import witness,Invalid
class OracleDevelopment(unittest.TestCase):
    def s(self):return {'graph':{'a':[edge('b',[1,5,2]),edge('b',[4,1,2]),edge('a',[0,0,0])],'b':[edge('g',[2,0,3])],'g':[]},'start':'a','goal':'g'}
    def test_known_parallel_three_scenario(self):
        self.assertEqual(oracle(self.s()),5)
        r={'path':['a','b','g'],'edges':[{'source':'a','edge_index':0,'target':'b'},{'source':'b','edge_index':0,'target':'g'}],'scenario_totals':[3,5,5],'worst_time':5};self.assertEqual(witness(self.s(),r)['worst_time'],oracle(self.s()))
        r['edges'][0]['edge_index']=1
        with self.assertRaises(Invalid):witness(self.s(),r)
        self.assertNotEqual(oracle(self.s()),6)
    def test_zero_self_disconnected_identity(self):
        s=self.s();s['graph']['b'][0]['scenario_times']=[0,0,0];self.assertEqual(oracle(s),4)
        s=self.s();s['graph']['b']=[];self.assertIsNone(oracle(s))
        s=self.s();s['goal']='a';self.assertEqual(oracle(s),0)
    def test_strict_types_dimensions(self):
        for value in ([1,2],[True,0,0],[1.0,0,0]):
            s=self.s();s['graph']['a'][0]['scenario_times']=value
            with self.assertRaises(Invalid):oracle(s)
