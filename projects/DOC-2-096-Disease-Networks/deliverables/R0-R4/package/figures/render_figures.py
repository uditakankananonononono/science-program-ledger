#!/usr/bin/env python3
"""Deterministically render the two new package figures from frozen CSVs only.
No scientific scoring, filtering, ranking, inference, or new analysis.
Requires matplotlib 3.10.9. Run from any directory.
The R0 figure is reused byte-identically from the frozen R0 tree; it is not
rerendered. Its sidecar records the frozen figure's own SHA-256.
"""
import csv, hashlib, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R2RES = os.path.join(ROOT, "frozen", "rounds", "DOC-2-096-R2-archives-20260921.tar-b0e91108", "DOC-2-096-R2-archives", "results")
R4RES = os.path.join(ROOT, "frozen", "rounds", "DOC-2-096-R4-competing-risks-20260921.tar-ed93bfa9", "DOC-2-096-R4-competing-risks", "results")
R0FIG = os.path.join(ROOT, "frozen", "rounds", "DOC-2-096-R0-negative-evidence-20260921.tar-ee188207", "DOC-2-096-R0-negative-evidence", "figures", "source_instability.png")
OUT = os.path.join(ROOT, "figures")
def sha(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def rows(path):
    with open(path, newline="", encoding="utf-8") as f: return list(csv.DictReader(f))
def r2_transport():
    src = os.path.join(R2RES, "locked_temporal_metrics.csv"); R = rows(src)
    models = ["raw", "positive_only", "reliability"]; trans = ["2020_to_2023", "2023_to_current"]
    def val(m, t, k): return [float(r[k]) for r in R if r["model"] == m and r["transition"] == t][0]
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.8))
    x = range(len(models)); w = 0.36
    for ax, key, title in ((axs[0], "brier", "Brier score"), (axs[1], "top_decile_enrichment", "Top-decile enrichment")):
        ax.bar([i - w/2 for i in x], [val(m, trans[0], key) for m in models], width=w, color="#315b91", label="2020->2023 (development)")
        ax.bar([i + w/2 for i in x], [val(m, trans[1], key) for m in models], width=w, color="#b9cae1", label="2023->current (replication)")
        ax.set_xticks(list(x)); ax.set_xticklabels(["raw", "positive-only", "reliability"], fontsize=8)
        ax.set_title(title, fontsize=10); ax.spines[["top", "right"]].set_visible(False)
        if key == "top_decile_enrichment": ax.axhline(1.0, color="#888888", linewidth=0.8, linestyle="--")
    axs[0].legend(fontsize=7, frameon=False)
    fig.suptitle("R2 locked temporal metrics (frozen values)")
    fig.text(.01, .01, "Source SHA-256: " + sha(src), fontsize=6); fig.tight_layout(rect=(0, .04, 1, .94))
    fig.savefig(os.path.join(OUT, "r2_locked_transport.png"), dpi=180, metadata={"SourceSHA256": sha(src)})
    plt.close(fig)
    open(os.path.join(OUT, "r2_locked_transport.SOURCE.sha256"), "w", encoding="utf-8").write(
        sha(src) + "  " + os.path.relpath(src, ROOT) + "\n")
def r4_enrichment():
    src = os.path.join(R4RES, "competing_risk_metrics.csv"); R = [r for r in rows(src) if r["split"] == "test"]
    targets = ["emergence", "resolution", "upgrade"]
    feats = []
    for r in R:
        if r["feature"] not in feats: feats.append(r["feature"])
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.4), sharey=False)
    for ax, t in zip(axs, targets):
        vals = [float(r["top10_enrichment"]) for r in R if r["target"] == t and r["split"] == "test"]
        labs = [r["feature"] for r in R if r["target"] == t and r["split"] == "test"]
        ax.bar(range(len(vals)), vals, color="#315b91")
        ax.axhline(1.0, color="#888888", linewidth=0.8, linestyle="--")
        ax.set_xticks(range(len(vals))); ax.set_xticklabels(labs, rotation=45, ha="right", fontsize=7)
        ax.set_title(t + " (replication)", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
        for i, v in enumerate(vals): ax.text(i, v + 0.05, "%.2f" % v, ha="center", fontsize=7)
    axs[0].set_ylabel("Top-decile enrichment")
    fig.suptitle("R4 competing-risk-set replication enrichment (frozen values)")
    fig.text(.01, .01, "Source SHA-256: " + sha(src), fontsize=6); fig.tight_layout(rect=(0, .06, 1, .93))
    fig.savefig(os.path.join(OUT, "r4_competing_risk_enrichment.png"), dpi=180, metadata={"SourceSHA256": sha(src)})
    plt.close(fig)
    open(os.path.join(OUT, "r4_competing_risk_enrichment.SOURCE.sha256"), "w", encoding="utf-8").write(
        sha(src) + "  " + os.path.relpath(src, ROOT) + "\n")
def r0_sidecar():
    open(os.path.join(OUT, "r0_source_instability.SOURCE.sha256"), "w", encoding="utf-8").write(
        sha(R0FIG) + "  " + os.path.relpath(R0FIG, ROOT) + "\n")
if __name__ == "__main__": r2_transport(); r4_enrichment(); r0_sidecar()
