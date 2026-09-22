# Orthogonal validation collapses metagenomic PET-hydrolase candidate counts by an order of magnitude - but yields a defensible experimental shortlist

## Abstract

Sequence-similarity mining of metagenomic catalogs has become a standard route to novel PET-hydrolase candidates, but published pipelines typically stop at sequence-level evidence. We subjected 468 previously discovered, cross-catalog-replicated, control-validated PET-hydrolase candidates from the MGnify protein catalog (Round 1) to a locked-protocol Round 2 of orthogonal validation: Pfam domain coherence (hmmscan), catalytic-triad integrity at IsPETase coordinates, structure-template modelability (RCSB), environmental provenance (MGnify studies), redundancy clustering (MMseqs2), and a non-PET-esterase anti-panel screen (DIAMOND). Only 28.4% of candidates have the PETase family PF12740 as their best domain - the dominant best-hit family is the tannase/feruloyl-esterase family PF07519 (56.8%) - and only 45/468 (9.6%) retain a strict Ser-Asp-His triad at IsPETase-aligned positions. Structure modelability decays sharply down the E-value ranking (58% in the top 50 vs 8% in ranks 51-150). The candidate set is nonetheless clean in other dimensions: zero redundancy at 90% identity, zero anti-panel flags, and complete provenance across 141 studies spanning marine, freshwater, soil, plant-surface, urban, and sludge biomes. The intersection of all hard checks leaves 41 candidates, from which we deliver 20 experimental-ready picks (12 with high-coverage structural templates, 17 at <40% identity to any characterized enzyme), each with intact catalytic triad, PF12740 coherence, and full provenance. Under a locked success gate defined before any candidate-level result was inspected, the round fails 2 of 7 gates; we argue these failures are the main result: orthogonal validation is not a formality but the difference between 468 and 41.

## 1. Introduction

Enzymatic PET depolymerization has moved from the discovery of IsPETase in Ideonella sakaiensis (Yoshida et al., PMID:33579403) to engineered variants operating at industrial relevance (PMID:33051015, engineered depolymerase reports retrieved 2026-09-21). Metagenome mining promises to widen the enzyme pool beyond cultured isolates (PMID:35656865, PMID:35495686), and the MGnify resource (Mitchell et al., PMID:31696235) now indexes >100M non-singleton predicted proteins. The standard mining recipe - profile or pairwise search against a reference panel, followed by identity and E-value filters - is demonstrably sensitive (our Round 1: 468 novel candidates, cross-catalog replication, zero scrambled-control hits). Its specificity at the novelty levels that make discovery worthwhile is far less examined. Sequence identity below ~40% sits in the regime where function transfer by homology is unreliable (PMID:20003388), and ester-bond hydrolases are a large, functionally heterogeneous clan (PMID:7946464): cutinases, tannases, feruloyl esterases, lipases, and PETases share the alpha/beta-hydrolase fold and the Ser-Asp-His catalytic machinery (PMID:7946464, PMID:21085121). The question Round 2 answers: how many "novel PET-hydrolase candidates" survive when sequence similarity is no longer accepted as evidence of family membership, catalytic competence, or structural tractability?

## 2. Methods

**Locked protocol.** All gates, thresholds, and analysis plans were fixed in writing (hash-locked) before any candidate-level Round-2 result was inspected; two gates subsequently failed and are reported verbatim. Grounding was live-source only: catalytic positions (Ser160/Asp206/His237) and the PF12740 family assignment come from the current UniProt feature table of A0A0K8P6T7, and every annotation route was validated end-to-end on the reference before bulk use.

**Domain coherence.** hmmscan against Pfam-A (EBI HMMER API; Potter et al., PMID:29905871) for all 468 candidates; family identity of best-E domains resolved against InterPro live.

**Catalytic triad.** Global alignment to the IsPETase mature sequence; residues at aligned positions of S160/D206/H237 read per candidate; intact iff Ser/Asp/His at all three.

**Structure.** RCSB sequence search (E<=1e-10) with local-alignment coverage against the best template chain; the Round-1 top-50 analysis was extended to rank 150, and every shortlist-pool member received a targeted template check.

**Provenance.** Hit-level metadata from the original search jobs mapped all candidates to MGnify studies, resolved through the MGnify API.

**False-positive adjudication.** MMseqs2 clustering (90% identity, 80% coverage); DIAMOND --very-sensitive screen against an 8-member live-retrieved panel of reviewed non-PET lipases/esterases, scored symmetrically against the 16-member PET-hydrolase reference panel.

