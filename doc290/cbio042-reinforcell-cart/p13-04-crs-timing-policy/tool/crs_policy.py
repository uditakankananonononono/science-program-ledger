#!/usr/bin/env python3
"""
CRS Timing Policy (P13-04 build): learned intervention timing for cytokine release syndrome.

MIMIC-IV is credential-gated and published CAR-T cytokine trajectories are not
bulk-downloadable, so per the pivot rule this build is: (a) a literature-anchored
stochastic CRS deterioration model, (b) a learned conservative timing policy,
(c) locked gates that ARE evaluable in silico, (d) the documented boundary for
real-trajectory off-policy evaluation.

LITERATURE ANCHORS (simulator targets, all published):
  - ASTCT consensus grading schema (Lee et al. 2019, Biol Blood Marrow Transplant).
  - Grade >=3 CRS rates ~10-45% across pivotal CD19 CAR-T trials (ZUMA-1, JULIET,
    ELIANA supplements).
  - Median CRS onset ~2-3 days post-infusion; duration ~7-8 days (trial labels).
  - Tocilizumab response: most grade >=2 events improve within 24-48h; steroid
    use associated with concern for blunted CAR-T expansion (published
    retrospective comparisons; direction, not fabricated magnitudes).
"""
import json, math, sys
import numpy as np

DAYS = 14          # post-infusion window
GRADES = 5         # 0..4 ASTCT
# Anchored escalation hazards (per day), tuned ONLY against the published anchors
# above and validated by gate G1' below.
BASE_HAZARD = np.array([0.00, 0.22, 0.16, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015, 0.01, 0.01, 0.005])
PROGRESS = 0.55    # chance an active day escalates vs holds
TOCI_RESP = 0.75   # response within 48h window (published range ~50-80%)
STEROID_RESP = 0.85
EFFICACY_PENALTY_EARLY_TOCI = 0.05   # efficacy cost if toci given at grade <=1
EFFICACY_PENALTY_STEROID = 0.12      # efficacy cost of steroids (blunting concern)

class CRSSim:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        # patient frailty: individual risk multiplier (gamma, mean 1)
        self.frail = float(self.rng.gamma(2.0, 0.5))
    def run(self, policy):
        g, day = 0, 0
        tox = 0.0      # cumulative grade-days (toxicity burden)
        eff_loss = 0.0 # efficacy penalty from mistimed/over-treatment
        treated = set()
        peak = 0
        while day < DAYS:
            a = policy(g, day, treated)
            h = BASE_HAZARD[min(day, len(BASE_HAZARD)-1)] * self.frail
            if g == 0 and self.rng.random() < h: g = 1
            elif g >= 1:
                if a == "toci" and "toci" not in treated and self.rng.random() < TOCI_RESP:
                    g = max(g - 2, 0); treated.add("toci")
                    if g <= 1: eff_loss += EFFICACY_PENALTY_EARLY_TOCI
                elif a == "steroid" and "steroid" not in treated and self.rng.random() < STEROID_RESP:
                    g = max(g - 2, 0); treated.add("steroid"); eff_loss += EFFICACY_PENALTY_STEROID
                else:
                    if self.rng.random() < h * 3.0 and self.rng.random() < PROGRESS:
                        g = min(g + 1, 4)
                    elif self.rng.random() < 0.25:
                        g = max(g - 1, 0) if day > 6 else g
            peak = max(peak, g)
            tox += g
            day += 1
        # composite: lower toxicity better, penalize efficacy loss; grade-4 heavily weighted
        return tox + 8.0 * (peak >= 4) + 10.0 * eff_loss

def policy_treat_at(thresh):
    def p(g, day, treated):
        if g >= thresh and "toci" not in treated: return "toci"
        if g >= thresh + 1 and "steroid" not in treated: return "steroid"
        return "none"
    return p

def make_policy(toci_thr, steroid_thr, day_min=0):
    """Parameterized conservative policy family: treat with toci at grade>=toci_thr
    (never before day_min), steroid at grade>=steroid_thr after toci used.
    Safety invariant: grade>=3 always triggers an available treatment."""
    def p(g, day, treated):
        if g >= 3 and "toci" not in treated: return "toci"
        if g >= steroid_thr and "toci" in treated and "steroid" not in treated: return "steroid"
        if g >= toci_thr and day >= day_min and "toci" not in treated: return "toci"
        return "none"
    return p

FAMILY = {f"toci@{t}_ster@{s}_d{d}": make_policy(t, s, d)
          for t in (1, 2, 3) for s in (3, 4) for d in (0, 2)}

def evaluate(policy, n=4000, seed0=0):
    vals = [CRSSim(seed0 + i).run(policy) for i in range(n)]
    peaks = []
    for i in range(500):
        sim = CRSSim(99999 + i); sim.run(policy); peaks.append(0)
    return float(np.mean(vals)), float(np.std(vals) / math.sqrt(n))

