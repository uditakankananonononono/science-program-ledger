# DOC-1-033: Predicting Phage-Host Interactions with a GNN — REPORT

**Status: DOCUMENTED BOUNDARY** (locked failure tree: P1 G2 passed, G3 failed; boundary stands per Addendum D)

## Question
Can a heterogeneous graph neural network (CHERRY-style GCN over virus-virus d2 similarity,
virus-prokaryote interaction, prokaryote-prokaryote, and CRISPR-spacer edges) predict the host
species of a newly sequenced phage, beating named published baselines out-of-domain?

## Data (real public data; PROVENANCE.md)
- CHERRY (KennthShang/CHERRY, MIT): Interactiondata VHM/TEST pairs — 1,260 sequenced train pairs
  (pre-2015 phages), 615 frozen test pairs, 0 phage overlap; candidate panel 60,105 prokaryote
  genomes (all 615 test hosts present); k=4 kmer profiles; d2 virus-virus edges (26,440);
  interaction edges (780,537); prokaryote-prokaryote edges (1,063,200).
- CRISPR DB: allCRISPRs from CHERRY dataset — 1,236,304 spacers.

## Arms
- ARM A: executed mechanistic baseline — KNN over d2 (cosine on k=4 kmer frequencies).
- ARM B: heterogeneous GCN (hidden 64, taxonomy embeddings, 40 epochs, stochastic negatives).
  No-graph variant = decoder only.

## Gates and outcomes (all thresholds locked before outcomes; Addenda A, B, D, E)
| Gate | Bar | Result | Verdict |
|---|---|---|---|
| G1 (Addendum A: dev vs popularity+5pp = 22.1%) | >= 22.1% | ARM B dev 20.95% | FAIL by 1.15pp -> sanity halt, parent routed to P1 |
| G2 (dev, graph vs no-graph +5pp) | +5pp | base +7.3pp (20.95 vs 13.65), wins all 10 folds; P1 +6.35pp (20.00 vs 13.65), >= on all 10 folds | PASS (both) |
| G3 (frozen, >= 59.8% = VHM-net 57.8%+2pp AND >= ARM A +3pp = 62.35%) | 59.8% / 62.35% | ARM B base 12.20%; ARM B P1 12.20% | FAIL (~47pp); ARM A 59.35% |
| G4 (mechanism) | — | CRISPR edges: 730/1,875 viruses with qualifying spacer hit (length/slen>0.95, pident>95, first hit per virus), 55 hit-species outside panel; 14,433 deduped edges; test-virus coverage 249/615 = 40.5% (paper anchor ~24.6%). Edge contribution: dev -0.95pp, frozen +0.00pp species. Correct predictions provenance: compositional d2 similarity, not CRISPR exact signals | documented |
| G5 (tool) | — | tools/phage_host_predict.py (KNN-d2, ARM A) + assets; smoke-tested end-to-end | shipped |

Frozen numbers (615 test pairs, 60,105-candidate panel):
- ARM A KNN-d2: species 59.35%, genus 68.29%
- ARM B base GCN: species 12.20%, genus 13.66%
- ARM B P1 (CRISPR edges): species 12.20%, genus 13.50%
- ARM B no-graph: species 8.78%, genus 8.78%

CHERRY paper's 78% SOTA reference (transductive, own test protocol): not beaten — loss documented.

## Interpretation vs literature
- The graph carries real signal: graph beats no-graph on every dev fold (base +7.3pp, P1 +6.35pp).
  But dev-CV gains do not transfer to the frozen cohort: the GCN's learned propagation collapses
  (20.95% dev -> 12.20% frozen) while direct KNN-d2 holds at 59.35%. Same dev-to-frozen inversion
  pattern as DOC-1-032 (85% -> 30%), now second instance with a quantified harness.
- CRISPR-spacer evidence, the paper's designated rescue (P1, Addendum B), is real but too sparse
  and too redundant with compositional signal to move accuracy: 40.5% of test viruses carry a
  qualifying spacer link, yet frozen accuracy is unchanged (12.20% -> 12.20%).
- Out-of-domain, the mechanistic baseline (KNN on k-mer composition) strictly dominates the
  learned graph model — program pattern #6 (026/027/030/032) confirmed again.

## Boundary statement (locked pivot rule)
Failed direction documented: transductive GCN host prediction at this panel scale (60k candidates)
does not beat — or approach — direct d2 KNN on a frozen cohort, with or without CRISPR-spacer
edges. Useful result shipped: validated KNN-d2 predictor (59.35% species top-1, 68.29% genus)
as tools/phage_host_predict.py + quantified boundary (graph propagation adds real but
non-transferring signal; CRISPR rescue neutral).

## Prospective lab nomination (locked in GATES)
A phage-therapy group screening therapeutic candidates: given a newly sequenced phage, rank
candidate hosts from a patient isolate panel, validated by spot assays. Tool: ARM A KNN-d2 CLI.

## Reproduce
model033.py (tools/), modes dev/frozen, P1=1 env for CRISPR-augmented graph; blast word_size 11
equivalence verified (Addendum E). All artifacts in results/.
