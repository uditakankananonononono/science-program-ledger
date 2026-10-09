import copy

def bases():
    specs=[('A',[(1,2),(4,0)],2,0,1,[0,3],'CERTIFIED_OPTIMAL'),('B',[(2,1),(5,0)],3,0,0,[0,2],'CERTIFIED_OPTIMAL'),('C',[(1,2),(3,0)],2,0,'1/2',[0,2],'CERTIFIED_OPTIMAL'),('D',[(1,2),(3,0)],1,1,1,[0,3],'UNAVAILABLE')];out=[]
    for name,costs,budget,i,lam,h,expect in specs:
        G={'a':[{'target':'g','time':t,'exposure':r,'scenario_times':[]} for t,r in costs],'g':[]};t,r=costs[i]
        out.append({'name':name,'statement':{'graph':G,'start':'a','goal':'g','budget':budget,'route':{'path':['a','g'],'edges':[{'source':'a','edge_index':i,'target':'g'}],'time':t,'exposure':r},'multiplier':lam,'potential':h},'expected':expect})
    return out

def cases():
    out=[]
    for base in bases():
        out.append(copy.deepcopy(base))
        for change in ('time','negative','source'):
            c=copy.deepcopy(base);c['name']+=':'+change;c['expected']='INVALID';s=c['statement']
            if change=='time':s['route']['time']+=1
            if change=='negative':s['multiplier']=-1
            if change=='source':s['potential'][0]=1
            out.append(c)
    for change in ('null','float','infeasible','budget'):
        c=copy.deepcopy(bases()[0]);c['name']='control:'+change;c['expected']='UNAVAILABLE' if change=='null' else 'INVALID';s=c['statement']
        if change=='null':s['multiplier']=None
        if change=='float':s['multiplier']=1.0
        if change=='infeasible':s['potential']=[0,5]
        if change=='budget':s['budget']=1
        out.append(c)
    return out
