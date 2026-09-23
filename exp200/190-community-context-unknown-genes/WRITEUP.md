# DOC-2-090 Community Context of Unknown Genes - sandbox slice (exp200/090)

**Outcome: PASS on all locked gates, in both organisms.**

## Setup
The full MGnify/HMP metagenome co-occurrence approach did not fit the sandbox (2 CPU / 1 GB). As a proxy for "community context" I used the phylogenetic co-occurrence channel of STRING v11.0: which genomes carry the gene alongside which other genes. Two independent organisms: E. coli K-12 and B. subtilis 168. Labels are KEGG pathways (global maps removed). Each gene's labels were hidden and its top-1 pathway predicted from a score-weighted vote of its co-occurrence neighbours (score >= 400). Null: 200 label shuffles.

## Results
| | E. coli | B. subtilis |
|---|---|---|
| co-occurrence precision (gate >= 0.30) | 0.760 | 0.751 |
| null / fold (gate >= 3x, p < 0.01) | 0.045 / 16.7x, p = 0.005 | 0.044 / 17.1x, p = 0.005 |
| coverage (gate >= 0.15) | 0.72 | 0.65 |
| gene neighbourhood precision / coverage | 0.63 / 0.80 | 0.56 / 0.82 |
| co-expression | 0.67 / 0.55 | 0.68 / 0.41 |
| textmining | 0.74 / 0.90 | 0.75 / 0.89 |
| database channel (KEGG-derived, leakage ceiling only) | 0.88 | 0.88 |

Co-occurrence context gave the most precise non-leaky call in both species. It beat operon neighbourhood by 13-19 points of precision, and neighbourhood covered more genes. Precision rises with vote share: 0.29-0.33 when the vote share is <= 0.5, 0.61-0.66 at 0.5-0.8, and 0.85-0.86 above 0.8. That makes the vote share a usable confidence score.

## Useful output
Calibrated pathway calls for genes with no KEGG pathway: 1,119 in E. coli and 949 in B. subtilis. 502 in each species have a vote share > 0.8 (expected precision ~85%). Files: results/unknown_predictions_{eco,bsu}.csv.

## Honest novelty and limits
- Phylogenetic profiling for function prediction is established (Pellegrini et al. 1999). This work contributes a same-framework head-to-head of context channels with calibration in two organisms, plus the prediction lists. It is not a new method.
- "No KEGG pathway" does not mean uncharacterized. Many of these genes are known but outside KEGG maps.
- Co-occurrence here is phylogenetic, not measured metagenomic abundance co-occurrence. The metagenomic version is untested.
- The p-value floor is set by the 200 permutations.
- Pathway labels overlap (a gene can sit in several pathways), and a top-1 hit is counted if it matches any of them.

## Reproduce
python3 code/run.py; python3 code/predict_unknown.py. Data URLs are in GATES.md and checksums in data/SHA256SUMS.
