import random,json
from collections import defaultdict
D=[];h=None;s=[]
for l in open('../172-protein-grammar/data/scope40.fa'):
    if l.startswith('>'):
        if h: D.append((h,''.join(s).upper()))
        h=l[1:].split()[:2];s=[]
    else: s.append(l.strip())
D.append((h,''.join(s).upper()))
D=[(i,c,q) for (i,c),q in D if c[0] in 'abcd' and 50<=len(q)<=300 and set(q)<=set('ACDEFGHIKLMNPQRSTVWYX')]
fold=lambda c:'.'.join(c.split('.')[:2]);sf=lambda c:'.'.join(c.split('.')[:3])
F=defaultdict(lambda:defaultdict(list))
for d in D: F[fold(d[1])][sf(d[1])].append(d)
ok=[f for f in F if sum(len(v)>=3 for v in F[f].values())>=2]
s1=json.load(open('../../ledger/exp200/172-protein-grammar/results/ids_p1.json'))
byid={d[0]:d for d in D};used={sf(byid[i][1]) for i in s1['q']}
R=random.Random(7);qs=[];refs=[]
for f in sorted(ok):
    good=sorted(k for k,v in F[f].items() if len(v)>=3);alt=[k for k in good if k not in used] or good
    q=R.choice(alt);qs+=F[f][q];refs+=[d for k,v in F[f].items() if k!=q for d in R.sample(v,min(8,len(v)))]
R.shuffle(qs);qs=qs[:300];other=[d for d in D if fold(d[1]) not in ok];R.shuffle(other);refs=(refs+other)[:1500]
json.dump(dict(q=[d[0] for d in qs],r=[d[0] for d in refs]),open('results/ids_split2.json','w'))
print(len(qs),len(refs),'overlap q with s1',len(set(d[0] for d in qs)&set(s1['q'])))
