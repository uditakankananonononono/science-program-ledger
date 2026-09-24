"""P21-01: identifiability + ensemble target-rank stability on Dwivedi2014 IL-6 model (BIOMD0000000535).
Run: python3 tool/ident.py results/results.json   (needs libroadrunner, numpy, scipy)"""
import sys, json, os, numpy as np, roadrunner
from scipy.stats import chi2 as CHI2
roadrunner.Logger.setLevel(roadrunner.Logger.LOG_CRITICAL)
HERE = os.path.dirname(os.path.abspath(__file__))
r = roadrunner.RoadRunner(os.path.join(HERE, 'BIOMD0000000535.xml'))
r.integrator.relative_tolerance = 1e-6; r.integrator.absolute_tolerance = 1e-10
allp = r.model.getGlobalParameterIds()
FIXED_PREFIX = ('mw640ca705','mw43ccad8c','mw9f83bdd3','mwa071fdbe','mw2c605ff5','mwc691d0d1','mwa8283449',
                'mw6729db10','mw434adaf5','mw6a5e10a9','mw1366c3b5','mwf67caf9d','mw4aea26f6','mwbd1d5bc3',
                'mw583e0056','Dose','ModelValue_48','Metabolite_3')
EST = [p for p in allp if not p.startswith(FIXED_PREFIX)]
import libsbml
_m = libsbml.readSBML(os.path.join(HERE, 'BIOMD0000000535.xml')).getModel()
NAME = {_m.getParameter(i).getId(): _m.getParameter(i).getName() for i in range(_m.getNumParameters())}
NOM = np.array([r[p] for p in EST]); LNOM = np.log10(NOM)
fl = r.model.getFloatingSpeciesIds()
OBS = ['['+next(i for i in fl if i.startswith(k))+']' for k in ('mwf626e95e','mw114aa90f','mw48867e93')]
OBS_NAMES = ['serum_IL6','serum_CRP','tissue_pSTAT3']
X0 = r.model.getFloatingSpeciesConcentrations().copy()
DAYS = np.array([0,1,3,7,14,21,28,42,56,70,84.]); T = DAYS*24; HOLD = np.isin(DAYS,[14,42,70]); TRAIN = ~HOLD
CV = np.array([0.10,0.10,0.15])

def setp(lp):
    r.resetAll(); 
    for p,v in zip(EST,10**lp): r[p]=v

def steady(lp):
    """untreated steady state for parameter set lp: settle 3000 h from nominal SS, no dose"""
    setp(lp); r['ModelValue_48']=0.0
    r.timeCourseSelections=['time']+['['+i+']' for i in fl]
    s=r.simulate(0,3000,3); return np.array(s[-1,1:])

def experiment(lp, times):
    xs = steady(lp); setp(lp)
    for i,idx in enumerate(fl): r.model.setFloatingSpeciesConcentrations([i],[max(xs[i],0.0)]) if False else None
    r.model.setFloatingSpeciesInitConcentrations(np.maximum(xs,0)); r.reset()
    r['ModelValue_48']=300.0; r.timeCourseSelections=['time']+OBS
    tt=np.unique(np.concatenate([[0],times]))
    s=np.array(r.simulate(times=list(tt)))
    out=s[:,1:]; return out[np.searchsorted(tt,times)]

def logobs(lp, times): return np.log(np.maximum(experiment(lp,times),1e-12))

def jac(lp, times, h=1e-3):
    y0=logobs(lp,times).ravel(); J=np.zeros((y0.size,len(lp)))
    for k in range(len(lp)):
        e=np.zeros(len(lp)); e[k]=h
        J[:,k]=(logobs(lp+e,times).ravel()-logobs(lp-e,times).ravel())/(2*h)
    return J

def target_scores(lp):
    base=steady(lp)[fl.index(OBS[2][1:-1])]; sc=np.zeros(len(lp))
    for k in range(len(lp)):
        l2=lp.copy(); l2[k]+=np.log10(0.5); sc[k]=(base-steady(l2)[fl.index(OBS[2][1:-1])])/base
    return sc

