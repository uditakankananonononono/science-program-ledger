#!/usr/bin/env python3
"""fetch_seq.py CHROM - tile chromosome reference sequence from UCSC API -> results/local/<chrom>.fa (gitignored)."""
import sys, requests
chrom=sys.argv[1]
LENS={'chr21':46709983,'chr22':50818468}
TILE=900_000
out=open(f'results/local/{chrom}.fa','w'); out.write(f'>{chrom}\n')
a=0; n=0
while a<LENS[chrom]:
    b=min(a+TILE,LENS[chrom])
    for t in range(4):
        try:
            r=requests.get(f'https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom={chrom};start={a};end={b}',timeout=60)
            if r.status_code==200:
                dna=r.json().get('dna','').upper()
                if len(dna)==b-a:
                    out.write(dna+'\n'); n+=1; break
        except Exception: pass
    else:
        print(f'FAIL tile {a}',flush=True); break
    if n%10==0: print(f'{chrom} {b}/{LENS[chrom]}',flush=True)
    a=b
out.close(); print(f'DONE {chrom} tiles={n}',flush=True)
