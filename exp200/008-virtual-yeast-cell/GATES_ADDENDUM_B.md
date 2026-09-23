# GATES ADDENDUM B - locked 2026-09-24 ~03:00 IST, BEFORE any rich-medium results.
# Parent-adjudicated legitimate (02:56 ruling: fresh gate, 006C pattern, not re-fishing).

Rationale: G1 as locked evaluates on the model-default MINIMAL-glucose medium, but the
frozen truth (SGD null-allele viability, Giaever-style deletion phenotyping) was measured
on RICH medium (YPD). That is a train/eval condition mismatch discovered after lock, not
a failed prediction of the model. The minimal-medium arm stands and is documented as a
boundary inside RESULTS.md regardless of this arm's outcome.

- B1 NEW ARM G1-rich: same models, same truth set (sgd_truth.json), same common
  comparison set definition (Yeast8 genes x iMM904 genes x SGD truth minus unsolvable),
  same essentiality rule (KO growth < 1% of arm WT growth), same solver (HiGHS, Addendum A).
- B2 RICH-MEDIUM CONFIG (mechanical, reproducible): minimal medium PLUS uptake opened
  (exchange lower bound = -10 mmol/gDW/h) for extracellular metabolites in these FIXED
  categories: (a) 20 standard amino acids; (b) nucleobases/nucleosides: adenine, adenosine,
  guanine, guanosine, cytosine, cytidine, uracil, uridine, thymine, thymidine;
  (c) vitamins/cofactor precursors: biotin, thiamine, riboflavin, nicotinate/nicotinamide,
  pantothenate, pyridoxine, folate, myo-inositol, 4-aminobenzoate (PABA), choline;
  (d) ergosterol; (e) fatty acids: palmitate (16:0), oleate (18:1). Matching by
  metabolite-name substring; the exact matched exchange-reaction IDs per model are
  recorded in results/rich_medium_<model>.json as part of the locked artifact.
  Glucose remains the sole sugar carbon source (no other sugars opened).
- B3 GATES (UNCHANGED BAR): G1-rich passes iff Yeast8 BA >= 0.85 AND Yeast8 BA >= iMM904
  BA, both computed on the rich medium on the same common set.
- B4 FAILURE: G1-rich fails -> 008 documented as boundary ("virtual cell does not
  validate on frozen external essentiality even under measurement-matched medium"),
  no further arms, no threshold relaxation.
- B5 G2 (engineering) is medium-independent by design (defined minimal production
  medium) and proceeds in parallel regardless of B-arm outcome.
