# SP-004 - The Small Protein Evidence Gap

**Outcome:** MIXED EVIDENCE; locked success gate failed.

This is a real open-data experiment on 110,974 reviewed bacterial UniProtKB entries: 30,573 proteins of 30-100 amino acids and 80,401 controls of 101-200 amino acids. The protocol and its hashes were locked before cohort retrieval. GO and function-comment coverage were lower for small proteins, including in equal-weight exact-organism comparisons. The prespecified claim nevertheless failed because raw PDB-link coverage was slightly higher, not lower, in the small-protein cohort. That contradiction is preserved.

Read `report/FULL_TECHNICAL_REPORT.md` first. Reproduce with `python3 code/run_analysis.py` using Python 3.10+, pandas, NumPy, SciPy, and Matplotlib. The raw UniProt exports and every independent RCSB response are included.
