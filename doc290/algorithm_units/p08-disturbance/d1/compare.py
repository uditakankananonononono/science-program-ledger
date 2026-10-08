"""Frozen full battery entry point; not executed before publication."""
from pathlib import Path
import json
from fractions import Fraction as F
from harness import run,Proportional,Sign

def score(manifest):
    if manifest['policy_reset_and_action_wall_seconds']!=1.0:raise ValueError('fixed timeout mismatch')
    policies={'proportional':Proportional,'sign':Sign};results=[]
    plant={key:F(manifest[key]) for key in ('initial','target','dt','bound','lower','upper','tolerance')}
    for name in manifest['policies']:
        for entry in manifest['cases']:
            c=entry['sequence'];case={key:[F(x) for x in c[key]] if key in ('gain','drift') else c[key] for key in c}
            results.append({'policy':name,'case':entry['name'],**run(policies[name],case,**plant)})
    return results
if __name__=='__main__':
    m=json.loads(Path(__file__).with_name('manifest.json').read_text())
    print(json.dumps(score(m),default=str,indent=2))
