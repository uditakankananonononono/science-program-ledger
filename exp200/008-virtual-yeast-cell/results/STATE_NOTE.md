# STATE at 03:28 IST (run-limit handoff) - ALL ANALYSIS DONE, only writeup/push/report left.
- G1 OFFICIAL (results/g1_official.json): minimal Yeast8 BA 0.747 vs iMM904 0.6177 FAIL(<0.85);
  rich (Addendum B) Yeast8 0.6979 vs 0.6031 FAIL. Both arms beat named baseline. => 008 = BOUNDARY
  on G1 per failure tree + B4. NOT counted. Tracker stays 47/100.
- G2 literal gate PASS but DEGENERATE (all 949 nonessential KOs = theoretical max 1.294 at 10% biomass floor).
- G2 supplementary growth-coupled scan COMPLETE (949/949, results/g2_gc90_ranked.json): WT gc90=0.1438.
  Top designs: FUM1/YPL262W 0.1648 (+15%), SDH3/YKL141W 0.1516, SDH2/YLL041C 0.1516, ZWF1 0.1465, RPE1 0.1465.
  MECHANISM CHECK = STRONG AGREEMENT: FUM1 (Arikawa 1999 SDH1+FUM1), SDH3 (Otero 2012 8D strain),
  SDH2 (SDH1/SDH2 disruption doi:10.1080/09168451.2014.877816). Gene identities verified against SGD
  phenotype_data.tab. SDH GPR (r_1021) fully consistent: SDH2/SDH3 in all 3 complex variants (KO disables),
  SDH4/SDH1/SDH9 each absent from >=1 variant (KO no effect, matches WT-level results).
  Literature: Otero PLoS ONE 2012 10.1371/journal.pone.0054144 (fetched, notes: sdh3 alone no in-vivo
  increase - honest framing: model recovers published TARGETS, magnitudes modest; 43-fold yield gain needed
  sdh3+ser3+ser33 COMBINATION).
- yeast_cell.py CLI written; WT smoke test PASSED (0.0811). KO/SUCC smoke tests not yet run (run them).
- TODO next run: (1) smoke tests KO YKL141W + SUCC YPL262W; (2) wet-lab nomination: FUM1 single KO as
  top single design + sdh3+ser3+ser33 combo per Otero; (3) RESULTS.md full honest writeup (G1 boundary both
  arms w/ confusion matrices + auxotroph-FP diagnosis, G2 degenerate pass, gc90 supplementary + mechanism
  check, CLI); PROVENANCE.md (all URLs+SHA256: GATES.md/ADDENDUM_A/B shas, data shas, literature DOIs);
  (4) commit+push ledger /home/sandbox/ledger GIT_SSH_COMMAND="ssh -i ~/.ssh_exp1/exp1_deploy_key -o
  IdentitiesOnly=yes"; verify git merge-base --is-ancestor HEAD origin/main; (5) CLAIMS.md mark 008 BOUNDARY
  not counted, keep 47/100; (6) report parent agent-01M2R8CPQMXQR26E3WGNHNNGY4: 008 boundary + mechanism
  win, ask whether proceed DOC-1-009; (7) next wake.
