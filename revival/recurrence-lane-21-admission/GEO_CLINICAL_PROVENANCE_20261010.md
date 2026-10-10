# GEO clinical-product terms and byte-provenance packet
October 10, 2026. Documentary verification only. No clinical-value analysis or derived-file changes.

## Result
All five existing derived clinical CSVs match their recorded SHA256. Current original source HTTP bodies have now been independently hashed. These are new current-byte receipts, not reconstructed historical original hashes. GSE2990 additionally has a retained original supplement that matches the current source exactly.

## Source/derived distinctions
The original pull script streamed matrix headers and stopped before the expression table; it serialized selected metadata to CSV. Its manifest hashes those CSVs, not the original compressed matrix files. The four current compressed source hashes below cannot be relabeled as historical pull receipts.

| Cohort | Current original bytes | Current original SHA256 | Derived CSV matches existing manifest |
|---|---:|---|---|
| GSE2990 | 13645 | 163a04ac54707a88f4ec7ebea0ecf2eaa4b926a1ab14ed0961ec1cfbda451106 | True |
| GSE7390 | 24203878 | 950cde4ba15f919d11cd446657798600776b1f9c84db180ff8e7c1af727780cc | True |
| GSE11121 | 9426477 | 965a52b907dd64fa5321c21059809ec9b8f75e6300102c82ee1eeacfda61d78a | True |
| GSE20685 | 136733806 | e818a4d5834e20bbcf01de515caf856c394abb36a02b9cccc95be05c22d0a279 | True |
| GSE25066 | 61627399 | beef319fba17f38e05ff0994513763dfbc7c9cfa9f6c4b2b7c31dcdd036060fb | True |

## Terms
Official GEO disclaimer states: "NCBI places no restrictions on the use or distribution of the GEO data." It immediately adds: "However, some submitters may claim patent, copyright, or other intellectual property rights in all or a portion of the data they have submitted." It says NCBI cannot provide unrestricted permission for such content.
Source: https://ncbi.nlm.nih.gov/geo/info/disclaimer.html .
All five current series pages were fetched. No source-specific license/restriction statement was found in the inspected catalog text. This is a scoped negative, not clearance of submitter rights or publication terms. Dataset access is documented; explicit source-specific reuse clearance remains unresolved. Do not use article licensing automatically as a dataset license.

## Per-source receipts
### GSE2990
- Catalog: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2990
- Verified original source URL: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE2nnn/GSE2990/suppl/GSE2990_suppl_info.txt
- Last-Modified: Wed, 20 Dec 2006 14:20:04 GMT; ETag: None.
- Derived CSV: data_cache/external/geo/clinical_GSE2990.csv; SHA256 fdac26722ff0fee79dbda0a1b719013b090a5370a789c7041a4c533065bb2a30.
- Historical original-source hash: not established by the prior manifest.
- Retained supplement SHA256 163a04ac54707a88f4ec7ebea0ecf2eaa4b926a1ab14ed0961ec1cfbda451106; exact current-source match. This verifies byte equality, not historical retrieval time or rights.
### GSE7390
- Catalog: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE7390
- Verified original source URL: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE7nnn/GSE7390/matrix/GSE7390_series_matrix.txt.gz
- Last-Modified: Sat, 03 Oct 2026 23:58:53 GMT; ETag: None.
- Derived CSV: data_cache/external/geo/clinical_GSE7390.csv; SHA256 3072c1cc44ba1589f71e0f10f074d33b514383444cef7d21ec3e883643155e5b.
- Historical original-source hash: not established by the prior manifest.
### GSE11121
- Catalog: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE11121
- Verified original source URL: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE11nnn/GSE11121/matrix/GSE11121_series_matrix.txt.gz
- Last-Modified: Fri, 02 Oct 2026 14:36:34 GMT; ETag: None.
- Derived CSV: data_cache/external/geo/clinical_GSE11121.csv; SHA256 347f8366e55c6d9be62c466cba16b53993c39a42642818ed7d9c6443d8e2d1a6.
- Historical original-source hash: not established by the prior manifest.
### GSE20685
- Catalog: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE20685
- Verified original source URL: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE20nnn/GSE20685/matrix/GSE20685_series_matrix.txt.gz
- Last-Modified: Fri, 02 Oct 2026 12:40:08 GMT; ETag: None.
- Derived CSV: data_cache/external/geo/clinical_GSE20685.csv; SHA256 6b7cd1ee62db7eddf353fa198d9c9a64addb01b694463a025a1f2e16fb67db66.
- Historical original-source hash: not established by the prior manifest.
### GSE25066
- Catalog: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE25066
- Verified original source URL: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE25nnn/GSE25066/matrix/GSE25066_series_matrix.txt.gz
- Last-Modified: Sat, 03 Oct 2026 15:29:01 GMT; ETag: None.
- Derived CSV: data_cache/external/geo/clinical_GSE25066.csv; SHA256 30f221eb6d25d3788ac46f769d2121a4e6cdcbf34dedb40ccd5e31cb43eca5bf.
- Historical original-source hash: not established by the prior manifest.

## Boundaries and remaining work
No new clinical CSV, endpoint, patient count, model fit, performance result, manuscript change or admission clearance was created. Matrix bodies were streamed for byte hashing only, not stored or analyzed. METABRIC ODbL acceptance and Fine-Gray holds are unchanged.
Next documentary step, if assigned: inspect each original study data-use/copyright statement for restrictions specific to its clinical product. Rights questions remain explicit UNKNOWN rather than inferred from public access.
Full machine-readable receipts: results/geo_clinical_provenance_20261010.json.
