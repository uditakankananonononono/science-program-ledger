# algo50/23 - Disease-gene prioritization on a physical interaction network: random walk with restart vs neighbour counting, with a degree-bias correction

Status: LOCKED before any method was scored (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Köhler et al. 2008 (Am J Hum Genet 82:949) showed random walk with restart (RWR) ranks hidden disease genes better than counting direct interactions with known disease genes. Does that hold on today's data using only experimental interactions (no text-mining or curated-database channels, which can leak disease knowledge)? And does correcting RWR for hub bias improve the top of the ranking?

## Data
- Network: STRING v12 human, detailed channels; edge kept if the EXPERIMENTAL channel score >= 400 (other channels ignored). Gene symbols from STRING protein.info.
- Disease genes: HPO genes_to_disease.txt, MENDELIAN associations only. Diseases with 5-50 genes present in the network.
- URLs, time, sha256 in data/.

## Evaluation
Leave-one-out within each disease: hide one gene, use the others as seeds, rank all network genes that are not seeds. Record the hidden gene's rank.

## Methods
- DEG: node degree (hub baseline).
- DN: number of seed neighbours (ties broken by degree).
- RWR: restart probability 0.7 (Köhler's setting), column-normalized adjacency, power iteration to L1 change < 1e-8 (max 100).
- RWR-dc (proposed): RWR score divided by the RWR score obtained with restart spread uniformly over all nodes (same restart probability). This removes the part of the score due to a node being a hub.

## Metrics
- AUROC per query = 1 - (rank-1)/(N_candidates-1), averaged.
- Top-100 recall = fraction of queries where the hidden gene ranks in the top 100.
- 95% CIs by 2000 bootstrap resamples of diseases, paired.

## Success gates (declared before scoring)
- G1: mean AUROC(RWR) - AUROC(DN) >= 0.02, CI lower bound > 0.
- G2: top-100 recall(RWR) - recall(DN) >= 0.02, CI lower bound > 0.
- G3: top-100 recall(RWR-dc) - recall(RWR) > 0, CI lower bound > 0.
All reported pass or fail; one post-hoc pivot allowed, locked first.
