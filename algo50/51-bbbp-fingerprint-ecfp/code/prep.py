"""Download BBBP.csv from the MoleculeNet/DeepChem S3 mirror."""
import hashlib, subprocess, datetime, os
url = 'https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv'
os.makedirs('data', exist_ok=True)
if not os.path.exists('data/BBBP.csv'):
    subprocess.run(['curl', '-sfL', '--max-time', '120', '-o', 'data/BBBP.csv', url], check=True)
b = open('data/BBBP.csv', 'rb').read()
open('data/provenance.txt', 'w').write(
    'retrieved %s UTC from %s\nsha256 %s\n' % (
        datetime.datetime.utcnow().isoformat(), url, hashlib.sha256(b).hexdigest()))
print('ok', len(b))
