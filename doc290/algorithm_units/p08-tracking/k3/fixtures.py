import copy

def cases():
    def diag(v):return [[v if i==j else 0 for j in range(4)] for i in range(4)]
    def base(name):return {'name':name,'truth':[[0]*4],'estimated':[[3,4,0,0]],'covariances':[diag(1)],'available':[True],'inject':None,'expected':'REFUSE'}
    def oracle(total,scored,excluded,p2,v2,nees,mean):return {'total':total,'scored':scored,'excluded':excluded,'position_squared':p2,'velocity_squared':v2,'nees':nees,'mean':mean}
    out=[]
    c=base('V1');c.update(expected='VALID',oracle=oracle(1,1,0,25,0,[25],25));out.append(c)
    c=base('V2');c.update(truth=[[0]*4,[0]*4],estimated=[[3,4,0,0],[0,0,0,5]],covariances=[diag(1),diag(2)],available=[True,True],expected='VALID',oracle=oracle(2,2,0,'25/2','25/2',[25,'25/2'],'75/4'));out.append(c)
    c=base('V3');c.update(truth=[[0]*4,[{'nonfinite':'NaN'}]*4],estimated=[[3,4,0,0],[1,2,3,4]],covariances=[diag(1),diag(1)],available=[True,False],expected='VALID',oracle=oracle(2,1,1,25,0,[25],25));out.append(c)
    c=base('V4');c.update(truth=[[{'nonfinite':'NaN'}]*4],available=[False],expected='VALID',oracle=oracle(1,0,1,None,None,[],None));out.append(c)
    c=base('R1');c['available']=[1];out.append(c)
    c=base('R2');c['truth'][0][0]={'nonfinite':'NaN'};out.append(c)
    c=copy.deepcopy(out[2]);c.update(name='R3',expected='REFUSE');c.pop('oracle');c['covariances'][1]=diag(0);out.append(c)
    c=base('R4');c['covariances']=[diag(0)];out.append(c)
    c=base('R5');c['estimated']=[['1e200',0,0,0]];out.append(c)
    c=base('R6');c['truth']=[['-1e308',0,0,0]];c['estimated']=[['1e308',0,0,0]];out.append(c)
    for name,kind in (('S1','raise'),('S2','nan')):
        c=base(name);c['inject']=kind;out.append(c)
    return out
