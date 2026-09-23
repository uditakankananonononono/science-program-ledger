---
id: P03-05
title: "Complex-Aware Drug Design: Catalytic vs Allosteric Targeting Across the Full PRC2 Complex"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# Complex-Aware Drug Design Across the Full PRC2 Complex

**Parent project:** CBIO008T - targets EZH2 as an isolated protein; EZH2 is only stable/active inside PRC2 (with EED, SUZ12, RBBP4/7).

## Premise
Designing against monomeric EZH2 misses the druggable reality: the catalytic SET domain, the EED allosteric site, and the H3K27me3-reading interfaces have different druggability and resistance profiles in the assembled complex.

## Hypothesis
Docking-based druggability ranking across all PRC2 complex structures identifies >= 1 allosteric site with better predicted ligandability than the catalytic site, and complex context changes the hit list vs monomer docking.

## Data sources (free/public)
- PDB PRC2 holo complexes (multiple conformational states, with inhibitors bound).
- ChEMBL EED and SET-domain inhibitor series with potency labels.

## Method outline
1. Assemble all public PRC2 structures; map known inhibitor binding modes per site.
2. Dock matched compound series into catalytic vs allosteric sites in monomer vs complex contexts; compare score distributions and pose fidelity to crystal poses (RMSD <= 2 A recovery rate).
3. Rank sites by druggability (open DoGSiteScorer) + docking enrichment on site-specific actives.

## Success gates (locked before results)
- G1: pose recovery >= 60% at RMSD <= 2 A for co-crystallized ligands per site, else that site's docking is declared unreliable.
- G2: per-site EF1% with CIs on site-matched actives; a site-level winner declared only at non-overlapping CIs.
- G3: monomer-vs-complex hit-list overlap reported; if overlap >= 80%, complex modeling declared non-informative (a real negative).

## Expected deliverable
`prc2site`: a site-level screening toolkit with the frozen structure ensemble, per-site benchmarks, and a druggability-ranked PRC2 site map.

## Failure/pivot rule
If complex context changes nothing, publish that - monomer EZH2 docking is sufficient and the cheaper pipeline is justified with evidence.
