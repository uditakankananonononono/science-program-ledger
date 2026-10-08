import copy

def cases_base():
    def m(lo,hi):return {'x':[0],'target':[0],'dt':[1,1],'B':[[1]],'lower':lo,'upper':hi,'limit':[1],'slew':[2],'previous':[0]}
    C1={'name':'C1','model':m([[0],[1],[0]],[[0],[1],[0]]),'witness':{'kind':'primal','controls':[1,-1]},'expected':'FEASIBLE'}
    C2={'name':'C2','model':m([[0],[2],[0]],[[0],[2],[0]]),'witness':{'kind':'farkas','multipliers':[1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]},'expected':'INFEASIBLE'}
    C3={'name':'C3','model':m([[1],[-1],[0]],[[1],[1],[0]]),'witness':{'kind':'farkas','multipliers':[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]},'expected':'INFEASIBLE'}
    C4={'name':'C4','model':{'x':[1,-1],'target':[4,1],'dt':['1/2','3/2'],'B':[[1,-2],[3,1]],'lower':[[1,-1],['7/4','-1/2'],[4,1]],'upper':[[1,-1],['7/4','-1/2'],[4,1]],'limit':[2,2],'slew':[1,2],'previous':['1/2','-1/2']},'witness':{'kind':'primal','controls':['1/2','-1/2','1/2','-1/2']},'expected':'FEASIBLE'}
    return [C1,C2,C3,C4]

def cases():
    out=[]
    for base in cases_base():
        out.append(copy.deepcopy(base));primal=base['witness']['kind']=='primal'
        for name in (('outbound','node','shape','bool') if primal else ('negative','zeros','station','shape')):
            c=copy.deepcopy(base);c['name']+=':'+name;c['expected']='UNAVAILABLE' if name=='zeros' else 'INVALID';v=c['witness']['controls' if primal else 'multipliers']
            if name=='outbound':v[0]=10
            if name=='node':v[0]=0
            if name=='shape':v.pop()
            if name=='bool':v[0]=True
            if name=='negative':v[0]=-1
            if name=='zeros':c['witness']['multipliers']=[0]*len(v)
            if name=='station':v[0]+=1
            out.append(c)
    for name in ('missing','floatdt','nodeshape','interval','extrakey','badkind','zerotime','signedzero'):
        c=copy.deepcopy(cases_base()[1]);c['name']='control:'+name;c['expected']='UNAVAILABLE' if name=='missing' else 'INVALID'
        if name=='missing':c['witness']=None
        if name=='floatdt':c['model']['dt'][0]=1.0
        if name=='nodeshape':c['model']['lower'].pop()
        if name=='interval':c['model']['lower'][0]=[2]
        if name=='extrakey':c['witness']['extra']=0
        if name=='badkind':c['witness']['kind']='other'
        if name=='zerotime':c['model']['dt'][0]=0
        if name=='signedzero':c['witness']['multipliers'][0]='-0/1'
        out.append(c)
    return out
