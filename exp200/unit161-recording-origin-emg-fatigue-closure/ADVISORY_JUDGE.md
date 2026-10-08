# Unit161 advisory outside-model judge

Source reported by parent: https://chatgpt.com/c/6ac77555-1f9c-83ee-95e8-470b4747e3a9
Received October8,2026. Advisory only; no rerun, band change or third candidate. Original closure ZIP SHA2568ad2ec0405841145bdc07c53fb865953d582558a84d29926631217bf87039b4e remains unchanged.

## Verbatim verdict

Adversarial methods review

Overall: methodology = mostly disciplined DEV closure; claim calibration = mostly good, with one important qualification around the zero-origin assumption. I would accept the DROP/NULL decision as a DEV-candidate closure, but I would not let the wording drift into a claim about "early-task" or "before-fatigue" prediction.

1. Methodology

The strongest part is the separation of DEV screening from TEST. The frozen hashes, explicit exclusion rules, subject-clustered nested GroupKFold, subject weighting, sealed even-subject TEST set, and no post-result retuning make the procedural stop reasonably defensible.

The observed result itself is weakly negative: -0.128 s gain, CI -5.91 to +5.92 s. That does not establish inferiority; it establishes that this candidate failed the prespecified >=5-s improvement criterion. Calling it "did not improve headroom" is therefore fairer than saying the representation is useless.

The permutation result is also appropriately restrained. Calling +3.16 s a noise-induced overfit possibility is justified; calling it evidence that labels are secure would not be. The closure explicitly avoids that mistake.

One methodological limitation is more substantive than a reporting nit: the CI is explicitly exploratory because the cluster bootstrap does not model overlapping-training covariance. Therefore the CI should not be used rhetorically as if it were a confirmatory uncertainty interval. The closure acknowledges this.

2. Zero-origin alignment: the critical qualification

The closure does an unusually good job not silently converting recording time into task time. It explicitly says the first 10 seconds are from the provided recording origin, whose relationship to task onset is unverified, and lists preparation, endpoint discrepancy, and lack of synchronized RPE.

That makes the current claim bounded.

However, "first10seconds" still has a semantic hazard: readers may instinctively interpret it as the first 10 seconds of the endurance task. The registry should continue to use wording such as "recording-origin prefix" and never shorthand it to "early-task," "pre-fatigue," or equivalent. This is not merely cosmetic because the biological interpretation changes materially if preparation occupies part of the prefix.

I would not call the zero-origin assumption adequately validated. I would call it explicitly unvalidated and appropriately quarantined. That distinction matters.

3. Power reporting: no obvious inflation

The 0.96 significance power versus ~0.50 full-WIN probability is actually a strength of the reporting. The closure correctly distinguishes probability of detecting a specified 5-s effect under the assumed SD/model versus probability of both achieving significance and observing the required >=5-s point-estimate gain. The 0.50 ceiling at an effect exactly equal to the threshold is mathematically unsurprising and prevents the misleading "96% power means 96% chance of winning" interpretation.

But the 0.96 figure is conditional, not empirical power. It depends on the assumed normal paired-error model and assumed SD=5 s. The closure does state the assumptions and gives the sensitivity range, so I would not call this inflated. Still, the headline should never say simply "96% powered."

The 80%-significance MDE of 9.67 s is useful, but it should not be interpreted as an empirical minimum detectable improvement for this entire modeling pipeline.

Verdict

No serious flaw that overturns the DEV stop. The principal risk is interpretive slippage from recording-origin prefix -> task-onset prefix. Keep that boundary prominent.

The strongest defensible conclusion is: This frozen candidate failed the prespecified DEV improvement gate; the result does not establish that prefix information lacks predictive value, that larger effects are impossible, or that the recording-origin prefix corresponds to a defined physiological stage of the task.

That is appropriately calibrated.

## Parent's additional provenance note (verbatim)

Note for the record: one sentence in the judge's first page response read "Six of 16 subjects improve in the real run, ten worsen." No edits or follow-up prompts were sent.

## Recorded response

Accepted as advisory interpretation limits. Keep "recording-origin prefix" and explicitly unvalidated onset boundary in registry and reporting; exploratory OOF intervals remain nonconfirmatory. Conditional normal-model power is not empirical full-pipeline power. No claim that all prefix information is useless, no inferiority claim from the endurance NULL, no larger-effect impossibility claim. No scientific outcome or frozen files changed.
