import copy

def cases_base():
    def m(maps,lo,hi):return {'x':[0],'dt':[1],'maps':maps,'lower':lo,'upper':hi,'limit':[1],'slew':[2],'previous':[0]}
    J1={'name':'J1','model':m([[[1]],[[2]]],[['1/2'],[1]],[['1/2'],[1]]),'witness':{'kind':'primal','controls':['1/2']},'expected':'FEASIBLE'}
    J2={'name':'J2','model':m([[[1]],[[2]]],[[1],[1]],[[1],[1]]),'witness':{'kind':'farkas','multipliers':[0,0,0,0,0,2,1,0]},'expected':'INFEASIBLE'}
    J3={'name':'J3','model':m([[[1]],[[1]]],[['1/2'],[-1]],[[1],['-1/2']]),'witness':{'kind':'farkas','multipliers':[0,0,0,0,0,1,1,0]},'expected':'INFEASIBLE'}
    J4={'name':'J4','model':{'x':[1,-1],'dt':['1/2','3/2'],'maps':[[[1,-2],[3,1]],[[-1,4],[2,-3]]],'lower':[[4,1],[-4,4]],'upper':[[4,1],[-4,4]],'limit':[2,2],'slew':[1,2],'previous':['1/2','-1/2']},'witness':{'kind':'primal','controls':['1/2','-1/2','1/2','-1/2']},'expected':'FEASIBLE'}
    return [J1,J2,J3,J4]

def cases():
    out=[]
    for base in cases_base():
        out.append(copy.deepcopy(base));primal=base['witness']['kind']=='primal'
        for name in (('outbound','terminal','shape','bool') if primal else ('negative','zeros','station','shape')):
            c=copy.deepcopy(base);c['name']+=':'+name;c['expected']='UNAVAILABLE' if name=='zeros' else 'INVALID';v=c['witness']['controls' if primal else 'multipliers']
            if name=='outbound':v[0]=10
            if name=='terminal':v[0]=0
            if name=='shape':v.pop()
            if name=='bool':v[0]=True
            if name=='negative':v[0]=-1
            if name=='zeros':c['witness']['multipliers']=[0]*len(v)
            if name=='station':v[5]+=1
            out.append(c)
    for name in ('missing','floatdt','interval','mapshape','badkind','extrakey','zerotime','signedzero'):
        c=copy.deepcopy(cases_base()[1]);c['name']='control:'+name;c['expected']='UNAVAILABLE' if name=='missing' else 'INVALID'
        if name=='missing':c['witness']=None
        if name=='floatdt':c['model']['dt']=[1.0]
        if name=='interval':c['model']['lower'][0]=[2]
        if name=='mapshape':c['model']['maps'][0]=[[1,1]]
        if name=='badkind':c['witness']['kind']='other'
        if name=='extrakey':c['witness']['extra']=0
        if name=='zerotime':c['model']['dt']=[0]
        if name=='signedzero':c['witness']['multipliers'][0]='-0/1'
        out.append(c)
    return out
