import copy,importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('i4_original_i3_fixtures',Path(__file__).resolve().parent.parent/'i3'/'fixtures.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
e,r=f.e,f.r
def bases():
    out=[]
    for b in f.bases():
        s={k:v for k,v in b['statement'].items() if k not in ('weights','multiplier','potential')};out.append({'name':b['name'],'statement':s,'expected':b['expected']})
    def add(name,G,start,goal,budget,route,status):out.append({'name':name,'statement':{'graph':G,'start':start,'goal':goal,'budget':budget,'route':route,'forbidden':[],'penalties':[]},'expected':status})
    add('E',{'a':[e('g',[2,3],0)],'g':[e('a',[1,1],0)]},'a','a',0,r(['a'],[],[0,0],0,0),'CERTIFIED_INTEGRATED')
    add('F',{'a':[e('g',[0,0],2),e('g',[3,3],0)],'g':[]},'a','g',0,r(['a','g'],[1],[3,3],0,0),'CERTIFIED_INTEGRATED')
    add('G',{'a':[e('g',[0,0],2),e('g',[7,7],1),e('g',[11,11],0)],'g':[]},'a','g',1,r(['a','g'],[1],[7,7],1,0),'UNAVAILABLE')
    add('H',{'a':[e('g',[2,2],0)],'g':[],'x':[e('y',[1,1],0)],'y':[e('x',[0,0],0)]},'a','g',0,r(['a','g'],[0],[2,2],0,0),'CERTIFIED_INTEGRATED')
    return out
def cases():
    out=[]
    for b in bases():
        out.append(copy.deepcopy(b));c=copy.deepcopy(b);c['name']+=':worst';c['statement']['route']['worst_time']+=1;c['expected']='INVALID';out.append(c)
    for name in ('null','boolindex','dimension','negative'):
        c=copy.deepcopy(bases()[0]);c['name']='control:'+name;c['expected']='UNAVAILABLE' if name=='null' else 'INVALID';s=c['statement']
        if name=='null':s['route']=None
        if name=='boolindex':s['route']['edges'][0]['edge_index']=True
        if name=='dimension':
            for es in s['graph'].values():
                for e in es:e['scenario_times']=[]
        if name=='negative':s['graph']['a'][0]['exposure']=-1
        out.append(c)
    return out
