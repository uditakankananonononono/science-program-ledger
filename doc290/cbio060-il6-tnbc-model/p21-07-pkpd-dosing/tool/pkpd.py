"""P21-07: label PK -> PD coupling on the IL-6 model (BIOMD0000000535). Reuses P21-01 tool/ident.py.
Run from repo root: python3 doc290/cbio060-il6-tnbc-model/p21-07-pkpd-dosing/tool/pkpd.py <out.json>"""
import sys, os, json, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE,'..','..','p21-01-identifiability','tool'))
import ident as I
from scipy.stats import chi2 as CHI2
r=I.r; PS=I.OBS[2][1:-1]; LN2=np.log(2)
def pid(name): return next(p for p in I.EST if I.NAME[p]==name)
KCAT=pid('kcatSTATPhos'); KON=pid('kRLOn')
# ---- PK (A2); time in h
RUX=dict(D=20.0,F=0.95,ka=2.0,V=72.0,CL=19.9,MW=306.4,fu=0.03,tau=12.0)
def rux_conc(t, doses):   # nM total plasma
    k=RUX['CL']/RUX['V']; c=np.zeros_like(np.atleast_1d(t),float)
    for td in doses:
        tt=np.atleast_1d(t)-td; m=tt>0
        c[m]+=RUX['F']*RUX['D']/RUX['MW']*1e6/RUX['V']*RUX['ka']/(RUX['ka']-k)*(np.exp(-k*tt[m])-np.exp(-RUX['ka']*tt[m]))
    return c
def mab_conc(t, doses, dose_mg, V, k):  # ug/mL
    c=np.zeros_like(np.atleast_1d(t),float)
    for td in doses:
        tt=np.atleast_1d(t)-td; m=tt>=0; c[m]+=dose_mg/V*np.exp(-k*tt[m])
    return c
UGML_TO_NM=1e3/148.0   # 1 ug/mL of 148 kDa IgG = 6.76 nM
TOC_V=3.2; TOC_kA=LN2/(21.5*24); TOC_kB=LN2/(7.6*24); SIL_V=4.5; SIL_k=0.23/4.5/24
DRUGS={
 'ruxolitinib':dict(param=KCAT,step=0.5,conc=lambda t: rux_conc(t,np.arange(0,672,12.0))*RUX['fu'],K=3.3,tau=12.0),
 'tocilizumab_A':dict(param=KON,step=6.0,conc=lambda t: mab_conc(t,[0.0],560.0,TOC_V,TOC_kA)*UGML_TO_NM,K=2.54,tau=672.0),
 'tocilizumab_B':dict(param=KON,step=6.0,conc=lambda t: mab_conc(t,[0.0],560.0,TOC_V,TOC_kB)*UGML_TO_NM,K=2.54,tau=672.0),
 'siltuximab':dict(param=KON,step=6.0,conc=lambda t: mab_conc(t,[0.0,504.0],770.0,SIL_V,SIL_k)*UGML_TO_NM,K=0.0025,tau=504.0),
}
def g1():
    t=np.linspace(0,24,24001); c=rux_conc(t,[0.0]); cmax=float(c.max())
    k=RUX['CL']/RUX['V']; out={'rux_cmax_nM':[cmax,710.0],'rux_thalf_h':[LN2/k,3.0],
      'toc_A_ss_cmax':[560/TOC_V/(1-np.exp(-TOC_kA*672)),176.0],'toc_A_thalf_d':[21.5,21.5],
      'toc_B_ss_trough_info':[560/TOC_V/(1-np.exp(-TOC_kB*672))*np.exp(-TOC_kB*672),13.4],
      'sil_ss_cmax':[770/SIL_V/(1-np.exp(-SIL_k*504)),332.0],'sil_thalf_d':[LN2/SIL_k/24,20.6]}
    chk={k_:bool(abs(v[0]/v[1]-1)<=0.2) for k_,v in out.items() if not k_.endswith('info')}
    return out,chk
def prepare(lp):
    xs=I.steady(lp); I.setp(lp); r['ModelValue_48']=0.0
    r.model.setFloatingSpeciesInitConcentrations(np.maximum(xs,0)); r.reset()
    return xs[I.fl.index(PS)]
