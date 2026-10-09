"""Original-bound skip without candidate expected generation or audit."""
import importlib.util
from pathlib import Path
from model import Invalid,integer
spec=importlib.util.spec_from_file_location('t14_immutable_t13_parent',Path(__file__).resolve().parent.parent/'t13/proof.py');baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
prior=baseline.prior;original=baseline.original;original_t7_proof=baseline.original_t7_proof
scenario_check=baseline.scenario_check;incumbent_check=baseline.incumbent_check;charged_check=baseline.charged_check;candidates_check=baseline.candidates_check
canonical=baseline.canonical
BASE_COUNTERS=baseline.BASE_COUNTERS
METHOD=baseline.METHOD|{'candidate_activation'};WRAPPER=baseline.WRAPPER

def check(s,payload,certificate=True):
    if type(payload) is not dict or set(payload) not in (METHOD,METHOD|WRAPPER):raise Invalid('exact T14 method or wrapper stages')
    branch=payload['candidate_activation']
    if type(branch) is not str or branch not in ('exposure_exit','original_bound_equality','candidates_activated'):raise Invalid('typed candidate activation')
    q=dict(payload);del q['candidate_activation']
    if branch!='original_bound_equality':
        baseline.check(s,q)
        if branch=='exposure_exit':
            if not q['certificate']['early_exit']:raise Invalid('candidate exposure exit mismatch')
        else:
            if q['certificate']['early_exit']:raise Invalid('candidate activated early mismatch')
            originalW=q['incumbent_original_upper'];oldL=q['certificate']['old_lower']
            if not oldL<originalW:raise Invalid('candidate activation requires original strict gap')
        return
    # No scalar expected constructor or candidate audit, no charged expectation.
    if q['candidate_ledger'] is not None or q['selected_candidate'] is not None or q['activation']!='old_bound_equality':raise Invalid('intentional typed absent ledger/index and downstream branch')
    original=prior.incumbent_expected(s);W=incumbent_check(s,original)
    if type(q['incumbent_original_upper']) is not int or type(q['incumbent_selected_upper']) is not int or q['incumbent_original_upper']!=W or q['incumbent_selected_upper']!=W or canonical(q['incumbent'])!=canonical(original) or canonical(q['route'])!=canonical(original):raise Invalid('skipped selected/original W SAME original indexed route')
    if type(q['counters']) is not dict or set(q['counters'])!=baseline.BASE_COUNTERS|baseline.NEW_COUNTERS or type(q['counters']['scalar_candidate_inspections']) is not int or q['counters']['scalar_candidate_inspections']!=0:raise Invalid('skipped scalar count exact zero')
    additions=('candidate_ledger','incumbent_original_upper','incumbent_selected_upper','selected_candidate')
    t12payload={k:v for k,v in q.items() if k not in additions};t12payload['counters']={k:v for k,v in q['counters'].items() if k!='scalar_candidate_inspections'}
    baseline.baseline.check(s,t12payload)
