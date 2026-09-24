# algo50/55 - MoleculeNet task pattern: does descriptor-sufficiency track bulk-property vs binding-pocket tasks?

Lane RES-1. Direct follow-up to the algo50/51 vs algo50/53 contrast.

## Question
algo50/51 (BBBP, a bulk-property task) found fingerprints add almost nothing
to a linear model over 3 physicochemical descriptors under scaffold split;
algo50/53 (BACE, a binding-pocket task) found the opposite. This study tests
whether that split generalizes across two more MoleculeNet tasks with known
mechanistic type: ClinTox (organism-level toxicity - predicted
bulk/descriptor-dominated) and HIV (protease/reverse-transcriptase binding -
predicted substructure-dominated), using the IDENTICAL feature stack,
hyperparameters, and scaffold-split scheme.

## Data
ClinTox (clintox.csv, label `CT_TOX`, ~1,478 compounds) and HIV
(hiv.csv, label `HIV_active`, ~41,127 compounds) from the MoleculeNet/
DeepChem S3 mirror. Reference numbers for BBBP and BACE are the locked
algo50/51 and algo50/53 results (not recomputed). Same parsing rules:
largest-fragment desalting, parse failures dropped and counted. Raw CSVs not
committed; provenance in `data/`.

## Split
Murcko-scaffold greedy k-fold (seed 0): k=5 for ClinTox; k=3 for HIV
(runtime; declared, not tuned after the fact).

## Models (identical to algo50/51/53)
- B0: 3-descriptor (MolLogP, MolWt, TPSA) logistic, C=1.0.
- B1: binary ECFP4 logistic, C in {0.1,1,10} by inner scaffold-grouped CV
  (inner training subsampled to 6,000 compounds for HIV, seed 0).
- M1: GBM on count-ECFP4+MACCS+8 descriptors (fixed hyperparameters).
- Descriptor gap := AUROC(B1) - AUROC(B0).

## Gates (declared before any model is run)
- G1: gap(ClinTox) < 0.10 (predicted descriptor-dominated, like BBBP's 0.017).
- G2: gap(HIV) > 0.05 (predicted substructure-dominated, like BACE's 0.180).
- G3: AUROC(M1) >= AUROC(B1) + 0.02 on BOTH new tasks.
- G4 (4-task sign consistency): gap < 0.05 on BBBP AND ClinTox, and
  gap > 0.05 on BACE AND HIV (BBBP 0.017 and BACE 0.180 are already locked;
  this gate binds only the two new numbers).

## Pivot plan (only if gates fail, pre-registered as amendments before results)
- P1: if G3 fails on HIV due to extreme class imbalance (~3.5% positive),
  re-evaluate with average precision instead of AUROC: gate P1 =
  AP(M1) >= AP(B1) + 0.02.
- P2: if G1 fails (ClinTox gap >= 0.10), test whether the gap is driven by
  heavy metals/organometallics ( ClinTox contains them; BBBP largely does
  not): exclude compounds with elements outside {H,C,N,O,F,P,S,Cl,Br,I} and
  recompute: gate P2 = restricted gap < 0.10.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates stay in
the README with their numbers.
