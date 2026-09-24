#!/usr/bin/env python3
"""ccre_cache.py - download encodeCcreCombined intervals for chr21/chr22 in 2Mb tiles -> results/local/ccre_<chrom>.txt (start-end per line)."""
import requests, sys
API='https://api.genome.ucsc.edu/getData/track?genome=hg38;track=encodeCcreCombined'
LENS={'chr21':46709983,'chr22':50818468}
for chrom in ['chr21','chr22']:
    out=open(f'results/local/ccre_{chrom}.txt','w'); n=0
    a=0
    while a<LENS[chrom]:
        b=min(a+2_000_000,LENS[chrom])
        r=requests.get(f'{API};chrom={chrom};start={a};end={b}',timeout=30)
        if r.status_code==200:
            for d in r.json().get('encodeCcreCombined',[]):
                out.write(f"{d['chromStart']}-{d['chromEnd']}\n"); n+=1
        a=b
    out.close(); print(chrom,n,'intervals',flush=True)
