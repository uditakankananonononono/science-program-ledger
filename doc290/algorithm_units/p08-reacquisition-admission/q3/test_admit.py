import hashlib,json,tempfile,unittest,unittest.mock as mock
from pathlib import Path
import admit as a
class Tests(unittest.TestCase):
    def test_info(self):
        self.assertEqual(a.info_pages(b'Pages: 2\nEncrypted: no\n'),2)
        for s in [b'Pages: 33\nEncrypted: no\n',b'Pages: 0\nEncrypted: no\n',b'Pages: 1\nPages: 2\nEncrypted: no\n',b'Pages: 1\nEncrypted: yes\n',b'Pages: 1\n']:
            with self.assertRaises(ValueError):a.info_pages(s)
    def test_grammar(self):
        p=a.text_pages(b'a\n\n\f\f',2);self.assertEqual(p[0]['lines'],['a','','']);self.assertTrue(p[1]['blank_or_nontext'])
        for s in [b'a',b'a\f\n',b'a\f\f',b'\xff\f']:
            with self.assertRaises((ValueError,UnicodeError)):a.text_pages(s,1)
    def test_dimensions(self):
        self.assertEqual(a.dimensions(b'Page 1 size: 612 x 792 pts (letter)\nPage 1 rot: 0\n',1),(1275,1650))
        for s in [b'Page 1 size: 99999 x 99999 pts\nPage 1 rot: 0\n',b'Page 1 size: 0 x 792 pts\nPage 1 rot: 0\n',b'Page 1 size: 612 x 792 pts\nPage 1 rot: 5\n',b'Page 1 size: nan x inf pts\nPage 1 rot: 0\n']:
            with self.assertRaises(ValueError):a.dimensions(s,1)
    def test_identity_before_parser(self):
        with tempfile.TemporaryDirectory() as d,mock.patch.object(a,'command',side_effect=AssertionError('parser')) as spy:
            src=Path(d)/'source';src.write_bytes(b'wrong');out=Path(d)/'out'
            with self.assertRaises(ValueError):a.run(src,out,{'bytes':4,'sha256':'wrong'})
            spy.assert_not_called();self.assertFalse(out.exists());self.assertEqual(sorted(p.name for p in Path(d).iterdir()),['source'])
    def test_native_synthetic(self):
        from reportlab.pdfgen import canvas
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture.pdf';c=canvas.Canvas(str(p),pagesize=(612,792));c.drawString(50,700,'Synthetic fixture only');c.showPage();c.showPage();c.save()
            sel={'bytes':p.stat().st_size,'sha256':a.hashpath(p),'max_render_bytes':134217728}
            m=a.run(p,Path(d)/'out',sel);self.assertEqual(m['pages'],2);self.assertFalse(m['visual_coverage_complete'])
    def test_parser_failure_cleanup(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'fixture';p.write_bytes(b'fixture');sel={'bytes':7,'sha256':a.hashpath(p)}
            with mock.patch.object(a,'command',side_effect=ValueError('parse')):
                with self.assertRaises(ValueError):a.run(p,Path(d)/'out',sel)
            self.assertEqual([x.name for x in Path(d).iterdir()],['fixture'])
if __name__=='__main__':unittest.main()
