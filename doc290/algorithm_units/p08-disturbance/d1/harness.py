"""Exact synthetic scalar plant; policy process sees only declared observations."""
from fractions import Fraction as F
import multiprocessing as mp

class Proportional:
    def __init__(self):self.latest=F(0)
    def action(self,observation,target,dt,bound):
        if observation is not None:self.latest=observation
        return max(-bound,min(bound,target-self.latest))
class Sign(Proportional):
    def action(self,observation,target,dt,bound):
        if observation is not None:self.latest=observation
        return bound if target>self.latest else -bound if target<self.latest else F(0)

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
    proc.start();child.close();x=initial;states=[x];records=[];effort=F(0);outcome=None;error=None
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
            try:u=rational(value)
            except ValueError:outcome='invalid_action';error='UnsupportedAction';records.append({'step':k,'observation':z,'action':None,'state_before':x,'state_after':None});break
            if abs(u)>bound:outcome='invalid_action';error='ActionBound';records.append({'step':k,'observation':z,'action':u,'state_before':x,'state_after':None});break
            before=x
            if not immobilized[k]:x+=dt*(gain[k]*u+drift[k])
            effort+=dt*abs(u);states.append(x)
            records.append({'step':k,'observation':z,'action':u,'state_before':before,'state_after':x})
            if not lower<=x<=upper:outcome='boundary_exit'
        if outcome is None:outcome='success' if abs(x-target)<=tolerance else 'terminal_miss'
    finally:
        if proc.is_alive():proc.kill()
        proc.join();parent.close()
    return {'outcome':outcome,'error_identifier':error,'records':records,'states':states,'completed_steps':len(states)-1,
            'final_error':abs(x-target),'control_effort':effort,'max_boundary_overshoot':max(max(F(0),lower-s,s-upper) for s in states)}
