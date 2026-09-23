#!/usr/bin/env python3
"""PPD risk-score CLI (DOC-PPD payload) - STATUS: FAILED external verification.
Applies the frozen 200-gene ElasticNet panel (discovery: GSE45603, 1st+3rd trimester)
to a JSON {gene_symbol: expression_value} (microarray log-intensity scale; missing panel
genes are imputed to their discovery-cohort means, documented).
WARNING: external-cohort AUROC was 0.429 (below chance) - this panel did NOT transport.
Shipped for audit/reuse, not for screening use."""
import sys, json
import numpy as np, joblib
d=joblib.load('results/ppd_panel_model.joblib')
counts=json.load(open(sys.argv[1]))
v=np.array([counts.get(g,np.nan) for g in d['genes']],np.float32)
v=np.where(np.isnan(v),d['gene_means'],v)
print(json.dumps(dict(ppd_score=float(d['model'].predict_proba(v[None,:])[0,1]),panel_genes_provided=int(np.sum([g in counts for g in d['genes']])),status='FAILED external verification (AUROC 0.429) - research/audit use only'),indent=2))
