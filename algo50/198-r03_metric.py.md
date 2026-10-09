# 198 frozen wrapper r03_metric.py (sha256 in 198-PREREG.md)
```python
"""Frozen R-03 scoring (prereg 198). In-place, symmetry- and stereo-aware heavy-atom RMSD, receptor frame, no translation/rotation.
Reference: 7KX5 chain A HETATM X7V (all 38 heavy atoms, no altlocs present), bond orders from data/raw/X7V_ideal.sdf (heavy, removeHs).
Pose: first MODEL of the Vina pose PDBQT; topology/stereo from its REMARK SMILES, atoms placed via REMARK SMILES IDX (smiles_idx -> pdbqt serial)."""
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

def crystal_mol(pdb_path, ideal_sdf):
    lines=[l for l in open(pdb_path) if l.startswith('HETATM') and l[17:20].strip()=='X7V' and l[21]=='A' and l[76:78].strip()!='H']
    assert all(l[16]==' ' for l in lines), 'altloc present'
    m=Chem.MolFromPDBBlock(''.join(lines),removeHs=True,proximityBonding=True)
    tmpl=Chem.MolFromMolFile(ideal_sdf,removeHs=True)
    mol=AllChem.AssignBondOrdersFromTemplate(tmpl,m)
    Chem.AssignStereochemistryFrom3D(mol)
    assert mol.GetNumHeavyAtoms()==tmpl.GetNumHeavyAtoms()==38
    return mol

def pose_mol(pdbqt_text):
    smi=None; idx={}; atoms={}; model_done=False
    for l in pdbqt_text.splitlines():
        if l.startswith('REMARK SMILES IDX'):
            t=l.split()[3:]
            for a,b in zip(t[::2],t[1::2]): idx[int(a)]=int(b)
        elif l.startswith('REMARK SMILES '): smi=l.split()[2]
        elif l.startswith('ENDMDL'): break
        elif l.startswith(('ATOM','HETATM')): atoms[int(l[6:11])]=(float(l[30:38]),float(l[38:46]),float(l[46:54]))
    m=Chem.MolFromSmiles(smi); assert m is not None and m.GetNumAtoms()==len(idx)==38
    conf=Chem.Conformer(m.GetNumAtoms())
    for si,serial in idx.items(): conf.SetAtomPosition(si-1,atoms[serial])
    m.AddConformer(conf); Chem.AssignStereochemistryFrom3D(m)
    return m

def inplace_rmsd(ref, pose, use_chirality=True):
    """min over all graph-isomorphic atom mappings (incl. symmetry), no alignment; sqrt(mean squared distance)."""
    matches=ref.GetSubstructMatches(pose,uniquify=False,useChirality=use_chirality,maxMatches=100000)
    if not matches: raise RuntimeError('no topology/stereo-preserving mapping')
    rc=ref.GetConformer().GetPositions(); pc=pose.GetConformer().GetPositions()
    best=min(np.sqrt(((rc[list(mt)]-pc)**2).sum(1).mean()) for mt in matches)
    return float(best), len(matches)

def hungarian_inplace(ref_xyz, ref_el, mob_xyz, mob_el):
    """graph-free secondary: per-element optimal assignment minimizing squared distance, no superposition."""
    from scipy.optimize import linear_sum_assignment
    tot=0.0;n=0
    for el in set(ref_el):
        ri=[i for i,e in enumerate(ref_el) if e==el]; mi=[i for i,e in enumerate(mob_el) if e==el]
        d=((np.asarray(ref_xyz)[ri][:,None,:]-np.asarray(mob_xyz)[mi][None,:,:])**2).sum(2)
        r,c=linear_sum_assignment(d); tot+=d[r,c].sum(); n+=len(r)
    return float(np.sqrt(tot/n))
```
