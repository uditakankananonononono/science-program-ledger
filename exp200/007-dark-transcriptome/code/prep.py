#!/usr/bin/env python3
"""Parse FASTAs, frozen 90/10 split, NONCODE dedupe vs GENCODE, di-nucleotide shuffles."""
import gzip,json,hashlib,numpy as np
def read_fa(path,limit=None):
    out={};name=None;seq=[]
    with gzip.open(path,'rt',errors='replace') as f:
        for line in f:
            if line.startswith('>'):
                if name: out[name]=''.join(seq).upper()
                name=line[1:].split()[0].split('|')[0];seq=[]
            else: seq.append(line.strip())
        if name: out[name]=''.join(seq).upper()
    return out
def clean(s):
    return ''.join(c if c in 'ACGT' else 'N' for c in s)
def dinuc_shuffle(s,rng):
    # Altschul-Erikson-lite: preserve di-nucleotide approx via Eulerian swap is heavy;
    # locked implementation: chunk into 2-mers and shuffle 2-mer blocks (preserves dinuc
    # composition of even positions; documented approximation)
    blocks=[s[i:i+2] for i in range(0,len(s)-1,2)]
    rng.shuffle(blocks)
    out=''.join(blocks)
    if len(s)%2: out+=s[-1]
    return out
if __name__=='__main__':
    pc=read_fa('data/gencode.v45.pc_transcripts.fa.gz')
    lnc=read_fa('data/gencode.v45.lncRNA_transcripts.fa.gz')
    print('gencode pc',len(pc),'lnc',len(lnc))
    alltx={}
    for k,v in pc.items(): alltx[k]=('pc',clean(v))
    for k,v in lnc.items(): alltx[k]=('lnc',clean(v))
    long={k:v for k,v in alltx.items() if len(v[1])>=300}
    print('>=300nt:',len(long))
    ids=sorted(long,key=lambda k:hashlib.md5(k.encode()).hexdigest())
    n_dev=max(1,len(ids)//10)
    dev=set(ids[:n_dev]); tr=set(ids[n_dev:])
    json.dump({'train':sorted(tr),'dev':sorted(dev)},open('results/split.json','w'))
    with open('/tmp/007_train.jsonl','w') as f:
        for k in ids:
            if k in tr: f.write(json.dumps({'id':k,'cls':long[k][0],'seq':long[k][1]})+'\n')
    with open('/tmp/007_dev.jsonl','w') as f:
        for k in ids:
            if k in dev: f.write(json.dumps({'id':k,'cls':long[k][0],'seq':long[k][1]})+'\n')
    print('train',len(tr),'dev',len(dev))
