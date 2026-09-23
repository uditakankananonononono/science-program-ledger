import wfdb,numpy as np,neurokit2 as nk,pickle,sys,warnings; warnings.filterwarnings('ignore')
RECS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230,100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
BEATS=set('NLRBAaJSVrFejnE/fQ?'); M=['pantompkins1985','hamilton2002','elgendi2010','christov2004','neurokit']
CLEAN={'pantompkins1985':'pantompkins1985','hamilton2002':'hamilton2002','elgendi2010':'elgendi2010','neurokit':'neurokit','christov2004':'neurokit'}
out={}
for r in RECS:
    rec=wfdb.rdrecord(f'../data/mitdb/{r}',channels=[0]); ann=wfdb.rdann(f'../data/mitdb/{r}','atr')
    sig=rec.p_signal[:,0]; ref=np.array([s for s,c in zip(ann.sample,ann.symbol) if c in BEATS])
    det={}
    for m in M:
        try:
            cl=nk.ecg_clean(sig,sampling_rate=360,method=CLEAN[m]); _,info=nk.ecg_peaks(cl,sampling_rate=360,method=m,correct_artifacts=False)
            det[m]=np.asarray(info['ECG_R_Peaks'],int)
        except Exception as e: det[m]=np.array([],int); print(r,m,'ERR',e,flush=True)
    out[r]={'ref':ref,'det':det,'n':len(sig)}; print(r,len(ref),{m:len(v) for m,v in det.items()},flush=True)
pickle.dump(out,open('../data/detections.pkl','wb'))
