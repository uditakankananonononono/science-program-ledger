# SP-003 Round 2 - Deep Orthogonal Validation of 468 Metagenomic PET-Hydrolase Candidates

**Project:** DOC-1-016 Round 2 (multi-round mandate: depth over breadth)
**Protocol:** locked 2026-09-21 21:35 IST, sha256 `f665fc0da55e4b0e6317fa9a31a27191dffa17f609ad4009328f8ab15ce077e6` (`protocol/protocol.json`), before any candidate-level Round-2 result was inspected.
**Locked-gate outcome: overall FAIL - 5 of 7 gates pass (G1, G2, G5, G6, G7); 2 gates fail and are preserved verbatim (G3, G4).** Gate text was never modified after lock.

## 1. Question

Which of the 468 Round-1 MGnify PET-hydrolase candidates survive orthogonal domain, catalytic-residue, structure, provenance and false-positive scrutiny, and which 20 form an experimental-ready prioritized shortlist?

Round 1 established sequence-level discovery: 16 live-verified reference PET hydrolases searched against MGnify30-C2 (128.7M sequences) yielded 2,362 hits filtered to 468 novel candidates (<45% identity to every reference, E<=1e-10, length and physicochemical filters), with cross-catalog replication (21/21 testable candidates replicated in MGnify30-C5-ppfam), 5 scrambled-sequence controls (0 hits), and a UniProt novelty screen. Round 1 was necessary but not sufficient: phmmer similarity does not establish domain architecture, catalytic competence, structure modelability, environmental context, or freedom from esterase-family false positives. Round 2 attacks exactly those five axes.

## 2. Locked success gate (verbatim) and outcome

| Gate | Locked text (abbrev.) | Threshold | Observed | Verdict |
|---|---|---|---|---|
| G1 | pre-execution grounding verified live | triad + PF12740 + hmmscan route + provenance route 5/5 | all verified pre-lock / pre-bulk | PASS |
| G2 | hmmscan annotation coverage | >=90% of 468 | 468/468 (100%) | PASS |
| G3 | PF12740 best-E domain coherence | >=60% of annotated | 133/468 (28.4%) | **FAIL** |
| G4 | intact catalytic triad S-D-H at IsPETase-aligned positions | >=200 | 45 | **FAIL** |
| G5 | environmental provenance resolved | >=150 | 468/468, 141 studies | PASS |
| G6 | clustering reported; anti-panel flag rate | reported; <20% | 468 singleton clusters; 0% | PASS |
| G7 | shortlist of exactly 20, all checks | 20 with triad+PF12740+unflagged+structure-or-exception; >=10 novel<40% | 20 delivered (12 template-pass, 8 documented exceptions); 17/20 novel<40% | PASS |

The locked gate was deliberately strict: it demanded that most sequence-level candidates keep PETase-specific domain identity (G3) and strict catalytic geometry (G4). They do not. That negative is the central scientific result of this round (section 4).

## 3. Methods (all grounded, all logged)

**Grounding before any bulk compute (G1).** UniProt entry A0A0K8P6T7 (IsPETase) retrieved live: active-site features Ser160 (nucleophile), Asp206 and His237 (charge relay), signal peptide 1-27; Pfam cross-reference PF12740 (PETase). Route validation: hmmscan-vs-pfam on the mature IsPETase sequence returned PF12740.14 as top hit, E=4.46e-130 (EBI job 02f0db55-c057-4ce5-9d29-9a7f5f8f65a4). Provenance route validation: 5 sample studies resolved through the MGnify API before bulk retrieval. All retrievals hashed and logged (`results/r2_provenance_ledger.jsonl`, 1,000+ entries).

**Domain annotation (G2, G3).** All 468 candidates (sequences re-assembled from the Round-1 HMMER cache; manifest sha256 `ccc530fda2999c2e283c7ec8df1ad94c5280344b05693447faa3f3bb041cb685`) annotated by hmmscan against Pfam-A via the EBI HMMER API, per-accession caching, hits kept at E<=1e-3.

**Catalytic triad (G4).** Global pairwise alignment (Biopython 1.88 PairwiseAligner, match +2, mismatch -1, gap open -5, extend -0.5) of each candidate to the IsPETase mature sequence; residues aligned to mature coordinates 133/179/210 (full-length 160/206/237 minus the 27-residue signal peptide; sanity-asserted S/D/H on the reference itself) were read off per candidate. Triad intact iff Ser/Asp/His at all three.

