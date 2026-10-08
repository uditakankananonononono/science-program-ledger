"""S2 pre-score harness. No evaluation without published freeze."""
import json,pathlib,sys,hashlib,argparse
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent));sys.path.insert(0,str(HERE.parent.parent/'p08-tracking'))
from kalman import ConstantVelocity
from deferred import resolve

def model(dt,q):
    F=np.eye(4);F[0,2]=F[1,3]=dt;Q=np.zeros((4,4))
    for a,b in ((0,2),(1,3)):
        Q[a,a]=q*dt**3/3;Q[a,b]=Q[b,a]=q*dt**2/2;Q[b,b]=q*dt
    return F,Q

def rmse(output,truth,indices):
    error=np.asarray(output)[indices,:2]-truth[indices,:2]
    return float(np.sqrt(np.mean(np.sum(error**2,axis=1))))

def trajectory(spec,seed,scenario):
    rng=np.random.default_rng(seed);n=spec['steps'];prior=np.array(spec['initial_mean'],float);P=np.diag(spec['initial_covariance_diagonal'])
    x=prior+rng.multivariate_normal(np.zeros(4),P);dt=rng.uniform(*spec['dt_uniform'],size=n)
    process=rng.standard_normal((n,4));noise=rng.standard_normal((n,2))
    truth=[];observations=[];R=np.eye(2)*spec['measurement_sigma']**2
    for i in range(n):
        F,Q=model(dt[i],spec['q']);x=F@x+np.linalg.cholesky(Q)@process[i]
        if scenario['maneuver'] and i==spec['maneuver_index']:x[2:]+=spec['maneuver_velocity_jump']
        truth.append(x.copy());z=x[:2]+spec['measurement_sigma']*noise[i]
        if i in scenario['corrupt_indices']:z=z+spec['corruption_offset']
        observations.append(None if i in spec['missing_indices'] else z)
    truth=np.array(truth);first=spec['first_return_index'];confirmation=spec['confirmation_index']
    if confirmation!=first+1 or observations[first] is None or observations[confirmation] is None:raise ValueError('unsupported return/confirmation schedule')
    outputs={};reject_indices=[];decision=None
    for method in ('immediate','gated','deferred'):
        kf=ConstantVelocity(prior,P,spec['q']);out=[]
        for i,z in enumerate(observations):
            if method=='deferred' and i==first:
                before=(kf.state.copy(),kf.covariance.copy());result=kf.step(dt[i])
            elif method=='deferred' and i==confirmation:
                decision=resolve(*before,spec['q'],dt[first],observations[first],R,dt[i],z,R)
                result=decision['confirmed'];kf.state=result['state'].copy();kf.covariance=result['covariance'].copy()
            elif method=='gated' and z is not None:
                prediction=ConstantVelocity(kf.state,kf.covariance,spec['q']).step(dt[i])
                e=z-prediction['state'][:2];S=prediction['covariance'][:2,:2]+R
                nis=float(e@np.linalg.solve(S,e))
                use=nis<=spec['gate_nis_threshold']
                if not use:reject_indices.append(i)
                result=kf.step(dt[i],z if use else None,R if use else None)
            else:result=kf.step(dt[i],z,R if z is not None else None)
            out.append(result['state'])
        outputs[method]=np.array(out)
    window=np.arange(first,first+10);all_indices=np.arange(n)
    metrics={m:{'return_window_position_rmse':rmse(o,truth,window),'full_position_rmse':rmse(o,truth,all_indices),
                'first_return_position_error':float(np.linalg.norm(o[first,:2]-truth[first,:2])),
                'confirmation_position_error':float(np.linalg.norm(o[confirmation,:2]-truth[confirmation,:2]))} for m,o in outputs.items()}
    d=metrics['deferred']['return_window_position_rmse']
    return {'seed':seed,'scenario':scenario['name'],'metrics':metrics,'deferred_minus_immediate':d-metrics['immediate']['return_window_position_rmse'],
            'deferred_minus_gated':d-metrics['gated']['return_window_position_rmse'],'gate_rejected_indices':reject_indices,
            'accepted_first':decision['accepted_first'],'confirmation_nll_reject_accept':decision['confirmation_nll_reject_accept'],
            'confirmation_delay':float(dt[confirmation]),'observed':sum(z is not None for z in observations),'missing':sum(z is None for z in observations)}

def run(spec):
    rows=[trajectory(spec,seed,s) for s in spec['scenarios'] for seed in spec['evaluation_seeds']];summary=[]
    for scenario in spec['scenarios']:
        group=[r for r in rows if r['scenario']==scenario['name']];entry={'scenario':scenario['name'],'trajectories':len(group)}
        entry['mean_return_window_rmse']={m:float(np.mean([r['metrics'][m]['return_window_position_rmse'] for r in group])) for m in ('immediate','gated','deferred')}
        for field in ('deferred_minus_immediate','deferred_minus_gated'):
            values=[r[field] for r in group];entry[field]={'mean':float(np.mean(values)),'lower':sum(v<0 for v in values),'equal':sum(v==0 for v in values),'higher':sum(v>0 for v in values)}
        summary.append(entry)
    return {'protocol_id':spec['id'],'scope':spec['scope'],'raw':rows,'summary':summary}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--published-freeze-reference',required=True)
    a=parser.parse_args();protocol=HERE/'protocol.json';r=run(json.loads(protocol.read_text()));r['published_freeze_reference']=a.published_freeze_reference
    r['run_hashes']={str(p.relative_to(HERE.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (protocol,HERE/'compare.py',HERE.parent/'deferred.py',HERE.parent.parent/'p08-tracking'/'kalman.py')}
    pathlib.Path(a.output).write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
