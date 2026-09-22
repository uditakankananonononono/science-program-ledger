# Literature synthesis, pass 1

- Leakage is broader than duplicated samples: biological relatedness, site, batch, patient, molecular scaffold, and temporal dependence can make random splits optimistic. DataSAIL formalizes similarity-aware splitting; the Nature Methods leakage guide frames the audit questions.
- Hidden stratification shows aggregate medical-imaging metrics can hide clinically meaningful subgroup failures. Any universal audit needs subgroup discovery/evaluation, not only global AUC.
- TRIPOD+AI and PROBAST+AI jointly require transparent reporting and risk-of-bias/applicability assessment; the product should emit an evidence dossier aligned to both rather than only a score.
- External-validation reviews document that independent evaluation remains uncommon and performance often changes materially, supporting external delta as a central endpoint.
- Cross-study transcriptomic work shows preprocessing and batch correction can alter transport performance. A useful stress test must compare correction learned only on training data against leaky pooled correction.
- FDA/IMDRF GMLP principles make representative datasets, independent train/test sets, human-AI interaction, monitoring, and deployed-model performance relevant product requirements.

Open design decision: pick datasets with explicit group/site/batch fields and permissive redistribution. Do not select purely on convenience. Candidate modalities: multi-study transcriptomics, multi-site tabular clinical data, and imaging-derived tabular features.

# Dataset and competitive feasibility search, pass 1

## ds1
- BC-Atlas Expression Database | https://doi.org/10.5281/zenodo.20767603 | 2026-06-20
- Annotated Compendium of 102 Breast Cancer Gene ... | https://www.biorxiv.org/content/10.1101/2023.09.22.559045v2.full-text | 2023-09-27
- curatedBreastData Manual | https://bioconductor.posit.co/packages/3.22/data/experiment/vignettes/curatedBreastData/inst/doc/curatedBreastData-manual.pdf | None
- MetaGxData: Clinically Annotated Breast, Ovarian and Pancreatic Cancer Datasets and their Use in Generating a Multi-Cancer Gene Signature | Scientific Reports | https://preview-www.nature.com/articles/s41598-019-45165-4 | 2019-06-19
- MetaGxData: Breast and Ovarian Clinically Annotated Transcriptomics Datasets | bioRxiv | https://www.biorxiv.org/content/10.1101/052910v1 | None
- A collection of annotated and harmonized human... | F1000Research | https://f1000research.com/articles/6-296 | 2018-02-09
- CoINcIDE: A framework for discovery of patient subtypes across multiple datasets | https://doi.org/10.1186/s13073-016-0281-4 | 2016-03-09
- Dataset:  Public breast cancer transcriptomes reveal substantial cohort effects and limited reproducibility of ancestry-associated expression patterns | Zenodo | https://zenodo.org/records/20801204 | 2026-06-22
- MetaGxBreast: Transcriptomic Breast Cancer Datasets | https://mirrors.sunsite.dk/bioconductor/packages/release/data/experiment/manuals/MetaGxBreast/man/MetaGxBreast.pdf | None
- MetaGxBreast: Transcriptomic Breast Cancer Datasets | https://bioconductor.posit.co/packages/3.24/data/experiment/manuals/MetaGxBreast/man/MetaGxBreast.pdf | 2026-07-21

## ds2
- curatedBreastData: Curated breast cancer gene expression data with survival and treatment information | https://mirrors.dotsrc.org/bioconductor-releases/devel/data/experiment/manuals/curatedBreastData/man/curatedBreastData.pdf | None
- curatedBreastData Manual | https://bioconductor.posit.co/packages/3.20/data/experiment/vignettes/curatedBreastData/inst/doc/curatedBreastData-manual.pdf | None
- curatedBreastData: Curated breast cancer gene ... | https://bioconductor.uib.no/packages/3.20/data/experiment/manuals/curatedBreastData/man/curatedBreastData.pdf | 2015-02-25
- Bioconductor - curatedBreastData | https://ftp.accum.se/mirror/bioconductor.org/packages/release/data/experiment/html/curatedBreastData.html | None
- GSE33926 - Molecular characteristics and metastasis predictor genes of triple-negative breast cancer - OmicsDI | https://www.omicsdi.org/dataset/geo/GSE33926 | None
- GSE53752 - Molecular characteristics and metastasis predictor genes of triple-negative breast cancer (II) - OmicsDI | https://www.omicsdi.org/dataset/geo/GSE53752 | None
- Annotated Compendium of 102 Breast Cancer Gene ... | https://www.biorxiv.org/content/10.1101/2023.09.22.559045v2.full-text | 2023-09-27
- MetaGxData: Breast and Ovarian Clinically Annotated Transcriptomics Datasets | bioRxiv | https://www.biorxiv.org/content/10.1101/052910v1 | None
- DataMed | https://datamed.org/dataset/4663646 | None
- Package 'curatedBreastData' | https://mirror.accum.se/mirror/bioconductor.org/packages/3.11/data/experiment/manuals/curatedBreastData/man/curatedBreastData.pdf | 2015-02-25

