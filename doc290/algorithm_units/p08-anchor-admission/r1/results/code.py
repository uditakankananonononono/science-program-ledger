"""Measured source table/coordinate figure reproduction only. No author code executed."""
from pathlib import Path
import json,hashlib,zipfile,io,csv
import numpy as np

def transform_trajectory(a,index):
    return np.column_stack((-a[:,1]/21,a[:,0]/21+20-6*index,a[:,2]/29.5,a[:,3]))
def transform_profile(a):return np.column_stack((a[:,1]/29.5,a[:,0]/21))
def transform_ramp(a):
    xy=a[:,:2]/21;theta=np.deg2rad(0.8);rot=xy@np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])
    rot-=(rot[0]-xy[0])/2;rot-=np.array([rot[0,0],148/21])
    return np.column_stack((-rot[:,0],rot[:,1],a[:,2]/29.5,a[:,3]))

def load_tables(archive,manifest):
    if hashlib.sha256(Path(archive).read_bytes()).hexdigest()!=manifest['subset_sha256']:raise ValueError('subset hash')
    tables={}
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('CRC')
        for r in manifest['entries']:
            raw=z.read(r['name'])
            if len(raw)!=r['size'] or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('entry hash')
            if not r['name'].startswith('Fig3/') or not r['name'].endswith('.txt'):continue
            if raw.decode().splitlines()[0]!=r['header']:raise ValueError('header')
            a=np.loadtxt(io.BytesIO(raw))
            if list(a.shape)!=r['shape'] or int((~np.isfinite(a)).sum())!=r['nonfinite_count']:raise ValueError('schema')
            if 'flowprofile' in r['name']:
                if not np.isfinite(a[:,0]).all() or np.isinf(a).any():raise ValueError('profile missingness')
            elif not np.isfinite(a).all():raise ValueError('trajectory finite')
            tables[r['name']]=a
    if len(tables)!=11:raise ValueError('eleven Fig3 tables')
    return tables

def generate(archive,manifest,output):
    tables=load_tables(archive,manifest);output=Path(output);output.mkdir(parents=True,exist_ok=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    records=[]
    def save(name,a,header):
        path=output/(name+'.csv');np.savetxt(path,a,delimiter=',',header=header,comments='',fmt='%.17g')
        records.append({'file':path.name,'rows':len(a),'nonfinite_count':int((~np.isfinite(a)).sum()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    fig,axes=plt.subplots(1,2,figsize=(11,7),layout='constrained');ax,prof=axes
    for index,V in enumerate(range(1,6)):
        t=tables[f'Fig3/Poiseuille_E_traj_{V}V.txt'];p=tables[f'Fig3/Poiseuille_E0V_flowprofile_{V}V.txt'];d=transform_trajectory(t,index);q=transform_profile(p)
        save(f'trajectory_{V}V',d,'display_minus_y_over_21,display_x_over_21_plus_offset,speed_over_29.5,voltage_V');save(f'profile_{V}V',q,'u_over_29.5,y_over_21')
        sc=ax.scatter(d[:,0],d[:,1],c=d[:,3],s=2,cmap='viridis',vmin=0,vmax=5)
        prof.plot(q[:,0],q[:,1],'.-',label=f'{V} V: {int(np.isfinite(q[:,0]).sum())}/{len(q)} finite')
    ax.set(xlabel='Displayed -y / 21 um',ylabel='Displayed x / 21 um + stagger',title='Fig3a source-coordinate content');fig.colorbar(sc,ax=ax,label='Applied voltage (V)')
    prof.set(xlabel='Flow speed / 29.5 um/s',ylabel='y / 21 um',title='Pre-field PIV profiles: 3 NaNs retained');prof.legend(fontsize=9)
    fig.suptitle('Electrotaxis source tables, not a dynamics fit',fontsize=16);fig.savefig(output/'constant_and_profiles.png',dpi=150);plt.close(fig)
    ramp=transform_ramp(tables['Fig3/Poiseuille_E_ramp_0-5V.txt']);save('ramp',ramp,'display_negative_rotated_x,display_rotated_y,speed_over_29.5,voltage_V')
    fig,ax=plt.subplots(figsize=(11,4.5),layout='constrained');sc=ax.scatter(ramp[:,0],ramp[:,1],c=ramp[:,3],s=2,cmap='viridis',vmin=0,vmax=5)
    ax.set(xlabel='Displayed negative x after 0.8 degree rotation/translation',ylabel='Displayed y after source translation',title='Fig3b source-coordinate content: all 5946 rows');fig.colorbar(sc,ax=ax,label='Applied voltage (V)');fig.savefig(output/'ramp.png',dpi=150);plt.close(fig)
    (output/'derived-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':
    import sys
    generate(sys.argv[1],json.loads(Path(sys.argv[2]).read_text()),sys.argv[3])
