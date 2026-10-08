# Canonical unit 165: fatigue13 - stop before modeling prereg

Status: STOP_PRE_PREREG_POWER_AND_CONFOUND. No full modeling prereg, no TEST outcome, no lock or pushes. Stage A preprocessing-only protocol was frozen before the uniform survey, with a signed no-repair label-clock exclusion amendment after the initial DEV boundary inspection. These are preprocessing freezes, not a prereg claiming hidden DEV metrics.

## Source and integrity
Zenodo record 14182446 v2: https://zenodo.org/records/14182446 . Live exact API https://zenodo.org/api/records/14182446 confirms CC BY 4.0. Supplied screen metadata and live publisher checksums agree. Metadata.xlsx, protocol.xlsx, code.ipynb and self_perceived_fatigue_index.zip match publisher MD5. Independent SHA256 values are in VERIFIED_METADATA_HASHES.json.

Raw sEMG_data.zip, 3,299,567,337 bytes, complete MD5 ea7338b95543ada98b1ddc65d4b6aabc matches publisher. Initial concurrent checksum ranges triggered HTTP429; retrieval stopped, cooled down and resumed serial ordered ranges with pauses. Complete archive bytes were used for cryptographic hashing only, not sensor parsing or storage. Only DEV nested archives were extracted. Their outer CRC, local SHA256 and inner CSV CRC were checked; local SHA256 is not a publisher member checksum. No license/readme members occur in raw root directory or the seven DEV nested ZIPs. TEST nested contents were not inspected for archive-specific terms.

Dataset documentation/paper: https://www.mdpi.com/1424-8220/24/24/8081 . Hardware-trigger starts, unsynchronized stops, four active-arm channels per trial, native self-perceived 0/1/2. This is a subjective report, not clinical fatigue truth. Registry check covered the provided reconciliation CLAIMS snapshot, not a live repository. No fatigue13 exact source match there; full live registry clearance is not asserted.

## Split and Stage A
Natural-numeric sorted IDs1-13; 0-based even DEV1,3,5,7,9,11,13, odd TEST2,4,6,8,10,12. TEST never parsed/scored. The supplied label ZIP itself contains TEST bytes but no TEST nested payload was opened by this build.

Frozen suffix rule removes28 all-eight-column-zero terminal rows in21trials. Seven whole-trial exclusions/84 (8.33%): s1/t11,s3/t4,s5/t7,s5/t9 have a nonincreasing label clock; s7/t1,t5 and s9/t5 have remaining partial-column sensor timestamp resets. No shift, deduplication, interpolation, sorting or mid-trial deletion. Max per-subject exclusions2/12. Guardrails >10% overall or >half a subject pass. Retained77trials have identical four clocks, interval .00079411718sec, raw duration95.65-1488.05sec; label starts0-.021sec and longer label stops. Nonzero label starts kept unshifted and true common support used. Calling these missing first samples an export artifact is an interpretation, not a verified publisher explanation.

## Exploratory DEV gate assessment
4848 nonoverlapping5sec windows, single-class labels per window; transition windows excluded. All three classes present in every DEV subject. Windows begin5sec or later to avoid inventing a label before first label timestamp. Prime-mover mapping follows supplied publisher notebook. Welch spectral features20-450Hz, logRMS, median/mean frequency, waveform-length mean, zero-crossing rate. Local features add differences from the first valid window and prior valid window. Original signals were used as exported, with no second bandpass filtering. MVC files not used for modeling. One candidate feature policy was assessed; no outcome-guided window tuning.

Fixed exploratory LOSODEV models: standardized class-balanced LR(C1), RF150trees/depth8/minleaf10, seed165. No inner tuning; model-family selection onDEV is disclosed. Subject-mean three-class balanced accuracy:
- RawLR .348493, RawRF .326626 (chance1/3).
- LocalLR .413101, LocalRF .410864.
- Time/trial-onlyLR .461300, time/trial-onlyRF .555574.

Strongest confound-only baseline dominates the EMG methods. LocalLR minus time/trialRF = -.142472; no incremental-value claim. RawLR comparison alone has gain+.064609, but rawLR is not an adequate strongest headline comparator. No strong-skill/headroom admission is asserted; a ceiling-only raw headroom calculation is not sufficient.

## Power stop
Fixed WIN delta .03, planned six subject clusters from split metadata only. Using DEV paired subject SD .080039 for localLR-vs-rawLR, a two-sided alpha.05 noncentral-t planning calculation gives11.72% power and80% MDE .1149. Against the stronger time/trialRF comparator, DEV pairedSD .084531 yields11.02% power at .03. Both are far below80%.

These are explicit parametric planning estimates based on exploratory DEV outcome variance, not empirical TEST power, a label-free power guarantee or the final subject-bootstrap test. The seven DEV clusters make SD estimates uncertain. No label-free variance-calibrated power estimate is available from only the six planned clusters. Correlated windows were never counted as independent n. No threshold enlargement, comparator weakening, task/target substitution or TEST rescue was attempted.

## Reproducibility and limits
Code, extracted DEV feature tables, all survey rows, hashes and scores are attached in the closure ZIP. Classical CPU-only; scikit-learn1.5.2 installed in local scratch, numpy/pandas/scipy preexisting. Numerical modeling scripts are exploratory gate tools, not a locked run.py. No permutation smoke was performed because the unit stopped before admission; no TEST permutation. No clinical, novelty, causal or transfer claim. Full prereg should not be drafted on these gate results.
