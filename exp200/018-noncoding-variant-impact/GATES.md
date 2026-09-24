# DOC-1-018 GATES - locked 2026-09-24 06:41 IST BEFORE any feature fetch or scoring
Topic: Predicting the impact of non-coding variants (program names AlphaGenome).
Access check (done pre-gates): AlphaGenome API is free for non-commercial use but requires a
user-held API key obtained via Google sign-in + ToS acceptance at deepmind.google.com/science/alphagenome.
No key exists in the user's vault (checked 06:39). Obtaining one is a user-side account/ToS action.
=> Public-data substitute arm executes now; AlphaGenome head-to-head is Addendum A1 pending a user key.

## Cohort (locked; counts checked for eligibility only, no outcomes seen)
ClinVar VCF GRCh38 release 2026-09-14 (ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz, 193,709,143 bytes).
chr21/chr22 SNVs (len(ref)=len(alt)=1), non-coding molecular consequences only
(UTR/upstream/downstream/intron/intergenic/non_coding/regulatory_region/TF_binding/splice*;
any coding-impact consequence excludes the variant).
Labels: CLNSIG Pathogenic|Likely_pathogenic|Pathogenic/Likely_pathogenic = P;
Benign|Likely_benign|Benign/Likely_benign = B; all others dropped.
Counts: chr21 642P/6660B, chr22 1460P/10608B. Benigns subsampled 3:1 per chromosome (seed 7):
dev = chr21 (642P + 1926B), frozen test = chr22 (1460P + 4380B), untouched until G2.

## Features (locked; UCSC Genome Browser REST API, hg38, api.genome.ucsc.edu)
f1 phyloP100way at variant base (named published baseline, Pollard et al. 2010)
f2 phastCons100way at variant base (named published baseline, Siepel et al. 2005)
f3 mean phyloP over +/-10bp window
f4 GC fraction +/-25bp (getData/sequence)
f5 CpG density +/-25bp
f6 cCRE overlap within +/-25bp (track encodeCcreCombined; 0/1)
Missing values: variant dropped and counted (report drop rate; if >10% of either class, flag in REPORT).

## Model (locked)
Logistic regression, L2 C=1.0, class_weight='balanced', standardized features, sklearn.
Composite = all 6 features. Fit on chr21 ONLY. No chr22 row is read until the composite is frozen.
Baselines: phyloP-only score; phastCons-only score (raw per-base values).

## Gates
G1 (dev, chr21): 5-fold stratified CV (seed 7) mean AUROC of composite >
   phyloP-only CV AUROC + 0.03 AND > phastCons-only CV AUROC + 0.03. Else document loss.
G2 (frozen, chr22): frozen composite AUROC >= 0.65 absolute AND >=
   max(phyloP-only, phastCons-only frozen AUROC) + 0.01. Single scoring pass, no refit.
G3 (mechanism vs literature): leave-one-feature-out AUROC deltas on dev CV + cCRE/conservation
   enrichment of pathogenic variants, interpreted against the conservation-dominance literature
   (e.g., non-coding pathogenicity concentrates at constrained sites; cCRE/regulatory context expected second).
G4: CLI score_variant.py (chrom pos ref alt -> features + composite score) smoke-tested on 3
   locked smoke variants + one prospective lab nomination.

## Failure tree (locked)
G1 fail -> P1: add 3-mer motif LR features; P2: stratum-restricted arms (splice-region-only, UTR-only).
If no arm beats both baselines by the locked margins -> documented boundary: conservation saturates
non-coding ClinVar signal in this envelope. Thresholds never relax after outcomes.

## Addendum A1 (named, not executed)
If the user obtains an AlphaGenome API key, score the identical frozen chr22 cohort through the API
for a head-to-head vs the composite (same locked metrics). No new gates needed; metrics locked here.
