# GATES ADDENDUM A - DOC-1-033 (locked 2026-09-24 09:53 IST, before dev CV completes)

## Trigger (design fact discovered at first fold, not a threshold relaxation)
Locked G1 quoted the paper's no-graph decoder anchor (56% species) as the coherence band
[0.35, 0.70]. That anchor is NOT comparable to our no-graph variant: the paper's decoder uses
k-mer features of BOTH viruses and prokaryotes (they hold prokaryote genomes), while our
scoped design (locked in GATES: no prokaryote genomes) gives prokaryotes taxonomy features
only. Our no-graph variant is therefore approximately a taxonomy-popularity model by
construction; the paper's 56% band cannot sanity-check it.

## Change (locked)
G1 (sanity halt) redefined: ARM B graph dev 10-fold CV species accuracy >= train-popularity
baseline + 5 percentage points, where the baseline predicts the most frequent train host
species (Mycolicibacterium smegmatis, 17.1% of train pairs) for every query. This check is
feature-matched, pre-registered against a number computable without training, and still halts
on incoherent data or model. G2/G3 unchanged; the paper anchors remain as documented
references only. Fold-0 progress values already computed (graph 0.175 / no-graph 0.103) are
disclosed here; the new band references the popularity baseline, which was computed from the
manifest independently of any model output.
