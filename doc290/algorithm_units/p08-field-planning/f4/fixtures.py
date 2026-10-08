import copy

def models():
    def m(x,y,dt,B,cap,rate,prev):return {'x':x,'target':y,'dt':dt,'B':B,'limit':cap,'slew':rate,'previous':prev}
    return [
      {'name':'R1','model':m([0],[1],[1],[[1,1]],[1,1],[2,2],[0,0]),'witness':{'kind':'feasible','integrals':['1/2','1/2']},'expected':'REACHABLE'},
      {'name':'R2','model':m([0,0],[1,-1],[1],[[1],[1]],[1],[2],[0]),'witness':{'kind':'separator','direction':[1,-1]},'expected':'UNREACHABLE'},
      {'name':'R3','model':m([0,0],[1,0],[1],[[1],[2]],[1],[2],[0]),'witness':{'kind':'separator','direction':[2,-1]},'expected':'UNREACHABLE'},
      {'name':'R4','model':m([1],['3/2'],['1/2'],[[1,2]],[2,2],[1,1],['1/2',0]),'witness':{'kind':'feasible','integrals':['1/4','1/8']},'expected':'REACHABLE'}]

def cases():
    from fractions import Fraction as F
    out=[]
    for base in models():
        out.append(copy.deepcopy(base));feas=base['witness']['kind']=='feasible'
        mutations=('outbox','terminal','shape','bool') if feas else ('opposite','zero','shape','float')
        for name in mutations:
            c=copy.deepcopy(base);c['name']+=':'+name;c['expected']='UNAVAILABLE' if name=='opposite' else 'INVALID';w=c['witness'];v=w['integrals' if feas else 'direction']
            if name=='outbox':v[0]=10
            if name=='terminal':v[0]=0
            if name=='shape':v.pop()
            if name=='bool':v[0]=True
            if name=='opposite':w['direction']=[-F(a) for a in v];w['direction']=[int(a) for a in w['direction']]
            if name=='zero':w['direction']=[0]*len(v)
            if name=='float':v[0]=1.0
            out.append(c)
    for name in ('missing','floatdt','negativetime','badB','signedzero','boundary'):
        c=copy.deepcopy(models()[0]);c['name']='control:'+name;c['expected']='UNAVAILABLE' if name in ('missing','boundary') else 'INVALID'
        if name=='missing':c['witness']=None
        if name=='floatdt':c['model']['dt']=[1.0]
        if name=='negativetime':c['model']['dt']=[-1]
        if name=='badB':c['model']['B']=[[1]]
        if name=='signedzero':c['witness']['integrals'][0]='-0/1'
        if name=='boundary':c['model']['target']=[2];c['witness']={'kind':'separator','direction':[1]}
        out.append(c)
    return out
