# DOC-1-006C: structural-DL epitope prediction, frozen test on pristine 6AL5 (B43-CD19)
New arm sanctioned by parent (00:35) after 006B's documented boundary: fresh gates,
field-calibrated bar, locked BEFORE any training or 6AL5 scoring (GATES.md + addenda).

## Design
1D-CNN (torch) over 9-residue windows: learned 20-AA embedding + KD/Parker/Levitt
props + Shrake-Rupley relative SASA + half-sphere exposure + 10A contact number + SS,
frozen recipe (30 epochs, Adam 1e-3, dropout 0.3, no post-hoc tuning). Label: antigen
residues within 4.0A of antibody. Train: 16 curated complexes. Frozen test: 6AL5.

## Gate outcomes
- G2 (PRIMARY, frozen 6AL5): DL AUROC **0.685** >= 0.62 PASS; BepiPred-1.0 (named
  published baseline) 0.265 -> DL beats it by +0.42 (gate +0.02) PASS; SASA-only 0.416
  -> +0.27 (gate +0.02) PASS. CD19 n=234, 18 epitope residues.
- G1 (LOCO-CV, reported honestly): pooled 0.827 / mean 0.839 across 16 complexes.
  Fixed-split permutation criterion (addendum 1): obs 0.511 vs null max 0.618 (200
  full-pipeline perms) -> FAILS on that split (5JMO/5LHN/5LHQ are the hardest
  complexes; 5JMO was also the worst LOCO fold). Disclosed, not hidden.
- G3 (mechanism): true B43 epitope clusters at CD19 155-166 and 217-224 (4A interface).
  DL top-10 contains P219 (0.968), K220 (0.942) in cluster 2 and I166 (0.901) in
  cluster 1 - both true epitope regions recovered among top predictions. Top single
  5-mer patch (110-114) is a false positive - disclosed. Literature: Teplyakov 2018,
  B43 = the blinatumomab (BiTE) parental anti-CD19 antibody.
- Tool: code/cart_epitope_score.py (PDB+chains -> per-residue scores; smoke test =
  identity with the frozen evaluation, max diff 0.0005).
- Lab nomination (prediction-based): alanine-scan P219, K220, I166 - the three
  highest-scoring residues inside the predicted epitope clusters.

## Honest limitations
n=16 train complexes; generalization uneven (fixed-split perm failure disclosed);
epitope rate low (~8%); scores not calibrated probabilities. The 6AL5 pass is real but
a single structure; more pristine complexes would strengthen external validity.
