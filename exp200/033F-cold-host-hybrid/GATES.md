# DOC-1-033F: Cold-Host Hybrid Exact-Signal Predictor — GATES (locked before any scoring)

Follow-up to DOC-1-033 (documented boundary: transductive GCN collapses frozen; KNN-d2 59.35%
holds). Parent-approved follow-up queue 2026-09-24 10:59:00. Fresh experiment, fresh gates;
NOT a retry of any 033 gate (008->METENG pattern).

## Question
On the cold-host subset — test phages whose true host species is structurally UNNAMEABLE by
KNN-d2 (absent from all train labels) — can a hybrid that votes from CRISPR-spacer exact
signals (falling back to KNN-d2) beat KNN-d2 by >= 5pp species top-1?

## Cold subset (locked, recomputable)
- Evaluated frozen test set = the 615 sequenced, host-in-panel test pairs of 033's
  committed manifest (manifest033.json, hashes in 033 PROVENANCE).
- Cold pair = test pair whose host_species string (manifest's own label) is absent from ALL
  1,260 train pairs' host_species strings. Recomputed count: 72 pairs over 32 species.
- Lineage disclosure: 033 GATES characterized "36 test host species absent from train" on the
  raw TEST671 set; under the evaluated 615-pair set (sequences + host-in-panel filters) the
  recomputable count is 32 species / 72 pairs. Subset file: cold_pairs033.json.
- KNN-d2's output space = train host species only, so its cold-subset ceiling is 0% BY
  CONSTRUCTION. This is the locked premise; G1 verifies it empirically.

## Eligibility findings (locked in as facts, computed pre-gate)
- CRISPR exact-signal coverage on cold viruses: 41/72 have >= 1 qualifying spacer edge
  (033's P1 qualification: length/slen > 0.95, pident > 95, first hit per virus; edges land
  in the 60,105-candidate panel).
- Protein-cluster sharing signal: NOT available in-envelope (database_gene_to_genome.csv is
  virus-side protein annotation only; no prokaryote cluster mapping; mmseqs2 build is the
  out-of-envelope step documented in 033). Locked out of scope.
- Power: with KNN-d2 at its 0% structural ceiling, the +5pp gate needs >= 4/72 correct calls;
  41 covered viruses give ample headroom. ELIGIBLE.

## Arms
- ARM A' = executed 033 ARM A (KNN-d2, cosine k=4 kmer, vote = train host species string)
  scored on the cold subset. Expected ~0% (structural); computed as G1 outcome.
- HYBRID: for each cold test virus v:
  1. If v has >= 1 qualifying CRISPR edge: predict the species of the panel prokaryote with
     the MOST spacer edges (tie-break: lowest panel index, deterministic). Species label =
     panel taxonomy binomial (first two words of terminal taxon).
  2. Else: fall back to ARM A' KNN-d2 vote.
- Label match: predicted binomial (first-two-words) vs host_species first-two-words. Locked
  normalization, disclosed; secondary genus metric = first word.

## Gates
- G1 (sanity halt): ARM A' cold-subset species top-1 <= 5% (structural-blindness premise).
  Else premise false -> halt, report to parent, do not score HYBRID.
- G2 (the claim): HYBRID cold-subset species top-1 >= ARM A' + 5pp, accuracy over ALL 72
  cold pairs (uncalled viruses with no CRISPR edge fall back to KNN-d2 and count as ordinary
  predictions; no coverage carve-out).
- G3 (no free lunch on warm): HYBRID on the 543 warm test pairs >= ARM A' - 2pp (exact-signal
  override must not materially damage the warm regime). Characterization of any regression.
- G4 (mechanism, runs regardless): provenance of correct cold calls (spacer-edge count
  distribution; hit prokaryote taxonomy vs literature anchors: CRISPR ~24.6% coverage);
  per-signal contribution; failure taxonomy of wrong calls (wrong-species spacer hit vs
  strain-level mismatch).
- G5: CLI cold_host_predict.py (hybrid voter, bundled edges + KNN assets) + prospective
  lab nomination.
- Failure tree: G1 fail -> halt to parent. G2 fail -> DOCUMENTED BOUNDARY (no further rescue:
  the exact signal is the only remaining mechanism; CRISPR IS the rescue).

## Prospective lab nomination (locked)
A phage-therapy group with a newly sequenced phage and a patient isolate panel: rank candidate
hosts; cold-regime exact-signal calls are the high-precision alerts for spot assays.

## Scoring discipline
cold_pairs033.json + this file + PROVENANCE.md committed BEFORE any arm is scored. Thresholds
never relax after seeing outcomes. All thresholds locked above.
