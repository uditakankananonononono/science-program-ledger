import copy

def cases():
    I4=[[1 if i==j else 0 for j in range(4)] for i in range(4)];I2=[[1,0],[0,1]]
    def base(name):return {'name':name,'state':[0,0,0,0],'P':copy.deepcopy(I4),'q':0,'dt':1,'measurement':None,'R':None,'inject':None,'expected':'REFUSE'}
    out=[]
    c=base('V1');c.update(state=[1,2,3,4],dt='0.5',expected='VALID',oracle={'state':['5/2',4,3,4],'P':[['5/4',0,'1/2',0],[0,'5/4',0,'1/2'],['1/2',0,1,0],[0,'1/2',0,1]],'innovation':None,'nis':None});out.append(c)
    c=base('V2');c.update(measurement=[3,-3],R=I2,expected='VALID',oracle={'state':[2,-2,1,-1],'P':[['2/3',0,'1/3',0],[0,'2/3',0,'1/3'],['1/3',0,'5/6',0],[0,'1/3',0,'5/6']],'innovation':[3,-3],'nis':6});out.append(c)
    c=base('V3');c.update(P=[[0]*4 for _ in range(4)],q=3,expected='VALID',oracle={'state':[0]*4,'P':[[1,0,'3/2',0],[0,1,0,'3/2'],['3/2',0,3,0],[0,'3/2',0,3]],'innovation':None,'nis':None});out.append(c)
    c=base('E1');c['dt']='1e308';out.append(c)
    c=base('E2');c.update(state=['1e308',0,'1e308',0],dt=2);out.append(c)
    c=base('E3');c.update(q='1e308',dt=2);out.append(c)
    c=base('E4');c.update(P=[['1e308' if i==j else 0 for j in range(4)] for i in range(4)],dt=2);out.append(c)
    c=base('E5');c.update(measurement=['1e200','-1e200'],R=I2);out.append(c)
    c=base('E6');c.update(P=[['5e307' if i==j else 0 for j in range(4)] for i in range(4)],measurement=[1,1],R=[['1e308',0],[0,'1e308']]);out.append(c)
    c=base('I1');c['dt']=0;out.append(c)
    c=base('I2');c.update(measurement=[1],R=I2);out.append(c)
    c=base('I3');c['R']=I2;out.append(c)
    for name,inject in (('S1','raise'),('S2','nan'),('S3','inf')):
        c=base(name);c.update(measurement=[1,1],R=I2,inject=inject);out.append(c)
    return out
