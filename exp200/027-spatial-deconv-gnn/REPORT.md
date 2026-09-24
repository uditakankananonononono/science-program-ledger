# DOC-1-027: Spatial Deconvolution with a Graph Neural Network
**Claim** (locked pre-outcomes): a GNN exploiting spatial neighborhood structure beats NNLS
(SPOTlight/Stereoscope core) at deconvolving simulated Visium-like spots, and transfers to a frozen
held-out cohort. **Verdict: DOCUMENTED BOUNDARY** (G2 fail, pre-registered P1 fail, tree exhausted).

## Scores (mean per-type Pearson r, 10 types, 2000 spots)
| arm | dev | frozen |
|---|---|---|
| NNLS baseline | 0.6856 | 0.7273 |
| GNN (locked arm) | 0.409 | 0.363 |
| GNN P1 (k=12, h=256) | 0.356 | 0.299 |
| MLP ablation (G4) | 0.747 | 0.710 |

G1 sanity: NNLS dev 0.6856 >= 0.50 - pass, no halt.
G2: 0.409 < 0.6856+0.05 - FAIL. P1: 0.356 - FAIL. Tree exhausted => boundary. G3 moot (both fail).

## Mechanism (G4) - the payload
1. Graph smoothing is actively HARMFUL: removing message passing (MLP, same architecture/training)
   gains +0.34 mean r (0.747 vs 0.409). Mean-aggregation regresses each spot toward its regional
   mean; the metric rewards per-spot compositional variation around that mean - exactly what
   smoothing destroys. Locked simulation had region-level sharing only in the dominant type;
   real Visium may share more, but the burden of proof is on the smoother.
2. Supervision transfers worse than mechanism under regime shift: the supervised MLP beats NNLS on
   dev (0.747 vs 0.686) but LOSES on the frozen cohort with sparser mixtures and disjoint cells
   (0.710 vs 0.727). The mechanistic NNLS generalizes across the mixture-regime shift; the
   distribution-fit does not. Echoes 026 (dev-fit beats curated in-domain, loses out-of-domain).
3. Erratum (Addendum B): aggregation was GCN-style mean, not GraphSAGE-concat; self-preserving
   variants untested per the locked tree. Boundary stands; parent adjudicates re-lock value.

## Tool (G5)
code/spot_deconv.py - NNLS deconvolver (winning arm). GNN arms removed from the tool surface.
## Prospective lab nomination (locked)
Spatial core running Visium mouse lung with matched scRNA reference; marker-concordance readout.
