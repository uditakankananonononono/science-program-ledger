# DOC-1-015F: PPI Interfaces + Structure Geometry — GATES (locked 2026-09-24 12:29 IST, before any scoring)

Follow-up to DOC-1-015 (boundary: linear head on ESM-2-8M+PSSM stalls ~5 AUROC points below
frozen bars; mechanism: feature poverty at interface geometry; PSSM adds +0.002 over ESM-only).
Parent-approved sketch 12:27:53 (fresh gates, 008->METENG pattern; NOT a retry of 015's G2).
Eligibility verified 12:27: RCSB sequence API exact-hits Dset_72 seq0 (375 hits >=95%
identity, score 1.0); experimental mmCIF (strict upgrade over sketched predicted structures,
approved).

## Structure mapping (locked mechanics)
- Per protein (Dset_72 + Dset_164 frozen sets; Dset_186 train): decode integer sequences
  (alphabetical AA order, validated in 015); RCSB search API v2, service=sequence,
  identity_cutoff=0.95, evalue_cutoff=1e-20, return_type=polymer_entity.
- Selection: FIRST entity of result_set as returned by the API (its internal rank); no
  re-ranking. If zero hits -> protein dropped and disclosed in REPORT (per-set drop counts
  reported before any gate verdict; dropped proteins also dropped from that arm's scores on
  BOTH arms so every comparison stays same-set).
- Chain CA coordinates from experimental mmCIF (files.rcsb.org); first model only.

## Arms
- ARM E (the claim): 015's multimodal features (ESM-2-8M residue embeddings 320d + PSSM 20d)
  + per-residue geometry block (4d): contact-graph degree (CA-CA <= 10A), 2-hop degree,
  local packing density (CA count within 10A sphere), normalized exposure proxy
  (1 - degree/max_degree over the protein). Same logistic head C=1.0, same 183/71/164
  proteins (015's exact splits after its locked truncation rule), same training protocol.
- ARM M-control: 015's multimodal arm re-trained and re-scored on the SAME mapped protein
  sets (same-set control; 015's committed 0.6697/0.6310 are the cross-set anchor).

## Gates
- G1 (sanity): ARM E train-cohort metric >= ARM M-control train-cohort metric (coherence;
  exact dev protocol disclosed in REPORT). Else incoherent - halt to parent.
- G2 (the claim, frozen): ARM E Dset_72 AUROC >= ARM M-control Dset_72 + 0.03 AND
  ARM E Dset_164 AUROC >= ARM M-control Dset_164 + 0.03 (parent ruling 12:27:53: +3pp over
  the BEST 015 arm, not PSSM-only).
- G3 (mechanism): geometry-block ablation - geometry-only arm vs multimodal-only control;
  does geometry carry interface signal the PLM already has (015's PSSM +0.002 story) or new
  signal? Report coefficient signs vs hot-spot literature (aromatic/charged enrichment).
- G4: CLI ppi_interface_geo.py + REPORT.md + prospective nomination.
- Failure tree: G1 fail -> halt to parent. G2 fail -> documented boundary (geometry was THE
  mechanism-targeted fix; no further rescue pre-registered). G2 pass + G3 shows geometry
  adds < +0.005 over multimodal -> finding: geometry is already inside the PLM; parent
  adjudicates.
