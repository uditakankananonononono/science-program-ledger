"""Lazy branch audit; distinct immutable repaired T11 baseline parent module."""
import importlib.util,json
from pathlib import Path
from model import Invalid,integer
spec=importlib.util.spec_from_file_location('t12_parent_unchanged_t11',Path(__file__).resolve().parent.parent/'t11/proof.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
original=prior.original;original_t7_proof=prior.original_t7_proof
scenario_check=prior.scenario_check;incumbent_check=prior.incumbent_check
charged_check=prior.charged_check;BASE_COUNTERS=prior.BASE_COUNTERS;NEW_COUNTERS=prior.NEW_COUNTERS
canonical=prior.canonical
METHOD={'route','counters','proof','certificate','scenario_proof','incumbent','charged_proof','bound_trace','activation'}
WRAPPER={'status','solve_seconds','build_seconds','rss_kib','affinity','as_limit_bytes','identity'}
def check(s,payload,certificate=True):
    if type(payload) is not dict or set(payload) not in (METHOD,METHOD|WRAPPER):raise Invalid('exact lazy method or wrapper schema')
    activation=payload['activation']
    if type(activation) is not str or activation not in ('exposure_exit','old_bound_equality','charged_bound'):raise Invalid('typed activation')
    q=dict(payload);del q['activation']
    if activation!='old_bound_equality':
        prior.check(s,q)
        if activation=='exposure_exit':
            if not q['certificate']['early_exit']:raise Invalid('lazy exposure branch')
        else:
            if q['certificate']['early_exit'] or not q['certificate']['old_lower']<q['certificate']['upper']:raise Invalid('lazy charged activation must old gap')
        return
    # No charged calculation or charged expected ledger on the skipped branch.
    if q['charged_proof'] is not None or q['bound_trace']!=[]:raise Invalid('absent charged branch ledger')
    counters=q['counters']
    if type(counters) is not dict or set(counters)!=BASE_COUNTERS|NEW_COUNTERS:raise Invalid('lazy full typed counters')
    for value in counters.values():integer(value)
    if any(counters[k]!=0 for k in NEW_COUNTERS):raise Invalid('lazy charged zero counts')
    c=q['certificate'];fields={'early_exit','equality_exit','reason','budget','lower','upper','old_lower','charged_lambda','source_bound_stronger'}
    if type(c) is not dict or set(c)!=fields or type(c['charged_lambda']) is not int or c['charged_lambda']!=1 or type(c['old_lower']) is not int or type(c['source_bound_stronger']) is not bool or c['source_bound_stronger']:raise Invalid('lazy exact certificate schema')
    baseline_cert={k:v for k,v in c.items() if k not in ('old_lower','charged_lambda','source_bound_stronger')}
    b=dict(q,certificate=baseline_cert,counters={k:v for k,v in counters.items() if k in BASE_COUNTERS})
    prior.baseline.check(s,b)
    ds=q['scenario_proof']['distances'];old=max(row[0] for row in ds)
    if c['early_exit'] or not c['equality_exit'] or c['old_lower']!=old or c['lower']!=old or c['upper']!=old:raise Invalid('old audited L equals actual W')
    if canonical(q['incumbent'])!=canonical(prior.incumbent_expected(s)):raise Invalid('lazy identical exposure incumbent')
    prior.preprocessing_check(s,q,False)
