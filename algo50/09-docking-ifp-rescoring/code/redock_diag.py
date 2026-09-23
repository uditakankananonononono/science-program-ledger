# POST-HOC diagnostic (not gated): redock crystal ligand at higher exhaustiveness, and from the crystal conformer.
import sys, numpy as np
from rdkit import Chem; from rdkit.Chem import AllChem, rdMolAlign
from meeko import MoleculePreparation, PDBQTWriterLegacy, PDBQTMolecule, RDKitMolCreate
from vina import Vina
cryH=Chem.MolFromMol2File('../data/ada/crystal_ligand.mol2',removeHs=False); cry=Chem.RemoveHs(cryH)
center=cryH.GetConformer().GetPositions().mean(0).tolist()
def rms(pdbqt):
    m=RDKitMolCreate.from_pdbqt_mol(PDBQTMolecule(pdbqt,skip_typing=True))[0]; m=Chem.RemoveHs(m); out=[]
    for c in m.GetConformers():
        p=Chem.Mol(m); p.RemoveAllConformers(); p.AddConformer(Chem.Conformer(c),assignId=True); out.append(rdMolAlign.CalcRMS(p,cry))
    return out
for start in ('smiles','crystal'):
    if start=='smiles':
        m=Chem.AddHs(Chem.MolFromSmiles(Chem.MolToSmiles(cry))); AllChem.EmbedMolecule(m,randomSeed=9); AllChem.MMFFOptimizeMolecule(m)
    else: m=Chem.AddHs(cry,addCoords=True)
    s=PDBQTWriterLegacy.write_string(MoleculePreparation().prepare(m)[0])[0]
    for ex in (16,32):
        v=Vina(sf_name='vina',seed=9,verbosity=0,cpu=2); v.set_receptor('../data/receptor.pdbqt'); v.compute_vina_maps(center=center,box_size=[22,22,22])
        v.set_ligand_from_string(s); v.dock(exhaustiveness=ex,n_poses=9)
        r=rms(v.poses(n_poses=9)); e=v.energies(n_poses=9)[:,0]
        print(start,ex,'top1 rmsd %.2f energy %.2f | best-of-9 rmsd %.2f'%(r[0],e[0],min(r)),flush=True)
