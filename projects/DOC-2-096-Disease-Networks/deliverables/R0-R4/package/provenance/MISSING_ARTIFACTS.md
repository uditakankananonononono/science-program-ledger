# Missing or intentionally external artifacts

No artifact present in the repository tree was missing; all 87 copied items MATCH the source tree.

The original sealed tar bytes named by the round directory prefixes (`DOC-2-096-R0-negative-evidence-20260921.tar-ee188207`, `...-R1-temporal-20260921.tar-7285855e`, `...-R2-archives-20260921.tar-b0e91108`, `...-R3-ranking-20260921.tar-d6826c64`, `...-R4-competing-risks-20260921.tar-ed93bfa9`) are not stored in the repository; only their extracted trees are. The extracted trees are preserved byte-for-byte here. The tars were not recreated.

Large raw ClinVar downloads are intentionally external and were not duplicated. They remain referenced by immutable SHA-256 (from the frozen per-round file manifests) and live URLs:
- R0 current snapshot: `variant_summary.txt.gz`, 443,063,763 bytes, SHA-256 `f25970aa49619fc73cdf8c878a3a20faaa69a0abd56cc8e14954f1d143e7e44e`; `submission_summary.txt.gz`, 389,000,708 bytes, SHA-256 `cd0c127b746e6fe1c2d9e6cea8da4e6dac39605724b9a626c59e163e7ff76b7c`. URLs and retrieval UTC (2026-09-21) are in the frozen R0 provenance files.
- R2 December 2020 archives: `variant_summary_2020-12.txt.gz`, 66,898,694 bytes, SHA-256 `c0a58a61189e56dc173b5c54a738f82ef8c0b28c3c32db98d40f152f181b72c3`; `submission_summary_2020-12.txt.gz`, 66,333,475 bytes, SHA-256 `c974b5a83b9059b6df10b7b064eedc47d0ea7f4dea1021cdbd2857f467a74e76`.
- R2 December 2023 archives: `variant_summary_2023-12.txt.gz`, 217,978,467 bytes, SHA-256 `19d7a2663d3eb3bab1b3440ca495b9b1b182a85e878a8899d53787bb9361f7c2`; `submission_summary_2023-12.txt.gz`, 210,161,401 bytes, SHA-256 `46d3994a96f0be80a44ab8e685f8dd64a4f2411d96d40a8278d9c4796e6edbef`. Archive URLs are in the frozen R2 provenance files.

This compact package does not claim full scientific-pipeline rerunnability without those external bytes. Nothing was recreated from memory.
