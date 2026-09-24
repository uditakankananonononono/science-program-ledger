# ADDENDUM B (2026-09-24 08:15): aggregation-style erratum + failure-tree outcome

Locked arm: "2-layer GraphSAGE (hidden 128...)". Implementation used symmetric-normalized
mean-aggregation (GCN-style, self-features included in the mean but NOT preserved as a separate
concat channel). Both locked arms (base + pre-registered P1 k=12/hidden-256) used this style.
This is an implementation deviation, not a threshold change; it is documented here after the
outcome and cannot rescue the verdict. Consequence: the GNN result should be read as
"mean-aggregation graph smoothing" specifically; a self-preserving GraphSAGE-concat variant was
NOT tested and is excluded by the locked failure tree ("no further arms"). Parent adjudicates
whether the boundary stands as-is (recommended: yes, per the tree) or merits a future re-locked
experiment with the corrected aggregation - that would be a NEW claim, not a rescue.
