import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

res = json.load(open('results/results.json'))
pg = res['logo']['per_gene']
genes = sorted(pg['B1'], key=lambda g: pg['M1'][g])
x = np.arange(len(genes)); w = 0.27
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
ax1.bar(x - w, [pg['B0'][g] for g in genes], w, label='B0 GC-only')
ax1.bar(x,     [pg['B1'][g] for g in genes], w, label='B1 RS1-style ridge')
ax1.bar(x + w, [pg['M1'][g] for g in genes], w, label='M1 boosted (ext feats)')
ax1.set_xticks(x); ax1.set_xticklabels(genes, rotation=45, ha='right', fontsize=8)
ax1.set_ylabel('Spearman (held-out gene)')
ax1.set_title('Leave-one-gene-out on Doench 2014')
ax1.legend(fontsize=8); ax1.axhline(0, color='k', lw=0.5)
tg = res['transfer_v2']['per_gene']
tgenes = sorted(tg, key=lambda g: tg[g]['M1'])
x2 = np.arange(len(tgenes))
ax2.bar(x2 - 0.2, [tg[g]['B1'] for g in tgenes], 0.4, label='B1')
ax2.bar(x2 + 0.2, [tg[g]['M1'] for g in tgenes], 0.4, label='M1')
ax2.set_xticks(x2); ax2.set_xticklabels(tgenes, rotation=45, ha='right', fontsize=7)
ax2.set_ylabel('Spearman')
ax2.set_title('Transfer to Doench 2016 (trained on V1, no refit)')
ax2.legend(fontsize=8); ax2.axhline(0, color='k', lw=0.5)
fig.tight_layout(); fig.savefig('results/fig_logo_transfer.png', dpi=140)
print('figure written')
