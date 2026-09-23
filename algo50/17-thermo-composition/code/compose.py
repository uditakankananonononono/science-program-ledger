# Resumable: amino-acid counts per proteome from UniProt FASTA stream.
import urllib.request, os, time, csv
AA='ACDEFGHIKLMNPQRSTVWY'; out='../results/composition.tsv'
done=set(l.split('\t')[0] for l in open(out)) if os.path.exists(out) else set()
if not done: open(out,'w').write('upid\trelease\tn_prot\t'+'\t'.join(AA)+'\n')
for row in csv.DictReader(open('../data/selected.tsv'),delimiter='\t'):
    u=row['upid']
    if u in done: continue
    for attempt in range(3):
        try:
            req=urllib.request.urlopen('https://rest.uniprot.org/uniprotkb/stream?query=proteome:%s&format=fasta'%u,timeout=120)
            rel=req.headers.get('X-UniProt-Release',''); txt=req.read().decode(); break
        except Exception as e: time.sleep(5); txt=None
    if txt is None: continue
    c=dict.fromkeys(AA,0); n=0
    for line in txt.splitlines():
        if line.startswith('>'): n+=1; continue
        for a in AA: c[a]+=line.count(a)
    with open(out,'a') as f: f.write('\t'.join([u,rel,str(n)]+[str(c[a]) for a in AA])+'\n')
