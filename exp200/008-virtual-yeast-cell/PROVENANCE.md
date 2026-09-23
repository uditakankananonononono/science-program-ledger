# PROVENANCE — DOC-1-008

## Public inputs (URLs + SHA-256)
- Yeast8 model: https://raw.githubusercontent.com/SysBioChalmers/yeast-GEM/main/model/yeast-GEM.xml
  SHA-256 30842b15eefb0ef7e36cbdea86a9efddfacf69a871c8b054165faa9af9f6c8eb (data/yeast-GEM.xml)
- iMM904 baseline model: https://bigg.ucsd.edu/static/models/iMM904.json
  SHA-256 1f7c573c2cf3da104fe48c49d6ae8e5a4a3472e7dc03c173c660e8bd9bb2557f (data/iMM904.json)
- SGD frozen truth: https://downloads.yeastgenome.org/curation/literature/phenotype_data.tab
  SHA-256 0ef7fdf3db0272b215a97b7b3c474aa755aaff8199ac56c3ace310bc9c357769 (data/phenotype_data.tab)
  Truth build: null alleles, viability column; per-gene collapse inviable-wins ->
  results/sgd_truth.json (6,266 genes: 1,245 inviable / 5,021 viable), built before any model scoring.

## Gates (locked before outcomes; SHA-256)
- GATES.md bf8afbfb06a3a1b13782c25b972d60a5245e1557b17a5035366bad9f460d189a
- GATES_ADDENDUM_A.md b07959aa16b7b20210bcfef7ac1f955f8a2e252a8f030a55df403370e4f61e4a
  (HiGHS solver swap, GPR-aware KO, unsolvable-gene rule; locked before valid G1 metrics)
- GATES_ADDENDUM_B.md e1a57a9f572eb752eb9d53dc5ad6ad28a242e610d5b6dd682c7159b68ba8e8e3
  (rich-medium YPD-matched arm, thresholds unchanged; parent-adjudicated legitimate 02:56;
  locked before any rich-medium results)

## Code (SHA-256)
- code/g1_scan_highs.py 869d5d6726d6c8e3d6fb882a0b4178bb27c7d9af298e8589eda8d361e007e3b9
- code/g1_scan_rich.py f769c1e4277b5ab34e750fa483240d6a4a020ce510f1d9f90cc0312c4336ad3b
- code/g1_score.py 5d88d127129a805b08529faf6e61f17bf5fee48338b470d5a49986a37152d8a3
- code/g2_succinate_scan.py b9836ec0dcf78e25f7fae282fc77a7251a193809e1aaf69489b4d4f76956e394
- code/g2_growth_coupled.py 07d8c255efdec2bcef8f4dbae8b46cf1f55ca18e467136223ecf21b83b3ad097
- yeast_cell.py 432cb75548540a592433624281906d7ec56e085aafc43ae1bea76a2e86519e86

## Key result artifacts (SHA-256)
- results/g1_official.json 9f866be7e3c72704e674710e8790fa12c60a261ed3d281cc88763c57296ddccd
- results/g2_gc90_ranked.json 1dcc1c9a57b7b5f74dc7165072351c08a19b674d7f40ffb9e2137e0d461aa048
- Rich-medium exchange sets: results/rich_medium_yeast8.json (72), results/rich_medium_imm904.json (55)

## Literature (mechanism check)
- Otero et al. 2012, PLoS ONE 7(12):e54144, doi:10.1371/journal.pone.0054144 (fetched full text)
- Biosci Biotechnol Biochem 2014, doi:10.1080/09168451.2014.877816 (SDH1/SDH2 disruption)
- FEMS Yeast Res 2017, doi:10.1093/femsyr/fox057 (review; Arikawa 1999 SDH1+FUM1)
- Raab et al. 2010, Metab Eng, PubMed 20854924

## Environment
python 3.10, cobra 0.32.1, scipy HiGHS (linprog method='highs', time_limit 20s), torch unused here.
All FBA in-environment; no external APIs, no cost.
