# D3 executable admission candidate

Full 32-row battery unscored. PINS binds D2 harness+compare source, D1/D2 manifests
and D3 manifest byte hashes. admit runs before importing D2 or constructing/resetting
policies. Caller manifest must recursively type-equal frozen file: bool vs int and
float vs int not equal. Plant constants/timeout match both older manifests; policy
list matches D2; exact factorial arrays derived from D1 verified before execution.
All pinned files and pins.py are committed artifacts; an attacker can modify local
code/pins themselves, so this is reproducibility refusal, not cryptographic trust or
malicious-edit security. Freeze review identifies the exact commit.

D2 runtime imported by exact path after hashes; temporary sys.modules harness binding
forces compare's `from harness import ...` to the checked module then restores prior
binding. D2 compare.score is NOT used, since it refuses alternate cases. D2 run and
pair used unchanged. D2 runtime transitive imports: fractions, multiprocessing,
pathlib,json,hashlib (standard library plus interpreter/OS). D3 stdlib import machinery
and pins.py locally. No third-party dependency/import found. Stdlib files/interpreter
and OS not individually pinned or hermetic; environment captured in result artifact.
Trusted policy/child/recv/serialization/OS wall limitations unchanged.

Four pre-score development methods pass: 32/16 cardinality construction without
runtime; typed constants/policies/boolean-array refusal before load_runtime; each of
five pinned artifacts tampered in temp copy refused before import; one-step partial
runtime fixture. Full factorial NOT run, no outcomes inspected/tuned. D1/D2 files
unchanged. Paired summaries retain counts/None/noncomparable through unchanged D2
pair. Closed-loop pairing, not same realized observed positions, four estimator/action
variants not four controller classes. No physiological parameters/CI/novelty gate.
Run compare.py only after exact executable freeze independent review and publication.