def static(lp,param,mult):
    I.setp(lp); r['ModelValue_48']=0.0; r[param]=r[param]*mult
    r.timeCourseSelections=['time','['+PS+']']; return float(r.simulate(0,3000,3)[-1,1])
def dynamic(lp,drug):
    d=DRUGS[drug]; base=prepare(lp); p0=r[d['param']]; r.timeCourseSelections=['time','['+PS+']']
    t=0.0; ts=[0.0]; ys=[base]
    while t<672-1e-9:
        t1=min(t+d['step'],672.0); cf=float(d['conc'](np.array([(t+t1)/2]))[0])
        r[d['param']]=p0*(1-cf/(cf+d['K'])); s=r.simulate(t,t1,2); ts.append(t1); ys.append(float(s[-1,1])); t=t1
    ts=np.array(ts); sup=1-np.array(ys)/base
    tavg=float(np.trapezoid(sup,ts)/672)
    start={'ruxolitinib':660.0,'tocilizumab_A':0.0,'tocilizumab_B':0.0,'siltuximab':0.0}[drug]; end=start+d['tau']
    win=(ts>=start-1e-9)&(ts<=end+1e-9); peak=float(sup[win].max()); trough=float(sup[np.argmin(np.abs(ts-end))])
    old_win=ts>=672-d['tau']-1e-9 if d['tau']<672 else ts>=0   # first (deviating) implementation, disclosed
    old=(float(sup[old_win].max()), float(sup[old_win][-1] if d['tau']>=672 else sup[old_win].min()))
    cmax=float(d['conc'](np.linspace(0,d['tau'] if d['tau']<672 else 24,2000)).max())
    st=1-static(lp,d['param'],1-cmax/(cmax+d['K']))/base
    return {'dynamic_tavg':tavg,'static_at_cmax':st,'peak_last':peak,'trough_last':trough,
            'sustained':bool(trough>=0.8*peak),'rebound':bool(trough<0.5*peak),'free_cmax_nM':cmax,
            'deviating_first_impl_peak_trough':old,'onset_t_to_90pct_of_peak_h':float(ts[np.argmax(sup>=0.9*sup.max())])}
def rankings(res, toc='tocilizumab_A'):
    ds=['ruxolitinib',toc,'siltuximab']
    dyn=sorted(ds,key=lambda k:-res[k]['dynamic_tavg']); st=sorted(ds,key=lambda k:-res[k]['static_at_cmax'])
    pairs={}
    for i in range(3):
        for j in range(i+1,3):
            a,b=ds[i],ds[j]; pairs[f'{a} vs {b}']={'static_winner':a if res[a]['static_at_cmax']>res[b]['static_at_cmax'] else b,
               'dynamic_winner':a if res[a]['dynamic_tavg']>res[b]['dynamic_tavg'] else b}
            pairs[f'{a} vs {b}']['reversed']=pairs[f'{a} vs {b}']['static_winner']!=pairs[f'{a} vs {b}']['dynamic_winner']
    return {'dynamic_order':dyn,'static_order':st,'pairs':pairs,'any_reversal':any(v['reversed'] for v in pairs.values())}
def fresh():
    # new solver instance: after a CVODE failure the instance stays in a failing state (run 1, disclosed)
    global r
    import roadrunner
    I.r=roadrunner.RoadRunner(os.path.join(HERE,'..','..','p21-01-identifiability','tool','BIOMD0000000535.xml'))
    I.r.integrator.relative_tolerance=1e-6; I.r.integrator.absolute_tolerance=1e-10; r=I.r
def member_eval(lp):
    for attempt in (0,1):
        try: return {dn:dynamic(lp,dn) for dn in ('ruxolitinib','tocilizumab_A','siltuximab')}, attempt
        except Exception as e:
            err=e; fresh()
    raise err
