import copy

def e(t,exposure,ss):return {'target':t,'time':1,'exposure':exposure,'scenario_times':ss}
def r(path,indices,exp,ss,turn):return {'path':path,'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],indices)],'exposure':exp,'scenario_totals':ss,'worst_time':max(ss),'turn_penalty':turn}
def bases():
    A={'graph':{'a':[e('b',1,[2,3]),e('b',2,[5,1])],'b':[e('c',1,[1,4])],'c':[]},'start':'a','goal':'c','budget':3,'forbidden':[],'penalties':[{'incoming':['a',1],'outgoing':['b',0],'delay':2}],'route':r(['a','b','c'],[1,0],3,[8,7],2)}
    B={'graph':{'a':[e('b',1,[1])],'b':[e('c',1,[1]),e('d',1,[1])],'c':[e('b',1,[1])],'d':[]},'start':'a','goal':'d','budget':4,'forbidden':[[['a',0],['b',1]]],'penalties':[{'incoming':['c',0],'outgoing':['b',1],'delay':3}],'route':r(['a','b','c','b','d'],[0,0,0,1],4,[7],3)}
    C={'graph':{'a':[e('a',1,[1,2])]},'start':'a','goal':'a','budget':2,'forbidden':[],'penalties':[{'incoming':['a',0],'outgoing':['a',0],'delay':4}],'route':r(['a','a','a'],[0,0],2,[6,8],4)}
    D=copy.deepcopy(A);D.update(goal='a',budget=0,route=r(['a'],[],0,[0,0],0))
    return [{'name':name,'statement':s,'expected':'FEASIBLE_WITNESS'} for name,s in zip('ABCD',(A,B,C,D))]
def cases():
    out=[]
    for base in bases():
        out.append(copy.deepcopy(base))
        for change in ('negative','turntotal','scenario'):
            c=copy.deepcopy(base);c['name']+=':'+change;c['expected']='INVALID';s=c['statement']
            if change=='negative':
                if base['name']=='D':s['route']=copy.deepcopy(bases()[0]['statement']['route'])
                s['route']['edges'][0]['edge_index']=-1
            if change=='turntotal':s['route']['turn_penalty']+=1
            if change=='scenario':s['route']['scenario_totals'][0]+=1
            out.append(c)
    for change in ('forbidden','budget','null','badrule'):
        c=copy.deepcopy(bases()[0]);c['name']='control:'+change;c['expected']='UNAVAILABLE' if change=='null' else 'INVALID';s=c['statement']
        if change=='forbidden':s['forbidden']=[[['a',1],['b',0]]]
        if change=='budget':s['budget']=2
        if change=='null':s['route']=None
        if change=='badrule':s['route']=None;s['penalties'][0]['incoming']=['a',-1]
        out.append(c)
    return out
