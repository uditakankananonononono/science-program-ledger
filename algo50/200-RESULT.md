# RESULT unit 200 - R-05 sensitivity audit of the "32/32 novel peptides" claim (PARTIAL: Swiss-Prot arms done, NCBI nr arm N1 paused, not run)
Target: mega27-09c-peptide-solubility-anticancer @ 07c576e1be9a4bbf94df7a4d2031615af1b6caca, results/c6_blast_novelty.json. Prereg: 200-PREREG.md (v5g) plus 200-PREREG-AMENDMENT-1.md. Novelty is not activity: nothing here bears on anticancer or solubility predictions. Same-organisation audit. Published verbatim; N1 section will be amended when N1 resolves.

## Outcome (labels from the prereg table, wording unchanged)
- N1 (NCBI nr): NOT RUN. Paused, see below. No N1 reply was received for any query.
- L1 (mmseqs2 vs Swiss-Prot): G PASS, S PASS, A = 32/32 candidates with no NOT-NOVEL hit, 0 NEAR.
- L2 (exhaustive Smith-Waterman vs Swiss-Prot, committed prefilter 20): G PASS, S PASS, A = 32/32 with no NOT-NOVEL hit, 17 NEAR.
- Applicable label: "novelty reproduced for arm X only; sensitivity shown on Swiss-Prot-derived known sequences only; no claim for the other database." Here X = Swiss-Prot (L1 and L2). The combined novelty-vs-nr label is NOT available: it requires N1 AND L1 both G-pass, and N1 has no data. The result makes no statement about novelty against nr. Sensitivity was shown on Swiss-Prot-derived known sequences only; not shown for unannotated or patent-only sequences in nr. Novelty is not activity.

## Plain statements the numbers require
1. L2 NEAR is uninformative. Shuffled negatives (C4) also draw NEAR hits from Swiss-Prot in L2 (17/32 in draw 1, 15/32 in draw 2): a 13-16-mer aligned somewhere in Swiss-Prot at >=70% identity over >=80% coverage happens at about this rate by chance for short cationic low-complexity sequences. The candidates' 17 L2 NEAR calls are at that chance rate. By the prereg, NEAR does not reduce A and a C4 NEAR is not a specificity miss.
2. L1 sensitivity is below 100%: draw 1 C2 30/32; draw 2 C1 31/32, C2 30/32. G still passes (C1 >= 30, C2 >= 28 in both draws).
3. Swiss-Prot controls are in Swiss-Prot by construction, so L1/L2 sensitivity is close to a software check; N1 was the real test and did not run.

## Gate table, prefilter 20 (primary), per draw and class
Columns: arm, draw, class, NOT NOVEL, NEAR, NOVEL, Clopper-Pearson 95% lower bound of the NOT-NOVEL proportion. C1 and C2 should be NOT NOVEL; C3 report-only; C4 should be NOVEL (not NOT NOVEL).
| arm | draw | class | NOT NOVEL | NEAR | NOVEL | CP lower |
|---|---|---|---|---|---|---|
| L1 | 1 | C1 | 32/32 | 0 | 0 | 0.891 |
| L1 | 1 | C2 | 30/32 | 0 | 2 | 0.792 |
| L1 | 1 | C3 | 12/32 | 18 | 2 | 0.211 |
| L1 | 1 | C4 | 0/32 | 0 | 32 | 0.000 |
| L1 | 2 | C1 | 31/32 | 0 | 1 | 0.838 |
| L1 | 2 | C2 | 30/32 | 0 | 2 | 0.792 |
| L1 | 2 | C3 | 3/32 | 24 | 5 | 0.020 |
| L1 | 2 | C4 | 0/32 | 0 | 32 | 0.000 |
| L2 | 1 | C1 | 32/32 | 0 | 0 | 0.891 |
| L2 | 1 | C2 | 32/32 | 0 | 0 | 0.891 |
| L2 | 1 | C3 | 13/32 | 19 | 0 | 0.237 |
| L2 | 1 | C4 | 0/32 | 17 | 15 | 0.000 |
| L2 | 2 | C1 | 32/32 | 0 | 0 | 0.891 |
| L2 | 2 | C2 | 32/32 | 0 | 0 | 0.891 |
| L2 | 2 | C3 | 6/32 | 26 | 0 | 0.072 |
| L2 | 2 | C4 | 0/32 | 15 | 17 | 0.000 |

