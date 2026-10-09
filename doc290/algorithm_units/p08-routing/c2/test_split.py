import unittest,copy
from split import split,verify_output,Invalid
class Development(unittest.TestCase):
    def chain(self):
        def e(t,time,exp,ss):return {'target':t,'time':time,'exposure':exp,'scenario_times':ss}
        return {'original':{'a':[e('b',2,1,[3])],'b':[e('a',7,4,[5]),e('c',1,0,[2])],'c':[e('b',9,2,[7])]},'compressed':{'a':[e('c',3,1,[5])],'c':[e('a',16,6,[12])]},'witnesses':{'a':[['a','b','c']],'c':[['c','b','a']]},'start':'b','goal':'c','budget':6,'forbidden':[],'penalties':[]}
    def test_literal_interior_costs_and_provenance(self):
        s=self.chain();r=split(s);self.assertEqual(r['anchors'],['a','b','c']);self.assertTrue(verify_output(s,r));self.assertEqual(r['compressed']['b'][0]['time'],1);self.assertEqual(r['compressed']['b'][1]['time'],7)
        r['provenance']['b'][0]['first_position']=0
        with self.assertRaises(Invalid):verify_output(s,r)
    def test_source_before_query_turns(self):
        s=self.chain();s['start']='missing';s['compressed']['a'][0]['time']=0;self.assertIn('source representation',split(s)['reason'])
        s=self.chain();s['penalties']=[1];self.assertEqual(split(s)['status'],'INVALID')
    def test_cycle_positions_same_and_two_query(self):
        def e(t,time=1):return {'target':t,'time':time,'exposure':time,'scenario_times':[time]}
        s={'original':{'a':[e('b'),e('c')],'b':[e('a'),e('c')],'c':[e('b'),e('a')]},'compressed':{'a':[e('a',3),e('a',3)]},'witnesses':{'a':[['a','b','c','a'],['a','c','b','a']]},'start':'b','goal':'b','budget':3,'forbidden':[],'penalties':[]}
        r=split(s);self.assertEqual(r['anchors'],['a','b']);self.assertTrue(verify_output(s,r));self.assertEqual(sum(len(v) for v in r['compressed'].values()),4)
        s['goal']='c';r=split(s);self.assertEqual(sum(len(v) for v in r['compressed'].values()),6);self.assertTrue(verify_output(s,r))
    def test_isolate(self):
        s={'original':{'a':[]},'compressed':{'a':[]},'witnesses':{'a':[]},'start':'a','goal':'a','budget':0,'forbidden':[],'penalties':[]};self.assertEqual(split(s)['status'],'SPLIT_REPRESENTATION')
    def test_oracle_hand_and_disagreement(self):
        from compare import oracle
        s=self.chain();self.assertEqual(oracle(s['original'],'b','a',4),7);self.assertIsNone(oracle(s['original'],'b','a',3));self.assertNotEqual(oracle(s['original'],'b','c',0),99)
    def test_source_gate_refusal(self):
        from compare import gate
        from unittest.mock import patch
        with patch('compare.hashlib.sha256',side_effect=ValueError('dev source failure')):
            with self.assertRaises(ValueError):gate()
if __name__=='__main__':unittest.main()
