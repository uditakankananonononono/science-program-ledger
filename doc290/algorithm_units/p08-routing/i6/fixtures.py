"""Prospective input descriptions only; no method evaluation."""
import copy,json
from pathlib import Path
MAX=2**53-1

def edge(target,ss=(1,1),exposure=0):return {'target':target,'time':1,'exposure':exposure,'scenario_times':list(ss)}
def statement(G,start='a',goal='g',budget=0,forbidden=None,penalties=None):return {'graph':G,'start':start,'goal':goal,'budget':budget,'forbidden':[] if forbidden is None else forbidden,'penalties':[] if penalties is None else penalties,'route':None}
def controls():
    return [
      ('unreachable',statement({'a':[edge('b')],'b':[],'g':[]}),'NO_FEASIBLE_PATH'),
      ('budget',statement({'a':[edge('g',exposure=2)],'g':[]},budget=1),'NO_FEASIBLE_PATH'),
      ('identity',statement({'a':[edge('b')],'b':[]},goal='a'),'COMPLETED'),
      ('revisit',statement({'a':[edge('b')],'b':[edge('c'),edge('g')],'c':[edge('b')],'g':[]},forbidden=[[['a',0],['b',1]]]),'COMPLETED'),
      ('tie',statement({'a':[edge('g',(2,2)),edge('g',(2,2))],'g':[]}),'COMPLETED'),
      ('modelDomain',statement({'a':[edge('g') for _ in range(7)],'g':[]}),'UNAVAILABLE_DOMAIN'),
      ('invalid',statement({'a':[edge('g',exposure=2)],'g':[]},budget=True),'INVALID'),
      ('witnessDomain',statement({'a':[edge('b',(MAX,MAX))],'b':[edge('g',(MAX,MAX))],'g':[]}),'UNAVAILABLE_WITNESS_DOMAIN')]
def cases():
    originals=json.loads((Path(__file__).resolve().parent.parent/'i5/cases.json').read_text());out=[]
    for c in originals:
        expected='INVALID' if c['expected']=='INVALID' else 'COMPLETED' if c['statement']['route'] is None else 'PRESERVED';out.append(dict(copy.deepcopy(c),expected=expected))
    for c in originals:
        if c['name'] in 'ABCDEFGH':
            s=copy.deepcopy(c['statement']);s['route']=None;out.append({'name':c['name']+':null','statement':s,'expected':'COMPLETED'})
    out += [{'name':'control6:'+name,'statement':s,'expected':expected} for name,s,expected in controls()]
    assert len(out)==36
    return out

def development():
    # Synthetic separate from fixed36, including all refusal stages.
    G={'q':[edge('z',(2,3))],'z':[edge('q',(1,2))]};s=statement(G,start='q',goal='z',forbidden=[[['q',0],['z',0]]])
    supplied=copy.deepcopy(s);supplied['route']={'path':['q','z'],'edges':[{'source':'q','edge_index':0,'target':'z'}],'scenario_totals':[2,3],'worst_time':3,'exposure':0,'turn_penalty':0}
    no=statement({'a':[edge('b',(2,3))],'b':[],'g':[]});dom=statement({'a':[edge('g',(2,3)) for _ in range(8)],'g':[]});invalid=copy.deepcopy(dom);invalid['budget']=False
    cap=statement({'a':[edge('b',(MAX,MAX-1))],'b':[edge('g',(2,2))],'g':[]})
    return [{'name':'dev:'+str(k),'statement':x,'expected':e} for k,(x,e) in enumerate([(s,'COMPLETED'),(supplied,'PRESERVED'),(no,'NO_FEASIBLE_PATH'),(dom,'UNAVAILABLE_DOMAIN'),(invalid,'INVALID'),(cap,'UNAVAILABLE_WITNESS_DOMAIN')])]
if __name__=='__main__':Path(__file__).with_name('cases.json').write_text(json.dumps(cases(),indent=2,sort_keys=True)+'\n')
