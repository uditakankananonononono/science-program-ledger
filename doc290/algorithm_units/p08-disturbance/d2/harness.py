"""D2 instrumented exact synthetic scalar plant; truth diagnostics parent-only."""
from fractions import Fraction as F
import multiprocessing as mp

class EstimatorPolicy:
    def __init__(self,predict=False,sign=False):
        self.estimate=F(0);self.predict=predict;self.sign=sign
    def action(self,observation,target,dt,bound):
        if observation is not None:self.estimate=observation
        used=self.estimate;error=target-used
        u=(bound if error>0 else -bound if error<0 else F(0)) if self.sign else max(-bound,min(bound,error))
        self.estimate=used+dt*u if self.predict else used
        return (used,u)
class HoldP(EstimatorPolicy):
    def __init__(self):super().__init__()
class PredictP(EstimatorPolicy):
    def __init__(self):super().__init__(predict=True)
class HoldSign(EstimatorPolicy):
    def __init__(self):super().__init__(sign=True)
class PredictSign(EstimatorPolicy):
    def __init__(self):super().__init__(predict=True,sign=True)

def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):raise ValueError('int/Fraction only')
    return F(x)

def worker(connection,factory):
    try:
        policy=factory();connection.send(('ready',None))
        while True:
            args=connection.recv()
            if args is None:break
            try:connection.send(('action',policy.action(*args)))
            except BaseException as e:connection.send(('exception',type(e).__name__))
    except BaseException as e:
        try:connection.send(('exception',type(e).__name__))
        except (OSError,EOFError):pass
    finally:connection.close()

def run(factory,case,initial=F(0),target=F(1),dt=F(1,10),bound=F(1),lower=F(-1,2),upper=F(3,2),tolerance=F(1,10)):
    # Linux fork is required. Policies are trusted code, process separation is a
    # causality/timeout mechanism, NOT sandbox security against malicious code.
    initial,target,dt,bound,lower,upper,tolerance=map(rational,(initial,target,dt,bound,lower,upper,tolerance))
    if dt<=0 or bound<=0 or tolerance<0 or not lower<=initial<=upper:raise ValueError('plant bounds')
    if set(case)!= {'gain','drift','observed','immobilized'}:raise ValueError('case keys')
    gain=list(map(rational,case['gain']));drift=list(map(rational,case['drift']))
    observed=list(case['observed']);immobilized=list(case['immobilized']);n=len(gain)
    if not n or any(len(a)!=n for a in (drift,observed,immobilized)) or any(g<0 for g in gain):raise ValueError('sequence shape/gain')
    if any(type(v) is not bool for a in (observed,immobilized) for v in a):raise ValueError('flags')
    context=mp.get_context('fork');parent,child=context.Pipe();proc=context.Process(target=worker,args=(child,factory))
    proc.start();child.close();x=initial;states=[x];records=[];effort=F(0);outcome=None;error=None;errors=[];drop_errors=[]
    def receive():
        # Fixed one-second wall budget for reset and each action. Timeout kills
        # process even if policy catches exceptions or spins forever.
        if not parent.poll(1.0):return ('exception','PolicyTimeout')
        try:return parent.recv()
        except (EOFError,OSError):return ('exception','PolicyProcessExit')
    try:
        kind,value=receive()
        if kind!='ready':outcome='controller_exception';error=value
        for k in range(n):
            if outcome is not None:break
            z=x if observed[k] else None
            try:parent.send((z,target,dt,bound))
            except (BrokenPipeError,EOFError,OSError):outcome='controller_exception';error='PolicyProcessExit';break
            kind,value=receive()
            if kind!='action':outcome='controller_exception';error=value;records.append({'step':k,'observation':z,'action':None,'state_before':x,'state_after':None});break
            if not isinstance(value,tuple) or len(value)!=2:
                outcome='invalid_action';error='ReturnShape';records.append({'step':k,'observation':z,'estimate':None,'action':None,'state_before':x,'state_after':None});break
            try:estimate=rational(value[0])
            except ValueError:
                outcome='invalid_action';error='UnsupportedEstimate';records.append({'step':k,'observation':z,'estimate':None,'action':None,'state_before':x,'state_after':None});break
            est_error=estimate-x;errors.append(est_error)
            if z is None:drop_errors.append(est_error)
            diag={'estimate':estimate,'estimation_error':est_error,'absolute_estimation_error':abs(est_error),'squared_estimation_error':est_error**2}
            try:u=rational(value[1])
            except ValueError:
                outcome='invalid_action';error='UnsupportedAction';records.append({'step':k,'observation':z,'action':None,'state_before':x,'state_after':None,**diag});break
            if abs(u)>bound:
                outcome='invalid_action';error='ActionBound';records.append({'step':k,'observation':z,'action':u,'state_before':x,'state_after':None,**diag});break
            before=x
            if not immobilized[k]:x+=dt*(gain[k]*u+drift[k])
            effort+=dt*abs(u);states.append(x)
            records.append({'step':k,'observation':z,'action':u,'state_before':before,'state_after':x,**diag})
            if not lower<=x<=upper:outcome='boundary_exit'
        if outcome is None:outcome='success' if abs(x-target)<=tolerance else 'terminal_miss'
    finally:
        if proc.is_alive():proc.kill()
        proc.join();parent.close()
    for record in records:
        for key in ('estimate','estimation_error','absolute_estimation_error','squared_estimation_error'):
            record.setdefault(key,None)
    return {'outcome':outcome,'error_identifier':error,'records':records,'states':states,'completed_steps':len(states)-1,
            'final_error':abs(x-target),'control_effort':effort,'missing_observation_count':sum(r['observation'] is None for r in records),'valid_estimate_count':len(errors),'estimation_mae':sum(map(abs,errors))/len(errors) if errors else None,'estimation_mse':sum(e*e for e in errors)/len(errors) if errors else None,'valid_dropout_estimate_count':len(drop_errors),'dropout_mae':sum(map(abs,drop_errors))/len(drop_errors) if drop_errors else None,'dropout_mse':sum(e*e for e in drop_errors)/len(drop_errors) if drop_errors else None,'max_boundary_overshoot':max(max(F(0),lower-s,s-upper) for s in states)}