Prefilter 30 second set (same inputs, l2run.py): L1 identical (L1 does not use the parasail prefilter). L2 G, S and all NOT-NOVEL counts identical; NEAR/NOVEL splits differ slightly for C3 and C4, candidates NEAR 16 at prefilter 30 vs 17 at prefilter 20 (pilot_QKKIGKFAKLQEPE is the candidate that differs: NEAR at 20, NOVEL at 30).
| arm | draw | class | NOT NOVEL | NEAR | NOVEL | CP lower |
|---|---|---|---|---|---|---|
| L1 | 1 | C1 | 32/32 | 0 | 0 | 0.891 |
| L1 | 1 | C2 | 30/32 | 0 | 2 | 0.792 |
| L1 | 1 | C3 | 12/32 | 18 | 2 | 0.211 |
| L1 | 1 | C4 | 0/32 | 0 | 32 | 0.000 |
| L1 | 2 | C1 | 31/32 | 0 | 1 | 0.838 |
| L1 | 2 | C2 | 30/32 | 0 | 2 | 0.792 |
| L1 | 2 | C3 | 3/32 | 24 | 5 | 0.020 |
| L1 | 2 | C4 | 0/32 | 0 | 32 | 0.000 |
| L2 | 1 | C1 | 32/32 | 0 | 0 | 0.891 |
| L2 | 1 | C2 | 32/32 | 0 | 0 | 0.891 |
| L2 | 1 | C3 | 13/32 | 19 | 0 | 0.237 |
| L2 | 1 | C4 | 0/32 | 17 | 15 | 0.000 |
| L2 | 2 | C1 | 32/32 | 0 | 0 | 0.891 |
| L2 | 2 | C2 | 32/32 | 0 | 0 | 0.891 |
| L2 | 2 | C3 | 6/32 | 26 | 0 | 0.072 |
| L2 | 2 | C4 | 0/32 | 13 | 19 | 0.000 |

Candidates, per-candidate evidence: scoring file score_local_p20.json (per_query calls and best HSP) in the working copy; the L1 and L2 raw hit outputs are not committed (several hundred MB for L2 at prefilter 30). Committed here: scoring summaries only. Candidate NOT-NOVEL calls: none in either arm.

