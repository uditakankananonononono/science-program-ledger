import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = json.load(open('results/results.json'))
a = json.load(open('results/amend1.json'))
dirs = ['DS1_train_DS2_test', 'DS2_train_DS1_test']
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
x = np.arange(2); w = 0.25
for i, m in enumerate(['B0', 'B1', 'M1']):
    ax1.bar(x + i*w, [r[d][m]['acc'] for d in dirs], w, label=m)
ax1.set_xticks(x + w); ax1.set_xticklabels(['DS1->DS2', 'DS2->DS1'])
ax1.set_ylim(0.8, 1.0); ax1.set_ylabel('overall accuracy'); ax1.legend(fontsize=8)
ax1.set_title('Inter-patient accuracy (morphology hurts B1 in DS2->DS1)')
classes = ['N', 'S', 'V', 'F']
x2 = np.arange(len(classes)); w2 = 0.18
for i, (lab, getter) in enumerate([
        ('M1 base', lambda d, c: r[d]['M1']['per_class_sens'].get(c, 0)),
        ('M1 +S-oversample (P1)', lambda d, c: a['P1_S_oversample'][d].get(c + '_sens', np.nan) if c in ('S','V') else np.nan)]):
    vals = [np.nanmean([getter(d, c) for d in dirs]) for c in classes]
    ax2.bar(x2 + i*w2, vals, w2, label=lab)
ax2.set_xticks(x2 + w2/2); ax2.set_xticklabels(classes)
ax2.set_ylabel('sensitivity (mean of both directions)')
ax2.set_title('Per-class sensitivity: S stays unlearnable, V is strong')
ax2.legend(fontsize=8)
fig.tight_layout(); fig.savefig('results/fig_interpatient.png', dpi=140)
print('figure written')
