# Exact primal witness and dual-gap check

Established weak-duality equality certificate, not invention. Caller supplies an
exact rational nonnegative normalized ternary joint table. Every target/offtarget
marginal must exactly match original rational model; event probability recomputed
rationally. Existing dual checker independently verifies/repairs all inequalities.
A witness probability exactly equal to lower bound certifies the minimum; equality
to upper certifies maximum. One witness need not certify both extrema. Positive
gaps mean no optimum claim. No rational reconstruction from solver mass implemented.

32 dev methods pass (28+4): exact minimum/maximum two-agent witnesses, nonzero gaps
explicitly not optimal, invalid exact marginals/negative or unnormalized mass refused.
Duplicate states may contribute masses normally; caller table size still unguarded
although model N<=5. Fraction/input-bit/CPU growth unbounded, outputs not JSON-ready.
Exact certificates concern supplied model only, not physical marginals/dependence,
coordination/energy/info/cost/biological cap. No score or scientific/novelty gate.
Previous production modules unchanged. Independent review pending.
