import importlib.util,copy
from pathlib import Path
spec=importlib.util.spec_from_file_location('c1fixtures',Path(__file__).resolve().parent.parent/'c1'/'fixtures.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def protocol():
    out=[]
    bases=old.bases()
    for name,base,bmax in (('A',bases[0],6),('B',bases[2],3),('C',bases[3],4)):
        s=copy.deepcopy(base['statement']);s.pop('route')
        for start in sorted(s['original']):
            for goal in sorted(s['original']):
                for budget in range(bmax+1):
                    c=copy.deepcopy(s);c.update(start=start,goal=goal,budget=budget);out.append({'name':f'{name}:{start}:{goal}:{budget}','statement':c,'expected':'SPLIT_REPRESENTATION'})
    s={'original':{'a':[]},'compressed':{'a':[]},'witnesses':{'a':[]},'start':'a','goal':'a','budget':0,'forbidden':[],'penalties':[]};out.append({'name':'D:a:a:0','statement':s,'expected':'SPLIT_REPRESENTATION'})
    for change in ('cost','backtrack','coverage','absent','turn','float'):
        s=copy.deepcopy(bases[0]['statement']);s.pop('route')
        if change=='cost':s['compressed']['a'][0]['time']+=1
        if change=='backtrack':
            s['compressed']['a'][0]['target']='a';s['compressed']['c'][0]['target']='c';s['witnesses']={'a':[['a','b','a']],'c':[['c','b','c']]}
        if change=='coverage':s['witnesses']['c']=[]
        if change=='absent':s['start']='missing'
        if change=='turn':s['penalties']=[1]
        if change=='float':s['original']['a'][0]['time']=2.0
        out.append({'name':'refusal:'+change,'statement':s,'expected':'INVALID'})
    return out
