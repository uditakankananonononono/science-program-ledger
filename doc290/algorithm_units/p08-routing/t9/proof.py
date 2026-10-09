"""Re-derive original ledgers/witness before classifying equality metadata."""
import importlib.util
from pathlib import Path
from model import Invalid,model,MAX
spec=importlib.util.spec_from_file_location('t9_original_t8_proof',Path(__file__).resolve().parent.parent/'t8'/'proof.py');original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
scenario_check=original.scenario_check
incumbent_check=original.incumbent_check
original_t7_proof=original.original

def check(s,payload,certificate=True):
    original_t7_proof.check(s,payload,certificate=False)
    if not certificate:return
    c=payload.get('certificate')
    if type(c) is not dict or set(c)!={'early_exit','equality_exit','reason','budget','lower','upper'} or type(c['early_exit']) is not bool or type(c['equality_exit']) is not bool or type(c['budget']) is not int or c['budget']!=s['budget'] or type(c['reason']) is not str:raise Invalid('T9 certificate schema')
    minimum=payload['proof']['start_minimum'];early=minimum is None or minimum>s['budget']
    if c['early_exit']!=early:raise Invalid('T9 exposure early flag')
    phase=('candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue','objective_bound_pruned')
    if early:
        reason='no_allowed_turn_path' if minimum is None else 'budget_infeasible'
        if c['equality_exit'] or c['reason']!=reason or c['lower'] is not None or c['upper'] is not None or payload['route'] is not None or payload.get('scenario_proof') is not None or payload.get('incumbent') is not None:raise Invalid('T9 infeasible metadata')
        for k in (*phase,'scenario_reverse_inspections','incumbent_inspections'):
            if payload['counters'][k]!=0:raise Invalid('T9 infeasible counters')
        return
    scenario_check(s,payload.get('scenario_proof'));W=incumbent_check(s,payload.get('incumbent'))
    source=[row[0] for row in payload['scenario_proof']['distances']]
    if any(x is None for x in source):raise Invalid('T9 feasible scenario None')
    L=max(source)
    if L>W:raise Invalid('T9 lower above upper')
    if type(c['lower']) is not int or type(c['upper']) is not int or c['lower']!=L or c['upper']!=W:raise Invalid('T9 exact lower/upper')
    equal=L==W;reason='equality_exit' if equal else 'strict_gap_search'
    if c['equality_exit']!=equal or c['reason']!=reason:raise Invalid('T9 equality flag/reason')
    if payload['route'] is None:raise Invalid('T9 feasible None')
    # Validate returned route as well; do not use dict equality for bool-equal indices.
    original.incumbent_check(s,payload['route'])
    if equal:
        if payload['route']!=payload['incumbent']:raise Invalid('T9 equality must return incumbent')
        for k in phase:
            if payload['counters'][k]!=0:raise Invalid('T9 equality phase counter')
