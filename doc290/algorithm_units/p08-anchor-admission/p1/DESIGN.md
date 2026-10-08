# P1 stationary measured flow-profile diagnostic design/admission

Established amplitude-only OLS model check, not invention or validated physics.
Five admitted Fig3 zero-field PIV profile tables from Zenodo13220167, associated with
five separate subsequent-voltage trajectory experiments. These measurements precede
field application: filename1V..5V does NOT mean PIV measured with that voltage applied.
No dynamic trajectory fit, timing inference,S3uncertainty column or physiological transfer.
No residuals computed before executable freeze/review/publication.

## Locked model and comparison

Source channel width100um; set halfwidthw=50um. At every reported position y_um,
basis f(y)=1-(y/50)^2. Predicted speed=A*f, zero at mathematical walls y=±50.
Fit one amplitude per profile A=sum(f*u)/sum(f*f), established unweighted zero-
intercept least squares. No fitted center,width,offset,wall slip or viscosity. Amplitude
unconstrained (do not clip negative fitted values silently); descriptive estimate only.
All spatial positions retained. Source4V/5V grids/coverage differences are not corrected
or pooled; per-experiment fits/results separate. No model selection from outcomes.

Comparator arithmetic: independent numpy.linalg.lstsq on one-column f design, same
finite rows, rank checked. Agreement a numerical implementation check, not evidence
for physics. Lock numerical comparison atol=1e-10,rtol=1e-12 for amplitude/predictions;
this is NOT measurement acceptance tolerance. Fail computational disagreement rather
than select preferred answer. Input exact byte hashes,headers/shapes and package/env
pinned. Minimum2finite rows and nonzero basis denominator needed; fail explicitly if
unsupported, never drop profile. Source profiles have19,19,19,19,20rows, three NaNs
in speed. Mask only nonfinite speed for arithmetic, preserve original missing rows with
prediction at their y and residual=None. Finite position required; infinite speed rejected.
No NaN interpolation/imputation or use as zero. Report total/finite/missing counts.

## Raw outputs and leave-one-location checks

Each finite-row signed residual is observed-minus-predicted speed, unitsum/s. Retain
y,f,observed,predicted,residual,absolute and squared residual, row ID. Missing rows keep
y,f,prediction, observed NaN represented safely as None in JSON, residual=None; CSV
may retain nan. Summary descriptive SSE,RMSE,MAE,max absolute,mean signed residual,
and amplitude, all per profile. These are sample residuals, not calibrated errors,
uncertainty bands,CIs,p-values,model-validation pass or transfer-cost ranking.

Leave-one-location-out: for EACH finite row refit amplitude on all other finite rows,
then predict withheld speed. Retain all refit amplitudes/predictions/errors and counts.
Report descriptive MAE/RMSE/max absolute; no independent held-out validation claim:
rows correlated in one PIV spatial profile, known exposed data, no separate experiment.
No pooling folds/profiles as independent trials or selecting fit after outcomes.
No inferred sensor precision/measurement covariance.5V has20finite rows,others18/18/18/19.

## Visual/report contract

Figure1: five separate observed+fitted speed-vs-y panels with finite/missing counts;
missing rows marked at y in a separate side marker, not fabricated speed. Figure2:
signed in-sample and leave-one-location residual-vs-y per profile, common residual
axis range derived from all retained finite errors for comparability, explicit units.
No smoothing/interpolation. Full tables/code/protocol/env/hashes retained. Actual
pixels inspected before completion, any post-freeze edits disclosed/refrozen as needed.
No source-styled pixel reproduction claim. Attribution Buness,Rana,Maass,Dey,
https://zenodo.org/records/13220167 CC-BY4.0.

## Meaning of outcomes

Nonzero residual is a measured source-table/model mismatch, not automatically omitted
wall/rheology physics: finite spatial resolution,approximately15%flow variation,
approximate geometry/centering,measurement noise and unmodeled effects unseparated.
Near-zero residual does not prove dynamics/transfer. No predetermined sign or pattern
promised, no tolerance/gain/width adjusted to force a bottleneck. All P08-08 science
gates open. After reviewed results, determine whether any specific residual/bottleneck
supports further work, rather than claiming invention from OLS or an arbitrary fit.
