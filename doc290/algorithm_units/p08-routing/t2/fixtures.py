import copy

def e(t,time):return {'target':t,'time':time,'exposure':0,'scenario_times':[]}
def r(path,idx,time):return {'path':path,'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],idx)],'time':time,'turn_penalty':0}
def bases():
    A={'graph':{'a':[e('g',2),e('g',5)],'g':[]},'start':'a','goal':'g','forbidden':[],'penalties':[],'route':r(['a','g'],[0],2),'potential':[0,2,2,2]}
    B={'graph':{'a':[e('b',1)],'b':[e('c',1),e('g',1)],'c':[e('b',1)],'g':[]},'start':'a','goal':'g','forbidden':[[['a',0],['b',1]]],'penalties':[],'route':r(['a','b','c','b','g'],[0,0,0,1],4),'potential':[0,1,2,4,3,4]}
    C={'graph':{'a':[e('a',1)]},'start':'a','goal':'a','forbidden':[],'penalties':[],'route':r(['a'],[],0),'potential':[0,0,0]}
    D={'graph':{'a':[e('b',1),e('b',2)],'b':[e('g',1)],'g':[]},'start':'a','goal':'g','forbidden':[],'penalties':[{'incoming':['a',0],'outgoing':['b',0],'delay':5}],'route':r(['a','b','g'],[1,0],3),'potential':[0,1,2,3,3]}
    return [{'name':n,'statement':s,'expected':'CERTIFIED_OPTIMAL'} for n,s in zip('ABCD',(A,B,C,D))]
def cases():
    out=[]
    for base in bases():
        out.append(copy.deepcopy(base))
        for kind in ('time','source','shape'):
            c=copy.deepcopy(base);c['name']+=':'+kind;c['expected']='INVALID';s=c['statement']
            if kind=='time':s['route']['time']+=1
            if kind=='source':s['potential'][0]=1
            if kind=='shape':s['potential'].pop()
            out.append(c)
    for kind in ('null','slack','float','badrule'):
        c=copy.deepcopy(bases()[0]);c['name']='control:'+kind;c['expected']='UNAVAILABLE' if kind in ('null','slack') else 'INVALID';s=c['statement']
        if kind=='null':s['potential']=None
        if kind=='slack':s['potential']=[0]*4
        if kind=='float':s['potential'][-1]=2.0
        if kind=='badrule':s['route']=None;s['forbidden']=[[['a',0],['g',0]]]
        out.append(c)
    return out
