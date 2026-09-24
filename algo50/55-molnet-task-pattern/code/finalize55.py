"""Build README + figure for algo50/55 from results.json (+ locked 51/53 refs)."""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

R = json.load(open('results/results.json'))
ref51 = json.load(open(os.path.expanduser('~/work/science-program-ledger/algo50/51-bbbp-fingerprint-ecfp/results/results.json')))
ref53 = json.load(open(os.path.expanduser('~/work/science-program-ledger/algo50/53-bace-scaffold-transfer/results/results.json')))

ct, hiv = R['clintox'], R['hiv']
g = R['gates']
g51 = ref51['auroc']; g53 = ref53['bace_classification']
rows = [
    ('BBBP (bulk property)', g51['B0'], g51['B1'], g51['M1']),
    ('ClinTox (organism tox)', ct['auroc']['B0'], ct['auroc']['B1'], ct['auroc']['M1']),
    ('BACE (binding pocket)', g53['B0_3desc'], g53['B1_binECFP'], g53['M1'] if 'M1' in g53 else g53.get('M1_gbm', float('nan'))),
    ('HIV (protease binding)', hiv['auroc']['B0'], hiv['auroc']['B1'], hiv['auroc']['M1']),
]
fig, ax = plt.subplots(figsize=(8.5, 4.5))
x = np.arange(4); w = 0.26
for i, (lab, c) in enumerate([('B0 3-descriptor logistic', '#8da0cb'), ('B1 binary-ECFP4 logistic', '#66c2a5'), ('M1 GBM count-ECFP+MACCS+desc', '#fc8d62')]):
    vals = [r[i+1] for r in rows]
    ax.bar(x + (i-1)*w, vals, w, label=lab)
for i, r in enumerate(rows):
    gap = r[2] - r[1]
    ax.text(i, 0.05, 'gap\n%+.3f' % gap, ha='center', fontsize=9, color='black')
ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows], fontsize=9)
ax.set_ylabel('AUROC (scaffold-held-out)')
ax.set_ylim(0, 1.02)
ax.set_title('algo50/55 - descriptor gap by task type across 4 MoleculeNet tasks')
ax.legend(fontsize=8, loc='upper left')
fig.tight_layout()
fig.savefig('results/fig_pattern.png', dpi=150)
print('figure written')

def gate(name, ok): return '| %s | %s |' % (name, 'PASS' if ok else 'FAIL')
readme = f"""# 55 - MoleculeNet task pattern: does descriptor-sufficiency track bulk-property vs binding-pocket tasks?

Lane RES-1. Direct follow-up to the algo50/51 vs algo50/53 contrast. Protocol hashed and locked before any model ran (`results/lock.txt`); the 51/53 reference gaps used for G4 were already locked in those projects.

## Question
algo50/51 (BBBP, bulk property) found fingerprints add almost nothing over 3 physicochemical descriptors (gap +{R['reference_gaps']['bbbp']:.3f}); algo50/53 (BACE, binding pocket) found the opposite (+{R['reference_gaps']['bace']:.3f}). 55 tests whether that split generalizes: ClinTox (organism-level toxicity, predicted descriptor-dominated) and HIV (protease binding, predicted substructure-dominated), identical pipeline, scaffold splits.

## Results
| Task | n (base rate) | B0 3-desc | B1 bin-ECFP4 | M1 GBM | gap (B1-B0) |
|---|---|---|---|---|---|
| ClinTox | {ct['n']} ({ct['base_rate']:.3f}) | {ct['auroc']['B0']:.3f} | {ct['auroc']['B1']:.3f} | {ct['auroc']['M1']:.3f} | {ct['gap_B1_minus_B0']:+.3f} |
| HIV | {hiv['n']} ({hiv['base_rate']:.3f}) | {hiv['auroc']['B0']:.3f} | {hiv['auroc']['B1']:.3f} | {hiv['auroc']['M1']:.3f} | {hiv['gap_B1_minus_B0']:+.3f} |

HIV average precision: B0 {hiv['ap']['B0']:.3f}, B1 {hiv['ap']['B1']:.3f}, M1 {hiv['ap']['M1']:.3f} (relevant to P1: AP gate if AUROC G3 fails on imbalance). ClinTox AP: B0 {ct['ap']['B0']:.3f}, B1 {ct['ap']['B1']:.3f}, M1 {ct['ap']['M1']:.3f}.

## Gates (locked before results)
{gate('G1 gap(ClinTox) < 0.10 (descriptor-dominated prediction)', g['G1_gap_clintox_lt_0.10'])}
{gate('G2 gap(HIV) > 0.05 (substructure-dominated prediction)', g['G2_gap_hiv_gt_0.05'])}
{gate('G3 M1 >= B1+0.02 on both new tasks', g['G3_M1_ge_B1+0.02_both'])}
{gate('G4 4-task sign consistency (BBBP+ClinTox < 0.05, BACE+HIV > 0.05)', g['G4_sign_consistency_4tasks'])}

Pre-registered pivots (run only if triggered): P1 = HIV average-precision form of G3 (AP(M1) >= AP(B1)+0.02); P2 = ClinTox gap after excluding compounds with elements outside {{H,C,N,O,F,P,S,Cl,Br,I}} (heavy-metal/organometallic drive test).

## Data and parsing
ClinTox (clintox.csv) and HIV (HIV.csv) from the MoleculeNet/DeepChem S3 mirror; provenance + sha256 in `data/provenance.txt` (regenerate via `code/prep.py`). Largest-fragment desalting, dedupe by fragment SMILES keeping first label: ClinTox n={ct['n']} ({ct['label_conflicts']} label conflicts), HIV n={hiv['n']} ({hiv['label_conflicts']} label conflicts). Murcko-scaffold greedy k-fold, seed 0: k=5 ClinTox, k=3 HIV (runtime, declared in protocol).

## Reproduce
`python3 code/prep.py && python3 code/run55.py && python3 code/finalize55.py`. Out-of-fold predictions: `results/oof_clintox.npz`, `results/oof_hiv.npz`. Figure: `results/fig_pattern.png`.

## Caveats
- Sandbox OOM note: the runner is memory-shaped (two passes, uint8/uint16 storage, float32 folds) for a 2GB box; the math is identical to the locked protocol's model specs.
- HIV is 3.5% positive; AUROC can flatter. AP numbers above; P1 applies if G3 failed on HIV.
- Scaffold splits make all numbers harder than random-split literature values.
"""
open('README.md', 'w').write(readme)
print('README written')
