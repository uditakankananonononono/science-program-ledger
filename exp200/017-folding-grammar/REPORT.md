# DOC-1-017 REPORT - A "Protein Folding Grammar" Model for de novo Design
EXP-1, 2026-09-24. Gates locked BEFORE design (commit 38e47ffa). VERDICT: all four locked gates PASS - submitted for adjudication.

## Design (locked grammar, GATES.md; no learned model)
200 sequences, (HPPHPPH)n amphipathic binary pattern + N/C-caps + GS-rich loops, net charge +2..+6, length 24-70. Baseline: composition-matched shuffles. Natural reference: 200 Swiss-Prot length-matched fragments.

## Results (single scoring passes)
- G1 (s4pred structural validation): designed mean helix fraction 0.867 (locked bar >= 0.40) AND 2.26x baseline 0.384 (locked bar >= 2x): PASS. Natural reference 0.299. Composition-matched shuffles keep 0.384 helix (composition alone carries helix propensity); the grammar more than doubles it.
- G2 (ESM-2 pseudo-PLL judge, R=8, 15% masking): designed -2.714 vs baseline -2.941 (margin +0.227, locked bar >= 0.20) and vs natural -2.617 (gap -0.097, locked bound >= -0.50): PASS. An independent PLM trained on natural proteins scores grammar designs essentially as protein-like as natural sequences.
- G3 (hydrophobic periodicity, KD autocorrelation lag 3-4): designed -0.0147 vs baseline -0.0222: formally PASS as locked, BUT the absolute signal is weak - documented finding below.
- G4: grammar_design.py CLI (emit N designs with charge/length), smoke-tested; Woolfson lab (Bristol) nomination.

## The G3 nuance (real design-rule finding)
The locked (HPPHPPH)n pattern places H at 0,3,6 then 7,10,13 across repeats - creating i,i+1 H-H junctions at block boundaries that fight the i,i+3 amphipathic register. Helix FORMATION (G1) and protein-likeness (G2) do not require clean periodicity, so both pass strongly, but the amphipathic register that would drive bundle assembly is only weakly present. A period-pure pattern (e.g., (HPPHPPH)n with junction-aware phasing or heptad (abcdefg)n with a/d hydrophobic) is the concrete next grammar revision - a fresh hypothesis needing its own gates, not an arm here.

## Why this one is different from the 011-015 boundaries
The small PLM was never the method under test; it was the judge. The hypothesis - that 40-year-old hand-written folding rules suffice to write sequences that two independent modern tools call helical and protein-like - is CONFIRMED. Design-by-grammar works at zero model cost.

## Honest limits
s4pred predicts propensity, not structure; ESM-2 PLL is an approximation (locked R=8/15%); no experimental aggregation/solubility data; natural reference fragments are cytosolic-leaning random Swiss-Prot, not fold-matched.
