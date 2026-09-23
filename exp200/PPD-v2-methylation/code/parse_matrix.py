import gzip, json, numpy as np
d='/home/sandbox/exp200/ppd-v2-methylation/data/'
# ---- metadata from header
labels={}; batches={}; gsm=[]
with gzip.open(d+'GSE44132_series_matrix.txt.gz','rt',errors='replace') as f:
    for line in f:
        if line.startswith('!Sample_geo_accession'):
            gsm=[x.strip().strip('"') for x in line.split('\t')[1:]]
        elif line.startswith('!Sample_characteristics_ch1'):
            parts=[x.strip().strip('"') for x in line.split('\t')[1:]]
            key=parts[0].split(':')[0].lower()
            vals=[p.split(':',1)[1].strip() if ':' in p else p for p in parts]
            if 'postpartum depression' in key: labels['ppd']=vals
            elif 'array batch' in key and 'experimental' not in key: batches['array']=vals
        elif line.startswith('!series_matrix_table_begin'):
            break
ppd=np.array([1 if v=='yes' else 0 for v in labels['ppd']]); batch=np.array(batches['array'])
print('samples',len(gsm),'ppd yes',int(ppd.sum()),'batches',{b:int((batch==b).sum()) for b in sorted(set(batch))})
print('batch label counts:',{b:(int(ppd[batch==b].sum()),int((batch==b).sum())) for b in sorted(set(batch))})
json.dump({'gsm':gsm,'ppd':ppd.tolist(),'batch':batch.tolist()},open('/tmp/ppdv2_meta.json','w'))
# ---- manifest: autosomal probes + gene map
mani={}
with gzip.open(d+'HM450.hg38.manifest.gencode.v22.tsv.gz','rt') as f:
    hdr=f.readline().rstrip('\n').split('\t')
    i_pid=hdr.index('probeID'); i_chr=hdr.index('CpG_chrm'); i_g=hdr.index('geneNames')
    for line in f:
        p=line.rstrip('\n').split('\t')
        mani[p[i_pid]]=(p[i_chr],p[i_g])
auto={k for k,(c,g) in mani.items() if c in {f'chr{i}' for i in range(1,23)}}
print('manifest probes',len(mani),'autosomal',len(auto))
hp=[k for k,(c,g) in mani.items() if g and ('HP1BP3' in g or 'TTC9B' in g)]
print('HP1BP3/TTC9B probes:',len(hp)); json.dump(hp,open('/tmp/ppdv2_baseline_probes.json','w'))
# ---- matrix: keep autosomal probes with no missing
rows=[]; keep=[]
with gzip.open(d+'GSE44132_series_matrix.txt.gz','rt',errors='replace') as f:
    intable=False
    for line in f:
        if line.startswith('!series_matrix_table_begin'): intable=True; next(f); continue
        if not intable: continue
        if line.startswith('!series_matrix_table_end'): break
        p=line.rstrip('\n').split('\t')
        pid=p[0].strip('"')
        if pid not in auto: continue
        v=p[1:]
        if any(x in ('','NA') for x in v): continue
        rows.append([float(x) for x in v]); keep.append(pid)
B=np.array(rows,dtype=np.float32)
np.savez_compressed('/tmp/ppdv2_beta.npz',beta=B,probes=np.array(keep))
print('matrix',B.shape,'beta range',float(B.min()),float(B.max()))
