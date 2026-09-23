import urllib.request, urllib.parse, json, random, time
BASE='https://rest.uniprot.org/uniprotkb/'
def get(url,retries=3):
    for i in range(retries):
        try: return urllib.request.urlopen(url,timeout=60).read()
        except Exception as e:
            if i==retries-1: raise
            time.sleep(3)
def idlist(query):
    ids=[]; cursor=None
    while True:
        q=urllib.parse.quote(query)+'&format=list&size=500'
        url=BASE+'search?query='+q+('' if not cursor else '&cursor='+cursor)
        req=urllib.request.Request(url)
        with urllib.request.urlopen(req,timeout=60) as r:
            body=r.read().decode(); link=r.headers.get('Link','')
        ids+=[l for l in body.split() if l]
        if 'rel="next"' in link:
            cursor=link.split('cursor=')[1].split('&')[0]
        else: break
    return sorted(set(ids))
def fasta_for(ids,out):
    with open(out,'w') as f:
        for i in range(0,len(ids),200):
            chunk=ids[i:i+200]
            url=BASE+'accessions?accessions='+','.join(chunk)+'&format=fasta'
            f.write(get(url).decode())
    return sum(1 for l in open(out) if l.startswith('>'))
rng=random.Random(42)
pools={}
# families
cas9=idlist('protein_name:Cas9'); cas12=idlist('protein_name:Cas12a'); cas13=idlist('protein_name:Cas13a')
print('family totals',len(cas9),len(cas12),len(cas13))
s9=rng.sample(cas9,150); h9=rng.sample([x for x in cas9 if x not in s9],200)
s12=rng.sample(cas12,12); h12=[x for x in cas12 if x not in s12]
s13=rng.sample(cas13,20); h13=[x for x in cas13 if x not in s13]
print('heldout 12/13',len(h12),len(h13))
# decoys
dec=idlist('((organism_id:83333) OR (organism_id:224308)) AND reviewed:true NOT "CRISPR"')
d1500=rng.sample(dec,1500)
hard=idlist('reviewed:true AND ("restriction endonuclease" OR "DNA-directed DNA polymerase" OR "DNA-directed RNA polymerase") NOT CRISPR NOT cas9 NOT cas12 NOT cas13')
h300=rng.sample(hard,300)
# frozen
import urllib.parse as _up
def first_pages(query,pages=5):
    ids=[]; cursor=None
    for _ in range(pages):
        q=_up.quote(query)+'&format=list&size=500'
        url=BASE+'search?query='+q+('' if not cursor else '&cursor='+cursor)
        req=urllib.request.Request(url)
        with urllib.request.urlopen(req,timeout=60) as r:
            body=r.read().decode(); link=r.headers.get('Link','')
        ids+=[l for l in body.split() if l]
        if 'rel="next"' in link: cursor=link.split('cursor=')[1].split('&')[0]
        else: break
    return sorted(set(ids))
fr=first_pages('(cas9 OR cas12 OR cas13) AND date_created:[2022-01-01 TO *]')
print('frozen raw',len(fr))
fdec=idlist('reviewed:true AND taxonomy_id:2 AND date_created:[2022-01-01 TO *] NOT CRISPR')
fd300=rng.sample(fdec,300)
json.dump({'seed_cas9':s9,'held_cas9':h9,'seed_cas12a':s12,'held_cas12a':h12,'seed_cas13a':s13,'held_cas13a':h13,
 'dev_decoys':d1500,'hard_decoys':h300,'frozen_raw':fr,'frozen_decoys':fd300},open('data/pool_ids.json','w'))
n=0
n+=fasta_for(s9+h9+s12+h12+s13+h13,'data/dev_cas.fasta')
n+=fasta_for(d1500,'data/dev_decoys.fasta'); n+=fasta_for(h300,'data/hard_decoys.fasta')
n+=fasta_for(fd300,'data/frozen_decoys.fasta')
print('dev+decoy fasta entries',n)
