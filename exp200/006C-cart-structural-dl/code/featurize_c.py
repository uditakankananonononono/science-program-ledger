#!/usr/bin/env python3
"""006C locked featurizer: SASA(Shrake-Rupley rel), HSE-up, 10A CA contact#,
SS (HELIX/SHEET), KD, Parker, Levitt Pa/Pb, +-4 window means. Label: 4.0A to Ab."""
import numpy as np, json, sys
from scipy.spatial import cKDTree
AA='ACDEFGHIKLMNPQRSTVWY'
KD=dict(zip(AA,[1.8,4.5,-3.5,-3.5,2.5,-3.5,-3.5,-0.4,-3.2,4.5,3.8,1.9,-3.5,-1.6,-3.5,-4.5,-0.8,-0.7,4.2,-0.9]))
PARKER=dict(zip(AA,[2.1,10.0,7.0,2.1,1.4,5.7,2.1,-5.7,4.2,-8.0,9.2,-4.2,7.1,-2.1,2.1,6.5,5.2,1.9,-1.9,-8.2]))
LEV_PA=dict(zip(AA,[1.42,0.98,0.67,1.01,0.70,1.51,1.00,0.57,1.00,1.21,1.16,0.69,1.45,1.13,0.57,0.77,0.83,1.08,1.19]))
LEV_PB=dict(zip(AA,[0.83,0.93,0.54,0.54,1.19,0.37,1.10,0.75,0.87,1.30,1.30,0.89,1.05,1.38,0.55,0.75,1.19,1.37,1.47]))
AA3={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
VDW={'N':1.65,'C':1.76,'O':1.40,'S':1.85}
MAXASA=dict(zip(AA,[121,265,187,187,148,214,214,97,195,191,230,167,203,228,154,143,163,264,255,165]))
def fib_sphere(n):
    i=np.arange(n)+0.5; phi=np.arccos(1-2*i/n); th=np.pi*(1+5**0.5)*i
    return np.c_[np.sin(phi)*np.cos(th),np.sin(phi)*np.sin(th),np.cos(phi)]
PTS=fib_sphere(96)
def parse(path):
    atoms=[]; ss={}
    for line in open(path):
        if line.startswith('ATOM'):
            el=line[76:78].strip() or line[12:14].strip()[0]
            atoms.append(dict(ch=line[21],resn=line[17:20].strip(),resi=line[22:26].strip()+line[26].strip(),
                name=line[12:16].strip(),x=float(line[30:38]),y=float(line[38:46]),z=float(line[46:54]),el=el[0] if el else 'C'))
        elif line.startswith('HELIX'):
            ss.setdefault(line[19],[]).append(('H',int(line[21:25]),int(line[33:37])))
        elif line.startswith('SHEET'):
            ss.setdefault(line[21],[]).append(('E',int(line[22:26]),int(line[33:37])))
    return atoms,ss
def featurize(path, ag_chain, ab_chains):
    atoms,ss=parse(path)
    ag_atoms=[a for a in atoms if a['ch']==ag_chain]
    ab_atoms=[a for a in atoms if a['ch'] in ab_chains]
    res_order=[]; seen=set()
    for a in ag_atoms:
        if a['resi'] not in seen: seen.add(a['resi']); res_order.append((a['resi'],a['resn']))
    n=len(res_order)
    seq=[AA3.get(r,'X') for _,r in res_order]
    # SASA (Shrake-Rupley) over antigen heavy atoms, antibody included as occluders
    all_a=atoms
    xyz=np.array([[a['x'],a['y'],a['z']] for a in all_a])
    radii=np.array([VDW.get(a['el'],1.76)+1.4 for a in all_a])
    tree=cKDTree(xyz)
    sasa_atom=np.zeros(len(all_a))
    for i in range(len(all_a)):
        ri=radii[i]
        nb=tree.query_ball_point(xyz[i], ri+3.3+1.4)
        nb=[j for j in nb if j!=i]
        pts=xyz[i]+ri*PTS
        if nb:
            occl=np.zeros(len(pts),bool)
            for j in nb:
                d=np.sqrt(((pts-xyz[j])**2).sum(1))
                occl|=d<radii[j]
            sasa_atom[i]=4*np.pi*ri*ri*(~occl).mean()
        else: sasa_atom[i]=4*np.pi*ri*ri
    res_sasa={}
    for k,a in enumerate(all_a):
        if a['ch']==ag_chain: res_sasa[a['resi']]=res_sasa.get(a['resi'],0)+sasa_atom[k]
    # per-residue CA/CB
    ca={};cb={}
    for a in ag_atoms:
        if a['name']=='CA': ca[a['resi']]=np.array([a['x'],a['y'],a['z']])
        if a['name'] in ('CB','CA'): cb.setdefault(a['resi'],np.array([a['x'],a['y'],a['z']]))
    ca_all=np.array([[a['x'],a['y'],a['z']] for a in atoms if a['name']=='CA'])
    contact=[];hse=[];rel=[]
    for rid,_ in res_order:
        c=ca.get(rid)
        if c is None: contact.append(0);hse.append(0);rel.append(0);continue
        d=np.sqrt(((ca_all-c)**2).sum(1))
        contact.append(int((d<10).sum())-1)
        v=cb[rid]-c; nv=np.linalg.norm(v); v=v/nv if nv>0 else np.array([0,0,1.])
        near=ca_all[d<10]
        hse.append(int((((near-c)@v)>0).sum())-1)
        aa1=AA3.get(dict(res_order)[rid],'X')
        rel.append(min(res_sasa.get(rid,0)/MAXASA.get(aa1,180.0),1.5))
    # SS
    ssv=[]
    helix=ss.get(ag_chain,[])
    for rid,_ in res_order:
        rn=int(''.join(c for c in rid if c.isdigit()) or 0)
        s='C'
        for t,a,b in helix:
            if a<=rn<=b: s=t;break
        ssv.append({'C':0,'H':1,'E':2}[s])
    # labels 4.0A
    ab_xyz=np.array([[a['x'],a['y'],a['z']] for a in ab_atoms])
    truth=[]
    for rid,_ in res_order:
        pts=np.array([[a['x'],a['y'],a['z']] for a in ag_atoms if a['resi']==rid])
        d=np.sqrt(((pts[:,None,:]-ab_xyz[None,:,:])**2).sum(-1)).min() if len(pts) else 99
        truth.append(int(d<4.0))
    # base numeric features
    base=np.array([[KD.get(a,0),PARKER.get(a,0),LEV_PA.get(a,0),LEV_PB.get(a,0)] for a in seq])
    base=np.c_[base,np.array(rel),np.array(contact,float),np.array(hse,float)]
    def roll(x,w=4):
        return np.array([x[max(0,i-w):min(n,i+w+1)].mean(0) for i in range(n)])
    win=roll(base)
    F=np.c_[base,win,np.eye(3)[ssv]]
    return dict(ids=[r for r,_ in res_order],seq=''.join(seq),truth=truth,F=F.tolist(),
                meta=dict(ag=ag_chain,ab=list(ab_chains),n=n,epitope=sum(truth)))
if __name__=='__main__':
    import os
    jobs=json.load(open(sys.argv[1]))
    for pdb,ag,ab,out in jobs:
        r=featurize(pdb,ag,ab)
        json.dump(r,open(out,'w'))
        print(os.path.basename(pdb),'n=%d epi=%d'%(r['meta']['n'],r['meta']['epitope']))
