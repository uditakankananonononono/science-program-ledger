#!/usr/bin/env python3
"""Parse Ab-Ag PDB complexes -> per-residue (features, interface truth).
Gates-frozen features: Parker, Kyte-Doolittle, Karplus-Schulz, Emini, Chou-Fasman
(window 5 means), Atchley 5 factors, CA burial (10A neighbor count)."""
import numpy as np, json
AA='ACDEFGHIKLMNPQRSTVWXY'
KD=dict(zip(AA,[0.2,6.3,4.2,-1.3,1.4,-2.5,3.4,2.3,0.0,-3.7,3.8,-1.9,2.8,0.0,0.4,-0.5,-0.9,-1.6,4.5,-0.7,-1.0]))
PARKER=dict(zip(AA,[2.1,10.0,7.0,2.1,1.4,5.7,2.1,-5.7,4.2,-8.0,9.2,-4.2,7.1,-2.1,2.1,6.5,5.2,1.9,-1.9,-8.2,-1.3]))
KS=dict(zip(AA,[1.031,1.025,1.008,1.049,1.020,1.052,0.992,1.019,1.054,1.094,1.007,0.982,0.992,1.036,1.021,1.014,1.009,0.982,0.967,1.035,1.014]))
EMINI=dict(zip(AA,[0.06,0.49,0.85,0.97,0.15,0.68,0.76,0.06,0.82,0.36,0.51,0.77,0.26,0.06,0.35,0.42,0.71,0.48,0.15,0.17,0.10]))
CF=dict(zip(AA,[0.46,0.25,0.35,0.39,0.33,0.22,0.53,0.20,0.74,0.39,0.36,0.31,0.37,0.26,0.51,0.64,0.50,0.26,0.41,0.34,0.31]))
ATCH={  # Atchley 2005 five factors
 'A':(-0.591,-1.302,-0.733,1.570,-0.146),'C':(-1.343,0.465,-0.862,-1.020,-0.255),
 'D':(1.538,0.987,-0.837,1.478,0.118),'E':(1.357,0.831,-0.241,1.453,0.517),
 'F':(-1.006,-0.590,1.891,-0.397,0.412),'G':(-0.384,1.652,1.330,1.045,2.064),
 'H':(0.336,-0.417,-1.673,-1.474,-0.078),'I':(-1.239,-0.547,2.131,0.393,0.816),
 'K':(1.831,-0.561,0.533,-0.277,1.648),'L':(-1.019,-0.987,-1.505,1.266,-0.912),
 'M':(-0.663,-1.524,2.219,-1.005,1.212),'N':(0.945,0.828,1.299,-0.169,0.933),
 'P':(0.189,2.081,-1.628,0.421,-1.392),'Q':(0.931,-0.179,-3.005,-0.503,-1.853),
 'R':(1.538,-0.055,1.502,0.440,2.897),'S':(-0.228,1.399,-4.760,0.670,-2.647),
 'T':(-0.032,0.326,2.213,0.908,1.313),'V':(-1.337,-0.279,-0.544,1.242,-1.262),
 'W':(-0.595,0.009,0.672,-2.128,-0.184),'Y':(0.260,0.830,3.097,-0.838,1.512)}
SCALES=[KD,PARKER,KS,EMINI,CF]
AB_TERMS=('antibody','heavy','light','fab','immunoglobulin','igg','scfv','vh','vl','fc ')
def parse_pdb(path):
    compnd={}; cur_chain=None; mol=''
    atoms=[]
    with open(path) as f:
        for line in f:
            if line.startswith('COMPND'):
                if 'CHAIN:' in line:
                    chs=line.split('CHAIN:')[1].replace(';','').replace(',',' ').split()
                    for c in chs: compnd.setdefault(c.strip(),[''])[0]=mol
                elif 'MOLECULE:' in line:
                    mol=line.split('MOLECULE:')[1].split(';')[0].strip()
            elif line.startswith('ATOM'):
                ch=line[21]; resn=line[17:20].strip(); resi=line[22:26].strip()+line[26].strip()
                try: x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
                except: continue
                atoms.append((ch,resn,resi,x,y,z))
    return compnd,atoms
AA3={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
def featurize(path):
    compnd,atoms=parse_pdb(path)
    chains={}
    for ch,resn,resi,x,y,z in atoms:
        chains.setdefault(ch,{})[resi]=resn
    ab=set(); ag=None
    for ch,res in chains.items():
        name=(compnd.get(ch,[''])[0] or '').lower()
        n=len(res)
        if any(t in name for t in AB_TERMS) or n<150:
            if any(t in name for t in AB_TERMS): ab.add(ch)
            elif n>=80 and ag is None: ag=ch
        elif n>=80 and ag is None: ag=ch
    if not ab or ag is None: return None
    ag_atoms=[a for a in atoms if a[0]==ag and a[2].rstrip('ABCDEF')!='' ]
    ab_xyz=np.array([[a[3],a[4],a[5]] for a in atoms if a[0] in ab])
    ag_res=sorted(chains[ag].items(),key=lambda kv:int(''.join(c for c in kv[0] if c.isdigit()) or 0))
    seq=[AA3.get(r,'X') for _,r in ag_res]
    ids=[i for i,_ in ag_res]
    xyz=[]
    for rid,_ in ag_res:
        ca=[a for a in ag_atoms if a[2]==rid and a[1]=='CA' or (a[2]==rid and a[1] in ('C1*','P'))]
        xyz.append(ca[0][3:6] if ca else [np.nan]*3)
    xyz=np.array(xyz,float)
    n=len(seq)
    # interface truth: any heavy atom within 5A of antibody atoms
    truth=np.zeros(n,int)
    ag_all=[a for a in atoms if a[0]==ag]
    for i,rid in enumerate(ids):
        pts=np.array([[a[3],a[4],a[5]] for a in ag_all if a[2]==rid])
        if len(pts)==0: continue
        d=np.sqrt(((pts[:,None,:]-ab_xyz[None,:,:])**2).sum(-1)).min()
        truth[i]=int(d<5.0)
    # features
    F=[]
    for i in range(n):
        row=[]
        for S in SCALES:
            w=[S.get(seq[j],0) for j in range(max(0,i-2),min(n,i+3))]
            row.append(np.mean(w))
        row+=list(ATCH.get(seq[i],(0,)*5))
        F.append(row)
    F=np.array(F)
    # burial: CA neighbor count 10A
    allca=np.array([[a[3],a[4],a[5]] for a in atoms if a[1]=='CA'])
    bur=[]
    for i in range(n):
        if np.isnan(xyz[i,0]): bur.append(0); continue
        bur.append(int((np.sqrt(((allca-xyz[i])**2).sum(1))<10).sum()-1))
    F=np.c_[F,np.array(bur)]
    return dict(ids=ids,seq=''.join(seq),truth=truth.tolist(),F=F.tolist(),n_ab=len(ab),ag_chain=ag)
if __name__=='__main__':
    import sys
    r=featurize(sys.argv[1])
    if r is None: print('INELIGIBLE')
    else: print('n=%d interface=%d chains ab=%d ag=%s'%(len(r['ids']),sum(r['truth']),r['n_ab'],r['ag_chain']))