**Structure (G4-support, G7).** RCSB sequence search (search.rcsb.org, evalue_cutoff 1e-10, 3 rows) extended from the Round-1 top-50 to ranks 51-150 (100 new queries), then targeted at every eligible shortlist-pool member lacking cached evidence (33 further queries); local-alignment coverage computed against the top template chain.

**Provenance (G5).** Round-1 EBI job result pages re-walked (16 jobs, all pages) to recover hit metadata (studies, assemblies, Pfam xrefs) for all 468 candidates; 141 distinct studies resolved to MGnify study records.

**False-positive adjudication (G6).** (a) Redundancy: MMseqs2 18-8cc5c easy-cluster, --min-seq-id 0.9 -c 0.8 --cov-mode 1. (b) Anti-panel: 8 reviewed, taxonomically diverse non-PET esterases/lipases retrieved live from UniProt (query: EC 3.1.1.3 OR 3.1.1.1, reviewed, 180-450 aa, NOT PET/cutinase/polyester; P07098, P37957, P26876, P54857, I6Y2J4, Q94252, P61871, Q71DJ5; retrieval hashes in `data/raw/antipanel/SHA256SUMS`). Screen: DIAMOND 2.1.13 blastp --very-sensitive -e 1e-5, applied symmetrically to the 16-reference panel and the 8-member anti-panel. Documented execution substitution: the EBI phmmer API does not accept a custom sequence panel, so the protocol-named phmmer anti-panel screen was executed locally with DIAMOND against both panels under identical scoring; the substitution is recorded in the environment ledger and does not touch gate text.

**Shortlist (G7).** Eligibility = triad intact AND PF12740 best-E domain AND not anti-panel flagged (41 of 468). Composite score: 2.0*novelty + 1.0*(E-value tier) + 1.5*template coverage + 0.5*(thermostability proxy: aliphatic index >= reference-panel median AND >=2 Cys) + 0.3*min(n_studies,3); gate-compliant selection (structure-pass first), biome-diversity greedy pass; exactly 20.

**Tooling mandate.** Open-source local compute wherever feasible: MMseqs2 18-8cc5c, DIAMOND 2.1.13, Biopython 1.88, numpy 2.2.6, matplotlib. Foldseek 10-941cd33 installed but not applicable (no candidate structures predicted; no local structure-prediction capacity - recorded compute ceiling). Local HMMER not installable (no root - recorded ceiling; EBI API route used as protocol-locked). Full pins, sha256s, and download URLs: `protocol/environment_ledger.json`.

## 4. Results and the two preserved negatives

### 4.1 G3 negative: domain coherence is the exception, not the rule

Only 133/468 candidates (28.4%) have PF12740 as their best-E Pfam domain (locked floor: 60%). The full best-domain distribution:

| best-E Pfam family | candidates | family identity |
|---|---|---|
| PF07519 | 266 | tannase / feruloyl-esterase family (InterPro, fetched live) |
| PF12740 | 133 | PETase family |
| (no hit E<=1e-3) | 15 | unannotated |
| PF01083 | 10 | cutinase family |
| PF07224 | 6 | Abhydrolase-like |
| 7 other families | 7 | singletons |

Interpretation: sequence-level (phmmer) recruitment by PET-hydrolase queries lands mostly in adjacent alpha/beta-hydrolase esterase families. PF07519 (tannase/feruloyl-esterase) dominates: these enzymes share the catalytic Ser-His-Asp machinery and hydrolyze ester bonds in plant polymers, and some feruloyl esterases show promiscuous activity on synthetic polyesters - so the 266 are not junk, but they are NOT PETase-family members and must not be marketed as such. This is precisely the false-positive class Round 2 existed to expose.

### 4.2 G4 negative: strict catalytic geometry decays fast with novelty

