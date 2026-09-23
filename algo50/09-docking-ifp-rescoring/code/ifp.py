# From-scratch residue interaction fingerprint + pose parsing.
import numpy as np
from rdkit import Chem
HYD={'C','A'}; POL={'N','NA','OA','O'}
def read_receptor(fn='../data/receptor.pdbqt'):
    at=[]
    for l in open(fn):
        at.append((l[17:20].strip()+l[22:26].strip(), np.array([float(l[30:38]),float(l[38:46]),float(l[46:54])]), l[77:79].strip()))
    return at
def site(rec, lig_xyz, cut=6.0):
    res=sorted({r for r,x,t in rec if np.min(np.linalg.norm(lig_xyz-x,axis=1))<=cut})
    idx=[i for i,(r,x,t) in enumerate(rec) if r in res]
    return res, idx
def ifp(rec, res, idx, lig):  # lig: list of (xyz, adtype), heavy atoms only
    bits=np.zeros(3*len(res),bool); pos={r:k for k,r in enumerate(res)}
    L=np.array([x for x,t in lig]); T=[t for x,t in lig]
    for i in idx:
        r,x,t=rec[i]; d=np.linalg.norm(L-x,axis=1); k=pos[r]
        for j,tj in enumerate(T):
            if t in HYD and tj in HYD and d[j]<=4.0: bits[3*k]=1
            if t in POL and tj in POL and d[j]<=3.5: bits[3*k+1]=1
            if t=='Zn' and tj in POL and d[j]<=2.8: bits[3*k+2]=1
    return bits
def tani(a,b):
    u=np.sum(a|b); return float(np.sum(a&b)/u) if u else 0.0
def poses(fn):
    out=[];cur=[]
    for l in open(fn):
        if l.startswith('MODEL'): cur=[]
        elif l.startswith(('ATOM','HETATM')):
            t=l[77:79].strip()
            if t not in ('H','HD'): cur.append((np.array([float(l[30:38]),float(l[38:46]),float(l[46:54])]),t))
        elif l.startswith('ENDMDL'): out.append(cur)
    return out
def crystal_lig(fn='../data/ada/crystal_ligand.mol2'):
    m=Chem.MolFromMol2File(fn,removeHs=False); c=m.GetConformer()
    lig=[]
    for a in m.GetAtoms():
        s=a.GetSymbol()
        if s=='H': continue
        t={'C':'A' if a.GetIsAromatic() else 'C','N':'NA','O':'OA','S':'SA'}.get(s,s)
        lig.append((np.array(c.GetAtomPosition(a.GetIdx())),t))
    return m, lig
