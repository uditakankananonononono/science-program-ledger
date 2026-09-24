# DOC-1-011F: PLM Discovery in the Remote-Homology Regime — REPORT (2026-09-24)

Follow-up to DOC-1-011 (boundary: ESM-2 8M retrieval redundant where sequence similarity
exists). 011F tests 011's own nominated hypothesis: PLM discovery value specifically where
sequence signal is ABSENT. Gates locked pre-scoring (GATES.md b7171ce5 + Addendum A pool
disjointness + Addendum B centroid-scorer mechanics; parent approval 12:54:54).
VERDICT: MIXED - G1 dev FAIL (clause 1), G2 frozen PASS. Documented; parent adjudicates.

## Pools (locked Addendum A; live UniProtKB counts 12:57)
- Dev remote positives n=311: 300 Cas12f1 (pre-2023, rng seed 7, of 1,107) + 6 Cas12b +
  5 Cas12k. Decoys n=1,551 length-matched to positive p5-p95 lengths [70, 909aa]: all
  length-eligible from 011's committed pools (1,386 bacterial + 165 hard nuclease/polymerase;
  below 1,500/300 targets - all eligible taken, disclosed per Addendum A section 2).
- Frozen n=326 positives: 300 Cas12f1 post-2023 (of 717) + 6 Cas12b + 20 Cas12k; 300
  length-matched post-2023 bacterial decoys (of 1,470 eligible). Zero dev/frozen overlap.
- Seeds: 011's exact 182 seed accessions re-fetched by accession (Addendum B).

## Results (all single scoring passes post-lock; results/*.json)
- G0 (premise audit): MMseqs2 -s 7.5 retrieval AUROC of dev positives vs decoys = 0.4957
  (halt bar >= 0.70). Hits: 3/311 positives, 28/1,551 decoys. PASS - sequence signal
  verifiably absent; the remote-homology regime is real, not assumed.
- G1 (dev): PLM centroid AUROC = 0.7574. Clause 1 (>= 0.80): FAIL. Clause 2
  (>= MMseqs2 + 0.20 = 0.6957): PASS (margin +0.26). Both required -> G1 FAIL.
- G2 (frozen, single-pass): PLM AUROC = 0.8212 on post-2023 deposits (bar >= 0.75: PASS);
  dev->frozen drop = -0.064, i.e. frozen BETTER than dev (bound <= 0.10: PASS). G2 PASS.
  MMseqs2 on the same frozen set: 0.4867 - chance again (PLM margin +0.33).
- G3 (mechanism): 311 dev positives' nearest seed centroids: Cas9 167 / Cas13a 142 /
  Cas12a 2. Cas12f does NOT map to a single family centroid (expected: it is TnpB-derived,
  not a Cas9/12a/13a subtype) yet embeds far from decoys - the 8M space separates remote
  CRISPR effectors from background WITHOUT subtype coherence, extending 011's PCA picture
  (class-2 architecture capture) to a family with no seed representation.
- G4: code/crispr_remote_finder.py CLI (FASTA -> score + nearest centroid), smoke-tested
  on frozen positives (scores 0.89-0.96). Nomination: metagenome-mining programs screening
  candidate effectors below MMseqs2 detectability (e.g. IGI remote-effector screens).

## Interpretation vs literature
011 showed the PLM adds nothing WHERE sequence search saturates. 011F shows the mirror:
where MMseqs2 is verifiably at chance (0.496/0.487), the same 8M embeddings carry real
effector signal (0.757 dev / 0.821 frozen, temporal validation passed). The locked dev
0.80 bar was still missed (0.757) - so per the failure tree the 011 boundary stands at dev
strictness, but the frozen-set inversion (0.821 >= 0.75, no drop) shows the signal is
durable across the annotation cutoff. PLM discovery value at 8M scale is regime-dependent:
absent on alignable families (011), present but sub-0.80-dev in remote homology (011F).
Literature fit: Cas12f/Cas14 compact TnpB-derived effectors (Makarova 2020; Altae-Tran 2021)
are exactly the class sequence search under-detects.

## Failure-tree routing
G1 fail -> "the 011 boundary generalizes: PLM adds no retrieval value even without sequence
signal at 8M scale; document + parent adjudicates." Documented with the frozen-set
counter-evidence above; reported to parent with full numbers for adjudication.

## Honest limits
Decoy shortfall (1,551 vs 1,800 target) disclosed; length matching removes size leakage but
composition effects remain possible; frozen positives are 92% Cas12f1 (post-2023 UniProtKB
deposition skew, same caveat as 011's Cas9 skew); centroid scorer compresses each family to
one point - per-seed max-cosine may behave differently (not tested; single locked scorer).
