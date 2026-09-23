import gzip, csv, random, json, collections
random.seed(1)
AA=set("ACDEFGHIKLMNPQRSTVWY")
rows=[]
with gzip.open('data/human_sprot.tsv.gz','rt') as f:
    r=csv.DictReader(f,delimiter='\t')
    for x in r:
        pf=[p for p in x['Pfam'].split(';') if p]
        s=x['Sequence']
        if len(pf)==1 and 80<=len(s)<=600 and set(s)<=AA:
            rows.append((x['Entry'],pf[0],s))
fam=collections.defaultdict(list)
for a,p,s in rows: fam[p].append((a,s))
elig=sorted(p for p,v in fam.items() if len(v)>=6)
fams=sorted(random.sample(elig,min(120,len(elig))))
out=[]
for p in fams:
    mem=sorted(fam[p]); random.shuffle(mem)
    for a,s in mem[:10]: out.append({'acc':a,'fam':p,'seq':s})
json.dump(out,open('data/set.json','w'))
print('single-pfam proteins',len(rows),'eligible fams',len(elig),'sampled fams',len(fams),'proteins',len(out))
