"""dock.py: Vina-dock a SMILES into a PDB pocket. Library use: dock(pdbfile, chain, lig_resname, center, smiles) -> kcal/mol."""
import subprocess,os,json,sys,tempfile
from openbabel import pybel
from vina import Vina
SOLV_KEEP=set()
def prep_receptor(pdbfile,chain,out):
    L=[l for l in open(pdbfile) if l.startswith('ATOM') and l[21]==chain]
    tmp=out+'.clean.pdb';open(tmp,'w').write(''.join(L)+'END\n')
    m=next(pybel.readfile('pdb',tmp));m.OBMol.AddPolarHydrogens();m.write('pdbqt',out,overwrite=True,opt={'r':None})
    # strip ROOT/BRANCH lines for rigid receptor
    t=[l for l in open(out) if l.startswith(('ATOM','HETATM'))];open(out,'w').write(''.join(t))
def prep_ligand(smiles,out):
    m=pybel.readstring('smi',smiles);m.OBMol.AddHydrogens();m.make3D(forcefield='mmff94',steps=300);m.write('pdbqt',out,overwrite=True)
def dock(pdbfile,chain,center,smiles,work,exh=4,seed=0):
    os.makedirs(work,exist_ok=True);r=os.path.join(work,'rec.pdbqt');l=os.path.join(work,'lig.pdbqt')
    prep_receptor(pdbfile,chain,r);prep_ligand(smiles,l)
    v=Vina(sf_name='vina',seed=seed,cpu=2,verbosity=0);v.set_receptor(r);v.set_ligand_from_file(l)
    v.compute_vina_maps(center=center,box_size=[22,22,22]);v.dock(exhaustiveness=exh,n_poses=3)
    v.write_poses(os.path.join(work,'poses.pdbqt'),n_poses=1,overwrite=True);return float(v.energies(n_poses=1)[0][0])
if __name__=='__main__':
    S=json.load(open('data/sets.json'));T=json.load(open('data/structures.json'))
    res=json.load(open('results/dock.json')) if os.path.exists('results/dock.json') else {}
    for d in ['imatinib','erlotinib']:
        for lab in ['b','n']:
            for e in T[d][lab]:
                k=f"{d}|{e['gene']}"
                if k in res: continue
                try: sc=dock(f"data/pdb/{e['pdb']}.pdb",e['chain'],e['center'],S[d]['smiles'],f"work/{d}_{e['gene']}")
                except Exception as ex: sc=None;print('ERR',k,ex,flush=True)
                res[k]=dict(label=lab,score=sc,**e);json.dump(res,open('results/dock.json','w'),indent=1);print(k,lab,sc,flush=True)
