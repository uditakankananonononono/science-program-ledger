"""F1 frozen candidate comparison harness, scoring requires publication."""
import pathlib,sys,json,time,hashlib,argparse
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from feasibility import solve
from reduced_terminal import solve_reduced

def instance(spec,seed,n,kind):
    rng=np.random.default_rng(seed);d=spec['state_dimension'];m=spec['actuators']
    B=rng.standard_normal((d,m));dt=rng.uniform(*spec['dt_uniform'],size=n)
    cap=np.full(m,spec['actuator_limit']);rate=np.full(m,spec['slew']);prev=rng.uniform(*spec['previous_uniform'],size=m)
    elapsed=np.cumsum(dt);lo=np.maximum(-cap,prev-elapsed[:,None]*rate);hi=np.minimum(cap,prev+elapsed[:,None]*rate)
    mix=rng.uniform(*spec['mixture_uniform'],size=m);u=(1-mix)*lo+mix*hi
    if kind=='rank_deficient_impossible':B[0]=0
    elif kind!='constructed_feasible':raise ValueError('unknown instance class')
    target=(dt@u)@B.T
    if kind=='rank_deficient_impossible':target[0]=1.
    return [np.zeros(d),target,dt,B,cap,rate,prev]

def call(method,args):
    start=time.perf_counter()
    try:
        r=(solve if method=='full' else solve_reduced)(*args)
        out={'status':r['status'],'residuals':r.get('residuals'),'exception':None}
    except Exception as e:out={'status':'exception','exception':type(e).__name__+': '+str(e),'residuals':None}
    out['wall_seconds']=time.perf_counter()-start;return out

def run(spec):
    warm=instance(spec,spec['development_seed'],8,'constructed_feasible')
    warm_results={m:call(m,warm) for m in ('full','reduced')}
    rows=[];ordinal=0
    for n in spec['horizons']:
        for kind in spec['classes']:
            for seed in spec['evaluation_seeds']:
                args=instance(spec,seed,n,kind)
                instance_hash=hashlib.sha256(b''.join(np.asarray(a,dtype='<f8').tobytes() for a in args)).hexdigest()
                for repeat in range(spec['repetitions']):
                    order=['full','reduced'] if (ordinal+repeat)%2==0 else ['reduced','full']
                    results={m:call(m,args) for m in order}
                    expected='primal_checked' if kind=='constructed_feasible' else 'solver_infeasible'
                    row={'seed':seed,'horizon':n,'class':kind,'repeat':repeat,'order':order,'instance_sha256':instance_hash,
                         'expected_status':expected,'results':results,'both_match_expected':all(r['status']==expected for r in results.values())}
                    if all(r['status']!='exception' for r in results.values()):
                        row['full_over_reduced_time']=results['full']['wall_seconds']/results['reduced']['wall_seconds']
                        row['reduced_minus_full_seconds']=results['reduced']['wall_seconds']-results['full']['wall_seconds']
                    rows.append(row)
                ordinal+=1
    summaries=[]
    for n in spec['horizons']:
        for kind in spec['classes']:
            group=[r for r in rows if r['horizon']==n and r['class']==kind];pairs=[r for r in group if 'full_over_reduced_time' in r]
            summaries.append({'horizon':n,'class':kind,'rows':len(group),'status_mismatch_rows':sum(not r['both_match_expected'] for r in group),
                'exceptions':{m:sum(r['results'][m]['status']=='exception' for r in group) for m in ('full','reduced')},
                'timed_pairs':len(pairs),'median_full_over_reduced':float(np.median([r['full_over_reduced_time'] for r in pairs])) if pairs else None,
                'mean_call_seconds':{m:float(np.mean([r['results'][m]['wall_seconds'] for r in group])) for m in ('full','reduced')},
                'reduced_lower_equal_higher':[sum(r['reduced_minus_full_seconds']<0 for r in pairs),sum(r['reduced_minus_full_seconds']==0 for r in pairs),sum(r['reduced_minus_full_seconds']>0 for r in pairs)]})
    return {'protocol_id':spec['id'],'scope':spec['scope'],'warmup':warm_results,'raw':rows,'summary':summaries}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--published-freeze-reference',required=True)
    a=parser.parse_args();p=HERE/'protocol.json';r=run(json.loads(p.read_text()));r['published_freeze_reference']=a.published_freeze_reference
    r['manifest_hashes']={str(f.relative_to(HERE.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (p,HERE/'compare.py',HERE.parent/'feasibility.py',HERE.parent/'reduced_terminal.py')}
    pathlib.Path(a.output).write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
