import random
H='LIVMFA'; P='STNQEDKR'; NCAP='STND'; CCAP='GN'; LOOP='GSTN'
def design_one(rng):
    nblocks=rng.choice([1,1,2])
    parts=[]
    for b in range(nblocks):
        nrep=rng.randint(3,5)
        body=''.join(rng.choice(H)+rng.choice(P)+rng.choice(P)+rng.choice(H)+rng.choice(P)+rng.choice(P)+rng.choice(H) for _ in range(nrep))
        body=rng.choice(NCAP)+body+rng.choiceCCAP() if False else rng.choice(NCAP)+body+rng.choice(CCAP)
        parts.append(body)
    seq=parts[0]
    for b in range(1,nblocks):
        seq+=''.join(rng.choice(LOOP) for _ in range(rng.randint(3,6)))+parts[b]
    return seq[:70]
def charge(s): return sum(1 for c in s if c in 'KR')-sum(1 for c in s if c in 'DE')
def main():
    rng=random.Random(42)
    out=[]
    while len(out)<200:
        s=design_one(rng)
        c=charge(s)
        if not (2<=c<=6): continue
        if 'P' in s[2:-2] and False: continue
        # R2: no Pro/Gly in helix interiors - designer never places Pro; Gly only via C-cap/loops
        if 24<=len(s)<=70: out.append(s)
    rng2=random.Random(43)
    with open('results/designed.fasta','w') as f, open('results/baseline.fasta','w') as g:
        for i,s in enumerate(out):
            f.write(f'>des{i}\n{s}\n')
            l=list(s); rng2.shuffle(l); g.write(f'>base{i}\n{"".join(l)}\n')
    print('designed',len(out),'median len',sorted(len(s) for s in out)[100])
if __name__=='__main__': main()
