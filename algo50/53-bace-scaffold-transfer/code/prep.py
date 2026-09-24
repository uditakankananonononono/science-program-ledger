"""Download BACE + BBBP CSVs from the MoleculeNet/DeepChem S3 mirror."""
import hashlib, subprocess, datetime, os
urls = {'bace.csv': 'https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/bace.csv',
        'BBBP.csv': 'https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv'}
os.makedirs('data', exist_ok=True)
for name, url in urls.items():
    if not os.path.exists('data/' + name):
        subprocess.run(['curl', '-sfL', '--max-time', '120', '-o', 'data/' + name, url], check=True)
with open('data/provenance.txt', 'w') as fh:
    for name, url in urls.items():
        b = open('data/' + name, 'rb').read()
        fh.write('%s retrieved %s UTC from %s\nsha256 %s\n\n' % (
            name, datetime.datetime.utcnow().isoformat(), url, hashlib.sha256(b).hexdigest()))
print('ok')
