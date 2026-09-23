# algo50/27 - Co-expression for guilt-by-association: Pearson vs mutual rank vs CLR on GTEx tissues

Status: LOCKED before any method was scored (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Co-expression networks are usually built with Pearson correlation (PCC). Obayashi & Kinoshita 2009 (DNA Res 16:249) argued the mutual rank (MR) of correlations finds functional partners better, and CLR (Faith et al. 2007, PLoS Biol) z-scores correlations against each gene's background. On human tissue profiles, does MR find genes that share a pathway better than PCC and CLR?

## Data
- Expression: GTEx v8 gene median TPM, 52 tissues (cell lines dropped), log2(TPM+1), genes with max TPM >= 1.
- Truth: Reactome (current release) leaf pathways (no child pathways) with 10-200 genes; two genes are partners if they share >= 1 such pathway.
- 8124 genes present in both; 1038 pathways. URLs, time, sha256 in data/.

## Methods (all over the same 8124 genes)
- PCC; SCC (Spearman, reported, not gated).
- MR: for genes i,j, r_i(j) = rank of j among i's PCCs (1 = highest); MR = sqrt(r_i(j) x r_j(i)); score = -MR.
- CLR: z_i(j) = (PCC_ij - mean_i)/sd_i over i's row; score = sqrt(max(0,z_i(j))^2 + max(0,z_j(i))^2).

## Metrics
For every gene with >= 1 partner: AUROC for ranking all other genes (partner vs not), and precision among its top 50. Averaged over genes. 95% CIs by 2000 bootstrap resamples of query genes, paired.

## Success gates (declared before scoring)
- G1: AUROC(MR) - AUROC(PCC) >= 0.01, CI lower bound > 0.
- G2: P@50(MR) - P@50(PCC) >= 0.005, CI lower bound > 0.
- G3: AUROC(MR) - AUROC(CLR) > 0, CI lower bound > 0.
All reported pass or fail; one post-hoc pivot allowed, locked first.

## Amendment 1 (implementation only, before any output)
The first run was killed for memory (four full 8124x8124 matrices) before printing anything. CLR z-scores and Spearman rows are now computed per query gene from the same quantities. No method change.

## Amendment 2 - pivot (POST HOC, locked before the pivot was scored)
Original result preserved (results/metrics_original.json): G1 FAIL (MR - PCC AUROC +0.003), G2 FAIL (MR slightly worse at P@50), G3 PASS (MR > CLR by +0.0025). All measures are weak here (AUROC ~0.61) and within 0.02 of each other. Pivot, designed after seeing that: a second-order measure that may denoise a 52-dimensional profile.
- SNN (shared nearest neighbours, Jarvis & Patrick 1973): each gene's top-50 genes by PCC; score(i,j) = |N_i intersect N_j| / 50, ties broken by PCC (+ 0.001 x PCC).
- P1: AUROC(SNN) - AUROC(PCC) >= 0.01, CI lower bound > 0. P2: P@50(SNN) - P@50(PCC) >= 0.005, CI lower bound > 0. Same genes, truth, metrics and bootstrap. No further pivots.
