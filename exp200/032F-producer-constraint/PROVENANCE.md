# 032F PROVENANCE
- Producer annotations (AGORA2/DEMETER curated tables, opencobra/COBRA.papers, CC-BY paper
  s41587-022-01628-0): https://raw.githubusercontent.com/opencobra/COBRA.papers/master/2021_demeter/input/{secretionProductTable,FermentationTable,BileAcidTable,PutrefactionTable,uptakeTable}.txt + AGORA2_infoFile.xlsx (fetched 2026-09-24).
- PRISM taxa + metadata: hallucigenia-sparsa/seqgroup data/ibd_taxa.rda, ibd_metadata.rda,
  ibd_lineages.rda (PRISM cohort, Franzosa/Mallick; original SRA BioProject PRJNA400072).
- PRISM metabolites: 032 workspace mpcomp.txt (Metabolomics Workbench PR000677, G-number
  rows) — join key = ibd_metadata$SRA_metagenome_name.
- HMP2 frozen: 032's committed artifacts (hmp2_meas.npy, hmp2_final_map.json,
  paired_ids.json, armA_frozen_rho.json, armB_frozen_rho.json) + per-sample
  taxonomic_profile.biom from https://g-227ca.190ebd.75bc.data.globus.org/ibdmdb//products/HMP2/MGX/2018-05-04/tax_profiles/ (official IBDMDB Globus endpoint).
- No new external labels; the 12-compound evaluable set is fixed by annotation availability
  only (coverage032F.json), committed pre-scoring.
