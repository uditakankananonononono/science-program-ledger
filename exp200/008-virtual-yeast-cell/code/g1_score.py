import json

truth=json.load(open('results/sgd_truth.json'))
tset={g for g,v in truth.items() if isinstance(v,str) and v in ('viable','inviable')}

def load(model,arm):
    if arm=='rich':
        parts=json.load(open(f'results/g1rich_{model}_parts.json'))
        wt=json.load(open(f'results/g1rich_{model}_wt.json'))['wt']
    else:
        p=f'results/g1_{model}_v2_parts.json'
        import os
        if not os.path.exists(p): p=f'results/g1_{model}_parts.json'
        parts=json.load(open(p))
        w=f'results/g1_{model}_wt_v2.json'
        if not os.path.exists(w): w=f'results/g1_{model}_wt.json'
        wt=json.load(open(w))['wt']
    return parts,wt

def score(parts,wt,genes):
    tp=tn=fp=fn=0; uns=[]
    for g in genes:
        v=parts[g]
        if v['unsolvable']: uns.append(g); continue
        ess = v['growth'] < 0.01*wt
        true_ess = truth[g]=='inviable'
        if ess and true_ess: tp+=1
        elif ess: fp+=1
        elif true_ess: fn+=1
        else: tn+=1
    sens=tp/(tp+fn) if tp+fn else 0.0; spec=tn/(tn+fp) if tn+fp else 0.0
    return {'BA':(sens+spec)/2,'sensitivity':sens,'specificity':spec,'tp':tp,'tn':tn,'fp':fp,'fn':fn,'unsolvable':uns,'n_scored':tp+tn+fp+fn}

out={}
for arm in ['minimal','rich']:
    y,wy=load('yeast8',arm); i,wi=load('imm904',arm)
    common=(set(y)&set(i)&tset)-{g for g in set(y)&set(i) if y[g]['unsolvable'] or i[g]['unsolvable']}
    ys=score(y,wy,sorted(common)); is_=score(i,wi,sorted(common))
    y_only=sorted(set(y)&tset)
    yo=score(y,wy,y_only)
    out[arm]={'wt_yeast8':wy,'wt_imm904':wi,'common_set_size':len(common),
              'yeast8_common':ys,'imm904_common':is_,'yeast8_own_intersect':{'n':len(y_only),**yo},
              'gate_G1':{'threshold_BA':0.85,'yeast8_BA':ys['BA'],'imm904_BA':is_['BA'],
                         'pass_BA':ys['BA']>=0.85,'beat_baseline':ys['BA']>=is_['BA'],
                         'PASS':ys['BA']>=0.85 and ys['BA']>=is_['BA']}}
json.dump(out,open('results/g1_official.json','w'),indent=1)
# overwrite the STALE INVALID files with official artifacts
json.dump(out['minimal'],open('results/g1_yeast8_metrics.json','w'),indent=1)
json.dump({'note':'OFFICIAL G1 artifact, supersedes the invalid 02:31 prototype file. See g1_official.json.'},open('results/g1_yeast8.json','w'))
for arm in ['minimal','rich']:
    g=out[arm]['gate_G1']
    print(arm,'| common n=',out[arm]['common_set_size'],'| Yeast8 BA',round(g['yeast8_BA'],4),'| iMM904 BA',round(g['imm904_BA'],4),'| pass_BA',g['pass_BA'],'| beat',g['beat_baseline'],'| GATE',('PASS' if g['PASS'] else 'FAIL'))
    print('   yeast8 confusion', {k:out[arm]['yeast8_common'][k] for k in ('tp','tn','fp','fn','sensitivity','specificity')})
