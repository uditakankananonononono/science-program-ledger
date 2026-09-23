# Resumable Vina docking of library.tsv (+ crystal ligand redock as id CRYSTAL).
import os, sys, numpy as np
from rdkit import Chem; from rdkit.Chem import AllChem
from meeko import MoleculePreparation, PDBQTWriterLegacy
from vina import Vina
R='../results/'; os.makedirs(R+'dock',exist_ok=True)
cry=Chem.MolFromMol2File('../data/ada/crystal_ligand.mol2',removeHs=False)
center=cry.GetConformer().GetPositions().mean(0).tolist()
v=Vina(sf_name='vina',seed=9,verbosity=0,cpu=2)
v.set_receptor('../data/receptor.pdbqt')
v.compute_vina_maps(center=center,box_size=[22,22,22])
done=set(l.split('\t')[0] for l in open(R+'scores.tsv')) if os.path.exists(R+'scores.tsv') else set()
rows=[l.rstrip('\n').split('\t') for l in open('../data/library.tsv')][1:]
todo=[('CRYSTAL',Chem.MolToSmiles(Chem.RemoveHs(cry)),'-1')]+rows
prep=MoleculePreparation()
for cid,smi,lab in todo:
    if cid in done: continue
    try:
        m=Chem.AddHs(Chem.MolFromSmiles(smi))
        if AllChem.EmbedMolecule(m,randomSeed=9)!=0: raise ValueError('embed')
        AllChem.MMFFOptimizeMolecule(m)
        s,ok,err=PDBQTWriterLegacy.write_string(prep.prepare(m)[0])
        v.set_ligand_from_string(s)
        v.dock(exhaustiveness=4,n_poses=5)
        e=v.energies(n_poses=5)[:,0]
        open(R+'dock/%s.pdbqt'%cid,'w').write(v.poses(n_poses=5))
        rec=[cid,lab,';'.join('%.3f'%x for x in e),'ok']
    except Exception as ex:
        rec=[cid,lab,'','fail:%s'%str(ex)[:60]]
    with open(R+'scores.tsv','a') as f: f.write('\t'.join(rec)+'\n')
    print(rec,flush=True)
