import copy
def e(t,ss,x):return {'target':t,'time':1,'exposure':x,'scenario_times':ss}
def r(path,idx,ss,x,turn):return {'path':path,'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],idx)],'scenario_totals':ss,'worst_time':max(ss),'exposure':x,'turn_penalty':turn}
def bases():
    A={'graph':{'a':[e('b',[1,1],1)],'b':[e('g',[1,1],1)],'g':[]},'start':'a','goal':'g','budget':2,'route':r(['a','b','g'],[0,0],[4,4],2,2),'weights':['1/2','1/2'],'multiplier':1,'potential':[0,2,6,6],'forbidden':[],'penalties':[{'incoming':['a',0],'outgoing':['b',0],'delay':2}]}
    B=copy.deepcopy(A);B['graph']['a'][0]['scenario_times']=[1,5];B['graph']['b'][0]['scenario_times']=[5,1];B['penalties'][0]['delay']=1;B.update(route=r(['a','b','g'],[0,0],[7,7],2,1),multiplier='1/2',potential=[0,'7/2',8,8])
    C={'graph':{'a':[e('b',[1,1],0),e('g',[5,5],0)],'b':[e('g',[1,1],0)],'g':[]},'start':'a','goal':'g','budget':0,'route':r(['a','g'],[1],[5,5],0,0),'weights':[1,0],'multiplier':0,'potential':[0,1,5,5,5],'forbidden':[[['a',0],['b',0]]],'penalties':[]}
    D={'graph':{'a':[e('g',[1,1],2),e('g',[3,3],0)],'g':[]},'start':'a','goal':'g','budget':1,'route':r(['a','g'],[1],[3,3],0,0),'weights':['1/2','1/2'],'multiplier':1,'potential':[0,3,3,3],'forbidden':[],'penalties':[]}
    return [{'name':n,'statement':s,'expected':'UNAVAILABLE' if n=='D' else 'CERTIFIED_INTEGRATED'} for n,s in zip('ABCD',(A,B,C,D))]
def cases():
    out=[]
    for base in bases():
        out.append(copy.deepcopy(base))
        for change in ('turn','negative','source'):
            c=copy.deepcopy(base);c['name']+=':'+change;c['expected']='INVALID';s=c['statement']
            if change=='turn':s['route']['turn_penalty']+=1
            if change=='negative':s['multiplier']=-1
            if change=='source':s['potential'][0]=1
            out.append(c)
    for change in ('null','sum','budget','infeasible'):
        c=copy.deepcopy(bases()[0]);c['name']='control:'+change;c['expected']='UNAVAILABLE' if change=='null' else 'INVALID';s=c['statement']
        if change=='null':s['multiplier']=None
        if change=='sum':s['weights']=[1,1]
        if change=='budget':s['budget']=1
        if change=='infeasible':s['potential']=[0,2,7,7]
        out.append(c)
    return out
