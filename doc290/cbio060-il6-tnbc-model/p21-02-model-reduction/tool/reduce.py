"""P21-02: greedy species-freezing reduction of BIOMD0000000535 (Dwivedi 2014 IL-6).
Run: python3 tool/reduce.py results/results.json  (libroadrunner, python-libsbml, numpy, scipy; ~5-10 min)"""
import sys, os, json, numpy as np, roadrunner, libsbml
from scipy.optimize import least_squares
roadrunner.Logger.setLevel(roadrunner.Logger.LOG_CRITICAL)
HERE=os.path.dirname(os.path.abspath(__file__)); SB=open(os.path.join(HERE,'BIOMD0000000535.xml')).read()
TOP5={'kcatSTATPhos','ksynthIL6Gut','kRLOn','kRShedding','kCRPSecretion'}; TIE={'kCRPSecretion','VmProtSynth'}
GATE_PARAMS=None  # filled from full-model screen ranks 1-20
FIXED_PREFIX=('mw640ca705','mw43ccad8c','mw9f83bdd3','mwa071fdbe','mw2c605ff5','mwc691d0d1','mwa8283449','mw6729db10',
  'mw434adaf5','mw6a5e10a9','mw1366c3b5','mwf67caf9d','mw4aea26f6','mwbd1d5bc3','mw583e0056','Dose','ModelValue_48','Metabolite_3')
TG=np.linspace(0,2016,201)
def build(frozen):
    d=libsbml.readSBMLFromString(SB); m=d.getModel()
    for sid in frozen: m.getSpecies(sid).setBoundaryCondition(True)
    r=roadrunner.RoadRunner(libsbml.writeSBMLToString(d))
    r.integrator.relative_tolerance=1e-6; r.integrator.absolute_tolerance=1e-10; return r
base=build([]); FL=list(base.model.getFloatingSpeciesIds())
_m=libsbml.readSBMLFromString(SB).getModel()
NAME={_m.getParameter(i).getId():_m.getParameter(i).getName() for i in range(_m.getNumParameters())}
EST=[p for p in base.model.getGlobalParameterIds() if not p.startswith(FIXED_PREFIX)]
def sid(prefix): return next(i for i in FL if i.startswith(prefix))
OUT=[sid('mw2c9b0499'),sid('mw48867e93')]           # tissue IL-6, tissue pSTAT3
OBS=[sid('mwf626e95e'),sid('mw114aa90f'),sid('mw48867e93')]  # P21-01 observables
SPNAME={_m.getSpecies(i).getId():_m.getSpecies(i).getName()+'@'+_m.getSpecies(i).getCompartment()[:8] for i in range(_m.getNumSpecies())}
def run(r,dose=300.0,inhib=None,times=TG,sel=OUT,lp=None):
    r.resetAll()
    if lp is not None:
        for p,v in zip(EST,10**lp): r[p]=v
    if inhib: r[inhib]=r[inhib]*0.5
    r['ModelValue_48']=0.0; r.timeCourseSelections=['time']+['['+s+']' for s in r.model.getFloatingSpeciesIds()]
    if inhib or lp is not None:
        s=r.simulate(0,3000,3); x=np.maximum(np.array(s[-1,1:]),0)
        r.model.setFloatingSpeciesInitConcentrations(x); r.reset()
    r['ModelValue_48']=dose; allsp=list(r.model.getFloatingSpeciesIds())+list(r.model.getBoundarySpeciesIds())
    r.timeCourseSelections=['time']+['['+s+']' for s in sel]
    tt=np.unique(np.concatenate([[0],times])); s=np.array(r.simulate(times=list(tt)))[:,1:]
    return s[np.searchsorted(tt,times)]
def nrmse(red,full): return np.sqrt(np.mean((red-full)**2,axis=0))/np.maximum(full.max(0)-full.min(0),1e-300)
def screen(r):
    def ss(inh):
        r.resetAll()
        if inh: r[inh]=r[inh]*0.5
        r['ModelValue_48']=0.0; r.timeCourseSelections=['time','['+OUT[1]+']']
        return float(r.simulate(0,3000,3)[-1,1])
    b=ss(None); return {NAME[p]:(b-ss(p))/b for p in EST}
