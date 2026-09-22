from pathlib import Path
import pandas as pd,numpy as np,json
from scipy.stats import spearmanr
R=Path(__file__).resolve().parents[2];O=R/'experiment/results';d=pd.read_csv(O/'primary_results.csv')
# paired configuration optimism from aggregate split performance
agg=d.groupby(['domain','model','split']).metric.mean().unstack('split').dropna().reset_index();agg['optimism_delta']=agg.naive-agg.rigorous_group
agg.to_csv(O/'optimism_by_config.csv',index=False)
# R1 first-stage audit score: prespecified group/cohort-delta dimension only is computable from these runs.
# Composite issuance correctly withheld (<5/7 dimensions), causing all-required gate failure until/full audit dimensions run.
result={'optimism':agg.to_dict('records'),'domains_with_material_optimism':int((agg.groupby('domain').optimism_delta.max()>=.05).sum()),'composite_issued':False,'dimensions_available':1,'dimensions_required':5,'scientific_gate_status':'FAIL_INCOMPLETE_AUDIT_DIMENSIONS','paper_allowed':False}
json.dump(result,open(O/'round1_interim_gate.json','w'),indent=2)
print(json.dumps(result,indent=2))
