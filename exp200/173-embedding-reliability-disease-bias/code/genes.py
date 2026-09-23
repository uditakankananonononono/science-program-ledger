import subprocess, json, random
random.seed(0)
u='https://rest.uniprot.org/uniprotkb/stream?query=reviewed:true+AND+organism_id:9606+AND+database:orphanet&fields=accession,gene_primary,length,lit_pubmed_id,xref_orphanet&format=tsv'
t=subprocess.run(['curl','-s','--max-time','110',u],capture_output=True,text=True).stdout
open('data/uniprot_orphanet.tsv','w').write(t)
rows=[l.split('\t') for l in t.strip().split('\n')[1:]]
rows=[r for r in rows if r[1] and int(r[2])<=2700]
print('orphanet genes',len(rows))
pick=random.sample(rows,600)
open('data/sample.tsv','w').write(''.join(f"{r[0]}\t{r[1].split(';')[0].strip()}\t{r[2]}\t{len([x for x in r[3].split(';') if x.strip()])}\n" for r in pick))
