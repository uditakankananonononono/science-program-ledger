from pathlib import Path
import pandas as pd, numpy as np, json, hashlib
R=Path(__file__).resolve().parents[2]
out=R/'experiment/data';out.mkdir(parents=True,exist_ok=True)
# UCI diabetes extraction, endpoint and independent-unit IDs only. No fitting here.
p=R/'data-feasibility/diabetes130/diabetic_data.csv'; d=pd.read_csv(p,na_values=['?'])
d['target_30d']=(d.readmitted=='<30').astype(int)
# exclusion fixed in protocol: death/hospice dispositions 11,13,14,19,20,21
d=d[~d.discharge_disposition_id.isin([11,13,14,19,20,21])].copy()
# preserve order proxy by encounter_id rank; encounter ID never predictor
d['encounter_order']=d.encounter_id.rank(method='first').astype(int)
d.to_csv(out/'diabetes.csv.gz',index=False,compression='gzip')
# Parkinson extraction
p=R/'data-feasibility/parkinsons/parkinsons_updrs.data'; z=pd.read_csv(p).rename(columns={'subject#':'subject'})
z.to_csv(out/'parkinsons.csv.gz',index=False,compression='gzip')
manifest={'diabetes':{'rows':len(d),'patients':int(d.patient_nbr.nunique()),'positives':int(d.target_30d.sum())},'parkinsons':{'rows':len(z),'subjects':int(z.subject.nunique()),'time_min':float(z.test_time.min()),'time_max':float(z.test_time.max())}}
json.dump(manifest,open(out/'domain_manifest.json','w'),indent=2)
print(json.dumps(manifest,indent=2))