## ds3
- UCI Machine Learning Repository | https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008 | None
- OpenML | https://www.openml.org/search?exact_name=Cardiovascular-Disease-dataset&id=45547&order=asc&sort=version&status=any&type=data | None
- Diabetes 130-Hospitals Dataset — Fairlearn 0.13.0 documentation | https://fairlearn.org/v0.13/user_guide/datasets/diabetes_hospital_data.html | None
- Diabetes 130-Hospitals Dataset — Fairlearn 0.15.0.dev0 documentation | https://fairlearn.org/main/user%5Fguide/datasets/diabetes%5Fhospital%5Fdata.html | None
- data / d / openml / openml-43682 · GitLab | https://gitlab.com/data/d/openml/43682 | None
- fairlearn.datasets.fetch_diabetes_hospital — Fairlearn 0.9.0 documentation | https://fairlearn.org/v0.9/api_reference/generated/fairlearn.datasets.fetch_diabetes_hospital.html | None
- data / d / openml / openml-5 · GitLab | https://gitlab.com/data/d/openml/5 | None
- SepsisExp: A Dataset of Patient Timelines with Expert Sepsis Labels - StatNLP Heidelberg | https://www.cl.uni-heidelberg.de/statnlpgroup/sepsisexp/ | 2026-02-17
- Prepare dataset - openml-python | https://openml.github.io/openml-python/v0.15.1/examples/Advanced/create_upload_tutorial/ | None
- Index - Open Machine Learning | https://docs.openml.org/reference/ | None

## mimic
- MIMIC-IV v3.1 - PhysioNet | https://physionet.org/content/mimiciv/ | 2024-10-11
- MIMIC-IV v2.2 | https://physionet.org/content/mimiciv/2.2/ | 2023-01-06
- How do I access MIMIC? | https://mimic.mit.edu/docs/faq/how-to-get-access.html | None
- MIMIC-IV v3.0 | https://physionet.org/content/mimiciv/3.0/ | 2024-07-23
- Accessing MIMIC-IV on the cloud | MIMIC | https://mimic.mit.edu/docs/gettingstarted/cloud/request.html | None
- MIMIC-IV v2.0 | https://www.physionet.org/content/mimiciv/2.0/ | 2022-06-12
- Getting Started | MIMIC | https://mimic.mit.edu/docs/gettingstarted/ | None
- MIMIC-IV v3.1 | https://physionet.org/content/mimiciv/3.1/ | 2024-10-11
- License for MIMIC-IV v0.4 - PhysioNet | https://physionet.org/content/mimiciv/view-license/0.4/ | None
- MIMIC-IV Clinical Database Demo v2.2 | https://physionet.org/content/mimic-iv-demo/2.2/ | 2023-01-31

## tools1
- DataSAIL: Data Splitting Against Information Leaking | https://github.com/kalininalab/DataSAIL | None
- DataSAIL ¶ | https://datasail.readthedocs.io/en/latest/ | None
- DataSAIL — DataSAIL 1.3.0 documentation | https://datasail.readthedocs.io/ | None
-  | https://datasail.readthedocs.io/en/latest/workflow/splits.html | None
-  | https://datasail.readthedocs.io/en/latest/index.html | None
-  | https://datasail.readthedocs.io/en/latest/interfaces/cli.html | None
- kalininalab/DataSAIL | https://github.com/kalininalab/datasail | 2023-02-06
-  | https://datasail.readthedocs.io/en/latest/workflow/workflow.html | None
- kalininalab/DataSAIL | https://github.com/KalininaLab/DataSAIL | None
- datasail | https://pypi.org/project/datasail/ | None

