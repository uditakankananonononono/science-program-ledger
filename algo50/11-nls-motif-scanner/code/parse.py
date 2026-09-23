# Keep proteins with >=1 experimentally supported (ECO:0000269) NLS motif; record segments.
import re, json
rows=[l.rstrip('\n').split('\t') for l in open('../data/nls_all.tsv')][1:]
out=[]
for acc,org,fam,mot,seq in rows:
    segs=[]
    for m in re.finditer(r'MOTIF (\d+)\.\.(\d+); /note="([^"]*)"; /evidence="([^"]*)"',mot):
        if 'uclear localization' in m.group(3) and 'ECO:0000269' in m.group(4):
            segs.append([int(m.group(1))-1,int(m.group(2))])
    if segs and set(seq)<=set('ACDEFGHIKLMNPQRSTVWY'):
        out.append({'acc':acc,'org':org,'fam':fam or acc,'seq':seq,'segs':segs})
json.dump(out,open('../data/pos.json','w'))
neg=[l.rstrip('\n').split('\t') for l in open('../data/neg_secreted.tsv')][1:]
neg=[{'acc':a,'fam':f or a,'seq':s} for a,f,s in neg if set(s)<=set('ACDEFGHIKLMNPQRSTVWY')]
json.dump(neg,open('../data/neg.json','w'))
print(len(out),'pos proteins',sum(len(p['segs']) for p in out),'segments',len({p['fam'] for p in out}),'families;',len(neg),'neg')
