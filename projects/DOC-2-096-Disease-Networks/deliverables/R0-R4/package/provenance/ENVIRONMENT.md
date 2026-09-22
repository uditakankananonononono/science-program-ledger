# Environment notes

Frozen analysis environments are documented in each round's frozen reports and code (`frozen/rounds/*/.../code/`, reports dated 21 September 2026). The frozen per-round `file_manifest_sha256.csv` files record every frozen input and output with bytes and SHA-256, including the large raw ClinVar downloads that remain external.

Packaging environment: Linux x86_64; Python 3 standard library for the exporter and tests; pdfTeX (TeX Live 2022) for the PDF; matplotlib 3.10.9 for the two new deterministic figures. Packaging does not invoke the scientific pipeline.

Figure rerender contract: `python3 figures/render_figures.py` under matplotlib 3.10.9. The renderer consumes only two frozen CSV files, embeds each source SHA-256 in the PNG metadata and image footer, and rewrites the source-hash sidecars. A packaging-time rerender produced byte-identical PNGs. The R0 figure is a byte-identical copy of the frozen original and is not rerendered.
