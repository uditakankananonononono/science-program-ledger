#!/usr/bin/env python3
"""abbench: P02-03 - how reliable is the parent's sequence-only antibody design chain?
Locked before results (lock evidence = commit adding this file; smoke test uses 1AHW only and 1AHW is
excluded from the test set, so no test-set result exists before the lock).

PARENT CHAIN: ProABC-2 paratope + MODELLER + MD + HADDOCK. Substituted (locked amendments below).
TEST SET (locked rule, applied by this script, deterministic):
  From data/sabdab_nr.csv (SAbDab all-summary downloaded 2026-09-24, filtered: protein antigen,
  resolution <= 2.8, H and L and single antigen chain, one row per unique CDR-H3, sorted by pdb4).
  EXCLUDE 1AHW (smoke test). Iterate in pdb4 order; skip a complex only when:
  (a) RCSB PDB file missing, (b) antigen chain < 30 or > 400 residues, (c) ANARCI numbering fails,
  (d) ImmuneBuilder or LightDock setup fails. Stop when 24 complexes have a completed modeled-Fv dock.
  N target = 24 (amendment from >= 200: 2-core / 2 GB VM budget).
ARMS: (1) modeled Fv (ImmuneBuilder ABodyBuilder2, UNREFINED models - openmm/pdbfixer unavailable);
      (2) control: crystal Fv excised from the native PDB, same docking budget -> isolates docking
      error from modeling error (stage attribution, G3).
DOCKING (locked): LightDock 0.9.4 rigid body, receptor = native antigen chain, 40 swarms, 100
  glowworms, 100 steps, default fastdfire, 2 cores. Top-1 pose by LightDock score across swarms.
SCORING: DockQ 2.1.3 (antibody chains H,L vs antigen) of the docked model vs the native complex.
  Modeling stage metrics: whole-Fv Calpha RMSD (sequence-aligned) and CDR-H3 Calpha RMSD after
  framework (IMGT 1-104) superposition; ANARCI IMGT numbering on model and native.
GATES (locked, evaluated once):
  G1: DockQ distribution over the N completed complexes reported with bootstrap CI (10k, seed 0);
      PASS iff median DockQ >= 0.23 on the modeled arm. N and any shortfall reported; if N < 12 the
      gate is reported NOT EVALUABLE (compute blocker), not failed.
  G2: affinity ranking on data/skempi_ab.csv (SKEMPI 2.0, 2026-09-24 download, PDB in SAbDab, parsed
      affinities): experimental ddG = RT ln(Kd_mut/Kd_wt), R=1.9872e-3 kcal/mol/K, T=298. Predicted
      ddG from RaSP (KULL-Centre 2022, sum of single-mutation predictions for multi-point mutants).
      PASS iff Spearman rho >= 0.4 over all mutations on complexes whose WT structure downloads.
      If RaSP cannot run in this environment, G2 is documented as blocked, not forced.
  G3: per-stage metrics published (modeling RMSD, control-arm vs modeled-arm DockQ, affinity rho);
      PASS iff REPORT contains all three stages, whatever the values.
USAGE: python3 abbench.py <data_dir> <work_dir> <results_dir> <stage>
  stage = select | model | dock | score | affinity | summarize  (stages run across multiple wakes)
"""
import sys, os, json, subprocess, urllib.request, math
import numpy as np, pandas as pd

data, work, out, stage = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(work, exist_ok=True); os.makedirs(out, exist_ok=True)
NR = pd.read_csv(os.path.join(data, 'sabdab_nr.csv'))
N_TARGET = 24
EXCLUDE = {'1AHW'}

def fetch_pdb(pdb4, dest):
    if os.path.exists(dest): return True
    try:
        urllib.request.urlretrieve(f'https://files.rcsb.org/download/{pdb4}.pdb', dest)
        return os.path.getsize(dest) > 1000
    except Exception:
        return False

def state_path(): return os.path.join(work, 'state.json')
def load_state():
    if os.path.exists(state_path()):
        return json.load(open(state_path()))
    return {'queue': [p for p in NR.pdb4.tolist() if p not in EXCLUDE], 'done': [], 'skipped': {}, 'started': False}

