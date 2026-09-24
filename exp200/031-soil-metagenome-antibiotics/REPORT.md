# DOC-1-031: Discovering Novel Antibiotics from Soil Metagenomes - DOCUMENTED BOUNDARY

## Outcome
The published AMP-discovery benchmark is homology-leakage-dominated, and neither a
physicochemical-RF (Macrel reimplementation) nor a compact 3-mer logistic generalizes to an
independent cohort. Dev gate G2 fails (ARM B below ARM A); pre-registered rescue P1
(homology-pruned retrain) fails the same gates; frozen DRAMP validation fails decisively
(MCC <= 0.38). Failure tree exhausted per locked GATES.md (2026-09-24 08:39 IST, pre-outcome)
+ Addendum A (08:40, AmPEP-only train per the paper's exact protocol).

## Data (all public, verified pre-lock; hashes in results/data_manifest.json)
- TRAIN: AmPEP train 3,268 AMP + 166,170 deduped non-AMP (Macrel protocol, Addendum A).
- DEV: iAMP-2L Supp-S2 test, 920 AMP + 920 NAMP (the Macrel paper Table 1 comparison set).
- FROZEN: DRAMP 3.0 antibacterial natural AMPs, deduped + 80%-identity pruned vs ALL train+dev
  => 2,068 positives (3,405 pruned); 2,068 length-matched UniProt reviewed segments as
  negatives (028 granularity rule), DRAMP-decontaminated.

## Results (MCC at 0.5 threshold)
| arm | dev (iAMP-2L) | Supp-S1 (ungated) | frozen DRAMP |
|---|---|---|---|
| published Macrel (named baseline) | 0.90 | - | - |
| published MacrelX / iAMP-2L / AmPEP* | 0.91 / 0.90 / 0.92* | - | - |
| ARM A Macrel-feature RF (dev-trained) | **0.975** (G1 PASS >=0.85) | 0.973 | 0.262 |
| ARM B 3-mer logistic (dev-trained) | 0.954 | 0.900 | 0.380 |
| P1 ARM A (homology-pruned train) | 0.592 | 0.866 | 0.227 |
| P1 ARM B (homology-pruned train) | 0.798 | 0.876 | 0.373 |
*AmPEP flagged as overlap-inflated by the Macrel paper itself; context only.

## Leakage audit (the payload)
- 1,358 of 3,268 AMP-side training sequences (42%) are >=80% identical to a dev test sequence
  (plus exact duplicates); removing them collapses ARM A dev MCC 0.975 -> 0.592 and
  ARM B 0.954 -> 0.798.
- 3,405 of 5,473 "independent" DRAMP frozen candidates (62%) were >=80% identical to train+dev
  and had to be pruned.
- After pruning, in-domain dev MCCs (0.59-0.80) still overstate cross-cohort skill: frozen
  DRAMP MCC is 0.23-0.38 for every arm. The published 0.90-0.92 numbers measure database
  overlap, not discovery skill.

## Gate adjudication (locked thresholds)
- G1 PASS (0.975 >= 0.85). G2 FAIL: ARM B 0.954 >= 0.92 but < ARM A 0.975 + 0.02.
- P1 FAIL: 0.798 < 0.92. G3 FAIL: ARM B frozen 0.380 << dev - 0.10. Tree exhausted.

## Mechanism (G4, runs regardless)
Top positive 3-mers in the pruned ARM B are Cys-rich disulfide-stabilized AMP motifs
(CCV 2.42, GYC 2.31, CSR 2.12, CCL 1.99, TCY 1.81) and Arg-containing cationic motifs
(RIV, RFG, RDY, GRL); net charge/aa AMP +0.063 vs non-AMP -0.002 - canonical cationic-AMP
biology, so the learned signal is real but family-specific: disjoint DRAMP families are missed.
Smoke-test illustration: a held-out DRAMP AMP scores 0.457 (< 0.5) while a non-AMP scores 0.0007.

## Tool (G5)
tools/amp_predict.py + results/amp_model_pruned.npz (the homology-pruned model, shipped as the
honest-generalization choice), smoke-tested. AMPSphere soil-subset nomination: STAGED, not
scored - the ampsphere.big-data-biology.org file URLs 404'd at run time (674-byte HTML stubs);
exact remainder: resolve the AMPSphere v2022-03 download, filter soil-habitat candidates, score
with amp_predict.py, novelty = <=80% identity to DRAMP, nominate top 10.

## Prospective lab nomination (locked)
An AMP wet-lab screening unit (MIC assays vs ESKAPE panels): test top-ranked soil-metagenome
candidates once the staged AMPSphere run completes; treat rankings as hypothesis-generating
(frozen MCC 0.37), prioritizing Cys-rich/cationic candidates the mechanism analysis supports.

## Payload (candidate for the program task-type map)
Benchmark leakage is the dominant term in this literature: published AMP classifiers measure
database overlap (42% train<->test near-dupes; 62% of an "independent" cohort prunable), and
honest homology control collapses dev MCC by 0.16-0.38 with cross-cohort skill at 0.23-0.38.
Compact k-mer models degrade more gracefully than physicochemical RFs under pruning
(0.798 vs 0.592) and frozen transfer (0.373 vs 0.227). Sibling to the 028 label-granularity
rule: cohort DISJOINTNESS granularity must match the discovery claim's granularity - verified
pre-lock from now on.

## AMPSphere soil-subset nomination (remainder completed 2026-09-24 10:47 IST)
Source resolved: Zenodo record 6511404 (AMPSphere v.2022-03, CC BY 4.0; the big-data-biology.org
file URLs remain dead). Files: AMPSphere_v.2022-03.faa.gz (863,498 peptides),
AMPSphere_v.2022-03.general_geneinfo.tsv.gz (habitat per gene),
DRAMP_anno_AMPSphere_v.2021-03.parsed.tsv.gz (novelty).

Protocol: genes with general_envo_name == "soil" -> 266,287 unique peptides; novelty filter
(excluded 1,774 peptides with a DRAMP alignment identity > 0.80) -> 265,727 scored with
tools/amp_predict.py + results/amp_model_pruned.npz. 58,135 scored p >= 0.5 (21.9%), spanning
41,119 SPHERE-III families. Nomination: best-scoring peptide per SPHERE-III family (diversity),
ties at p = 1.0 broken by AMP accession ascending (more observed copies first, per AMPSphere
numbering).

TOP 10 (results/soil_top10.json):
| # | AMP | SPHERE-III family | p | len | Cys | net chg |
|---|---|---|---|---|---|---|
| 1 | AMP10.013_525 | 434_459 | 1.0000 | 39 | 1 | +2 |
| 2 | AMP10.015_859 | 290_216 | 1.0000 | 30 | 0 | +3 |
| 3 | AMP10.020_263 | 002_214 | 1.0000 | 26 | 0 | +15 |
| 4 | AMP10.027_113 | 000_276 | 1.0000 | 41 | 2 | +3 |
| 5 | AMP10.031_875 | 001_688 | 1.0000 | 31 | 1 | +6 |
| 6 | AMP10.037_460 | 054_457 | 1.0000 | 37 | 0 | +4 |
| 7 | AMP10.045_928 | 000_551 | 1.0000 | 47 | 5 | +6 |
| 8 | AMP10.056_456 | 027_934 | 1.0000 | 57 | 0 | +6 |
| 9 | AMP10.056_498 | 013_960 | 1.0000 | 64 | 0 | +11 |
| 10 | AMP10.077_203 | 000_336 | 1.0000 | 36 | 0 | +5 |

Consistent with the locked lab-nomination guidance: strongly cationic candidates (#3 +15,
#9 +11) and a Cys-rich candidate (#7, 5 Cys) both surface. All rankings hypothesis-generating
(frozen MCC 0.37); sequences in results/soil_top10.json for the wet-lab screen.
