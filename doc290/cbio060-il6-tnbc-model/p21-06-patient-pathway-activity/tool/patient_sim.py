"""P21-06: patient-specific simulated pSTAT3 vs survival (METABRIC RFS, TCGA PanCan basal PFS) via cBioPortal API.
Run from repo root: python3 doc290/cbio060-il6-tnbc-model/p21-06-patient-pathway-activity/tool/patient_sim.py <out.json>"""
import sys, os, json, requests, numpy as np, pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
HERE=os.path.dirname(os.path.abspath(__file__)); BASE=os.path.join(HERE,'..','..')
sys.path.insert(0, os.path.join(BASE,'p21-01-identifiability','tool')); import ident as I, roadrunner
API='https://www.cbioportal.org/api'
GENES={3569:'IL6',3570:'IL6R',3716:'JAK1',5771:'PTPN2',6868:'ADAM17',6774:'STAT3'}
PMAP={'IL6':'ksynthIL6Gut','IL6R':'kRsynth','JAK1':'kcatSTATPhos','PTPN2':'VmSTATDephos','ADAM17':'kRShedding'}
K={I.NAME[p]:p for p in I.EST}
STAT3_IDS=[next(i for i in I.fl if i.startswith(k)) for k in ('mw2b255f94','mw48867e93')]
PS=I.OBS[2][1:-1]
def fetch_expr(study, profile, log1p):
    r=requests.post(f'{API}/molecular-profiles/{profile}/molecular-data/fetch',json={'entrezGeneIds':list(GENES),'sampleListId':f'{study}_all'},timeout=60)
    d=pd.DataFrame(r.json()); d['gene']=d.entrezGeneId.map(GENES)
    m=d.pivot_table(index='patientId',columns='gene',values='value',aggfunc='mean')
    return np.log2(m.clip(lower=0)+1) if log1p else m
def clin(study, kind):
    r=requests.get(f'{API}/studies/{study}/clinical-data',params={'clinicalDataType':kind,'pageSize':100000},timeout=60)
    d=pd.DataFrame(r.json()); return d.pivot_table(index='patientId',columns='clinicalAttributeId',values='value',aggfunc='first')
def cohort(name):
    if name=='METABRIC':
        s=clin('brca_metabric','SAMPLE'); p=clin('brca_metabric','PATIENT')
        tn=s[(s.ER_STATUS=='Negative')&(s.PR_STATUS=='Negative')&(s.HER2_STATUS=='Negative')].index
        e=fetch_expr('brca_metabric','brca_metabric_mrna',False); T,E='RFS_MONTHS','RFS_STATUS'
    else:
        p=clin('brca_tcga_pan_can_atlas_2018','PATIENT'); s=clin('brca_tcga_pan_can_atlas_2018','SAMPLE')
        sub=p['SUBTYPE'] if 'SUBTYPE' in p else s['SUBTYPE']
        tn=sub[sub=='BRCA_Basal'].index
        e=fetch_expr('brca_tcga_pan_can_atlas_2018','brca_tcga_pan_can_atlas_2018_rna_seq_v2_mrna',True); T,E='PFS_MONTHS','PFS_STATUS'
    ids=[i for i in tn if i in e.index and i in p.index]
    df=e.loc[ids].copy(); df['T']=pd.to_numeric(p.loc[ids,T],errors='coerce'); df['E']=p.loc[ids,E].astype(str).str.startswith('1').astype(int)
    n0=len(df); df=df.dropna(); return df,{'tnbc_with_expr':n0,'analysed':len(df),'events':int(df.E.sum())}
def simulate(mults, stat3):
    I.setp(I.LNOM)
    for pn,m in mults.items(): I.r[K[pn]]=I.r[K[pn]]*m
    for sid in STAT3_IDS: I.r['['+sid+']']=I.r['['+sid+']']*stat3
    I.r['ModelValue_48']=0.0; I.r.timeCourseSelections=['time','['+PS+']']
    return float(I.r.simulate(0,3000,3)[-1,1])
def fresh():
    I.r=roadrunner.RoadRunner(os.path.join(BASE,'p21-01-identifiability','tool','BIOMD0000000535.xml'))
    I.r.integrator.relative_tolerance=1e-6; I.r.integrator.absolute_tolerance=1e-10
def sim_retry(*a):
    for att in (0,1):
        try: return simulate(*a)
        except Exception as ex: err=ex; fresh()
    return np.nan
def evaluate(df, s):
    z=(df[list(GENES.values())]-df[list(GENES.values())].mean())/df[list(GENES.values())].std()
    sim=np.array([sim_retry({PMAP[g]:2**(s*z.loc[i,g]) for g in PMAP}, 2**(s*z.loc[i,'STAT3'])) for i in df.index])
    ok=~np.isnan(sim); d=df[ok].copy(); d['sim']=sim[ok]; d['simple']=z[ok].mean(axis=1)
    d['high']=(d.sim>d.sim.median()).astype(int)
    cph=CoxPHFitter().fit(d[['T','E','high']],'T','E'); hr=float(np.exp(cph.params_['high'])); p=float(cph.summary.loc['high','p'])
    ci=lambda x: float(concordance_index(d['T'],-d[x],d['E']))
    return {'n':int(len(d)),'sim_failures':int((~ok).sum()),'HR_high_vs_low':hr,'p':p,
            'cindex_sim':ci('sim'),'cindex_simple':ci('simple'),'cindex_IL6':ci('IL6'),'cindex_STAT3':ci('STAT3'),
            'sim_cv':float(d.sim.std()/d.sim.mean())}
def main(out):
    res={}
    for c in ('METABRIC','TCGA_basal'):
        df,info=cohort('METABRIC' if c=='METABRIC' else 'TCGA'); res[c]={'counts':info}
        for s in (0.25,0.5,1.0): res[c][f's={s}']=evaluate(df,s); print(c,s,res[c][f's={s}'],flush=True)
    a,b=res['METABRIC']['s=0.5'],res['TCGA_basal']['s=0.5']
    g1=(a['HR_high_vs_low']>=1.5 and a['p']<0.05 and b['HR_high_vs_low']>1) or (b['HR_high_vs_low']>=1.5 and b['p']<0.05 and a['HR_high_vs_low']>1)
    res['G1']={'pass':bool(g1)}
    res['G2']={'delta_cindex':{k:v['cindex_sim']-v['cindex_simple'] for k,v in (('METABRIC',a),('TCGA_basal',b))},
               'pass':bool(a['cindex_sim']-a['cindex_simple']>=0.02 and b['cindex_sim']-b['cindex_simple']>=0.02)}
    res['G3']={'pass':True,'note':'s=0.25/0.5/1.0 reported per cohort'}
    json.dump(res,open(out,'w'),indent=1,default=float); print(json.dumps({k:res[k] for k in ('G1','G2')}))
if __name__=='__main__': main(sys.argv[1])
