"""Download MIT-BIH AFDB (23 records) from the physionet-open S3 mirror."""
import hashlib, glob, os, subprocess, datetime
RECS = ['04015','04043','04048','04126','04746','04908','04936','05091','05121',
        '05261','06426','06453','06995','07162','07859','07879','07910','08215',
        '08219','08378','08405','08434','08455']
base = 'https://physionet-open.s3.amazonaws.com/afdb/1.0.0/'
os.makedirs('data', exist_ok=True)
for r in RECS:
    for ext in ('dat', 'hea', 'atr'):
        f = f'data/{r}.{ext}'
        if not os.path.exists(f):
            subprocess.run(['curl', '-sfL', '--max-time', '300', '-o', f,
                            base + f'{r}.{ext}'], check=True)
h = hashlib.sha256()
for f in sorted(glob.glob('data/*')):
    h.update(open(f, 'rb').read())
open('data_provenance.txt', 'w').write(
    'retrieved %s UTC from %s\nsha256(concat of sorted files) %s\n' % (
        datetime.datetime.utcnow().isoformat(), base, h.hexdigest()))
print('done')
