# 019F: metagenome-signature-decomposition (DOC-1-019F)
Boundary report. Parent adjudication 2026-09-24 14:01 IST: boundary, NOT counted.

## Question
019 found halophile metagenome proteins are LESS acidic (D+E) than the control biome -
the opposite of organism-scale halophile biology ("salt-in" proteomes are acidic).
019F decomposes the metagenome into halophile-origin vs non-origin proteins to test
whether the inversion is (a) dilution of a real halophile signal by a non-halophile
community, or (b) ecology not reducible to salt-in composition.

## Gates (locked 9925f404 pre-scoring; Addenda A 9119aaef, B pre-scoring 13:50)
- G0 organismal premise, halt-no-patch: (i) median D+E of 100 Halobacteria reference
  proteomes >= 100 bacterial reference controls +5pp; (ii) median IVYWREL of 83
  thermophile reference proteomes > control median.
- G1 (dev, MGYS00005861, 019's committed hypersaline_dev.fasta): MMseqs2 -s 7.5
  e<=1e-5 qcov>=0.5 origin assignment vs the 100-proteome Halobacteria DB;
  assignment rate >= 10% floor; median D+E(halo-origin) >= D+E(non-origin) + 3pp.
- G2: identical, single pass, on frozen Santa Pola Saltern MGYS00000384.
- G3 (documented): dilution arithmetic + MGnify SSU consistency.
- G4: signature_decompose.py CLI (code/), this report.

## Results
- G0: PASS both clauses. Halo D+E 16.97% vs control 11.87% (+5.10pp, bar +5pp),
  halo n=100, control n=100 full coverage. Thermophile IVYWREL 44.66% vs control
  39.46% (strict pass), therm n=83. Organism-scale signatures confirmed:
  halophiles ARE acidic-proteomed, thermophiles ARE IVYWREL-enriched.
- G1: FAIL. Assignment 17.4% (floor 10% PASS; 522/3000). Halo-origin D+E median
  13.13% vs non-origin 10.24% = +2.88pp < +3pp bar.
- G2: FAIL (single pass). Assignment 12.07% (floor PASS; 362/3000). Halo-origin
  15.67% vs non-origin 13.21% = +2.46pp < +3pp.
- G3: dilution arithmetic - dev: predicted bulk 12.75% (r=17.4% mixture of 16.97%
  halo and 11.87% control proteomes) vs observed 11.04%. Frozen: predicted 12.48%
  vs observed 13.49%. Mixing arithmetic does not reproduce either observed bulk,
  and the two misses run in opposite directions. SSU consistency: Santa Pola
  k__Archaea 8.9% of SSU assignments vs 12.07% protein-level origin assignment -
  same order, consistent.

## Interpretation vs literature
Oren's salt-in proteomics and Fukuchi 2003 / Zeldovich 2007 predict exactly the G0
organism-scale pattern, which held. The community-level test fails the locked bar
in BOTH independent cohorts, in the same direction (halo-origin proteins ARE more
acidic, but by +2.5-2.9pp, under the +3pp bar), while dilution arithmetic fails to
reproduce the observed bulk in both cohorts. 019's hypersaline inversion is
therefore NOT cleanly decomposable into halophile-origin dilution at MMseqs2
-s 7.5 resolution: the community signal is an ecology property (who is there and
what their non-salt-in proteomes look like), not a transportable salt-in signature
of the fraction assigned to Halobacteria.

## Verdict
G0 PASS, G1 FAIL clause, G2 FAIL clause. Locked failure tree: G1/G2 miss = the
inversion is ecology, documented with numbers; parent adjudicates counting.
Parent ruling 14:01 IST: boundary, not counted (53/100 unchanged).
