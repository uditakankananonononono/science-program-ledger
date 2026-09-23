import subprocess, os, json, gzip
for l in open('data/sample.tsv'):
    acc=l.split('\t')[0]
    for kind,url in [('am',f'https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-aa-substitutions.csv'),('pl',f'https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-confidence_v6.json')]:
        p=f'data/af/{acc}.{kind}.gz'
        if os.path.exists(p): continue
        r=subprocess.run(['curl','-s','-f','--max-time','60',url],capture_output=True)
        if r.returncode==0 and r.stdout: open(p,'wb').write(gzip.compress(r.stdout))
print('done')
