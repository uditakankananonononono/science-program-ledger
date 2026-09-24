"""P1: descriptor-only logistic, trained on all BBBP, scored on BACE."""
import json, os
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

DATA = os.path.expanduser('~/work/bace53/data')

def desc8(smiles_list):
    out = []
    for sm in smiles_list:
        m = Chem.MolFromSmiles(max(str(sm).split('.'), key=len))
        if m is None:
            out.append(None); continue
        out.append([Crippen.MolLogP(m), Descriptors.MolWt(m),
                    rdMolDescriptors.CalcTPSA(m), rdMolDescriptors.CalcNumHBD(m),
                    rdMolDescriptors.CalcNumHBA(m), rdMolDescriptors.CalcNumRotatableBonds(m),
                    rdMolDescriptors.CalcFractionCSP3(m),
                    sum(1 for a in m.GetAtoms() if a.GetIsAromatic()) / max(m.GetNumAtoms(), 1)])
    return out

bbbp = pd.read_csv(os.path.join(DATA, 'BBBP.csv'))
db = desc8(bbbp['smiles'].tolist())
ok = [i for i, d in enumerate(db) if d is not None]
Xbb = np.array([db[i] for i in ok], dtype=np.float32)
ybb = bbbp['p_np'].to_numpy()[ok]

bace = pd.read_csv(os.path.join(DATA, 'bace.csv'))
dc = desc8(bace['mol'].tolist())
okb = [i for i, d in enumerate(dc) if d is not None]
Xb = np.array([dc[i] for i in okb], dtype=np.float32)
yb = bace['Class'].to_numpy()[okb]

mu, sd = Xbb.mean(0), Xbb.std(0); sd[sd == 0] = 1
m = LogisticRegression(C=1.0, max_iter=2000).fit((Xbb - mu) / sd, ybb)
p = m.predict_proba((Xb - mu) / sd)[:, 1]
auc = float(roc_auc_score(yb, p))
out = {'P1_desc_only_bbbp_to_bace_auroc': auc, 'P1_gate_ge_0.60': bool(auc >= 0.60)}
print(json.dumps(out, indent=1))
json.dump(out, open('results/amend1.json', 'w'), indent=1)
