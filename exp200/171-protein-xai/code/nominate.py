import sys;sys.path.insert(0,'code');from predict import score
best=None
for l in open('data/nominate_pool.tsv').read().split('\n')[1:]:
    if not l: continue
    a,name,gene,ec,seq=l.split('\t');p=score(seq);i=max(range(len(p)),key=p.__getitem__)
    top5=sorted(range(len(p)),key=lambda j:-p[j])[:5]
    if best is None or p[i]>best[0]: best=(p[i],a,gene,name,ec,f'{seq[i]}{i+1}',[f'{seq[j]}{j+1}:{p[j]:.2f}' for j in top5])
print(best);open('results/nomination.txt','w').write(repr(best))
