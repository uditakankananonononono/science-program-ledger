# DOC-1-017 GATES - A "Protein Folding Grammar" Model for de novo Design
Locked 2026-09-24 06:24 IST by EXP-1 BEFORE any design, structure prediction, or PLL scoring.
Boundary-avoidance note (per program context): this is NOT "small PLM + linear head vs strong baseline on natural data" (the closed 011-015 boundary shape). The grammar is HAND-LOCKED literature rules with no learned model; PLM/predictor tools serve only as independent judges of a design question.

## The grammar (locked from de novo design literature: Woolfson 2021; Hecht binary patterning; Richardson & Richardson N/C-caps)
Designed sequence = amphipathic helix block(s) + loops:
- R1: helix body follows binary pattern (H P P H P P H)n: H sampled from {L,I,V,M,F,A}, P from {S,T,N,Q,E,D,K,R}.
- R2: N-cap from {S,T,N,D}; C-cap from {G,N}. Pro/Gly excluded from helix interiors.
- R3: net charge +2..+6 per sequence (solubility/aggregation rule).
- R4: 1-2 helix blocks joined by 3-6 residue loops sampled from {G,S,T,N}; total length 24-70.
Designs: N=200 sequences, seeded RNG (seed 42). Baseline: per-sequence composition-matched shuffle (seeded), destroying pattern while preserving length and composition exactly. Natural reference: 200 length-matched fragments from reviewed Swiss-Prot (seeded sample, documented in PROVENANCE).

## G1 - Structural validation by independent published tool
s4pred (Moffat & Jones, Bioinformatics 2021; psipred/s4pred v1.2.4, 5-model ensemble) secondary structure. G1 PASS iff mean helix fraction over designed sequences >= 0.40 AND >= 2x the baseline mean helix fraction. Single scoring pass.

## G2 - Independent PLM judge (ESM-2 pseudo-log-likelihood)
ESM-2 t6_8M masked pseudo-PLL (approximation locked here: R=8 replicates of 15% random masking; mean log-probability of true tokens at masked positions, per residue). G2 PASS iff PLL(design) EXCEEDS PLL(baseline) by >= 0.20 nats/residue AND PLL(design) >= PLL(natural reference) - 0.50 nats/residue. Single scoring pass.

## G3 - Periodicity interpretation
Hydrophobic periodicity of designed vs baseline (autocorrelation of Kyte-Doolittle hydrophobicity at lag 3-4, per Eisenberg hydrophobic-moment literature): designed helix blocks must show coherent 3.6-residue periodicity enrichment vs baseline. PASS iff coherent.

## G4 - Tool + nomination
grammar_design.py CLI: emit N grammar-designed sequences + their s4pred summary. Smoke-tested. Nomination: Woolfson lab (Bristol, de novo protein design) as prospective evaluator.

## Failure tree (locked)
ONE design batch (200+200 shuffles), ONE s4pred pass, ONE PLL pass. If G1 or G2 FAILS: no redesign, no threshold moves - documented boundary. Compute caps: 400 s4pred sequences; PLL on 600 sequences x 8 replicates.
