# U187 closure - Figshare 5202739 driver fatigue EEG: DROP at power gate (label-free)
No model, split, prereg, run.py or outcome compute. Main approved DROP 12:49 IST Oct 8 2026; no DEV-only screen.

## License and integrity
CC BY 4.0 (Figshare API https://api.figshare.com/v2/articles/5202739, DOI 10.6084/m9.figshare.5202739.v1, 2017-07-13). 12/12 ZIPs fetched serially from ndownloader.figshare.com; MD5 equals API computed_md5 for all (md5ref.txt); unzip -t CRC clean 12/12; local sha256 in u187_zip_sha256.txt. 559 MB.

## Layout (all 24 Neuroscan .cnt, 2 per subject: Normal state, Fatigue state)
40 channels, 1000 Hz, identical list in all 24 headers: HEOL HEOR FP1 FP2 VEOU VEOL F7 F3 FZ F4 F8 FT7 FC3 FCZ FC4 FT8 T3 C3 CZ C4 T4 TP7 CP3 CPZ CP4 TP8 A1 T5 P3 PZ P4 T6 A2 O1 OZ O2 FT9 FT10 PO1 PO2.
Header nsamples field is garbage; duration from event-table offset (offset-3900)/160 bytes at int32 x 40 ch. Seconds per file (Normal, Fatigue): s1 300.4/300.5; s2 300.0/300.7; s3 301.6/301.6; s4 300.8/301.4; s5 300.8/300.4; s6 300.8/301.2; s7 300.9/300.6; s8 300.8/300.6; s9 300.8/301.2; s10 300.2/300.1; s11 300.5/300.9; s12 300.2/301.4. Mean 300.65 / 300.88; 300-301 one-second epochs per file.

## Source paper and published baseline
Min, Wang, Hu, PLoS ONE 12(12):e0188756 (PMC5722287), https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0188756. Reports 98.3% accuracy (sens 98.3, spec 98.2) with "leave-one-out CV", but the text says 1 s epochs were randomly and equally split into training and testing sets: epoch-level split within the same subject and block, so the figure is leaky and is not a subject-level baseline. Fetch text: paper_min2017_fetch.txt.

## Label and time confound
Per subject exactly one Normal block (last 5 min of EEG after 20 min of driving) and one Fatigue block (last 5 min after 40-100 min of continuous driving, stopped when self-report scales said fatigued). Label = block = time in session, 100% collinear, separate files. Elapsed time to the fatigue block per subject is not in the dataset. State cannot be separated from time-on-task, drift, impedance, posture or reference changes. 1 s epochs inside a block are not independent units.

## Power math (label-free)
Units = 12 subjects (one paired contrast each); leave-subject-out TEST = 6 subjects; paired cluster bootstrap over 6 clusters. MDE approx 1.43 x sigma_d (80% power, t df 5, alpha .05 two-sided; sigma_d = between-subject SD of per-subject paired AUC gain): sigma_d .02 -> .029; .03 -> .043; .05 -> .071; .10 -> .143. WIN bar 0.03 with CI lower > 0 is not decidable at plausible sigma_d. Ceiling concern (published 98%, leaky) not tested; no outcome compute.

## Verdict
DROP at power gate (not decidable at 12 subjects, label fully confounded with session time). Claim scope if cited: driving-simulator EEG block classification, no medical or safety claim.
