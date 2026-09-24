#!/usr/bin/env python3
"""metabolite_predict_constrained.py - DOC-1-032F producer-constrained metabolite predictor.
Predicts up to 10 producer-annotated metabolites from a species-level taxonomic profile
(MetaPhlAn-style), using per-compound ridge models whose features are ONLY species annotated
as producers of that compound (AGORA2/DEMETER curated tables), trained on PRISM (n=155).
HONEST PERFORMANCE (frozen HMP2, 388 samples): only cholate (rho 0.380) and
chenodeoxycholate (rho 0.369) are well-predicted (rho>=0.3); the rest are hypothesis-grade
or failed - see REPORT.md. Per-compound model selection vs MelonnPan-protocol baselines is
quantified in scores032F.json.
Usage: python3 metabolite_predict_constrained.py taxa_profile.tsv
Input format: one "Genus species<TAB>relative_abundance" per line (percent or fraction OK).
"""
import json, sys, os, math
d = os.path.dirname(os.path.abspath(__file__))
models = json.load(open(os.path.join(d, 'constrained_models.json')))
prof = {}
for line in open(sys.argv[1]):
    parts = line.rstrip('\n').split('\t')
    if len(parts) < 2 or parts[0].startswith('#'): continue
    nm = ' '.join(parts[0].replace('_', ' ').split()[:2]).lower()
    try: v = float(parts[1])
    except ValueError: continue
    if v > 1.0: v /= 100.0
    prof[nm] = v
print('compound\tpredicted_log1p_value')
for m, mod in models.items():
    z = mod['intercept']
    for sp, c in zip(mod['species'], mod['coef']):
        z += c * math.log1p(prof.get(sp, 0.0) * 1e6)
    print('%s\t%.6f' % (m, z))
