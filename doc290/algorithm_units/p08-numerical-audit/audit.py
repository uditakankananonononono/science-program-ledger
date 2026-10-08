"""Non-scoring transactional numerical failure audit. No evaluation seeds."""
import sys,pathlib,json,hashlib
import numpy as np
TRACKING=pathlib.Path(__file__).resolve().parent.parent/'p08-tracking'
sys.path.insert(0,str(TRACKING))
from kalman import ConstantVelocity

CASES=(
    ('finite_dt_python_power_overflow',1e200,None,None,OverflowError),
    ('finite_measurement_innovation_square_overflow',.1,np.array([1e200,1e200]),np.eye(2),FloatingPointError),
    ('nonfinite_dt_rejected',float('inf'),None,None,ValueError),
    ('singular_R_rejected',.1,np.zeros(2),np.zeros((2,2)),ValueError),
)

def run():
    records=[]
    for name,dt,z,R,expected in CASES:
        kf=ConstantVelocity([0,0,1,0],np.eye(4),.25)
        state=kf.state.copy();P=kf.covariance.copy()
        try:kf.step(dt,z,R)
        except Exception as e:
            unchanged=bool(np.array_equal(state,kf.state) and np.array_equal(P,kf.covariance))
            if type(e) is not expected or not unchanged:
                raise AssertionError((name,type(e).__name__,unchanged)) from e
            records.append({'case':name,'exception':type(e).__name__,'state_and_covariance_unchanged':unchanged})
        else:raise AssertionError(name+' unexpectedly accepted')
    return {'scope':'non-scoring failure-path software audit, not domain-calibrated tolerances',
            'kalman_sha256':hashlib.sha256((TRACKING/'kalman.py').read_bytes()).hexdigest(),
            'numpy_version':np.__version__,'cases':records,
            'limitations':['Exception classes are heterogeneous and intentionally recorded, not normalized.',
                           'No near-singular condition threshold or physical noise calibration is established.',
                           'Four fixtures cannot establish safety for every finite input.']}

if __name__=='__main__':print(json.dumps(run(),indent=2,allow_nan=False))
