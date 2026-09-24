import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('results/minute_predictions.csv')
res = json.load(open('results/results.json'))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
ax1.hist(df.loc[df.y == 0, 'pM1'], bins=50, alpha=0.6, density=True, label='normal minutes')
ax1.hist(df.loc[df.y == 1, 'pM1'], bins=50, alpha=0.6, density=True, label='apnea minutes')
ax1.set_xlabel('M1 predicted apnea probability'); ax1.set_ylabel('density')
ax1.set_title('Per-minute scores (record-held-out)'); ax1.legend(fontsize=8)
rs = res['record_scores_M1']
order = sorted(rs, key=lambda r: rs[r])
colors = ['tab:red' if r[0] == 'a' else 'tab:orange' if r[0] == 'b' else 'tab:green' for r in order]
ax2.bar(range(len(order)), [rs[r] for r in order], color=colors)
ax2.set_xticks(range(len(order))); ax2.set_xticklabels(order, rotation=90, fontsize=6)
ax2.set_ylabel('mean M1 apnea probability')
ax2.set_title('Record-level score (red=a apnea, orange=b borderline, green=c control)')
fig.tight_layout(); fig.savefig('results/fig_scores.png', dpi=140)
print('figure written')
