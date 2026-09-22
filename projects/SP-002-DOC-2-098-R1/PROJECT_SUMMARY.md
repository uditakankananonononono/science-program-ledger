# Sculpted Project Summary - Universal Confounder Stress Test for Bio-AI, R1

## Status
Locked negative result. The audit score associated with validation optimism within domains but failed the frozen cross-domain sensitivity and full discrimination gates.

## Useful result
Across three real biomedical domains, the proposed confounder/audit score correlated with validation optimism (Spearman rho 0.770), but leave-domain sensitivity was only 0.571 and the full AUROC gate failed. The result shows that a seemingly strong pooled association does not establish a universal detector.

## What is new
The project asks whether common validation hazards can be summarized into one model-agnostic stress score that transports across biomedical prediction domains. It evaluates universality directly through leave-domain testing rather than reporting pooled correlation alone.

## Why it matters
Bio-AI benchmarks often use naive random splits that inflate performance under repeated subjects, sites, batches, prevalence shifts or group structure. A weakly transported audit score should not be sold as a universal certification.

## Working application
The bounded application is a validation-design checklist and diagnostic report that enumerates hazards and contrasts naive versus structure-aware splits. It must report domain-specific evidence and abstain from a universal pass/fail score.

## Top-lab reviewer questions
1. Which audit dimensions transport, and which are domain-specific?
2. Can a simplified score excluding the R1 dimensions that harmed transport work prospectively on untouched domains?
3. Does the score predict material optimism under site, subject and molecular-scaffold shifts?
4. How should false reassurance be penalized relative to false alarms?

## Next direction
R2 is already locked prospectively on three untouched domains: multi-site heart disease, subject-grouped human activity recognition and scaffold-split molHIV. The R1 negative remains development evidence only.

## Drive
- Report: https://drive.google.com/file/d/15hM2yZ_1Kkzpk2IHZs3zUR8TQePogGkI/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- Artifact: https://drive.google.com/file/d/19u2FEEEV-pMCArGKRw3ZKtAtt8E9jXpk/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- Sidecar: https://drive.google.com/file/d/1AbvzKyjso6-AkYJH8pxFZ9gY-cSbzeTr/view?usp=drivesdk&authuser=uditakankana%40gmail.com
