"""Download ClinTox + HIV from the MoleculeNet/DeepChem S3 mirror."""
import hashlib, subprocess, datetime, os
urls = {'clintox.csv.gz': 'https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/clintox.csv.gz',
        'HIV.csv': 'https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/HIV.csv'}
os.makedirs('data', exist_ok=True)
for name, url in urls.items():
    if not os.path.exists('data/' + name):
        subprocess.run(['curl', '-sfL', '--max-time', '300', '-o', 'data/' + name, url], check=True)
if not os.path.exists('data/clintox.csv'):
    subprocess.run(['gunzip', '-kf', 'data/clintox.csv.gz'], check=True)
with open('data/provenance.txt', 'w') as fh:
    for name in ('clintox.csv', 'HIV.csv'):
        b = open('data/' + name, 'rb').read()
        fh.write('%s retrieved %s UTC from %s\nsha256 %s\n\n' % (
            name, datetime.datetime.utcnow().isoformat(), urls[name if name != 'clintox.csv' else 'clintox.csv.gz'],
            hashlib.sha256(b).hexdigest()))
print('ok')
