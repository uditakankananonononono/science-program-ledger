"""P1: per-fold training-chosen threshold for M1, accuracy on held-out record."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score

CACHE = os.path.expanduser('~/work/apnea45/feat_cache')
RECS = ([f'a{i:02d}' for i in range(1, 21)] + [f'b{i:02d}' for i in range(1, 6)]
        + [f'c{i:02d}' for i in range(1, 11)])
Xs, ys, gs = [], [], []
for rec in RECS:
    z = np.load(os.path.join(CACHE, rec + '.npz'))
    Xs.append(z['X']); ys.append(z['y']); gs += [rec] * len(z['y'])
X = np.vstack(Xs); y = np.concatenate(ys); groups = np.array(gs)

grid = np.arange(0.05, 0.96, 0.01)
test_pred = np.full(len(y), -1, dtype=int)
thr_used = {}
for r in np.unique(groups):
    tr, te = groups != r, groups == r
    m = HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
        min_samples_leaf=20, l2_regularization=1.0,
        early_stopping=False, random_state=1).fit(X[tr], y[tr])
    ptr = m.predict_proba(X[tr])[:, 1]
    accs = [accuracy_score(y[tr], ptr > t) for t in grid]
    t_best = float(grid[int(np.argmax(accs))])
    thr_used[r] = t_best
    test_pred[te] = (m.predict_proba(X[te])[:, 1] > t_best).astype(int)
acc = float(accuracy_score(y, test_pred))
out = {'P1_pooled_accuracy_train_threshold': acc,
       'P1_gate_ge_0.80': bool(acc >= 0.80),
       'threshold_median': float(np.median(list(thr_used.values())))}
print(json.dumps(out, indent=1))
json.dump(out, open('results/amend1.json', 'w'), indent=1)