if stage == 'select':
    st = load_state()
    json.dump(st, open(state_path(), 'w'), indent=1)
    print(json.dumps({'queue_len': len(st['queue'])}))
    sys.exit(0)

# ---- shared helpers ----
from Bio.PDB import PDBParser, PDBIO, Select
P = PDBParser(QUIET=True)

def extract_chains(pdbfile, chains, dest):
    s = P.get_structure('x', pdbfile)
    io = PDBIO()
    class Sel(Select):
        def accept_chain(self, c): return c.id in chains
    io.set_structure(s); io.save(dest, Sel())
    return os.path.exists(dest) and os.path.getsize(dest) > 500

def chain_seq_len(pdbfile, chain):
    s = P.get_structure('x', pdbfile)
    for c in s[0]:
        if c.id == chain:
            return sum(1 for r in c if r.id[0] == ' ')
    return 0

if stage in ('model', 'dock'):
    st = load_state(); st['started'] = True
    done_set = set(st['done'])
    n_complete = len(done_set)
    row_by_pdb = {r.pdb4: r for r in NR.itertuples()}
    for pdb4 in list(st['queue']):
        if n_complete >= N_TARGET: break
        if pdb4 in done_set or pdb4 in st['skipped']: continue
        cdir = os.path.join(work, pdb4); os.makedirs(cdir, exist_ok=True)
        native = os.path.join(cdir, 'native.pdb')
        if not fetch_pdb(pdb4, native):
            st['skipped'][pdb4] = 'pdb_download'; continue
        row = row_by_pdb[pdb4]
        aglen = chain_seq_len(native, row.antigen_chain)
        if not (30 <= aglen <= 400):
            st['skipped'][pdb4] = f'ag_len_{aglen}'; continue
        if stage == 'model':
            if not os.path.exists(os.path.join(cdir, 'fv_model.pdb')):
                try:
                    from ImmuneBuilder import ABodyBuilder2
                    seqs = {'H': str(row.VH).replace('-', ''), 'L': str(row.VL).replace('-', '')}
                    pred = ABodyBuilder2(numbering_scheme='imgt').predict(seqs)
                    pred.save_single_unrefined(os.path.join(cdir, 'fv_model.pdb'))
                except Exception as e:
                    st['skipped'][pdb4] = f'model_fail_{type(e).__name__}'; continue
        if stage == 'dock':
            # extract receptor and ligands
            extract_chains(native, [row.antigen_chain], os.path.join(cdir, 'antigen.pdb'))
            extract_chains(native, [row.Hchain, row.Lchain], os.path.join(cdir, 'fv_native.pdb'))
            for arm, lig in [('modeled', 'fv_model.pdb'), ('native', 'fv_native.pdb')]:
                adir = os.path.join(cdir, arm); os.makedirs(adir, exist_ok=True)
                if os.path.exists(os.path.join(adir, 'dock.done')): continue
                lig_p = os.path.join(cdir, lig)
                if not os.path.exists(lig_p): continue
                try:
                    subprocess.run(['lightdock3_setup.py', os.path.join(cdir, 'antigen.pdb'), lig_p,
                                    '-s', '40', '-g', '100', '--noh', '--now', '--noxt'],
                                   cwd=adir, check=True, capture_output=True, timeout=600)
                    subprocess.run(['lightdock3.py', 'setup.json', '100', '-c', '2'],
                                   cwd=adir, check=True, capture_output=True, timeout=7200)
                    open(os.path.join(adir, 'dock.done'), 'w').write('ok')
                except Exception as e:
                    st['skipped'][pdb4 + '_' + arm] = f'dock_fail_{type(e).__name__}'
        if stage == 'dock':
            md = os.path.exists(os.path.join(cdir, 'modeled', 'dock.done'))
            if md:
                st['done'].append(pdb4); n_complete += 1
    json.dump(st, open(state_path(), 'w'), indent=1)
    print(json.dumps({'done': len(st['done']), 'skipped': len(st['skipped'])}))
    sys.exit(0)

print(f'stage {stage}: implemented in later commit (scoring/summarize added before first scoring run)', file=sys.stderr)
sys.exit(2)
