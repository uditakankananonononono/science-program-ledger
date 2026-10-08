"""F2 frozen-candidate boundary diagnostic, evaluation requires publication."""
import pathlib,sys,json,hashlib,argparse
from fractions import Fraction as F
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
from feasibility import solve
from reduced_terminal import solve_reduced
from rational_terminal import solve_terminal

def case(scale,offset):
    b=F(scale);target=b*(F(3,2)+F(offset))
    exact=solve_terminal([0],[target],[1,1],[[b]],[2],[F(1,2)],[0])
    args=([0],[float(target)],[1,1],[[float(b)]],[2],[.5],[0]);results={}
    for name,method in (('full',solve),('reduced',solve_reduced)):
        try:
            r=method(*args);out={'status':r['status'],'residuals':r.get('residuals'),'exception':None}
            if r['status']=='primal_checked':
                u=[F.from_float(float(row[0])) for row in r['controls']]
                terminal=b*sum(u);slew=max(abs(u[0]),abs(u[1]-u[0]))
                out.update({'controls':r['controls'],'exact_binary_control_declared_terminal':str(terminal),
                            'exact_declared_target_error':str(abs(terminal-target)),
                            'exact_actuator_violation':str(max(F(0),max(abs(x) for x in u)-2)),
                            'exact_slew_violation':str(max(F(0),slew-F(1,2)))})
        except Exception as e:out={'status':'exception','exception':type(e).__name__+': '+str(e)}
        results[name]=out
    return {'scale':str(b),'offset':str(F(offset)),'declared_target':str(target),'exact_status':exact['status'],
            'float_B_conversion_delta':str(F.from_float(float(b))-b),'float_target_conversion_delta':str(F.from_float(float(target))-target),
            'float_results':results}

def run(spec):
    rows=[case(scale,offset) for scale in spec['evaluation_scales'] for offset in spec['evaluation_relative_offsets']]
    summary={}
    for name in ('full','reduced'):
        summary[name]={'rows':len(rows),'exceptions':sum(r['float_results'][name]['status']=='exception' for r in rows),
            'exact_unreachable_float_primal_checked':sum(r['exact_status']=='exact_model_unreachable' and r['float_results'][name]['status']=='primal_checked' for r in rows),
            'exact_reachable_float_infeasible':sum(r['exact_status']=='exact_model_reachable' and r['float_results'][name]['status']=='solver_infeasible' for r in rows)}
    return {'protocol_id':spec['id'],'scope':spec['scope'],'raw':rows,'summary':summary}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--published-freeze-reference',required=True);a=p.parse_args()
    protocol=HERE/'protocol.json';r=run(json.loads(protocol.read_text()));r['published_freeze_reference']=a.published_freeze_reference
    names=[protocol,HERE/'compare.py']+[HERE.parent/n for n in ('feasibility.py','reduced_terminal.py','rational_terminal.py','integral_lift.py','rational_support.py')]
    r['manifest_hashes']={str(f.relative_to(HERE.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in names}
    pathlib.Path(a.output).write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
