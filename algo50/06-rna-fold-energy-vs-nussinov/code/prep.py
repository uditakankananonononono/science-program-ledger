import gzip, json, random, hashlib, time
def parse_sto(path):
    seqs={}; ss=None
    for line in open(path):
        line=line.rstrip('\n')
        if not line or line.startswith('# STOCKHOLM') or line.strip()=='//': continue
        if line.startswith('#=GC SS_cons'):
            c=line.split()[-1]; ss=(ss or '')+c
        elif line.startswith('#'): continue
        else:
            p=line.split()
            if len(p)==2: seqs[p[0]]=seqs.get(p[0],'')+p[1]
    return seqs,ss
def pairs_from_ss(ss):
    stacks={'(':[],'<':[],'[':[],"{":[]}
    close={')':'(', '>':'<', ']':'[', '}':"{"}
    pairs=[]
    for i,c in enumerate(ss):
        if c in stacks: stacks[c].append(i)
        elif c in close and stacks[close[c]]: pairs.append((stacks[close[c]].pop(),i))
    return pairs
random.seed(1)
out={}
for fam in ('RF00005','RF00001'):
    seqs,ss=parse_sto(f'data/{fam}.sto')
    ref=pairs_from_ss(ss)
    rows=[]
    seen=set()
    for name,aln in seqs.items():
        s=''.join(c for c in aln if c!='.' and c!='-').upper().replace('T','U')
        if not s or set(s)-set('ACGU') or s in seen: continue
        # map columns to sequence index
        col2pos={}; pos=0
        for i,c in enumerate(aln):
            if c not in '.-': col2pos[i]=pos; pos+=1
        rp=[(col2pos[a],col2pos[b]) for a,b in ref if a in col2pos and b in col2pos]
        # require the sequence covers >=80% of consensus pairs
        if len(rp)<0.8*len(ref): continue
        seen.add(s)
        rows.append(dict(name=name,seq=s,ref=rp))
    random.shuffle(rows)
    out[fam]=rows[:100]
    print(fam,'kept',len(rows),'using',len(out[fam]),'refpairs',len(ref))
json.dump(out,open('data/eval.json','w'))
open('data/retrieved_at.txt','w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
with open('data/SHA256_raw.txt','w') as f:
    f.write(hashlib.sha256(open('data/Rfam.seed.gz','rb').read()).hexdigest()+'  Rfam.seed.gz\n')
    f.write(hashlib.sha256(open('data/eval.json','rb').read()).hexdigest()+'  eval.json\n')
