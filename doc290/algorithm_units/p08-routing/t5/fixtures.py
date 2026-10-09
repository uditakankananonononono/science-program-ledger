import copy

def e(t,x):return {'target':t,'time':1,'exposure':x,'scenario_times':[1,1]}
def bases():
    A={'graph':{'a':[e('b',1)],'b':[e('g',1)],'g':[]},'start':'a','goal':'g','budget':10,'forbidden':[[['a',0],['b',0]]],'penalties':[],'distances':[None,None,0,0]}
    B=copy.deepcopy(A);B.update(budget=1,forbidden=[],distances=[2,1,0,0])
    C=copy.deepcopy(B);C.update(budget=2,penalties=[{'incoming':['a',0],'outgoing':['b',0],'delay':7}])
    D={'graph':{'a':[e('b',3)],'b':[e('a',3)]},'start':'a','goal':'a','budget':0,'forbidden':[],'penalties':[],'distances':[0,3,0,0]}
    return [{'name':n,'statement':s,'expected':{'A':'CERTIFIED_NO_TURN_PATH','B':'CERTIFIED_BUDGET_INFEASIBLE','C':'UNAVAILABLE','D':'UNAVAILABLE'}[n]} for n,s in zip('ABCD',(A,B,C,D))]
def cases():
    out=[]
    for b in bases():
        out.append(copy.deepcopy(b))
        for mutation in ('sink','source','budget'):
            c=copy.deepcopy(b);c['name']+=':'+mutation;c['expected']='INVALID';s=c['statement']
            if mutation=='sink':s['distances'][-1]=1
            if mutation=='source':s['distances'][0]=0 if s['distances'][0] is None else s['distances'][0]+1
            if mutation=='budget':s['budget']=True
            out.append(c)
    for mutation in ('null','drop','bool','rule'):
        c=copy.deepcopy(bases()[0 if mutation in ('null','drop') else 1 if mutation=='bool' else 2]);c['name']='control:'+mutation;c['expected']='UNAVAILABLE' if mutation=='null' else 'INVALID';s=c['statement']
        if mutation=='null':s['distances']=None
        if mutation=='drop':s['distances'].pop(2)
        if mutation=='bool':s['distances'][0]=True
        if mutation=='rule':s['forbidden']=[[['a',0],['a',0]]]
        out.append(c)
    return out
