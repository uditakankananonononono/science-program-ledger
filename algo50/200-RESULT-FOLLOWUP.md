# 200 R-05 RESULT follow-up 1 (2026-10-10)

This file corrects forward. It does not replace 200-RESULT.md, committed at 4c3b9b18277492c1eecbd393941d0f622c71976d (sha256 ec52f93a71c315b7c50aaa5aa96bdafb62125ae8d8584b840eb6b5867ae96885). That commit stands as published.

## 1. Original claim vs what was reproduced
The original claim, quoted in the prereg, is "zero alignments at the reporting floor in both arms for all 32" under the rule "no hit >= 90% identity over >= 80% of length". The 90/80 rule is reproduced (0 NOT NOVEL in L1 and L2). But L2 finds 17 candidates with NEAR hits (identity 70-90%, coverage >= 80%), so "zero alignments" is not reproduced in L2 (L1 has 0 NEAR). The label reproduces the 90/80 novelty rule only. The original "zero alignments" wording is not reproduced in L2 at the NEAR level.

## 2. Wording fix (claim 5)
4c3b9b18 says the L2 NEAR rate for candidates is "at chance". Corrected wording: the L2 NEAR rate for candidates is similar to the shuffled controls (C4 NEAR in L2: 17/32 in draw 1, 15/32 in draw 2; candidates 17/32 at prefilter 20, 16/32 at prefilter 30). NEAR counts at prefilter 30 are lower bounds.

## 3. N1 headline addition
N1 (nr) status: submitted, no reply. NOT RUN, paused by the parent's decision at 2026-10-10 08:37 IST (disclosed in 200-RESULT.md). Six RIDs were submitted and none returned a reply: first-item CK3GGTVJ014 and CK720A71016 timed out, CKAKFDKW014 in flight; full run CK90BW8W014, CK90XUM0014, CK91GHCD014 in flight. No N1 result exists. The N1 amendment will be published when N1 resumes or resolves.

## 4. Evidence files (sha256 of committed file contents)
- 5caf007f476e8a36b945c446f3fc01ae807ef171536c38aab64e0c03853941be  200-score_local_p20.json.md
- 86528806304e0f28a500ce2bed70a526af56fe26ada54b6d1bce39873b0abd3d  200-score_local_p30.json.md
- af490a6a5b10b4777fb5d2be2c9da8b693be23371868af9c9d3b32297c5cfea3  200-l1.m8.tsv.md
- f98bd6b4148c9b58ce869df0d22674ac824fa452e8d41f2409eb2b4473c79e8e  200-l2_p20_filtered_hsps.json.md
- (L1 m8 is the tsv; the p20 filtered HSPs are l2_merged_p20.json compacted)
