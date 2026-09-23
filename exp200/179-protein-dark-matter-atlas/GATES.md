# DOC-2-079 The Protein "Dark Matter" Atlas - locked gates (written 2026-09-23 21:50 IST, before any outcome data is joined)

## Sandbox-fit slice
Full atlas (UniProt+InterPro+STRING+AFDB triangulation, dated UniProt snapshots) does not fit 2 CPU / 1 GB RAM. Slice: human placeholder-named genes, a dated network snapshot, dated outcome from HGNC renames.

## Question
Among human genes carrying a placeholder symbol (C#orf#, FAM#, KIAA#, TMEM#, CCDC#, LOC-style) on 2019-01-01, does network evidence in a pre-T0 snapshot (STRING v11.0, released Jan 2019) predict which get a functional (non-placeholder) HGNC symbol after 2019-01-01?

## Data (public, checksummed in data/SHA256SUMS)
- HGNC complete set (current), https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt
- STRING v11.0 human links + protein info, https://stringdb-static.org/download/...v11.0/

## Cohort / outcome
- Dark at T0: current placeholder symbol with date_symbol_changed empty or < T0 and approved before T0 (still dark = negative), OR current functional symbol whose prev_symbol includes a placeholder and date_symbol_changed >= 2019-01-01 (positive).
- Genes renamed before T0 excluded.

## Features (all from pre-T0 STRING v11.0 only)
F1 degree at combined score >=700; F2 degree >=400; F3 sum of scores; F4 fraction of >=700 neighbours that are non-placeholder genes (neighbourhood characterisation); F5 max score. Baseline B0: protein length proxy is NOT used (not in STRING info reliably) - baseline is F2-free "any STRING presence" indicator.

## Primary gate (all must hold)
G1 Logistic model (F1-F5, 5-fold stratified CV) AUROC >= 0.65.
G2 95% bootstrap CI lower bound (1000 resamples, gene unit) > 0.55.
G3 Beats presence-only baseline by >= 0.05 AUROC.
G4 Label-permutation control AUROC within 0.45-0.55.

## Leakage audit
STRING v11.0 textmining channel can already reflect pre-rename literature on the gene - this is legitimate pre-T0 signal, but report an ablation without textmining (needs channel scores: from links.detailed if memory allows; otherwise stated as unaudited).

## Failure policy
Negative stays. Pivot allowed only with new gates locked here before the new result, appended below as "Pivot N".

## Amendment A (21:52, before any outcome join): STRING info file carries protein_size, so a length-only baseline B1 is added. G3 becomes: beats max(B0, B1) by >= 0.05 AUROC. Mapping: STRING v11 preferred_name (the 2019 symbol) matched to HGNC current symbol or prev_symbol.

## Primary result (21:50) - FAIL, preserved
AUROC 0.581 (95% CI 0.541-0.624) < 0.65; presence-only baseline 0.581, so G3 fails; permutation 0.497. Diagnosis: presence baseline is a mapping artifact - 91% of still-dark genes map to STRING v11 by symbol vs 72% of later-renamed genes (renamed genes often carried more than one placeholder symbol). Univariate network AUROCs were all < 0.5 on the full cohort (unmapped filled with 0) - observed, so NOT reused as a new hypothesis.

## Pivot 1 (locked 21:53, before computation): does the 2019 network predict WHAT function the gene was later given?
Cohort: positives (renamed after T0) that map to STRING v11, have a current HGNC gene_group, and have >= 3 STRING v11 neighbours at score >= 700 that carry an HGNC gene_group.
Excluded uninformative groups (both sides): names containing "open reading frame", "family with sequence similarity", "Coiled-coil domain containing", "Transmembrane proteins", "uncharacterized", "KIAA", "Long non-coding".
Prediction: top-3 most frequent gene groups among the gene's >= 700 neighbours (2019 network).
P1-G1 hit rate (renamed gene's current group in its top-3) >= 20%.
P1-G2 >= 3x the null mean, empirical p < 0.01 (1000 permutations shuffling neighbour sets across eligible genes).
P1-G3 n eligible >= 40.
Leakage note: gene groups are current; a group created at rename time that includes 2019 neighbours is exactly the signal claimed, but it is reported.

## Addendum F (22:10, forward application requested by parent, relaying user feedback): no new gate - applies the Pivot-1 method, frozen as validated, to genes still dark today.
Cohort: current HGNC approved protein-coding genes with a placeholder symbol (same regex). Network: STRING v12.0 (current), score >= 700. Groups: current HGNC gene groups, same exclusion list. Nomination = top-3 neighbour gene groups, reported with neighbour count and vote share. Eligibility identical to Pivot 1 (>= 3 grouped neighbours). Expected accuracy carried from the retrospective test: 44% top-3 (18/41, 95% Wilson CI shown in the writeup), valid only for eligible genes.
Display rules (set before reading the ranked list in detail, disclosed): the host-gene groups "MicroRNA protein coding host genes" and "Small nucleolar RNA protein coding host genes" are dropped from nominations (they describe a locus, not a function; one such false hit was already noted in Pivot 1). A flag marks genes already in their top nominated group today (named placeholder, but already classified - not a new nomination).
