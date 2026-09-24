#!/usr/bin/env python3
"""fetch_features2.py IN.tsv OUT.tsv [budget_sec] - v3: grouped conservation calls; seq+cCRE local.
Groups variants within 300bp -> 1 phyloP + 1 phastCons call per group. f4/f5 from local chr fasta; f6 from local cCRE."""
import sys, time, threading, bisect, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
IN, OUT = sys.argv[1], sys.argv[2]
BUDGET = float(sys.argv[3]) if len(sys.argv)>3 else 95.0
API='https://api.genome.ucsc.edu/getData/track?genome=hg38'
tls=threading.local()
def sess():
    if not hasattr(tls,'s'):
        tls.s=requests.Session(); tls.s.headers['User-Agent']='exp200-018-research'
    return tls.s
def get(url, tries=4):
    for t in range(tries):
        try:
            r=sess().get(url,timeout=25)
            if r.status_code==200: return r.json()
            time.sleep(0.4*(t+1))
        except Exception: time.sleep(0.4*(t+1))
    return None
SEQ={}; CCRE={}
def seq_load(chrom):
    if chrom not in SEQ:
        s=open(f'results/local/{chrom}.fa').read().split('\n',1)[1].replace('\n','')
        SEQ[chrom]=s
    return SEQ[chrom]
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
    for k in range(max(0,i-3),min(len(iv),i+3)):
        if iv[k][0]<b and iv[k][1]>a: return 1
    return 0
def group_fetch(chrom, members):
    a=min(m[1] for m in members); b=max(m[1] for m in members)
    pp=get(f'{API};track=phyloP100way;chrom={chrom};start={a-10};end={b+11}')
    pc=get(f'{API};track=phastCons100way;chrom={chrom};start={a};end={b+1}')
    if not pp or 'phyloP100way' not in pp or not pc or 'phastCons100way' not in pc: return None
    pv={int(d['start']):float(d['value']) for d in pp['phyloP100way']}
    cv={int(d['start']):float(d['value']) for d in pc['phastCons100way']}
    s=seq_load(chrom); out={}
    for idx,pos in members:
        if pos not in pv or pos not in cv: out[idx]=None; continue
        win=[pv.get(p) for p in range(pos-10,pos+11) if p in pv]
        s51=s[pos-25:pos+26]
        if len(s51)<51: out[idx]=None; continue
        out[idx]={'f1':pv[pos],'f2':cv[pos],'f3':sum(win)/len(win) if win else None,
                  'f4':(s51.count('G')+s51.count('C'))/51.0,'f5':s51.count('CG')/50.0,
                  'f6':ccre_overlap(chrom,pos-25,pos+26)}
    return out
def main():
    rows=[l.rstrip('\n').split('\t') for l in open(IN)]
    done=set()
    try:
        for l in open(OUT):
            if l.startswith('chrom\t'): continue
            p=l.rstrip('\n').split('\t'); done.add((p[0],p[1]))
    except FileNotFoundError: pass
    todo=[(i,r) for i,r in enumerate(rows) if (r[0],r[1]) not in done]
    todo.sort(key=lambda x:(x[1][0],int(x[1][1])))
    groups=[]; cur=[]; curkey=None
    for item in todo:
        key=(item[1][0], int(item[1][1]))
        if cur and (key[0]!=curkey[0] or key[1]-curkey[1]>300):
            groups.append(cur); cur=[]
        curkey=key; cur.append((item[0],key[1]))
    if cur: groups.append(cur)
    print(f'total {len(rows)} done {len(done)} todo {len(todo)} groups {len(groups)}',flush=True)
    t0=time.time(); n=0; drop=0
    mode='a' if done else 'w'
    f=open(OUT,mode)
    if mode=='w': f.write('chrom\tpos\tref\talt\tlabel\tmc\tf1\tf2\tf3\tf4\tf5\tf6\n')
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs={ex.submit(group_fetch,rows[g[0][0]][0],g):g for g in groups}
        for fut in as_completed(futs):
            g=futs[fut]; res=None
            try: res=fut.result()
            except Exception: pass
            if res is None:
                drop+=len(g)
            else:
                for i,pos in g:
                    ft=res.get(i)
                    r=rows[i]
                    if ft is None or ft.get('f1') is None or ft.get('f3') is None: drop+=1
                    else:
                        f.write('\t'.join([r[0],r[1],r[2],r[3],r[4],r[5]]+[f"{ft[k]:.5g}" for k in ['f1','f2','f3','f4','f5','f6']])+'\n'); n+=1
                if n%300==0: f.flush(); print(f'{n} fetched, {drop} dropped, {time.time()-t0:.0f}s',flush=True)
            if time.time()-t0>BUDGET:
                print('budget stop',flush=True)
                for x in futs: x.cancel()
                break
    f.flush(); f.close()
    print(f'STAGE-END fetched={n} dropped={drop} elapsed={time.time()-t0:.0f}s',flush=True)
main()
