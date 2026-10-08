# F3 executable freeze candidate

Full prereg OID 6cca1dfb0fc8f2c972c02a47c13fe940e490fc31, parent
302aed55e1b47af56a8306155c9b112817a67b63. Exact candidate OID/tree and complete
source identities accompany review report; self-identities cannot be embedded
recursively. Manifest covers code, all30 constructed fixtures, schema contract,
environment, tests and unchanged floating baseline before any scoring. Its own
identity is carried in freeze-hashes.sha256/review commit.

Model keys exactly x/dt/maps/targets/limit/slew/previous. Witness exactly z/lambda,
or null meaning absent AFTER valid-model check. List arrays only; caps as prereg.
Integers accepted excluding bool, <=80 decimal chars including sign. Strings ONLY
canonical n/d with positive denominator, gcd1, no leading zeros/plus/signed zero;
0/1 accepted; 1/1 accepted alongside integer1; integer -0 is Python/JSON normalized
0, NOT separately retained. Float/decimal/NaN/Inf rejected for rational fields.
JSON parser refuses duplicate keys/nonfinite constants; 128KiB bytes and depth10,
UTF8 strict; integer tokens capped during parse. Parser ordinary bounded JSON,
not hostile-code sandbox or peak-memory certificate. Direct verifier has exact
model dimensions, scalar caps; malformed custom Python objects not authorized.

Row order and dual sign fixed by prereg. Explicit all actuator rows BEFORE all
slew rows BEFORE all terminal rows THEN -t. Separate independently written
multidimensional/non-unit-time/nonzero-x/previous test checks eight literal rows;
nonzero-previous slew-tight exact certificate exercises signs and objective gap.
Seven development tests pass. Four analytic battery fixtures constructed but full
30-row comparator and four floating calls NOT run. Existing minimax.py untouched,
SHA25623695a3e8534e60afe326b631a6ce8a4783a94f53ea6594aee405cf811713572.

After review/publication: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 compare.py results/report.json.
Identity/version/thread failure aborts without report. Result publication requires
separate exact review. A text freeze-reference is not mechanical authority; actual
publication precedes permitted execution. Validator is exact supplied-model witness
checking, not witness generation/infeasibility claim/physical truth/invention.

## Replacement after environment-grounding review HOLD

Rejected candidate0c7a8d359859e8c50d11eb9d9989cf32ea50d878 retained in history,
never published/scored. Reviewer cleared math but requested executable/module
identity grounding and direct/discovery test parity. Replacement pins resolved
Python executable bytes plus loaded Fraction/json/re/hashlib and compiled hashing/
JSON/regex cores, NumPy/SciPy entry points, optimize.linprog and HiGHS compiled
wrapper, and all currently loaded NumPy/SciPy/json/re/importlib/collections source
paths/hashes. Verify all before case comparison or baseline call. Environment
uses local absolute paths; changed environment aborts instead of silently rebinding.
This is a pinned loaded-source set, not full dynamic-loader/shared-library closure,
OS provenance, or adversarial replacement sandbox. NumPy/SciPy imports occur for
identity verification; no baseline LP runs before admission. No scores obtained.
Both direct test script and discovery now run seven development tests. No math,
fixture, baseline or 30-row scope changes. Witness validator still solver-free.

Builder corrections: intermediate5adf0bf6 failed development import because it
assumed obsolete SciPy _highs path; retained rejected history, no review/publication
or evaluation. Inspected actual loaded SciPy1.15.3 _highspy paths, corrected import.
Built-in _sre has no separate source file: bind its bytes to Python executable,
check loaded built-in path via executable. Generated runtime identity set and reran
seven direct/discovery tests. Builder-found, not reviewer-requested math repair.
