import gzip, re, csv, sys
AA3={'Ala':'A','Arg':'R','Asn':'N','Asp':'D','Cys':'C','Gln':'Q','Glu':'E','Gly':'G','His':'H','Ile':'I','Leu':'L','Lys':'K','Met':'M','Phe':'F','Pro':'P','Ser':'S','Thr':'T','Trp':'W','Tyr':'Y','Val':'V'}
pat=re.compile(r'\(p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})\)$')
ok_rev={'criteria provided, multiple submitters, no conflicts','reviewed by expert panel','practice guideline'}
P={'Pathogenic','Likely pathogenic','Pathogenic/Likely pathogenic'}
B={'Benign','Likely benign','Benign/Likely benign'}
out=csv.writer(open('data/missense_2star.tsv','w'),delimiter='\t')
out.writerow(['gene','wt','pos','mut','label','last_eval','variation_id','review'])
seen=set();n=0
with gzip.open('data/variant_summary.txt.gz','rt') as f:
    next(f)
    for line in f:
        c=line.rstrip('\n').split('\t')
        if c[1]!='single nucleotide variant' or c[16]!='GRCh38': continue
        if c[24] not in ok_rev: continue
        cs=c[6]
        if cs in P: lab=1
        elif cs in B: lab=0
        else: continue
        m=pat.search(c[2])
        if not m or m.group(1) not in AA3 or m.group(3) not in AA3: continue
        gene=c[4]
        if ';' in gene or gene=='-': continue
        key=(gene,m.group(2),m.group(3))
        if key in seen: continue
        seen.add(key)
        out.writerow([gene,AA3[m.group(1)],m.group(2),AA3[m.group(3)],lab,c[8],c[30],c[24]]); n+=1
print('rows',n)
