#!/usr/bin/env python3
"""Unit 186 frozen pipeline; no TEST evaluation is implemented by design.

Outcome computation, if run, is DEV-only. TEST subjects are held aside before
loading their EDF/annotations. Hash of this script and PREREG.md must be recorded
before any future TEST outcomes are computed.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os
from pathlib import Path
import numpy as np
import pandas as pd
import pywt
import scipy.stats as stats
from mne_features.feature_extraction import extract_features
from mne_bids import BIDSPath, read_raw_bids
from antropy import hjorth_params, sample_entropy
from sklearn.model_selection import GroupKFold
from sklearn.metrics import average_precision_score, roc_auc_score
from lightgbm import LGBMClassifier

SEED=42
SEEDS_SENSITIVITY=(17,29)
EPOCH_S=0.25
RATE=1000
MAX_LEVEL=5
LAGS=(1,2,4,8,16,32)
HARD_NEG_TOL=0.25
TEST_IDS=frozenset({'sub-09','sub-12','sub-02','sub-19','sub-04'})
BASE_FEATURES=['teager_kaiser_energy_1_std','teager_kaiser_energy_2_std','ptp_amp','hjorth_mobility','hjorth_complexity','teager_kaiser_energy_3_std','teager_kaiser_energy_5_mean','teager_kaiser_energy_0_std','kurtosis','teager_kaiser_energy_1_mean','teager_kaiser_energy_5_std','samp_entropy','chan_ptp','chan_kurt']


def subject_id_hash(s): return hashlib.sha256(s.encode()).hexdigest()
def split_subjects(ids):
    ordered=sorted(ids,key=lambda s:(subject_id_hash(s),s))
    assert len(ordered)==25 and set(ordered[:5])==TEST_IDS
    return ordered[5:],ordered[:5]

def haar_features(epoch):
    x=np.asarray(epoch,dtype=np.float64)
    if x.shape != (250,): raise ValueError('expected 250 samples')
    x=x-x.mean(); sd=x.std()
    x=x/sd if np.isfinite(sd) and sd>0 else np.zeros_like(x)
    coeffs=pywt.wavedec(x,'haar',mode='symmetric',level=MAX_LEVEL)
    # pywt returns [A5,D5,D4,D3,D2,D1]; energy is mean squared coefficient.
    energies=[float(np.mean(c*c)) if len(c) else 0.0 for c in coeffs]
    ac=[]
    for lag in LAGS:
        if x.std()==0: ac.append(0.0)
        else: ac.append(float(np.dot(x[:-lag],x[lag:]) / np.dot(x,x)))
    return np.asarray(energies+ac,dtype=np.float64)

def comparator_features(epochs, channel_ptp, channel_kurt, sfreq=RATE):
    epochs=np.asarray(epochs,dtype=np.float64)
    mob,comp=hjorth_params(epochs,axis=1)
    frame=pd.DataFrame({'kurtosis':stats.kurtosis(epochs,axis=1),'hjorth_mobility':mob,'hjorth_complexity':comp,'ptp_amp':np.ptp(epochs,axis=1),'samp_entropy':np.array([sample_entropy(x) for x in epochs])})
    raw=extract_features(epochs[:,None,:],sfreq,['teager_kaiser_energy'],return_as_df=True)
    raw.columns=[name[0]+'_'+name[1].replace('ch0_','') for name in raw.columns]
    frame=pd.concat([frame,raw],axis=1)
    frame['chan_ptp']=channel_ptp;frame['chan_kurt']=channel_kurt
    return frame[BASE_FEATURES].replace([np.inf,-np.inf],np.nan).fillna(0.0).to_numpy()

def candidate_features(epochs, channel_ptp, channel_kurt):
    e=np.asarray([haar_features(x) for x in epochs])
    return np.column_stack([e,np.full(len(e),channel_ptp),np.full(len(e),channel_kurt)])

def read_subject(root,sid):
    """Read one subject only; caller must exclude TEST from DEV run."""
    root=Path(root); edf=root/sid/'ieeg'/f'{sid}_task-sleep_ieeg.edf'
    ann=root/'derivatives'/f'{sid}_task-sleep_events_interpretation.tsv'
    raw=read_raw_bids(BIDSPath(subject=sid[4:],task='sleep',root=str(root),datatype='ieeg'),verbose='ERROR')
    sfreq=raw.info['sfreq']
    if sfreq != RATE: raise ValueError(f'{sid}: expected 1kHz got {sfreq}')
    annotations=pd.read_csv(ann,sep='\t')
    event_rows=[]
    for row in annotations.itertuples(index=False):
        onset=float(row.time_in_sec); chs=str(row.chans).split()
        for ch in chs: event_rows.append({'subject':sid,'onset':onset,'channel':ch,'event':len(event_rows)})
    ann_channels=sorted(set(e['channel'] for e in event_rows))
    missing=set(ann_channels)-set(raw.ch_names)
    if missing: raise ValueError(f'{sid}: annotated missing channels {sorted(missing)}')
    raw.pick_channels(ann_channels,ordered=True)
    raw.load_data()
    signal={name:raw.get_data(picks=[name])[0] for name in raw.ch_names}
    # Only annotation-bearing channels are supervised; other channels never negative.
    ann_by_ch={c:[] for c in sorted(set(e['channel'] for e in event_rows))}
    for ev in event_rows: ann_by_ch[ev['channel']].append(ev['onset'])
    # Recompute feature matrices in exact same row traversal order
    Xb=[];Xc=[];pos_flags=[];neg_eligible=[];row_key=[]
    for ch,onsets in ann_by_ch.items():
        full=signal[ch];mu=full.mean();sd=full.std();norm=(full-mu)/sd if sd>0 else np.zeros_like(full)
        cp=float(np.ptp(norm));ck=float(stats.kurtosis(norm));n=max(0,len(norm)-4*250);n=(n//250)*250
        ss=np.arange(0,n,250,dtype=int);ep=np.stack([norm[s:s+250] for s in ss]) if len(ss) else np.empty((0,250))
        if not len(ep):continue
        Xb.extend(comparator_features(ep,cp,ck,sfreq));Xc.extend(candidate_features(ep,cp,ck))
        pset={int(o//EPOCH_S) for o in onsets if 0<=int(o//EPOCH_S)<len(ep)}
        ex={j for j,start in enumerate(ss/RATE) if any(abs(start-o)<=HARD_NEG_TOL+1e-12 for o in onsets)}
        pos_flags.extend([int(j in pset) for j in range(len(ep))])
        neg_eligible.extend([int(j not in pset and j not in ex) for j in range(len(ep))])
        row_key.extend([(sid,ch,j,float(s/RATE)) for j,s in enumerate(ss)])
    return {'X_base':np.asarray(Xb),'X_candidate':np.asarray(Xc),'y':np.asarray(pos_flags,dtype=np.int8),'negative_eligible':np.asarray(neg_eligible,dtype=bool),'groups':np.asarray([r[0] for r in row_key]),'channels':np.asarray([r[1] for r in row_key]),'epoch_ids':np.asarray([r[2] for r in row_key]),'starts':np.asarray([r[3] for r in row_key]),'events':event_rows}

def make_event_table(scores,data,sid):
    # scores row-aligned with concatenated annotation-bearing channel epochs.
    lookup={(str(g),str(c),int(e)):float(p) for g,c,e,p in zip(data['groups'],data['channels'],data['epoch_ids'],scores)}
    ann_file=data['_ann_path'];anns=pd.read_csv(ann_file,sep='\t');out=[]
    for r in anns.itertuples(index=False):
        idx=int(float(r.time_in_sec)//EPOCH_S); chs=str(r.chans).split(); vals=[]
        for c in chs:
            key=(sid,c,idx)
            if key in lookup: vals.append(lookup[key])
        if vals:out.append((max(vals),1,sid,float(r.time_in_sec)))
    return out

def train_predict(Xtrain,ytrain,Xeval,seed=SEED):
    # Undersample only the training partition; no validation/test resampling.
    keep=np.flatnonzero((ytrain==1))
    neg=np.flatnonzero((ytrain==0))
    if len(keep)==0 or len(neg)==0:raise ValueError('training needs both classes')
    rng=np.random.default_rng(seed);neg=rng.choice(neg,size=min(len(neg),len(keep)),replace=False)
    ix=np.concatenate([keep,neg]);rng.shuffle(ix)
    model=LGBMClassifier(boosting_type='gbdt',num_leaves=31,max_depth=-1,learning_rate=0.1,n_estimators=100,subsample_for_bin=200000,min_split_gain=0.0,min_child_weight=1e-3,min_child_samples=20,subsample=1.0,subsample_freq=0,colsample_bytree=1.0,reg_alpha=0.0,reg_lambda=0.0,random_state=seed,n_jobs=1,verbosity=-1)
    model.fit(Xtrain[ix],ytrain[ix])
    return model.predict_proba(Xeval)[:,1],model

def oof_predictions(X, train_labels, negative_eligible, groups, seed):
    scores=np.full(len(train_labels),np.nan)
    for tr,va in GroupKFold(n_splits=5).split(X,train_labels,groups):
        train_ok=(train_labels[tr]==1)|negative_eligible[tr]
        tr=tr[train_ok]
        p,_=train_predict(X[tr],train_labels[tr],X[va],seed)
        scores[va]=p
    if not np.isfinite(scores).all(): raise ValueError('missing DEV OOF score')
    return scores

def score_metrics(scores, labels, negative_eligible, groups, channels, epoch_ids, base, dev_ids):
    events=[]; missed=0; center_events={}
    for sid in dev_ids:
        ann=pd.read_csv(base/'derivatives'/f'{sid}_task-sleep_events_interpretation.tsv',sep='\t')
        meta=json.loads((base/sid/'ieeg'/f'{sid}_task-sleep_ieeg.json').read_text()); center=str(meta['InstitutionName'])
        ix=np.flatnonzero(groups==sid)
        lookup={(str(channels[i]),int(epoch_ids[i])):float(scores[i]) for i in ix}
        for r in ann.itertuples(index=False):
            idx=int(float(r.time_in_sec)//EPOCH_S)
            vals=[lookup[(c,idx)] for c in str(r.chans).split() if (c,idx) in lookup]
            if vals: events.append(max(vals));center_events.setdefault(center,[]).append(max(vals))
            else: missed+=1
    negidx=np.flatnonzero(negative_eligible)
    metric_y=np.asarray([1]*len(events)+[0]*len(negidx))
    metric_p=np.asarray(events+scores[negidx].tolist())
    feasible=[]
    for threshold in np.unique(metric_p):
        predicted=metric_p>=threshold
        precision=float(metric_y[predicted].sum()/predicted.sum())
        if precision>=0.80:feasible.append((int(metric_y[predicted].sum()),float(threshold),precision))
    if feasible:
        tp,threshold,achieved=max(feasible,key=lambda z:(z[0],-z[1]))
        sensitivity=float(tp/len(events)) if events else float('nan')
        threshold_record={'target_precision':0.80,'threshold':threshold,'achieved_precision':achieved,'event_sensitivity':sensitivity,'status':'achievable'}
        center_sensitivity={c:float(np.sum(np.asarray(v)>=threshold)/len(v)) for c,v in center_events.items() if v}
    else:
        threshold_record={'target_precision':0.80,'status':'not achievable'};center_sensitivity={c:None for c in center_events}
    return {'event_positive_count':len(events),'event_rows_without_scoring_epoch':missed,'negative_window_count':len(negidx),'average_precision':float(average_precision_score(metric_y,metric_p)),'roc_auc':float(roc_auc_score(metric_y,metric_p)),'sensitivity_at_0.80_precision':threshold_record,'per_center_event_sensitivity_at_same_threshold':center_sensitivity}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bids-root',required=True);ap.add_argument('--mode',choices=['audit','dev'],default='audit');ap.add_argument('--output',default='unit186_dev_metrics.json');args=ap.parse_args()
    base=Path(args.bids_root)
    ids=sorted(p.name for p in base.glob('sub-*') if p.is_dir())
    dev_ids,test_ids=split_subjects(ids)
    print(json.dumps({'dev_ids':dev_ids,'sealed_test_ids':test_ids,'split_rule':'SHA256 literal subject ID ascending, first five TEST; no stratification/reroll'}))
    if args.mode=='audit': return
    # DEV-only read. Test subjects' files are not loaded by this branch.
    data={sid:read_subject(base,sid) for sid in dev_ids}
    # Concatenate, then fixed subject-group five-fold OOF predictions.
    arrays={key:np.concatenate([data[s][key] for s in dev_ids],axis=0) for key in ('X_base','X_candidate','y','negative_eligible','groups','channels','epoch_ids','starts')}
    result={'split':{'dev':dev_ids,'test_sealed':test_ids},'primary':'event AP; +0.03 candidate minus comparator win bar','oof':{}}
    scored={}
    for name,key in [('comparator','X_base'),('candidate','X_candidate')]:
        scores=oof_predictions(arrays[key],arrays['y'],arrays['negative_eligible'],arrays['groups'],SEED)
        scored[name]=scores
        result['oof'][name]=score_metrics(scores,arrays['y'],arrays['negative_eligible'],arrays['groups'],arrays['channels'],arrays['epoch_ids'],base,dev_ids)
    delta=result['oof']['candidate']['average_precision']-result['oof']['comparator']['average_precision']
    result['oof']['candidate_minus_comparator_ap']=float(delta)
    result['oof']['win_bar_0.03_met']=bool(delta>=0.03)
    # Predeclared seed sensitivity only if primary-seed absolute AP gain is under 0.01.
    if abs(delta)<0.01:
        sens={}
        for seed in SEEDS_SENSITIVITY:
            pair={}
            for name,key in [('comparator','X_base'),('candidate','X_candidate')]:
                scores=oof_predictions(arrays[key],arrays['y'],arrays['negative_eligible'],arrays['groups'],seed)
                pair[name]=score_metrics(scores,arrays['y'],arrays['negative_eligible'],arrays['groups'],arrays['channels'],arrays['epoch_ids'],base,dev_ids)['average_precision']
            sens[str(seed)]={'comparator_ap':pair['comparator'],'candidate_ap':pair['candidate'],'delta_ap':pair['candidate']-pair['comparator']}
        result['seed_sensitivity']=sens
    # One label-shuffle smoke check: preserve positive counts within patient-channel groups.
    perm_rng=np.random.default_rng(18642); perm_y=arrays['y'].copy()
    group_keys=np.asarray([f'{g}::{c}' for g,c in zip(arrays['groups'],arrays['channels'])])
    for group in np.unique(group_keys):
        ix=np.flatnonzero(group_keys==group); perm_y[ix]=perm_rng.permutation(perm_y[ix])
    permutation={}
    for name,key in [('comparator','X_base'),('candidate','X_candidate')]:
        ps=oof_predictions(arrays[key],perm_y,arrays['negative_eligible'],arrays['groups'],SEED)
        permutation[name]=score_metrics(ps,arrays['y'],arrays['negative_eligible'],arrays['groups'],arrays['channels'],arrays['epoch_ids'],base,dev_ids)['average_precision']
    result['permutation_smoke']={'seed':18642,'within_patient_channel_positive_counts_preserved':True,'comparator_ap_against_original_dev_events':permutation['comparator'],'candidate_ap_against_original_dev_events':permutation['candidate'],'interpretation':'diagnostic only, not inferential'}
    result['warning']='Development-only exploratory headroom; no TEST outcomes computed. This script does not implement TEST evaluation.'
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
