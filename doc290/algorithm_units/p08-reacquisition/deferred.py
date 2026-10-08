"""Restricted two-branch deferred reacquisition baseline, not new MHT."""
import pathlib,sys
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/'p08-tracking'))
from kalman import ConstantVelocity,matrix

def resolve(state,covariance,q,first_dt,first_measurement,R,confirmation_dt,confirmation_measurement,confirmation_R):
    """Reject or accept first observation using one later confirmation observation.

    First-time output is prediction-only. On confirmation choose smaller Gaussian
    predictive negative log density, then update selected branch. Tie rejects.
    First-measurement likelihood/prior clutter probability intentionally NOT used:
    this heuristic score is not a posterior association probability or full MHT.
    Exactly two branches and one-observation latency. No caller state mutated.
    Missing confirmation unsupported; caller retains prediction until it exists.
    """
    reject=ConstantVelocity(state,covariance,q);accept=ConstantVelocity(state,covariance,q)
    provisional=reject.step(first_dt)
    accept.step(first_dt,first_measurement,R)
    z=np.asarray(confirmation_measurement,dtype=float)
    if z.shape!=(2,) or not np.isfinite(z).all():raise ValueError('confirmation measurement must be finite 2-vector')
    noise=matrix(confirmation_R,(2,2),'confirmation R',True)
    scores=[];outputs=[]
    for branch in (reject,accept):
        pred=ConstantVelocity(branch.state,branch.covariance,q).step(confirmation_dt)
        innovation=z-pred['state'][:2];S=pred['covariance'][:2,:2]+noise
        sign,logdet=np.linalg.slogdet(S)
        if sign<=0:raise ValueError('confirmation innovation covariance invalid')
        with np.errstate(over='raise',invalid='raise'):
            score=float(.5*(logdet+innovation@np.linalg.solve(S,innovation)+2*np.log(2*np.pi)))
        if not np.isfinite(score):raise ValueError('confirmation score overflow')
        scores.append(score);outputs.append(branch.step(confirmation_dt,z,noise))
    choice=int(scores[1]<scores[0])
    return {'provisional':provisional,'confirmed':outputs[choice],'accepted_first':bool(choice),
            'confirmation_nll_reject_accept':scores,'latency_observations':1,
            'scope':'heuristic bounded hypothesis baseline, not calibrated posterior or causal first-time revision'}
