import os, subprocess
recs = ([f'a{i:02d}' for i in range(1,21)] + [f'b{i:02d}' for i in range(1,6)]
        + [f'c{i:02d}' for i in range(1,11)])
base = 'https://physionet-open.s3.amazonaws.com/apnea-ecg/1.0.0/'
os.makedirs('data', exist_ok=True)
for r in recs:
    for ext in ('dat', 'hea', 'apn'):
        f = f'data/{r}.{ext}'
        if not os.path.exists(f):
            subprocess.run(['curl', '-sL', '--max-time', '120', '-o', f,
                            base + f'{r}.{ext}'], check=True)
    print(r, os.path.getsize(f'data/{r}.dat'))

# after fetch: record sha256 + retrieval time for provenance (raw stays uncommitted)
import hashlib, glob, datetime
h = hashlib.sha256()
for f in sorted(glob.glob('data/*')):
    h.update(open(f, 'rb').read())
open('data_provenance.txt', 'w').write(
    'retrieved %s UTC from %s\nsha256(concat of sorted files) %s\n' % (
        datetime.datetime.utcnow().isoformat(), base, h.hexdigest()))
