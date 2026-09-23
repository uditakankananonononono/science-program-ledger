# Flagship Quality Standard

The user requires every project to carry the depth of a 12-month research effort. Project count and speed are subordinate to rigor.

A project may count toward the final 100 only when it includes:

1. Exhaustive, current literature grounding with a source ledger and explicit novelty claim.
2. A locked protocol written before outcome inspection: hypotheses, endpoints, comparators, success gate, and failure policy.
3. Multiple independent real datasets when the field permits, with a true external or cross-dataset validation stage.
4. Strong baselines, ablations, negative controls, leakage audits, confounder checks, and robustness/sensitivity analyses.
5. Statistical uncertainty that respects the sampling unit and multiple testing.
6. Mechanistic or biological interpretation that remains separate from prediction performance.
7. Honest preservation of negative, contradictory, and non-transporting results.
8. Fully reproducible code, complete data provenance, processed result datasets, publication-grade figures, a full technical report, and a research paper.
9. Clear limits, ethics, and a decisive follow-up plan.
10. A final internal quality review confirming that the contribution is genuinely flagship-level rather than a shallow benchmark exercise.

Passing a numerical gate alone does not make a project one of the final 100. SP-001 remains a pilot pending independent validation and deeper analysis.

## No-thin-work rule

Nothing thin ships. No stubs, placeholders, toy analyses, empty sections, synthetic stand-ins where real data exist, or inflated page counts. Reports must earn their length through substantive methods, evidence, diagnostics, tables, figures, limitations, and reproducible artifacts. Advanced methods are used only when scientifically justified and must be compared against simpler baselines. Incomplete projects remain internal work-in-progress and do not enter a delivery batch as finished research.

## Commercial and professional-use standard

Every counted project must mature beyond a demonstration into a credible professional research product. In addition to scientific validity, it must include:

- a defined real user, decision, or workflow and the concrete value the result creates;
- a deployable system or reusable analysis package where the science supports one, with tested interfaces rather than mocked screens;
- comparison with current operational and scientific alternatives, including cost, accuracy, latency, data burden, and failure modes where relevant;
- validation under realistic distribution shift, missingness, class imbalance, and operational constraints;
- documented data rights, privacy, security, safety, regulatory, and misuse considerations;
- an adoption path: integration requirements, monitoring, human oversight, rollback criteria, and post-deployment evaluation;
- a credible commercialization or translation analysis covering customer/user segment, value proposition, competitive landscape, deployment economics, and evidence still needed;
- professional publication and product documentation suitable for expert review.

Commercial framing may never inflate the scientific claim. A scientifically negative project remains negative even if its product concept sounds attractive. A method must not be labeled production-ready until realistic testing supports that claim.

## Capacity and parallelism

The 12-month-equivalent standard applies independently to every project. Parallel execution may increase throughput, but no project may borrow evidence, validation, page count, or completion status from another. Each project keeps its own locked protocol, source ledger, data provenance, analysis environment, negative-result record, reproducibility review, and flagship quality decision. Parallel work must not cause outcome inspection before protocol lock or turn incomplete components into stubs.

## Useful-results metric and novel-direction gate

The standing target is 100 useful results. The running count is audited in `orchestration/useful-results-ledger.csv`; setup and feasibility GO alone do not count. Informative negatives count only when a frozen design establishes a durable scientific, source, transport, identifiability, or compute boundary.

Before a new experiment starts, its protocol must state plainly:
- what is genuinely new here;
- what useful discovery could result;
- why it matters;
- what a top-lab reviewer would ask next.

Queue selection favors novel, falsifiable directions over incremental reruns. A blocked design must be redesigned within open-data, computational-only constraints, with the substitution locked and documented before inspecting the redesigned outcome. Competition-quality rigor is a quality standard, not a claim that the work is entered in a competition.

## Discovery-grade ambition without claim inflation

Queue selection should favor questions where a genuinely original biological or methodological finding is plausible and consequential. Ambition may reach discovery-grade science, but evidence controls the claim. Reports must say plainly when a result is confirmatory, incremental, non-novel, or negative. No award-level, field-changing, or breakthrough label is permitted without independent evidence that supports it. Quality outranks quota.

## Fun in the question, serious in the method

Queue selection should also favor experiments that are genuinely interesting to follow: surprising biological angles, playful but falsifiable hypotheses, and results whose story is worth reading even when negative. "Fun" never weakens the protocol. The question can be imaginative; the data provenance, controls, statistics, uncertainty, and claim boundaries remain strict.

## Sculpted project standard

A useful result is a scientific finding, not a finished project. Every useful result must become a complete project package before graduation:

1. **Neat approximately 20-page report.** A designed, readable report with abstract, question, novelty, literature and gap, methods, provenance, locked protocol, results, uncertainty, controls, failures/substitutions, biological interpretation, limits, ethics, application, next experiments, references, figures and appendices. Page count is a design target, never padding.
2. **Research-paper-grade write-up.** A separate manuscript with title, abstract, introduction, related work, methods, results, discussion, data/code availability, author/contribution record, references and supplement. Claims must match the evidence.
3. **Working tool or concrete application.** Build a tested reusable tool when the science supports one: CLI/package, reproducible workflow, interactive atlas, calibrated scoring/reporting service or decision-support interface. If a tool would overstate a negative result, deliver a concrete application angle instead: a failure detector, dataset audit, benchmark, monitoring rule or experimental-priority workflow. No mocked interface counts.
4. **External-review kit.** Include a one-page abstract, clear poster/figure set, reproducibility notebook/log, limitations sheet and a question bank for expert review.
5. **Cumulative project synthesis.** Integrate all positive, negative, contradictory and non-estimable rounds. Do not let the final positive result erase earlier failures.

A result may count toward the 100-result metric once adjudicated, but a topic graduates only after this project package and the multi-round graduation standard are complete.

## External quality references

The program uses official public criteria as structural references, not as evidence of entry or prize-worthiness:

- Regeneron STS evaluates original, independent work through a Research Report and PhD-level review, then public explanation and interviews: https://www.societyforscience.org/regeneron-sts/judging-and-awards/
- ISEF emphasizes a clear testable contribution, well-defined controls, systematic and reproducible analysis, appropriate statistics, creativity, potential impact, limitations, independence and quality of future-research ideas: https://www.societyforscience.org/isef/grand-award/criteria/
- Davidson Fellows uses expert judges and category-specific project evidence, with careful authorship and attribution requirements: https://www.davidsongifted.org/gifted-programs/fellows-scholarship/eligibility/how-to-apply/
- Nobel-level ambition is interpreted only as a long-range discovery standard. The official medicine criteria center discoveries of major importance that change scientific paradigms and benefit humankind; the program never labels its own work Nobel-level without extraordinary independent evidence: https://www.nobelprize.org/nomination/medicine/
