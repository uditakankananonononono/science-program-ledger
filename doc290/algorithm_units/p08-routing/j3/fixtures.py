import copy
def e(t,ss,x):return {'target':t,'time':1,'exposure':x,'scenario_times':ss}
def r(path,idx,ss,x):return {'path':path,'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],idx)],'scenario_totals':ss,'worst_time':max(ss),'exposure':x}
def bases():
    A={'graph':{'a':[e('g',[1,1],2),e('g',[4,4],0)],'g':[]},'start':'a','goal':'g','budget':2,'route':r(['a','g'],[0],[1,1],2),'weights':['1/2','1/2'],'multiplier':1,'potential':[0,3]}
    B={'graph':{'a':[e('b',[1,5],1)],'b':[e('g',[5,1],1)],'g':[]},'start':'a','goal':'g','budget':2,'route':r(['a','b','g'],[0,0],[6,6],2),'weights':['1/2','1/2'],'multiplier':'1/2','potential':[0,'7/2',7]}
    C={'graph':{'a':[e('g',[2,2],1),e('g',[5,5],0)],'g':[]},'start':'a','goal':'g','budget':3,'route':r(['a','g'],[0],[2,2],1),'weights':[1,0],'multiplier':0,'potential':[0,2]}
    D={'graph':{'a':[e('g',[1,1],2),e('g',[3,3],0)],'g':[]},'start':'a','goal':'g','budget':1,'route':r(['a','g'],[1],[3,3],0),'weights':['1/2','1/2'],'multiplier':1,'potential':[0,3]}
    return [{'name':n,'statement':s,'expected':'UNAVAILABLE' if n=='D' else 'CERTIFIED_JOINT'} for n,s in zip('ABCD',(A,B,C,D))]
def cases():
    out=[]
    for base in bases():
        out.append(copy.deepcopy(base))
        for change in ('exposure','negative','source'):
            c=copy.deepcopy(base);c['name']+=':'+change;c['expected']='INVALID';s=c['statement']
            if change=='exposure':s['route']['exposure']+=1
            if change=='negative':s['multiplier']=-1
            if change=='source':s['potential'][0]=1
            out.append(c)
    for change in ('null','sum','budget','infeasible'):
        c=copy.deepcopy(bases()[0]);c['name']='control:'+change;c['expected']='UNAVAILABLE' if change=='null' else 'INVALID';s=c['statement']
        if change=='null':s['multiplier']=None
        if change=='sum':s['weights']=[1,1]
        if change=='budget':s['budget']=1
        if change=='infeasible':s['potential']=[0,5]
        out.append(c)
    return out