def main(out):
    rng=np.random.default_rng(2101); res={'model':'BIOMD0000000535 Dwivedi2014 IL-6','n_est':len(EST),
        'estimated':[NAME[p] for p in EST]}
    # A4 structural
    Td=np.linspace(0,2016,201)[1:]
    Js=jac(LNOM,Td); U,S,Vt=np.linalg.svd(Js,full_matrices=False); rel=S/S[0]
    null=Vt[rel<1e-6]; struct_nonid=[NAME[EST[k]] for k in range(len(EST)) if null.size and np.abs(null[:,k]).max()>0.1]
    res['structural']={'rank':int((rel>=1e-6).sum()),'n':len(EST),'singular_rel':rel.tolist(),'non_identifiable':struct_nonid}
    # data
    ytrue=logobs(LNOM,T); y=ytrue+rng.normal(0,1,ytrue.shape)*CV
    W=np.tile(1/CV**2,(len(T),1))
    def chi2(lp,mask=TRAIN):
        try: d=logobs(lp,T)-y
        except Exception: return np.inf
        return float(((d[mask]**2)*W[mask]).sum())
    # A5 practical (FIM on training design, log10 params)
    Jt=jac(LNOM,T[TRAIN])*np.log(10); Wt=np.tile(1/CV**2,(TRAIN.sum(),1)).ravel()
    F=Jt.T@(Jt*Wt[:,None]); Finv=np.linalg.pinv(F); se=np.sqrt(np.maximum(np.diag(Finv),0))
    se[np.diag(F)<1e-12]=np.inf
    prac=[bool(1.96*s<=0.5) for s in se]
    res['practical']={'criterion':'1.96*SE(log10 p)<=0.5','n_identifiable':int(sum(prac)),
       'table':[{'param':NAME[p],'nominal':float(v),'se_log10':(float(s) if np.isfinite(s) else None),'identifiable':pi,
                 'structural_ok':NAME[p] not in struct_nonid} for p,v,s,pi in zip(EST,NOM,se,prac)]}
    # targets nominal
    sc0=target_scores(LNOM); order=np.argsort(-sc0); top5=list(order[:5])
    res['nominal_targets']=[{'param':NAME[EST[k]],'pSTAT3_drop':float(sc0[k])} for k in order[:10]]
    # A6 ensemble
    C=np.linalg.inv(F+np.eye(len(EST))/1.0**2); Lc=np.linalg.cholesky(C+1e-12*np.eye(len(EST)))
    c0=chi2(LNOM); thr=CHI2.ppf(0.95,len(EST))
    # A6 (original) outcome recorded, not re-run: 3 accepted / 20000 draws
    res['ensemble_A6_independence']={'accepted':3,'draws':20000}
    def logpost(lp):
        c=chi2(lp)
        if not np.isfinite(c) or c-c0>thr: return -np.inf
        return -0.5*float(((lp-LNOM)**2).sum())
    step=np.sqrt(2.38**2/len(EST)*0.05); cur=LNOM.copy(); lcur=logpost(cur); acc=[]; nacc=0; draws=0
    for it in range(4000):
        prop=cur+step*(Lc@rng.normal(size=len(EST))); lpp=logpost(prop); draws+=1
        if np.log(rng.uniform())<lpp-lcur: cur,lcur=prop,lpp; nacc+=1
        if it<1000 and it%100==99:
            a=nacc/100; step*=1.5 if a>0.4 else (0.6 if a<0.2 else 1.0); nacc=0
            print('burn',it,a,step,flush=True)
        if it>=1000 and (it-1000)%10==9: acc.append(cur.copy())
    res['ensemble']={'sampler':'A6b RW-Metropolis','members':len(acc),'post_burn_accept':nacc/3000,
        'chi2_nominal':c0,'threshold':thr,'final_step':step,
        'unique_members':int(len({tuple(np.round(a,8)) for a in acc})),
        'log10_sd_per_param':{NAME[EST[k]]:float(np.std(np.array(acc)[:,k])) for k in range(len(EST))},
        'log10_sd_median':float(np.median(np.std(np.array(acc),axis=0))),
        'max_abs_log10_dev_median_over_members':float(np.median(np.abs(np.array(acc)-LNOM).max(axis=1)))}
    print("ensemble done",len(acc),draws,flush=True); ranks=[]; stay=[]; preds=[]
    dropped=0
    for lp in acc:
        try: sc=target_scores(lp); pr=experiment(lp,T)
        except Exception: dropped+=1; continue
        rk=np.empty(len(sc),int); rk[np.argsort(-sc)]=np.arange(len(sc))
        ranks.append(rk); stay.append(all(rk[k]<10 for k in top5)); preds.append(pr)
    res['ensemble']['dropped_screen_failures']=dropped
    ranks=np.array(ranks); frac=float(np.mean(stay)) if stay else None
    res['G2']={'top5':[NAME[EST[k]] for k in top5],'frac_all_top5_in_top10':frac,
       'per_target_frac_in_top10':{NAME[EST[k]]:float(np.mean(ranks[:,k]<10)) for k in top5},
       'per_target_rank_median_IQR':{NAME[EST[k]]:[float(np.percentile(ranks[:,k]+1,q)) for q in (25,50,75)] for k in top5},
       'pass':bool(frac is not None and frac>=0.8)}
    # G3
    obs=np.exp(y); med=np.median(np.array(preds),axis=0); nr={}
    for j,n in enumerate(OBS_NAMES):
        rng_=obs[:,j].max()-obs[:,j].min(); nr[n]=float(np.sqrt(np.mean((med[HOLD,j]-obs[HOLD,j])**2))/rng_)
    res['G3']={'nRMSE_heldout':nr,'pass':bool(all(v<=0.2 for v in nr.values()))}
    res['G1']={'structural_reported':len(EST),'practical_reported':len(EST),'pass':True,
       'hypothesis_part1_fewer_than_half_identifiable':bool(sum(prac)<len(EST)/2)}
    # failure rule: candidate extra measurements if G2 fails
    if not res['G2']['pass']:
        cands={}
        for j,n in enumerate(OBS_NAMES):
            for extra in ([0.25,0.5],[2,5],[10,35]):
                te=np.sort(np.concatenate([T[TRAIN],np.array(extra)*24]))
                Je=jac(LNOM,te)*np.log(10); Je=Je.reshape(len(te),3,-1)
                Fe=F+sum((Je[np.isin(te,np.array(extra)*24),jj,:].T@Je[np.isin(te,np.array(extra)*24),jj,:])/CV[jj]**2 for jj in [j])
                g=np.zeros(len(EST)); Ce=np.linalg.pinv(Fe)
                # rank uncertainty proxy: variance of top-5 score gradient directions
                cands[f'{n}@days{extra}']=float(np.trace(Ce[np.ix_(top5,top5)]))
        base=float(np.trace(Finv[np.ix_(top5,top5)]))
        res['OED']={'baseline_top5_param_var':base,'candidates':dict(sorted(cands.items(),key=lambda x:x[1])[:6])}
    json.dump(res,open(out,'w'),indent=1,default=float); print(json.dumps({k:res[k] for k in ('structural','G1','G2','G3','ensemble')},default=float)[:3000])
if __name__=='__main__': main(sys.argv[1])
