# algo50/09 - Docking screen of adenosine deaminase (DUD-E) with interaction-fingerprint rescoring

Protocol and gates locked before docking (PROTOCOL.md, results/lock.txt, locked 2026-09-23T21:05:36Z). There's a disclosure note about the lost earlier attempt. DUD-E ADA: 93 actives + 465 random decoys, AutoDock Vina (exhaustiveness 4), 0 failed docks. The IFP was written from scratch over 32 binding-site residues + zinc.

## Results (results/metrics.json, results/per_compound.tsv)
| score | AUROC | EF5% | BEDROC20 |
|---|---|---|---|
| Vina score | 0.473 | 0.21 | 0.13 |
| IFP similarity to crystal pose | 0.776 | 3.64 | 0.58 |
| Consensus (Vina + IFP ranks) | 0.659 | 2.79 | 0.39 |
| 2D ECFP4 similarity to crystal ligand | 0.882 | 6.00 | 0.92 |
| Heavy-atom count | 0.562 | 2.79 | 0.34 |
| Random | 0.545 | 0.86 | 0.20 |

## Gates
- G0 FAIL (validity): the redocked crystal ligand's top pose is 6.15 A from the crystal pose (needed < 2 A). Per the locked protocol, all pose-based (IFP) results below are marked UNRELIABLE.
- G1 PASS: consensus AUROC beats Vina by +0.186 (95% CI 0.142 to 0.230).
- G2 PASS: consensus EF5% is 2.79 vs Vina 0.21.
- G3 FAIL (the honest control): plain 2D similarity to the crystal ligand beats the consensus by 0.223 AUROC (CI -0.271 to -0.176). It also beats IFP alone (0.776) and everything else.

## Post-hoc redock diagnostic (not gated; results/redock_diag.txt)
| start conformer | exhaustiveness | top-1 RMSD | best of 9 poses |
|---|---|---|---|
| from SMILES | 16 | 6.16 A | 4.16 A |
| from SMILES | 32 | 6.16 A | 4.16 A |
| crystal | 16 | 6.09 A | 1.53 A |
| crystal | 32 | 6.12 A | 4.39 A |
More search does not fix it. Vina keeps ranking the same wrong pose (~ -9.4 kcal/mol) first, even when a near-native pose (1.5 A) is found. So this is a scoring/receptor-setup failure, not a search failure. Likely causes: no zinc-specific term in the vina scoring function, the zinc-bound water missing from the DUD-E receptor, and heuristic receptor atom typing.

## What this means
On this setup, the Vina score does no better than random at picking ADA actives (AUROC 0.47). Rescoring by interaction-fingerprint match rescues much of the enrichment, so G1 and G2 pass. But the headline claim does not survive the honest control: 2D similarity to the known ligand does better without any docking. Since the redocking check failed, the IFP gain most likely reflects that actives resemble the crystal ligand and so touch similar residues, not that the poses are right. Bottom line: G1/G2 pass on paper, but G0 and G3 fail, so this should be read as a negative for docking-based rescoring on ADA in this setup.

## Caveats
One target only; decoys subsampled 5:1; exhaustiveness 4 in the main run (the diagnostic shows higher exhaustiveness would not change the top pose). DUD-E actives are known to share chemotypes with crystal ligands, which favours 2D similarity.

## Reproduce
Download data/source_url.txt into data/ (untar), then cd code && python3 prep.py && python3 dock.py (~1.5 h on 2 cores) && python3 g0.py && python3 analyze.py && python3 redock_diag.py
