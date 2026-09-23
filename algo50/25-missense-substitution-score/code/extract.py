# ClinVar GRCh38 SNV missense, P/LP vs B/LB, review status with assertion criteria; dedup VariationID.
import gzip, re, csv
T={'Ala':'A','Arg':'R','Asn':'N','Asp':'D','Cys':'C','Gln':'Q','Glu':'E','Gly':'G','His':'H','Ile':'I','Leu':'L','Lys':'K','Met':'M','Phe':'F','Pro':'P','Ser':'S','Thr':'T','Trp':'W','Tyr':'Y','Val':'V'}
POS={'Pathogenic','Likely pathogenic','Pathogenic/Likely pathogenic'}; NEG={'Benign','Likely benign','Benign/Likely benign'}
OK={'criteria provided, single submitter','criteria provided, multiple submitters, no conflicts','reviewed by expert panel','practice guideline'}
pat=re.compile(r'\(p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})\)$'); seen=set(); n=[0,0]
with open('../data/missense.tsv','w') as out:
    out.write('variation_id\tgene\tref\tpos\talt\tlabel\treview\n')
    f=gzip.open('../data/variant_summary.txt.gz','rt'); h=next(f).lstrip('#').rstrip('\n').split('\t'); I={k:i for i,k in enumerate(h)}
    for l in f:
        p=l.rstrip('\n').split('\t')
        if p[I['Assembly']]!='GRCh38' or p[I['Type']]!='single nucleotide variant': continue
        cs=p[I['ClinicalSignificance']]; rs=p[I['ReviewStatus']]
        if rs not in OK or (cs not in POS and cs not in NEG): continue
        m=pat.search(p[I['Name']])
        if not m or m.group(1) not in T or m.group(3) not in T or m.group(1)==m.group(3): continue
        v=p[I['VariationID']]
        if v in seen: continue
        seen.add(v); y=int(cs in POS); n[y]+=1
        out.write('\t'.join([v,p[I['GeneSymbol']],T[m.group(1)],m.group(2),T[m.group(3)],str(y),rs])+'\n')
print('benign',n[0],'pathogenic',n[1])
