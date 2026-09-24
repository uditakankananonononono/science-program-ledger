# DOC-1-035: A "Dark Matter" Protein Function Predictor with Genomic Context — GATES
Locked 2026-09-24 10:52 IST, BEFORE any outcome analysis. All thresholds final; changes only
via addenda locked before the outcomes they govern.

## Question
Can genomic-context association evidence (STRING v12 prokaryotic gene-neighborhood,
gene-fusion, and phylogenetic co-occurrence channels) predict the COG functional category
(letter) of prokaryotic dark-matter proteins - validated on a temporally frozen cohort of
"newly lit" proteins (no COG assignment in COG-2014; assigned a COG letter in COG-2020)?

## Data (real public data; PROVENANCE.md)
- STRING v12.0 per-species downloads (stringdb-downloads.org): protein.links.full (channel
  scores: neighborhood, fusion, cooccurrence, and reference channels), protein.info,
  protein.aliases - for the locked panel below.
- COG-2020 (NCBI FTP): cog-20.cog.csv (protein -> COG), cog-20.def.tab / fun-20.tab (letters).
- COG-2014 (NCBI FTP): cog2003-2014.csv, prot2003-2014.tab (gi -> RefSeq accession bridge).
- ID bridge: STRING protein ids carry locus tags for RefSeq-era genomes; protein.aliases
  (RefSeq source) as backup; genome accession (GCA, version stripped) links STRING <-> COG.

## Panel (locked rule; exact list fixed in manifest BEFORE scoring, never after)
Genomes present in COG-2014 AND COG-2020 AND STRING v12 with a per-species links.full file;
from these, 150 genomes sampled with seed 42, stratified by phylum, minimum 1,500 COG-2020
proteins each. If any download/mapping fails for a genome, it is dropped and documented in the
manifest (no cherry-picking replacements). Locked minimum mapping rates (eligibility halt,
documented pre-outcome if unmet): >= 60% of a genome's COG-2020 proteins mapped to STRING ids;
>= 60% of newly-lit proteins mapped across the panel.

## Cohorts (temporal split; granularity matched to claim: protein-level claim, protein-level split)
- Long-lit (train/dev): proteins with a COG letter in BOTH COG-2014 and COG-2020; dev = 10-fold
  CV at protein level. Neighbor labels and features use ONLY 2014 knowledge (temporal purity).
- Frozen newly-lit (external validation): proteins with NO COG-2014 assignment but a COG-2020
  letter. Never touched for training, tuning, or threshold choice.
- Dark targets (prospective only): no COG-2020 assignment; tool output, not scored.

## Arms
- ARM A (NAMED PUBLISHED BASELINE, executed): genomic-context guilt-by-association neighbor
  transfer - Huynen, Snel, Lathe & Bork, Genome Res 10:1204 (2000) Type II gene-neighborhood
  method: predict a protein's COG letter by neighborhood-score-weighted vote of its STRING
  neighborhood-channel neighbors' 2014 letters.
- ARM B: multinomial logistic regression combining ALL THREE context channels (features =
  per-channel score-weighted neighbor-letter distributions) + amino-acid-composition features,
  trained on long-lit proteins with 2014-only features.

## Gates
- G1 (sanity halt): ARM A dev 10-fold mean accuracy within [popularity + 5pp, 80%]. Outside
  the band = incoherent; document and stop for routing. Huynen 2000 coverage anchors (37% gene
  order, 50% combined on a 25-genome-era panel) reported qualitatively, not as a gate.
- G2 (dev): ARM B >= ARM A + 5pp mean CV accuracy AND ARM B >= ARM A on >= 8/10 folds.
- G3 (frozen, newly-lit): ARM B >= ARM A + 3pp AND ARM B >= popularity + 5pp.
  Beat ARM A or document the loss explicitly (ISEF).
- G4 (mechanism, runs regardless): per-channel ablation; provenance of correct newly-lit
  predictions (which channel drove them) vs the Huynen 2000 qualitative hierarchy
  (gene order strongest, fusion cleanest, co-occurrence weakest).
- G5: working CLI darkfunc_predict.py + one prospective lab nomination (locked below).

## Failure tree
G1 halt -> parent routing (no self-override). G2 fail -> P1, exactly one pre-registered rescue:
P1 = ARM B replaced by 2-step label propagation over the combined-channel graph (same gates,
same thresholds). P1 fail or G3 fail -> DOCUMENTED BOUNDARY. No threshold relaxation after
seeing any result.

## Prospective lab nomination (locked)
A microbial-genomics group characterizing hypothetical proteins from an environmental isolate:
prioritize dark proteins with high-margin COG-letter predictions and fusion-channel support for
targeted knockout/complementation assays.

## User pivot rule
If a component gives no useful result, steer in a new direction to find a useful result:
failed direction documented, new gates locked before new results.

## Addendum A (locked 2026-09-24 11:11 IST, before ARM B scoring; ARM A recomputed under it)

**Label definition.** Some COGs carry a dual functional code in cog-20.def.tab /
cognames2003-2014.tab (e.g. "CE"), which produced 153 composite label values in the first
ARM A pass. The locked task is prediction of THE COG functional-category letter. Resolution:
the label is the PRIMARY (first) letter of the COG functional code; dual-code COGs collapse
to their primary letter (26-class task). Applied identically to 2014 and 2020 labels, to
neighbor-vote targets and to all arms. ARM A dev and G1 are recomputed under this definition
before ARM B runs; all gates, thresholds, and bands unchanged (they are defined on accuracy
margins vs ARM A and popularity, both recomputed consistently). This is a data-processing
definition, not a threshold change; no outcome under the composite-label pass is used anywhere.
