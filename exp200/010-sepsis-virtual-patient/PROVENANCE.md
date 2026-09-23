# DOC-1-010 PROVENANCE
Dataset: PhysioNet/CinC Challenge 2019 "Early Prediction of Sepsis from Clinical Data" v1.0.0.
Project page: https://physionet.org/content/challenge-2019/1.0.0/
Reference: Reyna MA et al., "Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019", Critical Care Medicine 2020;48(2):210-217.
Download route: AWS Open Data public mirror, HTTPS bucket physionet-open.s3.amazonaws.com, prefix challenge-2019/1.0.0/training/ (no auth). Downloaded 2026-09-24 ~04:45 IST.
- training_setA/: 20,336 .psv files (published count 20,336 - match), 131,388,704 bytes total. Per-file sizes verified against S3 listing; 300-file random MD5 spot-check vs S3 ETags: 0 mismatches. Manifest (key, ETag-MD5, size): data/manifest_A.tsv. Aggregate manifest SHA-256 (sorted name+MD5 pairs): 13fd57e35636b99f85662208d49080519350c39fefacbab4444b464daef69763
- training_setB/: 20,000 .psv files (published count 20,000 - match), 123,668,780 bytes total. Same verification: 0 size mismatches, 0/300 MD5 mismatches. Manifest: data/manifest_B.tsv. Aggregate manifest SHA-256: fbe8d5f997884440ab9ff86bf81d42c19e7727e97625155123be467f9911bc39
Format: one .psv per patient, hourly rows, 40 clinical columns + SepsisLabel; organizers shift labels 6h before clinical onset. Sets A and B come from different hospital systems (cross-hospital split by design).
License: PhysioNet open-access (ODbL-style per project LICENSE.txt).
Upstream publishes no per-file checksums; integrity anchored to S3 ETags (MD5) recorded at download time.
