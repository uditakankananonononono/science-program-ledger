# 198 RESULT - R-03 (Mpro redock 0.97 A, mega27-12 @ 97588a78)
Prereg: algo50/198-PREREG.md (v2 + timeout fix, committed ~04:55 IST before any docking; text sha256 8415ff876ef556cbb8158602e7328824392f856027ca9146f5e5b786bc40feb9), wrappers algo50/198-r03_metric.py.md / 198-r03_run.py.md. Run once, results below verbatim. Same-organisation re-execution; not a novel method.

## Outcome label (fixed in prereg): aligned statistic reproduced; prospective in-frame single-complex redocking check passed.
This is NOT a replication of an original in-frame docking-error claim, because the original 0.97 A was computed after Kabsch superposition of the pose onto the crystal ligand (graph-free per-element matching).

## Q1 numerical reproduction (A) - PASS
Unmodified studies/study12_redock.py, seed 42, my environment (vina 1.2.7, meeko 0.8.0, rdkit 2023.9.6). Reported RMSD 1.0489 A (window [0.80,1.15]), gate PASS, best affinity -9.274 kcal/mol. Committed original: 0.9701 A, -9.319. The numbers do not match exactly (environment differs; original environment unknown), so this is a tolerance reproduction, not a bit-exact one.

## Q2 in-frame check (prospective)
B (A's pose, primary in-place symmetry+stereo-preserving RMSD, 8 mappings, validity gate passed): 1.138 A (graph-free Hungarian secondary 1.124). PASS (<2.0).
C (10 fresh seeds 196001-196010): 7/10 under 2.0 A, median 1.128 A. Criterion >=7/10 and median <2.0: PASS, with 3 of 10 runs landing in a different pose at about 5.1-5.6 A. 7/10 sits exactly at the preregistered threshold. No errors, timeouts or retries.

| seed | best affinity | in-frame RMSD (primary) | Hungarian secondary | secs |
|---|---|---|---|---|
| 196001 | -9.098 | 1.133 | 1.094 | 78 |
| 196002 | -8.807 | 5.121 | 2.199 | 83 |
| 196003 | -9.29 | 1.127 | 1.111 | 78 |
| 196004 | -8.266 | 5.605 | 3.215 | 77 |
| 196005 | -9.43 | 1.070 | 1.058 | 75 |
| 196006 | -9.351 | 1.070 | 1.051 | 74 |
| 196007 | -9.086 | 1.058 | 1.005 | 77 |
| 196008 | -9.145 | 1.128 | 1.112 | 78 |
| 196009 | -8.482 | 5.091 | 2.208 | 80 |
| 196010 | -9.204 | 1.129 | 1.116 | 77 |

## Caveats
Box centred on the crystal ligand; single protein/ligand pair; does not validate docking generally. The 3 bad seeds show the top-ranked pose is not always the crystal-like pose, so a single-seed redock (as in the original) overstates reliability. Counts toward the replication tally at the parent's discretion; the labelled outcome is the only claim.

## Verbatim
```
{
 "returncode": 0,
 "secs": 78.28684639930725,
 "stdout_tail": "ligand SMILES: C[C@H](NC(=O)[C@@H](c1cccnc1)N(C(=O)c1ccco1)c1ccc(-c2ccccc2)cc1)c1ccccc1\nligand PDBQT written\naffinities: [-9.274, -9.015, -8.727, -8.679, -8.591, -8.582, -8.558, -8.542, -8.382]\nredocking RMSD (heavy-atom assignment): 1.049 A\nprotocol validation gate (<2.0 A): PASS\nwrote results/redock_7KX5.json\n",
 "stderr_tail": "[04:56:42] Warning: molecule is tagged as 2D, but at least one Z coordinate is not zero. Marking the mol as 3D.\n",
 "repo_reported": {
  "ligand": "JUN8-76-3A (X7V)",
  "structure": "7KX5",
  "best_affinity_kcal_mol": -9.274,
  "all_affinities": [
   -9.274,
   -9.015,
   -8.727,
   -8.679,
   -8.591,
   -8.582,
   -8.558,
   -8.542,
   -8.382
  ],
  "rmsd_A": 1.0489155478321743,
  "gate": "PASS",
  "exhaustiveness": 16
 },
 "scored": {
  "inplace_rmsd_primary": 1.138127282216851,
  "n_mappings": 8,
  "hungarian_inplace_secondary": 1.123804358792982
 }
}
{"n_lt2": 7, "median_all10_failures_as_inf": 1.1283069843343014, "rmsds": [1.1326788344916057, 5.121184728782568, 1.127221479194703, 5.605440299152996, 1.0700201055661474, 1.0697475353903296, 1.058013593087487, 1.1280914133358633, 5.091481438328348, 1.1285225553327398]}
```
