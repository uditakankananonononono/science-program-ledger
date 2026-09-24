import sys, os, subprocess, h5py, numpy as np, pandas as pd, gzip, io, urllib.request
BASE='https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM8694nnn/{gsm}/suppl/{gsm}_MC38_{lab}_spatial'
SAMPLES={
 'm09':('GSM8694501','aPD1_NR_m09'),'m10':('GSM8694502','aPD1_NR_m10'),
 'm11':('GSM8694503','aPD1_NR_m11'),'m12':('GSM8694504','aPD1_NR_m12'),
 'm13':('GSM8694505','aPD1_NR_m13'),'m14':('GSM8694506','aPD1_NR_m14'),
 'm15s1':('GSM8694507','aPD1_R_m15_sec1'),'m15s2':('GSM8694508','aPD1_R_m15_sec2'),
 'm16s1':('GSM8694509','aPD1_R_m16_sec1'),'m16s2':('GSM8694510','aPD1_R_m16_sec2'),
 'm16s3':('GSM8694511','aPD1_R_m16_sec3')}
CHOL=['Hmgcs1','Hmgcr','Mvk','Pmvk','Mvd','Idi1','Fdft1','Sqle','Ldlr','Srebf2']
CD8=['Cd8a','Cd8b1','Gzmb','Prf1']; TPAN=['Cd3d','Cd3e','Cd8a','Cd8b1','Gzmb','Prf1']
GENES=sorted(set(CHOL+CD8+TPAN))
def process(name, gsm, lab, out):
    h5url=f'{BASE.format(gsm=gsm,lab=lab)}_filtered_feature_bc_matrix.h5'
    posurl=f'{BASE.format(gsm=gsm,lab=lab)}_tissue_positions_list.csv.gz'
    h5p=f'/tmp/{name}.h5'
    if not os.path.exists(h5p):
        subprocess.run(['curl','-s','-o',h5p,'--max-time','100',h5url], check=True)
    f=h5py.File(h5p,'r'); mg=f['matrix']
    genes=[g.decode() for g in mg['features']['name'][:]]
    barcodes=[b.decode() for b in mg['barcodes'][:]]
    gidx=[genes.index(g) for g in GENES]
    # CSC: genes x barcodes -> column sums = library size
    data=mg['data'][:]; indptr=mg['indptr'][:]; indices=mg['indices'][:]
    lib=np.diff(indptr).astype(np.float64)*0
    np.add.at(lib, np.repeat(np.arange(len(indptr)-1), np.diff(indptr)), data)
    gi_set=set(gidx)
    rows=np.zeros((len(gidx), len(barcodes)), np.float32)
    # walk columns, collect target genes
    gpos={g:i for i,g in enumerate(gidx)}
    for c in range(len(barcodes)):
        s,e=indptr[c],indptr[c+1]
        seg_i=indices[s:e]; seg_d=data[s:e]
        for r,v in zip(seg_i, seg_d):
            p=gpos.get(r)
            if p is not None: rows[p,c]=v
    norm=np.log1p(rows/np.maximum(lib,1)[None,:]*1e4)
    gset={g: norm[GENES.index(g)] for g in GENES}
    chol=np.mean([gset[g] for g in CHOL],0); cd8=np.mean([gset[g] for g in CD8],0); tpan=np.mean([gset[g] for g in TPAN],0)
    pos=pd.read_csv(posurl, header=None, names=['bc','in_tissue','row','col','pxr','pxc'])
    pos=pos.set_index('bc').reindex(barcodes)
    m=pos['in_tissue'].values==1
    np.savez_compressed(out, chol=chol[m].astype(np.float32), cd8=cd8[m].astype(np.float32),
        tpan=tpan[m].astype(np.float32), row=pos['row'].values[m], col=pos['col'].values[m],
        pxr=pos['pxr'].values[m], pxc=pos['pxc'].values[m])
    f.close(); os.remove(h5p)
    print(name, 'spots_in_tissue', int(m.sum()), 'chol_mean', round(float(chol[m].mean()),3))
if __name__=='__main__':
    for name in sys.argv[1:]:
        gsm,lab=SAMPLES[name]
        process(name, gsm, lab, f'results/local/{name}.npz')
