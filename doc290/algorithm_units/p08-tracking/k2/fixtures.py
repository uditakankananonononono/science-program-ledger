import copy

def cases():
    def diag(v):return [[v if i==j else 0 for j in range(4)] for i in range(4)]
    def base(name):return {'name':name,'means':[[0]*4,[2,-2,4,-4]],'covs':[diag(1),diag(1)],'predictions':[[0]*4],'pcs':[diag(2)],'Fs':[diag(1)],'inject':None,'expected':'REFUSE'}
    out=[]
    c=base('V1');c.update(expected='VALID',oracle_means=[[1,-1,2,-2],[2,-2,4,-4]],oracle_covs=[diag('3/4'),diag(1)]);out.append(c)
    c=base('V2');c.update(means=[[1,2,3,4]],covs=[diag(1)],predictions=[],pcs=[],Fs=[],expected='VALID',oracle_means=[[1,2,3,4]],oracle_covs=[diag(1)]);out.append(c)
    c=base('V3');c['means'][1]=[0]*4;c['covs'][1]=diag(2);c.update(expected='VALID',oracle_means=[[0]*4,[0]*4],oracle_covs=[diag(1),diag(2)]);out.append(c)
    c=base('R1');c['pcs']=[diag(0)];out.append(c)
    c=base('R2');c['means'][0][0]={'nonfinite':'NaN'};out.append(c)
    c=base('R3');c['covs'][0]=diag(5);out.append(c)
    c=base('R4');c['means']=[['1e308',0,0,0],['-1e308',0,0,0]];out.append(c)
    c=base('R5');c['covs'][0]=diag('1e308');c['pcs']=[diag(1)];c['Fs']=[diag(2)];out.append(c)
    c=base('R6');c['predictions']=[[0,0,0]];out.append(c)
    for name,kind in (('S1','raise'),('S2','nan'),('S3','inf')):
        c=base(name);c['inject']=kind;out.append(c)
    return out
