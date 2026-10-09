import unittest,copy
from fractions import Fraction as F
from unittest.mock import patch
from generator import generate,candidates,reverse
from proof import distances,audit,guarded_potential
from model import Failure,Invalid,Domain,model,i3
class Development(unittest.TestCase):
    def e(self,t,ss):return {'target':t,'time':1,'exposure':0,'scenario_times':ss}
    def s(self):
        # Multiple finite maxima at source and x incoming, plus unreachable cycle.
        return {'graph':{'a':[self.e('b',[2,4])],'b':[self.e('g',[3,1])],'g':[self.e('a',[1,1])],'x':[self.e('b',[0,0])],'u':[self.e('u',[0,0])]},'start':'a','goal':'g','budget':0,'forbidden':[],'penalties':[],'route':{'path':['a','b','g'],'edges':[{'source':'a','edge_index':0,'target':'b'},{'source':'b','edge_index':0,'target':'g'}],'scenario_totals':[5,5],'worst_time':5,'exposure':0,'turn_penalty':0}}
    def test_full_candidates_and_checker_each(self):
        s=self.s();import generator;actual=generator.invoke_i3
        with patch('generator.invoke_i3',wraps=actual) as calls:r=generate(s)
        self.assertEqual(r['status'],'CERTIFIED_INTEGRATED');self.assertEqual(len(r['candidates']),12);self.assertEqual(calls.call_count,12);self.assertEqual(r['selected_index'],0)
        self.assertEqual(len(candidates(1)),4);self.assertEqual(len(candidates(4)),20)
    def test_clamp_nonunique_boundary_allstates(self):
        s=self.s();G,n,st,ar,pr=model(s);w=(F(1),F(0));d=reverse(st,ar,G,w,F(0));aa=audit(s,w,F(0),st,d);h,M=guarded_potential(d,aa);self.assertTrue(any(x is None for x in d));self.assertGreaterEqual(sum(x==M for x in d),2);self.assertTrue(all(c+h[a]-h[b]>=0 for a,b,c,*_ in aa))
        for bad in ([F(0)]*len(d),[None]*len(d)):
            with self.assertRaises(Failure):audit(s,w,F(0),st,bad)
        self.assertIsNone(guarded_potential([F(0),None,F(0)],[(1,2,F(0),None,0)]))
        with self.assertRaises(Failure):guarded_potential([None,F(0)],[])
    def test_audit_precedence_checker_invalid(self):
        with patch('generator.audit',side_effect=Failure('audit')),patch('generator.guarded_potential') as g:
            with self.assertRaises(Failure):generate(self.s())
            g.assert_not_called()
        with patch('generator.invoke_i3',return_value={'status':'INVALID'}):
            with self.assertRaises(Failure):generate(self.s())
        with patch('generator.reverse',return_value=[None]*7):
            with self.assertRaises(Failure):generate(self.s())
    def test_missing_invalid_and_types(self):
        s=self.s();s['route']=None;self.assertEqual(generate(s)['status'],'UNAVAILABLE');s['budget']=True;self.assertEqual(generate(s)['status'],'INVALID')
        for v in (True,1.0,-1):
            s=self.s();s['route']['edges'][0]['edge_index']=v;self.assertEqual(generate(s)['status'],'INVALID')
    def test_guard_no_emission_domain(self):
        with patch('generator.guarded_potential',return_value=None),patch('generator.invoke_i3') as check:r=generate(self.s());check.assert_not_called();self.assertTrue(all(c['status']=='UNAVAILABLE_TOPOLOGY' for c in r['candidates']))
        with patch('generator.reverse',side_effect=Domain('cap')):r=generate(self.s());self.assertEqual(r['status'],'UNAVAILABLE_DOMAIN');self.assertEqual(len(r['candidates']),12)
    def test_potential_mutations(self):
        s=self.s();r=generate(s);c=r['candidates'][0];statement=dict(s,weights=c['weights'],multiplier=c['multiplier'],potential=c['potential']);self.assertNotEqual(i3.check(statement)['status'],'INVALID')
        for k,v in ((0,1),(-1,100)):
            p=copy.deepcopy(statement);p['potential'][k]=v;self.assertEqual(i3.check(p)['status'],'INVALID')
        G,n,st,ar,pr=model(s);d=reverse(st,ar,G,(F(1),F(0)),F(0));d[1]=None
        with self.assertRaises(Failure):audit(s,(F(1),F(0)),F(0),st,d)
    def test_nonunique_max_with_actual_unreachable_and_mutations(self):
        # Source D=1; two incoming states from x/y each have suffix M=3,
        # neither reachable from source. Clamp must use them, not source subset.
        s={'graph':{'a':[self.e('g',[1,1])],'g':[],'x':[self.e('z',[0,0])],'y':[self.e('z',[0,0])],'z':[self.e('g',[3,3])],'u':[self.e('u',[0,0])]},'start':'a','goal':'g','budget':0,'forbidden':[],'penalties':[],'route':{'path':['a','g'],'edges':[{'source':'a','edge_index':0,'target':'g'}],'scenario_totals':[1,1],'worst_time':1,'exposure':0,'turn_penalty':0}}
        from proof import verify
        r=generate(s);verify(s,r);c=r['candidates'][0];self.assertEqual(c['clamp'],'3/1');self.assertGreaterEqual(c['distances'].count('3/1'),2);self.assertIn(None,c['distances']);self.assertIn('-2/1',c['potential'])
        for field,value in (('clamp','1/1'),('distances',['0/1']*len(c['distances'])),('potential',['0/1']*len(c['potential']))):
            rr=copy.deepcopy(r);rr['candidates'][0][field]=value
            with self.assertRaises(Failure):verify(s,rr)
        rr=copy.deepcopy(r);rr['candidates'][0]['states'][1]['incoming'][1]=False
        with self.assertRaises(Failure):verify(s,rr)
    def test_domain_caps_and_larger_than_source_clamp(self):
        s=self.s();s['graph']['x'][0]['scenario_times']=[i3.b3.MAX,i3.b3.MAX];s['graph']['x'][0]['exposure']=i3.b3.MAX;s['graph']['u'].append(self.e('x',[0,0]));r=generate(s);self.assertTrue(any(c['status']=='UNAVAILABLE_DOMAIN' for c in r['candidates']));self.assertEqual(len(r['candidates']),12)
    def test_revisit_and_json(self):
        s={'graph':{'a':[self.e('b',[1,1])],'b':[self.e('c',[1,1]),self.e('g',[1,1])],'c':[self.e('b',[1,1])],'g':[]},'start':'a','goal':'g','budget':0,'forbidden':[[['a',0],['b',1]]],'penalties':[],'route':{'path':['a','b','c','b','g'],'edges':[{'source':a,'edge_index':i,'target':b} for a,i,b in [('a',0,'b'),('b',0,'c'),('c',0,'b'),('b',1,'g')]],'scenario_totals':[4,4],'worst_time':4,'exposure':0,'turn_penalty':0}}
        self.assertEqual(generate(s)['status'],'CERTIFIED_INTEGRATED')
        from model import load_bytes
        for b in (b'{"x":1,"x":2}',b'{"x":NaN}',b'['*11+b'0'+b']'*11):
            with self.assertRaises(Invalid):load_bytes(b)
    def test_parent_schedule_independent(self):
        from proof import verify
        r=generate(self.s())
        with patch('generator.candidates',side_effect=RuntimeError('must not use shared schedule')):verify(self.s(),r)
