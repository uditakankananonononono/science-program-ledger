import hashlib, json, random, subprocess, time, os
os.makedirs('data', exist_ok=True)
# 1. fetch reference if missing
ref_path='data/NC_000913.3.fa'
if not os.path.exists(ref_path):
    url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta&retmode=text'
    subprocess.run(['curl','-sL',url,'-o',ref_path],check=True)
with open(ref_path) as f:
    open('data/retrieved_at.txt','w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
    h=hashlib.sha256(open(ref_path,'rb').read()).hexdigest()
    open('data/SHA256_raw.txt','w').write(h+'  NC_000913.3.fa\n')
ref=''.join(l.strip() for l in open(ref_path) if not l.startswith('>')).upper()
assert set(ref)<=set('ACGT'), set(ref)-set('ACGT')
G=len(ref); print('genome',G)
# 2. simulate reads, seed 1
rng=random.Random(1)
comp=str.maketrans('ACGT','TGCA')
meta=[]
with open('data/reads.fa','w') as out:
    rid=0
    for eps in (0.05,0.10,0.15):
        for j in range(200):
            L=rng.randint(3000,12000)
            s=rng.randint(0,G-L)
            seq=ref[s:s+L]
            strand='+'
            if rng.random()<0.5:
                seq=seq.translate(comp)[::-1]; strand='-'
            # errors: 90% sub, 5% ins, 5% del
            nerr=int(round(eps*L))
            types=rng.choices(['sub','ins','del'],weights=[0.90,0.05,0.05],k=nerr)
            # apply at distinct random positions (positions refer to current seq; rebuild via list)
            seq=list(seq)
            ops=sorted(rng.sample(range(len(seq)),min(nerr,len(seq))), reverse=True)
            for typ,pos in zip(types,ops):
                if typ=='sub': seq[pos]=rng.choice('ACGT')
                elif typ=='ins': seq.insert(pos,rng.choice('ACGT'))
                else: del seq[pos]
            seq=''.join(seq)
            out.write(f'>r{rid} eps={eps} start={s} len={L} strand={strand}\n')
            for i in range(0,len(seq),80): out.write(seq[i:i+80]+'\n')
            meta.append(dict(id=f'r{rid}',eps=eps,start=s,len=L,strand=strand))
            rid+=1
json.dump(meta,open('data/manifest.json','w'))
h=hashlib.sha256(open('data/reads.fa','rb').read()).hexdigest()
open('data/SHA256_raw.txt','a').write(h+'  reads.fa\n')
print('reads',rid)
