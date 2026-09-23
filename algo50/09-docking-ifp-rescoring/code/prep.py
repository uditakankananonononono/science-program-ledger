# Receptor PDBQT (AD4 types, heuristic) + library selection. Seeded, deterministic.
import random, numpy as np
D='../data/ada/'
arom={'PHE':'CG CD1 CD2 CE1 CE2 CZ','TYR':'CG CD1 CD2 CE1 CE2 CZ','TRP':'CD2 CE2 CE3 CZ2 CZ3 CH2 CG CD1','HIS':'CG CD2 CE1'}
lines=[l for l in open(D+'receptor.pdb') if l.startswith('ATOM')]
xyz=[(float(l[30:38]),float(l[38:46]),float(l[46:54])) for l in lines]
names=[l[12:16].strip() for l in lines]
out=[]
for i,l in enumerate(lines):
    n=names[i]; res=l[17:20].strip(); e=n[0] if n!='ZN' else 'ZN'
    if n[0].isdigit(): e=n[1]
    if e=='H':
        # polar H if nearest heavy atom is N/O
        d=[(np.linalg.norm(np.subtract(xyz[i],xyz[j])),names[j]) for j in range(max(0,i-25),min(len(lines),i+25)) if j!=i and names[j][0] not in 'H123']
        nb=min(d)[1]
        if nb[0] not in 'NO': continue
        t='HD'
    elif e=='ZN': t='Zn'
    elif e=='C': t='A' if n in arom.get(res,'').split() else 'C'
    elif e=='N': t='NA' if (res=='HIS' and n in('ND1','NE2')) else 'N'
    elif e=='O': t='OA'
    elif e=='S': t='SA'
    else: continue
    out.append('%-54s%6.2f%6.2f    %6.3f %-2s\n'%(l[:54].ljust(54),1.0,0.0,0.0,t))
open('../data/receptor.pdbqt','w').writelines(out)
act=[l.split()[:2] for l in open(D+'actives_final.ism')]
dec=[l.split()[:2] for l in open(D+'decoys_final.ism')]
random.seed(9); ds=random.sample(dec,465)
with open('../data/library.tsv','w') as f:
    f.write('id\tsmiles\tlabel\n')
    for s,i in act: f.write(f'{i}\t{s}\t1\n')
    for s,i in ds: f.write(f'{i}\t{s}\t0\n')
print(len(out),'receptor atoms;',len(act),'actives',len(ds),'decoys')
