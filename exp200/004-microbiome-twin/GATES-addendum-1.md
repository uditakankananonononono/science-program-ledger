# ADDENDUM 1 (locked 2026-09-23 ~23:28 IST, before model evaluation)
Permutation null reuses the outer-fold alpha selected on real labels (compute budget;
same convention as DOC-1-001). Undetected (0) metabolite values are treated as
missing for that metabolite-sample pair (per gates); detection = value > 0.
G2 name matching: case-insensitive substring match of the pre-registered names against
mtb.map.tsv Compound.Name where High.Confidence.Annotation == TRUE.
