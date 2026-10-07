# 92 mitbih-prototype-balanced-beat-classifier

Algo50 batch 2 (builder lane, agent-run, not owner-verified). Result: NEGATIVE - DS2 macro-F1(S,V,F) 0.1462 vs kNN 0.2232 (diff -0.0770, CI [-0.1436,-0.0274]); shared feature pipeline weak (baseline V F1 0.58).
Protocol: PROTOCOL.md (locked before outcome evaluation; amendments appended inside). Code: code/run.py (data fetched from sources and sha256 in PROTOCOL.md; raw data not committed).

v2 (steered re-prereg, DS2 SECOND LOOK): NEGATIVE again, macro-F1 0.1339 vs kNN 0.2133 (diff -0.0794, CI [-0.1584,-0.0240]); lead choice + 0.5-40 Hz bandpass did not help.
