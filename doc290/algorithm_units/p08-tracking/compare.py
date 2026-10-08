"""P08-03-S1 locked synthetic baseline harness. Run only after freeze publication."""
import argparse,json,hashlib,pathlib
import numpy as np
from kalman import ConstantVelocity
from smoother import smooth
from metrics import evaluate

def model(dt,q):
    F=np.eye(4);F[0,2]=F[1,3]=dt
    Q=np.zeros((4,4))
    for a,b in ((0,2),(1,3)):
        Q[a,a]=q*dt**3/3;Q[a,b]=Q[b,a]=q*dt**2/2;Q[b,b]=q*dt
    return F,Q

def trajectory(spec,seed,regime):
    rng=np.random.default_rng(seed);n=spec['steps']
    prior=np.array(spec['initial_mean'],float);P=np.diag(spec['initial_covariance_diagonal'])
    truth=prior+rng.multivariate_normal(np.zeros(4),P)
    dt=rng.uniform(*spec['dt_uniform'],size=n)
    process=rng.standard_normal((n,4));noise=rng.standard_normal((n,2));drop=rng.random(n)
    kf=ConstantVelocity(prior,P,spec['filter_q']);last=prior[:2].copy()
    truths=[];fm=[];fc=[];pm=[];pc=[];Fs=[];holds=[];observed=0
    for i in range(n):
        F,Q=model(dt[i],spec['true_q']);truth=F@truth+np.linalg.cholesky(Q)@process[i]
        # Records map filtered post-step i-1 to post-step i for smoother.
        if i:
            _,filterQ=model(dt[i],spec['filter_q']);pm.append(F@kf.state);pc.append(F@kf.covariance@F.T+filterQ);Fs.append(F)
        available=drop[i]>=regime['dropout_probability']
        z=truth[:2]+regime['measurement_sigma']*noise[i] if available else None
        if available:last=z.copy();observed+=1
        r=kf.step(dt[i],z,np.eye(2)*regime['measurement_sigma']**2 if available else None)
        truths.append(truth.copy());fm.append(r['state']);fc.append(r['covariance']);holds.append(last.copy())
    sm,sc=smooth(fm,fc,pm,pc,Fs)
    truths=np.array(truths);mask=np.ones(n,dtype=bool)
    causal=evaluate(truths,fm,fc,mask);offline=evaluate(truths,sm,sc,mask)
    hold=float(np.sqrt(np.mean(np.sum((np.array(holds)-truths[:,:2])**2,axis=1))))
    return {'seed':seed,'regime':regime['name'],'observed':observed,'missing':n-observed,'hold_position_rmse':hold,
            'kalman':causal,'offline_rts':offline,'kalman_minus_hold':causal['position_rmse']-hold,
            'offline_rts_minus_kalman':offline['position_rmse']-causal['position_rmse']}

def run(spec):
    rows=[trajectory(spec,s,r) for r in spec['regimes'] for s in spec['evaluation_seeds']]
    summaries=[]
    for regime in spec['regimes']:
        group=[r for r in rows if r['regime']==regime['name']]
        out={'regime':regime['name'],'trajectories':len(group)}
        for field in ('kalman_minus_hold','offline_rts_minus_kalman'):
            vals=[r[field] for r in group]
            out[field]={'mean':float(np.mean(vals)),'lower':sum(v<0 for v in vals),'equal':sum(v==0 for v in vals),'higher':sum(v>0 for v in vals)}
        out['mean_trajectory_position_rmse']={'hold':float(np.mean([r['hold_position_rmse'] for r in group])),
             'kalman':float(np.mean([r['kalman']['position_rmse'] for r in group])),
             'offline_rts':float(np.mean([r['offline_rts']['position_rmse'] for r in group]))}
        summaries.append(out)
    return {'protocol_id':spec['id'],'scope':spec['scope'],'raw':rows,'summary':summaries}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--protocol',default=str(pathlib.Path(__file__).with_name('comparison_protocol.json')))
    parser.add_argument('--output',required=True);parser.add_argument('--published-freeze-reference',required=True)
    args=parser.parse_args();path=pathlib.Path(args.protocol);spec=json.loads(path.read_text());result=run(spec)
    result['protocol_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();result['published_freeze_reference']=args.published_freeze_reference
    result['code_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in pathlib.Path(__file__).parent.glob('*.py')}
    pathlib.Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
