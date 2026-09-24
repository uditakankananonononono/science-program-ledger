# QC audit - P06 CBIO013(2024) DeepGraphDTI pandemic screening

Auditor: Doc230 lane A v6 | 2026-09-24 11:03 IST | Every spec read in full; named data sources spot-checked by live fetch (HTTP 200 on portal/API, or an API query returning records). Specs name resources, not accession URLs - OK means the named resource is live and openly fetchable.

Verdicts: OK (build-ready) | FIX (small source/method edit before build) | REWRITE (controlled-access/dead core data or hand-wavy method)

Live checks: GitHub search for DeepGraphDTI returns 0 repos - the model code is NOT public. BindingDB 200; TDC (DAVIS/KIBA) 200; RCSB Nipah glycoprotein search returns 53 entries; NCBI Virus 200; MMV site 403 (bot-blocked) but Pathogen Box / Pandemic Response Box compound data is in ChEMBL (CHEMBL3637841, CHEMBL4513161 CO-ADD screen) - the open route.

| id | verdict | note |
|----|---------|------|
| P06-01 | FIX | DeepGraphDTI code is not public; substitute an open DTA model with structure graphs (GraphDTA/DGraphDTA public repos) and state the substitution in the header. Benchmarks live. |
| P06-02 | OK | NiV G/F structures verified (53 RCSB hits); Vina/smina/Gnina open. Hit identities must come from the parent abstract/paper. |
| P06-03 | FIX | Same model substitution as P06-01. |
| P06-04 | FIX | Same substitution; null-encoding design is concrete. |
| P06-05 | FIX | Henipavirus structures fine (AlphaFold API live); get box compound lists from ChEMBL, not mmv.org. |
| P06-06 | OK | Conformational-state structures + boxes via ChEMBL. |
| P06-07 | FIX | ESM-2 public; graph encoder side inherits the P06-01 substitution. |
| P06-08 | FIX | Inherits substitution; conformal libs open. |
| P06-09 | OK | NCBI Virus variation + ESM-2 + AlphaFold all live. |
| P06-10 | FIX | WHO list fine; box lists via ChEMBL documents (Pathogen Box CHEMBL3637841, Pandemic Response Box CO-ADD screen CHEMBL4513161). |
