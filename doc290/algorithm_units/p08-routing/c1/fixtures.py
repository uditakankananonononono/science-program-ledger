import copy

def e(t,time=1,exposure=1,ss=None):return {'target':t,'time':time,'exposure':exposure,'scenario_times':[1] if ss is None else ss}

def route(a,b,i,time,exp,ss):return {'path':[a,b],'edges':[{'source':a,'edge_index':i,'target':b}],'time':time,'exposure':exp,'scenario_totals':ss,'worst_time':max(ss)}

def bases():
    G={'a':[e('b',2,1,[3,4])],'b':[e('a',7,4,[5,6]),e('c',1,0,[2,1])],'c':[e('b',9,2,[7,8])]}
    C={'a':[e('c',3,1,[5,5])],'c':[e('a',16,6,[12,14])]};W={'a':[['a','b','c']],'c':[['c','b','a']]}
    def s(g,c,w,start,goal,budget,r):return {'original':g,'compressed':c,'witnesses':w,'start':start,'goal':goal,'budget':budget,'forbidden':[],'penalties':[],'route':r}
    A=s(G,C,W,'a','c',1,route('a','c',0,3,1,[5,5]));B=copy.deepcopy(A);B.update(start='c',goal='a',budget=6,route=route('c','a',0,16,6,[12,14]))
    gc={'a':[e('b'),e('c')],'b':[e('a'),e('c')],'c':[e('b'),e('a')]}
    cc={'a':[e('a',3,3,[3]),e('a',3,3,[3])]};wc={'a':[['a','b','c','a'],['a','c','b','a']]};Cyc=s(gc,cc,wc,'a','a',3,route('a','a',0,3,3,[3]))
    gt={'a':[e(v,ss=[1,2]) for v in ('b','c','d')],'z':[e(v,ss=[1,2]) for v in ('b','c','d')]}
    for v in ('b','c','d'):gt[v]=[e('a',ss=[1,2]),e('z',ss=[1,2])]
    ct={'a':[e('z',2,2,[2,4]) for _ in range(3)],'z':[e('a',2,2,[2,4]) for _ in range(3)]};wt={'a':[['a',v,'z'] for v in ('b','c','d')],'z':[['z',v,'a'] for v in ('b','c','d')]}
    D=s(gt,ct,wt,'a','z',2,route('a','z',1,2,2,[2,4]))
    return [{'name':name,'statement':v,'expected':'FEASIBLE_WITNESS'} for name,v in zip(('A','B','C','D'),(A,B,Cyc,D))]

def cases():
    out=[]
    for base in bases():
        out.append(copy.deepcopy(base))
        for mutation in ('negative_index','totals','unknown_interior'):
            c=copy.deepcopy(base);c['name']+=':'+mutation;c['expected']='INVALID';s=c['statement']
            if mutation=='negative_index':s['route']['edges'][0]['edge_index']=-1
            if mutation=='totals':s['route']['exposure']+=1
            if mutation=='unknown_interior':s['witnesses'][next(iter(s['witnesses']))][0][1]='unknown'
            out.append(c)
    for mutation in ('interior','turn','float','null'):
        c=copy.deepcopy(bases()[0]);c['name']='control:'+mutation;c['expected']='UNAVAILABLE' if mutation=='null' else 'INVALID';s=c['statement']
        if mutation=='interior':s['start']='b'
        if mutation=='turn':s['forbidden']=[[['a',0],['b',1]]]
        if mutation=='float':s['original']['a'][0]['time']=2.0
        if mutation=='null':s['route']=None
        out.append(c)
    return out
