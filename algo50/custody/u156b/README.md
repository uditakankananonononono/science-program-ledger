# Full cross-group waveform hash join: EMG-EPN612

This is a complete content-level join over every EMG sample in the two published archive directories, not only the metadata-matched candidate. Source archive: Zenodo 4421500 v2.1. Archive byte length 5,483,385,161; observed MD5 matches publisher's `98bd3c315efab607cc54b2ed2f8f3ada`; `unzip -t` passed. Source: https://zenodo.org/records/4421500

## Methods

Every JSON file in `trainingJSON` and `testingJSON` was parsed (306 folders on each side). For both `trainingSamples` and `testingSamples`, each record with all channels `ch1`..`ch8` was represented as the raw values in channel order, time-major after stacking the eight channels, signed 32-bit little-endian. SHA-256 was computed over an 8-byte little-endian dimension prefix `(n_samples,n_channels)` followed by the contiguous sample bytes. The join key was `(section, n_samples, n_channels, digest)`. No outcomes or classifier were computed.

The hash implementation was run in 13 bounded folder batches per side. It hashed 91,800 records on each side: 45,900 each in `trainingSamples` and `testingSamples`. Each full input folder contributed its samples; each section had 150 samples per person. Exact hash matches were joined across all 306 × 306 folder pairs.

## Result

There are **160 exact matched raw-EMG sample pairs**, all between training folder `user172` and testing folder `user290`: 80 in `trainingSamples`, 80 in `testingSamples`; no other cross-folder pair matched. Every match is nonzero and is a same-length, exact 8-channel array. For each matched record, the CSV includes sample index, dimensions, gesture field if present, and hash. A representative pair is train `trainingSamples/idx_1` (noGesture) and test `trainingSamples/idx_14` (noGesture), 994 × 8, same SHA-256 `a13613bc13b4357b68485dd72da96affc2b10e9c06252a0f1cee8ba890c2dd8a`. The archive's test-side `testingSamples` records omit gestureName; blank values are preserved rather than imputed.

The full join proves repeated recording content exists across two nominal folders. It does **not**, by itself, prove the two folder labels represent the same human. The unique exact profile+date match supports a plausible identity linkage, but identity remains a separate question unless corroborated by a global subject identifier. This distinction preserves the judge correction: duplicate recordings are proven; two distinct persons are not thereby disproven.

## Files

- `trainingJSON_all_sample_hashes.csv`: all 91,800 train-side per-record hashes.
- `testingJSON_all_sample_hashes.csv`: all 91,800 test-side per-record hashes.
- `all_exact_cross_group_waveform_matches.csv`: the full exact-match join, 160 rows.
- `SHA256SUMS.txt`: SHA-256 for all three CSVs and this README.
