#!/usr/bin/env python3
"""fetch_features.py IN.tsv OUT.tsv [budget_sec] - resume-safe feature fetch (v2: cCRE from local cache).
f1 phyloP base, f2 phastCons base, f3 mean phyloP +/-10bp, f4 GC +/-25bp, f5 CpG +/-25bp, f6 cCRE overlap +/-25bp."""
import sys, time, threading, bisect, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
IN, OUT = sys.argv[1], sys.argv[2]
BUDGET = float(sys.argv[3]) if len(sys.argv)>3 else 95.0
API='https://api.genome.ucsc.edu/getData'
tls=threading.local()
def sess():
    if not hasattr(tls,'s'):
        tls.s=requests.Session(); tls.s.headers['User-Agent']='exp200-018-research'
    return tls.s
def get(url, tries=4):
    for t in range(tries):
        try:
            r=sess().get(url,timeout=20)
            if r.status_code==200: return r.json()
            time.sleep(0.5*(t+1))
        except Exception: time.sleep(0.5*(t+1))
    return None
def track(tr,chrom,a,b):
    j=get(f'{API}/track?genome=hg38;track={tr};chrom={chrom};start={a};end={b}')
    if not j or tr not in j: return None
    return j[tr]
def seq(chrom,a,b):
    j=get(f'{API}/sequence?genome=hg38;chrom={chrom};start={a};end={b}')
    return (j or {}).get('dna','').upper() or None
CCRE={}
def ccre_load(chrom):
    if chrom not in CCRE:
        iv=[]
        for l in open(f'results/local/ccre_{chrom}.txt'):
            a,b=l.strip().split('-'); iv.append((int(a),int(b)))
        iv.sort(); CCRE[chrom]=iv
    return CCRE[chrom]
def ccre_overlap(chrom,a,b):
    iv=ccre_load(chrom); starts=[x[0] for x in iv]
    i=bisect.bisect_right(starts,b)-1
    j=max(0,i-3)
    for k in range(j,min(len(iv),i+3)):
        if iv[k][0]<b and iv[k][1]>a: return 1
    return 0
def features(chrom,pos):
    pos=int(pos); out={}
    pp=track('phyloP100way',chrom,pos-10,pos+11)
    if pp is None: return None
    vals={int(d['start']):float(d['value']) for d in pp}
    out['f1']=vals.get(pos); out['f3']=sum(vals.values())/len(vals) if vals else None
    pc=track('phastCons100way',chrom,pos,pos+1)
    out['f2']=float(pc[0]['value']) if pc else None
    s=seq(chrom,pos-25,pos+26)
    if s is None or len(s)<51: return None
    out['f4']=(s.count('G')+s.count('C'))/len(s)
    out['f5']=s.count('CG')/(len(s)-1)
    out['f6']=ccre_overlap(chrom,pos-25,pos+26)
    return out
def main():
    rows=[l.rstrip('\n').split('\t') for l in open(IN)]
    done=set()
    try:
        for l in open(OUT):
            p=l.rstrip('\n').split('\t'); done.add((p[0],p[1]))
    except FileNotFoundError: pass
    todo=[r for r in rows if (r[0],r[1]) not in done]
    print(f'total {len(rows)} done {len(done)} todo {len(todo)}',flush=True)
    t0=time.time(); n=0; drop=0
    mode='a' if done else 'w'
    f=open(OUT,mode)
    if mode=='w': f.write('chrom\tpos\tref\talt\tlabel\tmc\tf1\tf2\tf3\tf4\tf5\tf6\n')
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs={ex.submit(features,r[0],r[1]):r for r in todo}
        for fut in as_completed(futs):
            r=futs[fut]; ft=None
            try: ft=fut.result()
            except Exception: pass
            if ft is None or ft.get('f1') is None or ft.get('f2') is None:
                drop+=1
            else:
                f.write('\t'.join([r[0],r[1],r[2],r[3],r[4],r[5]]+[f"{ft[k]:.5g}" for k in ['f1','f2','f3','f4','f5','f6']])+'\n')
                n+=1
                if n%200==0: f.flush(); print(f'{n} fetched, {drop} dropped, {time.time()-t0:.0f}s',flush=True)
            if time.time()-t0>BUDGET:
                print('budget stop',flush=True)
                for x in futs: x.cancel()
                break
    f.flush(); f.close()
    print(f'STAGE-END fetched={n} dropped={drop} elapsed={time.time()-t0:.0f}s',flush=True)
main()
