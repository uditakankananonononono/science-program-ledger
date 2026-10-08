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
