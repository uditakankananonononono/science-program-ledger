import copy,json
from pathlib import Path
MAX=2**53-1
def edge(target,exposure):return {'target':target,'time':1,'exposure':exposure,'scenario_times':[1,1]}
def statement(G,start='a',goal='g',budget=0,forbidden=None,penalties=None,distances=None):return {'graph':G,'start':start,'goal':goal,'budget':budget,'forbidden':forbidden or [],'penalties':penalties or [],'distances':distances}
def controls():
    return [('unreachable',statement({'a':[edge('b',0)],'b':[],'g':[]})),('budget',statement({'a':[edge('g',2)],'g':[]},budget=1)),('identity',statement({'a':[edge('b',3)],'b':[edge('a',3)]},goal='a')),('larger',statement({'a':[edge('g',k) for k in range(1,8)],'g':[]},budget=1)),('zero',statement({'a':[edge('b',0)],'b':[edge('g',0)],'g':[]})),('delay',statement({'a':[edge('b',1)],'b':[edge('g',1)],'g':[]},budget=2,penalties=[{'incoming':['a',0],'outgoing':['b',0],'delay':9}])),('allstate',statement({'a':[edge('g',1)],'g':[edge('u',4)],'u':[edge('g',2)],'z':[edge('g',8)]},budget=1)),('invalid',statement({'a':[edge('g',2)],'g':[]},budget=True))]
def cases():
    original=json.loads((Path(__file__).resolve().parent.parent/'t5/cases.json').read_text());out=[]
    for c in original:out.append(dict(copy.deepcopy(c),expected='INVALID' if c['expected']=='INVALID' else 'COMPLETED' if c['statement']['distances'] is None else 'PRESERVED'))
    for c in original:
        if c['name'] in 'ABCD':
            s=copy.deepcopy(c['statement']);s['distances']=None;out.append({'name':c['name']+':null','statement':s,'expected':'COMPLETED'})
    out += [{'name':'control10:'+name,'statement':s,'expected':'INVALID' if name=='invalid' else 'COMPLETED'} for name,s in controls()];assert len(out)==32;return out

def development():
    missing=statement({'q':[edge('z',2)],'z':[edge('q',0)]},start='q',goal='z',budget=1)
    supplied=copy.deepcopy(missing);supplied['distances']=[2,0,2,0]
    corrupted=copy.deepcopy(supplied);corrupted['distances'][0]=True
    invalid=copy.deepcopy(missing);invalid['budget']=False
    return [{'name':'dev:'+str(k),'statement':s,'expected':e} for k,(s,e) in enumerate([(missing,'COMPLETED'),(supplied,'PRESERVED'),(corrupted,'INVALID'),(invalid,'INVALID')])]
if __name__=='__main__':Path(__file__).with_name('cases.json').write_text(json.dumps(cases(),indent=2,sort_keys=True)+'\n')
