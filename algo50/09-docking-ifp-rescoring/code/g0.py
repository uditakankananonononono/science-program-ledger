# G0: symmetry-aware RMSD of redocked crystal ligand pose 1 vs crystal (no realignment).
from rdkit import Chem; from rdkit.Chem import rdMolAlign
from meeko import PDBQTMolecule, RDKitMolCreate
cry=Chem.RemoveHs(Chem.MolFromMol2File('../data/ada/crystal_ligand.mol2'))
pm=PDBQTMolecule.from_file('../results/dock/CRYSTAL.pdbqt',skip_typing=True)
mols=RDKitMolCreate.from_pdbqt_mol(pm)[0]
out=[]
for k in range(mols.GetNumConformers()):
    p=Chem.Mol(mols,confId=k); p=Chem.RemoveHs(p)
    pk=Chem.Mol(p); pk.RemoveAllConformers(); pk.AddConformer(Chem.Conformer(p.GetConformer(k)),assignId=True)
    out.append(rdMolAlign.CalcRMS(pk,cry))
print('rmsd_by_pose',['%.2f'%x for x in out]); print('G0', 'PASS' if out[0]<2.0 else 'FAIL', '%.2f'%out[0])
