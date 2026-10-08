import copy,json,unittest,unittest.mock as mock
import admit as a
class Tests(unittest.TestCase):
 def fixture(self):
  rs=[b'a\r\n\n',b'{"n":1,"b":false,"x":[{"v":"0"}]}',b'[null,"x"]',b'last']
  sel={'files':[{'path':f'{i}.json' if i in [1,2] else f'{i}.md','bytes':len(b),'sha256':a.sha(b),'git_blob_oid':a.oid(b)} for i,b in enumerate(rs)],'max_file_bytes':131072,'max_aggregate_bytes':524288}
  schemas={r['path']:a.schema(a.strict(b)) for r,b in zip(sel['files'],rs) if r['path'].endswith('.json')};return rs,sel,schemas
 def test_admission_coordinates(self):
  rs,s,t=self.fixture();x=a.inspect(rs,s,t);self.assertTrue(x['status'].startswith('ALL4'));self.assertEqual(x['files']['0.md'][-1]['final_empty'],True);self.assertEqual(x['files']['0.md'][1]['byte_offset'],3)
 def test_all_identity_before_analysis(self):
  for i in range(4):
   rs,s,t=self.fixture();rs[i]+=b'x'
   with mock.patch.object(a,'strict',side_effect=AssertionError('analysis')) as spy:
    self.assertFalse(a.inspect(rs,s,t)['partial_inventory']);spy.assert_not_called()
 def test_strict_json(self):
  for b in [b'{"x":1,"x":2}',b'{"x":NaN}',b'\xff']:
   with self.assertRaises((ValueError,UnicodeError)):a.strict(b)
 def test_schema_bool_and_shape(self):
  s=a.schema({'n':1,'rows':[{'x':'0'}]})
  for x in [{'n':True,'rows':[{'x':'0'}]},{'n':1,'rows':[]},{'n':1,'rows':[{'x':0}]},{'n':1,'rows':[{'x':'0'}],'extra':0}]:
   with self.assertRaises(ValueError):a.validate(x,s)
 def test_unavailable_no_partial(self):
  rs,s,t=self.fixture();t['1.json']['fields']['n']['kind']='bool';x=a.inspect(rs,s,t);self.assertNotIn('files',x)
if __name__=='__main__':unittest.main()