def main(out):
    res={}
    fs=screen(base); rank=sorted(fs,key=lambda k:-fs[k]); res['full_screen_top10']=[(k,fs[k]) for k in rank[:10]]
    inv={NAME[p]:p for p in EST}; gate=[inv[k] for k in rank[:20]]
    SEL=[100.,300.,600.]; fullsel={d:run(base,dose=d) for d in SEL}; fullgate={p:run(base,inhib=p) for p in gate}
    frozen=[]; path=[]
    while len(FL)-len(frozen)>12:
        best=None
        for s_ in FL:
            if s_ in frozen or s_ in OUT: continue
            try:
                r=build(frozen+[s_]); e=max(float(nrmse(run(r,dose=d),fullsel[d]).max()) for d in SEL)
            except Exception: e=np.inf
            if best is None or e<best[1]: best=(s_,e)
        frozen.append(best[0]); path.append({'n_odes':len(FL)-len(frozen),'froze':SPNAME[best[0]],'sel_err':best[1]})
        print(path[-1],flush=True)
    res['path']=path; red=build(frozen)
    kept=[SPNAME[s_] for s_ in FL if s_ not in frozen]; res['kept_species']=kept; res['frozen_species']=[SPNAME[s_] for s_ in frozen]
    G1v={}
    for p in gate:
        try: G1v[NAME[p]]=nrmse(run(red,inhib=p),fullgate[p]).tolist()
        except Exception: G1v[NAME[p]]=[np.inf,np.inf]
    allv=np.array(list(G1v.values()))
    res['G1']={'n_odes':len(kept),'nRMSE_[tissueIL6,tissuePSTAT3]':G1v,'max':float(allv.max()),'mean':float(allv.mean()),
               'pass':bool(len(kept)<=12 and allv.max()<=0.1)}
    rs=screen(red); rr_=sorted(rs,key=lambda k:-rs[k]); t5=set(rr_[:5])
    ok = t5==TOP5 or t5==(TOP5-{'kCRPSecretion'})|{'VmProtSynth'}
    res['G2']={'reduced_top10':[(k,rs[k]) for k in rr_[:10]],'reduced_top5':sorted(t5),'pass':bool(ok)}
    # G3: synthetic data from P21-01 recipe
    rng=np.random.default_rng(2101); DAYS=np.array([0,1,3,7,14,21,28,42,56,70,84.]); T=DAYS*24; TR=~np.isin(DAYS,[14,42,70])
    CV=np.array([.1,.1,.15]); y=np.log(np.maximum(run(base,times=T,sel=OBS),1e-12))+rng.normal(0,1,(len(T),3))*CV
    L0=np.log10(np.array([base[p] for p in EST]))
    def fit(r):
        def resid(lp):
            try: m=np.log(np.maximum(run(r,times=T,sel=OBS,lp=lp),1e-12))
            except Exception: return np.full(TR.sum()*3,1e3)
            return ((m-y)/CV)[TR].ravel()
        f=least_squares(resid,L0,bounds=(L0-2,L0+2),diff_step=1e-3,max_nfev=60)
        J=f.jac; k=int((np.abs(J).sum(0)>1e-8).sum()); n=f.fun.size; rss=float((f.fun**2).sum())
        return {'rss_w':rss,'n':n,'k':k,'aic':n*np.log(rss/n)+2*k,'nfev':int(f.nfev)}
    ff=fit(base); fr=fit(red); res['G3']={'full':ff,'reduced':fr,'pass':bool(fr['aic']<=ff['aic'])}
    json.dump(res,open(out,'w'),indent=1,default=float)
    print(json.dumps({k:res[k] for k in ('G2','G3')},default=float)[:2000]); print('G1',res['G1']['max'],res['G1']['mean'],res['G1']['pass'])
if __name__=='__main__': main(sys.argv[1])
