# GATES v2 (locked 2026-09-23 ~22:49 IST, before any network-prediction outcome metrics)
v1 failure documented: the self-knockdown mRNA gate (target log2FC < -0.25) is
biologically miscalibrated for this assay - CRISPR KO is a protein-level lesion; target
mRNA rarely drops (1/27 targets passed; stimulated condition no better). QC inspection
of self-effects only; NO network-prediction outcome metric has been computed.

## Pivot: effect-presence panel rule (replaces self-knockdown rule; all else identical)
- Panel rule v2: targets with >=25 unstimulated cells whose pseudobulk DE magnitude
  (sum of squared DE across the same top-500 control-variable genes) exceeds the 95th
  percentile of a 100x control-split null (random halves of the 615 unstimulated
  controls, same pseudobulk DE computation - pure noise floor).
- If panel size < 5: experiment declared under-powered; boundary ships documented, not
  counted. If >= 5: G1/G2 as in GATES.md on the v2 panel.
- Biological payload added: target-mRNA invisibility of CRISPR KO QC documented as a
  boundary finding with numbers.