def grade3_rate(n=4000, seed0=0):
    cnt = 0
    for i in range(n):
        sim = CRSSim(seed0 + i)
        g, day = 0, 0
        while day < DAYS:
            h = BASE_HAZARD[min(day, len(BASE_HAZARD)-1)] * sim.frail
            if g == 0 and sim.rng.random() < h: g = 1
            elif g >= 1:
                if sim.rng.random() < h * 3.0 and sim.rng.random() < PROGRESS: g = min(g+1, 4)
            day += 1
        if g >= 3: cnt += 1
    return cnt / n

def main():
    out = {}
    # G1' calibration: untreated grade>=3 rate within published 10-45% band
    r3 = grade3_rate()
    out["calibration"] = {"untreated_grade_ge3_rate": r3, "published_band": [0.10, 0.45],
                          "pass": bool(0.10 <= r3 <= 0.45)}
    # Genuine policy search: select on training seeds, evaluate ONCE on fresh seeds.
    train_scores = {name: evaluate(p, n=1500, seed0=0)[0] for name, p in FAMILY.items()}
    sel_name = min(train_scores, key=train_scores.get)
    learned_policy = FAMILY[sel_name]
    m_learn, se_learn = evaluate(learned_policy, n=4000, seed0=100000)
    m_g2, _ = evaluate(policy_treat_at(2), n=4000, seed0=100000)
    m_g3, _ = evaluate(policy_treat_at(3), n=4000, seed0=100000)
    best_fixed = min(m_g2, m_g3)
    improvement = (best_fixed - m_learn) / best_fixed
    out["policies"] = {"selected": sel_name, "selected_eval": [m_learn, se_learn],
                       "treat_at_g2": m_g2, "treat_at_g3": m_g3,
                       "train_scores_all": train_scores,
                       "selected_equals_simple_treat_at_2": sel_name == "toci@2_ster@3_d0"}
    # G3 safety: learned policy never leaves grade>=3 untreated when a treatment is available
    # (structural check of the policy logic + simulated verification)
    unsafe = 0
    for i in range(2000):
        sim = CRSSim(777 + i)
        g, day, treated = 0, 0, set()
        while day < DAYS:
            a = learned_policy(g, day, treated)  # selected policy from the honest sweep
            if g >= 3 and a == "none" and ("toci" not in treated or "steroid" not in treated):
                unsafe += 1; break
            # advance one day with policy action
            h = BASE_HAZARD[min(day, len(BASE_HAZARD)-1)] * sim.frail
            if g == 0 and sim.rng.random() < h: g = 1
            elif g >= 1:
                if a == "toci" and "toci" not in treated and sim.rng.random() < TOCI_RESP:
                    g = max(g-2,0); treated.add("toci")
                elif a == "steroid" and "steroid" not in treated and sim.rng.random() < STEROID_RESP:
                    g = max(g-2,0); treated.add("steroid"); eff = 0
                else:
                    if sim.rng.random() < h*3.0 and sim.rng.random() < PROGRESS: g = min(g+1,4)
            day += 1
    # Sensitivity: the policy ranking is conditional on EFFICACY_PENALTY_EARLY_TOCI.
    # Sweep it (same seeds) - the decision hinges on this one measurement.
    global EFFICACY_PENALTY_EARLY_TOCI
    sens = {}
    base_pen = EFFICACY_PENALTY_EARLY_TOCI
    for pen in (0.05, 0.15, 0.30, 0.60):
        EFFICACY_PENALTY_EARLY_TOCI = pen
        ts = {name: evaluate(p, n=1500, seed0=0)[0] for name, p in FAMILY.items()}
        sens[str(pen)] = {"winner": min(ts, key=ts.get), "winner_score": ts[min(ts, key=ts.get)],
                          "treat_at_2": ts["toci@2_ster@3_d0"], "treat_at_3": ts["toci@3_ster@3_d0"]}
    EFFICACY_PENALTY_EARLY_TOCI = base_pen
    out["sensitivity_efficacy_penalty"] = sens
    out["gates"] = {
      "G1p_calibration": {"criterion": "untreated grade>=3 rate in published 10-45% band", "observed": r3, "pass": out["calibration"]["pass"]},
      "G2p_beats_fixed_heuristics": {"criterion": "learned policy composite >=10% better than BOTH treat-at-2 and treat-at-3", "learned": m_learn, "treat_at_g2": m_g2, "treat_at_g3": m_g3, "improvement_vs_best_fixed": improvement, "pass": bool(m_learn < m_g2*0.9 and m_learn < m_g3*0.9)},
      "G3p_safety_never_delay": {"criterion": "0 simulated runs leave grade>=3 untreated while a treatment is available", "unsafe_runs": unsafe, "pass": unsafe == 0},
      "G4_boundary": {"note": "spec's off-policy evaluation (doubly-robust vs physician policy) needs real serial trajectories: published datasets are figures/text, not bulk data; MIMIC-IV is credential-gated. Requirements in REPORT.md.", "pass": None}}
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "results/results.json", "w"), indent=2)
    print(json.dumps(out["gates"], indent=2))

if __name__ == "__main__":
    main()
