import admit as a,json,unittest
class Tests(unittest.TestCase):
 def test_grammar(self):
  x=a.lines(b'A\r\n\rB\nC\v\xc2\x85\xe2\x80\xa8');self.assertEqual([r['byte_offset_0based'] for r in x],[0,3,4,6]);self.assertIn('\u2028',x[-1]['text']);self.assertEqual(len(a.lines(b'\n')),1);self.assertEqual(a.lines(b''),[])
 def test_strict(self):
  for raw in (b'{"x":1,"x":2}',b'{"x":NaN}',b'\xff'):
   with self.assertRaises((ValueError,UnicodeError)):a.strict(raw)
 def test_all5_gate(self):
  raws=[b'x']*5;s={'max_file_bytes':1,'max_total_bytes':5,'files':[{'path':str(i),'bytes':1,'sha256':a.sha(b'x'),'git_blob_sha1':a.blob(b'x')} for i in range(5)]}
  a.gate(raws,s)
  for i in range(5):
   bad=list(raws);bad[i]=b'z';r=a.inspect(bad,s);self.assertNotIn('files',r);self.assertFalse(r['partial_inventory_exposed'])
 def test_metadata(self):
  ms=[{'ordinal_1based':i,'raw_bytes':389460137 if i==628 else 0,'line_count':1,'inventory_filename':str(i),'inventory_sha256':'a'*64} for i in range(628,673)]
  summary={'status':'all_selected_raw_literal_text_inventories','members':ms,'total_lines':45};hashes={**{str(i):{'sha256':'a'*64,'bytes':1} for i in range(628,673)},'summary.json':{'sha256':'a'*64,'bytes':1},'manifest.json':{'sha256':'a'*64,'bytes':1}};a.consistency(summary,hashes)
  ms[0]['line_count']=True
  with self.assertRaises(ValueError):a.consistency(summary,hashes)
if __name__=='__main__':unittest.main()
