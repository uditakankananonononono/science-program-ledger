# Positives: proteins whose EVERY TRANSMEM segment carries structure/experimental evidence (ECO:0007744 or ECO:0000269).
import re, json, random
AA=set('ACDEFGHIKLMNPQRSTVWY'); pos=[]
for l in list(open('../data/tm.tsv'))[1:]:
    acc,fam,org,ft,seq=l.rstrip('\n').split('\t')
    segs=[];ok=True
    for m in re.finditer(r'TRANSMEM (\d+)\.\.(\d+);(.*?)/evidence="([^"]*)"',ft):
        if not re.search(r'ECO:0007744|ECO:0000269',m.group(4)): ok=False
        segs.append([int(m.group(1))-1,int(m.group(2))])
    if ok and segs and set(seq)<=AA and 'Beta stranded' not in ft: pos.append({'acc':acc,'fam':fam or acc,'seq':seq,'segs':segs})
neg=[]
for l in list(open('../data/soluble.tsv'))[1:]:
    acc,fam,seq=l.rstrip('\n').split('\t')
    if set(seq)<=AA: neg.append({'acc':acc,'fam':fam or acc,'seq':seq})
random.seed(19); neg=random.sample(neg,min(1500,len(neg)))
json.dump(pos,open('../data/pos.json','w')); json.dump(neg,open('../data/neg.json','w'))
print(len(pos),'pos',sum(len(p['segs']) for p in pos),'segs',len({p['fam'] for p in pos}),'fams;',len(neg),'neg')
