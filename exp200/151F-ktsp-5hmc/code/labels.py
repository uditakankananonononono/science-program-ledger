import gzip,collections
R={}
for l in gzip.open('GSE89570_sm.txt.gz','rt'):
    if l.startswith('!Sample_'):
        f=[x.strip('"') for x in l.rstrip('\n').split('\t')];R.setdefault(f[0],[]).append(f[1:])
ch=R['!Sample_characteristics_ch1'];desc=R['!Sample_description'][2]
rows=[]
for i in range(len(desc)):
    d={c[i].split(': ')[0]:c[i].split(': ',1)[-1] for c in ch};rows.append((desc[i],d.get('tissue'),d.get('disease site'),d.get('disease state')))
print(collections.Counter((r[1],r[2],r[3]) for r in rows))
