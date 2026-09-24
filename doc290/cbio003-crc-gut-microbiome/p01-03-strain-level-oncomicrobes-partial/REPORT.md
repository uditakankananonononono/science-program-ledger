# P01-03 Build Report (PARTIAL SCOPE): Virulence-Locus Resolution vs Genus for CRC Transport

**Parent:** CBIO003 CRC Gut Microbiome (2025) | **Spec:** doc290/cbio003-crc-gut-microbiome/03-strain-level-oncomicrobes.md
**Built:** 2026-09-24 | **Scope:** partial, parent-approved - locus arm of G1 + G3 only. Strain profiling and G2 (pks vs SBS88) not built; see README.md and ../03-BLOCKERS-p01-03.md.
**Status:** G1 (locus arm) FAIL; G3 satisfied. Tool locked in db6b5be1 before any result.

## What was built
`tool/locusres.py` - identical gradient-boosted classifiers (HistGradientBoosting, max_iter 150,
early stopping, seed 7) at four resolutions on identical leave-one-cohort-out (LOCO) folds, with
per-cohort paired bootstrap tests against genus.

## Data (frozen in data/)
Frozen P01-01 benchmark (767 samples, 8 cohorts; names per erratum): genus_matrix.csv (164 genera),
species_matrix.csv (849 mOTU species, 5% prevalence used), locus_matrix.csv = per-sample log10
abundances of clb (pks island), bft, fadA and bai from Wirbel 2019 (doi:10.1038/s41591-019-0406-6)
MOESM8 Panel_c + MOESM9 Panel_c; 767/767 samples matched, 0 label mismatches.

## Locked amendments
- Partial scope (strain level and G2 not built).
- Loci from published per-sample tables instead of ShortBRED/hmmsearch on raw reads.
- G1 count kept at 4 cohorts while the benchmark has 8 (spec said 4 of 6).

## Results vs locked gates
| resolution | mean LOCO AUC |
|---|---|
| genus | 0.830 |
| species | 0.820 |
| genus + locus | 0.819 |
| locus only (4 genes) | 0.632 |

| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 (locus arm) | locus beats genus by >= 0.05 (paired p<0.05) in >= 4 cohorts | 0 of 8 (locus worse in all 8, by 0.09-0.31) | **FAIL** |
| G3 | identical folds, all resolutions reported | yes | **satisfied** |

Reported, no gate: genus+locus vs genus - no cohort gains >= 0.05 (range -0.070 to +0.033);
species vs genus - no cohort gains (range -0.035 to +0.027).

## What the result means
1. **Four toxin/virulence genes alone carry real but weak signal (0.63)** - far below genus-level
   community composition (0.83).
2. **Adding them to genera adds nothing** (0.819 vs 0.830): the genus profile already captures what
   clb/bft/fadA/bai carry, likely through the taxa that host them (e.g., Fusobacterium for fadA).
3. **Finer taxonomy doesn't help either**: species (849 mOTUs) = genus. At the resolutions testable
   with open processed data, resolution is not the bottleneck for CRC transport.
4. **Not tested:** strain-level resolution and the pks-SBS88 mutational link, which were the spec's
   main hypothesis. This partial build does not speak to them.

## What this build needs next
- Strain profiling on raw reads (StrainPhlAn 4/inStrain) on a machine with enough memory/storage.
- Controlled-access PCAWG/TCGA signature data for G2.
