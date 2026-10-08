# Supplied interval marginal robust allocation

Development extension of exact one/two-agent target-only Frechet baseline.
Inputs are exact rational marginal ranges [lo,hi], positive payloads and target
threshold. Ranges are a rectangle supplied by caller, not fitted confidence bands,
posterior credible intervals, physiological uncertainty or calibrated safety limits.
No off-target/collateral model; energy/information/cost equality still unmodeled.

Threshold delivery is coordinatewise increasing in target bits. Raising a marginal
can be coupled by changing some failed bits to target bits without reducing success;
lowering a marginal can be coupled by thinning target bits. Therefore infimum over
all joint distributions at allowed marginals occurs at the vector of lower endpoints,
and supremum at upper endpoints. Fixed-marginal extrema come from the established
exact Frechet method. All marginals/dependence combinations are allowed by the
rectangle; correlated parameter constraints would be a different uncertainty set.

Finite-menu selection retains all results/ties and ranks the worst lower guarantee.
Same total payload required; allocation-specific probability ranges must be supplied,
not assumed invariant or empirically validated. No continuous design optimizer,
comparison freeze, scored validation, invention or swarm-superiority result.

Six development methods pass including point-range reduction, iterable payload
normalization, full [0,1] uncertainty, invalid ranges and finite-menu ranking.
675 denominator-4 rectangle/weight/threshold cases compare against grid enumeration
of all admissible point marginals and their exact extrema (dependent implementation
uses the existing interval primitive, so not an independent mathematical proof).
No held-out data. Wide uncertainty [0,1]^2 returns [0,1], intentionally uninformative.
Prior to commit, inspection found iterable payload consumption across endpoint calls;
normalized once and added regression. No frozen/scored artifact changed.

Output exact Fractions, not JSON-ready. Scope does not expand the unadmitted-source
status in EXPERIMENT-SCREEN.md. This decision baseline enables honest treatment of
supplied calibration uncertainty but does not manufacture calibration evidence.
