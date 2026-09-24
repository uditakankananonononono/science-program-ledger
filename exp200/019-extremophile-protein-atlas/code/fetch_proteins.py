#!/usr/bin/env python3
"""fetch_proteins.py - build locked per-biome dev/frozen protein sets from MGnify v5.0 assemblies (GATES.md)."""
import json, urllib.request, urllib.parse, gzip, io, random, os, time
def get(u, raw=False, tries=3):
    for t in range(tries):
        try:
            with urllib.request.urlopen(u,timeout=60) as r:
                return r.read() if raw else json.load(r)
        except Exception: time.sleep(1+t)
    return None
STUDIES={'vent':['MGYS00002304'],'hotspring':['MGYS00005963'],
         'hypersaline':['MGYS00005861'],'control':['MGYS00005863']}
FROZEN_HOTSPRING=['MGYS00003602','MGYS00002328','MGYS00002327']
def analyses(study):
    d=get(f'https://www.ebi.ac.uk/metagenomics/api/v1/studies/{study}/analyses?page_size=50')
    if not d: return []
    return sorted([a['id'] for a in d['data'] if a['attributes'].get('analysis-status')=='completed'
                   and a['attributes'].get('experiment-type')=='assembly'
                   and str(a['attributes'].get('pipeline-version'))=='5.0'])
def cds_url(analysis):
    d=get(f'https://www.ebi.ac.uk/metagenomics/api/v1/analyses/{analysis}/downloads?page_size=60')
    if not d: return None
    for f in d['data']:
        if f['id'].endswith('_FASTA_predicted_cds.faa.gz'):
            return f'https://www.ebi.ac.uk/metagenomics/api/v1/analyses/{analysis}/file/{f["id"]}'
    return None
def proteins(analysis):
    u=cds_url(analysis)
    if not u: return []
    raw=get(u,raw=True)
    if not raw: return []
    out=[]
    try: txt=gzip.decompress(raw).decode('utf-8','replace')
    except Exception: return []
    for blk in txt.split('\n>'):
        blk=blk.lstrip('>')
        if blk and '\n' in blk:
            h,s=blk.split('\n',1); s=''.join(s.split())
            if 30<=len(s)<=300 and set(s)<=set('ACDEFGHIKLMNPQRSTVWYX'): out.append(s)
    return out
rng=random.Random(7)
def build(biome, split, study_list, share):
    allids=[]
    for st in study_list: allids+=analyses(st)
    allids=sorted(set(allids))
    n=len(allids); cut=max(1,int(round(n*0.6)))
    ids = allids[:cut] if split=='dev' else allids[cut:]
    if split=='frozen' and biome=='hotspring':
        ids=[]
        for st in FROZEN_HOTSPRING: ids+=analyses(st)
        ids=sorted(set(ids))
    pool=[]
    for a in ids:
        p=proteins(a); pool+=p
        print(f'  {a}: {len(p)} proteins',flush=True)
    pool=list(set(pool))
    rng.shuffle(pool)
    pool=pool[:3000]
    with open(f'results/{biome}_{split}.fasta','w') as f:
        for i,s in enumerate(pool): f.write(f'>{biome}_{split}_{i} len={len(s)}\n{s}\n')
    print(f'{biome} {split}: analyses={len(ids)} final={len(pool)}',flush=True)
import sys
which=sys.argv[1] if len(sys.argv)>1 else 'all'
for biome,studies in STUDIES.items():
    if which not in ('all',biome): continue
    for split in ['dev','frozen']:
        build(biome,split,studies,0.6)
