# ADDENDUM A (locked 2026-09-24 07:56, BEFORE any scoring)
Design gap found while implementing (no outcome computed yet): the two sections have INDEPENDENT Leiden
clusterings, so a (LR, A->B) triple from the fit section has no counterpart index on the validation
section. Repair: validation-section spots are assigned to the FIT section's clusters by nearest
fit-cluster centroid (cosine distance in the shared 416-LR-gene PCA space, SVD fit on the fit section
only). Clustering itself is never refit on the validation section; the frozen section stays untouched by
cluster definition. Direction swap (P2A) uses the mirror-image procedure. No gate, margin, or threshold
changes.
