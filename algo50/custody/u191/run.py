#!/usr/bin/env python3
"""UCI 296 Unit 191 frozen runner. No network calls; one selected row/person.

split mode reads only patient/encounter IDs and age. prelock-dev requires the
explicit one-time DEV outcome window and never forms a TEST label. final mode
verifies both lock hashes before loading DEV/TEST outcomes and evaluates once.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, sys, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, SplineTransformer, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from lightgbm import LGBMClassifier

SEED=42
EXCLUDED_IDS={'25040448','55500588','109210482','40867677'}
HF_PROXY={'pioglitazone','rosiglitazone','metformin-rosiglitazone','metformin-pioglitazone','glimepiride-pioglitazone'}
DIAG={'diag_1','diag_2','diag_3'}
DROP_ALWAYS=DIAG|{'encounter_id','patient_nbr','number_diagnoses','readmitted','weight','discharge_disposition_id'}
NUMERIC=['time_in_hospital','num_lab_procedures','num_procedures','num_medications','number_outpatient','number_emergency','number_inpatient']
CAT_BASE=['race','gender','age','admission_type_id','admission_source_id','payer_code','medical_specialty','max_glu_serum','A1Cresult','metformin','repaglinide','nateglinide','chlorpropamide','glimepiride','acetohexamide','glipizide','glyburide','tolbutamide','pioglitazone','rosiglitazone','acarbose','miglitol','troglitazone','tolazamide','examide','citoglipton','insulin','glyburide-metformin','glipizide-metformin','glimepiride-pioglitazone','metformin-rosiglitazone','metformin-pioglitazone','change','diabetesMed']
MEDS={'metformin','repaglinide','nateglinide','chlorpropamide','glimepiride','acetohexamide','glipizide','glyburide','tolbutamide','pioglitazone','rosiglitazone','acarbose','miglitol','troglitazone','tolazamide','examide','citoglipton','insulin','glyburide-metformin','glipizide-metformin','glimepiride-pioglitazone','metformin-rosiglitazone','metformin-pioglitazone'}
AGE_MAP={f'[{i}-{i+10})':i+5 for i in range(0,100,10)}
MISSING={'','?','NA','NaN','None'}
LGBM_PARAMS=dict(n_estimators=100,num_leaves=31,learning_rate=.05,random_state=SEED,n_jobs=1,verbosity=-1)


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def id_hash(x): return hashlib.sha256(str(x).encode()).hexdigest()
def hash_order(ids): return sorted((str(x) for x in ids),key=lambda x:(id_hash(x),x))
def split_ids(ids):
    ids=hash_order(ids); ntest=round(.25*len(ids))
    return ids[ntest:],ids[:ntest]
def selected_ids_from_source(path):
    """Census/selection pass: IDs, encounter_id and age only; no target values."""
    first={}
    with open(path,newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            pid=str(row['patient_nbr'])
            if pid in EXCLUDED_IDS: continue
            eid=str(row['encounter_id'])
            key=(int(eid),eid)
            if pid not in first or key<first[pid][0]: first[pid]=(key,row['age'])
    return first
def make_and_write_manifest(csvpath,outpath):
    first=selected_ids_from_source(csvpath)
    dev,test=split_ids(first)
    manifest={'rule':'After fixed patient_nbr exclusions, SHA256 of canonical decimal patient_nbr ascending; first round-half-even(0.25*N) TEST; remainder DEV; no stratification/reroll','excluded_patient_nbr':sorted(EXCLUDED_IDS),'n_eligible':len(first),'n_dev':len(dev),'n_test':len(test),'dev_ids':dev,'test_ids':test}
    Path(outpath).write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

def load_partition(csvpath, allowed_ids, with_label):
    """Collect one selected row per allowed ID only; never target-load other IDs."""
    allowed=set(map(str,allowed_ids)); chosen={}
    with open(csvpath,newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            pid=str(row['patient_nbr'])
            if pid not in allowed: continue
            eid=str(row['encounter_id']); key=(int(eid),eid)
            if pid not in chosen or key<(int(chosen[pid]['encounter_id']),str(chosen[pid]['encounter_id'])):
                chosen[pid]=row
    if set(chosen)!=allowed: raise ValueError(f'expected {len(allowed)} records, got {len(chosen)}')
    df=pd.DataFrame.from_records(list(chosen.values()))
    if with_label:
        y=df[list(DIAG)].astype(str).apply(lambda c:c.str.strip().eq('428')).any(axis=1).astype('int8').to_numpy()
    else: y=None
    return df,y

def age_changed_ids(csvpath):
    """Counts/identity-only sensitivity membership census; never reads labels."""
    seen={}
    with open(csvpath,newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            pid=str(row['patient_nbr'])
            if pid in EXCLUDED_IDS: continue
            seen.setdefault(pid,set()).add(row['age'])
    return {pid for pid,ages in seen.items() if len(ages)>1}

def med_columns(cols):return sorted(set(cols)&MEDS)
def feature_cols(df, all_meds=False):
    cols=[c for c in df.columns if c not in DROP_ALWAYS]
    cols=[c for c in cols if c not in HF_PROXY]
    if all_meds: cols=[c for c in cols if c not in MEDS]
    # deterministic derived availability flags, not source features; computed without label.
    cols += ['age_missing','stay_missing']
    return cols

def prepare_X(df, cols):
    source_cols=[c for c in cols if c not in {'age_missing','stay_missing'}]
    x=df[source_cols].copy()
    for c in x.columns:
        x[c]=x[c].replace(list(MISSING),np.nan)
    if 'age' in x:
        age=x['age'].map(AGE_MAP)
        x['age_missing']=age.isna().astype(float)
        x['age']=age
    if 'time_in_hospital' in x: x['stay_missing']=pd.to_numeric(x['time_in_hospital'],errors='coerce').isna().astype(float)
    for c in NUMERIC:
        if c in x: x[c]=pd.to_numeric(x[c],errors='coerce')
    return x

def cat_cols(cols):return [c for c in CAT_BASE if c in cols]
def other_numeric(cols):return [c for c in NUMERIC if c in cols and c!='time_in_hospital']
def all_numeric(cols):return [c for c in NUMERIC if c in cols]

def encoder():return OneHotEncoder(handle_unknown='ignore')
def impute_cat():return Pipeline([('impute',SimpleImputer(strategy='constant',fill_value='__MISSING__')),('onehot',encoder())])
def impute_num():return Pipeline([('impute',SimpleImputer(strategy='median',add_indicator=True)),('scale',StandardScaler(with_mean=False))])
def spline_pipe():return Pipeline([('impute',SimpleImputer(strategy='median')),('spline',SplineTransformer(n_knots=2,degree=3,include_bias=False))])
def ensure_cols(cols, wanted):
    got=[c for c in wanted if c in cols]
    return got

def make_candidate(cols):
    cats=[c for c in cat_cols(cols) if c!='age']; nums=other_numeric(cols)
    transformers=[
      ('age_spline',spline_pipe(),['age']),
      ('stay_spline',spline_pipe(),['time_in_hospital']),
      ('age_missing',SimpleImputer(strategy='constant',fill_value=0),['age_missing']),
      ('stay_missing',SimpleImputer(strategy='constant',fill_value=0),['stay_missing']),
    ]
    if nums: transformers.append(('numeric',impute_num(),nums))
    if cats: transformers.append(('categorical',impute_cat(),cats))
    trans=ColumnTransformer(transformers,sparse_threshold=1.0)
    return Pipeline([('features',trans),('model',LogisticRegression(penalty='l1',C=.1,solver='saga',max_iter=1500,tol=1e-4,random_state=SEED,n_jobs=1))])
def make_lgbm(cols, drop_all_meds=False):
    cats=cat_cols(cols);nums=all_numeric(cols);transformers=[]
    if nums:transformers.append(('numeric',impute_num(),nums))
    if cats:transformers.append(('categorical',impute_cat(),cats))
    trans=ColumnTransformer(transformers,sparse_threshold=1.0)
    return Pipeline([('features',trans),('model',LGBMClassifier(**LGBM_PARAMS))])
def make_demographic(cols):
    cats=[c for c in ('gender','race') if c in cols]
    transformers=[('age',spline_pipe(),['age']),('age_missing',SimpleImputer(strategy='constant',fill_value=0),['age_missing'])]
    if cats:transformers.append(('categorical',impute_cat(),cats))
    trans=ColumnTransformer(transformers,sparse_threshold=1.0)
    return Pipeline([('features',trans),('model',LogisticRegression(penalty='l2',C=1.0,solver='liblinear',random_state=SEED))])

def folds_for_people(people, dev_ids):
    order=hash_order(dev_ids); f={pid:i%5 for i,pid in enumerate(order)}
    return np.asarray([f[str(p)] for p in people],dtype=int)
def new_model(name,cols):
    return {'candidate':make_candidate(cols),'lgbm':make_lgbm(cols),'demographic':make_demographic(cols)}[name]
def oof(df, y, dev_ids, cols, model_name, train_y=None):
    people=df['patient_nbr'].astype(str).to_numpy();fold=folds_for_people(people,dev_ids)
    target=np.asarray(y if train_y is None else train_y,dtype=int);pred=np.full(len(y),np.nan)
    for k in range(5):
        tr=np.flatnonzero(fold!=k);va=np.flatnonzero(fold==k)
        model=new_model(model_name,cols);model.fit(prepare_X(df.iloc[tr],cols)[cols],target[tr]);pred[va]=model.predict_proba(prepare_X(df.iloc[va],cols)[cols])[:,1]
    if not np.isfinite(pred).all():raise RuntimeError('OOF incomplete')
    return pred

def metric(y,p):
    pred=np.asarray(p)>=0.5; y=np.asarray(y,dtype=int)
    tp=int(np.sum(pred&(y==1)));fp=int(np.sum(pred&(y==0)));tn=int(np.sum((~pred)&(y==0)));fn=int(np.sum((~pred)&(y==1)))
    return {'roc_auc':float(roc_auc_score(y,p)),'average_precision':float(average_precision_score(y,p)),'brier':float(brier_score_loss(y,p)),'sensitivity_at_0.5':float(tp/(tp+fn)) if tp+fn else None,'specificity_at_0.5':float(tn/(tn+fp)) if tn+fp else None,'precision_at_0.5':float(tp/(tp+fp)) if tp+fp else None}
def perm_auc_smoke(df,y,dev_ids,cols):
    # One deterministic global permutation of DEV labels; evaluate every frozen model once.
    rng=np.random.default_rng(SEED); shuffled=rng.permutation(y)
    out={}
    for name in ('candidate','lgbm','demographic'):
        p=oof(df,y,dev_ids,cols,name,train_y=shuffled)
        out[name]={'auc_against_shuffled_labels':float(roc_auc_score(shuffled,p)),'auc_against_original_labels':float(roc_auc_score(y,p))}
    return out
def eval_models(train_df,train_y,test_df,test_y,names=('candidate','lgbm','demographic'),all_meds=False):
    cols=feature_cols(train_df,all_meds=all_meds)
    Xtr=prepare_X(train_df,cols);Xte=prepare_X(test_df,cols)
    out={};preds={}
    for name in names:
        model=new_model(name,cols)
        model.fit(Xtr[cols],train_y)
        preds[name]=model.predict_proba(Xte[cols])[:,1]
        out[name]=metric(test_y,preds[name])
    return out,preds,cols

def paired_bootstrap(y,preds,seed=SEED,n_boot=2000):
    rng=np.random.default_rng(seed); n=len(y); out={}
    candidate=preds['candidate']
    for name in ('lgbm','demographic'):
        ds=[]
        for _ in range(n_boot):
            ix=rng.integers(0,n,n)
            if len(np.unique(y[ix]))<2: continue
            ds.append(float(roc_auc_score(y[ix],candidate[ix])-roc_auc_score(y[ix],preds[name][ix])))
        out[name]={'valid_bootstraps':len(ds),'ci95':[float(np.quantile(ds,.025)),float(np.quantile(ds,.975))] if ds else [None,None]}
    return out

def peak_rss_kb():
    try:
        for l in Path('/proc/self/status').read_text().splitlines():
            if l.startswith('VmHWM:'):return int(l.split()[1])
    except Exception:pass
    return None
PRELOCK_STAGE_ORDER=[f"oof_{model}_fold{k}" for model in ("candidate","lgbm","demographic") for k in range(5)]+["headroom_gate"]+[f"perm_{model}_fold{k}" for model in ("candidate","lgbm","demographic") for k in range(5)]
def atomic_json(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,path)
def prelock_stage(csvpath,splitpath,stage,outdir):
    """One fold or deterministic gate per invocation; stage outputs are create-once atomic JSON."""
    if stage not in PRELOCK_STAGE_ORDER: raise SystemExit('unknown prelock stage')
    outdir=Path(outdir); target_path=outdir/(stage+'.json')
    if target_path.exists(): raise SystemExit('stage output already exists; refusing rerun')
    m=json.loads(Path(splitpath).read_text());dev=m['dev_ids']
    df,y=load_partition(csvpath,dev,with_label=True);cols=feature_cols(df)
    if stage=='headroom_gate':
        preds={}
        for model in ('candidate','lgbm','demographic'):
            arr=np.full(len(y),np.nan)
            for k in range(5):
                path=outdir/(f'oof_{model}_fold{k}.json')
                if not path.exists():raise SystemExit('missing OOF stage: '+path.name)
                rec=json.loads(path.read_text())
                ix={str(pid):float(score) for pid,score in rec['predictions']}
                for i,pid in enumerate(df.patient_nbr.astype(str)):
                    if pid in ix: arr[i]=ix[pid]
            if not np.isfinite(arr).all():raise SystemExit('OOF folds incomplete')
            preds[model]=arr
        mets={name:metric(y,pred) for name,pred in preds.items()}
        best=max(mets['lgbm']['roc_auc'],mets['demographic']['roc_auc'])
        comparator='lgbm' if mets['lgbm']['roc_auc']>=mets['demographic']['roc_auc']-.001 else 'demographic'
        drop=bool(best>=.94 or best<=.5)
        result={'stage':stage,'n':len(y),'positive':int(y.sum()),'negative':int(len(y)-y.sum()),'models':mets,'delta_candidate_minus_best_comparator_auc':float(mets['candidate']['roc_auc']-best),'win_threshold':.03,'win':bool(mets['candidate']['roc_auc']-best>=.03),'comparator_tie_epsilon_auc':.001,'locked_best_comparator':comparator,'best_comparator_auc':mets[comparator]['roc_auc'],'headroom_to_ceiling':1.-best,'drop_if_within_2x_win_of_ceiling':bool(best>=.94),'drop_no_skill':bool(best<=.5),'drop_gate':drop}
        atomic_json(target_path,result);return result
    is_perm=stage.startswith('perm_'); _,model,fold_s=stage.split('_');k=int(fold_s.replace('fold',''))
    people=df.patient_nbr.astype(str).to_numpy();folds=folds_for_people(people,dev)
    tr=np.flatnonzero(folds!=k);va=np.flatnonzero(folds==k)
    train_y=np.random.default_rng(SEED).permutation(y) if is_perm else y
    mdl=new_model(model,cols);xtr=prepare_X(df.iloc[tr],cols)[cols];xva=prepare_X(df.iloc[va],cols)[cols]
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        mdl.fit(xtr,train_y[tr]);probs=mdl.predict_proba(xva)[:,1]
    warns=[{'category':w.category.__name__,'message':str(w.message)} for w in ws]
    result={'stage':stage,'model':model,'fold':k,'permutation':is_perm,'n_train':len(tr),'n_validation':len(va),'convergence_warnings':warns,'predictions':[[str(people[i]),float(probs[j])] for j,i in enumerate(va)]}
    atomic_json(target_path,result);return {'stage':stage,'n_train':len(tr),'n_validation':len(va),'convergence_warnings':warns,'output':str(target_path)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',required=True);p.add_argument('--mode',choices=['split','prelock-dev','final'],default='split');p.add_argument('--split-manifest',default='/tmp/unit191/split_manifest.json');p.add_argument('--output',default='/tmp/unit191/results.json');p.add_argument('--prereg',default='/tmp/unit191/PREREG.md');p.add_argument('--expected-prereg-sha256');p.add_argument('--expected-run-sha256');p.add_argument('--locked-comparator',choices=['lgbm','demographic']);p.add_argument('--allow-prelock-window',action='store_true');p.add_argument('--prelock-stage');p.add_argument('--stage-dir',default='/tmp/unit191/prelock_stages');a=p.parse_args()
    if a.mode=='prelock-dev' and a.prelock_stage:
        if not a.allow_prelock_window: raise SystemExit('requires explicit --allow-prelock-window')
        print(json.dumps(prelock_stage(a.csv,a.split_manifest,a.prelock_stage,a.stage_dir),indent=2));return
    if a.mode=='split':
        m=make_and_write_manifest(a.csv,a.split_manifest)
        print(json.dumps({'n_eligible':m['n_eligible'],'n_dev':m['n_dev'],'n_test':m['n_test'],'split_manifest_sha256':sha(a.split_manifest)}));return
    if not Path(a.split_manifest).exists():raise SystemExit('frozen split manifest missing')
    m=json.loads(Path(a.split_manifest).read_text())
    first=selected_ids_from_source(a.csv);expected_dev,expected_test=split_ids(first)
    if m.get('dev_ids')!=expected_dev or m.get('test_ids')!=expected_test:raise SystemExit('frozen split does not match source census')
    dev,test=m['dev_ids'],m['test_ids']
    if a.mode=='prelock-dev' and not a.allow_prelock_window:raise SystemExit('requires explicit --allow-prelock-window')
    if a.mode=='final':
        if not a.expected_prereg_sha256 or not a.expected_run_sha256:raise SystemExit('final requires locked hashes from parent')
        if sha(a.prereg)!=a.expected_prereg_sha256 or sha(__file__)!=a.expected_run_sha256:raise SystemExit('lock hash mismatch')
        if not a.locked_comparator: raise SystemExit('final requires prereg-locked DEV comparator name')
        evalids=test; trainids=dev
    else: evalids=dev;trainids=dev
    # A single partition pass: TEST labels are never collected in prelock mode.
    data,y=load_partition(a.csv,evalids,with_label=True)
    cols=feature_cols(data)
    if a.mode=='prelock-dev':
        outputs={'n':len(y),'positive':int(y.sum()),'negative':int(len(y)-y.sum()),'models':{},'permutation_smoke':None,'dev_gate':None}
        scores={}
        for name in ('candidate','lgbm','demographic'):
            scores[name]=oof(data,y,dev,cols,name)
            outputs['models'][name]=metric(y,scores[name])
        best=max(outputs['models']['lgbm']['roc_auc'],outputs['models']['demographic']['roc_auc'])
        d=outputs['models']['candidate']['roc_auc']-best
        outputs['delta_candidate_minus_best_comparator_auc']=float(d)
        outputs['win_threshold']=.03;outputs['win']=bool(d>=.03)
        eps=.001
        outputs['comparator_tie_epsilon_auc']=eps
        outputs['locked_best_comparator']='lgbm' if outputs['models']['lgbm']['roc_auc']>=outputs['models']['demographic']['roc_auc']-eps else 'demographic'
        outputs['best_comparator_auc']=outputs['models'][outputs['locked_best_comparator']]['roc_auc']
        outputs['headroom_to_ceiling']=1.0-best
        outputs['drop_if_within_2x_win_of_ceiling']=bool(best>=.94)
        outputs['drop_no_skill']=bool(best<=.5)
        # one fixed DEV-only permutation smoke, every prespecified model
        outputs['permutation_smoke']=perm_auc_smoke(data,y,dev,cols)
        outputs['peak_rss_kb']=peak_rss_kb()
        outputs['stage']='one-time pre-lock DEV outcome window; after recording these values in prereg, lock and seal targets'
    else:
        # Final: fit DEV once per fixed model and score held TEST once.
        devdf,yd=load_partition(a.csv,dev,with_label=True)
        testdf,yt=load_partition(a.csv,test,with_label=True)
        outputs={'n_test':len(yt),'positive':int(yt.sum()),'negative':int(len(yt)-yt.sum()),'models':{},'sensitivities':{}}
        outputs['models'],preds,cols=eval_models(devdf,yd,testdf,yt)
        best_name=a.locked_comparator
        best=outputs['models'][best_name]['roc_auc']
        delta=outputs['models']['candidate']['roc_auc']-best
        outputs['best_comparator']=best_name
        outputs['delta_candidate_minus_best_comparator_auc']=float(delta);outputs['win_threshold']=.03;outputs['win']=bool(delta>=.03)
        outputs['paired_patient_bootstrap_delta_ci95']=paired_bootstrap(yt,preds)
        # Sensitivity A: drop all age-bin-change IDs in their original partition; do not rehash/reroll.
        changed=age_changed_ids(a.csv)
        dev_keep=np.asarray([str(x) not in changed for x in devdf.patient_nbr])
        test_keep=np.asarray([str(x) not in changed for x in testdf.patient_nbr])
        dev_age=devdf.loc[dev_keep].reset_index(drop=True); ydev_age=yd[dev_keep]
        test_age=testdf.loc[test_keep].reset_index(drop=True); ytest_age=yt[test_keep]
        age_out,age_preds,_=eval_models(dev_age,ydev_age,test_age,ytest_age)
        outputs['sensitivities']['age_bin_change_excluded']={'changed_ids_excluded_from_dev':int((~dev_keep).sum()),'changed_ids_excluded_from_test':int((~test_keep).sum()),'models':age_out,'candidate_minus_lgbm_auc':float(age_out['candidate']['roc_auc']-age_out['lgbm']['roc_auc']),'candidate_minus_demographic_auc':float(age_out['candidate']['roc_auc']-age_out['demographic']['roc_auc'])}
        # Sensitivity B: remove all 23 medication columns from every model.
        outputs['sensitivities']['all_23_medications_excluded'],med_preds,medcols=eval_models(devdf,yd,testdf,yt,all_meds=True)
        outputs['sensitivities']['all_23_medications_excluded']['candidate_minus_lgbm_auc']=float(outputs['sensitivities']['all_23_medications_excluded']['candidate']['roc_auc']-outputs['sensitivities']['all_23_medications_excluded']['lgbm']['roc_auc'])
        outputs['sensitivities']['all_23_medications_excluded']['candidate_minus_demographic_auc']=float(outputs['sensitivities']['all_23_medications_excluded']['candidate']['roc_auc']-outputs['sensitivities']['all_23_medications_excluded']['demographic']['roc_auc'])
        outputs['age_change_ids_n_fullcohort']=len(changed)
        outputs['paired_per_patient_deltas']=[{'patient_nbr':str(testdf.patient_nbr.iloc[i]),'target':int(yt[i]),'candidate_score':float(preds['candidate'][i]),'lgbm_score':float(preds['lgbm'][i]),'demographic_score':float(preds['demographic'][i]),'candidate_minus_lgbm_brier_contribution':float((preds['candidate'][i]-yt[i])**2-(preds['lgbm'][i]-yt[i])**2),'candidate_minus_demographic_brier_contribution':float((preds['candidate'][i]-yt[i])**2-(preds['demographic'][i]-yt[i])**2)} for i in range(len(yt))]
        # TEST label permutation happens only in this final single-pass runner, fixed predictions.
        shuffled=np.random.default_rng(SEED).permutation(yt)
        outputs['sealed_test_permutation']={name:{'auc_against_shuffled_TEST_labels':float(roc_auc_score(shuffled,preds[name])),'fixed_model_predictions':True} for name in preds}
        outputs['peak_rss_kb']=peak_rss_kb();outputs['stage']='final locked TEST run; sensitivity analyses and TEST-label permutation occur once here'
    result={'unit':191,'dataset':'UCI 296','mode':a.mode,'source_csv_bytes':Path(a.csv).stat().st_size,'source_csv_sha256':sha(a.csv),'split_manifest_sha256':sha(a.split_manifest),'n_dev':len(dev),'n_test':len(test),'result':outputs}
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
