# Unit 156: EMG-EPN612 split-integrity closure packet

**Disposition:** DROP at screen - dataset flaw: the advertised independent-person train/test split is contradicted by verified cross-directory waveform duplication and a matching full profile/date record. This finding is limited to split integrity; it is not a model result. No preregistration, headroom evaluation, fitting, score computation, or TEST outcome analysis was run. No re-split or salvage analysis was attempted.

## Decision evidence

The live Zenodo v2.1 record describes the archive as 612 people divided into training and testing groups of 306 people each. Its lab-page link also describes 612 users. The complete published archive was downloaded by byte ranges, each range length checked, assembled, and verified against Zenodo's published MD5. ZIP CRC validation passed.

The archive contains 306 JSON records in `trainingJSON` and 306 in `testingJSON`; each side reuses the folder-local labels `user1` through `user306`. Folder labels alone cannot identify distinct people across the two folders.

A complete 306 x 306 comparison was performed on each training/testing `userInfo` record pair:

- Exact equality of all nine recorded profile fields (age, gender, occupation, ethnic group, handedness, arm-damage field, elbow-to-Myo distance, elbow-to-ulna distance, and arm perimeter): 17 cross-folder pairs, across 16 distinct folders per side. These coarse profile matches by themselves are not proof of shared identity.
- Exact recording-date equality: one cross-folder pair.
- Exact equality of both the nine-field profile and date: one pair only, training `user172` vs testing `user290`.
- That pair has the same profile and date: 29-Oct-2019; age 24; woman; student; Latin; right-handed; `ArmDamage=False`; elbow-to-Myo 9 cm; elbow-to-ulna 24 cm; arm perimeter 28 cm.

For that single exact profile/date candidate, direct elementwise comparison of the eight raw EMG channels (not model fitting) found:

- `trainingSamples`: 80 exact, nonzero waveform matches among the 150 records. All 80 matched records have matching gesture names on both sides: 13 noGesture, 15 waveOut, 10 pinch, 17 open, 10 fist, 15 waveIn. Matches use permuted `idx_*` positions.
- `testingSamples`: 80 exact, nonzero waveform matches among the 150 records. The test-side records omit `gestureName` in this section; the training-side corresponding records carry the labels. Do not infer labels for the test side from that omission.
- The matches are exact 8-channel integer arrays after JSON decoding, with equal array dimensions; per-array SHA-256 values are recorded in `exact_waveform_pairs.csv`. At least one verified example is training `idx_1` vs testing `idx_14`, noGesture, 994 samples x 8 channels, hash `5b36807e5ddf863f902b0a18eebef1be102d6ab995f923d5ef5eaffd2157fe4c`. In the other section, training `idx_1` vs testing `idx_6`, 994 x 8, hash `3da4f67ca5a167c83c30c18693194d7e57adbca7ec62cf7414ae90fc5935e509`.

The exact raw waveform duplication plus the unique cross-folder full profile/date match establishes a cross-split data/identity conflict. This contradicts treating the two archive folders as a verified unseen-person split. The data do not expose a separate global subject identifier in those folder names; the evidence supports a strong identity match but does not justify claiming every folder's real-world identity has been reconciled.

## Full comparison artifact

`cross_group_pairwise_306x306.csv` contains all 93,636 train/test pairs, with one row per training folder and a column per test folder. Cell codes:

- `B`: same exact date and all nine profile fields
- `D`: same exact date only
- `M`: same exact nine-field profile only
- blank: neither full comparison signature matches

`metadata_candidate_pairs.csv` lists each of the 17 profile-match pairs and the unique date-match pair, with booleans for each criterion. The two tables are complete for those fields; a matching signature remains a screening link, not a standalone identity assertion.

## Publisher discrepancy preserved verbatim in substance

- Zenodo v2.1 says the dataset contains signals of 612 people and “is divided into two groups of 306 people each,” one for training/design and the other for testing. It lists CC BY 4.0 and the 5,483,385,161-byte ZIP, published MD5 `98bd3c315efab607cc54b2ed2f8f3ada`.
- The linked EPN lab page says: “Dataset (in format JSON) with EMG signals of 5 gestures of 612 users using MYO Armband.”
- The verified archive has 306 local folders on each side, reuses `user1`–`user306` independently in both, and includes the cross-folder profile/date and raw-waveform duplicates documented above. These statements conflict with a clean independent-person holdout claim. The original publisher wording is not silently repaired here.
- The 2024 paper reports 93.0% six-gesture accuracy on 306 described as unseen testing users. This is a published claim, not a new result here, and does not resolve or override the contradictions observed in the MD5-verified archive.

## Integrity and provenance

- Source/version: Zenodo record 4421500, EMG-EPN-612 Dataset v2.1.
- Record/source URL: https://zenodo.org/records/4421500
- EPN lab page: https://laboratorio-ia.epn.edu.ec/en/resources/dataset/2020_emg_dataset_612
- 2024 paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11459555/
- Downloaded archive byte length: 5,483,385,161.
- Published/observed MD5: `98bd3c315efab607cc54b2ed2f8f3ada` (match).
- Independently computed SHA-256: `4ee8db037385e7bee1e6ac6f9e9eea4f0869e25f7825f5eb7e5be0dff4f93c21`.
- ZIP test: `unzip -t` completed with “No errors detected in compressed data.” The archive lists 1,839 entries; sum of uncompressed lengths: 11,677,190,838 bytes.
- Metadata comparisons use only the `userInfo` fields named above. Signal comparison uses the 8-channel arrays under each record's `emg` object; SHA-256 is computed over channels ch1..ch8 column-stacked, cast to signed 16-bit integers in C row-major order. Hash matches were additionally checked with elementwise array equality. All matched arrays are nonzero.
- Pairwise metadata files and exact waveform-pair file are attached in this packet archive; no waveform payload or subject photos are included.

## Boundaries

No training/test scores were computed. No test labels or test outcomes were used for tuning, model selection, or a benchmark. The 2024 paper's 93% number remains external context only. Because the hard independent-person split gate failed, there is no DEV headroom result, preregistration lock, run.py, TEST computation, or advisory judge round. Registry changes and the one-round closure judge remain with the parent routing the unit.
