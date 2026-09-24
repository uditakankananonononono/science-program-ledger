# 55 - MoleculeNet task pattern: does descriptor-sufficiency track bulk-property vs binding-pocket tasks?

Lane RES-1. Direct follow-up to the algo50/51 vs algo50/53 contrast. Protocol hashed and locked before any model ran (`results/lock.txt`); the 51/53 reference gaps used for G4 were already locked in those projects.

## Question
algo50/51 (BBBP, bulk property) found fingerprints add almost nothing over 3 physicochemical descriptors (gap +0.017); algo50/53 (BACE, binding pocket) found the opposite (+0.180). 55 tests whether that split generalizes: ClinTox (organism-level toxicity, predicted descriptor-dominated) and HIV (protease binding, predicted substructure-dominated), identical pipeline, scaffold splits.

## Results
| Task | n (base rate) | B0 3-desc | B1 bin-ECFP4 | M1 GBM | gap (B1-B0) |
|---|---|---|---|---|---|
| ClinTox | 1473 (0.071) | 0.671 | 0.703 | 0.878 | +0.032 |
| HIV | 40936 (0.035) | 0.648 | 0.718 | 0.807 | +0.069 |

HIV average precision: B0 0.149, B1 0.149, M1 0.380 (relevant to P1: AP gate if AUROC G3 fails on imbalance). ClinTox AP: B0 0.111, B1 0.206, M1 0.493.

## Gates (locked before results)
| G1 gap(ClinTox) < 0.10 (descriptor-dominated prediction) | PASS |
| G2 gap(HIV) > 0.05 (substructure-dominated prediction) | PASS |
| G3 M1 >= B1+0.02 on both new tasks | PASS |
| G4 4-task sign consistency (BBBP+ClinTox < 0.05, BACE+HIV > 0.05) | PASS |

Pre-registered pivots (run only if triggered): P1 = HIV average-precision form of G3 (AP(M1) >= AP(B1)+0.02); P2 = ClinTox gap after excluding compounds with elements outside {H,C,N,O,F,P,S,Cl,Br,I} (heavy-metal/organometallic drive test).

## Data and parsing
ClinTox (clintox.csv) and HIV (HIV.csv) from the MoleculeNet/DeepChem S3 mirror; provenance + sha256 in `data/provenance.txt` (regenerate via `code/prep.py`). Largest-fragment desalting, dedupe by fragment SMILES keeping first label: ClinTox n=1473 (0 label conflicts), HIV n=40936 (17 label conflicts). Murcko-scaffold greedy k-fold, seed 0: k=5 ClinTox, k=3 HIV (runtime, declared in protocol).

## Reproduce
`python3 code/prep.py && python3 code/run55.py && python3 code/finalize55.py`. Out-of-fold predictions: `results/oof_clintox.npz`, `results/oof_hiv.npz`. Figure: `results/fig_pattern.png`.

## Caveats
- Sandbox OOM note: the runner is memory-shaped (two passes, uint8/uint16 storage, float32 folds) for a 2GB box; the math is identical to the locked protocol's model specs.
- HIV is 3.5% positive; AUROC can flatter. AP numbers above; P1 applies if G3 failed on HIV.
- Scaffold splits make all numbers harder than random-split literature values.