Strict triad (Ser at 160, Asp at 206, His at 237 in IsPETase-aligned coordinates) is intact in only 45/468 (locked floor: 200). Per-position conservation: Ser160 in 295 (63%), Asp206 in 163 (35%), His237 in 90 (19%). The nucleophile is the most conserved element and the histidine the least - the expected order for divergent hydrolases, where the acid/base pair tolerates more drift and His is frequently replaced or shifted. 63 of 468 keep S+H without the D; 32 candidates do not even align at the nucleophile position. Combined with section 4.1: requiring BOTH PF12740 coherence AND strict triad leaves 41 candidates (8.8% of Round-1's output). That 41, not 468, is the true experimental target space.

### 4.3 Structure modelability collapses down the ranking

RCSB template pass (E<=1e-10, >=60% local coverage): 29/50 (58%) in the Round-1 top-50 but only 8/100 (8%) in ranks 51-150. Combined 37/150 (24.7%). Among the 41-member eligible pool, targeted template checks found 12 with template-pass quality and 8 more with a template below the coverage bar (documented per candidate with exact coverage). Practical consequence: prioritization by E-value alone over-promises structural tractability; template checking must run before any shortlist is called experimental-ready.

### 4.4 Zero redundancy, zero anti-panel flags (G6)

All 468 candidates are singletons at 90% identity / 80% coverage (468 clusters). No candidate aligns to any of the 8 non-PET lipase/esterase anti-panel members at E<=1e-5 under DIAMOND --very-sensitive, while all 468 align to the reference panel: flag rate 0%. The Round-1 set is non-redundant and carries no detectable classic-lipase contamination.

### 4.5 Environmental provenance (G5)

All 468 candidates resolve to >=1 MGnify study; 141 distinct studies in total. Top contributing studies include antibiotic-fate environmental surveys (30 candidates), Amazon river continuum metagenomes (27), urban environmental metagenomes (27), Tara Oceans marine samples (24 + 15 across two assemblies), deep-sea bacteria (21), Malaspina expedition, bioGEOTRACES marine, maize phylloplane (14), rainforest soils, and activated sludge. The candidate pool is global and biome-diverse - consistent with ester-bond hydrolysis being a broadly distributed function, and it means shortlist picks can be selected for source-environment diversity (done in G7).

### 4.6 The 20-candidate experimental-ready shortlist (G7)

Selection pool: 41 (triad intact + PF12740-best + unflagged). Delivered: exactly 20; 12 with RCSB template E<=1e-10 and >=60% coverage, 8 with documented structure exceptions (template present, coverage <60%, exact coverage on each card); 17/20 at <40% identity to every Round-1 reference; all 20 carry intact S160/D206/H237, PF12740 as best-E domain, and resolved study provenance. Top picks:

| rank | accession | novelty (max ref id.) | length | template (cov.) | aliphatic idx | Cys | study |
|---|---|---|---|---|---|---|---|
| 1 | MGYP003583961369 | 33.2% | 347 | 8SPK (0.746) | 82.2 | 6 | ERP131768 |
| 2 | MGYP006180250121 | 29.0% | 254 | 8CRU (0.654) | 84.6 | 2 | ERP137364 |
| 3 | MGYP009564209523 | 27.3% | 329 | 7PZJ (0.623) | 89.9 | 9 | ERP129541 |

Full per-candidate rationale cards (scores, all Pfam hits, aligned triad residues, studies, thermostability proxies, exception documentation): `results/shortlist_20.json`.

## 5. Round-over-round verdict

Round 1 asked "are there novel PET-hydrolase-like sequences in the global metagenome?" - answer: yes, 468, replicated across catalogs, robust to scrambled controls. Round 2 asked "how many of them are really PETase-family, catalytically intact, modelable, non-redundant, provenance-resolved enzymes?" - answer: 41 survive every hard check, and 20 are packaged as experimental-ready. The two gate failures are the finding: sequence similarity to PET hydrolases, at the novelty levels discovery requires, mostly recruits adjacent-family esterases with degraded catalytic geometry. Any pipeline that reports Round-1-style candidate counts without Round-2-style orthogonal validation overstates its yield by an order of magnitude (468 -> 41).

## 6. Limitations

- The anti-panel screen used DIAMOND rather than phmmer (custom panels unsupported by the EBI API); symmetric scoring makes the 0% flag rate internally consistent, but a profile-HMM anti-panel (e.g., local HMMER against lipase Pfam profiles) would be a stricter test and is future work.
- Structure coverage is sequence-based template mapping, not predicted structures; Foldseek was installed but no structure-prediction capacity exists in this environment (recorded ceiling). AlphaFold/ESMFold modeling of the 20 shortlisted candidates is the natural Round-3 step.
- Triad checking is alignment-position-based against a single reference frame (IsPETase); candidates whose catalytic residues sit at shifted register (insertions) may be falsely counted as non-intact. The shortlist is therefore conservative.
- Biome resolution is study-level (MGnify study metadata), not sample-level; sample-level biome labels were not available for all studies.

## 7. Provenance and reproducibility

Every retrieval is logged with timestamp and sha256 (`results/r2_provenance_ledger.jsonl`). Tool pins and binaries hashed in `protocol/environment_ledger.json`. All scripts in `code/` are idempotent and cache-backed. Locked protocol hash: `f665fc0d...`. Candidate set hash: `ccc530fd...`.
