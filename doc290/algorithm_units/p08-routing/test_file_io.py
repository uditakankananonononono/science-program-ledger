import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from test_runner import BASE

class FileInputTests(unittest.TestCase):
    def run_path(self,path):
        return subprocess.run([sys.executable,'runner.py',str(path)],text=True,capture_output=True)
    def assert_error(self,proc):
        self.assertEqual(proc.returncode,2)
        self.assertEqual(proc.stdout,'')
        self.assertEqual(json.loads(proc.stderr)['status'],'error')
        self.assertNotIn('Traceback',proc.stderr)
    def test_regular_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'graph.json';path.write_text(json.dumps(BASE))
            proc=self.run_path(path)
            self.assertEqual(proc.returncode,0)
            self.assertEqual(json.loads(proc.stdout)['result']['worst_time'],3)
    def test_missing_path(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assert_error(self.run_path(Path(directory)/'absent.json'))
    def test_directory_path(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assert_error(self.run_path(directory))
    def test_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'invalid.json';path.write_bytes(b'\xff\xfe')
            self.assert_error(self.run_path(path))
