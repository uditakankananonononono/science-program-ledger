import gzip, re, csv
genes={l.split('\t')[1] for l in open('data/sample.tsv')}
AA={'Ala':'A','Arg':'R','Asn':'N','Asp':'D','Cys':'C','Gln':'Q','Glu':'E','Gly':'G','His':'H','Ile':'I','Leu':'L','Lys':'K','Met':'M','Phe':'F','Pro':'P','Ser':'S','Thr':'T','Trp':'W','Tyr':'Y','Val':'V'}
pat=re.compile(r'\(p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})\)$')
STAR={'criteria provided, single submitter':1,'criteria provided, multiple submitters, no conflicts':2,'reviewed by expert panel':3,'practice guideline':4}
out=open('data/clinvar_missense_sample.tsv','w'); seen=set()
with gzip.open('data/variant_summary.txt.gz','rt',errors='replace') as f:
    next(f)
    for line in f:
        c=line.rstrip('\n').split('\t')
        if c[16]!='GRCh38' or c[1]!='single nucleotide variant' or c[4] not in genes: continue
        m=pat.search(c[2])
        if not m or m.group(1) not in AA or m.group(3) not in AA or m.group(1)==m.group(3): continue
        cs=c[6].lower(); st=STAR.get(c[24],0)
        if st<1: continue
        if cs in ('pathogenic','likely pathogenic','pathogenic/likely pathogenic'): y=1
        elif cs in ('benign','likely benign','benign/likely benign'): y=0
        else: continue
        v=f'{AA[m.group(1)]}{m.group(2)}{AA[m.group(3)]}'; k=(c[4],v)
        if k in seen: continue
        seen.add(k); out.write(f'{c[4]}\t{v}\t{y}\t{st}\t{c[8]}\t{c[30]}\n')
out.close(); print('variants',len(seen))
