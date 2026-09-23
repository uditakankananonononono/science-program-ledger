import json, subprocess
tg=json.load(open('data/targets.json'))
acc=sorted({c['accession'] for t in tg if t.get('organism')=='Homo sapiens' and t.get('target_type')=='SINGLE PROTEIN' for c in t.get('target_components',[]) if c.get('accession')})
print('accessions',len(acc))
out=open('data/uniprot_targets.tsv','w'); hdr=True
for i in range(0,len(acc),100):
    q='+OR+'.join('accession:'+a for a in acc[i:i+100])
    t=subprocess.run(['curl','-s','--max-time','90',f'https://rest.uniprot.org/uniprotkb/search?query=({q})&fields=accession,gene_primary,xref_interpro,sequence&format=tsv&size=500'],capture_output=True,text=True).stdout
    lines=t.strip().split('\n'); out.write('\n'.join(lines if hdr else lines[1:])+'\n'); hdr=False
out.close()
