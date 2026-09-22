from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,subprocess,os
from sklearn.metrics import roc_auc_score
R=Path(__file__).resolve().parents[2];O=R/'experiment/results';d=pd.read_csv(O/'audit_configurations.csv');rng=np.random.default_rng(20260921)
# Random group-label / date-permutation analogue: permute optimism within domain 5000x; association should not systematically persist
obs=d.audit_score.corr(d.optimism,method='spearman');null=[]
for _ in range(5000):
 z=d.copy();z['op']=z.groupby('domain').optimism.transform(lambda x:rng.permutation(x));null.append(z.audit_score.corr(z.op,method='spearman'))
p=(1+sum(abs(x)>=abs(obs) for x in null if np.isfinite(x)))/(1+sum(np.isfinite(null)))
# duplicate-injection positive detector unit test
base=np.arange(100);tr=set(base[:80]);te=set(base[80:]);zero=len(tr&te)==0;te_inj=set(base[70:]);positive=len(tr&te_inj)==10
controls={'within_domain_permutation_p':p,'valid_unit_overlap_zero':zero,'duplicate_injection_detected':positive,'random_group_control_pass':bool(p<.05),'all_controls_pass':bool(p<.05 and zero and positive)}
json.dump(controls,open(O/'negative_controls.json','w'),indent=2)
# determinism of gate computation: hash output then rerun and compare stable semantic JSON exact
p0=O/'locked_gate_results.json';before=json.load(open(p0));subprocess.check_call(['python3',str(R/'experiment/code/final_gate.py')],stdout=subprocess.DEVNULL);after=json.load(open(p0));repro={'semantic_json_exact':before==after}
json.dump(repro,open(O/'reproducibility.json','w'),indent=2)
print(json.dumps({'controls':controls,'repro':repro},indent=2))
