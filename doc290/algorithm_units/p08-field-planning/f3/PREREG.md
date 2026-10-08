# F3 exact finite-scenario minimax witness validator preregistration

Parent: 302aed55e1b47af56a8306155c9b112817a67b63. Method gap recorded in
../MINIMAX.md: floating primal objective consistency is not a dual optimality
certificate. Artifact is an independent exact rational witness verifier, not a
new LP invention, automatic witness generator or measured-data benchmark.
Existing minimax.py remains unchanged and its identity is pinned at freeze.

## Exact statement and independent reconstruction

Input supplied rational initial vector x, positive times dt, finite constant
scenario maps B, scenario targets y, positive componentwise actuator limits,
nonnegative slew rates, previous actuator within limits. Nonempty dimensions,
all scenarios share dimensions. Scalars are integers or canonical rational
strings n/d (positive denominator, reduced, no leading zeros except zero);
booleans/floats including NaN/Inf/decimal strings rejected. Witness values follow
same grammar. Input domains have no inferred physical units or measured precision.

Flatten controls step-major as u[k,j]; append t. Free variable vector z. Minimize
c^T z=t subject to A z <= b, all reconstructed from supplied model, never accepted
as arbitrary caller matrices. Order: actuator upper/lower per k,j; slew upper/lower
per k,j (previous offset only at k=0); terminal upper/lower per scenario, coordinate;
finally -t<=0. Terminal coefficients sum dt[k]*B[s,d,j]; upper residual inequality
terminal-x-target <= t, lower its negative <= t. No corridor/intermediate safety.

Accept ONLY if rational primal z has correct dimensions, A z<=b, every supplied
lambda>=0, c+A^T lambda=0, and c^T z=-b^T lambda EXACTLY. These establish matching
primal feasible upper/dual lower bounds for this supplied finite rational LP.
Complementarity residuals may be reported but are not a substitute for equality.
Zero floating tolerance, no approximate conversion, solver-status proof or repair.
No infeasibility certificate offered. Witness absent: UNAVAILABLE, not infeasible;
malformed model/witness or failed proof: INVALID with reason, never proof success.
No general promise that a floating solution admits an exact supplied witness.

## Fixed evaluation scope, exposed analytic fixtures

Four named dimensionless models, all x=0, previous=0, dt positive unit steps.
1. two-gain: one step, maps 1 and 2, targets 1 each, limit=1, slew=2;
   witness u=2/3,t=1/3. Terminal lower gain1 lambda=2/3 and terminal upper
   gain2 lambda=1/3, all other multipliers zero.
2. capped: one step, map1,target1, limit=1/2,slew=2;
   u=1/2,t=1/2; upper actuator lambda1, terminal lower lambda1.
3. zero: one step,map1,target0,limit1,slew2;u0,t0; -t lambda1 only.
4. two-step-capped: two steps,map1,target2,limit1/2,slew2;
   u=(1/2,1/2),t1; both upper actuator lambda1, terminal lower lambda1.

These exact witnesses are disclosed construction checks, not blind validation.
Each model evaluated with its valid certificate and five fixed mutations:
primal t increased by 1; first control increased by 2; first multiplier set -1;
all multipliers zero; dual vector final entry removed. Plus six standalone
malformed-input controls: float dt, boolean limit, noncanonical 2/4 witness,
zero denominator witness, missing witness, wrong target dimension. 30 rows total.
Missing witness expects UNAVAILABLE, all other corruptions INVALID, valid four
expect VERIFIED. All 30 retained with verdict/reason, expected/actual equality,
model/witness identities. No fixture selection after results or refusal counting
as algorithm superiority. Separate development tests cover independent assembly,
exact dual algebra, grammar/shape boundaries and intentional harness disagreement.

Comparator is expected symbolic verdict versus actual verifier output, not a
performance ranking. For four valid fixtures, unchanged floating minimax baseline
also run once; retain controls/objective/exception and separately report difference
from exact optimum, never use it to issue a certificate. Float binary rational
conversion only for descriptive objective difference, not witness manufacture.
No timing win, CI, heldout, hardware/physiology or novelty/science gate claim.

## Route and bounds

Prereg review/publication BEFORE implementation. Executable+protocol+fixtures+
environment+source hashes review/publication BEFORE 30-row evaluation or baseline
run. Development tests are separate, not the full battery. Strict JSON duplicate
keys/nonfinite values/type handling; every pinned identity checked before harness
run, tamper aborts without partial score. Pure Python Fraction verifier, no solver
import; baseline separately uses existing SciPy. Fixed limits: at most 8 steps,
4 actuators,4 coordinates,8 scenarios; scalar token <=80 chars; no arbitrary
iterables or expression evaluation. Caps are domain limits, not peak memory proof.
No source acquisition, code downloads, training or GPU; single BLAS thread.
Results exact independent review before publication. All exceptions/losses and
post-freeze changes disclosed; no tolerance or fixture rescue. Scope supplied-model
algebra only, not actual physical truth or claimed invention.
