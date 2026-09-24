import json,random,urllib.request,urllib.parse,os,re
S=json.load(open('data/sets.json'));os.makedirs('data/pdb',exist_ok=True)
def get(u,data=None):
    r=urllib.request.Request(u,data=data,headers={'Content-Type':'application/json'} if data else {});return urllib.request.urlopen(r,timeout=40).read().decode()
def uniprot(g):
    q=urllib.parse.quote(f'(gene:{g}) AND (organism_id:9606) AND (reviewed:true)')
    t=get(f'https://rest.uniprot.org/uniprotkb/search?format=tsv&fields=accession,gene_primary&size=5&query={q}').split('\n')[1:]
    t=[l.split('\t') for l in t if l]
    ex=[a for a,gp in t if gp.upper()==g.upper()];return ex[0] if ex else (t[0][0] if t else None)
SOLV={'HOH','GOL','EDO','SO4','PO4','PEG','PG4','DMS','ACT','CL','NA','MG','MN','ZN','CA','K','IOD','BR','MPD','TRS','EPE','MES','FMT','1PE','P6G','PGE','NO3','CIT','BME','IMD','ACY','SCN'}
def pdbs(acc):
    q={"query":{"type":"group","logical_operator":"and","nodes":[
      {"type":"terminal","service":"text","parameters":{"attribute":"rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession","operator":"exact_match","value":acc}},
      {"type":"terminal","service":"text","parameters":{"attribute":"exptl.method","operator":"exact_match","value":"X-RAY DIFFRACTION"}},
      {"type":"terminal","service":"text","parameters":{"attribute":"rcsb_entry_info.resolution_combined","operator":"less_or_equal","value":3.0}},
      {"type":"terminal","service":"text","parameters":{"attribute":"rcsb_entry_info.nonpolymer_entity_count","operator":"greater","value":0}}]},
     "return_type":"entry","request_options":{"sort":[{"sort_by":"rcsb_entry_info.resolution_combined","direction":"asc"}],"paginate":{"start":0,"rows":25}}}
    try: return [x['identifier'] for x in json.loads(get('https://search.rcsb.org/rcsbsearch/v2/query',json.dumps(q).encode()))['result_set']]
    except Exception: return []
def pick(acc):
    for pid in pdbs(acc):
        f=f'data/pdb/{pid}.pdb'
        if not os.path.exists(f):
            try: open(f,'w').write(get(f'https://files.rcsb.org/download/{pid}.pdb'))
            except Exception: continue
        L=open(f).read().split('\n');chains={l[12:14].strip()+':'+l[33:42].strip() for l in L if l.startswith('DBREF ')}
        ch=[l[12] for l in L if l.startswith('DBREF ') and l[33:41].strip()==acc]
        if not ch: continue
        mod={l[12:15].strip() for l in L if l.startswith('MODRES')}|{'PTR','SEP','TPO','MSE','CSO','CME','OCS','KCX','LLP'}
        het={}
        for l in L:
            if l.startswith('HETATM') and l[21] in ch and l[17:20].strip() not in SOLV and l[17:20].strip() not in mod and l[76:78].strip()!='H':
                het.setdefault((l[17:20].strip(),l[21],l[22:26]),[]).append((float(l[30:38]),float(l[38:46]),float(l[46:54])))
        big=[(k,v) for k,v in het.items() if len(v)>=15]
        if big:
            k,v=max(big,key=lambda kv:len(kv[1]));c=[sum(x[i] for x in v)/len(v) for i in range(3)]
            return dict(pdb=pid,chain=k[1],lig=k[0],center=c)
    return None
random.seed(0);out={}
for d,s in S.items():
    b=[g for g in s['binders'] if g!='ABL1p'];n=list(s['nonbinders']);random.shuffle(b);random.shuffle(n)
    sel={'b':[],'n':[]}
    for lab,pool,q in [('b',b,10),('n',n,20)]:
        for g in pool:
            if len(sel[lab])>=q: break
            acc=uniprot(g);st=pick(acc) if acc else None
            print(d,lab,g,acc,st,flush=True)
            if st: sel[lab].append(dict(gene=g,acc=acc,**st))
    out[d]=sel
json.dump(out,open('data/structures.json','w'),indent=1)
