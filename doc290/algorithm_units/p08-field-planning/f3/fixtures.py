"""Disclosed analytic construction. No evaluation occurs on import."""
import copy

def model(dt,maps,targets,limit,slew):
    return {'x':[0],'dt':dt,'maps':maps,'targets':targets,'limit':[limit],'slew':[slew],'previous':[0]}

def fixture_set():
    # Explicit row indices follow prereg ordering, not queried from verifier.
    specs=[('two-gain',model([1],[[[1]],[[2]]],[[1],[1]],1,2),['2/3','1/3'],9,{5:'2/3',6:'1/3'}),
           ('capped',model([1],[[[1]]],[[1]],'1/2',2),['1/2','1/2'],7,{0:1,5:1}),
           ('zero',model([1],[[[1]]],[[0]],1,2),[0,0],7,{6:1}),
           ('two-step-capped',model([1,1],[[[1]]],[[2]],'1/2',2),['1/2','1/2',1],11,{0:1,2:1,9:1})]
    out=[]
    for name,M,z,n,active in specs:
        lam=[0]*n
        for i,v in active.items():lam[i]=v
        out.append({'name':name,'model':M,'witness':{'z':z,'lambda':lam}})
    return out

def evaluation_cases():
    from fractions import Fraction
    out=[]
    for f in fixture_set():
        out.append(dict(copy.deepcopy(f),expected='VERIFIED'))
        for mutation in ('gap','control','negative','stationarity','shape'):
            g=copy.deepcopy(f);g['name']+=':'+mutation;g['expected']='INVALID';w=g['witness']
            if mutation=='gap':
                v=Fraction(w['z'][-1])+1;w['z'][-1]=f'{v.numerator}/{v.denominator}'
            if mutation=='control':
                v=Fraction(w['z'][0])+2;w['z'][0]=f'{v.numerator}/{v.denominator}'
            if mutation=='negative':w['lambda'][0]=-1
            if mutation=='stationarity':w['lambda']=[0]*len(w['lambda'])
            if mutation=='shape':w['lambda'].pop()
            out.append(g)
    for name in ('float-dt','bool-limit','unreduced','zero-denominator','missing','target-shape'):
        g=copy.deepcopy(fixture_set()[0]);g['name']='malformed:'+name;g['expected']='UNAVAILABLE' if name=='missing' else 'INVALID'
        if name=='float-dt':g['model']['dt']=[1.0]
        if name=='bool-limit':g['model']['limit']=[True]
        if name=='unreduced':g['witness']['z'][0]='2/4'
        if name=='zero-denominator':g['witness']['z'][0]='2/0'
        if name=='missing':g['witness']=None
        if name=='target-shape':g['model']['targets'][0]=[1,1]
        out.append(g)
    return out
