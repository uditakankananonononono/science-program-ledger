"""Stationary measured-profile descriptive OLS diagnostic, no physical validation."""
import json,hashlib,zipfile,io,sys,platform,importlib.metadata,csv
from pathlib import Path
import numpy as np

def fit(f,u):
    den=float(f@f)
    if not np.isfinite(den) or den<=0:raise ValueError('zero/nonfinite basis denominator')
    amplitude=float((f@u)/den)
    coef,_,rank,_=np.linalg.lstsq(f[:,None],u,rcond=None)
    if rank!=1 or not np.isfinite(amplitude) or not np.isfinite(coef).all():raise ValueError('fit rank/finite')
    if not np.allclose(amplitude,coef[0],atol=1e-10,rtol=1e-12) or not np.allclose(amplitude*f,coef[0]*f,atol=1e-10,rtol=1e-12):raise RuntimeError('arithmetic comparator disagreement')
    return amplitude,float(coef[0])

def diagnostic(a):
    a=np.asarray(a,float)
    if a.ndim!=2 or a.shape[1]!=2 or not np.isfinite(a[:,0]).all() or np.isinf(a).any():raise ValueError('profile schema/finite positions')
    y,u=a.T;f=1-(y/50)**2;mask=np.isfinite(u)
    if mask.sum()<2:raise ValueError('two finite speeds required')
    amp,cmp=fit(f[mask],u[mask]);pred=amp*f;rows=[];res=[];loo=[]
    for i in range(len(y)):
        row={'row':i,'y_um':float(y[i]),'basis':float(f[i]),'observed_um_per_s':float(u[i]) if mask[i] else None,'predicted_um_per_s':float(pred[i]),'residual_um_per_s':None,'absolute_residual':None,'squared_residual':None,'loo_amplitude':None,'loo_prediction':None,'loo_error':None}
        if mask[i]:
            error=float(u[i]-pred[i]);other=mask.copy();other[i]=False
            aa,cc=fit(f[other],u[other]);prediction=float(aa*f[i]);held=float(u[i]-prediction)
            row.update(residual_um_per_s=error,absolute_residual=abs(error),squared_residual=error**2,loo_amplitude=aa,loo_prediction=prediction,loo_error=held)
            res.append(error);loo.append(held)
        rows.append(row)
    stats=lambda errors:{'sse':float(np.sum(np.square(errors))),'rmse':float(np.sqrt(np.mean(np.square(errors)))),'mae':float(np.mean(np.abs(errors))),'max_absolute':float(np.max(np.abs(errors))),'mean_signed':float(np.mean(errors))}
    return {'total_rows':len(y),'finite_rows':int(mask.sum()),'missing_rows':int((~mask).sum()),'amplitude_um_per_s':amp,'lstsq_amplitude':cmp,'in_sample':stats(res),'leave_one_location':stats(loo),'rows':rows}

def load(archive,protocol):
    if protocol['python']!=sys.version or any(importlib.metadata.version(n)!=v for n,v in protocol['packages'].items()):raise ValueError('environment pin')
    if hashlib.sha256(Path(archive).read_bytes()).hexdigest()!=protocol['subset_sha256']:raise ValueError('archive pin')
    names=[f'Fig3/Poiseuille_E0V_flowprofile_{v}V.txt' for v in range(1,6)]
    if [r['name'] for r in protocol['profiles']]!=names:raise ValueError('exact profile set/order')
    out={}
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('CRC')
        for r in protocol['profiles']:
            raw=z.read(r['name'])
            if hashlib.sha256(raw).hexdigest()!=r['sha256'] or len(raw)!=r['size'] or raw.decode().splitlines()[0]!=r['header']:raise ValueError('entry pin')
            a=np.loadtxt(io.BytesIO(raw))
            if list(a.shape)!=r['shape'] or int((~np.isfinite(a)).sum())!=r['nonfinite_count']:raise ValueError('shape/missingness pin')
            out[r['name']]=a
    return out

def generate(archive,protocol,output):
    tables=load(archive,protocol);out=Path(output);out.mkdir(parents=True,exist_ok=False)
    results=[{'profile':name,**diagnostic(a)} for name,a in tables.items()]
    (out/'raw.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
    for r in results:
        path=out/(r['profile'].split('/')[-1][:-4]+'.csv')
        with path.open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(r['rows'][0]));writer.writeheader();writer.writerows(r['rows'])
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,5,figsize=(17,5),sharex=True,sharey=True,layout='constrained')
    for ax,r in zip(axes,results):
        rows=r['rows'];y=[a['y_um'] for a in rows];u=[np.nan if a['observed_um_per_s'] is None else a['observed_um_per_s'] for a in rows];pr=[a['predicted_um_per_s'] for a in rows]
        ax.plot(y,u,'o',ms=4,label='Observed');ax.plot(y,pr,'-',label='Amplitude OLS')
        missing=[a['y_um'] for a in rows if a['observed_um_per_s'] is None]
        ax.plot(missing,[.025]*len(missing),'rx',transform=ax.get_xaxis_transform(),label='Missing speed: bottom strip marker')
        ax.set(title=f"{r['profile'].split('_')[-1][:-4]} pre-field\n{r['finite_rows']}/{r['total_rows']} finite",xlabel='y (um)')
    axes[0].set_ylabel('Speed (um/s)');handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside lower center',ncol=3);fig.suptitle('Measured zero-field profiles: amplitude-only parabola, not physics validation');fig.savefig(out/'profiles.png',dpi=140);plt.close(fig)
    limit=max(abs(a[k]) for r in results for a in r['rows'] for k in ('residual_um_per_s','loo_error') if a[k] is not None);limit=max(limit*1.1,1e-12)
    fig,axes=plt.subplots(1,5,figsize=(17,5),sharex=True,sharey=True,layout='constrained')
    for ax,r in zip(axes,results):
        finite=[a for a in r['rows'] if a['observed_um_per_s'] is not None]
        ax.axhline(0,color='#aaa',lw=.6);ax.plot([a['y_um'] for a in finite],[a['residual_um_per_s'] for a in finite],'o',label='In sample');ax.plot([a['y_um'] for a in finite],[a['loo_error'] for a in finite],'x',label='Leave one location')
        ax.set(title=f"{r['profile'].split('_')[-1][:-4]} pre-field",xlabel='y (um)',ylim=(-limit,limit))
    axes[0].set_ylabel('Observed minus predicted speed (um/s)');handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside lower center',ncol=2);fig.suptitle('Descriptive spatial errors: common scale, no calibrated tolerance');fig.savefig(out/'residuals.png',dpi=140);plt.close(fig)
    files=sorted(out.iterdir())
    provenance={'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'protocol_sha256':hashlib.sha256(json.dumps(protocol,sort_keys=True).encode()).hexdigest(),'python':sys.version,'platform':platform.platform(),'packages':{n:importlib.metadata.version(n) for n in protocol['packages']},'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (out/'manifest.json').write_text(json.dumps(provenance,indent=2)+'\n')
if __name__=='__main__':
    generate(sys.argv[1],json.loads(Path(sys.argv[2]).read_text()),sys.argv[3])
