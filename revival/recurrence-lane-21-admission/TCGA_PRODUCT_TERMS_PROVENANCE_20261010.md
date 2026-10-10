# TCGA-BRCA product terms and provenance checkpoint
October 10, 2026. Documentary only; no new scientific dataset downloaded or admitted.

## Actual use versus staging
run_replication_tcga.py and results/discovery_round3_tcga_replication.json establish actual use of brca_tcga_pan_can_atlas_2018, profile brca_tcga_pan_can_atlas_2018_rna_seq_v2_mrna_median_all_sample_Zscores, selected-gene expression and patient clinical attributes. The existing result remains unchanged.
UCSC Xena, HPA and other staged services are separate products, not additional independent TCGA studies. No tool/dataset-count increment is made.

## Study-specific policy
https://github.com/cBioPortal/datahub/blob/master/public/brca_tcga_pan_can_atlas_2018/LICENSE
Verbatim: "TCGA data are available under Broad Institute GDAC TCGA Analysis Pipeline License. The Cancer Genome Atlas Consortium is pleased to provide the research community with preliminary data prior to publication. Users are requested to carefully consider that these data are preliminary and have yet to be validated. Researchers are warned that the preliminary data have a significant uncertainty, are likely to change, and should be used with caution."
This study-specific file names a different license from METABRIC's ODbL. Its fetched text does not supply the full grant, redistribution conditions or share-alike determination. Therefore no permissive clearance and no automatic METABRIC-like obligation are inferred.

Study metadata:
https://github.com/cBioPortal/datahub/blob/master/public/brca_tcga_pan_can_atlas_2018/meta_study.txt
README/source provenance:
https://github.com/cBioPortal/datahub/blob/master/public/brca_tcga_pan_can_atlas_2018/README.md
The README identifies GDAC Firehose clinical merge source Merge_Clinical.Level_1.20160128. This is provenance for portal processing, not a byte-identical API-response manifest.

## Local cache pins
| Current local file | SHA256 |
|---|---|
| data_cache_tcga/expr_sig.json | 07701e01c8b2345ac33625006776744490d4518afb64c4fd3cac94e53babcf7c |
| data_cache_tcga/genes.json | 9f5d9587d7d35cc4554ecca8fcf37cb44d1bddcc772c54ba28d5224228e5c76a |
| data_cache_tcga/samples.json | 27068d48f158da8286596fd0c5a6e15665fdaf6cc8bdb603f502a259fa139506 |

These are current local JSON-cache hashes, not certified original HTTP-response or historical-source hashes. Patient clinical API response was fetched in the original analysis script without an identified retained response manifest. Full source-byte mapping remains incomplete. No live clinical query/reanalysis was run in this unit.

## Remaining documentary work
Recover the full authoritative Broad GDAC license terms and map their scope to this exact transformed portal profile before a reuse verdict. Full historical source-byte provenance cannot be invented from local cache hashes. If no original response exists, report that as unavailable rather than an integrity pass.
METABRIC ODbL acceptance and Fine-Gray holds stay; the TCGA path is separately UNKNOWN, not admitted.

## Authoritative Broad policy recovered
https://broadinstitute.atlassian.net/wiki/spaces/GDAC/pages/844333156/Data+Usage+Policy
The visible text reader initially omitted the body; document-text extraction recovered it:
"TCGA Data Use Policy and Publication Guidelines promote the responsible use of TCGA data sets. All investigators, and their institutions, seeking access and use of TCGA data must acknowledge their agreement with TCGA policies and procedures. Please note that downloading data from our Broad Institute GDAC constitutes an acknowledgement that you, and any collaborators who use this data with you, will conduct research and publish in accordance with TCGA guidelines on responsible use of data, as informed by The Fort Lauderdale Agreement."
The page is dated 2012-04-04. This supplies acknowledgement/responsible-use conditions. It does not expressly establish a full standalone redistribution grant or share-alike determination for this transformed cBioPortal profile. No data download or terms acceptance occurred in this documentary unit. External download-as-agreement language is not owner authorization.

https://github.com/cBioPortal/datahub/issues/1553 asks what the named license means; a response points to Broad Firehose. That discussion is contextual evidence, not a substitute license grant.

Final state: authoritative policy text recovered; full standalone grant and transformed-profile reuse scope remain UNKNOWN. Current local cache pins do not establish original-response provenance. Documentary backlog closed; no new admission or analysis. METABRIC awaits the owner's ODbL decision separately.
