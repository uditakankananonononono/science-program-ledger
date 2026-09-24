"""P21-09: chemo +/- IL-6 blockade on the Nazari 2018 IL-6 / cancer-stem-cell model (BIOMD0000000819).
Run: python3 tool/csc.py results/results.json   (libroadrunner, python-libsbml, numpy)"""
import sys, os, json, numpy as np, roadrunner, libsbml
roadrunner.Logger.setLevel(roadrunner.Logger.LOG_CRITICAL)
HERE=os.path.dirname(os.path.abspath(__file__))
def sbml_with_chemo():
    d=libsbml.readSBML(os.path.join(HERE,'BIOMD0000000819.xml')); m=d.getModel(); comp=m.getCompartment(0).getId()
    for sp,k in (('Cancer_Stem_Cell_S','kcS'),('Progenitor_tumor_cell_E','kcE'),('Differentiated_tumor_cell_D','kcD')):
        p=m.createParameter(); p.setId(k); p.setValue(0.0); p.setConstant(False)
        r=m.createReaction(); r.setId('chemo_'+sp); r.setReversible(False)
        if r.getLevel()>2 or d.getLevel()>2: r.setFast(False)
        s=r.createReactant(); s.setSpecies(sp); s.setStoichiometry(1.0); s.setConstant(True) if d.getLevel()>2 else None
        kl=r.createKineticLaw(); kl.setMath(libsbml.parseL3Formula(f'{comp} * {k} * {sp}'))
    return libsbml.writeSBMLToString(d)
SB=sbml_with_chemo()
def fresh():
    r=roadrunner.RoadRunner(SB); r.integrator.relative_tolerance=1e-8; r.integrator.absolute_tolerance=1e-6; return r
R=[fresh()]
PERT=['alpha_S','Pstar_Smin','P_Smax','myu','gamma_S','gamma_E','gamma_D','K_f','K_r','rho','lambda','K_p']
SEL=['time','Cancer_Stem_Cell_S','Progenitor_tumor_cell_E','Differentiated_tumor_cell_D']
def sf(row): return row[1]/(row[1]+row[2]+row[3])
def arm(params, chemo, b, ratio=10.0, kc=0.3):
    r=R[0]; r.resetAll()
    for k,v in params.items(): r[k]=v
    r.timeCourseSelections=SEL; s0=r.simulate(0,100,2); kf=r['K_f']
    if chemo: r['kcE']=kc; r['kcD']=kc; r['kcS']=kc/ratio
    r['K_f']=kf*(1-b); s1=r.simulate(100,121,2)
    r['kcE']=r['kcD']=r['kcS']=0.0; r['K_f']=kf; s2=r.simulate(121,142,2)
    return {'sf_d100':sf(s0[-1]),'sf_d121':sf(s1[-1]),'sf_d142':sf(s2[-1]),'total_d121':float(sum(s1[-1][1:])),'total_d142':float(sum(s2[-1][1:]))}
def arm_retry(*a,**k):
    for att in (0,1):
        try: return arm(*a,**k)
        except Exception as e: err=e; R[0]=fresh()
    raise err
def compare(params, ratio=10.0, b=0.98):
    c=arm_retry(params,True,0.0,ratio); cb=arm_retry(params,True,b,ratio); bo=arm_retry(params,False,b,ratio); un=arm_retry(params,False,0.0,ratio)
    return {'untreated':un,'blockade_only':bo,'chemo':c,'chemo_blockade':cb,
            'benefit_d121':1-cb['sf_d121']/c['sf_d121'],'benefit_d142':1-cb['sf_d142']/c['sf_d142'],
            'chemo_raises_sf':c['sf_d121']>un['sf_d121']}
def main(out):
    res={}; nom=compare({}); res['nominal']=nom
    res['sensitivity_b']={str(b):compare({},b=b)['benefit_d121'] for b in (0.5,0.9,0.98)}
    print(json.dumps(res,default=float)[:2500],flush=True)
    base={k:R[0][k] for k in PERT}; rng=np.random.default_rng(2109); ben=[]; ok=[]; fails=0; signs=[]
    for i in range(200):
        p={k:base[k]*10**rng.normal(0,0.3) for k in PERT}; ratio=10**rng.uniform(0.5,1.5)
        try: c=compare(p,ratio); ben.append(c['benefit_d121']); ok.append(c['benefit_d121']>=0.3); signs.append(c['benefit_d121']>0)
        except Exception: fails+=1; ok.append(False)
    ben=np.array(ben)
    res['G2']={'nominal_benefit_d121':nom['benefit_d121'],'sets':200,'fails':fails,'frac_benefit_ge_30pct':float(np.mean(ok)),
       'benefit_quantiles_5_25_50_75_95':np.percentile(ben,[5,25,50,75,95]).tolist() if len(ben) else None,
       'frac_benefit_positive':float(np.mean(signs)) if signs else None,
       'pass':bool(nom['benefit_d121']>=0.3 and np.mean(ok)>=0.8)}
    res['G1']={'verdict':'NOT MET - no digitisable conversion data (A5); sign-level predictions only','pass':False}
    res['G3']={'verdict':'NOT EVALUABLE (A7)','baseline_sf_untreated_d121':nom['untreated']['sf_d121'],'pass':None}
    json.dump(res,open(out,'w'),indent=1,default=float); print('G2',res['G2'])
if __name__=='__main__': main(sys.argv[1])
