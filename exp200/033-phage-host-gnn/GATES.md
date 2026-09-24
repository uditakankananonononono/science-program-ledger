# GATES - DOC-1-033 (locked 2026-09-24 09:48 IST, BEFORE any model fitting or scoring)

## Claim
A compact, in-envelope graph neural network predicts phage-host interactions (which prokaryote
a novel phage infects) from sequence-derived graph structure, beating the best non-CHERRY named
published tools on the field's standard frozen benchmark, with mechanistic attribution of the
signal and a working prediction CLI.

## Data (eligibility verified BEFORE this lock)
- Benchmark: CHERRY (Shang & Sun 2022, Brief Bioinform 21:bbac182, PMC9487644) official repo
  Interactiondata: VHM_PAIR_TAX.xls (1,426 train pairs, 1,426 unique phages, 188 host species)
  and TEST_PAIR_TAX.xls (671 test pairs, 671 unique phages, 96 host species), plus BACTERIA
  sheets (31,918 / 60,105 prokaryote candidate genomes with taxonomy). Downloaded and parsed
  2026-09-24.
- Sequences/features: dataset/nucl.fasta.bz2 (35MB, virus genomes), dataset/prokaryote.csv
  (9.2MB, candidate metadata+taxonomy), dataset/database_gene_to_genome.csv (8.75MB,
  protein-cluster sharing map). Prokaryote genomes themselves are NOT downloaded (scale);
  prokaryote nodes use taxonomy features only - scoped, disclosed.
- Protocol = the paper's own: transductive link prediction. Each test virus is scored against
  ALL 60,105 candidate prokaryotes; top-1 prediction vs the known host. Train viruses are
  pre-2015 submissions; test viruses are later, so TRAIN/TEST PHAGES ARE FULLY DISJOINT
  (verified: 0 accession overlap). Host species overlap train/test = 60/96 (the task is
  host prediction for NOVEL phages against a KNOWN candidate panel - disjointness granularity
  matches the claim granularity per the 031 rule). Cold-host slice (36 test host species
  absent from train) reported as characterization, no gate.
- 028 rule: label granularity = per-(virus, prokaryote) pair interaction vs predicted score;
  headline = per-virus top-1 accuracy. Match.

## Named published baselines and anchors (verbatim from the paper)
- CHERRY (the SOTA, graph GCN): 78% species-level accuracy on this exact test set.
- CHERRY no-graph ablation (decoder only, k-mer features): 56% species-level on the test set.
- VHM-net: next-best named tool, 35% below CHERRY (78/1.35 = 57.8% species-level).
- BLAST-KNN (paper's alignment baseline) returns a prediction for only ~65.5% of viruses.
- ARM A (executed): KNN over d2 k-mer similarity to the 1,426 train phages (the paper's
  BLAST-KNN baseline reimplemented with composition similarity, in-envelope), same protocol.
- ARM A' (anchor comparison): published numbers above on the identical benchmark (documented
  as anchors; CHERRY itself is not re-runnable in-envelope - full pipeline needs BLAST DBs,
  dashing, CRISPR extraction over 60k genomes).

## Arms
- ARM A: executed KNN baseline (above).
- ARM B (the claim): compact 2-layer GCN (torch CPU), transductive. Nodes: 2,097 viruses
  (1,426 train + 671 test, test unlabeled) + 60,105 prokaryotes. Node features: virus k-mer
  (k=4) frequency vectors; prokaryote nodes: taxonomy one-hot (phylum..genus from
  prokaryote.csv). Edges: virus-virus d2 similarity (threshold locked at manifest),
  virus-prokaryote known train pairs, prokaryote-prokaryote same-genus links. Negative
  sampling per the paper. Decoder scores (virus, prokaryote) pairs.
- P1 (pre-registered rescue if G2 fails): add virus-prokaryote protein-sharing edges from
  database_gene_to_genome.csv (virus protein clusters via mmseqs2 on protein.fasta), same gates.

## Gates
- G1 (sanity halt): ARM B no-graph variant (decoder only) dev 10-fold CV species accuracy in
  [0.35, 0.70] (paper's no-graph test anchor 0.56). Else incoherent - document, stop.
- G2 (dev, 10-fold CV on train pairs): ARM B >= ARM B no-graph + 5pp species accuracy.
- G3 (frozen, TEST671): ARM B species accuracy >= 57.8% + 2pp = 59.8% (beats VHM-net, the
  best non-CHERRY named published tool) AND >= ARM A executed KNN + 3pp. CHERRY's 78% is the
  SOTA reference: beat or document the loss explicitly.
- Failure tree: G2 fail -> P1, same gates; P1 fail or G3 fail -> DOCUMENTED BOUNDARY.
- G4 (mechanism, runs regardless): edge-type ablation contribution; provenance of correct
  cold-host predictions (CRISPR-style exact signals vs compositional similarity) vs literature
  (BLASTN ~65.5%, CRISPR ~24.6% coverage anchors).
- G5: working CLI phage_host_predict.py + one prospective lab nomination.

## Prospective lab nomination (locked)
A phage-therapy group screening therapeutic candidates: given a newly sequenced phage, rank
candidate hosts from a patient isolate panel, validated by spot assays.

## Scoring discipline
Sample manifest (pair lists, disjointness stats, edge thresholds, file hashes) committed BEFORE
any training. Thresholds never relax after seeing results; errata in GATES_ADDENDUM files
locked before the outcomes they govern.