## market
- PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods - PMC | https://pmc.ncbi.nlm.nih.gov/articles/PMC11931409/ | 2025-03-24
- CHARMS and PROBAST+AI: an updated template for Data Extraction and Risk of Bias Assessment in systematic reviews of prediction models | https://www.medrxiv.org/content/10.64898/2026.08.26.26361189v1 | None
- APPLICATION TO ACT AS SUPERVISOR AND RESEARCH PROJECT PROPOSAL | https://www.unisr.it/attachments/ECM10--Automating-Methodological-Audits-in-Digital-Oncology--A-Neuro-Symbolic-Multi-Agent-Approach-for-Compliance-Verification-with-PROBAST-AI-and-TRIPOD-AI-Standards/e5d69854-d9b0-4a9c-b79f-33c11193f0df/5b929530-4a44-4c1b-aa3a-7e8b3000dec4.pdf | None
- AI-Enabled Clinical Trials: The 2025 Evidence Engineering Framework 3 juillet 2025 Executive Summary The COVID-19 pandemic proved that drug development timelines can be compressed | https://twingital-ventures.com/assets/docs/ai-enabled-clinical-trials-evidence-engineering.pdf | None
- PROBAST | https://www.probast.org/wp-content/uploads/2020/02/PROBAST_20190515.pdf | None
- Original Research Assessing the quality of prediction models in health care using the Prediction model Risk Of Bias ASsessment Tool (PROBAST): an evaluation of its use and practical application | https://www.sciencedirect.com/science/article/pii/S0895435625000654 | None
- PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods | https://lirias.kuleuven.be/retrieve/378c9379-69c0-4dec-bd3b-c8f2752fb1ce | None
- PROBAST+AI Assessment Guide | https://unpkg.com/medsci-skills@5.25.0/skills/check-reporting/references/checklists/PROBAST_AI.md | None
- PROBAST: A Tool to Assess the Risk of Bias and Applicability of Prediction Model Studies FREE | https://www.acpjournals.org/doi/10.7326/M18-1376 | None
- PROBAST+AI: an updated quality, risk of bias, and ... | https://pubmed.ncbi.nlm.nih.gov/ | None

## Dataset feasibility decision, 2026-09-21

The UCI Diabetes 130-US Hospitals dataset is feasible and downloaded from the official UCI static distribution (101,766 encounters, 71,518 patients, 50 columns; archive SHA-256 f82ac129da2ddd2299391ff6fbae3a6a58b3edcf59ac9d7bd480c00fe453112a). It supports patient-group leakage tests because patients can recur. It does not expose hospital/site ID despite the title, so it cannot by itself support hospital-level external validation. It can serve as one operational tabular domain, with patient-grouped and pseudo-temporal/order-based stress tests, but not the sole dataset.

CuratedBreastData / MetaGxData are promising multi-study transcriptomic sources with explicit study/cohort boundaries and clinical outcomes. Feasibility requires obtaining the Bioconductor package or source files and confirming endpoints, sample sizes, licenses, and a common feature space. This is the preferred external-validation domain because leave-one-study-out evaluation directly measures cohort transport.

MIMIC-IV is not suitable for a frictionless open-data deliverable because access requires credentialing and a data-use agreement. It may be discussed as a future evaluation but should not be an execution dependency.

## R/ExpressionSet feasibility resolved

A user-space R 4.4.3 environment with Biobase was installed through micromamba, avoiding any system mutation. The CC-BY curatedBreastData test archive decodes successfully as two real ExpressionSet cohorts:
- `study_1379_GPL1223_all`: 22,582 features x 60 samples, 153 clinical fields.
- `study_2034_GPL96_all`: 22,293 features x 286 samples, 153 clinical fields.
Both expose unique patient IDs, study/site metadata, treatment, pathologic complete response, recurrence/survival endpoints, ER/PR/HER2, grade, lymph-node, and other clinical covariates. This proves the multi-study transcriptomic domain is executable. The full 296MB CC-BY archive can expand it beyond the feasibility pair.

The two cohorts use different Affymetrix platforms; rigorous cross-study analysis therefore requires mapping probes to common gene identifiers within training-safe preprocessing. Cohort identity must never be corrected using held-out outcomes. The protocol should include both raw-platform and mapped-common-feature arms, plus a deliberately leaky pooled-harmonization diagnostic arm that is explicitly invalid for deployment.

## Protocol freeze

The Round 1 protocol froze at 21:42 IST before any endpoint model was fitted. Three real domains are fixed: recurrent-patient diabetes readmission, five-study breast pCR transcriptomics, and repeated-subject longitudinal Parkinson severity. The gate is configuration-level and leave-one-domain-out, preventing an audit threshold from being tuned on the domain it judges. Any failed required criterion makes the round negative.
