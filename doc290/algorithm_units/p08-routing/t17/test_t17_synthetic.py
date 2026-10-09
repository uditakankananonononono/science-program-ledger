"""Private synthetic development controls. No fixed corpus or baseline comparison."""
import copy,unittest
from unittest.mock import patch
from bindings import load
from model import Invalid

def edge(ss,x=0,target='g'):return dict(target=target,time=1,scenario_times=ss,exposure=x)
def statement(edges,budget=4):return dict(graph={'a':edges,'g':[]},start='a',goal='g',budget=budget,forbidden=[],penalties=[])

class Synthetic(unittest.TestCase):
 def setUp(self):self.m,self.p=load('t17')
 def checked(self,s):
  result=self.m.solve(s);self.p.check(s,result);return result
 def test_trigger_improvement(self):
  s=statement([edge([8,8]),edge([0,12]),edge([12,0]),edge([5,5])])
  r=self.checked(s)
  self.assertEqual(r['weighted_proof']['preweighted_W'],8)
  self.assertEqual(r['weighted_proof']['selected_W'],5)
  self.assertIs(r['incumbent'],r['candidate_ledger'][-1]['route'])
  self.assertEqual(r['route']['worst_time'],5)
 def test_duplicate_and_overbudget(self):
  for s in [statement([edge([6,6]),edge([0,10]),edge([10,0])]),statement([edge([8,8]),edge([0,12]),edge([12,0]),edge([4,4],9)],4)]:
   r=self.checked(s);self.assertIsNotNone(r['weighted_proof']);self.assertEqual(r['weighted_proof']['selected_index'],0)
  self.assertFalse(r['candidate_ledger'][-1]['audit']['eligible'])
 def test_nontrigger_raise(self):
  for s in [statement([edge([2,2])]),statement([edge([8,8]),edge([2,2],1)]),statement([edge([2,2],9)],0)]:
   with patch.object(self.m,'weighted_candidate',side_effect=RuntimeError('absent')),patch.object(self.p,'weighted_candidate_expected',side_effect=RuntimeError('absent')):
    r=self.checked(s)
   self.assertIsNone(r['weighted_proof']);self.assertEqual(r['counters']['weighted_candidate_inspections'],0)
 def test_delay_once_and_revisit(self):
  s=dict(graph={'a':[edge([1,5],1,'b')],'b':[edge([1,1],1,'c'),edge([5,1],1)],'c':[edge([1,1],1,'b')],'g':[edge([0,0],0,'u')],'u':[edge([0,0])]},start='a',goal='g',budget=4,forbidden=[[['a',0],['b',1]]],penalties=[dict(incoming=['c',0],outgoing=['b',1],delay=2)])
  r=self.checked(s);self.assertEqual(r['route']['path'],['a','b','c','b','g']);self.assertEqual(r['route']['turn_penalty'],2)
 def test_attacks(self):
  s=statement([edge([8,8]),edge([0,12]),edge([12,0]),edge([5,5])]);r=self.checked(s)
  for key in r['counters']:
   for delta in (1,999):
    q=copy.deepcopy(r);q['counters'][key]+=delta
    with self.assertRaises(Invalid,msg=key):self.p.check(s,q)
  for key,value in [('turn_delay_factor',1),('weights',[1,2]),('trigger','wrong'),('selected_index',True),('weighted_index',4.0),('produced_count',2),('selected_W',6),('exposure_weight',1)]:
   q=copy.deepcopy(r);q['weighted_proof'][key]=value
   with self.assertRaises(Invalid,msg=key):self.p.check(s,q)
  for mutate in [lambda q:q['weighted_proof'].update(extra=1),lambda q:q['weighted_proof'].pop('weights'),lambda q:q['candidate_ledger'][-1].update(index=True),lambda q:q['candidate_ledger'][-1]['audit'].update(eligible=False)]:
   q=copy.deepcopy(r);mutate(q)
   with self.assertRaises(Invalid):self.p.check(s,q)
 def test_last_prefix_and_charged_skip(self):
  last=statement([edge([8,8]),edge([1,10],1),edge([2,2],1)],1)
  charged=statement([edge([8,8]),edge([2,2],6)],0)
  for source in (last,charged):
   with patch.object(self.m,'weighted_candidate',side_effect=RuntimeError('absent')),patch.object(self.p,'weighted_candidate_expected',side_effect=RuntimeError('absent')):r=self.checked(source)
   self.assertIsNone(r['weighted_proof'])
  self.assertEqual(r['candidate_activation'],'charged_original_bound_equality')
 def test_audit_error_propagates(self):
  source=statement([edge([8,8]),edge([0,12]),edge([12,0]),edge([5,5])]);audit=self.m.route_audit
  def reject(s,route):
   if route['scenario_totals']==[5,5]:raise Invalid('weighted audit deliberate rejection')
   return audit(s,route)
  with patch.object(self.m,'route_audit',side_effect=reject):
   with self.assertRaises(Invalid):self.m.solve(source)
 def test_selected_weighted_tie_retains_first(self):
  source=statement([edge([5,5]),edge([0,12]),edge([12,0]),edge([5,5])]);r=self.checked(source)
  self.assertEqual(r['weighted_proof']['selected_index'],0)
  self.assertIs(r['incumbent'],r['candidate_ledger'][0]['route'])
 def test_weighted_delay_factor_direct(self):
  source=dict(graph={'a':[edge([1,7],0,'b'),edge([7,1],0,'b')],'b':[edge([1,1])],'g':[]},start='a',goal='g',budget=0,forbidden=[],penalties=[dict(incoming=['a',0],outgoing=['b',0],delay=3)])
  from model import model
  G,n,_,_,states,arcs=model(source);c={'weighted_candidate_inspections':0}
  route,stop=self.m.weighted_candidate(source,states,arcs,G,n,c)
  expected,ledger=self.p.weighted_candidate_expected(source)
  self.assertEqual(route,expected);self.assertEqual(stop,ledger)
  self.assertEqual(route['edges'][0]['edge_index'],1)
  self.assertEqual(stop['tentative_distances'][-1],10)
 def test_once_charged(self):
  s=statement([edge([8,8]),edge([0,12]),edge([12,0]),edge([5,5])]);reverse=self.m.charged_reverse;audit=self.m.charged_check;calls=[];checks=[]
  def once(*args):
   if calls:raise RuntimeError('rerun')
   value=reverse(*args);calls.append(value);return value
  def check(*args):
   if checks:raise RuntimeError('reaudit')
   checks.append(args[1]);return audit(*args)
  with patch.object(self.m,'charged_reverse',side_effect=once),patch.object(self.m,'charged_check',side_effect=check):r=self.checked(s)
  self.assertIs(r['charged_proof']['distances'],calls[0]);self.assertIs(r['charged_proof'],checks[0])

if __name__=='__main__':unittest.main(verbosity=2)
