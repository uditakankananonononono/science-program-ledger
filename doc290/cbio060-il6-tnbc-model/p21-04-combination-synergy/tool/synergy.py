"""P21-04: IL-6 model Bliss synergy atlas + ALMANAC matching. Reuses P21-01 ident.py and the P21-07 saved ensemble.
Run from repo root: python3 doc290/cbio060-il6-tnbc-model/p21-04-combination-synergy/tool/synergy.py <out.json> [almanac_rux.csv]"""
import sys, os, json, itertools, numpy as np, pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__)); BASE=os.path.join(HERE,'..','..')
sys.path.insert(0, os.path.join(BASE,'p21-01-identifiability','tool')); import ident as I, roadrunner
PS=I.OBS[2][1:-1]; IL=next(i for i in I.fl if i.startswith('mw2c9b0499'))
def fresh():
    I.r=roadrunner.RoadRunner(os.path.join(BASE,'p21-01-identifiability','tool','BIOMD0000000535.xml'))
    I.r.integrator.relative_tolerance=1e-6; I.r.integrator.absolute_tolerance=1e-10
def ss(lp, mults):
    I.setp(lp); I.r['ModelValue_48']=0.0
    for p,m in mults.items(): I.r[p]=I.r[p]*m
    I.r.timeCourseSelections=['time','['+PS+']','['+IL+']']; s=I.r.simulate(0,3000,3); return float(s[-1,1]),float(s[-1,2])
def atlas(lp):
    b=ss(lp,{})[0]; single={p:1-ss(lp,{p:0.5})[0]/b for p in I.EST}; out={}
    for a,c in itertools.combinations(I.EST,2):
        comb=1-ss(lp,{a:0.5,c:0.5})[0]/b; sa,sc=single[a],single[c]; out[(a,c)]=comb-(sa+sc-sa*sc)
    return out
def atlas_retry(lp):
    for att in (0,1):
        try: return atlas(lp)
        except Exception as e: err=e; fresh()
    raise err
def mapped_grid(lp, pa, pb):
    b=ss(lp,{})[0]; ex=[]
    for fa in (0.25,0.5,0.75):
        for fb in (0.25,0.5,0.75):
            sa=1-ss(lp,{pa:1-fa})[0]/b; sb=1-ss(lp,{pb:1-fb})[0]/b
            sab=1-ss(lp,{pa:1-fa,pb:1-fb})[0]/b if pa!=pb else 1-ss(lp,{pa:(1-fa)*(1-fb)})[0]/b
            ex.append(sab-(sa+sb-sa*sb))
    return float(np.mean(ex))
def main(out, alm=None):
    res={}; N=lambda p:I.NAME[p]
    # G1: ALMANAC matching (only ruxolitinib NSC 763371 maps, JAK -> kcatSTATPhos)
    if alm and os.path.exists(alm):
        d=pd.read_csv(alm); tn=d[d.CELLNAME.str.contains('MDA-MB-231|HS 578T|BT-549|MDA-MB-468',regex=True)&d.NSC2.notna()]
        partners=sorted(set(tn.NSC1.astype(int))|set(tn.NSC2.astype(int))-{763371})
        res['G1']={'source':'NCI-ALMANAC ComboDrugGrowth_Nov2017 (DrugComb API unreachable from sandbox)',
          'mapped_drugs_in_almanac':['Ruxolitinib (NSC 763371) -> JAK -> kcatSTATPhos'],
          'rux_combo_rows_tnbc':int(len(tn)),'rux_partners_tnbc':len(partners),'matched_pairs_both_mapped':0,
          'verdict':'UNDERPOWERED (0 < 10)','pass':False}
    res['G2']={'verdict':'NOT EVALUABLE (0 matched pairs)','pass':None}
    # model-side: mapped-mechanism pairs (JAK/STAT3 node, IL-6/IL-6R, gp130)
    K=lambda n:next(p for p in I.EST if I.NAME[p]==n)
    mech={'JAK_or_STAT3':K('kcatSTATPhos'),'IL6_or_IL6R_antibody':K('kRLOn'),'gp130':K('kgp130On')}
    res['mapped_mechanism_bliss']={f'{a}+{b}':mapped_grid(I.LNOM,mech[a],mech[b]) for a,b in itertools.combinations_with_replacement(mech,2)}
    print(res['mapped_mechanism_bliss'],flush=True)
    nom=atlas_retry(I.LNOM); order=sorted(nom,key=lambda k:-nom[k]); top5=order[:5]
    res['atlas_top10']=[(N(a)+'+'+N(c),nom[(a,c)]) for a,c in order[:10]]
    res['atlas_bottom5']=[(N(a)+'+'+N(c),nom[(a,c)]) for a,c in order[-5:]]
    res['atlas_n_pairs']=len(nom); res['atlas_frac_positive_bliss']=float(np.mean([v>1e-4 for v in nom.values()]))
    print(res['atlas_top10'],flush=True)
    ens=np.load(os.path.join(BASE,'p21-07-pkpd-dosing','results','results_ensemble.npy'))[5::6]
    hit={k:0 for k in top5}; fails=0
    for i,lp in enumerate(ens):
        try: a=atlas_retry(lp)
        except Exception: fails+=1; continue
        t20=set(sorted(a,key=lambda k:-a[k])[:20])
        for k in top5: hit[k]+=k in t20
        if i%10==9: print('member',i+1,flush=True)
    fr={N(a)+'+'+N(c):hit[(a,c)]/len(ens) for a,c in top5}
    res['G3']={'members':len(ens),'fails':fails,'frac_in_top20':fr,'pass':bool(all(v>=0.8 for v in fr.values()))}
    json.dump(res,open(out,'w'),indent=1,default=float); print('G3',res['G3'])
if __name__=='__main__': main(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None)
