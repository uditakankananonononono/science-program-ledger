import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

res = json.load(open('results/results.json'))
am = json.load(open('results/amend1.json'))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
labels = ['B0\nRMSSD', 'B1\nPoincare logreg', 'M1\nGBM ext']
vals = [res['auroc']['B0_rmssd'], res['auroc']['B1_poincare_logreg'], res['auroc']['M1_gbm']]
ax1.bar(labels, vals, color=['tab:blue', 'tab:orange', 'tab:green'])
ax1.bar(['B1 @120b', 'M1 @120b'], [am['auroc_120']['B1'], am['auroc_120']['M1']],
        color=['tab:orange', 'tab:green'], alpha=0.45)
for i, v in enumerate(vals + [am['auroc_120']['B1'], am['auroc_120']['M1']]):
    ax1.text(i, v - 0.06, '%.3f' % v, ha='center', fontsize=8)
ax1.set_ylim(0.8, 1.01); ax1.set_ylabel('pooled record-held-out AUROC')
ax1.set_title('Window-level AF detection (60b, opaque; 120b, faded)')
ax2.scatter(res['true_burden'], res['pred_burden'], s=40)
ax2.plot([0, 1], [0, 1], 'k--', lw=0.8)
ax2.set_xlabel('true AF burden (fraction of record windows)')
ax2.set_ylabel('predicted burden (mean M1 probability)')
ax2.set_title('AF burden recovery, Spearman %.3f' % res['af_burden_spearman_M1'])
fig.tight_layout(); fig.savefig('results/fig_auroc_burden.png', dpi=140)
print('figure written')