def regen_ensemble():
    rng=np.random.default_rng(2101); ytrue=I.logobs(I.LNOM,I.T); y=ytrue+rng.normal(0,1,ytrue.shape)*I.CV
    W=np.tile(1/I.CV**2,(len(I.T),1))
    def chi2(lp):
        try: d=I.logobs(lp,I.T)-y
        except Exception: return np.inf
        return float(((d[I.TRAIN]**2)*W[I.TRAIN]).sum())
    Jt=I.jac(I.LNOM,I.T[I.TRAIN])*np.log(10); Wt=np.tile(1/I.CV**2,(I.TRAIN.sum(),1)).ravel()
    F=Jt.T@(Jt*Wt[:,None]); C=np.linalg.inv(F+np.eye(len(I.EST))); Lc=np.linalg.cholesky(C+1e-12*np.eye(len(I.EST)))
    c0=chi2(I.LNOM); thr=CHI2.ppf(0.95,len(I.EST))
    def lpost(lp):
        c=chi2(lp)
        return -np.inf if (not np.isfinite(c) or c-c0>thr) else -0.5*float(((lp-I.LNOM)**2).sum())
    step=np.sqrt(2.38**2/len(I.EST)*0.05); cur=I.LNOM.copy(); lc=lpost(cur); acc=[]; na=0
    for it in range(4000):
        pr=cur+step*(Lc@rng.normal(size=len(I.EST))); lp_=lpost(pr)
        if np.log(rng.uniform())<lp_-lc: cur,lc=pr,lp_; na+=1
        if it<1000 and it%100==99:
            a=na/100; step*=1.5 if a>0.4 else (0.6 if a<0.2 else 1.0); na=0
        if it>=1000 and (it-1000)%10==9: acc.append(cur.copy())
    return acc,c0
def main(out):
    res={}; pk,chk=g1(); res['G1']={'values_[model,label]':pk,'checks':chk,'pass':all(chk.values())}; print(res['G1'],flush=True)
    nom={dname:dynamic(I.LNOM,dname) for dname in DRUGS}; res['nominal']=nom
    res['G2']={'arm_A':rankings(nom,'tocilizumab_A'),'arm_B':rankings(nom,'tocilizumab_B'),'pass':True}
    hyp={'toc_sustained':nom['tocilizumab_A']['sustained'],'sil_sustained':nom['siltuximab']['sustained'],
         'rux_rebound':nom['ruxolitinib']['rebound'],'any_reversal':res['G2']['arm_A']['any_reversal']}
    res['hypothesis_nominal']=hyp; print(json.dumps(nom),json.dumps(res['G2']['arm_A']),hyp,flush=True)
    acc,c0=regen_ensemble(); res['ensemble_regen']={'members':len(acc),'chi2_nominal':c0}; print('ens',len(acc),c0,flush=True)
    np.save(out.replace('.json','_ensemble.npy'),np.array(acc))
    # fresh solver instance after the MCMC: the long sampler run left CVODE in a failing state (all members
    # raised CV_CONV_FAILURE in the first run); numerical plumbing only, disclosed in REPORT
    fresh()
    sub=acc[2::3]; same=[]; orders=[]
    for i,lp in enumerate(sub):
        try:
            rr,att=member_eval(lp); res.setdefault('member_retries',0); res['member_retries']+=att
            rk=rankings(rr); h={'toc_sustained':rr['tocilizumab_A']['sustained'],'sil_sustained':rr['siltuximab']['sustained'],
               'rux_rebound':rr['ruxolitinib']['rebound'],'any_reversal':rk['any_reversal']}
            same.append(rk['dynamic_order']==res['G2']['arm_A']['dynamic_order'] and h==hyp); orders.append(rk['dynamic_order'])
        except Exception as e:
            same.append(False); orders.append(['fail']); res.setdefault('member_errors',[]).append(repr(e)[:200])
        if i%20==19: print('member',i+1,np.mean(same),flush=True)
    from collections import Counter
    res['G3']={'members':len(sub),'frac_same_conclusions':float(np.mean(same)),
               'dynamic_order_counts':{' > '.join(k):v for k,v in Counter(tuple(o) for o in orders).items()},
               'pass':bool(np.mean(same)>=0.8)}
    json.dump(res,open(out,'w'),indent=1,default=float); print('G3',res['G3'])
if __name__=='__main__': main(sys.argv[1])
