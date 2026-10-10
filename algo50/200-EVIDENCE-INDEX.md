# 200 R-05 evidence index (follow-up 1, 2026-10-10)

The score and HSP evidence is committed gzip+base64 encoded in parts, because the web editor cannot take the raw files. Decode: concatenate the parts in order (each part may be joined with a newline; base64 ignores newlines), run `base64 -d | gunzip`. The decoded sha256 equals the original local file hash.

Decoded sha256 (original files):
- 5caf007f476e8a36b945c446f3fc01ae807ef171536c38aab64e0c03853941be  score_local_p20.json (single file 200-score_local_p20.json.md.gz.b64)
- af490a6a5b10b4777fb5d2be2c9da8b693be23371868af9c9d3b32297c5cfea3  L1 m8 (4 parts, 200-l1.m8.tsv.md.gz.b64.part00-03)
- f98bd6b4148c9b58ce869df0d22674ac824fa452e8d41f2409eb2b4473c79e8e  L2 p20 filtered HSPs, l2_merged_p20.json compacted (4 parts, 200-l2_p20_filtered_hsps.json.md.gz.b64.part00-03)

Not committed: score_local_p30.json (sha256 86528806304e0f28a500ce2bed70a526af56fe26ada54b6d1bce39873b0abd3d, local only; p30 numbers are in 200-RESULT.md).

sha256 of committed part files (as served by raw.githubusercontent.com):
- 6eac2cc0faa590a9c699fd94387c6fe81f46206955d9bff9886f8327cdcd7a37  200-l1.m8.tsv.md.gz.b64.part00
- e351c78f132b30cb8a4380c42d29a6352828154b8da8cf5165c05447c83b57af  200-l1.m8.tsv.md.gz.b64.part01
- 62c0485861b9028349f5f8e0674f5b16f05a98a86ff691d920888e7e91d86ad2  200-l1.m8.tsv.md.gz.b64.part02
- 9b63b495f2ba05e86e993e89d904f538ea2c972ca0241ab200b0a2cd4e79532d  200-l1.m8.tsv.md.gz.b64.part03
- e2c24b3414a258d3afac76513be3ae7bcc34b51a2e423c1198fa97a00a877023  200-l2_p20_filtered_hsps.json.md.gz.b64.part00
- b17c66ebd51ed060c040321518fd6f5ba76c081ce645f3659d4f9b557768920d  200-l2_p20_filtered_hsps.json.md.gz.b64.part01
- 67280fc1d5da12d6fc078f4f6e364c02cb73b88848f40f33fb36eb4572e432de  200-l2_p20_filtered_hsps.json.md.gz.b64.part02
- 09144c15f935633dedf348d517f06cd8c74f8c27c279b1b1ea85e4288e69dca2  200-l2_p20_filtered_hsps.json.md.gz.b64.part03
- b3699a99313171dc4597e63d628dd77c20007e22dbd74afa2080bd931fc895b8  200-score_local_p20.json.md.gz.b64
