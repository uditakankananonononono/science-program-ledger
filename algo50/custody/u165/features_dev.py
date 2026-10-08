import json,zipfile,io,re,os,numpy as np,pandas as pd
from scipy.signal import welch
root='/tmp/unit165/';labels=zipfile.ZipFile('/downloads/zen14182446-self_perceived_fatigue_index-d70ffa61.zip');prime={1:1,2:0,3:3,4:2,5:0,6:1,7:2,8:3,9:1,10:0,11:3,12:2};rows=[];audit=[]
for sid in [1,3,5,7,9,11,13]:
 p=root+f'dev_raw/subject_{sid}.zip';out=root+f'dev_raw/features_{sid}.csv'
 if os.path.exists(out) or not os.path.exists(p+'.verified.json'):continue
 z=zipfile.ZipFile(p);gt=zipfile.ZipFile(io.BytesIO(labels.read(f'self_perceived_fatigue_index/subject_{sid}.zip')));rr=[]
 survey={x['trial']:x for x in json.load(open(root+f'dev_raw/survey_{sid}.json'))}
 for trial in range(1,13):
  if survey[trial]['exclude']:continue
  d=pd.read_csv(z.open(f'subject_{sid}/trial_{trial}.csv'));g=pd.read_csv(gt.open(next(n for n in gt.namelist() if n.lower()==f'subject_{sid}/trial_{trial}.csv')));v=d.to_numpy();removed=survey[trial]['suffix_removed'];v=v[:-removed] if removed else v;t=v[:,prime[trial]*2];sig=v[:,prime[trial]*2+1];dt=np.diff(t);fs=1/np.median(dt)
  assert np.isfinite(v).all() and np.all(dt>0) and abs(fs-1259)<5 and t[0]==0
  audit.append({'subject':sid,'trial':trial,'rows':len(d),'columns':list(d.columns),'start':float(t[0]),'stop':float(t[-1]),'label_stop':float(g.time.iloc[-1]),'estimated_fs':fs,'license_members':[n for n in z.namelist() if any(k in n.lower() for k in ['license','readme','terms'])]})
  # Nonoverlapping 5-second windows; within-window label majority, exclude changing-level windows.
  first=None;prev=None
  for start in np.arange(5,min(t[-1],g.time.iloc[-1])-5,5):
   end=start+5;x=sig[(t>=start)&(t<end)];gg=g.loc[(g.time>=start)&(g.time<end),'label'].to_numpy()
   if len(x)<.95*fs*5 or len(gg)==0 or len(np.unique(gg))!=1:continue
   fre,pow=welch(x,fs=fs,nperseg=min(1024,len(x)));mask=(fre>=20)&(fre<=450);f=fre[mask];ps=pow[mask];s=ps.sum()
   if s<=0:continue
   mdf=float(f[np.searchsorted(np.cumsum(ps),s/2)]);mnf=float((f*ps).sum()/s);rms=float(np.sqrt(np.mean(x*x)));features=np.array([np.log(rms+1e-12),mdf,mnf,float(np.mean(np.abs(np.diff(x)))),float(np.mean(x[:-1]*x[1:]<0))])
   if first is None:first=features.copy()
   delta=features-first;change=features-(prev if prev is not None else features);prev=features.copy()
   row={'subject':sid,'trial':trial,'time':start,'y':int(gg[0])};row.update({f'f{i}':a for i,a in enumerate(features)});row.update({f'd{i}':a for i,a in enumerate(delta)});row.update({f'c{i}':a for i,a in enumerate(change)});rr.append(row)
 pd.DataFrame(rr).to_csv(out,index=False);print('FEATURES',sid,len(rr),flush=True)
 path=root+f'dev_raw/audit_{sid}.json';json.dump([a for a in audit if a['subject']==sid],open(path,'w'),indent=2)
