# algo50/18 - Beta-binomial vs fixed-threshold pileup for diploid SNP calling (simulated ground truth)

Status: LOCKED before any method-vs-method results were computed (lock time in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
At a heterozygous site a read sampler draws alt alleles ~Binomial(n, 0.5); at a homozygous-ref site alts come only from errors. Does a beta-binomial genotype-likelihood caller (het vs hom-ref vs hom-alt, error-aware) beat the classic fixed rules (>=20% alt and >=4 alt reads) at 30x, and where does each break at 8x?

## Data (simulated, ground truth known)
E. coli K-12 NC_000913.3 (sha256 in data/). Seed 1: sprinkle 2000 heterozygous + 1000 homozygous-alt SNPs at random positions (spacing >=50 bp, ACGT only, alt != ref). Reads: 300 bp single-end, uniform, 1% substitution error, at 30x and 8x, same read simulator as algo50/16 (seeded per chunk). Pileup at the 3000 variant sites plus 297,000 matched non-variant sites (every 16th eligible position).

## Task
Per-site genotyping: call het / hom-alt / no-call (hom-ref implied). Metrics per method at both coverages: het recall, het precision, hom-alt recall, false-positive rate on non-variant sites.

## Methods
- FT (fixed threshold): call het if alt_count>=4 AND 0.2<=alt_frac<=0.8; hom-alt if alt_frac>0.8 and alt_count>=4.
- BB (proposed): genotype likelihoods under binomial with error: P(data|hom-ref)=(e/3)^a(1-e/3)^n ... standard; het: 0.5^n; hom-alt: (e/3)^r(1-e/3)^a; priors 0.001/0.0005 per site (het/hom-alt); call max posterior genotype if posterior > 0.9 else no-call.

## Success gates
- G1: 30x BB het F1 >= FT het F1 + 0.02.
- G2: 30x BB false-positive calls on non-variant sites <= FT's.
- G3: 8x BB het recall >= FT + 0.05 at precision >= 0.9.
- G4: 30x BB hom-alt recall >= 0.95.
Project PASSES if G1 and G2 pass; G3/G4 boundary gates reported either way.

## Failure policy
Negative results recorded as-is; failed direction triggers a documented pivot with gates locked in an amendment.

## Notes locked in advance
- SNPs only, single-end reads, no mapping error, no indels, no base-quality variation: a best-case world for both methods; FT's simplicity may look artificially good here, which is itself a documented finding.
