import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = json.load(open('results/results.json'))
a = json.load(open('results/amend1.json'))
df = pd.read_csv('results/predictions.csv')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
c = r['bace_classification']
labels = ['B0\n3-desc', 'B1\nbin-ECFP', 'M1\nGBM full']
vals = [c['B0_3desc'], c['B1_binECFP'], c['M1_gbm']]
ax1.bar(labels, vals, color=['tab:blue', 'tab:orange', 'tab:green'])
ax1.bar(['BBBP->BACE\ntransfer M1', 'P1 desc-only\ntransfer'],
        [r['transfer_bbbp_to_bace_M1'], a['P1_desc_only_bbbp_to_bace_auroc']],
        color=['tab:red', 'tab:red'], alpha=0.55)
for i, v in enumerate(vals + [r['transfer_bbbp_to_bace_M1'], a['P1_desc_only_bbbp_to_bace_auroc']]):
    ax1.text(i, v + 0.01, '%.3f' % v, ha='center', fontsize=8)
ax1.axhline(0.5, color='k', lw=0.8, ls='--')
ax1.set_ylabel('AUROC'); ax1.set_title('BACE classification + failed cross-task transfer')
ax1.tick_params(axis='x', labelsize=8)
ax2.scatter(df['pIC50'], df['sGBM'], s=8, alpha=0.5)
ax2.plot([df.pIC50.min(), df.pIC50.max()], [df.pIC50.min(), df.pIC50.max()], 'k--', lw=0.8)
ax2.set_xlabel('true pIC50'); ax2.set_ylabel('predicted pIC50 (GBM)')
ax2.set_title('pIC50 regression, Spearman %.3f (ridge 8-desc %.3f)' % (
    r['regression_pIC50']['gbm_full_spearman'], r['regression_pIC50']['ridge_8desc_spearman']))
fig.tight_layout(); fig.savefig('results/fig_bace.png', dpi=140)
print('figure written')
