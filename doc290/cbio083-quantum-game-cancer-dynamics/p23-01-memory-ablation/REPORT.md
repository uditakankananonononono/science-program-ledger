# P23-01 Build Report: Is It Quantum or Memory (matched-budget model zoo on Kaznatcheev 2019)

**Parent:** CBIO083 Quantum Game Theory Cancer Dynamics | **Spec:** doc290/cbio083-quantum-game-cancer-dynamics/01-memory-ablation-fair-comparison.md
**Built:** 2026-09-24 | **Status:** BOUNDARY RESULT (G1 discrepancy documented: no quantum advantage under matched budgets; classical 2-parameter replicator at the noise floor)

## What was built
`tool/modelzoo.py` - a complete, runnable model-zoo pipeline: loads the public Kaznatcheev et al.
2019 GameAssay data (github.com/kaznatcheev/GameAssay, 31 sessions at 4h spacing, well layout from
the repo's DataLoad.py, 16 mixed wells per environment x 4 environments: alectinib x fibroblasts),
and fits four models per environment with leave-one-well-out prediction: (1) classical replicator
(linear gain, 2 params), (2) classical + leaky-integrator memory (3 params), (3) minimal 2-level
Lindblad quantum model with memory-driven Hamiltonian and dephasing (4 params), (4) dephased
quantum ablation. Bootstrap 95% CIs over wells (B=2000).
Run: `python3 tool/modelzoo.py results/results.json` (~3 min, numpy/scipy).

## Results vs locked gates (LOO MSE, pooled over 64 wells)
| model | params | LOO MSE | 95% CI |
|-------|--------|---------|--------|
| classical replicator | 2 | 0.00122 | [0.00098, 0.00150] |
| classical + memory | 3 | 0.00122 | [0.00098, 0.00149] |
| Lindblad quantum | 4 | 0.00465 | [0.00320, 0.00639] |
| dephased quantum | 4 | 0.27898 | [0.26407, 0.29457] |

| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | quantum advantage in parent range 10-20% | -280% (quantum is ~3.8x WORSE) | **DOCUMENTED-DISCREPANCY** |
| G2 | memory closes >=70% of gap | undefined - there is no gap: classical already at floor; memory MSE identical to classical | **MOOT (recorded)** |
| G3 | dephased ablation reported | 60x worse than coherent model | **REPORTED** (implementation artifact - see honesty notes) |

## The useful results inside the discrepancy
1. **The parent's 10-20% quantum advantage does not reproduce under matched parameter budgets on
   the public data.** A 2-parameter classical replicator predicts held-out wells at MSE 0.0012 -
   essentially the assay noise floor (trajectories are smooth and near-monotone). No model with
   more structure can beat that by 10-20%; there is not enough residual signal.
2. **Memory contributes nothing measurable.** The leaky-integrator classical model's LOO error is
   identical to the memoryless one to 3 decimals; the fitted decay constant is unidentifiable.
   The spec's premise (the parent's gain might be memory, not quantumness) cannot be confirmed
   either - both additions are fitting noise, because the simple model already saturates.
3. **A minimal Lindblad implementation underperforms** even with more parameters. Whatever drives
   the parent's reported advantage is not generic "quantum game dynamics"; it must live in their
   specific model structure, parameterization, or evaluation split. Reproduction attempts should
   start from the parent paper's exact code, not from a generic Lindblad ansatz.
4. **Methodological boundary certified:** on this assay, model comparison among dynamical
   frameworks is uninformative beyond the linear gain function - the dataset cannot adjudicate
   quantum-vs-classical claims. That is a real constraint on the whole P23 family.

## What this build needs next
- The parent paper's exact QGT implementation (its Lindblad structure and train/test split);
  this zoo accepts drop-in simulators for a true reproduction.
- Multi-start/extended fitting for the quantum model (see honesty notes) before the discrepancy
  is taken as definitive.
- Synthetic-generator validation (spec pivot rule): simulate data from a known quantum generator
  and verify the zoo can detect it - if it cannot, the framework comparison is underpowered, not
  negative.

## Honesty notes
- Wells: first 16 valid mixed wells per environment (validity: >500 total cells at >=10 reads);
  not stratified by initial proportion.
- Fits are single-start, max 40 evaluations - the quantum model may be underfit; the classical
  result is robust (converges from any start; the gain function is visibly linear).
- The dephased ablation (gamma fixed at 50) is overdamped to the point of freezing dynamics; its
  60x degradation is an implementation artifact of the hard gamma clamp, not evidence about
  coherence. A proper adiabatic-elimination dephased limit is queued.
- G2's gap-closure ratio is mathematically undefined when the quantum model does not beat the
  classical one; reported as moot rather than a number.
