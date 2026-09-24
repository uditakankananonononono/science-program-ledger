# DOC-1-014F: Score-Guided AMP Design — GATES (locked 2026-09-24 13:22 IST, before any scoring)

Follow-up to DOC-1-014 (boundary: unconditional 8M masked-LM sampling never finds AMP
order - 0.2% vs 10.2% shuffle baseline; "needs CONDITIONING or a search/guidance loop").
014F tests the guidance loop. Parent-approved sketch 13:20:36 ("lock G0-G3 numerically
pre-scoring... guide/judge separation... If G0 shows either judge can't recover known AMPs,
halt and report rather than substituting judges"). All thresholds numeric below.

## Design (all locked)
- SEEDS: 014's committed baseline_shuffled.fasta (shuffled-AMP compositions; 014's 10.2%
  Macrel baseline set); rng-seed-7 sample n=200.
- GUIDE: Macrel (014's exact published scorer, --keep-negatives full-set probability).
- REFINEMENT LOOP (fixed budget, no post-hoc changes): 30 iterations; per iteration,
  re-mask a uniform-random 15% of each sequence's positions and resample with 014's exact
  ESM-2 t6_8M masked decoding (temperature 1.0, 014's generate.py); greedy accept iff the
  Macrel probability does not decrease. rng seed 7 throughout.
- JUDGES (independent of the guide): amPEPpy 1.1.0 (Lawrence 2020 Bioinformatics, default
  probability threshold 0.5) AND AMPlify (BCGSC, Li 2022; balanced model, its published
  score cutoff 5.0). Both judges required for every "AMP+" verdict below.

## Gates
- G0 (judge calibration, pre-scoring, halt-no-patch per parent 13:20:36): each judge's AMP+
  rate on 014's committed heldout_apd.fasta (known AMPs) at its locked threshold must be
  >= 30%. Guide-judge and judge-judge agreement rates on the seed set disclosed. If either
  judge < 30% recovery -> HALT, report to parent, no judge substitution.
- G1 (dev, headline): final-sequence AMP+ rate >= 3x the SEED set's AMP+ rate on the SAME
  judge, for EACH judge separately (both required). Absolute rates reported alongside.
- G2 (novelty + envelope): among both-judge AMP+ winners (if any): >= 90% novel vs 014's
  apd_natural.fasta (MMseqs2 -s 7.5, < 70% pident) AND median net charge >= +2 AND median
  hydrophobic ratio in [0.30, 0.60] (cationic-amphipathic envelope, Hancock & Sahl 2006;
  ranges mirror 014's G3 context: top-50 median charge +3.5, hydrophobic 0.418). If zero
  winners, G2 is vacuous and disclosed as such.
- G3 (mechanism, documented): trajectory audit - median Macrel-probability gain from seed
  to final, median iteration of last improvement (saturation), fraction of 200 trajectories
  with any improvement; judge-score deltas alongside guide deltas (does the climb
  generalize off the guide?).
- G4: amp_guided_design.py CLI + REPORT.md + one prospective nomination.
- Failure tree: G0 halt -> report to parent (no substitution). G1 fail -> guidance loop
  does not fix 014's boundary at 8M scale; document, parent adjudicates (with judge-vs-guide
  divergence analysis from G3). G2 fail -> winners are memorized/non-AMP-like; document.
