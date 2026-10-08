import json,zipfile,io,os,hashlib,numpy as np,pandas as pd
root='/tmp/unit165/';assert hashlib.sha256(open(root+'PREPROCESSING_PROTOCOL.md','rb').read()).hexdigest()=='0f8adb3161d21ff91d921b407b9e96deea1e3edefe49d35e01881d5f01e8adf7';labels=zipfile.ZipFile('/downloads/zen14182446-self_perceived_fatigue_index-d70ffa61.zip')
for sid in [1,3,5,7,9,11,13]:
 p=root+f'dev_raw/subject_{sid}.zip';out=root+f'dev_raw/survey_{sid}.json'
 if not os.path.exists(p+'.verified.json'):continue
 z=zipfile.ZipFile(p);gt=zipfile.ZipFile(io.BytesIO(labels.read(f'self_perceived_fatigue_index/subject_{sid}.zip')));rr=[]
 for tr in range(1,13):
  d=pd.read_csv(z.open(f'subject_{sid}/trial_{tr}.csv'));v=d.to_numpy();row={'subject':sid,'trial':tr,'original_rows':len(v),'suffix_removed':0,'exclude':False,'reasons':[]}
  if v.shape[1]!=8 or not np.issubdtype(v.dtype,np.number) or not np.isfinite(v).all():row['reasons'].append('schema_or_finite_fail')
  else:
   decreases=np.any(np.diff(v[:,::2],axis=0)<0,axis=1);resets=int(decreases.sum());i=len(v)
   while i>0 and np.all(v[i-1]==0):i-=1
   if 0<i<len(v) and np.any(v[i,::2]<v[i-1,::2]):row['suffix_removed']=len(v)-i;v=v[:i]
   if resets>1:row['reasons'].append('multiple_resets')
   if len(v)==0:row['reasons'].append('absent_valid_prefix')
   else:
    dt=np.diff(v[:,::2],axis=0)
    if np.any(dt<=0):row['reasons'].append('remaining_nonmonotonic')
    if np.all(v[:,1::2]==0):row['reasons'].append('entirely_zero_signal')
    row.update({'retained_rows':len(v),'four_clock_max_abs_difference':float(np.max(np.abs(v[:,::2]-v[:,0,None]))),'start_times':v[0,::2].tolist(),'end_times':v[-1,::2].tolist(),'median_intervals':np.median(dt,axis=0).tolist()})
   g=pd.read_csv(gt.open(next(n for n in gt.namelist() if n.lower()==f'subject_{sid}/trial_{tr}.csv')));row.update({'label_start':float(g.time.iloc[0]),'label_stop':float(g.time.iloc[-1]),'label_monotonic':bool(np.all(np.diff(g.time)>0)),'label_finite':bool(np.isfinite(g.to_numpy()).all()),'label_levels':sorted(int(x) for x in g.label.unique())})
  if not row.get('label_monotonic',False):row['reasons'].append('nonincreasing_label_clock')
  row['exclude']=bool(row['reasons']);rr.append(row)
 json.dump(rr,open(out,'w'),indent=2);print('SURVEY',sid,'suffix_trials',sum(x['suffix_removed']>0 for x in rr),'rows',sum(x['suffix_removed'] for x in rr),'excluded',sum(x['exclude'] for x in rr),flush=True)
