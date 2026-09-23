import gzip, random, json
AA=set('ACDEFGHIKLMNPQRSTVWY'); recs={}; cur=None; buf=[]
def flush():
    if cur: recs[cur]=''.join(buf)
for line in gzip.open('../data/ss.txt.gz','rt'):
    line=line.rstrip('\n')
    if line.startswith('>'):
        flush(); cur=line[1:]; buf=[]
    else: buf.append(line)
flush()
seen=set(); chains=[]
for k,v in recs.items():
    if not k.endswith(':sequence'): continue
    base=k[:-9]; s=v; ss=recs.get(base+':secstr','')
    ss=ss.ljust(len(s))[:len(s)]
    if 50<=len(s)<=400 and set(s)<=AA and s not in seen:
        seen.add(s); chains.append((base,s,ss))
random.seed(21); pick=random.sample(chains,1500)
m={'H':'H','G':'H','I':'H','E':'E','B':'E'}
out=[{'id':b,'seq':s,'ss3':''.join(m.get(c,'C') for c in ss)} for b,s,ss in pick]
json.dump(out,open('../data/chains.json','w'))
print(len(chains),'unique eligible;',len(out),'picked;',sum(len(o['seq']) for o in out),'residues')