## Deviations and disclosures (all of them)
1. N1 pause. N1 started 2026-10-10 08:03 IST (22:33 ET Fri) after amendment 1. No reply came back for any RID. Frozen state at 2026-10-10T03:09:22Z (08:39 IST, 23:09 ET): first item c3_ADKLKPKLRKAWEE: 3 attempts used, RIDs CK3GGTVJ014 (submitted 21:00 ET, timed out at 60 min still WAITING), CK720A71016 (22:00 ET, timed out WAITING), CKAKFDKW014 (23:01 ET, in flight). Full run: 3 in flight with 1 attempt each: c3_AEKKAEKFMLKTDKL CK90BW8W014 (22:33:47 ET), c3_DAKKAQDHKRFKP CK90XUM0014 (22:34:05 ET), c3_EYKKDIKKHLKKEH CK91GHCD014 (22:34:23 ET), ~35 polls each, all WAITING; 220 items never submitted. Rationale: 60+ minutes WAITING for a 14-mer against nr suggests a backed-up NCBI queue (NCBI's page says searches from heavy users may be moved to a slower queue); the parent agent decided at 08:37 IST to pause submissions for a 4-hour backoff to avoid spending the resubmission budget against a backed-up queue. No error or throttle message was received. Poll-only checks of the 4 in-flight RIDs continue every 180 s without new submissions. Pause is a deviation from the continuous-run plan; N1 resumption will be published as an amendment.
2. N1 first-item-alone rule relaxed by amendment 1 (commit 8e379362673f2b974f6f49d10a63a5edaafeb0f8, 2026-10-10 02:33:22Z = 08:03:22 IST; the full run started at about 08:03 IST, committed immediately before start per commit timestamps, within clock precision). Authorised by the parent agent's message at 08:00:57 IST. Order relaxation and the resulting cap (92 per rolling 24 h: the first item's submissions are tracked in a separate state) disclosed.
3. L2 wrappers committed AFTER the runs they describe. l2run.py (commit 55daa7df492a5407924201c550a2b8c90ce54929, 08:04:49 IST) and l2run20.py (commit ada1e75ebf78d7f442b8e119b2764b1556e0ab5e, 08:05:16 IST) came after both L2 runs. The wrapper hashes show what was committed afterwards with readable code, not proof that the same bytes ran; the local files that ran had sha256 06e3b0d1f3bf44a209f87e9d95ef68c899fca1b65bdd393366625654a16171fe (l2run.py) and 14bbda9b5e7e0859e98ce4bc913909739f2aedc0e5c277f58678e2f666e55a46 (l2run20.py), identical to the committed files. The driver the wrappers import is r05_driver.py sha256 e40aa660528aaf98c4fd5a684ae4aea4a884c012d87b3ca3fc23fbe36e8cd7ed (the committed one).
4. L2 deviation history. The committed driver's L2 default (traceback prefilter score >= 20) exhausted the 2-CPU, 2 GB box. I first ran L2 with prefilter 30 through l2run.py (claim made: qualifying hits score >= 36). Independent verification showed this holds for NOT NOVEL calls (minimum qualifying score 34 over all 288 queries) but not for NEAR (ungapped NEAR alignments can score 25-29 for 81 of 288 queries). I then re-ran all 9 files at the committed prefilter 20 with l2run20.py v2 (the driver's _l2_worker logic copied verbatim plus a collection-time filter). Corrected claim: NOT NOVEL calls are unaffected by the prefilter; prefilter-30 NEAR counts are lower bounds; final numbers above are at prefilter 20.
5. L2 stored-HSP filter. The prefilter-20 output keeps only HSPs with coverage >= 0.8 and identity >= 0.7 (memory). The prereg says sub-80%-coverage hits are listed; for L2 they are not, so this result cannot list them. All calls are unaffected (the rule uses coverage >= 0.8 only).
6. Chunk split reproducibility. For l2run20.py the Swiss-Prot fasta (sha256 1372f18e218d761027616bf17479bcf450b30314fc0a8095fcb0e97e85d6ecf9) was split into 16 files: record i (0-based, in file order) goes to chunk sp{i mod 16:02d}.fa. Check: sorted lines of the concatenated chunks equal sorted lines of sprot.fasta (same digest). Per-chunk sha256: sp00=b8355def28b0ac18, sp01=523877e0a02cc822, sp02=0c6739ad5292ac5b, sp03=6bf416a4eb569e68, sp04=b6782a4a835aef59, sp05=2f472551d3b7f9ee, sp06=f3a3a1f9739d266f, sp07=7ab5c59f26a9055a, sp08=2de261c708183827, sp09=ae29257e0dad3d97, sp10=645ffe978a07211f, sp11=a85b40f47a0a4b75, sp12=1f62d3f38c7600e5, sp13=069032ade988f652, sp14=be94d8cbaf05ed7f, sp15=32c68b2fdb018917 (first 16 hex digits). Each (query, chunk) pair is a separate worker task; per-query HSP lists are concatenated.
7. Insulin format check. Two unscored submissions of an unrelated insulin sequence to the N1 settings, made at about 20:05 ET and 20:08 ET on Fri 2026-10-09 (05:35 and 05:38 IST), i.e. before the ET submission window (9 pm-5 am ET weekdays) opened; the first was orphaned when a local shell was killed, the second (RID CK0ER3SW014) was lost to a workspace reset while still WAITING, so the parser was never tested against a real NCBI JSON2_S reply. The prereg weekend wording ("today is Saturday") was IST-based; the NCBI rule is in US Eastern time (the window opened 21:00 ET).
8. Stale prereg title: the committed PREREG says "no driver written yet" in a header; the driver is committed and hash-pinned in the body. Cosmetic, not re-committed.
9. Workspace rebuilds. The sandbox was reset twice on 2026-10-10 (about 06:09 and 06:26 IST). I rebuilt from committed files and re-verified every pinned hash (driver, candidates, 10 control and manifest files, Swiss-Prot fasta, mmseqs binary). L1 was rerun after the first reset.
10. NCBI contact: requests carry tool=algo50-r05-audit and an agent mailbox as email, per the parent agent's decision.
11. Commit timestamps are author-set metadata. Committed before running per commit timestamps: driver, candidates, control manifests, prereg (00:23-00:28Z), before any scored query. No claim of independent public-push ordering.

## What this does and does not show
Supported: against Swiss-Prot, with the pipeline shown able to flag known Swiss-Prot sequences (G pass in both draws), none of the 32 candidates has a >= 90% identity hit over >= 80% of its length (L1, L2), so the "no Swiss-Prot near-duplicate" half of the claim reproduces. Not supported either way: novelty against NCBI nr (N1 not run). Not a novel method; a replication/audit of a negative-search claim. Novelty is not activity. Tally: the parent decides whether this counts.
