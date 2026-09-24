import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = json.load(open('results/results.json'))
df = pd.read_csv('results/predictions.csv')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
labels = ['B0\n3 descriptors', 'B2\nTanimoto 1-NN', 'B1\nbinary ECFP logreg', 'M1\nGBM cnt-ECFP+']
vals = [r['auroc']['B0'], r['auroc']['B2'], r['auroc']['B1'], r['auroc']['M1']]
ax1.bar(labels, vals, color=['tab:blue', 'tab:gray', 'tab:orange', 'tab:green'])
for i, v in enumerate(vals):
    ax1.text(i, v - 0.07, '%.3f' % v, ha='center', fontsize=9)
ax1.set_ylim(0.7, 0.95); ax1.set_ylabel('pooled AUROC (scaffold-held-out)')
ax1.set_title('BBBP, Murcko-scaffold 5-fold CV')
ax2.hist(df.loc[df.y == 0, 'pM1'], bins=40, alpha=0.6, density=True, label='non-permeant')
ax2.hist(df.loc[df.y == 1, 'pM1'], bins=40, alpha=0.6, density=True, label='permeant')
ax2.set_xlabel('M1 predicted permeability probability'); ax2.set_ylabel('density')
ax2.set_title('Score separation (base rate 0.765)'); ax2.legend(fontsize=8)
fig.tight_layout(); fig.savefig('results/fig_bbbp.png', dpi=140)
print('figure written')
