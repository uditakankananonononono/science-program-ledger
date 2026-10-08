# D1 executable admission candidate

Implements published design 8f4e622f01cb79e99bb4cb00f3ada4e3918bbe3e with the
following pinned additions before scoring. Full manifest NOT executed yet.

Action int/Fraction only, bool/float (finite or nonfinite) and all other types rejected.
Bound violation invalid_action, no silent clip. Unsupported invalid values retained
as UnsupportedAction identifier, not serialized raw arbitrary objects; action field
None. Fraction/int bound-violating value retained. Exception stores class identifier
only, never raw message. Failed action/exception retains attempted observation and
pre-step state, no transition/state_after/effort contribution. Reset failure has zero
records. Final error is absolute target error at last completed state; effort sum of
dt*abs(action) over completed transitions including immobilized transitions. Maximum
overshoot is max(0,lower-x,x-upper) over visited states including initial. Early/no-step
failures get their literal metrics, not None/zero-filled target error.

Policy reset plus each action has a one-second wall-clock budget via Linux fork child
and parent Pipe polling. Nonreturning child killed, joined, typed controller_exception
with PolicyTimeout. Child process exit similarly PolicyProcessExit. Policy receives
only observation,target,dt,bound per call; mutable policy state stays child-local.
Trusted policy code only: fork isolation is NOT a security sandbox, inherited process
memory may contain harness inputs, and malicious policies could access it. Causal
contract is restricted call interface plus honest implementations and adversarial
observed-prefix tests, not information-theoretic adversary protection. Parent process
startup/serialization/OS scheduling are not covered by a total runtime guarantee.

Eight dev tests pass: literal state/effort/reset; dropout hold; observed prefix/hidden
future action equality for both baselines; bool/NaN/bound invalid and exception early
metrics; never-return policy timeout; inclusive boundary/terminal and boundary priority;
immobilization effort; malformed protocol. These small fixtures are not the 10-row
manifest battery. No physiological source values admitted, tuning, scored results,
CI/atlas controller-count/science gate or invention claim. Dimensionless sign and
proportional only. Run `python3 compare.py` only after independent admission/publish.
