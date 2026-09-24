# 032F GATES ADDENDUM A — locked 2026-09-24 11:30 IST, BEFORE any model fitting or scoring

## Erratum: evaluable set 12 keys -> 10 distinct compounds
The locked 12-item list contains two synonym duplicate keys: 'deoxycholate' and
'lithocholate' are HMP2-side synonym keys of 'deoxycholic.acid' and 'lithocholic.acid'
(hmp2_final_map maps both synonyms to the SAME HMP2 rows 47 and 45). The evaluable set is
therefore 10 DISTINCT compounds: propionate, butyrate...isobutytare., cholate,
chenodeoxycholate, deoxycholic.acid, lithocholic.acid, chenodeoxycholate.deoxycholate.,
putrescine, glutamate, N.acetylspermidine. All gate fractions and bars are computed over
these 10. Canonical keys for ARM A/ARM B bar lookup: deoxycholic.acid, lithocholic.acid.

## PRISM cluster->name bridge (locked, verified)
mpcomp.txt columns are unnamed LC-MS cluster IDs. Bridge to compound names:
(1) direct annotation from ST001000 mwTab (Metabolomics Workbench, Franzosa PRISM study):
    25 of 80 clusters carry direct names;
(2) positional correspondence between model.txt (shipped MelonnPan weights, 80 named
    columns) and mpcomp.txt (80 cluster columns): verified against ALL 25 direct anchors -
    24 exact matches + 1 exact synonym (2-hydroxymyristic acid = X2.hydroxymyristic.acid,
    same compound) = 25/25 agreement. Positional naming adopted for the 10 targets;
    direct-name agreement verified where available (cholate, chenodeoxycholate confirmed;
    others have no direct mwTab name and rest on the 25/25 positional validation).
Target clusters: propionate=HILIC-neg_Cluster_0003 (pos 27), butyrate...isobutytare.=
HILIC-neg_Cluster_0013 (pos 28); remaining 8 resolved in scoring manifest (committed).
