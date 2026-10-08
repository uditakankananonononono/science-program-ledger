import admit as a,hashlib,unittest
from unittest.mock import patch
CAP={'depth':128,'nodes':200000,'text_characters':8388608,'attribute_characters':2097152}
def s(raw):return {'metadata_size':len(raw),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
class Tests(unittest.TestCase):
 def test_literals_paths(self):
  raw=b'<r xmlns="u"><x a="NaN">text</x>TAIL<x>Infinity</x><z><x>-0</x></z></r>'
  inv=a.inventory(raw,CAP);self.assertEqual(inv['element_count'],5)
  x=inv['elements'];self.assertEqual(x[1]['tail'],'TAIL');self.assertEqual(x[1]['attributes'],{'a':'NaN'});self.assertEqual(x[2]['text'],'Infinity')
  self.assertEqual(x[2]['path_segments'][-1]['same_expanded_name_sibling_ordinal_1based'],2);self.assertEqual(x[2]['path_segments'][-1]['expanded_name'],'{u}x')
  self.assertEqual([e['document_element_preorder_ordinal_1based'] for e in x],[1,2,3,4,5])
 def test_traps(self):
  for raw in (b'<!DOCTYPE r><r/>',b'<!DOCTYPE r [<!ENTITY x "x">]><r>&x;</r>',b'<!DOCTYPE r SYSTEM "https://example.invalid/evil"><r/>',b'<r><x></r>',b'<?xml version="1.0" encoding="iso-8859-1"?><r/>',b'<r>\xff</r>'):
   with patch('urllib.request.urlopen',side_effect=AssertionError('network trap')): inv=a.inventory(raw,CAP)
   self.assertNotIn('elements',inv);self.assertEqual(inv['status'],'unresolved_syntax_unsafe_encoding_or_cap')
 def test_caps_no_partial(self):
  for cap in ('depth','nodes','text_characters','attribute_characters'):
   caps=dict(CAP);caps[cap]=1
   inv=a.inventory(b'<r a="long"><x>long</x></r>',caps);self.assertNotIn('elements',inv)
 def test_no_processing(self):
  raw=b'<?xml-stylesheet href="https://example.invalid/x"?><r xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include href="https://example.invalid/y"/></r>'
  with patch('urllib.request.urlopen',side_effect=AssertionError('network trap')):inv=a.inventory(raw,CAP)
  self.assertEqual(inv['element_count'],2);self.assertIn('include',inv['elements'][1]['path_segments'][-1]['expanded_name'])
 def test_each_identity_gates_all(self):
  raws=[b'<r/>',b'<r/>'];selection={'files':[s(r) for r in raws]}
  for i in range(2):
   bad=list(raws);bad[i]=b'<bad/>'
   with patch('admit.inventory',side_effect=AssertionError('parse trap')):self.assertFalse(a.analyze(bad,selection,CAP)['analysis_performed'])
 def test_transport(self):
  class Response:
   status=200;headers={'Content-Length':'4'}
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def geturl(self):return 'x'
   def read(self,n):return b''
  class Opener:
   def open(self,*args,**kwargs):return Response()
  with self.assertRaises(ValueError):a.download('https://x',10,[10],Opener())
  self.assertIsNone(a.NoRedirect().redirect_request(None,None,None,None,None,None))
if __name__=='__main__':unittest.main()
