# DOC-2-089 One Function, Many Microbes - locked gates (22:10 IST, before data download)

## Sandbox-fit slice
MGnify/HMP metagenome-wide analysis does not fit the sandbox. Slice: KEGG complete-module calls for sampled prokaryotic genomes (KEGG REST link/module/<org>), covering 5 functions that have documented alternative KEGG routes:
- Lysine biosynthesis: M00016, M00525, M00526, M00527 (DAP variants), M00030, M00433 (AAA)
- Isoprenoid precursors: M00096 (MEP), M00095, M00849 (MVA variants)
- Glycolytic backbone: M00001 (EMP), M00008 (Entner-Doudoroff), M00633 (semi-phosphorylative ED)
- Heme: M00121 (protoporphyrin route), M00926 (coproporphyrin-dependent), M00847 (siroheme-dependent)
- Menaquinone: M00116 (classical), M00930, M00931 (futalosine)
Genomes: KEGG list/organism prokaryotes, one organism per genus, random sample of 150 (seed 0). Phylum = 3rd lineage field.
A genome's "route" for a function = the sorted combination of its complete modules from that list. Genomes with none are excluded for that function. Route classes used by < 5 genomes are pooled as "other".

## Questions
Q1 (lineage lock): is route choice explained by phylum? Cramer's V(route x phylum), permutation null (1000 shuffles of route labels).
Q2 (convergence): how many routes are used by >= 3 distinct phyla?

## Gates
G1 median Cramer's V across the 5 functions >= 0.40.
G2 permutation p < 0.01 in >= 4/5 functions.
G3 (convergence, descriptive but gated) >= 3 of the 5 functions have a route used in >= 3 phyla alongside a different route in the same phyla (both solutions within the same lineage).
Failure policy: negative preserved; pivots appended with new locked gates.

## Amendment A (22:11, before any module data): KEGG list/organism returns HTTP 400 today. Sampling changed to: list/genome -> random 600 entries (seed 0) -> lineage from get gn:<T> (LINEAGE line) -> keep Bacteria/Archaea -> one per genus -> random 150. Phylum = 2nd LINEAGE field after the domain. Everything else unchanged.
Amendment B (22:12, before any module data): KEGG LINEAGE lines are indented and include a kingdom rank (e.g. "Bacteria; Pseudomonadati; Pseudomonadota; ..."). Phylum = first lineage field ending in "ota" (fallback: 3rd field). Genus = second-to-last field. Candidate draw raised from 600 to 900 genomes so that ~150 prokaryotic genera remain.

## Primary result (22:14) - FAIL on G3, preserved
150 genomes, 25 phyla. G1 pass: median Cramer's V 0.81 (lysine 0.58, glycolysis 0.72, heme 0.81, isoprenoid 0.83, menaquinone 1.00). G2 pass: p <= 0.007 in 5/5. G3 FAIL: same-lineage alternative solutions only in 2/5 functions (lysine DAP variants, EMP vs ED); isoprenoid, heme and menaquinone show no phylum with two routes at this sample size.
Known issue: raw Cramer's V is biased upward with many sparse phyla (menaquinone n = 18 gives V = 1.0).

## Pivot 1 (locked 22:15, before computation): does lineage lock survive sparsity correction?
Restrict to phyla with >= 5 genomes (Pseudomonadota, Actinomycetota, Bacillota, Bacteroidota, Methanobacteriota, Mycoplasmatota). Bias-corrected Cramer's V (Bergsma 2013). Permutation null of 1000 shuffles. Functions with < 15 genomes after restriction are reported but count as failures.
P1-G1 corrected V >= 0.30 with p < 0.01 in >= 4/5 functions.
P1-G2 in each passing function, the modal route of >= 2 phyla differs (it is a lineage split, not one route everywhere).

## Pivot 1 result (22:15) - PASS 4/5 (menaquinone n = 14 counted as fail)
Corrected V: heme 0.77, isoprenoid 0.69, lysine 0.46, glycolysis 0.45; all p = 0.001; every passing function shows different modal routes across phyla.
