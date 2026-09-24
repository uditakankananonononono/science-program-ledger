"""Download MIT-BIH Arrhythmia DB (44 non-paced records) from physionet-open S3."""
import hashlib, glob, os, subprocess, datetime
DS1 = ['101','106','108','109','112','114','115','116','118','119','122','124',
       '201','203','205','207','208','209','215','220','223','230']
DS2 = ['100','103','105','111','113','117','121','123','200','202','210','212',
       '213','214','219','221','222','228','231','232','233','234']
base = 'https://physionet-open.s3.amazonaws.com/mitdb/1.0.0/'
os.makedirs('data', exist_ok=True)
for r in DS1 + DS2:
    for ext in ('dat', 'hea', 'atr'):
        f = f'data/{r}.{ext}'
        if not os.path.exists(f):
            subprocess.run(['curl', '-sfL', '--max-time', '120', '-o', f,
                            base + f'{r}.{ext}'], check=True)
h = hashlib.sha256()
for f in sorted(glob.glob('data/*')):
    h.update(open(f, 'rb').read())
open('data_provenance.txt', 'w').write(
    'retrieved %s UTC from %s\nsha256(concat of sorted files) %s\n' % (
        datetime.datetime.utcnow().isoformat(), base, h.hexdigest()))
print('done')
