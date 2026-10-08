"""Frozen D2 entry point; full battery not executed before publication."""
from pathlib import Path
import json,hashlib
from fractions import Fraction as F
from harness import run,HoldP,PredictP,HoldSign,PredictSign

def pair(a,b,n):
    # b minus a, prediction minus hold. No early-run metric 'wins'.
    result={'hold_outcome':a['outcome'],'predict_outcome':b['outcome'],'hold_steps':a['completed_steps'],'predict_steps':b['completed_steps']}
    complete=all(r['completed_steps']==n and r['outcome'] in ('success','terminal_miss') for r in (a,b))
    for metric,count in (('final_error',None),('control_effort',None),('estimation_mae','valid_estimate_count'),('estimation_mse','valid_estimate_count'),('dropout_mae','valid_dropout_estimate_count'),('dropout_mse','valid_dropout_estimate_count')):
        valid=complete and a[metric] is not None and b[metric] is not None and (count is None or a[count]==b[count])
        result[metric]={'comparable':valid,'predict_minus_hold':b[metric]-a[metric] if valid else None,'hold_count':a[count] if count else a['completed_steps'],'predict_count':b[count] if count else b['completed_steps']}
    return result

def score(m):
    d1=Path(__file__).resolve().parent.parent/'d1/manifest.json'
    if hashlib.sha256(d1.read_bytes()).hexdigest()!=m['d1_manifest_sha256']:raise ValueError('D1 identity')
    if json.loads(d1.read_text())['cases']!=m['cases']:raise ValueError('D1 sequence change')
    policies={'hold_p':HoldP,'predict_p':PredictP,'hold_sign':HoldSign,'predict_sign':PredictSign};rows=[]
    plant={k:F(m[k]) for k in ('initial','target','dt','bound','lower','upper','tolerance')}
    for name in m['policies']:
        for entry in m['cases']:
            c=entry['sequence'];c={k:[F(x) for x in v] if k in ('gain','drift') else v for k,v in c.items()}
            rows.append({'policy':name,'case':entry['name'],**run(policies[name],c,**plant)})
    pairs=[]
    for rule in ('p','sign'):
        for entry in m['cases']:
            get=lambda name:next(r for r in rows if r['case']==entry['name'] and r['policy']==name)
            pairs.append({'rule':rule,'case':entry['name'],**pair(get('hold_'+rule),get('predict_'+rule),len(entry['sequence']['gain']))})
    return {'rows':rows,'pairs':pairs}
if __name__=='__main__':
    print(json.dumps(score(json.loads(Path(__file__).with_name('manifest.json').read_text())),default=str,indent=2))
