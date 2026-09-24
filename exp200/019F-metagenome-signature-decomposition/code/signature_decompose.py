#!/usr/bin/env python3
"""signature_decompose.py - decompose a metagenomic protein set into halophile-origin
vs non-halophile-origin fractions and test whether the bulk acidic-proteome signal
is carried by halophile-origin sequences.

019F (DOC-1-019F). Locked procedure (GATES.md + Addenda A/B):
  - origin assignment: MMseqs2 search (-s 7.5, e<=1e-5, query cov >= 0.5, cov-mode 0)
    of each query protein against a reference DB of 100 Halobacteria reference
    proteomes (UniProt, rng-seed-7 sample of the 283 UniProtKB-covered reference
    proteomes of class Halobacteria, pulled 2026-09-24).
  - a query is 'halophile-origin' iff it has at least one hit passing the thresholds.
  - outputs: per-query origin labels, community assignment rate, median D+E of each
    origin fraction, the origin contrast, and the dilution prediction
    r*halo_proteome_median + (1-r)*control_median vs the observed bulk median.

Usage:
  signature_decompose.py --query proteins.fasta --db halo_db.fasta --mmseqs /path/mmseqs --out outdir
Reference medians default to the locked 019F panels (G0): 16.97% D+E (halo) / 11.87% (control).
"""
import argparse, os, subprocess, tempfile, statistics, json

def read_fasta(path):
    seqs={}; name=None
    for line in open(path):
        line=line.rstrip()
        if line.startswith('>'):
            name=line[1:].split()[0]; seqs[name]=''
        elif name is not None: seqs[name]+=line
    return seqs

def de_frac(s):
    return sum(1 for c in s if c in 'DE')/len(s) if s else 0.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--query', required=True)
    ap.add_argument('--db', required=True, help='halophile reference proteome fasta')
    ap.add_argument('--mmseqs', default='mmseqs')
    ap.add_argument('--halo-proteome-de', type=float, default=0.1697)
    ap.add_argument('--control-proteome-de', type=float, default=0.1187)
    ap.add_argument('--out', required=True)
    a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    mm=a.mmseqs
    with tempfile.TemporaryDirectory() as td:
        qdb, ddb, res = f'{td}/q', f'{td}/d', f'{td}/r'
        subprocess.run([mm,'createdb',a.query,qdb,'-v','1'],check=True)
        subprocess.run([mm,'createdb',a.db,ddb,'-v','1'],check=True)
        subprocess.run([mm,'search',qdb,ddb,res,f'{td}/tmp','-s','7.5','-e','1e-5',
                        '-c','0.5','--cov-mode','0','--threads','2','-v','1'],check=True)
        m8=f'{a.out}/hits.m8'
        subprocess.run([mm,'convertalis',qdb,ddb,res,m8,
                        '--format-output','query,target,evalue,qcov','-v','1'],check=True)
    best={}
    for line in open(m8):
        q,t,e,qc=line.rstrip().split('\t'); e=float(e)
        if q not in best or e<best[q]: best[q]=e
    seqs=read_fasta(a.query)
    halo={q:seqs[q] for q in best if q in seqs}
    non={q:s for q,s in seqs.items() if q not in best}
    with open(f'{a.out}/origin_labels.tsv','w') as f:
        for q in seqs: f.write(f"{q}\t{'halophile-origin' if q in best else 'non-origin'}\n")
    r=len(halo)/len(seqs) if seqs else 0
    mh=statistics.median(de_frac(s) for s in halo.values()) if halo else None
    mn=statistics.median(de_frac(s) for s in non.values()) if non else None
    obs=statistics.median(de_frac(s) for s in seqs.values()) if seqs else None
    pred=r*a.halo_proteome_de+(1-r)*a.control_proteome_de
    out={'n_queries':len(seqs),'n_halo_origin':len(halo),'assignment_rate':r,
         'halo_origin_de_median':mh,'non_origin_de_median':mn,
         'origin_contrast_pp':(mh-mn)*100 if mh is not None and mn is not None else None,
         'observed_bulk_de_median':obs,'predicted_bulk_de_median':pred}
    json.dump(out, open(f'{a.out}/decomposition.json','w'), indent=2)
    print(json.dumps(out, indent=2))

if __name__=='__main__':
    main()
