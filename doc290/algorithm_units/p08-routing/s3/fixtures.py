import copy

def e(t,ss):return {'target':t,'time':1,'exposure':0,'scenario_times':ss}
def r(path,idx,ss):return {'path':path,'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],idx)],'scenario_totals':ss,'worst_time':max(ss)}
def bases():
    A={'graph':{'a':[e('g',[2,2]),e('g',[1,4])],'g':[]},'start':'a','goal':'g','route':r(['a','g'],[0],[2,2]),'weights':['1/2','1/2'],'potential':[0,2]}
    B={'graph':{'a':[e('b',[1,5])],'b':[e('g',[5,1])],'g':[]},'start':'a','goal':'g','route':r(['a','b','g'],[0,0],[6,6]),'weights':['1/2','1/2'],'potential':[0,3,6]}
    C={'graph':{'a':[e('g',[1,3]),e('g',[4,0])],'g':[]},'start':'a','goal':'g','route':r(['a','g'],[0],[1,3]),'weights':[0,1],'potential':[0,0]}
    D={'graph':{'a':[e('g',[0,4]),e('g',[4,0])],'g':[]},'start':'a','goal':'g','route':r(['a','g'],[0],[0,4]),'weights':['1/2','1/2'],'potential':[0,2]}
    return [{'name':n,'statement':s,'expected':'CERTIFIED_MINIMAX' if n in 'AB' else 'UNAVAILABLE'} for n,s in zip('ABCD',(A,B,C,D))]
def cases():
    out=[]
    for base in bases():
        out.append(copy.deepcopy(base))
        for change in ('worst','negative','source'):
            c=copy.deepcopy(base);c['name']+=':'+change;c['expected']='INVALID';s=c['statement']
            if change=='worst':s['route']['worst_time']+=1
            if change=='negative':s['weights'][0]=-1
            if change=='source':s['potential'][0]=1
            out.append(c)
    for change in ('null','sum','proxy','dimension'):
        c=copy.deepcopy(bases()[1]);c['name']='control:'+change;c['expected']='UNAVAILABLE' if change=='null' else 'INVALID';s=c['statement']
        if change=='null':s['weights']=None
        if change=='sum':s['weights']=[1,1]
        if change=='proxy':s['route']['scenario_totals']=[10,10];s['route']['worst_time']=10
        if change=='dimension':s['graph']['a'][0]['scenario_times']=[1];s['route']=None
        out.append(c)
    return out
