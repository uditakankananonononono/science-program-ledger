# Gate evaluation

- G1: **FAIL / not evaluable in full.** All three source/unit manifests pass, but no protocol-compliant frozen configuration matrix exists in the supplied artifact, so 36 configurations and 8+/8- composition were not produced.
- G2: **NOT EVALUABLE; universal scoring closed.**
- G3: **NOT EVALUABLE; universal scoring closed.**
- G4: **NOT EVALUABLE.**
- G5: **PARTIAL.** The review-support validator fails closed on missing dimensions, corrupt protocol hash, bad ranges, and missing provenance. Modeling controls could not be run without frozen implementation details.
- G6: **PARTIAL.** Environment and source hashes are pinned; prediction reproducibility is not evaluable because no protocol-compliant predictions were generated.
- G7: **PARTIAL PASS.** The supplied review-support validator has deterministic output, corrupt/missing input rejection, provenance requirement, and explicit non-certification boundary. Runtime/peak-memory ledger for full modeling is absent.

Overall R2 verdict: **NEGATIVE / STOPPED BEFORE ENDPOINT MODELING due to protocol underspecification.** Under the all-required rule, R2 is negative. Since G2/G3 are not passed, universal scoring is closed; only the source audit and non-scoring evidence-dossier/checklist are supportable.
