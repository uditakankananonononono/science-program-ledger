# algo50/76 - ORF finding: longest-ORF vs codon-scored six-frame search

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55). Data: NC_000913.3 (hash in data/SHA256_raw.txt).

## Bottom line
Three findings, none matching the naive expectation: (1) MEAN hexamer log-odds per codon is a broken scorer - its 1/length variance favors tiny ORFs (2.3% correct-stop); switching to TOTAL log-odds lifts the same method to 34.7% on identical loci. Aggregation choice is the whole ballgame. (2) Scoring CANNOT beat longest-ORF when the confusion is with real neighboring genes (+-3kb flanks: longest 16.1%, scored 15.7%; +-1kb: 38.5% vs 34.7%) - neighbors are real coding sequence and score as coding. (3) 41% of longest-ORF errors at +-3kb are OTHER REAL GENES (stop matches a true CDS elsewhere): the "longest is real, just elsewhere" effect - locus definition, not scoring, is the bottleneck.

## Gates
- Original: G1/G3/G4 FAIL, G2 PASS (longest fails 84% of loci at +-3kb).
- Amendment 1: P1 FAIL (scored ~ longest, not +0.10), P2 FAIL (34.7% < 60%), P3 PASS (41% neighbor-gene errors).
All failures preserved and explained above; no third amendment - the neighbor-confusion boundary is the finding.

## Caveats
- Start-codon correctness excluded by design (stop+frame criterion); GTG/TTG starts truncated to downstream ATG, which can still match stop.
- Hexamer table trained on the same genome's other genes (750/750 split, no leakage of the tested locus's own row but same-genome statistics).

## Reproduce
`python3 code/run.py` (original), `code/pivot.py` (total-score + flank comparison); biopython+numpy, ~30 s.