**Shortlist.** Composite scoring (novelty, E-value tier, template coverage, thermostability proxies, provenance breadth) over the intersection pool, with gate-compliant selection and a biome-diversity pass.

## 3. Results

**Domain coherence fails at scale.** PF12740 is the best-E domain in only 133/468 candidates (28.4%). PF07519 (tannase/feruloyl-esterase) dominates with 266 (56.8%); cutinase-family PF01083 takes 10; 15 candidates have no Pfam hit at E<=1e-3 at all. Sequence recruitment by PET-hydrolase queries therefore lands mostly in adjacent esterase families.

**Catalytic geometry fails faster than domain identity.** A strict Ser-Asp-His triad at IsPETase-aligned coordinates survives in 45/468 (9.6%). Conservation is position-ordered: Ser160 in 63%, Asp206 in 35%, His237 in 19% of candidates - matching the expectation that the nucleophile anchors the mechanism while the acid/base pair drifts (PMID:7946464, PMID:21085121).

**Structure modelability decays down the ranking.** Template-pass rates (E<=1e-10, >=60% coverage): 58% in the top 50, 8% in ranks 51-150. E-value rank over-promises structural tractability beyond the head of the list.

**Cleanliness checks pass completely.** 468 singleton clusters at 90% identity; 0% anti-panel flag rate; 468/468 provenance-resolved across 141 studies (marine/Tara Oceans, Amazon continuum, urban, soil, phylloplane, sludge, antibiotic-fate surveys).

**The intersection is the deliverable.** Requiring PF12740 coherence AND strict triad AND no anti-panel flag leaves 41 of 468 (8.8%). From these, 20 experimental-ready candidates were selected: 12 with template coverage >=60% (templates include 8SPK, 8CRU, 7PZJ, 8ETY, 9XV6), 8 with documented sub-threshold template evidence, 17 at <40% identity to every characterized reference; thermostability proxies (aliphatic index >= reference median, >=2 Cys) favor a subset including MGYP009564209523 (AI 89.9, 9 Cys).

## 4. Discussion

The two gate failures are the paper. A pipeline reporting "468 novel PET-hydrolase candidates" is accurate at the sequence level and wrong by an order of magnitude at the experimental level: 8.8% survive domain coherence, catalytic integrity, and false-positive screening. Two design lessons follow. First, Pfam-domain coherence should be a first-class filter in discovery pipelines, not a post-hoc annotation: it is cheap (100% annotation coverage here) and eliminates the dominant false-positive class. Second, catalytic-residue checks must be register-aware: alignment-position checking against a single reference frame is conservative (it will miss shifted-register homologs), and even so it removes 90% of candidates - a motif/HMM-based catalytic-machinery model would be the natural refinement.

The surviving 20 are genuinely valuable: highly novel (17/20 under 40% identity to anything characterized), catalytically intact, domain-coherent, non-redundant, provenance-resolved across diverse biomes, and partly structure-modelable. They are the right size for experimental follow-up: expression, PET-film hydrolysis assays, and thermostability screens. Structure prediction (Foldseek-searchable models) for all 20 is the immediate next computation; the tannase/feruloyl-esterase 266 are themselves an interesting pool for polyester-adjacent activities, but they must be pursued as what they are.

## 5. Data and code availability

All artifacts (locked protocol + hash, environment ledger with tool pins, per-candidate annotations, triad calls, template checks, provenance mapping, shortlist cards, provenance ledger with retrieval hashes, literature ledger of live PubMed retrievals) accompany this paper. Every external datum was retrieved live from UniProt, Pfam/InterPro, RCSB, MGnify, EBI HMMER, and NCBI on 2026-09-21 and is hash-logged.

## References (live-retrieved, PMIDs)

Yoshida S (2021) Ideonella sakaiensis, PETase, and MHETase. PMID:33579403. Son HF (2020) Structural bioinformatics-based protein engineering of thermo-stable PETase. PMID:33051015. Eiamthong B (2022) Discovery and genetic code expansion of a PET hydrolase from metagenome. PMID:35656865. Carr CM (2022) BgP, a cutinase-like polyesterase from deep-sea sponge metagenome. PMID:35495686. Mitchell AL (2020) MGnify: the microbiome analysis resource in 2020. PMID:31696235. Potter SC (2018) HMMER web server: 2018 update. PMID:29905871. Jaeger KE (1994) Bacterial lipases. PMID:7946464. Weerapana E (2010) Quantitative reactivity profiling. PMID:21085121. Mizianty MJ (2009) Prediction in the twilight zone. PMID:20003388. Kimura Y (2023) Plastisphere enzyme discovery. PMID:37775475. Full topic-wise ledger: report/literature_ledger.md.
