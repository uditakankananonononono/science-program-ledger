# Deploy Keys

Write deploy keys for science-program builders, maintained by the orchestrator. Keys are identified by fingerprint, not title. Revoke only on respawn instructions from the orchestrator.

Note: GitHub allows a given deploy key on only one repository, so a builder that pushes to both a slice repo and this ledger needs a separate key per repo.

| Added (UTC) | Title | Fingerprint (SHA256) | Lane / agent | Deployed on | Notes |
|---|---|---|---|---|---|
| 2026-09-24 | B01 v3 PB2 builder | r6of2QA9CbmipjNWsmV2uaSBk2+JWc6ZKl5xchyAKS0 | B01 v3 (H5N1 PB2), agent-01M38M9CPHDBHJ2QDXA97XMP8K | h5n1-mammal-jump (write) | Key self-labeled "b14-builder-v4" and quoted the B14 v4 agent id while reporting from the B01 v3 envelope; identity tracked by fingerprint per orchestrator. Ledger add failed (GitHub: key already in use on h5n1-mammal-jump); needs a separate keypair for ledger write access. The actual B14 v4 (dengue) key will be added separately when it reports. |
| 2026-09-24 | B01 v3 ledger builder | fdYb6rLN91H1C2pPe21EaSeE+moS+I07OJlxetXt834 | B01 v3 (H5N1 PB2), agent-01M38M9CPHDBHJ2QDXA97XMP8K | science-program-ledger (write) | Second keypair from B01 v3, self-labeled "b01v3-ledger"; added per orchestrator after the first keypair could not be shared across repos (GitHub one-repo-per-deploy-key rule). Verified on-page: Read/write. |
| 2026-09-24 | sp-ledger-lane4-v2 | P2XYviFAXPkQGU/hcJkCxJedPfsRVRj9G0uY26Vc8yY | EXP-4 (lane 4) | science-program-ledger (write) | Rotation: EXP-4 sandbox rebuilt 9:14 IST and lost the lane-4 key. Old key "EXP-4 sp-ledger-lane4" (FQhVTZ/TvJ0L2z4lAhsqzexghhPYnc5DtZRz+LXblnM) REVOKED same day; new key verified on-page Read/write. EXP-4 work verified safe through 8240f812. |
| 2026-09-24 | orchestrator-qc-readback-v3 | 8LQBM7DY7AkBfr5sSvb61m1F+H4SWXmrWjh3hUa8B4Y | Instinct orchestrator (QC readback) | account-level SSH key | Infrastructure rotation: orchestrator sandbox was rebuilt and lost the qc private key. Old account key "orchestrator-qc-readback-v2" (FdNeaBYbmw5+QUrfZTjxMxOxBgI+2PgpBHFGEHVWh1Y) REVOKED; v3 verified on-page and live-tested (ls-remote + this push). |
| 2026-09-24 | EXP-1 exp1-deploy-20260924 | aqnqIXlyNF0Us4n9qygozj8y1YYc+4Bp4x/R8hgx+q0 | EXP-1 (lane 1) | science-program-ledger (write) | Rotation: EXP-1 sandbox rebuilt ~9:27 IST and lost its deploy key (second rebuild this morning, same wave as spawn deaths). Old key "EXP-1 exp1-lane1-science-program-ledger" (Ny9jB9UqJ1xLWQsx6gY3JVDFu/pPbRTL5KI6m0DnTJE) REVOKED same day; new key verified on-page Read/write. EXP-1 holding 032 HMP2 staging + local scoring to push. |
| 2026-09-24 | Instinct algo50 lane1 v2 | bQSU9XrBuFqJiz6nudfFkKtKqKKpJYIIwIP5MlHU+ns | RES-1 v5 (algo50 lane 1), agent-01M38DSMZXV0PV7DC9J7WT4ZRM | science-program-ledger (write) | Rotation: RES-1 sandbox rebuilt ~9:30 IST, lost key + 55 cache (third rebuild this morning: EXP-4 9:14, EXP-1 9:27, RES-1 9:30 - same error wave). Old key "Instinct algo50 lane1" (bc4bD5E2KbNjL7kLfO6X1WRYUpmWwnonrwDCCvaqGvA) REVOKED same day; new key verified on-page Read/write. 55's locked protocol is safe in the repo; featurization re-running (~25 min) then folds. |
| 2026-09-24 | B14 v8 dengue builder | KyLKvfEL2+SELQnv0mpMFyMVniHSC8P/mEJkwsjDEjs | B14 v8 (dengue DENV-1/2), agent-01M38SF6R2YD9C6DSY1JG69FFY | dengue-e-protein-expansion (write) | First B14 keypair, self-labeled "b14-dengue-builder". Lane survived 9 spawn deaths before v8 came alive 9:36 IST. Verified on-page: Read/write. |
| 2026-09-24 | B14 v8 ledger builder | iZvG1ao1LZt0m5MY2V+ynQrMYRsv6/ZOSX5TgAxCPag | B14 v8 (dengue DENV-1/2), agent-01M38SF6R2YD9C6DSY1JG69FFY | science-program-ledger (write) | Second B14 v8 keypair, self-labeled "b14-ledger-builder" (two-keypair pattern: GitHub allows a deploy key on only one repo). Verified on-page: Read/write. |
| 2026-09-24 | B01 v3 PB2 builder v2 | 5mfwBcwDB6aJiDlCZcOFT1SIc5Sff07FN4yIkbJPRCU | B01 v3 (H5N1 PB2), agent-01M38M9CPHDBHJ2QDXA97XMP8K | h5n1-mammal-jump (write) | Rotation: B01 v3 container rebuilt (4th rebuild this morning), old private keys destroyed. Old h5n1 key (r6of2QA9CbmipjNWsmV2uaSBk2+JWc6ZKl5xchyAKS0) REVOKED same day; new key (label b01v3-h5n1-v2) verified on-page Read/write. Locked gates 40b8b6a safe. |
| 2026-09-24 | B01 v3 ledger builder v2 | jyqxAOrqMnTsctlKuy942iK6ORa2lOcuZL4ZOb/rNV0 | B01 v3 (H5N1 PB2), agent-01M38M9CPHDBHJ2QDXA97XMP8K | science-program-ledger (write) | Rotation: same rebuild. Old ledger key (fdYb6rLN91H1C2pPe21EaSeE+moS+I07OJlxetXt834) REVOKED same day; new key (label b01v3-ledger-v2) verified on-page Read/write. |
| 2026-09-24 | doc230-laneA-ledger | f7uVotxLxkZiGPzdSt+VvG7OH3Ba/R4PPjDk5Byp3gE | Doc230 lane A v6 (parents 1-6), agent-01M38XRK333GGJ21PPRF8Q9QAF | science-program-ledger (write) | Doc230 relaunch 10:51 IST (all 4 prior lanes died overnight). Ledger-write keypair per two-keypair pattern; lane's pathway/work key HELD (no per-project repos). Verified on-page: Read/write. Program folder = doc290/. |
| 2026-09-24 | doc230-laneB-ledger | DuGa1OFa+iDRNal2fxFkqpE65M5pY94t/r1yzVpR7VU | Doc230 lane B v5 (parents 7-12), agent-01M38XRM4CKTE7Y71VV5EMXHR3 | science-program-ledger (write) | Same relaunch; work key doc230-laneB-main HELD. Verified on-page: Read/write. |
| 2026-09-24 | doc230-laneD-ledger | wzKLGJ1VPY7FGPUJUX0kuCoXt09U13XzeLq27jAAiP0 | Doc230 lane D v3 (parents 18-23), agent-01M38XRP0B1K1JYYBF51CPXQX1 | science-program-ledger (write) | Same relaunch; work key doc230-laneD-science HELD. Verified on-page: Read/write. |
| 2026-09-24 | doc230-laneC-v2-ledger | TjYmityEE0+1iVeRqifHO/Uoosf+h7MGLiZn8ey3ZHw | Doc230 lane C v2 (parents 13-17), agent-01M38XRN22S6SMVG5WRWH7PRZ4 | science-program-ledger (write) | Same relaunch; repo key HELD (no per-project repos). Verified on-page: Read/write. |
| 2026-09-24 | Doc290 lane A v5 | 31ETQuZ0ju46jLuzS+82hZQQv3WGvgNG7JgwC3Cs1Kk | Doc230 lane A v5 (dead, completed-state) | science-program-ledger (write) | REVOKED 2026-09-24: lane died in overnight error wave; replaced by lane A v6 (f7uVotxL...). |
| 2026-09-24 | Doc290 lane B v4 | YFCa9ZwbU29XSCo4JwNtPMft8XSekP6S4VfKUvG/5d0 | Doc230 lane B v4 (dead, failed overnight) | science-program-ledger (write) | REVOKED 2026-09-24: replaced by lane B v5 (DuGa1OFa...). |
| 2026-09-24 | Doc290 lane C | q92McUAmnlbHLhZh8eEb1+YqyHkYIPPUNTXvi11YeO8 | Doc230 lane C (dead, failed overnight) | science-program-ledger (write) | REVOKED 2026-09-24: replaced by lane C v2 (TjYmityE...). |
| 2026-09-24 | Doc290 lane D v2 | VExnCLG5QbYiat92LQEX3E3PMiktMzCPi53noBA3ZhU | Doc230 lane D v2 (dead, completed-state) | science-program-ledger (write) | REVOKED 2026-09-24: replaced by lane D v3 (wzKLGJ1V...). |
| 2026-09-24 | meemee-phaseB-builder | Y6Ie5sNkJ6P4nxWk42f0YHtVBxBSjnItrITESAZelCA | meemee phase-B builder | meemee (write) | User-verified batch (WhatsApp "You add" 11:03:07 IST, wamid ...QUNBOTAwRjZBQzFGMUQ1RTQ0Q0Y3NzRGQUQyQjBCQkQA): batch-add public builder keys to meemee/atlas-ai/sugarcode-ai. Verified on-page: Read/write. |
| 2026-09-24 | instinct-meemee-pb4 | JznCq0rlssBSGi3Xz6iy5+2bLyMbvMPBxd2sSDMI/2c | meemee builder pb4 | meemee (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | instinct-pb7-meemee | w4CVTSnAOHg+IYmbwJPrk7ViM5rzU3bdjdBa81ureNM | meemee builder pb7 | meemee (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | instinct-pb1-meemee | ehUSoey8Ahg1OmGFDDKJu6jwR4/X3xr38f1/Lpl7BhM | meemee builder pb1 | meemee (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | atlas-builder-2026-09-24 | 003NWfsBmdtFt9SPU+4HmRqUO3lyDsu8j+zSvxyvWq8 | atlas-ai builder | atlas-ai (write) | Same verified batch. Read/write on-page. Note: atlas-ai intentionally public per user 11:03:55 IST ("Nope it okay"). |
| 2026-09-24 | instinct-atlas-pb5 | ZNer6QwfO4Q5mYq7nFwdd+dETSyJfUsUIpXYVYrzdE4 | atlas-ai builder pb5 | atlas-ai (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | atlas-pb2 | 8+jB3Lr9/UrwTPcFH3FpKwK6gMwvnAF+A9zzof3fCJU | atlas-ai builder pb2 | atlas-ai (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | atlas-pb8-builder | jMqoT0XFi3gW3Gp+gb7rC8awLpybqxbwLy5XyicIIdI | atlas-ai builder pb8 | atlas-ai (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | instinct-pb3-sugarcode | a9fNM2iTcbOJMFy4IJhYBlL8g7p3L7hsvDoBRfC/vlY | sugarcode-ai builder pb3 | sugarcode-ai (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | sugarcode-pb6-builder | L1Tjk69xTZsrjJFMIZYudtyHXJfnb+VIAWZfk/4vML4 | sugarcode-ai builder pb6 | sugarcode-ai (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | sugarcode-builder-2026-09-24 | FXQ2m7jjI7CZq5514VoilQQNBwSwgowW6x9Xbo6DRwQ | sugarcode-ai builder | sugarcode-ai (write) | Same verified batch. Read/write on-page. |
| 2026-09-24 | atlas-ai-merge-agent | XR9BLOThGlpAwo8JEcTz1ACPpg8o0Tmql8PJbm2SyxY | atlas-ai merge agent | atlas-ai (write) | Continuation of the user-verified "You add" batch (11:03:07 IST). Verified on-page: Read/write. |
| 2026-09-24 | instinct-doc230-laneB | 9UwbJ0no5z8GKe5F3Fvs1N45k8hqTcQf8acC106cHpA | Doc230 lane B (replacement) | science-program-ledger (write) | Replaces dead lane B v5. Old key doc230-laneB-ledger (DuGa1OFa+iDRNal2fxFkqpE65M5pY94t/r1yzVpR7VU) REVOKED same day - lane B v5 died without ever pushing (zero lane-B commits since key add). New key verified on-page: Read/write. |
| 2026-09-24 | sugarcode-ai-merge-agent | fKSpAUEKHoL+hskUXXABnXCzfb4MfSZRuCECGnGn1A4 | sugarcode-ai merge agent | sugarcode-ai (write) | Same verified batch scope. Second keypair per GitHub one-repo-per-deploy-key rule: the atlas-ai-merge-agent pubkey (XR9BLOTh...) was rejected on this repo as already-in-use (lives on atlas-ai). Verified on-page: Read/write. |
| 2026-09-24 12:14 IST | ADD | snakebite-antivenom-atlas | instinct-snakebite-closer | SHA256:DlYG43aHLs9FiSuN8qWDJmKzhzIv7ICFJlfRwK4btpk | write | B09 closer (paper + full manifest + seal commit); replaces deleted stale B09 builder; verified on-page Read/write |
| 2026-09-24 13:02 IST | ADD | science-program-ledger | instinct-res2 | SHA256:rkWSFsR3BlgW73L++OP/EC43XhAEX+j/g0NEgvpo6L0 | write | RES-2 lane; same shape as RES-1/EXP lanes; verified on-page Read/write |
| 2026-09-24 13:33 IST | ADD | science-program-ledger | instinct-res3 | SHA256:EqrnVXIhJMpr5g89GiP/qTwJc1esAM537t5uuFSD04U | write | RES-3 lane; verified on-page Read/write |
| 2026-09-24 13:34 IST | ADD | atlas-ai | instinct-m16-builder | SHA256:ZAKRYDKE6M3ylAp1ZDeAuTWRiTrlT2lsu3JeHLbxkkQ | write | M16 sprint builder; verified on-page Read/write |
| 2026-09-24 13:34 IST | ADD | atlas-ai | instinct-atlas-m15-keys | SHA256:ZAvRCG/5GSC4WhTEiD2wS465/WL1vJ3Eqa8VVu8CwZ8 | write | M15 sprint builder; verified on-page Read/write |
| 2026-09-24 13:40 IST | ADD | atlas-ai | instinct-merge-m15m16 | SHA256:Tf82h6nSgW9o2YOmD5b7YLXkUWWS3+/1hyMHd7zIxt0 | write | M15/M16 integrator; verified on-page Read/write |
| 2026-09-24 14:04 IST | REVOKE | science-program-ledger | EXP-1 exp1-deploy-20260924 (old) | SHA256:aqnqIXlyNF0Us4n9qygozj8y1YYc+4Bp4x/R8hgx+q0 | write | EXP-1 sandbox rebuilt, private key lost; replaced per Main 14:02 (REPLACE authorized) |
| 2026-09-24 14:05 IST | ADD | science-program-ledger | EXP-1 exp1-deploy-20260924 (new) | SHA256:iu5uHNs2+FK/JAFuUZ6ouZK+/0NdCaCpfjAw+LXqdv0 | write | replacement for revoked EXP-1 key; verified on-page Read/write |
| 2026-09-24 14:05 IST | ADD | account-level (all repos) | orchestrator-qc-readback-v4 | SHA256:r0pgaWby7mgWhu9smt3Ss+GCfy4A8xezKx8j2gd4n+w | read/write (account) | replaces orchestrator-qc-readback-v3 whose private key was lost in orchestrator workspace rebuild ~14:00; same-shape restore of previously approved readback key; SSH auth tested OK |
| 2026-09-24 14:20 IST | REVOKE+ADD | atlas-ai | instinct-merge-m15m16 | old SHA256:Tf82h6nSgW9o2YOmD5b7YLXkUWWS3+/1hyMHd7zIxt0 -> new SHA256:QZ8TjV7PEDCBzkYKWcXyT3gILRRutza5jZBdXoH+DQM | write | integrator sandbox rebuilt; swap per Main 14:11; new key verified on-page Read/write, old confirmed gone |
| 2026-09-24 14:57 IST | REVOKE+ADD | atlas-ai | atlas-builder-2026-09-24 -> instinct-atlas-builder-2026-09-24-b | old SHA256:003NWfsBmdtFt9SPU+4HmRqUO3lyDsu8j+zSvxyvWq8 -> new SHA256:ggnUZybhxfeosAXyBQFCY1hEfPeg8gwlA7HsLJjKRzw | write | atlas lead key swap per Main 14:56; new verified Read/write, old deleted on-page |
| 2026-09-24 14:58 IST | ADD | meemee | meemee-builder-2 | SHA256:QiOJEbTG/Q5r6WIjKApExS3jZLukt0A2FqhP0ANx4DQ | write | meemee lead fresh key per Main 14:53; verified on-page Read/write; dead-predecessor revoke target pending Main naming (candidates: meemee-phaseB-builder, instinct-meemee-pb4, instinct-pb7-meemee, instinct-pb1-meemee) |
| 2026-09-24 14:58 IST | ADD | sugarcode-ai | sugarcode-builder-2026-09-24-b | SHA256:vxFGxI/nyCaBRbDRAoTViIBodj6vSzU8gqePAVovfzk | write | sugarcode lead fresh key per Main 14:58; verified on-page Read/write |

| 2026-09-24 15:05 IST | ADD | shared-models | meemee-shared-models-builder | SHA256:TQhGf6L/rAjpH4ViieinHsUBubiFLsSg9U1KLmeca5s | write deploy key, per-lead fresh (one-repo-per-key rule); relayed via Main from meemee lead | Read/write verified on-page |
| 2026-09-24 15:06 IST | ADD | shared-models | atlas-shared-models-builder | SHA256:R2+AbedqBh8Kp0KIO3FEr1hCWQep23Gd39l6mjgUJ5I | write deploy key, per-lead fresh; relayed via Main from atlas lead | Read/write verified on-page |
| 2026-09-24 15:06 IST | ADD | shared-models | sugarcode-shared-models-builder | SHA256:IxTG8Bk0uJlSGnFz1IJPtdyKHcPzTzYkjsR2wv6O99A | write deploy key, per-lead fresh; relayed via Main from sugarcode lead | Read/write verified on-page |
| 2026-09-24 15:07 IST | REVOKE | meemee | meemee-phaseB-builder | SHA256:Y6Ie5sNkJ6P4nxWk42f0YHtVBxBSjnItrITESAZelCA | private half destroyed per lead (relayed via Main 15:59:48); other meemee lanes untouched | verified gone on-page |

| 2026-09-24 15:32 IST | REVOKE | meemee | meemee-builder-2 | SHA256:QiOJEbTG/Q5r6WIjKApExS3jZLukt0A2FqhP0ANx4DQ | private half dead (lead sandbox rebuilt, relayed via Main 15:32) | verified gone on-page |
| 2026-09-24 15:32 IST | ADD | meemee | meemee-builder-3 | SHA256:qPEg1RaYn43Q48tOwF7A7H/7VmebSe9LeuDHqSpCj44 | write deploy key, replacement for builder-2; relayed via Main | Read/write verified on-page |
| 2026-09-24 15:33 IST | REVOKE | shared-models | meemee-shared-models-builder | SHA256:TQhGf6L/rAjpH4ViieinHsUBubiFLsSg9U1KLmeca5s | private half dead (same sandbox rebuild) | verified gone on-page |
| 2026-09-24 15:33 IST | ADD | shared-models | meemee-shared-models-builder-2 | SHA256:7RaOHwlxBfZtW0nw0Elj1OviW6QeSwfRr/cfIh3+Kys | write deploy key, replacement; relayed via Main | Read/write verified on-page |

Note 2026-09-24: builder sandboxes are resetting ~every 40 min this session, killing private key halves; expect further same-shape rotations (relayed via Main).

| 2026-09-24 15:37 IST | ADD | account-level | orchestrator-qc-readback-v5 | SHA256:E6dQmCYJrD3ih8z/91TPvoUZp2nyDI5qw7eV9oCrEps | qc v4 private half lost in workspace rebuild ~15:36 (same sandbox-reset wave hitting builders); v5 = same-shape restore under sprint instruction, same precedent as v3->v4 accepted by Main 14:08 | SSH auth tested OK |

| 2026-09-24 15:38 IST | REVOKE | account-level | orchestrator-qc-readback-v4 | SHA256:r0pgaWby7mgWhu9smt3Ss+GCfy4A8xezKx8j2gd4n+w | private half dead (workspace rebuild); revoke directed by Main 15:38; v3 left per prior decision | verified gone on-page |
| 2026-09-24 15:39 IST | REVOKE | shared-models | atlas-shared-models-builder | SHA256:R2+AbedqBh8Kp0KIO3FEr1hCWQep23Gd39l6mjgUJ5I | private half dead (atlas lead sandbox reset, relayed via Main 15:38) | verified gone on-page |
| 2026-09-24 15:39 IST | ADD | shared-models | atlas-shared-models-builder-2 | SHA256:kHfbsf9GFc4Gv5lrdvXugc1/YjC4E5Ovgz7eLPeAI/g | write deploy key, replacement; relayed via Main | Read/write verified on-page |
| 2026-09-24 15:39 IST | REVOKE | atlas-ai | instinct-atlas-builder-2026-09-24-b | SHA256:ggnUZybh... | private half dead (same reset); relayed via Main 15:38 | verified gone on-page |
| 2026-09-24 15:39 IST | ADD | atlas-ai | instinct-atlas-builder-2026-09-24-c | SHA256:T0XCTFxMVTDz2+GzpdXKQ5SjNcL24mR0Vhghzr2hBVQ | write deploy key, replacement; relayed via Main | Read/write verified on-page |

| 2026-09-24 15:41 IST | REVOKE | sugarcode-ai | sugarcode-builder-2026-09-24-b | SHA256:vxFGxI/n... | private half dead (sugarcode lead sandbox reset, relayed via Main 15:41) | verified gone on-page |
| 2026-09-24 15:41 IST | ADD | sugarcode-ai | sugarcode-builder-2026-09-24-c | SHA256:q3KokKBBxictu5Q56cStT4CjPukaKu3LZTK8RNN8okc | write deploy key, replacement; relayed via Main | Read/write verified on-page |
| 2026-09-24 15:42 IST | REVOKE | shared-models | sugarcode-shared-models-builder | SHA256:IxTG8Bk0uJlSGnFz1IJPtdyKHcPzTzYkjsR2wv6O99A | private half dead (same reset) | verified gone on-page |
| 2026-09-24 15:42 IST | ADD | shared-models | sugarcode-shared-models-builder-b | SHA256:1ExIU+uy58i5TufHomz/dXwtmBluVixN1kQOKLYZim0 | write deploy key, replacement; relayed via Main | Read/write verified on-page |

| 2026-09-24 15:46 IST | REVOKE | atlas-ai | instinct-merge-m15m16 | SHA256:QZ8TjV7PEDCBzkYKWcXyT3gILRRutza5jZBdXoH+DQM | private half dead (integrator hit twice in reset waves, relayed via Main 15:46) | verified gone on-page |
| 2026-09-24 15:46 IST | ADD | atlas-ai | instinct-merge3 | SHA256:Fk/DGBLrizYR6oiC/w4f7NiKXCPxujptIeNWcEymc0s | write deploy key, replacement for M15/M16 integrator; relayed via Main | Read/write verified on-page |

| 2026-09-24 15:59 IST | ADD | sugarcode-ai | audit5-sugarcode-read | SHA256:qaMLkd37e5hmFY0NfopURartEJ9PGmRrtmTilFM44K4 | READ-only audit key; relayed via Main | Read-only verified on-page |
| 2026-09-24 16:00 IST | ADD | sugarcode-ai | audit4-sugarcode-read | SHA256:5YuixF9xTDacRUrgCowgdVUE8CU3/Mt/K3494ddLzos | READ-only audit key; relayed via Main | Read-only verified on-page |
| 2026-09-24 16:00 IST | ADD | sugarcode-ai | audit6-sugarcode-read | SHA256:5A2JbqQYQTsLyA2auu9u7Ea7ut8Ar+1AcSEX5eoXA7E | READ-only audit key; relayed via Main | Read-only verified on-page |
| 2026-09-24 16:00 IST | REVOKE | sugarcode-ai | audit4/5/6-sugarcode-read (all 3) | fingerprints as above | audit distribution moved to source snapshot; keys unused; revoke directed by Main 16:00 | verified all gone on-page |

| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | doc230-laneA-ledger | SHA256:f7uVotxLxkZiGPzdSt+VvG7OH3Ba/R4PPjDk5Byp3gE | lane A deleted (agent-slot cleanup), private half orphaned; revoke directed by Main 16:01; fresh keygen on resume | verified gone on-page |
| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | instinct-doc230-laneB | SHA256:9UwbJ0no5z8GKe5F3Fvs1N45k8hqTcQf8acC106cHpA | lane B deleted; same direction | verified gone on-page |
| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | doc230-laneC-v2-ledger | SHA256:TjYmityEE0+1iVeRqifHO/Uoosf+h7MGLiZn8ey3ZHw | lane C deleted; same direction | verified gone on-page |
| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | doc230-laneD-ledger | SHA256:wzKLGJ1VPY7FGPUJUX0kuCoXt09U13XzeLq27jAAiP0 | lane D deleted; same direction | verified gone on-page |
| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | EXP-1 exp1-deploy-20260924 | SHA256:iu5uHNs2+FK/JAFuUZ6ouZK+/0NdCaCpfjAw+LXqdv0 | EXP-1 deleted; same direction | verified gone on-page |
| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | sp-ledger-lane4-v2 | SHA256:P2XYviFAXPkQGU/hcJkCxJedPfsRVRj9G0uY26Vc8yY | EXP-4 deleted; same direction | verified gone on-page |
| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | instinct-res2 | SHA256:rkWSFsR3BlgW73L++OP/EC43XhAEX+j/g0NEgvpo6L0 | RES-2 deleted; same direction | verified gone on-page |
| 2026-09-24 16:02 IST | REVOKE | science-program-ledger | instinct-res3 | SHA256:EqrnVXIhJMpr5g89GiP/qTwJc1esAM537t5uuFSD04U | RES-3 deleted; same direction | verified gone on-page |

Note 2026-09-24 16:02 IST: ledger also carries "RES-2 v3 algo50 even" (SHA256:vAQ6rIzEdj3mSggONoHJBZYyBm+1JBH8eGjfDHuaZnM, never used, no KEYS.md add-row) - title suggests RES-2 but unconfirmed; HELD pending Main confirmation. Doc230 lane "work keys" (doc230-laneB-main, doc230-laneD-science) are NOT deployed on the ledger; if they exist on other repos they remain live.

| 2026-09-24 16:03 IST | REVOKE | science-program-ledger | RES-2 v3 algo50 even | SHA256:vAQ6rIzEdj3mSggONoHJBZYyBm+1JBH8eGjfDHuaZnM | RES-2 lane deleted; revoke confirmed by Main 16:03 ("no key carrying its name should stay live") | verified gone on-page |

Note: doc230-laneB-main / doc230-laneD-science work keys NOT FOUND on any of the 13 fleet repos (checked all deploy-key pages 16:03 IST) - they were never deployed anywhere. Nothing to revoke.

| 2026-09-24 20:53 IST | ADD | mega27-02-virtual-cell (deploy key) | instinct-mega27-item2-virtual-cell-v2 | SHA256:QLpfIdVo7yksfQKXv2azFzW8Br2a7mhwctiVLhnHY/E | item-2 sandbox rebuilt; v2 key relayed by Main 20:51; replaces dead v1 (dropped from queue, never added) | verified on-page: title + fingerprint + Read/write |

Account-level mega27 builder keys added 2026-09-24 20:54-20:57 IST after GitHub sudo-mode email verification (throttle lifted). All added via github.com/settings/ssh/new, each verified on-page (title + SHA256 fingerprint match vs relayed pubkey, Read/write). Old item2 account key dropped from queue (sandbox rebuilt, replaced by repo deploy key item2-virtual-cell-v2). Relays via Main; mega27 program authorized by user WhatsApp 19:49:23 (verified phone_messages).
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-builder | SHA256:7avQE9lZDC8Qo+d4ydX5W9/JsK4IrO2eX4VZvzId8ds | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-laneB | SHA256:r4vhN2ugxM+EkgtIzocHYnYhkqzAYT8IQtblWvIQmgA | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-laneC | SHA256:A+b92+oJ1xvS81IUCwPJwq+emlNafpNnKzuHGPym8Us | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-laneD | SHA256:vGPsaxW6Zfr7uoOfDvzzcsNX03w4bO5py9CSCPfTOlA | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-laneE | SHA256:YQ5JjCddrVLEgGlgLdRWoNgw4hBrjWt/1GRbJ1e1aQU | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-laneF | SHA256:8oSz4e/hVMd1Kimi+x0cKWCvgOltwvBPizpyrpZYe0Y | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-laneG-builder | SHA256:OXbdiREgyIWXgtH+ZT+1D81R20h5OTS88U4fi5ll+Ns | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-item5-yeast | SHA256:rKxV9lgalSMgASaQ6iBCe9JryKSMpxPhhRhveK7tWM4 | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-06a | SHA256:uPBfG1HhFdakvbkshT5t2S5Tan3IGPQQTdX2whQILA8 | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-lane06b | SHA256:+P1sNFJj+5ZfEVwBZyWhq0/dBWvAYLGRhHPtOP4aPHQ | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-item8-phage | SHA256:Vfzqc3Z/sM8PKGkANRhigc6gexQ+2wVDJjgKaMR1eKQ | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-09a-amp | SHA256:eFCtEj4PLech+WTG8m1ujk6XoF2QwLPYEm3udk/kqOQ | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-09b-peptide-hla-cpp | SHA256:IKsTzR4ApU2dhFn5736Eyfcsk5Cq748KBT/TIUhLz3U | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:57 IST | ADD | account-level (all repos) | instinct-mega27-11b-protein-redesign-4-5 | SHA256:yn6x2Vvl+lHhGcrgAWdWIqoZHgieNaZC5GpZJEXWcaE | mega27 builder key, relayed by Main | verified on-page |
| 2026-09-24 20:59 IST | ADD | account-level (all repos) | instinct-mega27-10a-dl-diagnosis | SHA256:/1wNORT1dOFlj8vD5Z81xP0AjBg7d02O8H+79uKGT4U | 10a sandbox rebuilt 19:56-20:58, new keypair relayed by Main 20:59 | verified on-page |
| 2026-09-24 21:10 IST | ADD | account-level (all repos) | instinct-mega27-lane09c | SHA256:iRpYC8e6CDAbeCHaVyLPysPJ4BZtTdZgmReyfrv7Vro | 09c sandbox rebuilt, key relayed by Main 21:07; repo mega27-09c-peptide-solubility-anticancer created (private) same session | verified on-page |
| 2026-09-24 21:15 IST | ADD | account-level (all repos) | instinct-mega27-lane13a-v2 | SHA256:+ehtfXYMi8ExmD6lYQM9yV/OwckakbzYMK7EaQjcH5I | 13a key re-sent (first relay malformed); repo mega27-13-deep-rl-therapeutics | verified on-page |
| 2026-09-24 21:15 IST | ADD | account-level (all repos) | instinct-mega27-item11a-v2 | SHA256:7l5sPfB9FLvrlpaY4XpB6Cw5+gcUDuy+COBH2bK7/xc | 11a sandbox rebuilt, key relayed by Main 21:15; repo mega27-11-protein-redesign | verified on-page |
| 2026-09-24 21:24 IST | ADD | account-level (all repos) | instinct-mega27-10b | SHA256:J2ERaSsSIAFVMs+gFFjoh7310mbuphhagOK5zL9LO+0 | 10b clean key relayed by Main 21:23; works mega27-10-dl-diagnosis-suite subitems_4_5/ | verified on-page |
| 2026-09-24 22:05 IST | ADD | account-level (all repos) | instinct-mega27-laneB-2 | SHA256:LCMzNZAFrMx5jR0aG8rGgRB8JqyLssoap4Qvq3PJGbA | lane B sandbox rebuilt (memory exhaustion), key relayed by Main 22:03 | verified on-page |
| 2026-09-24 22:05 IST | REVOKE | account-level | instinct-mega27-laneB | SHA256:r4vhN2ugxM+EkgtIzocHYnYhkqzAYT8IQtblWvIQmgA | dead key from rebuilt sandbox; revoke explicitly authorized by Main 22:03 ("remove the dead instinct-mega27-laneB key") | verified gone on-page |
| 2026-09-24 22:28 IST | ADD | account-level (all repos) | instinct-mega27-10a-rebuilt | SHA256:myvdKaGI/SV4BK6diwOKPomHFPQnHXnXjkL75wSsE6c | 10a sandbox rebuilt ~22:27, key relayed by Main 22:28; repo mega27-10-dl-diagnosis-suite | verified on-page |
| 2026-09-24 22:31 IST | REVOKE | account-level | instinct-mega27-10a-dl-diagnosis | SHA256:/1wNORT1dOFlj8vD5Z81xP0AjBg7d02O8H+79uKGT4U | orphaned by 10a sandbox rebuild; revoke explicitly authorized by Main 22:29 ("same authorization as the laneB removal") | verified gone on-page |
| 2026-09-24 22:45 IST | ADD | account-level (all repos) | instinct-mega27-10a-rebuilt2 | SHA256:mcLKCuNWaXQB+YSEAW7vYLedCY+HBbcgzBxMN31BcQQ | 10a box OOM-died and rebuilt 2nd time; key relayed by Main 22:44; repo mega27-10-dl-diagnosis-suite | verified on-page |
| 2026-09-24 22:45 IST | REVOKE | account-level | instinct-mega27-10a-rebuilt | SHA256:myvdKaGI/SV4BK6diwOKPomHFPQnHXnXjkL75wSsE6c | orphaned when 10a's box rebuilt again; explicit Main instruction 22:44 | verified gone on-page |
| 2026-09-24 23:30 IST | ADD | account-level (all repos) | instinct-mega27-builder-2 | SHA256:Gty/QHcEnL9KvlRpCeZNdyQ7uxXRrd6KaZ/MYEXr4es | mega27 lead (item 1) sandbox rebuilt ~23:28; key relayed by Main 23:29; needs write on sugarcode-ai + mega27-01-sugarcode-realdata-validation | verified on-page |
| 2026-09-24 23:30 IST | REVOKE | account-level | instinct-mega27-builder | SHA256:7avQE9lZDC8Qo+d4ydX5W9/JsK4IrO2eX4VZvzId8ds | orphaned when lead sandbox rebuilt; explicit Main instruction 23:29 ("remove the lead's orphaned key") | verified gone on-page |
| 2026-09-25 00:11 IST | ADD | account-level (all repos) | instinct-mega27-builder-3 | SHA256:pPXAHr66UbEJlCLWYTYLj9bbYgi8qw5+t0koh+ZkRuM | mega27 lead (item 1) sandbox reset ~23:54; key relayed by Main 00:00; needs write on sugarcode-ai + mega27-01-sugarcode-realdata-validation | verified on-page |
| 2026-09-25 00:11 IST | REVOKE | account-level | instinct-mega27-builder-2 | SHA256:Gty/QHcEnL9KvlRpCeZNdyQ7uxXRrd6KaZ/MYEXr4es | orphaned when lead sandbox reset; explicit Main instruction 00:00 ("Revoke the orphaned builder-2 key") | verified gone on-page |
| 2026-09-25 11:29 IST | ADD | account-level (all repos) | orchestrator-qc-readback-v7b | SHA256:+ekbEhIpQHMwCrae6Ps7V281Xrt0YHZPe6RHvdluJoQ | orchestrator readback key; added by Main via warm browser session after v6 (SHA256:Y2BNFLC3BU5AIowclIe3NupAPpOGcJw8bGzv8fiRnyA) and v7 (SHA256:fH9f7rmIz/irTW3fZNeaDUo5zovje556OrqPllO2SdY) were both rejected by GitHub as "Key is already in use" despite verified-distinct bodies; v6 private half shredded, v7 discarded; v5 (orchestrator-qc-readback-v5) still ON account with private half lost - revoke pending her decision | verified working via SSH ls-remote + pushes 11:29-11:32; Main confirmed on-page |
| 2026-09-25 11:24 IST | ADD | deploy: mega27-13-deep-rl-therapeutics | mega27-13a-20260925-rebuild | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: mega27-26b-immortal-jellyfish-genomics | mega27-26b-deploy-key | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: mega27-11a-protein-redesign-1-3 | instinct-mega27-lane11a | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: mega27-25-biomarkers-underserved-diseases | instinct-mega27-25-biomarkers | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: mega27-14-digital-embryo | instinct-mega27-14-digital-embryo | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: atlas-ai | atlas-m23-task | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: atlas-ai | atlas-m01-task | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: mega27-27-isef-bioinf-derived-tools | mega27-task-3-6 | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | deploy: mega27-27-isef-bioinf-derived-tools | mega27-task-7-10 | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session, read/write verified | verified by Main |
| 2026-09-25 11:24 IST | ADD | account-level (all repos) | instinct-mega27-laneG-builder | uncaptured (added via Main browser batch; not read back) | batch add via Main browser session | verified by Main |
| 2026-09-25 11:24 IST | REJECTED (never attached) | n/a | mega27-laneC-item24 | n/a | GitHub rejected "Key is already in use" - never attached to her account | reported by Main |
| 2026-09-25 11:24 IST | REJECTED (never attached) | n/a | orchestrator-qc-readback-v6 | SHA256:Y2BNFLC3BU5AIowclIe3NupAPpOGcJw8bGzv8fiRnyA | GitHub rejected "Key is already in use" - never attached to her account; private half shredded | reported by Main |
| 2026-09-25 11:24 IST | REJECTED (never attached) | n/a | orchestrator-qc-readback-v7 | SHA256:fH9f7rmIz/irTW3fZNeaDUo5zovje556OrqPllO2SdY | GitHub rejected "Key is already in use" - never attached to her account; key material discarded | reported by Main |
| 2026-09-25 11:24 IST | REJECTED (never attached) | n/a | atlas-luxury-task | n/a | GitHub rejected "Key is already in use" - never attached to her account | reported by Main |
| 2026-09-25 11:24 IST | REJECTED (never attached) | n/a | atlas-m22-task | n/a | GitHub rejected "Key is already in use" - never attached to her account | reported by Main |
| 2026-09-25 12:28 IST | ADD | account-level (all repos) | mega27-fix-6a-9c | SHA256:x8FJmvD0iNgqV6vnB06/Lm0uUhZOWyXlXB5LNHWsRaE | fix agent 6a+9c key relayed by Main 12:26; account-level per Main 12:27 revision (GitHub key global uniqueness makes multi-repo deploy keys impossible); covers mega27-06a-crispr-gap-tools-1-5 + mega27-09c-peptide-solubility-anticancer | verified on-page |
| 2026-09-25 12:28 IST | ADD | account-level (all repos) | mega27-fix-15-18-20-21 | SHA256:xjDAYoVYWJoLPBMtm/3a3AJwpxP+u/qQXXVJv5W9o7M | fix agent 15+18+20+21 key relayed by Main 12:26 (agent disowned its earlier BLANK_PLACEHOLDER - never added); account-level per Main 12:27 revision; covers mega27-15/18/20/21 | verified on-page |
| 2026-09-25 12:28 IST | ADD | account-level (all repos) | instinct-mega27-fixwave-5-8-17 | SHA256:iPH9JBSqt9GfbQwrF7mbHOXaqgGb3k+NbKG51+IROGo | fix agent 5+8+17 key relayed by Main 12:26; account-level per Main 12:27 revision; covers mega27-05-yeast-metabolic-twin + mega27-08-phage-design + mega27-17-drug-synergy-biclonal-cart | verified on-page |
| 2026-09-25 12:28 IST | REVOKE | deploy: mega27-05-yeast-metabolic-twin | instinct-mega27-fixwave-5-8-17 | SHA256:iPH9JBSqt9GfbQwrF7mbHOXaqgGb3k+NbKG51+IROGo | added as deploy key 12:26 under initial per-repo plan, then removed per explicit Main instruction 12:27 ("REMOVE it from 05's deploy keys, then add the same public key as an ACCOUNT-LEVEL key") - account-level now covers 05 | verified gone on-page |
| 2026-09-25 12:28 IST | ADD | deploy (write): mega27-13b-deep-rl-4-5 | mega27-13b-deploy-2026-09-25 | SHA256:fw7Bxg8G+nr108XTq00AyEaIQngNFJl1HoROjB6nXKc | fix agent 13b key relayed by Main 12:26; single-repo agent so per-repo write deploy key per Main 12:27 revision | verified on-page |
| 2026-09-25 12:29 IST | ADD | deploy (write): mega27-02-virtual-cell | mega27-02-virtual-cell | SHA256:ZGrR4/HU3+Xf8AIFuznjXnpS1/sILkLo8nhA1RqaapI | virtual-cell fix agent key relayed by Main 12:26; single-repo, per-repo write deploy key | verified on-page |
| 2026-09-25 12:29 IST | ADD | deploy (write): mega27-06b-crispr-gap-tools-6-10 | mega27-6b | SHA256:YKdRkbpl0K1J4JnIxyA1tAlMKzz37nLnVWAi2VQrxrE | 6b/7/11b agent sent distinct per-repo keys (Main 12:27); initially added 12:29 with stale title mega27-6b-7-11b, immediately re-titled mega27-6b (delete+re-add, same key body) | verified on-page |
| 2026-09-25 12:29 IST | ADD | deploy (write): mega27-07-pancreatic-ai-and-codon-optimizer | mega27-07 | SHA256:D5/K3xdznQLHcg2WcTT1QPa/7w6sqIxPm/ktVpaQWJE | 6b/7/11b agent per-repo key (Main 12:27) | verified on-page |
| 2026-09-25 12:29 IST | ADD | deploy (write): mega27-11b-protein-redesign-4-5 | mega27-11b | SHA256:Td5Zqp41IfdOzsvkKN1FKqFTJXfYxF2Nt0CyhaLporY | 6b/7/11b agent per-repo key (Main 12:27) | verified on-page |
| 2026-09-25 12:59 IST | ADD | account-level (all repos) | instinct-atlas-selfimprove-20260925 | SHA256:IhqYWSSRD8X+cv0FellN9YPOQZBCxKGhtpPCrvbHxKQ | Atlas self-improvement lane key relayed by Main 12:58 | verified on-page |
| 2026-09-25 14:18 IST | ADD | account-level (all repos) | weird10-lane | SHA256:SLTaekvREsmUrHopsHj5jMFina/8ynFPUbzfiRSNImM | lane-29 weird-science build agent key relayed by Main 14:10 (user green-lighted all 10 projects); account-level per multi-repo rule; covers weird-01-paleoscentome through weird-10-permafrost-enzymes (10 private empty repos created 14:15-14:18) | verified on-page |
| 2026-09-25 14:31 IST | ADD | account-level (all repos) | instinct-mega27-laneG-builder-v2 | SHA256:sxiGeuGc/PwRwiOG/oFZNpzKFWzPninDUkFffgHJZiA | lane G (items 16/22/23a/23b) sandbox rebuilt, lost private key entirely, generated fresh keypair; relayed by Main 14:30; covers mega27-16/22/23a/23b; v1 (instinct-mega27-laneG-builder) left in place - no revoke instructed | verified on-page |
| 2026-09-25 15:12 IST | ADD | deploy (write): mega27-17s-spatial-morphoscan | instinct-mega27-17s-spatial | SHA256:7DTcttRjfXSOFQ6Bvk1Cle+9P72cJd/M/fmVx6FNbUg | 17s spatial lane key relayed by Main 15:11; single-repo agent so per-repo write deploy key on the new private empty repo mega27-17s-spatial-morphoscan (created 15:12, no README/license/gitignore) | verified on-page |
| 2026-09-25 16:14 IST | ADD | deploy (write): mega27-13-deep-rl-therapeutics | mega27-13a-20260925-rotation | SHA256:kJHEOp5Ll4K9U1WXyBF8SL66VmZ3CLds0Ii0iVKauCA | 13a lane rotation: its local pubkey fp MATCHED the attached rebuild key yet correct-URL reads/pushes still 404'd (per-key GitHub flakiness); fresh keypair generated by lane, public line relayed by Main 16:14, validated with ssh-keygen -lf before adding | verified on-page |
| 2026-09-25 16:15 IST | REVOKE | deploy: mega27-13-deep-rl-therapeutics | mega27-13a-20260925-rebuild | SHA256:VH2/pJbmoNrIHJ4ubIUZCg8qwefmYGZ2WuKkE85cI98 | explicit Main revoke instruction 16:13/16:14 naming this key (rotation of the flaky key; replacement rotation key already live and verified before deletion) | verified gone on-page |
| 2026-09-25 17:11 IST | ADD | deploy (write): mega27-25-biomarkers-underserved-diseases | mega27-25-deploy-20260925 | SHA256:S/DjPBrS+KBQtqVLvSYebdnSbRi8iciPgkwZGOBORqA | item-25 lane lost its push path (sandbox lost remote config + private half of prior key); fresh keypair generated by lane, public line relayed by Main 17:11, validated with ssh-keygen -lf before adding | verified on-page |
| 2026-09-25 17:12 IST | REVOKE | deploy: mega27-25-biomarkers-underserved-diseases | instinct-mega27-25-biomarkers | SHA256:62n3c+FY5tIWhZAnISNBDhUQ9dKEsiw51OePp5V3v1I | explicit Main revoke instruction 17:10:42 naming this key and fingerprint (private half lost on lane side; replacement mega27-25-deploy-20260925 added and verified on-page first) | verified gone on-page |
| 2026-09-26 00:33 IST | ADD | deploy (write): mega27-25-biomarkers-underserved-diseases | builder-25-ic | SHA256:1/fMQUxYPuUCDUT0ub3/xQjzz/yI5ZGcEfnqbkCCtww | builder key relayed by Main 00:27 (user order "deploy 25 builders" WhatsApp 00:22:56 + "You add" grant 2026-09-24; revocable on her word); validated ssh-keygen -lf; GitHub sudo-mode email re-auth completed 00:33 to unblock this add | verified on-page |
| 2026-09-26 00:34 IST | ADD | deploy (write): mega27-25-biomarkers-underserved-diseases | builder-25-ppd | SHA256:dWe1TqXW0kwvU/zKFhjVmYpUWxI5xAJzvnUuJ1kWfl4 | builder key relayed by Main 00:27; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:34 IST | ADD | deploy (write): mega27-25-biomarkers-underserved-diseases | builder-25-chagas | SHA256:iDYsCVhm53MRAzft7/LuoIFNZX0aKCRKGhTpgJNFauw | builder key relayed by Main 00:27; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:34 IST | ADD | deploy (write): mega27-10-dl-diagnosis-suite | builder-10-expansion | SHA256:SFxMef2p9TGBV63V/w8qUDMvQ0Yb5BFE9aJpQChWFfc | builder key relayed by Main 00:27 with quoted fingerprint - matched exactly; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:35 IST | ADD | deploy (write): mega27-13-deep-rl-therapeutics | builder-13a-hiv | SHA256:OzJ+WnCvodoV08WShwZ7eZddeTtJCWI53IOnXSfqHWA | builder key relayed by Main 00:28; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:35 IST | ADD | deploy (write): mega27-13-deep-rl-therapeutics | builder-13a-t1d-20260926 | SHA256:8WMqEXBEfp+hJ2SLaRO68op3tYEj0cfhAUqvBv4d8Lc | builder key relayed by Main 00:28; IPTD variant ONLY per Main correction - the earlier INfe mis-transcription was never added; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:35 IST | ADD | deploy (write): mega27-13-deep-rl-therapeutics | builder-13a-onco | SHA256:JTEndLC3Q0VGrZiF4adUj8PJ055jnYUhil4X1FGUzB8 | builder key relayed by Main 00:28; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:35 IST | ADD | deploy (write): mega27-27-isef-bioinf-derived-tools | builder-27-venom | SHA256:tovNa/pvZOESPKttRg7Qzy9s2tsOwZApbbKw98vL5nU | builder key relayed by Main 00:28; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:36 IST | ADD | deploy (write): mega27-27-isef-bioinf-derived-tools | builder-27-phos | SHA256:Gu4wEl6wPdZ+9TfT6Rhqn6TFxsrXuTm70tNQDCn7QaY | builder key relayed by Main 00:28 (builder-corrected placeholder); validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:36 IST | ADD | deploy (write): mega27-24-enviropig-phosphorus | builder-c-enviropig | SHA256:+D7hKg2z5gK/i3i0+gD8pgQ0np0Nd6jbbTnE5EyPFZE | builder key relayed by Main 00:28; validated ssh-keygen -lf | verified on-page |
| 2026-09-26 00:50 IST | ADD | deploy (write): mega27-10-dl-diagnosis-suite | builder-10-expansion-r2 | SHA256:Zf/bqLZWZqt9lb1jqvPvpKMqbfRAmgQDLnN3YNMCP+Y | rotation: builder-10 sandbox wiped ~00:48, private key lost; fresh keypair, public line relayed by Main 00:50 with quoted fingerprint (matched ssh-keygen -lf exactly); added BEFORE revoking orphaned key | verified on-page |
| 2026-09-26 00:50 IST | REVOKE | deploy: mega27-10-dl-diagnosis-suite | builder-10-expansion | SHA256:SFxMef2p9TGBV63V/w8qUDMvQ0Yb5BFE9aJpQChWFfc | explicit Main revoke instruction 00:50:06 naming this key and fingerprint (orphaned by sandbox wipe; replacement r2 live and verified on-page first) | verified gone on-page |
| 2026-09-26 02:13 IST | ADD | deploy (READ-ONLY): mega27-10-dl-diagnosis-suite | builder-27-venom-readonly-mega10 | SHA256:fl9m9CAXcZk29by9ZA7mZ4DLslknGDyUT6ugBzQix9Q | builder-27-venom redeployed to item-10b report-only work (Main 02:12); site-wide key-body uniqueness blocked reusing its mega27-27 key, so fresh keypair relayed by Main 02:13; validated ssh-keygen -lf; Allow write access deliberately UNCHECKED - page confirms "Read-only" | verified on-page |
| 2026-09-26 04:38 IST | NOTE | all builders / push-route failures | n/a | n/a | on "Permission denied (publickey)", FIRST check the active SSH identity matches the builder's designated key (GIT_SSH_COMMAND / ssh -i pointing at the wrong key caused the 04:37 false alarm on builder-c-enviropig - its commit 659b0e3 landed on origin fine once the correct identity ~/.ssh/builder-c-enviropig was used; repo deploy key was never the problem) before assuming a repo-side/deploy-key issue | Main 04:37 directive, verified via ls-remote |
| 2026-09-26 09:46 IST | ADD | deploy (write): mega27-26a-xenobot-evolution | mega27-26a-xenobot-evolution | SHA256:zj+epCXhvWekgYd1++WRcZ9qeJAG/cH4N5jpw+yzLKc | builder 26a push route after browser-upload failure; key relayed by Main 09:45 under standing builder-key grant (user "You add" 2026-09-24); validated ssh-keygen -lf; required fresh sudo email re-auth (window from 00:33 expired) | verified on-page |
| 2026-09-26 13:05 IST | ADD | deploy (write): mega27-10-dl-diagnosis-suite | mega27-10-close | SHA256:4B894AQN7wjOt09Of+C1EFwkvbRmm+mfNZ3Dcxpps48 | closure agent agent-01M3EA5H8RC5VKQ9ZKYC881DN3 (10b closure edits) key relayed by Main 13:05 under standing "You add" grant; validated ssh-keygen -lf; fresh sudo email re-auth required and completed | verified on-page |
| 2026-09-26 13:08 IST | REVOKE | deploy: mega27-10-dl-diagnosis-suite | mega27-10-close | SHA256:4B894AQN7wjOt09Of+C1EFwkvbRmm+mfNZ3Dcxpps48 | explicit Main revoke instruction 13:08:40 naming this key (10b closure agent's work done); builder-10-expansion-r2 and builder-27-venom-readonly-mega10 verified still present | verified gone on-page |

## 2026-09-26 13:39 IST — mega27-04-microbiome-twin rotation (Main 1:38 PM relay, corrected key)
- REVOKE: `instinct-mega27-laneD` (SHA256:vGPsaxW6Zfr7uoOfDvzzcsNX03w4bO5py9CSCPfTOlA) — old lane-D builder key, account-level since Sep 24, private half dead with lane D's sandbox. Deleted from account SSH keys (settings/keys); verified gone post-delete.
- ADD: deploy key `microbiome-builder-20260926` on uditakankananonononono/mega27-04-microbiome-twin — ssh-ed25519 SHA256:2Lz3NEEhmq9mRHxF17eLHVa8IPfiEICtJJgRxCIsXYk, Read/write, added Sep 26, 2026. Verified on-page (SSH, Read/write, Delete button present).
- NOTE: Main's first relay of this key was mistyped by the builder (body ending ...MGrZ9Nd0gdkaDoTdnb8jIwRZuKMDePA6Tc88ZhaOyGx, fp SHA256:ePvK7myCPzpYKVBPDcrhgNQiVQEO9P/fn0Mq5hPEEvs). It was validated locally only and NEVER added anywhere. Only the corrected key (read from the builder's .pub file) was added.
- Discovery: the repo had ZERO deploy keys before this add — the lane had been pushing via the account-level laneD key. Post-state: exactly one builder key on the repo (write).
- Repo state: main afe42ac ("commit final paper PDF and regenerated bundle").

## 2026-09-26 14:02 IST — item-22 project replacement (user order 13:58 "DELETE THE OLD PROJECT" via Main)
- DELETE: repo uditakankananonononono/mega27-22-dreams-computational (old DREAMING project - DreamBank dream-content analysis - superseded by her new sleep-EEG neurodegeneration direction). Pre-delete verification: single branch main @ 27dd590, no other refs/tags, nothing unmerged; sealed head B22@5c09719 not an object in this repo (no seal anchor destroyed); full history preserved in Drive (backup-20260925d-22.bundle list-heads = exact HEAD 27dd590; paper MEGA27-22-50p.pdf/docx also in Drive). Deletion verified live: API 404.
- CREATE: uditakankananonononono/mega27-22-sleep-eeg-neurodegeneration - private, empty (no README/gitignore/license; builder scaffold staged per Main).
- ADD: deploy key `dreaming22-builder-20260926` on uditakankananonononono/mega27-22-sleep-eeg-neurodegeneration - ssh-ed25519 SHA256:vkVW7jUGTA/drbMmSQAYR3rdLBiSfwCruVt+iR2oUvM, Read/write, added Sep 26, 2026 (standing builder-key grant; ssh-keygen -lf validated pre-add). Verified on-page: SSH, Read/write, Delete button present.

## 2026-09-26 15:04 IST — item-23a delete/cancel/restore + new direction (user orders 15:01:54 and 15:03:32 via Main)
- Sequence: user ordered "THEN DELETE THAT AND ENTER THIS DIRECTION: Drosophila connectome -> ANN principles" (15:01:54). Identified mega27-23a-fruitfly-brain-connectome as the sole fly-brain-connectome repo (23b-dna-encoder-cyborg-cell ruled out, not fly/connectome). Backed up byte-exact to Drive, then deleted per order (GitHub confirm ~15:03:29). Her cancel "dont delete then" (15:03:32) landed ~1s after the confirm. Per Main's RESTORE instruction the repo was recreated and content restored from the Drive bundle.
- BACKUP: backup-20260926-23a.bundle in Drive folder 1D-yJqoTmmIb9EvrTHN0LiVYfZIajKGeP (id 1raHX3t9WLJNkLqYXrhQxYdxzZ87jZK0-, 3,979,383 bytes, sha256 94ecaa8e8d5fc2d9d79aa3ab1800613e84c458abb9c57125d973821de03f0c27 - downloaded-back copy byte-identical).
- RESTORE: mega27-23a-fruitfly-brain-connectome recreated (private), pushed from the bundle clone; remote HEAD verified = a574fe797e4f269a6152fee09101381e157c1dbc (13 commits, identical to pre-delete). NOTE: repo was deleted and recreated - any deploy keys/collaborators/webhooks it had before the delete are gone (it had none on record); GitHub repo id changed.
- CREATE: uditakankananonononono/mega27-23a-drosophila-connectome-ann - private, empty (new direction: Drosophila connectome -> ANN principles).
- ADD: deploy key `mega27-23a-builder` on uditakankananonononono/mega27-23a-drosophila-connectome-ann - ssh-ed25519 SHA256:MM85w/FruGUQNIxHpxKN+gfFkveSURKiI9IJCC3NP6U, Read/write, added Sep 26, 2026 (standing builder-key grant; ssh-keygen -lf validated pre-add). Verified on-page.
- Old-project inventory (for the record): 13 commits Sep 24-25 (LaneG), main @ a574fe7; GNN analysis of Winding-2023 larval Drosophila connectome (2,953-neuron matrix), GCN 0.547 vs CNN 0.451 vs linear 0.425 cell-type classification (14 classes); DISCOVERY: 97 wiring-contradiction misannotation candidates (3.8%, pair enrichment, 0/97 unpaired confound); 40-tool (later 42+) external-tools build-out over connectome + 130 Drosophila gene accessions; 52-page paper + audit appendix; formula gate 10 numbered equations; retrain stability 85/97 Jaccard 0.802. 3.8 MiB pack / 167M working tree.

## 2026-09-26 15:13 IST — item-27 teardown + fresh rebuild repo (user order 15:10:46 via Main)
- User order (verbatim): "yes check and delete the current ones under that command and build 5 new" - item 27's six tools (ToxinAudit, CodonContext, GraphHoldout, TranscriptShift, VenomFunction-2, PhosGene).
- IDENTIFY: all item-27 work lived in ONE repo, mega27-27-isef-bioinf-derived-tools - 4 branches: main @ 780bc0d (266 commits), builder-27-phos @ d3d5cb4 (246), builder-27-venom @ 5c96edb (217), item27-transfer @ 913113b (134). The 27-phos/27-venom builders pushed to branches of this repo; no separate venom/phos repos exist. search-code for all six tool names returned zero account-wide (index caveat noted). Repo contents purely item-27 (survey, isefdev, venom/, phosgene/, projects/, builds/, judge rounds) - no mixed-lane ambiguity.
- DISCREPANCY FOUND: judge_rounds_27/ (44 files, rounds 0-5 for the six tools) exists ONLY in this repo - mega27-25-biomarkers-underserved-diseases has NO judge_rounds_27 anywhere (root 404 + find over full tree empty). Main's note that it lives in 25 did not hold; the bundle below is the sole archive. Also: main advanced TODAY (12:15-13:35) with six judge-preservation commits by "Instinct Agent" (a sibling judge worker) - all captured in the bundle; remote re-checked unchanged at delete time.
- BACKUP: backup-20260926-27.bundle (30,376,438 bytes, all refs) split into 2 parts in Drive folder 1D-yJqoTmmIb9EvrTHN0LiVYfZIajKGeP: part-00 id 1xOetWXOu_9Y2d17uvpMFHI7C-DwXd2Im, part-01 id 10t7OIZe3z4MQ7ylMk_nQGAOUACMjvJF8. Byte-exact verified: re-downloaded parts concatenate to sha256 c037ac6378b5320a48df1ef2a31415a9cb92e8da25fd1604befe010835946276 = original.
- DELETE: mega27-27-isef-bioinf-derived-tools deleted ~15:13, API 404 verified.
- CREATE: uditakankananonononono/mega27-27-isef-bioinf-derived-tools - private, empty (fresh start for the 5-tool rebuild, same name per Main).
- ADD: deploy key `mega27-27-builder` on the fresh repo - ssh-ed25519 SHA256:ESpiDxPKv/OKoPPb8AYGwOC/dgg446OWaEBbaKDaJos, Read/write, added Sep 26, 2026 (standing builder-key grant; ssh-keygen -lf validated pre-add). Verified on-page.

## 2026-09-26 15:22 IST — mega27-13-synthetic-lethal-rl created + builder key (corrected relay)
- CREATE: uditakankananonononono/mega27-13-synthetic-lethal-rl - private, empty (new item-13 direction).
- ADD: deploy key `synthetic-lethal-rl-builder-20260926` on mega27-13-synthetic-lethal-rl - ssh-ed25519 SHA256:xpTmjsbRGHbrxSudhTLcejPwlK5qrDLwG4ky3kVJE5s, Read/write, added Sep 26, 2026 (standing builder-key grant; ssh-keygen -lf validated pre-add). Verified on-page.
- NOTE: Main's first relay of this key (15:22:06) was mistyped by the builder (fp SHA256:E7RN9FfoqC9I76T1iXSp6TKA04ergws8h4TGJ1PcVJo); it was NEVER added anywhere. Only the corrected key (Main 15:22:08, verbatim from the builder's key file) was installed. One key total on the repo.

## 2026-09-26 15:30 IST — confirmed 3-repo delete list: 2 executed, lane B held (user "yes" 15:22:48; lane-B cancel 15:25:51 - virtual yeast cell REDIRECTED not deleted)
- HELD (never deleted): lane B repos. mega27-03-virtual-organoid (author "mega27 lane B") and mega27-05-yeast-metabolic-twin both INTACT, never touched. Her 15:25:51 order: virtual yeast cell redirected, not deleted.
- ADD: deploy key `instinct-mega27-05-redirect` on mega27-05-yeast-metabolic-twin - ssh-ed25519 SHA256:NcO6pBFwVarlhrOj5hn0QqP1a3xPociQWqxXBB9njYY, Read/write, added Sep 26, 2026 (standing "You add" builder-key grant; ssh-keygen -lf validated). Verified on-page.
- DELETE: mega27-13-deep-rl-therapeutics ~15:30 (API 404 verified). Inventory: 573 commits all-refs; branches 13a @ 7fa19d98 (HEAD), builder-13a-hiv d8cbe7b8, builder-13a-onco 2beb478e, builder-13a-t1d 1b5eae4; 810MB pack. NOTE: its 4 write deploy keys (incl. the lane rotation key) died with the repo. "Instinct Research" lane was committing judge-preservation work as late as 13:46 today - all captured in the bundle; that lane now has no remote.
- BACKUP 13a (byte-exact verified): backup-20260926-13a.bundle = 849,135,788 bytes split into 34 parts (backup-20260926-13a.bundle.part-00..33) in Drive folder 1D-yJqoTmmIb9EvrTHN0LiVYfZIajKGeP; re-downloaded parts concatenate to sha256 b41242bac05205742382b5b62432fd1168e878e7020d1f3f9f1f6363bb47dd9d = original; bundle heads verified. Part IDs on file with the orchestrator.
- DELETE: mega27-24-enviropig-phosphorus ~15:30 (API 404 verified). Inventory: 158 commits all-refs; main @ 9bfb4a4b, builder-c-enviropig @ 394fc457; 58MB pack. Lane C item-24 published-data Enviropig audit (Powell loss, failed superiority per Main).
- BACKUP enviropig (byte-exact verified): backup-20260926-enviropig.bundle = 61,089,050 bytes split into 3 parts in the same Drive folder; re-downloaded parts concatenate to sha256 79d09b95c7c47d73fb054936486a575c2c328b426465909b8bb478b50113169d = original.

## 2026-09-26 15:40 IST — mega27-26b expansion builder key
- ADD: deploy key `jellyfish-26b-expansion-builder-20260926` on mega27-26b-immortal-jellyfish-genomics - ssh-ed25519 SHA256:jQlwig7gmI4N1IXbQQL97ZzvbiQTE19WcLVpjcOCHw0, Read/write, added Sep 26, 2026 (standing "You add" builder-key grant; ssh-keygen -lf validated pre-add, fingerprint matched Main's relay exactly). Verified on-page: keys list shows the key Read/write with Delete control, alongside existing mega27-26b-deploy-key. Repo now has 2 deploy keys. For the reopened 26b expansion lane (aging/longevity + neurology; 50+ body-page paper rule).

## 2026-09-26 15:44 IST — mega27-19-xenobot-causal-networks created (new item-19 lane)
- CREATE: uditakankananonononono/mega27-19-xenobot-causal-networks - private, empty (xenobot emergent-intelligence project; builder agent-01M3EKA1R836GV9BHDY6QE2Y0M per Main 15:43:56). Deploy key pending builder relay.

## 2026-09-26 15:47 IST — mega27-19-xenobot-causal-networks builder key
- ADD: deploy key `mega27-19-xenobot-causal-networks-20260926` on mega27-19-xenobot-causal-networks - ssh-ed25519 SHA256:A3wBce7wdZiOgbTF8nzMZ6SntsrTg/az+qCMXvKpmfk, Read/write, added Sep 26, 2026 (standing "You add" builder-key grant; ssh-keygen -lf validated pre-add, fingerprint matched Main's relay exactly). Verified on-page: keys list shows the key Read/write with Delete control; repo has exactly 1 deploy key.

## 2026-09-26 15:51 IST — mega27-26a-xenobot-evolution DELETED (user order "delete previosu xenobot project" 15:43:58; pick "first one delete" 15:48:27, Main-confirmed mapping 15:49:33)
- DELETE: uditakankananonononono/mega27-26a-xenobot-evolution ~15:51 (SSH ls-remote "Repository not found" + repo-list absence verified). Inventory: 63 commits, sole branch main @ b64f56ad030e6576f5fa6e2a4477b86d49649dab, 2.01MiB pack. Project: xenobot evolution in a 2-D contact-clearing simulator (weird-science item 26a).
- BACKUP (byte-exact verified): backup-20260926-26a.bundle = 2,097,303 bytes, single file in Drive folder 1D-yJqoTmmIb9EvrTHN0LiVYfZIajKGeP (file id 1pEGpprPhlT0t46ua8CvB9xTjM7Gdzo4j); re-download sha256 7e8d79c595eead4f7cb581d9314a7f113ce4026264b5789fdabbd61a443197c8 = original; git bundle verify "records a complete history" (main b64f56a + HEAD).
- NOT deleted (second candidate, kept): mega27-19-medical-microbots-xenobots - she asked for its results instead.

## 2026-09-26 15:56 IST — lane-29 prune: 8 weird-* repos DELETED (user WhatsApp orders 15:50:52 + 15:51:03; keep W02 + W09; replacements to follow)
Lane mapping (obvious one-repo-per-project, verified before deleting): W01=weird-01-paleoscentome, W02=weird-02-quantum-compass, W03=weird-03-zombie-effectors, W04=weird-04-transmissible-cancer, W05=weird-05-longevity-convergence, W06=weird-06-mirror-life-audit, W07=weird-07-good-prions, W08=weird-08-bioelectric-sim, W09=weird-09-radiation-toolkit, W10=weird-10-permafrost-enzymes.
- DELETE weird-01-paleoscentome (42 commits, main 9055aaa) — backup-20260926-weird-01-paleoscentome.bundle.part-00 (25,122,736B, Drive id 15GR4EQSSI82HGHk9jMIGnscDU1HrQSUc) sha256 608b0a1d11eab5ccd670f403483c9b10a877d537145e04249333a8e6f120ab23
- DELETE weird-03-zombie-effectors (28 commits, main cda3cd3) — bundle 183,633,361B in 8 parts (Drive ids on file w/ orchestrator, part-00 18uTqhP8DIbADKJbU1VIXK4EZuri5Amz1) sha256 3824c30fb5296d20e6a32d9c49d1d43ecd4ea7c564ada659609c244eabffa58e
- DELETE weird-04-transmissible-cancer (14 commits, main 6fdbc06) — bundle 87,875,848B in 4 parts (part-00 18q0tZinU87iYFavEuYMO4F8Aqt2t6XNC) sha256 368a6624dc386689dfbf2826d1fd831de4c6e446a0a77dabd576ac72f6d216c6
- DELETE weird-05-longevity-convergence (6 commits, main b8cd2c0) — bundle 9,448B (1XfVLQ0xGGttSnRR2l6gRG0mRqG5OztnY) sha256 8127bb0d6610f820f7e05a3f30e12c69bc5a814c7c63da960e365fbf5c10ba16
- DELETE weird-06-mirror-life-audit (6 commits, main 4b30bf1) — bundle 9,528B (18LWWeb4wEva06DUiJfxlVZSRI00gBkLX) sha256 48094c86f3f07fc3a5096611d8ae4ab7181c4a22a265ca6fe5efd716c0a29846
- DELETE weird-07-good-prions (6 commits, main e7b6140) — bundle 9,653B (16_C4w4pFW2T6B0Bmos1rQpKoosVsLo6R) sha256 b586261e5ea47b28627d6aedaf3dcd2c8ff0c4a14d7017c48a1472bc497cd573
- DELETE weird-08-bioelectric-sim (6 commits, main b4b082b) — bundle 9,576B (16QWJYwrshtFwbgHBRJ2JBUI_O0chaoO7) sha256 f9d1dce32154750455c62fcbe04998502f7b6216dd0b2145b285ae1587c2afa0
- DELETE weird-10-permafrost-enzymes (6 commits, main 54a7f79) — bundle 9,650B (1pF4MwnTpQfyobE9qo3XDAsiXFC5WMmcD) sha256 cfaf490c271f39f55b8d1bb8103af7a1d6cd953dd236ff1c5b7c0036b340ab46
All 8: bundles re-downloaded byte-exact (sha256 match) + git bundle verify "complete history" BEFORE deletion; all 8 SSH 404-confirmed after. Keepers verified alive: weird-02-quantum-compass b852b29f, weird-09-radiation-toolkit f7d7eefd. Any deploy keys on the deleted repos died with them (repo-scoped).

## 2026-09-26 15:58 IST — weird-11-ai-evolved-biofactories created (replacement slot, "AI-Evolved Biological Factories" spec)
- CREATE: uditakankananonononono/weird-11-ai-evolved-biofactories - private, empty (lane-29 builder agent-01M3BQ8VRH45DFNC4PAPAY4AYH per Main 15:57:12). Deploy key installs on builder pubkey relay per standard protocol.

## 2026-09-26 16:15 IST — mega27 revival builder keys (wave start)
- ADD: deploy key `mega27-revival-02-03-builder` on mega27-02-virtual-cell - ssh-ed25519 SHA256:zuW1ODsVdpg/ZugxtVyKPiffLEAC+rqsxeC6PqH4NYc, Read/write, added Sep 26, 2026 (standing "You add" builder-key grant; Main relay 16:13:11 from builder agent-01M3EMX3R6TXGXQKE4Q7XB1YEV; ssh-keygen -lf validated pre-add, fingerprint matched relay). Verified on-page: keys list shows `mega27-revival-02-03-builder` Read/write.
- BLOCKED: same key body rejected on mega27-03-virtual-organoid with GitHub "Key is already in use" - deploy key bodies must be unique account-wide, so one relayed pubkey can serve only ONE repo as a deploy key. Affects all multi-repo revival builders (02/03, peptide 5-repo, diag 4-repo sets). Escalated to Main: account-level key per builder vs per-repo keypairs.

## 2026-09-26 16:16 IST — mega27-25-biomarkers key: ALREADY LIVE (no-op)
- Relayed install request (Main 16:15:53, builder agent-01M39X0ERCTCN72VNWC4J7G7MQ) for deploy key `mega27-25-deploy-20260925` SHA256:S/DjPBrS+KBQtqVLvSYebdnSbRi8iciPgkwZGOBORqA. ssh-keygen -lf matched the relayed fingerprint exactly. On-page verification: the key is ALREADY a Read/write deploy key on mega27-25-biomarkers-underserved-diseases (original-build key; repo also holds builder-25-ic, builder-25-ppd, builder-25-chagas). Re-add attempt returned GitHub "Key is already in use" = no-op. Builder is unblocked; nothing to change.

## 2026-09-26 16:19 IST — revival wave: 17 per-repo deploy keys installed (option B: per-repo keypairs, Main decision 16:16:56)
All pubkeys ssh-keygen -lf validated pre-add; each install verified on-page (title listed, correct access level). GitHub enforces deploy-key body uniqueness account-wide (proven: "Key is already in use" on duplicate body) - the earlier family/combined keys are superseded by per-repo keys per Main 16:17:18.
- ADD mega27-03-virtual-organoid: `mega27-revival-03-builder` SHA256:XbxhK5UDQ0pOfAxUOugqazobOJUn6H7bJz1U6ceOoEU R/W (builder agent-01M3EMX3R6TXGXQKE4Q7XB1YEV; its 02 sibling key already on mega27-02).
- ADD mega27-09a-amp-design-discovery: `instinct-revival-mega27-09a` SHA256:mnELXsVegQqCir6rk21fmKQGvC3tpnZsTstdOnaUNVc R/W. NOTE: superseded family key `instinct-mega27-peptide-protein-revival` (SHA256:88InLQq+t+h7JaPlQ45qF2a++QKlV0DlYPA1CaJfRwY) also on this repo - revoke candidate, awaiting Main's explicit instruction.
- ADD mega27-09b-peptide-hla-cpp: `instinct-revival-mega27-09b` SHA256:OVDZQNd9NvF+n0JY7EV/blkkLz2IDdRl+vMiGSBESlQ R/W.
- ADD mega27-09c-peptide-solubility-anticancer: `instinct-revival-mega27-09c` SHA256:1zjuzG3xICcBaeREjrbV5vQ4Jpl5f/lCFkuJdqJgtbA R/W.
- ADD mega27-11a-protein-redesign-1-3: `instinct-revival-mega27-11a` SHA256:V+d44QbeU8XbOklZrBoclx+jDk9luXZnGGcFkEkTboA R/W.
- ADD mega27-11b-protein-redesign-4-5: `instinct-revival-mega27-11b` SHA256:DOYEWkJ3uKjmuehOKpCRHt3eX/KLRK7YwDMl0mwt/pg R/W.
- ADD mega27-10-dl-diagnosis-suite: `revival-mega27-10-20260926` SHA256:XlRXouKEy4DhMAvk+ylE4VOGWMvw5yB+chLsXaMMMSI R/W (family diag key never installed; superseded pre-use).
- ADD mega27-10b-dl-diagnosis-4-5: `revival-mega27-10b-20260926` SHA256:SgmYx7VyS3VTw5ls60ajsAexKjzkMVbyjpVcH9i40J4 R/W (repo was 0-commit placeholder; builder filling diagnoses 4-5).
- ADD mega27-16-biodataset-ml-treatment: `revival-mega27-16-20260926` SHA256:UL+YPBAOvLutQQb76Nm7bE+tqvBO8StuXkW1mYxgAA4 R/W.
- ADD mega27-20-drug-target-prediction: `revival-mega27-20-20260926` SHA256:SZbLF2i5h9YT5jGkT263JS92C2QNV4ogoPCBjTY+1pA R/W.
- ADD weird-11-ai-evolved-biofactories: `weird-lane-w11-20260926` SHA256:J6/bPsL414TktujMabIcgwr1umO0aM0tLszc7Ygol6E R/W (lane-29 builder; resolves weird-11 key wait).
- ADD mega27-01-sugarcode-realdata-validation: `instinct-task-mega27-01-validation` SHA256:8iFtPX5yf+iNRJlzTQRdayAmGs5w7AO7nnBa4gBD5Ms R/W (sugarcode validation builder; commits only to mega27-01).
- ADD mega27-14-digital-embryo: `revival-mega27-14-digital-embryo-20260926` SHA256:USs1fBKW6VuZ3GI0AfnEcS8I4Gqzkcl18uAgOmNnAbg R/W (RESOLVES the item-14 builder key pending since 2026-09-25 21:23).
- ADD mega27-23b-dna-encoder-cyborg-cell: `revival-mega27-23b-dna-encoder-cyborg-cell-20260926` SHA256:AzKeHP82l9D8/EE6iiEzo50W5mwFZnp4GLuz+YK6KDo R/W.
- ADD mega27-13b-deep-rl-4-5: `revival-mega27-13b-deep-rl-4-5-20260926` SHA256:4DkAH/9YalzaFt6noaHqZvFHb06bRJS3CI2F0rpSAzA R/W.
- ADD mega27-07-pancreatic-ai-and-codon-optimizer: `revival-mega27-07-pancreatic-ai-and-codon-optimizer-20260926` SHA256:gA5CxwuiTz/qASSWwQQ1X9hbcnPA5TMwrVod2tTT21k R/W.
- ADD sugarcode-ai: `instinct-task-mega27-01-readonly-sugarcode-ai` SHA256:acpnbB/Wn5sQkbuJ2W2ZeVR5cN5u188bhN7OH2KNkF8 READ-ONLY (write checkbox deliberately unchecked; validation builder clones/executes only, feeds reports to product lane).

## 2026-09-26 16:20 IST — superseded family key revoked on mega27-09a
- REVOKE: deploy key `instinct-mega27-peptide-protein-revival` (SHA256:88InLQq+t+h7JaPlQ45qF2a++QKlV0DlYPA1CaJfRwY) removed from mega27-09a-amp-design-discovery (Main's explicit relay 16:20:27 naming the key; superseded by per-repo `instinct-revival-mega27-09a`). Verified on-page: "successfully deleted", repo now holds exactly 1 deploy key (the per-repo replacement, R/W).

## 2026-09-26 16:25 IST — revival wave continued: 5 more per-repo deploy keys
All ssh-keygen -lf validated pre-add; verified on-page (title listed, R/W).
- ADD mega27-12-3d-drug-discovery: `revival-12-3d-drug-discovery-20260926` SHA256:n2lVdJm4RqHEdG1bZTZbFaxLFwNlrpf6uW1mqjOzEzg R/W.
- ADD mega27-21-cancer-recurrence: `revival-21-cancer-recurrence-20260926` SHA256:ulp4Mc8zy2729Kn7zSigaztHxuHDjebiwswgTwYlxVY R/W.
- ADD mega27-18-mirna-research: `revival-18-mirna-research-20260926` SHA256:udXLPJk9hCpzwwJWPv8wYQ36Hj6cenQRolAyi9F/05Q R/W.
- ADD mega27-17-drug-synergy-biclonal-cart: `revival-drug-synergy-20260926` SHA256:cnzn5NlN5gS6UdpyS3kRWiNxlIqOJRlyuP/4A+obfZo R/W.
- ADD mega27-17s-spatial-morphoscan: `revival-spatial-morphoscan-20260926` SHA256:4PnT1beiO4VRktF76rA5ocyuk+Xj6/b1S9F1IzAkQCY R/W.

## 2026-09-26 16:41 IST — atlas-ai builder key
- ADD: deploy key `atlas-build-deploy-key` on atlas-ai (public repo) - ssh-ed25519 SHA256:yIxBn9D31v5pAONgx11/h82wyjSidN8XvMz8tnCispU, Read/write (Main relay 16:40:35 from Atlas paired-browser/social-layer builder; ssh-keygen -lf validated pre-add). Verified on-page: listed Read/write with matching fingerprint; repo holds several pre-existing builder keys (untouched).

## 2026-09-26 17:03 IST — mega27-09d + 09e created (peptide builder expansion)
- CREATE: uditakankananonononono/mega27-09d-oncovax-pep - private, empty (Main relay 17:03:01 from peptide builder agent-01M3EMXQ8V7BHAVQ8TZ663XZ9Z; ChatGPT ideation picked topics).
- CREATE: uditakankananonononono/mega27-09e-resistpep - private, empty (same relay).
- Deploy keys PENDING: standard protocol - builder generates one keypair PER repo (option B), pubkeys arrive via Main relay; install on receipt.

## 2026-09-26 17:04 IST — mega27-09d + 09e builder keys
- ADD: deploy key `instinct-revival-mega27-09d` on mega27-09d-oncovax-pep - ssh-ed25519 SHA256:OxxCVT+OaOQjWF24xz73TH6yIK8H8Vw4qGnwWar1DxU, Read/write (Main relay 17:04:27 from peptide builder agent-01M3EMXQ8V7BHAVQ8TZ663XZ9Z; ssh-keygen -lf validated pre-add). Verified on-page.
- ADD: deploy key `instinct-revival-mega27-09e` on mega27-09e-resistpep - ssh-ed25519 SHA256:QqbJqYYpVb/a68TIfX11j9bYvGJulD7xEK3GI3FmLq4, Read/write (same relay). Verified on-page.

## 2026-09-26 17:04 IST — standing rule: iterative final audit (~10 passes)
- RULE (user email 17:04 in "Bound - every line" thread, gmail auth checks passed, consistent with her authenticated 17:00 WhatsApp spec; via Main): before ANY candy/completion line, every line of her bound project commands is checked against actual implementation about TEN times - repeated line-by-line verification passes against live evidence, not a single audit. No completion claim goes out without that evidence trail. Filed with the 16:41 verification rules + 17:00 ChatGPT-judge novelty rule.

## 2026-09-26 17:05 IST — final-audit rule AUTHENTICATED + external cross-check element
- Her 17:05:14 WhatsApp reply (wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUMzN0FGRTQzN0VBRkNDMEIwNDkzNzIyNUE0NDVCMjYA, replying to her own 17:00 spec) authenticates the 17:04 email rule as a user mandate: ~10 word-for-word verification passes per bound command line vs actual implementation before any candy line. ADDS: "check it externally with other ai tools" - implementation claims get cross-verified with external AI tools, run through HER OWN accounts where sign-in is needed (same pattern as the ChatGPT judge loop); private project material never goes to arbitrary third-party services. Final audit protocol = ~10 passes + external cross-verification before any completion line.

## 2026-09-26 17:49 IST — standing quality bar: repeated improvement, depth + breadth
- RULE (user email 17:49 in "Confirmed - bound" thread, gmail auth checks pass, in-thread with her authenticated WhatsApp confirmations; via Main): keep improving repeatedly and push greater depth and breadth on each task. Lanes iterate on each task rather than declaring done early. Standing alongside the 17:00 novelty rule and 16:41 verification rules.

## 2026-09-26 20:16-20:29 IST — user steering burst: speed + ChatGPT-consult defaults (5 rules)
All five verbatim from her WhatsApp, verified in phone_messages against wamids; broadcast by Main to all 19 lanes.
1. 20:16:32 (wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUNEMUYzOEZENTZCNzBGRDk5MjU2QTg3RjY4N0MxRkMA): "And don't wait for chatgpt cap resets, just text and paste the papers" - judge/critique rounds paste paper TEXT into ChatGPT; Free-tier upload cap no longer gates anything; cap-reset waits cancelled fleet-wide.
2. 20:16:50 (wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUNFMDBCQjE1RjNGM0MxQjNDQ0Y1NzRBMzVGRDc3QjQA): "Make it faster. If at a pause without knowing what to do contact chatgpt" - speed priority; rounds back-to-back as fast as the account allows; ChatGPT text consult replaces any idle pause (consult documented).
3. 20:17:38 (wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUNFOTgyQUNDREIwMDU5NkVFQUQ5NkNDM0IyMENCNjAA): "Any problem, not able to find results etc ask chatgpt what to do" - ChatGPT text consult is the default unblock move for ANY problem, not only idle pauses.
4. 20:27:49 (wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUNGQjhGRDlEQzY0RjZDNkM2QzA5ODZEMzIwMzVBMUQA): "And please keep only a little bit of failed parts in the paper etc. I don't want it filled with failures" - papers foreground verified results; failures compressed to brief honest notes; full audit trail stays in repos; withdrawn claims never presented as wins.
5. 20:28:42 (wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUNDQzIxNjgzMTBDMzdEOTJGQkE3RjhFMThGRkQzMTAA): "Please make sure every project delivered concrete research and results" - concrete deliverables (gated result / evidenced discovery candidate / working tool) are the contract per project; audits and guards are scaffolding; stuck lanes redirect via ChatGPT consult.
Related context not separately ledgered: 20:26:50 WhatsApp ("Ok well so far so good with your tasks? See anywhere your not getting results or are not able to go towards meaningful direction ask for chatgpts help", wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUNCNzAxRTVBN0FBRTFEMzk1Mzc0MEZEMUFGRENGMUMA) - same consult-default intent as rule 3.

## 2026-09-26 20:31-20:37 IST — revival B sandbox-wipe rotation: 7 repos re-keyed
Trigger (Main relay 20:17 + 20:31 URGENT): revival B sandbox rebuilt ~19:55-20:17; ALL per-repo SSH private keys on it wiped; old keys dead and removed; fresh pubkeys relayed by Main (all ssh-keygen -lf validated pre-add; one keypair per repo per standing option-B rule). All adds verified on-page (exactly 1 deploy key per repo, title + fingerprint + Read/write matching). Sudo-mode email gate hit once on first add; verified via her Gmail (code single-use, 15-min window), then all remaining rotations ran clean.
- mega27-09a-amp-design-discovery: REVOKED `instinct-revival-mega27-09a` (SHA256:mnELXsVegQqCir6rk21fmKQGvC3tpnZsTstdOnaUNVc); ADDED `mega27-09a-deploy-20260926` SHA256:SyPe1VnkDEHCCr1FjRAaRYIIMkVpoVkxrEX9CJorC3c R/W.
- mega27-09b-peptide-hla-cpp: REVOKED `instinct-revival-mega27-09b` (SHA256:OVDZQNd9NvF+n0JY7EV/blkkLz2IDdRl+vMiGSBESlQ); ADDED `mega27-09b-deploy-20260926` SHA256:3w8WgRzl3w9A96XhwivXU0ciEKmd6BYnNapf9rxqO+Y R/W.
- mega27-09c-peptide-solubility-anticancer: REVOKED `instinct-revival-mega27-09c` (SHA256:1zjuzG3xICcBaeREjrbV5vQ4Jpl5f/lCFkuJdqJgtbA); ADDED `mega27-09c-deploy-20260926` SHA256:rzc1oJ1B5cauvOBex73LFW8XNzNgoLYm+B3+mXkQljc R/W.
- mega27-11a-protein-redesign-1-3: REVOKED `instinct-revival-mega27-11a` (SHA256:V+d44QbeU8XbOklZrBoclx+jDk9luXZnGGcFkEkTboA) AND older-generation `instinct-mega27-lane11a` (SHA256:ufbrOz7Q4jGg9lc7j8YTfyDJKN8eCjsWsSBb5RSB/pk - same lane lineage, orphaned; flagged to Main); ADDED `mega27-11a-deploy-20260926` SHA256:5yPOwpN/uucmQ5ZS2LbHCJDVwAiiGgUHlsU7B3sGF00 R/W.
- mega27-11b-protein-redesign-4-5: REVOKED `instinct-revival-mega27-11b` (SHA256:DOYEWkJ3uKjmuehOKpCRHt3eX/KLRK7YwDMl0mwt/pg) AND older-generation `mega27-11b` (SHA256:Td5Zqp41IfdOzsvkKN1FKqFTJXfYxF2Nt0CyhaLporY - same lane lineage, orphaned; flagged to Main); ADDED `mega27-11b-deploy-20260926` SHA256:wVmU0akAgXNaMFiQIFsc3R90o7SVpCV9gONIfIPrAT8 R/W.
- mega27-09d-oncovax-pep: REVOKED `instinct-revival-mega27-09d` (SHA256:OxxCVT+OaOQjWF24xz73TH6yIK8H8Vw4qGnwWar1DxU); ADDED `mega27-09d-deploy-20260926` SHA256:ixE0cHzgxPTRdxLTuqepB0xsOzUp+4+NP88/wr0XaqE R/W.
- mega27-09e-resistpep: REVOKED `instinct-revival-mega27-09e` (SHA256:QqbJqYYpVb/a68TIfX11j9bYvGJulD7xEK3GI3FmLq4); ADDED `mega27-09e-deploy-20260926` SHA256:MXJ2ViTw8sCOkuj6S5P1LmHImIQn2QH/NSFEnpB6kAs R/W.
Note: public halves of the two older-generation 11a/11b keys are not held locally (predate today's wave); restoration, if ever needed, requires a fresh pubkey relay.

## 2026-09-26 21:33 IST — mega27-27 rotation PENDING (browser budget)
Main relay 21:33:14 (item-27 sandbox-wipe pattern): fresh pubkey validated (ssh-keygen -lf SHA256:QVbFQ6KjY6nWAMfHmGjES3gvbKP6vgiu4AXzgRongwk, title item27-rebuild-20260926). Install R/W on mega27-27-isef-bioinf-derived-tools + revoke dead previous builder key (`mega27-27-builder`, Main's explicit removal instruction) is PENDING: browser daily budget exhausted until local midnight. One-shot wake set 2026-09-27 00:05 IST. Lane's local HEAD 4a9866d590750db6a115714ab3e1d27a32247753 (2 ahead of published b79f514) - interim restore path via Drive bundle + orchestrator push (proven on mega27-13 at 20:46).

## 2026-09-26 21:35 IST — 4 Jev-integration keys PENDING + item-27 bundle restores
- BUNDLE RESTORES (orchestrator push per standing authority, ancestry-verified fast-forwards): mega27-27-isef-bioinf-derived-tools main b79f514 -> d4ffad1 (bundle sha256 569a0b86...d85eb54, matched Main's stated hash) then d4ffad1 -> f9613106 (bundle sha256 640675b5...56f522, matched). 4 commits restored: 10cae16, 4a9866d, d4ffad1, f961310. Remote verified via ls-remote at f96131061a98e7385dec91c4fa941a59c5f3b454.
- PENDING (00:05 IST wake, browser budget): ADD R/W deploy keys from Jev-integration agent (Main relay 21:35): shared-models SHA256:XR0+soBbbjo0Mcc+TuNDJ67kBtAZbm2sRES5NUZT1/U, atlas-ai SHA256:CKepKy8BFNr2O7f/hMviDm7aFcHHLG0nBzUd7l0DAIM, meemee SHA256:Nf7ft6ga9kD6ef52qmYeaB58GM7ZDKaBbGKPveaWBzA, sugarcode-ai SHA256:9T4xbdkY8EGzyDPQz5woChIrxA9feh+t6OxAlPtZn70. All ssh-keygen -lf validated. ADD ONLY - no revocations on these 4 repos.

## 2026-09-26 21:42 IST — 4 OpenClaw+Hermes keys PENDING (same 00:05 wake)
Main relay 21:42: ADD-ONLY R/W deploy keys from OpenClaw+Hermes integration agent (distinct from Jev set - keep both): shared-models SHA256:1VPeEnB60T3thBr4OnBEhZU6eJywT8yAbBERO6Tn9us, atlas-ai SHA256:bUnEG1q7tKWR/8QqAL3vdoBXBy+o+E89zEmf+yf7IBA, meemee SHA256:ZR8jxs1N9woWT5PpS4ycZlww4IVY95YwLkJDgrdBWeU, sugarcode-ai SHA256:F0Tmqo0/n4NZvOHC05Q5by5ndhKYIJsJ0RdSrmOf9rc. All ssh-keygen -lf validated. 00:05 rotation now 9 adds + 1 revoke (mega27-27-builder).

## 2026-09-26 21:49 IST — item-27 restore #3 + biomarkers-25 false alarm + flakiness rule
- RESTORE: mega27-27-isef-bioinf-derived-tools main 6fa666a7 -> 7ef135bcd70f8ecfb7d2e1a9e29c307fd1985e81 (bundle item27-rebuild-20260926-2149.bundle, sha256 1f7807df...bef79e5 matched Main's stated hash; ancestry-verified fast-forward, no force). 1 commit: 7ef135b "Log published PB-PSB1 DGR genome and authentic baseline runtime block".
- FALSE ALARM: biomarkers-25 lane reported 2x "Repository not found" on mega27-25-biomarkers-underserved-diseases at 21:48; orchestrator check 21:49 found the repo fully intact (HEAD 9c5293ab82529d477cec9badd109af106bed25b6, all builder-25-* branches present, no unauthorized change); lane's third ls-remote succeeded - transient GitHub flakiness, NOT a wipe or key removal. No restore, no key change.
- RULE (Main 21:49): GitHub read flakiness is recurring (slug typos earlier, transient 404s now) - always TRIPLE-CHECK ls-remote before declaring a wipe/access-loss.

## 2026-09-27 00:12 IST — midnight rotation COMPLETE (9 adds + 1 revoke) + item-27 restore to 492c65cf
Ran at 00:07 on Main's 00:07:10 instruction (lanes blocked; ahead of the 00:05 wake which is being retired). Browser lease config-c, sudo gate passed via her Gmail code.
- mega27-27-isef-bioinf-derived-tools: REVOKED dead `mega27-27-builder` (SHA256:ESpiDxPKv/OKoPPb8AYGwOC/dgg446OWaEBbaKDaJos) per Main's 21:33 explicit removal instruction; ADDED `item27-rebuild-20260926` SHA256:QVbFQ6KjY6nWAMfHmGjES3gvbKP6vgiu4AXzgRongwk R/W. Verified on-page: exactly 1 deploy key.
- shared-models: ADDED `jev-docfix-shared-models-20260926` SHA256:XR0+soBbbjo0Mcc+TuNDJ67kBtAZbm2sRES5NUZT1/U and `openclaw-hermes-shared-models-20260926` SHA256:1VPeEnB60T3thBr4OnBEhZU6eJywT8yAbBERO6Tn9us, both R/W, fingerprints verified on-page. Pre-existing keys untouched.
- atlas-ai: ADDED `jev-docfix-atlas-ai-20260926` SHA256:CKepKy8BFNr2O7f/hMviDm7aFcHHLG0nBzUd7l0DAIM R/W verified. OCH key SHA256:bUnEG1q7tKWR/8QqAL3vdoBXBy+o+E89zEmf+yf7IBA BLOCKED: GitHub rejected with "Key is already in use" - the body is already attached as a deploy key somewhere else in the account (confirmed NOT on shared-models/meemee/sugarcode-ai/atlas-ai, NOT an account-level SSH key). Needs either a fresh keypair from the OCH lane or a Main-directed revocation at its current (unknown) attachment. Flagged to Main.
- meemee: ADDED `jev-docfix-meemee-20260927` SHA256:Nf7ft6ga9kD6ef52qmYeaB58GM7ZDKaBbGKPveaWBzA and `openclaw-hermes-meemee-20260927` SHA256:ZR8jxs1N9woWT5PpS4ycZlww4IVY95YwLkJDgrdBWeU, both R/W verified.
- sugarcode-ai: ADDED `jev-docfix-sugarcode-ai-20260927` SHA256:9T4xbdkY8EGzyDPQz5woChIrxA9feh+t6OxAlPtZn70 and `openclaw-hermes-sugarcode-ai-20260927` SHA256:F0Tmqo0/n4NZvOHC05Q5by5ndhKYIJsJ0RdSrmOf9rc, both R/W verified.
- ORCHESTRATOR ERROR (corrected, pending cleanup): the first meemee/sugarcode-ai submissions hand-typed the key bodies instead of piping the .pub files, attaching 4 inert garbage keys (mistyped bodies, no known private halves, unusable): meemee `jev-docfix-meemee-20260926` SHA256:ls2mue1ILl+5QWhIImuKZ46BDCfCO171Gl5sonyLulQ and `openclaw-hermes-meemee-20260926` SHA256:12GO0NsSllcNqXQ29YaWJC6Rdm9Yg41Ymube4vu13dE; sugarcode-ai `jev-docfix-sugarcode-ai-20260926` SHA256:b6bb7CGFoasHlF3hMzyeOXF4IDV4U/XPEclUsfFUSVM and `openclaw-hermes-sugarcode-ai-20260926` SHA256:8vUmzfvqtjOB8VSwORSUxOmO1q3at69mTwBpBJoXKo8. Left in place pending Main's explicit revocation instruction. RULE (ledgered): NEVER hand-type key bodies into browser forms - pipe the .pub file via stdin; verify every add by on-page fingerprint against ssh-keygen -lf of the source file, never by title or key count.
- ITEM-27 RESTORES: across the evening's bundle relays remote main advanced 7ef135b -> ... -> ab4741ef (each orchestrator-pushed, ancestry-verified fast-forwards, reported to Main per bundle). Final leg 00:12: bundle item27-rebuild-20260927-0012b.bundle (sha256 8d856c689402fcad79fcb07c59640c6b5af6066a63135791877f1ef45b7714f6 matched Main's stated hash; the 0012 bundle was superseded before push), FF ab4741ef810e82c3bad8357a460eafd8c2565c21 -> 492c65cf2caaa7e1cbe5c2acba25463c30d2fb39, ls-remote verified. 2 commits: 4d8ecb12 "Distinguish coherent HSP alignment from spliced oracle coverage"; 492c65cf "Refresh DGR gate status without scoring oracle retrieval". Note: item-27's own new deploy key (item27-rebuild-20260926) is now live, so future pushes should come from the lane itself.

## 2026-09-27 00:15 IST — garbage-key cleanup + fresh OCH atlas-ai key
- REVOKED (Main's explicit 00:14:15 instruction naming all 4): meemee `jev-docfix-meemee-20260926` (SHA256:ls2mue1ILl+5QWhIImuKZ46BDCfCO171Gl5sonyLulQ) and `openclaw-hermes-meemee-20260926` (SHA256:12GO0NsSllcNqXQ29YaWJC6Rdm9Yg41Ymube4vu13dE); sugarcode-ai `jev-docfix-sugarcode-ai-20260926` (SHA256:b6bb7CGFoasHlF3hMzyeOXF4IDV4U/XPEclUsfFUSVM) and `openclaw-hermes-sugarcode-ai-20260926` (SHA256:8vUmzfvqtjOB8VSwORSUxOmO1q3at69mTwBpBJoXKo8). Inert mis-paste bodies, no private halves existed. Verified on-page: all 4 titles absent, counts meemee 7 / sugarcode-ai 10. The correct -20260927 keys remain live on both repos.
- ADDED on atlas-ai (Main relay 00:14:35, fresh OCH keypair replacing the collided one): `openclaw-hermes-atlas-ai-20260927-unique` SHA256:jIzn1EXlVCJuVgvAZdsw7G74rervpYWKo+rVk9MX4V8 R/W, ssh-keygen-validated against Main's stated fingerprint before install, verified on-page. The unknown pre-existing attachment of the rejected body (SHA256:bUnEG1q7...) was NOT touched per Main's decision. Rotation now fully complete: 10 adds + 5 revokes.

## 2026-09-27 00:16 IST — master program spec RE-BOUND (user verbatim 00:16:38, wamid.HBgMOTE4MTM0MDk4NTcxFQIAEhggQUNFMkRBMDJGNDJEQUU1NUZDRjQ4MkQ4NENFNUU5MUIA, via Main)
User re-issued the master spec verbatim and ordered it BOUND; binds the finish line, not a reset. Operative rules in todo-01M39WKDAKZWWFVPQE1NDCN8JB. Re-affirmed for every lane: (1) every project passes through ChatGPT as judge and improves novelty until it passes (DeepSeek/Gemini added surfaces); ChatGPT for redirection on failure/low novelty. (2) Non-negotiable per-project gates: 120+ datasets, 40+ external tools, 10+ numbered formulas, 50+ page Times-New-Roman paper (body text only per prior amendment), separate repo, real data, real discovery + working tool beating the best world benchmark in its field. (3) Full AUDIT ROUND before any candy line: every requirement verified exactly as asked except her explicit deletions/redirections. (4) Later corrections override older lines: Atlas/sugarcode = self-audit; NO ISEF competition framing; doc200/230/portfolio dropped.

## 2026-09-27 00:24 IST — item-25 migration: 10 repos created + 10 builder keys installed (Main GO 00:19:40, lane pubkeys relay 00:20:18)
Separate-repo gate of the re-bound master spec. All 10 repos PRIVATE + empty under uditakankananonononono, existence verified by ls-remote (empty). One R/W deploy key per repo, lane-generated (private halves stay in the lane's sandbox), each ssh-keygen-validated then piped from file and fingerprint-verified on-page:
- mega27-25-preeclampsia-biomarkers: mega27-25-preeclampsia-builder-20260927 SHA256:BBLvGfF6LNLuGYQRg6Z01qzo3h5eLYHrMz2rKbsJsn4
- mega27-25-leishmaniasis-biomarkers: mega27-25-leishmaniasis-builder-20260927 SHA256:FYm8TkcONhFMxOyPZKxi7B+51dfbY3aFSJ5nI1QtMe8
- mega27-25-postpartum-depression-biomarkers: mega27-25-postpartum-depression-builder-20260927 SHA256:JTHTEaxo5iwV8RtMrJxPqQe19/zbiASy+KpRiCi/Sso
- mega27-25-long-covid-biomarkers: mega27-25-long-covid-builder-20260927 SHA256:m1Qh4PRGW9Ey8xVzemLWtlTm6iUisEXj85kL+f3mxSw
- mega27-25-me-cfs-biomarkers: mega27-25-me-cfs-builder-20260927 SHA256:R+G3ESHV87NVihGfm4aCSmAB6F3NDS33frSjFH/AoE0
- mega27-25-pcos-biomarkers: mega27-25-pcos-builder-20260927 SHA256:pnGTSfGRPtP8pnpqt+czjSfPFaawxsJo+U8stqbQH0w
- mega27-25-endometriosis-biomarkers: mega27-25-endometriosis-builder-20260927 SHA256:tDC8iRS5pTt7lL/yO5FFT1JyngR1uBzAPcEW3gIkJCQ
- mega27-25-fibromyalgia-biomarkers: mega27-25-fibromyalgia-builder-20260927 SHA256:GGIPIafIuLJMUOUcO/en5fxbQnwzyZwsdBMwRv/c84M
- mega27-25-interstitial-cystitis-biomarkers: mega27-25-interstitial-cystitis-builder-20260927 SHA256:Xbv/gDdlLnJ7t3HU87T7LU07d9N0vYT+U36PHWRHFFQ
- mega27-25-chagas-biomarkers: mega27-25-chagas-builder-20260927 SHA256:TU4fu4MRucqUPm3sdEOjlLYdDqx1632rLJNw0DD4zCE
Shared repo mega27-25-biomarkers-underserved-diseases INTACT (main 343705c888cf at 00:21, key mega27-25-deploy-20260925 SHA256:S/DjPBrS+KBQtqVLvSYebdnSbRi8iciPgkwZGOBORqA present); nothing deleted, no force-pushes. Lane's 00:20-00:21 SSH failures = recurring transient flakiness (4th instance tonight) - its own pushes kept landing throughout. Lane owns content/manifests; builder-only branches integrate via the lane.

## 2026-09-27 00:33 IST — builder-25-chagas-revival key on shared biomarkers repo (Main relay 00:33:20)
ADDED R/W on mega27-25-biomarkers-underserved-diseases: `builder-25-chagas-revival` SHA256:DntjGQEbdbxnqL8eJUCdrFq9A68awQa5gfx+ZmHVmJ4. ssh-keygen-validated pre-install, piped from file, fingerprint-verified on-page (Never used, Read/write). Standing builder-key grant, re-affirmed tonight.

## 2026-09-27 00:42 IST — sugarcode-agent key + multi-repo key blocker
- ADDED on sugarcode-ai (Main relay 00:41:32): `sugarcode-agent-20260927` SHA256:UkBscBzguvBY1BeTYxdBFcMOfesbODZX6MC8ORByrSs R/W, validated + fingerprint-verified on-page.
- BLOCKED pending per-repo keypairs (GitHub one-body-one-attach constraint, option B forecloses account-level): lane29-paper-build SHA256:IphVOh/03/2qaEGUOse0mwFU9Stl36FZiUu+VQijs28 (targets weird-02-quantum-compass, weird-09-radiation-toolkit, weird-11-ai-evolved-biofactories) and paper-assembly-2026-09-27 SHA256:1Vt4fjyToRiTmOxFTmhbpkMarQDsnXPvrs/X9Kg/1CU (targets mega27-09a-amp-design-discovery, mega27-09b-peptide-hla-cpp, mega27-09c-peptide-solubility-anticancer, mega27-11a-protein-redesign-1-3, mega27-11b-protein-redesign-4-5). Reported to Main 00:42; awaiting per-repo keypairs or a named single repo per key.

## 2026-09-27 00:44 IST — sugarcode-agent revoked + 8 per-repo paper-builder keys
- REVOKED on sugarcode-ai (Main's explicit 00:42:31 instruction; agent retired after its patch landed as 1ac902e51d35d106e666850bc4e379c5181063db): `sugarcode-agent-20260927` SHA256:UkBscBzguvBY1BeTYxdBFcMOfesbODZX6MC8ORByrSs. Verified absent on-page.
- OBSOLETE without install (lanes discarded): shared bodies lane29-paper-build SHA256:IphVOh/03/2qaEGUOse0mwFU9Stl36FZiUu+VQijs28 and paper-assembly-2026-09-27 SHA256:1Vt4fjyToRiTmOxFTmhbpkMarQDsnXPvrs/X9Kg/1CU - never installed anywhere.
- ADDED R/W, per-repo (Main relays 00:42:35/00:42:40), each ssh-keygen-validated, piped from file, fingerprint-verified on-page:
  - mega27-09a-amp-design-discovery: `paper-build-mega27-09a-amp-design-discovery` SHA256:NPwptItH2q52f1nQpOkhdYLNwVVdTEoDQjkLaR3YmOk
  - mega27-09b-peptide-hla-cpp: `paper-build-mega27-09b-peptide-hla-cpp` SHA256:k4DFAOZX2aF9/YCsqpxEee0lc4GHcfoY5ct2tM1w4jE
  - mega27-09c-peptide-solubility-anticancer: `paper-build-mega27-09c-peptide-solubility-anticancer` SHA256:JgE+1qzw/luk/Vuh4UJv0tzlOY6noZ1h8Cg/kB1C9fo
  - mega27-11a-protein-redesign-1-3: `paper-build-mega27-11a-protein-redesign-1-3` SHA256:y6cSFZVPULv8UecOFoBaDZCWKljWoabzDEy+96INTMY
  - mega27-11b-protein-redesign-4-5: `paper-build-mega27-11b-protein-redesign-4-5` SHA256:y0mOOdzFGmepFpFLEDyINmocB1YpbOuu8bSZL58SSqE
  - weird-02-quantum-compass: `lane29-paper-02` SHA256:f8kGJL2KfogLADSdtQOSHbRTMUY1IuJ0+oJTe2d+qRU
  - weird-09-radiation-toolkit: `lane29-paper-09` SHA256:t9r2pVMGMNe5cDtYSLTMgXHQy4U1SKMeiY7LzdIavLI
  - weird-11-ai-evolved-biofactories: `lane29-paper-11` SHA256:nLIfuLq4AKpvba081xYctXdhmRqWHabGu+tU7F0Sb1s
- IC readback resolved (Main 00:43:04): mega27-25-interstitial-cystitis-biomarkers remote is EMPTY - ls-remote 0 refs (exit 0) + fresh clone warns empty. No e9a5ba5, no ae0635f on the remote; the lane's pushes have not landed. (Note: my 00:36 report said empty x3; no e9a5ba5 was ever read by me.)

## 2026-09-27 00:51 IST — IC repo recreated + fresh builder key (Main 00:48:43 / 00:50:56 / 00:51:19)
- mega27-25-interstitial-cystitis-biomarkers: repo 404'd persistently for the lane despite valid auth (empty repo, 0 refs verified x3 + clone). DELETED (verified empty first - nothing lost) and RE-CREATED private/empty under the same name; ls-remote reachable (exit 0, 0 refs).
- Original key body re-add failed "Key is already in use" (deleted repo's key record lingering GitHub-side); lane generated a FRESH keypair per Main 00:51:19. ADDED R/W: `mega27-25-interstitial-cystitis-builder-20260927b` SHA256:fn2A0E1orcLYOajrmjBGGoFFaeohwWYmYbc+9SAHagc (ssh-keygen-validated vs Main's stated fingerprint, piped from file, verified on-page: exactly 1 deploy key, Never used, Read/write). Lane pushes ae0635f next.
- Tonight's truth rule (Main 00:50:56): never trust a push error or a single ls-remote; only key-ops readbacks or triple ls-remote over minutes count. Lane-29's "failed" pushes (W02 1a001e3, W09 e20f718, W11 4ab1470) actually landed.

## 2026-09-27 00:56 IST — biomarkers push duty migrated to orchestrator (Main 00:55:08 decision)
CAUSE: lane's git-transport 404s persisted on fresh repo + fresh key with correct auth (key last-used flipped). Transport test: fresh deploy key from MY sandbox read IC fine (exit 0) -> lane-side IP/transport is the broken leg; my account-key transport provably works. Lane now hands bundles via Main; I push.
PUSHED this batch (each: git bundle verify OK, head matched Main's stated prefix, live-remote-empty check, fetch-then-push, ls-remote readback exact match; no force anywhere):
- mega27-25-biomarkers-underserved-diseases (shared): 343705c888cf -> 2960853b02f9c405d952063ff8a1612d6f9921d1 (FF; 2 commits: d228455 "Pin committed disease-specific paths and hashes for repo split", 2960853 "Anchor migration hashes to committed tree, not dirty worktree")
- mega27-25-interstitial-cystitis-biomarkers: ae0635f8c7d819de3582c6c91f787527607e0045 (first content)
- mega27-25-endometriosis-biomarkers: 09aa7acfa6e7c0bbbbce58c6bd52f1eb49579d78 (first content)
- mega27-25-pcos-biomarkers: 54ae18ab15d973442f8d591456f240d9961560ee (first content)
- mega27-25-leishmaniasis-biomarkers: 4235a6d6cf58f9485f66e120f53a79da726a1264 (first content)
- mega27-25-preeclampsia-biomarkers: ba47690cb59cc1b4e04d9dedfe0c94560f762754 (first content)
- mega27-25-long-covid-biomarkers: ddfce77acb38a7691db655cb7a3ad4b8fecc788e (first content)
- mega27-25-me-cfs-biomarkers: a03275bf700627a0f2e7a75ecd44cb031871b713 (first content)
- mega27-25-fibromyalgia-biomarkers: a611a1f413aa6d3c0b7f3cea026799db25c4884b (first content)
Skipped per Main: chagas bundle (shared-main snapshot only), PPD bundle (dafbe79 already remote-confirmed). All 10 disease repos now have content. NOTE: `orchestrator-ic-transport-test` deploy key (SHA256:QkadDYAEucPXsp5VGEAVvyK9oHEN2rKliv4jwYiCHHs) remains on the IC repo from the transport test - removal pending Main's explicit instruction.

## 2026-09-27 00:58 IST — transport-test key removed + chagas migration closed
- REVOKED on mega27-25-interstitial-cystitis-biomarkers (Main's explicit 00:57:47 instruction): `orchestrator-ic-transport-test` SHA256:QkadDYAEucPXsp5VGEAVvyK9oHEN2rKliv4jwYiCHHs. Verified absent on-page; lane's 20260927b key intact. Local keypair deleted from orchestrator sandbox.
- CHAGAS: standalone repo was empty; lane bundle was only a shared-main snapshot. Fetched builder-25-chagas branch from the shared repo and pushed to mega27-25-chagas-biomarkers main: 536a904664f68965352f45401204b335d89d982f "Services 38-40: NCBI Datasets v2 host-gene reports, IntAct second-source interactions, WikiData entity resolution - DISTINCT gate 40/40 MET" (newer than the e4644eb Main cited). ls-remote verified. ALL 10 disease repos now genuinely migrated.
- Bundle relay is the standing route for the biomarkers lane until its transport recovers (Main 00:57:47).

## 2026-09-27 00:58 IST — PPD update bundle pushed (bundle-relay route)
mega27-25-postpartum-depression-biomarkers: dafbe79e8407 -> e67c3de7a80d7e31493c767d91a96879d143782e "Preserve broad versus explicit euthymic source labels in PPD audit" (bundle verified complete history; FF vs live remote dafbe79; 1 commit; label-integrity correction per lane: GSE45603's 32 controls = 27 explicitly euthymic + 5 only 'condition: control'; no expression results altered). ls-remote verified.

## 2026-09-27 01:10 IST — chagas standalone builder key added
ADDED R/W on mega27-25-chagas-biomarkers (relayed by Main 01:09:46): `builder-25-chagas-standalone` SHA256:EbB4NNjrVcuRZUpj6Xus/YtkrYeR7TA0Bz4qhs+MmdE. On-page fingerprint matches ssh-keygen -lf of the relayed pubkey exactly. Existing mega27-25-chagas-builder-20260927 (SHA256:TU4fu4...) left intact.

## 2026-09-27 01:51 IST — chestnut + PPD update bundles pushed (bundle-relay route)
- mega27-24-blight-resistant-chestnut: 3dda31a9e45a -> c55ca71b3e525d3db8ea60cc31c1b9b1c8be3c73 "Audit independent chestnut cohort metadata and accession mismatch" (bundle verified complete history; FF vs live remote 3dda31a; 1 commit; metadata-only 2009-cohort accession/species mismatch screen, lane reports 4 tests pass). Also readback for Main: lane C's earlier pushes DID land despite 'Repository not found' errors - 7dea7d3 -> 88db27b -> 3dda31a all on main; 88db27b was created after a failed audit test per lane C and is flagged as not-valid content (still in history, FF-only).
- mega27-25-postpartum-depression-biomarkers: e67c3de7a80d -> 68a688483260e51e648620fc3621d50c1534ff2a "Measure source-control definition sensitivity in exposed PPD cohort" (bundle verified; FF vs live remote; 1 commit; label-sensitivity run: 16v27 strict contrast, 601/9,744 effects reverse sign mostly near-zero, no gene passes BH-FDR in either contrast, min q 0.368 broad / 0.708 strict).

## 2026-09-27 01:51 IST — chestnut follow-up bundle pushed
mega27-24-blight-resistant-chestnut: c55ca71b3e52 -> ef58a9869b6c27d0bd17264be11a6caec012f6e4 "Cross-check 2009 canker discrepancy against deposited experiment titles" (bundle verified complete history, contains c55ca71; FF vs live remote; 1 commit; firmer source check: ENA experiment titles call SRX001804 C. mollissima and SRX001799 C. dentata, reversing the paper's literal paragraph order). ls-remote verified.

## 2026-09-27 02:32 IST — rice seed-bank replay bundle pushed
mega27-24-rice-oral-vaccine: ae913d90d84c -> 72ae19deb578b691cdd00372ad1eafdb0f686586 "Replay 477 shared seed-bank proteomics counts from original supplement" (bundle verified complete history; FF vs live remote - lane had pushed ae913d90 itself past scaffold 7b9bc1c; 1 commit; MucoRice 51A Additional file 3 replay, 477 rows, raw PSM R2 0.9815 vs authors' 0.982, log1p R2 0.852 scale sensitivity, lane reports 7 tests pass). ls-remote verified.

## 2026-09-27 02:51 IST — PPD bundle #3 pushed
mega27-25-postpartum-depression-biomarkers: 68a688483260 -> baa92b3fc3e6e06567ebfae38abde368424393c3 "Rebuild PPD exposed matrix exactly from hashed GEO raw sources" (bundle verified complete history; FF vs live remote; 1 commit; reproducibility rebuild: GSE45603 series matrix + GPL10558 annotation re-fetched hash-pinned, rebuild_gse45603.py reconstructs 9,744-gene matrix exactly, lane reports 12 tests pass. Documented caveat: historical probe selection uses all 210 samples before column selection, not fold-isolated for a future classifier). ls-remote verified.

## 2026-09-27 03:16 IST — salmon reciprocal-FC bundle pushed (target corrected)
mega27-24-aquadvantage-salmon: a4168d676f62 -> 28aff13ef6185212d7bb40aa07b02689948351c3 "Resolve salmon supplement classification to reciprocal FC cutoff" (bundle verified complete history; FF vs live remote; 1 commit; 17 author-green rows failing printed FC<=0.66 all pass exact reciprocal 2/3; q<0.05 + FC>=1.5 or <=2/3 reproduces all S1-S3 green/non-green rows, zero disagreements; lane reports 3 tests pass). NOTE: Main's relay said "push to the rice repo" but bundle ancestry is the salmon scaffold 3b919b7 - rice push would have required a forbidden force-push; pushed to salmon (clean FF) and flagged to Main. ls-remote verified.

## 2026-09-27 03:51 IST — PPD update 4 bundle pushed
mega27-25-postpartum-depression-biomarkers: baa92b3fc3e6 -> 6368d9b18efe101b49e61d73d644d155caafa439 "Qualify PPD sign flips and distinguish published prediction task" (bundle verified complete history; FF vs live remote; 1 commit; sensitivity correction: of 601 nominal sign reversals only 2 have |Hedges g|>=0.1 in both control scopes, 0 at >=0.2 - 6.17% headline is mostly near-zero crossing; new code/tests 12 pass; prior-art note Mehta 2014's 88% is a different predictive task, not same-task benchmark). ls-remote verified.

## 2026-09-27 04:09 IST — ADVISORY: average_precision tie-handling flaw (item-27)
Item-27 found a metric flaw in its shared helper average_precision: ties are credited at within-tie position instead of threshold-grouped. On a tied fixture sklearn gives 0.8333 vs the helper's 0.5. Item-27 is fixing its own copy and rerunning pinned evals. ADVISORY to all lanes: any lane with a custom AP implementation must check tie-handling before trusting exact APs; validate against sklearn.metrics.average_precision_score on a tied fixture before reporting AP numbers.

## 2026-09-27 04:47 IST — rice harmonization bundle pushed
mega27-24-rice-oral-vaccine: 72ae19deb578 -> d68383c3a1350f8e515e718da2c7cb0a0e808484 "Fix metabolite dedupe protocol; cross-study pooling ruled not defensible" (bundle verified complete history; FF vs live remote; 1 commit; dedupe/normalization protocol in code, MTBLS437 212->104 analytes, 288 31->31, 801 split 205->62/splitless 706->199; verdict: cross-study quantitative pooling not defensible, allowed use = analyte-presence overlap + within-study contrasts; lane reports 8 tests pass). ls-remote verified.

## 2026-09-27 04:51 IST — PPD update 5 bundle pushed
mega27-25-postpartum-depression-biomarkers: 6368d9b18efe -> b72a6776d11eb7cf5453a51bb4930506fe3fa2e3 "Document public-access and assay hold on 2026 PPD PBMC cohort" (bundle verified complete history; FF vs live remote; 1 commit; public-data hold: Sept 16 PBMC RNA-seq paper claims PRJNA1456230 but NCBI/ENA return zero records; reviewer-token link deliberately unused; assay/task mismatch documented; prior art not validation). ls-remote verified.

## 2026-09-27 05:33 IST — rice stability bundle pushed
mega27-24-rice-oral-vaccine: d68383c3a135 -> 2f5666f73e7a4903b7adcc243a2fcb76932d0172 "Audit identifier-deduped seed metabolome stability against label controls" (bundle ref HEAD, complete history verified; FF vs live remote; 1 commit; MTBLS437 post-outcome stability replay after fixed dedupe: 95/104 analytes retain direction through all nine leave-one-out deletions; rotated-label controls include one exceeding observed so NO signature claim; lane reports 9/9 tests pass). ls-remote verified.

## 2026-09-27 05:52 IST — PPD update 6 bundle pushed
mega27-25-postpartum-depression-biomarkers: b72a6776d11e -> bb0f4873537d07a5ffa38fd1894f3e1e2d120303 "Screen published PPD comparators without conflating tasks or access" (bundle verified complete history; FF vs live remote; 1 commit; six comparator papers classified by task/assay alignment; no verified public independent same-task holdout found - absence not proved; standing warning: never cite Mehta 2014's 88% as a same-task comparator). ls-remote verified.

## 2026-09-27 06:17 IST — salmon read-inventory bundle pushed
mega27-24-aquadvantage-salmon: 28aff13ef618 -> 55d6dae25fd3fc469726577f6ac2b433a0962897 "Reconcile paired-end read units and size the salmon RNA-seq payload" (bundle ref HEAD, complete history verified; FF vs live remote; 1 commit; ENA/Table-1 unit discrepancy closed: article counts mates, ENA counts paired fragments, exact 2x over 18/18 runs; totals pinned; metadata result, not biological). ls-remote verified.

## 2026-09-27 06:51 IST — IC script-restore bundle pushed + migration omission register
mega27-25-interstitial-cystitis-biomarkers: ae0635f8c7d8 -> 8a18630f53c9da2215837df3f13092a0536b2446 "Restore six IC analysis scripts omitted in migration" (bundle verified complete history; FF vs live remote; 1 commit; six ic_* analysis scripts the split heuristic missed, copied byte-for-byte from shared source 2960853; lane reports 19 common tests pass; end-to-end rerun NOT claimed). ls-remote verified.
MIGRATION OMISSION REGISTER (same split-heuristic gap, restore bundles to follow from the lane): preeclampsia 17 scripts, leishmaniasis 4, long-covid 3, ME/CFS 4, endometriosis 3, fibromyalgia 1.

## 2026-09-27 06:52 IST — script-restore batches 2+3 pushed (6 repos)
All bundles verified complete history, FF vs live remotes, ls-remote readbacks exact; scripts copied byte-for-byte from shared source 2960853; lane reports 19 common tests pass each; end-to-end reruns NOT claimed; builder branches untouched.
- mega27-25-preeclampsia-biomarkers: ba47690cb59c -> e836e892710d8765b4cd5787638e8ec67fef8dd6 "Restore preeclampsia analysis scripts omitted in migration" (17 pe_ scripts)
- mega27-25-leishmaniasis-biomarkers: 4235a6d6cf58 -> 5edbf841d8fbdb7cccc3b8f2b038a04ae73e431e "Restore leishmaniasis analysis scripts omitted in migration" (4 leish_ scripts)
- mega27-25-long-covid-biomarkers: ddfce77acb38 -> 112488703f3c74a3da72e5d5f8d0e84a15d8d93d "Restore long-covid analysis scripts omitted in migration" (3 longcovid_ scripts)
- mega27-25-me-cfs-biomarkers: a03275bf7006 -> a6dde4b6f805edb0f44d0882dd668e6af739f0ab "Restore me-cfs analysis scripts omitted in migration" (4 mecfs_ scripts)
- mega27-25-endometriosis-biomarkers: 09aa7acfa6e7 -> b180992830880c7e7a9e498023d3ca95acdfc5ad "Restore endometriosis analysis scripts omitted in migration" (3 endo_ scripts)
- mega27-25-fibromyalgia-biomarkers: a611a1f413aa -> 392a516c271b6962a64fe6466e24ec0546f58b11 "Restore fibromyalgia analysis scripts omitted in migration" (fibro_p43_neutrophils.py)
Omission register from 06:51 entry now fully closed: IC (06:51) + these 6 = all 7 affected repos restored.

## 2026-09-27 06:53 IST — dependency-repair batches 4+5 pushed (6 pushes + 1 redundant)
All bundles verified complete history, FF vs live remotes, ls-remote readbacks exact. Content: disease-named committed result files used by the restored scripts + disease-filtered accession manifests. Caveats carried: restores committed results, not all raw data; end-to-end replay NOT established; named-file presence is not rerun validation.
- mega27-25-interstitial-cystitis-biomarkers: 8a18630f53c9 -> 9cb1b97859650c23a6ac10051fbbc5292a4f6059 "Restore disease-scoped result dependencies and manifest"
- mega27-25-endometriosis-biomarkers: b18099283088 -> 56c81c8b509513b05cb8674296415eebdaea3da5 "Restore disease-scoped result dependencies and manifest"
- mega27-25-leishmaniasis-biomarkers: 5edbf841d8fb -> 29f71974ea101873aaf24ca792f548c5a895482f "Restore disease-scoped result dependencies and manifest"
- mega27-25-preeclampsia-biomarkers: e836e892710d -> f938f61fde6aa70ca8e160718444b67314d07122 "Restore disease-scoped result dependencies and manifest"
- mega27-25-long-covid-biomarkers: 112488703f3c -> 806b4669a621ee552732f80df64df379a29fc6cb "Restore committed result and source dependencies omitted at split" (3 scripts, 8 named results, 1 Excel input)
- mega27-25-me-cfs-biomarkers: a6dde4b6f805 -> 38148094157183be4b041b2fa82a2a4ae8e9d85e "Restore disease-scoped result dependencies and manifest" (4 scripts, 18 results, disease manifest)
- mega27-25-fibromyalgia-biomarkers: batch-5 bundle was byte-identical to batch 2's (same head 392a516c271b6962a64fe6466e24ec0546f58b11 already live) - REDUNDANT, no push, no change.

## 2026-09-27 07:03 IST — chestnut run-route bundle pushed
mega27-24-blight-resistant-chestnut: ef58a9869b6c -> 8c984dd270c08a2151099f5ddd5ce96e982c7f24 "Map chestnut infection experiments to indexed run-file route" (bundle verified complete history; FF vs live remote; 1 commit; CRA006690 run route: 15 CRX mapped one-to-one to CRR464767-781 via SeqOut index, 74.6GB advertised; first CNCB file HEAD-verified 200; retrieval lead only, no payloads fetched; lane reports 5/5 tests). ls-remote verified.

## 2026-09-27 07:52 IST — IC reproduction upgrade bundle pushed
mega27-25-interstitial-cystitis-biomarkers: 9cb1b9785965 -> 9b582fb4a76a8317cbf9f198110d649ce4b56cd9 "Replay IC historical sensitivities with pinned GEO source matrices" (bundle verified complete history; FF vs live remote; 1 commit; historical GSE621/GSE11783 processed matrices + GEO raw series files added, fresh GETs matched both raw SHA-256; three sensitivity scripts now REPLAY prior numerical results from the standalone repo: 683/3,556 sign changes, donor |g| shift 0.056158 no sign change, 43/50 GSE57560 signs p=0.0469 FAILS the 0.025 threshold - all honest). ls-remote verified.

## 2026-09-27 08:33 IST — rice label-sensitivity bundle pushed
mega27-24-rice-oral-vaccine: 2f5666f73e7a -> d87c5a81975c55614cd99414bba37423a99e0de7 "Enumerate rice metabolome label sensitivity without inferential claims" (bundle verified complete history; FF vs live remote; 1 commit; MTBLS437 9-sample stability control expanded to all 126 group assignments: observed 95/104, max 97, median 55; descriptive post-outcome sensitivity, NO permutation claim). ls-remote verified.

## 2026-09-27 08:44 IST — banana scope ruling executed (user-confirmed)
User confirmed via Main (WhatsApp 08:43, verbatim "Ok do it the two things required from me"): archive the out-of-scope design line and make the published-design variability line main on mega27-24-banana-vaccine-enviropig.
- ARCHIVE: refs/heads/archive/out-of-scope-designs = a3ef09549b89dcb365d25431712b41d13d508eb9 (prior main, epitope-conservation discovery line, preserved in full).
- MAIN: moved to 2e6885a528608a7b722f8fc9a65d75d76ff8d363 "Screen published oral-vaccine observations against registered numeric endpoint" as a deliberate NON-fast-forward replacement (histories unrelated by root; NOT a merge - no out-of-scope material folded in). Bundle verified complete history.
- ls-remote readback: main = 2e6885a528..., archive/out-of-scope-designs = a3ef09549b..., HEAD -> main.

## 2026-09-27 08:52 IST — IC probe-level reproducibility correction pushed
mega27-25-interstitial-cystitis-biomarkers: 9b582fb4a76a -> f9519903474d41a0849ef8d550474017302452a6 "Verify IC cached gene matrices against hashed GEO probe sources" (bundle verified complete history; FF vs live remote; 1 commit; fresh GEO GETs matched GPL262/GPL570 annotation hashes; standalone reconstruction exactly matched all GSE621 cached gene values (3,556 x 14 used GSMs) and GSE11783's 21,594 x 16 cache to max abs 5.55e-7 float32 rounding; 2 new tests pass, 19 common tests pass. Lane's honest framing: narrows the cached-matrix hold for old descriptive inputs ONLY - source-label contamination and donor independence NOT narrowed; IC sensitivity still FAILS its preregistered p=0.025 sign threshold (observed 0.0469). No gate credit). ls-remote verified.

## 2026-09-27 09:23 IST — banana retention two-stage bundle pushed
mega27-24-banana-vaccine-enviropig: 2e6885a52860 -> 3f2948bc090c3eddf93d1e4e82090cadafe63bad "Pin oral-vaccine lettuce retention denominators after direction consult" (bundle verified complete history; FF vs live remote; 1 commit; source-grounded two-stage denominator distinction from original lettuce oral-vaccine paper PMC3088802: >=90% antigen loss fresh->freeze-dried, then 95-98% retention of remaining powder/tablet content after a year at room temperature; ~2.3 ug/tablet, 3 vs 10 technical repeats; NOT digestion survival, no predictor, no gate credit). ls-remote verified; archive/out-of-scope-designs untouched at a3ef095.

## 2026-09-27 09:52 IST — PPD update 7 bundle pushed
mega27-25-postpartum-depression-biomarkers: bb0f4873537d -> 6c98d3f7b7cb67dec6f494412ca3c31a539527ed "Check GSE290313 published supplement without inventing donor keys" (bundle verified complete history; FF vs live remote; 1 commit; GSE290313 donor-map screen: publisher supplement has aggregate Table S3 (188 postpartum-sampled women) but no GSM-to-person key; GEO/BioSample spot-check shows no common donor ID; conclusion: 119 selected libraries are specimen records, not 119 proven people; GSE290313 CANNOT be promoted to patient-independent transfer validation; audit tests 9 passed; no new biomarker/benchmark/judge credit). ls-remote verified.

## 2026-09-27 10:37 IST — judge-floor bundles pushed (5 repos, after workspace outage + re-attach)
All bundles verified complete history, FF vs live remotes, ls-remote readbacks exact. Content: judge-ledger updates to one owner-provided round per her 10:00:07 rule change (relayed by Main); earlier agent-initiated consults preserved, not auto-counted.
- mega27-25-postpartum-depression-biomarkers: 6c98d3f7b7cb -> 4420183da901c852b6160bbee14d3b0ec1a723c7 "Update PPD judge gate to one owner-provided round pending evidence"
- mega27-24-rice-oral-vaccine: d87c5a81975c -> 97cdfbcbbc404b22351af0aa365c6a48bc9ed7f3 "Set user-provided judge review floor to one round"
- mega27-24-aquadvantage-salmon: 55d6dae25fd3 -> 8247f0ac80ec58d124ad784d139b5f6d1e71129d "Set user-provided judge review floor to one round"
- mega27-24-blight-resistant-chestnut: 8c984dd270c0 -> 24a90b1e10c235afb2a814719908124fc9f2459b "Set user-provided judge review floor to one round"
- mega27-24-banana-vaccine-enviropig: 3f2948bc090c -> 5641a45c404d70d1bf7a245866d8614692ab6026 "Set user-provided judge review floor to one round"
INCIDENT NOTE: orchestrator workspace shell errored 10:01-10:35 (every command interrupted); the 5 newest bundle attachments were lost with the sandbox write, older files intact. Main re-attached all 5; processed immediately on recovery. An interim status message sent during the outage did not reach Main.

## Bundle relay - salmon three-temperature (Sep 27, 2026, ~10:49 IST)
- Repo: mega27-24-aquadvantage-salmon
- Bundle: salmon-three-temperature-35f25d06.bundle (verified: complete history, head 1f2300477bfd9e36447b8aee0d661d5ee55e9f5b)
- Pre-push live remote: 8247f0ac80ec58d124ad784d139b5f6d1e71129d (ancestry FF confirmed)
- Push: 8247f0a..1f23004 main
- ls-remote readback: 1f2300477bfd9e36447b8aee0d661d5ee55e9f5b refs/heads/main
- Commit: "Check three-temperature transcript summary overlap and source arithmetic"

## Bundle relay - shared repo no-author (Sep 27, 2026, ~11:17 IST)
- Repo: mega27-25-biomarkers-underserved-diseases
- Bundle: shared-noauthor-9e9f4792.bundle (verified: requires prerequisite 2960853b02f9c405d952063ff8a1612d6f9921d1, head ac814070233a680fec668c38adb0f9025080bccc)
- Pre-push live remote main: 2960853b02f9c405d952063ff8a1612d6f9921d1 (= required ancestor, no intervening change; ancestry FF confirmed)
- Push: 2960853..ac81407 main (1 commit)
- ls-remote readback: ac814070233a680fec668c38adb0f9025080bccc refs/heads/main
- Commit: "Remove program byline and author metadata from working papers"

## Bundle relay - shared audit51 (Sep 27, 2026, ~11:30 IST)
- Repo: mega27-25-biomarkers-underserved-diseases
- Bundle: shared-audit51-22c217eb.bundle (ref HEAD; requires prerequisite ac814070233a680fec668c38adb0f9025080bccc = live main; FF confirmed)
- Push: ac81407..92e76a8 main (1 commit)
- ls-remote readback: 92e76a8d5ab324a5b4705c2b6e9794a5acfb9ef2 refs/heads/main
- Commit: "Extend shared biomarker working paper with PPD source audit and sole Udita byline"
- paper/manuscript.pdf at 92e76a8 = 51 pages (blob 8bbf1d53560b251c3a29af80762d2a697c257e8d). manuscript-times.pdf remains the older 49pp snapshot - not for distribution.

## Bundle relay - shared reframe (Sep 27, 2026, ~11:30 IST)
- Repo: mega27-25-biomarkers-underserved-diseases
- Bundle: shared-reframe-8920a433.bundle (ref HEAD; requires 92e76a8d5ab324a5b4705c2b6e9794a5acfb9ef2 = live main; FF confirmed)
- Push: 92e76a8..be7eacd main (1 commit)
- ls-remote readback: be7eacd080f1f75efbef4f604883df8eaedaa50b refs/heads/main
- Commit: "Lead shared biomarker paper with audited evidence and bounded sign transport"
- paper/manuscript.pdf at be7eacd = 51 pages (blob 369ed6e740aa6981d79efaeb52c158e5aa4b24ed). Title/abstract reframe per her 10:35 positive-spine rule (relayed via Main).

## Bundle relay batch (Sep 27, 2026, ~12:16-12:17 IST) - 8 bundles, all FF-verified, exact readbacks
- mega27-27-isef-bioinf-derived-tools: 4d037188..ae9f35ba (4 bundles in chain: 9d270d85 verdict-lock, e5b6a3fc DGR v2 protocol freeze, e11c57e7 DGR cohort leads, ae9f35ba comparator-leakage preempt). Readback ae9f35ba91baaf89d5966d00bfb0952f5ab846a4. Repo stays PRIVATE (HMDD license blocker).
- atlas-ai: ea2755cd..3a410986 (4 commits, Claire owner-interview module). Readback 3a410986784fecb1f14fd11c49d2664ba747cba2. Bundle sha256 verified e11e1cd0.
- sugarcode-ai: 1ac902e5..1ecddeb7 (1 commit, zero-stub gate strict). Readback 1ecddeb71e741f3ab6bea08bb04c881cae7dc56f. Bundle sha256 verified 070b0fd3.
- mega27-24-rice-oral-vaccine: 97cdfbcb..24b8031b (three-lot expression audit). Readback 24b8031b79ea0181d244c7243020639cdc0ae5d0.
- mega27-25-postpartum-depression-biomarkers: 4420183d..702db060 (GSE45603 comparator screen). Readback 702db060abf4427d3907841081ee132b83167af3.
- mega27-25-biomarkers-underserved-diseases: be7eacd0..09a48709 (2 bundles: 6e3604d8 owner-verdict archive, 09a48709 manifest-units reconcile). Readback 09a48709a6a715e65d7ee204d02a25f090d4b498.

## Visibility flips to PUBLIC (Sep 27, 2026, 11:36-12:12 IST) - user WhatsApp directive 11:34 "MAKE ALL THESE REPOS PUBLIC" + Main expanded scope 11:38
- 77 repos flipped + verified via anonymous-200 checks (list in orchestrator state /tmp/done.txt). GitHub sudo email-code re-auth completed 11:36.
- SKIPPED/HELD: mega27-27-isef-bioinf-derived-tools (HMDD academic-use-only rows - license blocker, stays PRIVATE per Main 11:38:40), mega27-18-mirna-research (miRTarBase fetch script + OmniPath mirnatarget dump - held for her license call).
- EXCLUDED: atlas-ai/sugarcode-ai/meemee (product, already public), fairycore-portfolio (non-science), mega27-01-sugarcode-realdata-validation (sugarcode-branded).
- Secret scans (HEAD + recent history, ghp_/gho_/github_pat_/sk-/AKIA/PRIVATE KEY/password=/token=): zero real hits; FPs were peptide/UniProt sequence substrings, python token= vars, DRAMP rows. License scans: FPs were NCBI DBHMDD* accessions, DrugBank citations, public GEO/her2st/MyChem data.
- mega27-27-isef-bioinf-derived-tools: ae9f35ba..7e611be9 (5th item-27 bundle, "Pin supplementary source discrepancy and group-II decoy lead"). Readback 7e611be9bf91e333e41e9393075a2f6078b83c89. Repo stays PRIVATE.
- atlas-ai: 3a410986..21e0d984 ("Add actor-scoped persistent owner decision journal", bundle sha256 70d974829171a45787ac6f0c22c37f4fbb16a7d645ab995b4e1c6e461669cf7a verified). Readback 21e0d9842c45328f701679165fe3e78ed0974066.
- meemee: e4865b2..6b8c4442 ("Normalize monitor deadlines and require positive fire budgets", bundle sha256 1dd5c61f8da1348422f9a88da04f696cb062dcf10c02f3375c917cec146e7712 verified). Readback 6b8c4442d4f25ba238e78ea9444b9fecdbccaeba. Repo STAYS PRIVATE (push only, no flip).
- atlas-ai: 21e0d984..ce9ba56e ("Migrate durable Claire interview and journal tables", bundle sha256 64bdd47d951dd0d5ed8c3410bf5295f3c389f03491d9b4a239d8ad20fd64a3e7 verified). Readback ce9ba56e6232c4a37b1cdfd5abe9c9e8b2a1623b.
- sugarcode-ai: 1ecddeb7..24bd2fdc ("Reject invalid codon designs and impossible forbidden motifs", bundle sha256 e105b802d966b80f17ae7c76ba651d83d0fc2654d6bc11d76e39e9d777dab6a5 verified). Readback 24bd2fdc040a4991208a49555f1e59d74cb6db64.
- sugarcode-ai: 24bd2fdc..1ccbd030 ("Count zero-reference codons correctly in CAI", bundle sha256 5c36fbbceff641dc5d186f2a1f433e99d65370be7c9e89b853e28ab5f0555f40 verified). Readback 1ccbd0305cd9b639b06324fa136654d686483b7a.
- atlas-ai: ce9ba56e..6317d485 ("Connect Claire to read-only source-backed opportunity triage", bundle sha256 114e4c23df4b52d5e814529d4c294ceab099000589b5548bcb37b9f4747dc8cd verified). Readback 6317d485d872335d3ed94cea6f8f427226f909b4.
- atlas-ai: 6317d485..6437de54 ("Expose Claire interview and opportunity review in workbench", bundle sha256 289aab845b99cc1ff673cb92f8441ffc54b5b61b58957fd43d70dd2aa12ea445 verified). Readback 6437de54178eb9771aa4d1da36a67b0d7af1dcfc.
- FLIP: mega27-10-dl-diagnosis-suite -> PUBLIC 12:35 IST, anon-200 verified. Secret scan CLEAN; license hit was base64-embedded PNG noise in properties_profile.html (FP).
- FLIP: mega27-02-virtual-cell -> PUBLIC 12:39 IST, anon-200 verified. Secret scan CLEAN; license hits were peptide-sequence substrings in E. coli GenBank data, base64 PNG in notebook, PDF binary noise (all FP).
- FLIP: mega27-05-yeast-metabolic-twin -> PUBLIC 12:39 IST, anon-200 verified. Secret scan CLEAN; license hit was HMDD-as-peptide-substring in swissprot.tsv sequences (FP; UniProt is CC BY 4.0).
- mega27-27-isef-bioinf-derived-tools: 7e611be9..bfffd649 ("Freeze four review-responsive lane protocol drafts and stop rules" - LoopShift/miR-Time/CellPerturb/PocketShift plans, not measurements). Readback bfffd6496eb23771e3079bb232bcf493e8c84f83. Repo stays PRIVATE.
- atlas-ai: 03135800..5957c755 ("Verify Claire workbench in mocked Chromium flow", bundle sha256 38a48c0359db939b7252e4dfe83195aaf31f7e25c81db4af00a9a7ad27fdf226 verified). Readback 5957c755cea3c382b285ada30d314f4f1839b6c3.
- atlas-ai: 5957c755..313309be ("Review stored social signals without external effects" - tenant-scoped read-only review cards, no external effects, bundle sha256 29b8c65522beb37f3e1970c778d482603c6aeb6e6157bfdd0392829d2654c6bf verified). Readback 313309be2a960a84b909d1834c3046f884e21a7e.
- FLIP: enzyme-mining-pollution -> PUBLIC 12:44 IST, anon-200 verified. Secret scan CLEAN; license hits were HMDD-as-peptide-substring in FASTA/.faa sequence lines (FP; MGnify is public EBI data).
- FLIP: weird-09-radiation-toolkit -> PUBLIC 12:46 IST, anon-200 verified. Secret scan CLEAN; license hits were HMDD-as-peptide-substring in public proteome .faa files (FP).
- FLIP: mega27-08-phage-design -> PUBLIC 12:51 IST, anon-200 verified. Secret scan CLEAN; license hits were HMDD-as-peptide-substring in phage GenBank translations + a DrugBank xref inside a public UniProtKB entry JSON (FP).
- mega27-25-interstitial-cystitis-biomarkers: f9519903..8c883aa3 ("Adjudicate IC paired lesion source against original 25-person paper" - GSE238208 2023 iScience 25-paired-patient cohort, not GSE28242; cohort-level only; P25 still fails 31/46, emp p=0.0679). Readback 8c883aa39907de13c7e52b2a80086ad657b8551a.
- mega27-25-biomarkers-underserved-diseases: 09a48709..5b481a10 ("Correct IC clinical-adjudication target in shared audit"). Readback 5b481a10e41d2f927801a9ec4c4a843810f4fcd5.
- mega27-27-isef-bioinf-derived-tools: bfffd649..f76a58bf ("Add four source-grounded separate paper seeds without final claims" - LoopShift/miR-Time/CellPerturb/PocketShift). Readback f76a58bf3f6a128ca8b8ab136d5b6e5f9a3947f7. Repo stays PRIVATE.
- mega27-27-isef-bioinf-derived-tools: f76a58bf..0e027c46 (five provisional PDF draft builds, all lanes seeded, DRAFT-marked, gates 0/5 OPEN). Readback 0e027c4646190819169f1463e276970104c337fe. Repo stays PRIVATE.
- mega27-09c-peptide-solubility-anticancer: fed185f..df54e3c ("Add DeepSol CNN training script from lane handoff package" - runs/train_deepsol.py from Drive deepsol_handoff_v4.zip/deepsol_fix2.zip, per Main instruction; checkpoint deliberately not committed, run in flight). Readback df54e3c0dd3cf2111829a42b2630338431056b40.
- FLIP: science-program-ledger -> PUBLIC 13:09 IST, anon-200 verified. Secret scan: 776 AKIA hits all digit-free peptide substrings (FP), 6 token-shaped hits all on one KEYS.md line quoting the scan pattern list itself (FP), zero BEGIN PRIVATE KEY. License hits: KEYS.md self-references + GenBank peptide substrings (FP). FLIP PROGRAM COMPLETE: all 85 scanned repos public.
- mega27-27-isef-bioinf-derived-tools: 0e027c46..d0cd94f4 ("Record clean 52-test DGR engineering checkpoint"). Readback d0cd94f4227b4ed6a3123957550b15d958d93650. Repo stays PRIVATE.
- DECISION (hers, relayed by Main 13:12 IST): mega27-18-mirna-research stays PRIVATE, keep building. License-hold resolved - NO flip. (mega27-27-isef stays PRIVATE per HMDD block; mega27-01-sugarcode-realdata-validation exclusion kept as-is per Main.)
- mega27-27-isef-bioinf-derived-tools: d0cd94f4..3912f4c8 (two draft-PDF precision corrections from item-27 agent). Readback 3912f4c80fb0f7d9b86868e951720ecf224a3ff5. Repo stays PRIVATE.
- mega27-27-isef-bioinf-derived-tools: 3912f4c8..1de89b7b (full engineering test suite result from item-27 agent). Readback 1de89b7ba93a1c55270ac3db5c41f2fb8f8424d5. Repo stays PRIVATE.
- mega27-24-blight-resistant-chestnut: 24a90b1e..69d15589 ("Replay 15-library chestnut infection quality table and mapping gap", lane C verified-complete bundle). FF-verified vs lane's own 24a90b1e. Readback 69d155891ced89416bbb97ac6155b419b45fff1f.
- mega27-25-biomarkers-underserved-diseases: 5b481a10..3046b32e (source-audit CLI tool). Readback 3046b32edb5cafd43f3e1d0c1b86590566bf91d3.
- mega27-27-isef-bioinf-derived-tools: 1de89b7b..88819551 (pre-2PM truth-status doc). Readback 88819551d3e0e27a705cb89d29a973acefb5640f. Repo stays PRIVATE.
- mega27-24-banana-vaccine-enviropig: 5641a45c..020383a3 ("Screen lettuce CTB-ESAT6 capsule paper as endpoint near-miss", lane C verified bundle, lettuce CTB-ESAT6 endpoint screen fifth study honest 0/5). FF-verified vs lane's 5641a45c. restored-main branch created at a3ef095 (= archive/out-of-scope-designs). Readback main 020383a3789574186f21577a4f5e73f836e53c46.
- mega27-25-biomarkers-underserved-diseases: 3046b32e..a5ea2bf7 ("Register held-out PCOS cumulus sign test before expression read"), then a5ea2bf7..b9722da6 (P46 PCOS registered test result, negative p=0.108). Readback b9722da6c53b8b891d9e99f6269070fe2c510577.
- mega27-24-rice-oral-vaccine: 24b8031b..669b3aae ("Reconcile published rice CTB summaries across distinct estimands", lane C verified bundle, 12/12 tests). FF-verified. Readback 669b3aae322c86fb4ba0c8d3b59365975bb5ee45.

## 2026-09-27 15:32 IST - deploy key ADDED: mega27-05-yeast-metabolic-twin
- Title: mega27-05-redirect-laneB-revival
- Key type: ssh-ed25519, write access, one-per-repo (fresh keypair for this repo only)
- Fingerprint (verified on-page vs local ssh-keygen -lf): SHA256:xV1jNAxsxnezETvpOZTqXLybIuyLKRLW1NrOQ+KUkgY
- Authorized by: Main relay 15:30 IST under her standing 2026-09-24 "You add" ruling (fresh builder public keys, write, one per repo)
- For: revived yeast lane B agent (agent-01M3H4TTZDBY5V2CF685SSQJHB)
- Verified on-page: entry present with Read/write + Delete button; pre-existing key "instinct-mega27-05-redirect" (SHA256:NcO6pBFwVarlhrOj5hn0QqP1a3xPociQWqxXBB9njYY) untouched.

## 2026-09-27 15:43-15:57 IST - WIPE-WAVE KEY ROTATION (44 deploy-key adds, 1 removal)
Sandbox wipe wave ~15:41-15:43 IST destroyed builder keys across lanes (23a, lane-29, VC2/VO3, biomarkers-25, microbiome, xenobot, peptides, revival-C, lane C, item-27) and the orchestrator's own account-level key v7b (private half lost; orphan still on account - revoke pending HER decision, do NOT touch, same posture as v5).
All adds authorized under her standing 2026-09-24 "You add" ruling (fresh builder public keys, write, one keypair per repo, rotated on sandbox reset), relayed by Main 15:43-15:53. Every add verified on the repo's settings/keys page (entry + fingerprint + Read/write + Delete control). Local ssh-keygen -lf fingerprints match on-page values.

### Lane keys (read-write deploy keys, one per repo)
- mega27-23a-drosophila-connectome-ann: mega27-23a-deploy-rebuild-20260927 SHA256:FWbRjdUjxUvXmeMpf2H1IjaQOJWa1AAlcPx8r0jSRmM
- mega27-19-xenobot-causal-networks: instinct-builder-xenobot-lane-20260927 SHA256:LShM7b591QOawKQvkbYxj09fEdXDTzwFM8PnMPmj3+0
- mega27-04-microbiome-twin: mega27-04-microbiome-twin SHA256:AI5NAzWwhwsYZfE+hKsQDNmYWRp13dAGdptZRGfDYaU
- weird-09-radiation-toolkit: deploy-weird-09-radiation-toolkit-20260927 SHA256:euyjhS979tk6fRmpT7V7nCiWSAU49Ya9VYbOQ1XGJdA (REPLACED shared key weird10-builder-20260927 SHA256:pMaMkSQsozgKxJExRj3a7Uno/mMk78eav9DYDtSLqMg, removed per Main - GitHub one-key-one-repo rule)
- weird-11-ai-evolved-biofactories: deploy-weird-11-ai-evolved-biofactories-20260927 SHA256:N2mDG/MDK90y6YGmks+qvt1p5nEwIdTf+3idDX6CKWM
- weird-02-quantum-compass (private): deploy-weird-02-quantum-compass-20260927 SHA256:iinze7OuuThqtCuILNnZtqQzim9vyjXK9FGN/3Bcul4
- mega27-25-chagas-biomarkers: chagas-builder-25-20260927 SHA256:81lXWs3yFcrhuD14PTjoKXCPO6LZihw4aIcmlSFzpGo
- mega27-09a-amp-design-discovery: mega27-09a-rebuild-20260927 SHA256:ky3Xb6zVXaofd9KT31UrNlbtWQpm/7uYCYek3/kx7og
- mega27-09b-peptide-hla-cpp: mega27-09b-rebuild-20260927 SHA256:e/y36mszi84zb5qqKWr4nVMsZn+F7+EXpvxJsF/9ZSU
- mega27-09c-peptide-solubility-anticancer: mega27-09c-rebuild-20260927 SHA256:v8n42QugrfvbdicEASCtrfcLcCgGUwmaF1BFTIS6p3U
- mega27-09d-oncovax-pep: mega27-09d-rebuild-20260927 SHA256:mvhnskId7xXhnH2aeEpsn1sp5FAtooXjQodIZCTDaIs
- mega27-09e-resistpep: mega27-09e-rebuild-20260927 SHA256:LwRzAH1VcyNxk0dRhPPZqiZSzit7CmPu5GUO+jamv64
- mega27-11a-protein-redesign-1-3: mega27-11a-rebuild-20260927 SHA256:qJfo180WUzlx9gmRMsZhZP7gGd9K4xyIak0oHbtYGZo
- mega27-11b-protein-redesign-4-5: mega27-11b-rebuild-20260927 SHA256:FijuOUUSZBHZuHlpVqf0FvPHShAsE0Hjc8NG+huLDBM
- mega27-12-3d-drug-discovery: mega27-12-recovery-20260927 SHA256:l6WuXd7i4bMNOPD0vn5XsZ/iuwsINhgKgso90ScioEM (CORRECTED key per Main; mistyped original never installed)
- mega27-18-mirna-research (private): mega27-18-recovery-20260927 SHA256:FOM6Vnl8Bqnyi1yU54+9T9AQUMnJ/A3OwRWw0CqJW4k (CORRECTED per Main)
- mega27-21-cancer-recurrence: mega27-21-recovery-20260927 SHA256:X8y5KSL+dCA7Iqjum8fVDnv0LK2sMRWLAq8WrWrTVg8 (CORRECTED per Main)
- mega27-24-rice-oral-vaccine: mega27-24-rice-rebuild-20260927 SHA256:jQ1ZoqHNuDgQ84gWYhagcJUlXB2sSlXsa/MM9UVNhrM
- mega27-24-aquadvantage-salmon: mega27-24-salmon-rebuild-20260927 SHA256:gs6JF4D0Shc0TppmIFTikHcVzPEh2yT2Rv1dgeHPBA8
- mega27-24-blight-resistant-chestnut: mega27-24-chestnut-rebuild-20260927 SHA256:gP7Cr5OWgZliCoJj5FARRx/Gz/EvKTpOsHta0wIZ56U
- mega27-24-banana-vaccine-enviropig: mega27-24-banana-rebuild-20260927 SHA256:j3A/yYd0e9xA5nj75Ul5paxGu/dm4RsA4mWbxxbUbwY
- mega27-02-virtual-cell: vc2-recovery-20260927 SHA256:MdQHLKQQoQ1DfOp2tsPwu7fhydqgLYIpB3MbCAY6JLc
- mega27-03-virtual-organoid: vo3-recovery-20260927 SHA256:jcRs+yvGcAz60wo8ggmN700AEsvdTDypl+ebWrZlxMw
- mega27-27-isef-bioinf-derived-tools (private; = item-27 repo): item27-recovery-20260927 SHA256:rIEvHEmeqqJj1qo2PVeskCUUSdRVp+SouKIn+ZcxMiY

### biomarkers-25 keys (read-write, one per repo, titles <repo>@task)
- mega27-25-biomarkers-underserved-diseases: SHA256:rooMvTeuQjJlBJv7yPJ9iiAD65dU0iKfUOpmepB1gt0
- mega27-25-postpartum-depression-biomarkers: SHA256:NEIO8FYKTSU7dp+RDWDPiCjVehH8freVMw4B50inOvA
- mega27-25-interstitial-cystitis-biomarkers: SHA256:xba78w7Jr+7cpaeY6U+91fAFb3kUQyAmOLgL9xrZSDc
- mega27-25-endometriosis-biomarkers: SHA256:7jS7jBuo/laTs6xfVJYcjs5qurb0mfylXIehyl/gHEk
- mega27-25-pcos-biomarkers: SHA256:ajzyMcs5j3WzAceCFhRGvD9DnI5gMOhVp6VL5lz0Nzg
- mega27-25-leishmaniasis-biomarkers: SHA256:/8KViyk/bhz96VTUWodgxIBRh6dk/l/OfL+tZxW4Qeo
- mega27-25-preeclampsia-biomarkers: SHA256:TwaZMaNoaSkrJdfs3LV6g9opsLZ27RIj94mf5qChy8E
- mega27-25-long-covid-biomarkers: SHA256:5v4e6MgPkrAsBnvbCXWHDo0opZN8gliyyFGIOBisGGU
- mega27-25-me-cfs-biomarkers: SHA256:BkTzrEqyUowMKtmIijDI9PwOJWjWStpTnRFw8/uqnYk
- mega27-25-fibromyalgia-biomarkers: SHA256:ua9HWB5MP2rcoeSDFKU2fggO4x3SW2zBZLqiWLpUS0k

### Orchestrator recovery keys (Main 15:43 route: per-repo deploy keys on push targets + read on item-27, after v7b loss)
- science-program-ledger: orchestrator-ledger-20260927 SHA256:xCcCyl5/AscTK6B1TYThIF9JH/Hboh7XcZjOWD/y0MA (write)
- atlas-ai: orchestrator-atlas-20260927 SHA256:ynIvcRKCMu/3wcZ2Rgnfi46tqwvVKQerwhLp+W3mNfs (write)
- sugarcode-ai: orchestrator-sugarcode-20260927 SHA256:XG7DcZhw9Vtm3RRkGj71vYF5+1M2Fv/BS0rfAOXpdpk (write)
- shared-models: orchestrator-shared-models-20260927 SHA256:HbDGTqrapXsQEBzv9qbPAQXnt2JEbeuX+FVdyJ+cUTE (write)
- mega27-24-rice-oral-vaccine: orchestrator-rice-20260927 SHA256:kSjk/BV5pdS6QJ4NnYQ+ZtgwOmzpbmvmELGkL1Zmo9Y (write)
- mega27-24-blight-resistant-chestnut: orchestrator-chestnut-20260927 SHA256:8Yi0H+ewUrxMUUF/uxTMDnZpnuTpUm+f1ht0bq5LxUU (write)
- mega27-24-banana-vaccine-enviropig: orchestrator-banana-20260927 SHA256:+lMAsgTbKxVKyGoMU1Th5cb7vIcxOSD3vYSxkhBs28E (write)
- mega27-09c-peptide-solubility-anticancer: orchestrator-09c-20260927 SHA256:fGr2zGcUa6plzHhFZPgYxmQe8u2lUreRl0lfYW4nLYU (write)
- mega27-25-interstitial-cystitis-biomarkers: orchestrator-ic-20260927 SHA256:ky75+fGyTgGTFGFeAy4q1ofgZmOOIPGxB67/BO1ZONM (write)
- mega27-27-isef-bioinf-derived-tools: orchestrator-item27-read-20260927 SHA256:eSOyLxvm5gFOPvQjRyOYtzCm71t5aiP4IUG2i2KGFhY (READ-ONLY per Main "read item-27")

### Removal
- weird-09-radiation-toolkit: REMOVED weird10-builder-20260927 SHA256:pMaMkSQsozgKxJExRj3a7Uno/mMk78eav9DYDtSLqMg (Main 15:45 "disregard the earlier single weird10-builder key - remove if installed"; replaced by per-repo deploy-weird-09 key). No other removals. v5 and orphaned v7b account keys untouched pending HER decision.

## 2026-09-27 15:59 IST - wipe-rotation keys: lane-16/10/20 (second wipe ~15:58)
- mega27-10-dl-diagnosis-suite: "mega27_10 task-agent 20260927" SHA256:Cxb2rjDn8BnFYwcIUEoHNLi3cqITtUD3BWktQ8xZDGQ (write)
- mega27-16-biodataset-ml-treatment: "mega27_16 task-agent 20260927" SHA256:YXdpJG01qcgDhZFTnkRb4AS8XkIjxWV5YZWicZBpgYE (write)
- mega27-20-drug-target-prediction: "mega27_20 task-agent 20260927" SHA256:Ydu76gcnM79b1Loa+jxmAAjlZDm6cKizk48DUAC0OF8 (write)
Same grant grounding (her 2026-09-24 "You add" ruling via Main 15:59). Repo names verified against live account (agent wrote mega27_10/16/20). All verified on-page.

## 2026-09-27 16:03 IST - wipe-rotation key: jellyfish 26b continuation agent
- mega27-26b-immortal-jellyfish-genomics: jellyfish26b-20260927 SHA256:uYqLdl3YDxmgN/k3cT/MVwtcGS9yM5cMLab0bJ49kOE (write). Agent has material local result dab2c7a awaiting push. Same grant grounding (her 2026-09-24 "You add" via Main 16:03). Verified on-page.

## 2026-09-27 16:07 IST - orchestrator key + bundle relay: mega27-24-aquadvantage-salmon
- Deploy key added: orchestrator-salmon-20260927 SHA256:PuZAZDAZHwSRtvDvrLrD5sVPYN6fVK4o8l27OByqW80 (write) - needed for this bundle relay (no prior orchestrator key on salmon).
- Bundle push (lane C, salmon-independent-heat-screen-552ada2f.bundle): remote main 1f2300477bfd9e36447b8aee0d661d5ee55e9f5b -> 0bf3a3988867f80405b473013fe53f1ecbbed119. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push). Commit message verbatim: "Screen independent salmon heat cohort as unmatched validation source". Readback confirmed 0bf3a398.

## 2026-09-27 16:09 IST - wipe-rotation key: yeast lane B (second wipe)
- mega27-05-yeast-metabolic-twin: mega27-05-redirect-laneB-revival-2 SHA256:g0WQW4yYbeegCt+xd7v+riYXLP9GUcEk6Hunl+YJJNo (write). Same grant grounding (her 2026-09-24 "You add" via Main 16:09). Verified on-page. First revival key (mega27-05-redirect-laneB-revival SHA256:xV1jNAxsxnezETvpOZTqXLybIuyLKRLW1NrOQ+KUkgY) remains attached - its private half died in the lane sandbox; revoke only on Main's explicit instruction.

## 2026-09-27 16:15 IST - wipe-rotation keys: lane-29 SECOND wipe, replacements (old keys left attached pending her revocation sweep)
- weird-09-radiation-toolkit: lane29-weird-09-20260927-2 SHA256:Mxuh7gqH2gfZlz5LJQAHSa1dVE8tVyIsJtDuE6ApNc0 (write)
- weird-11-ai-evolved-biofactories: lane29-weird-11-20260927-2 SHA256:mrlqV+teg+0scXH1PTbSWEIdMsfbDCP5eoUBCv3C5wA (write)
- weird-02-quantum-compass (private): lane29-weird-02-20260927-2 SHA256:aaT/iMJBSTGcrATQcGXPKxiNcEuNgdM72fWoxq/I0bU (write)
Main 16:15: install as new, leave first-round keys (deploy-weird-09/11/02-...-20260927) attached - one revocation sweep later with her approval. Same grant grounding. All verified on-page.

## 2026-09-27 16:51 IST - bundle relay: mega27-24-blight-resistant-chestnut
- Bundle push (lane C, chestnut-mapping-gc-qc-f65dbcc1.bundle): remote main 69d155891ced89416bbb97ac6155b419b45fff1f -> 88e5ebd28843a1c7e10839dcfecbe100cbb18095. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 69d155891). Commit message verbatim: "Audit chestnut 9h mapping gap against GC and Q30 table metrics". Triple ls-remote readback confirmed 88e5ebd2. Orchestrator key orchestrator-chestnut-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 17:38 IST - bundle relay: mega27-24-banana-vaccine-enviropig
- Bundle push (lane C, banana-spirulina-near-miss-c6ac1d27.bundle): remote main 020383a3789574186f21577a4f5e73f836e53c46 -> 589b944b2b111bfb8d6889cc6c99c20edb25b38c. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 020383a37). Commit message verbatim: "Reconcile banana screen count and flag spirulina antibody near-miss". Triple ls-remote readback confirmed 589b944b. Orchestrator key orchestrator-banana-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 18:24 IST - bundle relay: mega27-24-rice-oral-vaccine
- Bundle push (lane C, rice-19a-wgs-accession-scope-4e8c40db.bundle): remote main 669b3aae322c86fb4ba0c8d3b59365975bb5ee45 -> 9590ec415456ae4c1f29af811aa4762439348f31. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 669b3aae). 2 commits, messages verbatim: "Resolve MucoRice 19A accession as one genomic run, not dose data" (c1e8453, 18:22) and "Make MetaboLights replay independent of filesystem glob order" (9590ec4, 18:23). Triple ls-remote readback confirmed 9590ec41. Orchestrator key orchestrator-rice-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 18:58 IST - orchestrator key + bundle relay: mega27-25-biomarkers-underserved-diseases
- Deploy key added: orchestrator-b25shared-20260927 SHA256:1IRUBY/UDad/TiX0L7NxZ9ZlKLtf9/0eAydLixoMfKE (write) - needed for this item-25 bundle relay (no prior orchestrator key on shared-core). Grant: Main 15:43:46 recovery route (per-repo deploy keys on bundle-relay targets) + her 2026-09-24 "You add". GitHub sudo email gate cleared (code read from her Gmail). Verified on-page (Never used, Read/write, Delete button present).
- Bundle push (item-25, item25-p35-parent-20260927-002637cb.bundle): remote main 4563a73f059ed5e1b8706976e08be2cca4453bd8 -> 018988f27d468bd6f4b6807d8465923ee0955a7a. Bundle verified OK (requires 4563a73, present locally), ancestry proven: tip's direct parent IS the live head (FF). Commit message verbatim: "Reconcile source-used P35 leishmaniasis parent series" (Instinct Agent, 18:55:00 IST). NOTE: first push attempt of the raw SHA was rejected "needs force" with a non-commit hint despite proven FF ancestry (both objects verified type=commit); retry via a local branch ref landed as clean FF 4563a73..018988f, no force used. Triple ls-remote readback confirmed 018988f2.

## 2026-09-27 19:09 IST - bundle relay: mega27-24-aquadvantage-salmon
- Bundle push (lane C, salmon-temperature-endpoint-reversal-ad42bdf9.bundle): remote main 0bf3a3988867f80405b473013fe53f1ecbbed119 -> 910d7696c46ce4af55319d7f4d61e697822788b4. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 0bf3a398). Commit message verbatim: "Audit opposing salmon time-to-weight and feed-efficiency endpoints" (Instinct Agent, 19:08:34 IST; adds data/sources/ignatz2019_thesis.pdf + docs/results/scripts/tests). Pushed via local branch ref. Triple ls-remote readback confirmed 910d7696. Orchestrator key orchestrator-salmon-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 19:52 IST - bundle relay: mega27-24-blight-resistant-chestnut
- Bundle push (lane C, chestnut-darling-performance-3d161a5b.bundle): remote main 88e5ebd28843a1c7e10839dcfecbe100cbb18095 -> 85d2b15dcf6a4aa7aa039707afb1c4ab07041de5. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 88e5ebd2). 2 commits, messages verbatim: "Audit TACF Darling identity and field survival denominators" (a7ad621, 19:52:11) and "Use tolerant floating-point check for field-rate difference" (85d2b15, 19:52:15). Pushed via local branch ref. Triple ls-remote readback confirmed 85d2b15d. Orchestrator key orchestrator-chestnut-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 19:56 IST - orchestrator key + bundle relay: mega27-25-postpartum-depression-biomarkers
- Deploy key added: orchestrator-b25ppd-20260927 SHA256:7jSchXGataLLH+S+Akr7NurXq744/Yv6992VRihacKQ (write) - needed for this item-25 PPD bundle relay (no prior orchestrator key on PPD). Grant: Main 15:43:46 recovery route + her 2026-09-24 "You add". No sudo gate this time (earlier sudo session still active). Verified on-page (Never used, Read/write).
- Bundle push (item-25 PPD, item25-ppd-qut-20260927-838b71a9.bundle): remote main 702db060abf4427d3907841081ee132b83167af3 -> 78e668a8b0b91686731c73f457baaa98e08d82e4. Bundle verified OK (requires 702db06, tip's direct parent - FF). Commit message verbatim: "Correct PPD QUT repository source and antenatal endpoint boundary" (Instinct Agent, 19:55:32 IST). Pushed via local branch ref. Triple ls-remote readback confirmed 78e668a8.

## 2026-09-27 20:38 IST - bundle relay: mega27-24-banana-vaccine-enviropig
- Bundle push (lane C, banana-berardi-thesis-endpoint-0ad7236f.bundle): remote main 589b944b2b111bfb8d6889cc6c99c20edb25b38c -> 34ee094893babb6acdf30da8a4d454054093c27b. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 589b944b). Commit message verbatim: "Audit thesis numeric GI-antigen readouts without endpoint substitution" (Instinct Agent, 20:38:08 IST; adds data/sources/berardi2013_thesis.pdf (5.49MB) + docs/results/scripts/tests). Pushed via local branch ref. Triple ls-remote readback confirmed 34ee0948. Orchestrator key orchestrator-banana-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 20:56 IST - bundle relay: mega27-25-interstitial-cystitis-biomarkers
- Bundle push (item-25 IC, item25-ic-p25-source-20260927-8baa6ef7.bundle): remote main 8c883aa39907de13c7e52b2a80086ad657b8551a -> 966512320fc729f058cc2d4551e20445bf44bca9. Bundle verified OK (requires 8c883aa, tip's direct parent - FF). Commit message verbatim: "Audit fifty used P25 IC paired biopsies and reconcile units" (Instinct Agent, 20:55:43 IST; adds GSE238208 expression matrix + 50 GSM soft files + crosswalk). Pushed via local branch ref. Triple ls-remote readback confirmed 96651232. Orchestrator key orchestrator-ic-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 21:27 IST - bundle relay: mega27-24-rice-oral-vaccine
- Bundle push (lane C, rice-7e40c08-5c76890c.bundle): remote main 9590ec415456ae4c1f29af811aa4762439348f31 -> 7e40c0880bdcd15f0872380634fd2ce95bae8b09. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 9590ec41). Commit message verbatim: "Replay printed 19A shared-protein supplement table with defect accounting" (Instinct Agent, 21:27:00 IST; adds data/sources/PMC10978600_DataSheet_1.pdf (5.86MB) + docs/results/scripts/tests). Pushed via local branch ref. Triple ls-remote readback confirmed 7e40c088. Orchestrator key orchestrator-rice-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 21:56 IST - orchestrator key + bundle relay: mega27-25-endometriosis-biomarkers
- Deploy key added: orchestrator-b25endo-20260927 SHA256:AtE8oG/F1DsLrRhTpB8vPM6wB6RmGlrYsnljTqm19cg (write) - needed for this item-25 endo bundle relay (no prior orchestrator key on endo). Grant: Main 15:43:46 recovery route + her 2026-09-24 "You add". No sudo gate. Verified on-page (Never used, Read/write).
- Bundle push (item-25 endo, item25-endo-used7846-20260927-v2-003ef3eb.bundle - the v2 Main designated): remote main 56c81c8b509513b05cb8674296415eebdaea3da5 -> b0a0e6f66ff2b92f6d21ae3bc2960bf26b89ad76. Bundle verified OK (requires 56c81c8, present - FF). 2 commits, messages verbatim: "Reconcile ten analyzed GSE7846 sample records without resolving tissue conflict" (e610467, 21:55:06) and "Normalize compressed GEO record filenames and verify hashes" (b0a0e6f, 21:55:12). Pushed via local branch ref. Triple ls-remote readback confirmed b0a0e6f6.

## 2026-09-27 22:14 IST - bundle relay: mega27-24-rice-oral-vaccine
- Bundle push (lane C, rice-c277487e-d0462f81.bundle): remote main 7e40c0880bdcd15f0872380634fd2ce95bae8b09 -> c277487ebfce7ef564bc5955bc59bd0d506b58b3. Bundle verified OK (complete history), FF-OK over live remote (re-checked immediately before push, still 7e40c088). Commit message verbatim: "Replay printed 19A supplementary Table 1 aggregate percentage arithmetic" (Instinct Agent, 22:12:53 IST; docs/results/scripts/tests, 110 insertions). Pushed via local branch ref. Triple ls-remote readback confirmed c277487e. Orchestrator key orchestrator-rice-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 22:16 IST - bundle relay: mega27-24-aquadvantage-salmon
- Bundle push (lane C, salmon-094fd7b-ad3fb341.bundle): remote main 910d7696c46ce4af55319d7f4d61e697822788b4 -> 094fd7b0e5b8a6bafe0cd0c3f7e541af097041c7. Bundle verified OK (complete history, 4 refs), FF-OK over live remote (re-checked immediately before push, still 910d7696). Commit message verbatim: "Replay printed thesis growth-table degree-day accounting" (Instinct Agent, 22:15:31 IST; 5 files, 249 insertions). Pushed via local branch ref. Triple ls-remote readback confirmed 094fd7b0. Orchestrator key orchestrator-salmon-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 22:17 IST - bundle relay: mega27-24-blight-resistant-chestnut
- Bundle push (lane C, chestnut-08af2f5-5cd8e646.bundle): remote main 85d2b15dcf6a4aa7aa039707afb1c4ab07041de5 -> 08af2f5d696bbec38d40bda4639d47adcd704d00. Bundle verified OK (complete history, 4 refs), FF-OK over live remote (re-checked immediately before push, still 85d2b15d). Commit message verbatim: "Verify all 30 advertised infection-cohort file URLs by archived HEAD record" (Instinct Agent, 22:16:56 IST; 6 files, 353 insertions). Pushed via local branch ref. Triple ls-remote readback confirmed 08af2f5d. Orchestrator key orchestrator-chestnut-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 22:19 IST - bundle relay: mega27-24-banana-vaccine-enviropig
- Bundle push (lane C, banana-a6d2884-34dd0622.bundle): remote main 34ee094893babb6acdf30da8a4d454054093c27b -> a6d2884aa0c0e80ea406e11c178c95c200ec285a. Bundle verified OK (complete history, 6 refs), FF-OK over live remote (re-checked immediately before push, still 34ee0948). Commit message verbatim: "Pin and replay Pelosi 2012 published dose-record provenance" (Instinct Agent, 22:18:40 IST; 6 files, 207 insertions incl. data/sources/pmc3527624.xml). Pushed via local branch ref. Triple ls-remote readback confirmed a6d2884a. Orchestrator key orchestrator-banana-20260927 (pre-existing) used; no key ops this relay.

## 2026-09-27 22:56 IST - orchestrator key + bundle relay: mega27-25-pcos-biomarkers
- Deploy key added: orchestrator-b25pcos-20260927 SHA256:DXZy7aDlavYXL2P5n+tbqNci68VwWox5Cm0Vcj8krqg (write) - needed for this item-25 PCOS bundle relay (no prior orchestrator key on PCOS). Grant: Main 15:43:46 recovery route + her 2026-09-24 "You add". No sudo gate. Verified on-page (Never used, Read/write).
- Bundle push (item-25 PCOS, item25-pcos-gse5090-20260927-ee38fbc5.bundle): remote main 54ae18ab15d973442f8d591456f240d9961560ee -> 348379dcb8c102d3e6b36ce725d8b8abde4c92ad. Bundle verified OK (requires 54ae18a, tip's direct parent - FF). Commit message verbatim: "Reconcile seventeen historically analyzed PCOS adipose arrays" (Instinct Agent, 22:55:17 IST; adds 17 GSE5090 GSM soft.txt.gz files + README updates). Pushed via local branch ref. Triple ls-remote readback confirmed 348379dc.

## 2026-09-27 23:02 IST - bundle relays: lane C cycle 2 (all 4 repos)
All bundles verified OK (complete history), tips matched Main's stated heads, FF-OK over live remotes (re-checked immediately before each push), pushed via local branch ref, triple ls-remote readback over ~50s confirmed each. Orchestrator keys pre-existing on all four; no key ops.
- mega27-24-rice-oral-vaccine: c277487ebfce7ef564bc5955bc59bd0d506b58b3 -> 954d1195fa85f26f91c4810c23687a58b693e2b6. Commit message verbatim: "Audit 19A supp Tables 2/4 printed-string lengths: all labeled strings consistent, 19 primers 18-22nt" (lane-c, 23:00:24 IST).
- mega27-24-blight-resistant-chestnut: 08af2f5d696bbec38d40bda4639d47adcd704d00 -> 0e2a7f8f768db1326e28131f5bb5d0b774b84eb7. Commit message verbatim: "Audit 2025 curation paper Table 1: accession coverage, live ENA resolution, two scope flags" (lane-c, 22:57:19 IST).
- mega27-24-banana-vaccine-enviropig: a6d2884aa0c0e80ea406e11c178c95c200ec285a -> 0cb2e03d6f75528aa2628c484387c2044ead6d39. Commit message verbatim: "Pin PMC549291 (Thanavala 2005) abstract dose record; correct screen citation label; replay printed ratios" (lane-c, 22:58:56 IST).
- mega27-24-aquadvantage-salmon: 094fd7b0e5b8a6bafe0cd0c3f7e541af097041c7 -> 6bec9b7af734adde5ae4fb438175143d5b0fcd04. Commit message verbatim: "Audit thesis Tables 2-2/2-3: cross-equation replay, FI-unit negative, mass-balance screen" (lane-c, 22:55:47 IST).
- 2026-09-27 23:57 IST | ADD | repo deploy key `orchestrator-b25leish-deploy-20260927` on mega27-25-leishmaniasis-biomarkers | ED25519 SHA256:xwz2akoeUwqKEJQeuqo67SAjuItkJMCiQkklejUzz3E | read-write | per-repo route (Main 15:43:46) under builder-key grant (Main 15:45:07) | verified on-page (Never used - Read/write)

| 2026-09-28 11:16 IST | CREATE+ADD | repo uditakankananonononono/objective-fragility-method (PRIVATE, created by orchestrator via browser for algorithm invention track, agent-01M3K8F6AMJKPPCQW1RE682ERG, per Main 11:12 relay) | deploy key builder-objective-fragility-method-20260928 | SHA256:L1SPThIdpF8HlgcRKMkSTxYPtBsCHXrus/b20Z3UN+U | fresh keypair, one key for this repo only, write access | verified on-page (title + fingerprint + Read/write + Delete button); GitHub sudo email code flow used |

| 2026-09-28 11:17 IST | ADD | repo uditakankananonononono/objective-fragility-method | deploy key objective-fragility-method-agent | SHA256:NqVp3MHFHTB8iFRvklIukV/uwS7iuozaRf9IkgtX2yM | invention agent's (agent-01M3K8F6AMJKPPCQW1RE682ERG) own keypair relayed by Main; FIRST relayed string was a mis-paste - NOT added, superseded by Main's 11:17 correction; private half stays in the agent's environment; write access, second key on this repo | verified on-page (title + fingerprint + Read/write + Delete button) |

## 2026-09-28 13:28 IST - key add: 13a lane builder key

- ADD: deploy (write) key `synthetic-lethal-rl-builder-20260928` on mega27-13-synthetic-lethal-rl ONLY - ssh-ed25519 SHA256:cIkvjfup5Xd8oPK2KKxNkfhCvwZ+rDs9n0nJ/UOdOX0, relayed by Main 13:25 (13a lane's own new keypair for its authorship audit of all 108 files at df687fb; private half stays in lane workspace). ssh-keygen -lf validated pre-add, fingerprint matched Main's relay exactly. Key body pasted verbatim from archived pubkey file (/tmp/pubkeys/13a-builder-20260928.pub). Verified on-page: 2 deploy keys listed, new key shows Read/write with Delete control, fingerprint exact. Note: first two form POSTs were consumed by GitHub sudo email gate (no error surfaced); completed sudo via email code, GitHub replayed the POST. Same grant grounding: her 2026-09-24 11:03 "You add" via Main.

## 2026-09-28 — orch-selective-transfer-certificate-20260928 (ADD, write)
- Repo: uditakankananonononono/selective-transfer-certificate (new, PRIVATE; created per Main relay 2026-09-28 ~21:12 IST, user-delegated)
- Key: orch-selective-transfer-certificate-20260928 — SHA256:xtx9le6kz4kVKcPTZOGc1LdevSbJs4gwplD/svtQ2bQ (ed25519, write deploy key, verified on-page Read/write 2026-09-28 21:24 IST)
- Purpose: orchestrator seeding/ops key for this repo

## 2026-09-28 — orch-selective-transfer-certificate (ADD, write)
- Repo: uditakankananonononono/selective-transfer-certificate
- Key: orch-selective-transfer-certificate — SHA256:QOWf+Z1Nwog4xKBssQ8GQiya6MgvLPt0kvZwYzeiLYQ (ed25519, write deploy key, verified on-page Read/write 2026-09-28 21:35 IST)
- For: agent-01M3K8F6AMJKPPCQW1RE682ERG (invention/builder agent), pubkey relayed by Main 2026-09-28 21:34 IST under the Sep-24 "You add" grant; ssh-keygen -lf matched Main's expected fingerprint before adding

## 2026-09-29 — orch-phage-capsule-rbp-kpneumoniae-20260929 (ADD, write)
- Repo: uditakankananonononono/phage-capsule-rbp-kpneumoniae (new, PRIVATE; created per Main relay 2026-09-29 00:19 IST, user-ordered lane)
- Key: orch-phage-capsule-rbp-kpneumoniae-20260929 — SHA256:uhLj6s72sJ18cVHVdVri2sHUzG7NqyCXrIZ6hPNaLbA (ed25519, write deploy key, verified on-page Read/write 2026-09-29 00:20 IST)
- Purpose: orchestrator seeding/ops key for this repo. Lane builder key to follow via Main relay.

## 2026-09-29 — phage-capsule-rbp-kpneumoniae-builder (ADD, write)
- Repo: uditakankananonononono/phage-capsule-rbp-kpneumoniae
- Key: phage-capsule-rbp-kpneumoniae-builder — SHA256:ABz40gQ1f182xzIvRrEbxSXK/d1rnpBtvU/yGUECkCs (ed25519, write deploy key, verified on-page Read/write 2026-09-29 00:24 IST)
- For: lane agent-01M3MNEJHBME8Y4RZYJ9RNTQKF, pubkey relayed by Main 2026-09-29 00:23 IST under the Sep-24 "You add" grant; ssh-keygen -lf matched Main's expected fingerprint before adding

## 2026-09-29 — orch-agent-cognition-memos-20260929 (ADD, write)
- Repo: uditakankananonononono/agent-cognition-memos (new, PRIVATE; created per Main relay 2026-09-29 00:38 IST)
- Key: orch-agent-cognition-memos-20260929 — SHA256:numU3ZHyRxUD4n+JTrFUa7A/vk0Dwl3Tm3apN2BCJzc (ed25519, write deploy key, verified on-page Read/write 2026-09-29 00:39 IST)
- Purpose: orchestrator seeding/ops key. Exploration agent-01M3MPJ1E4941G4BCS2R88ZNTQ builder key to follow via Main relay if it will push itself.

## phage-capsule-rbp-kpneumoniae-closer — 2026-09-29
- Repo: uditakankananonononono/phage-capsule-rbp-kpneumoniae (PRIVATE)
- Key: ssh-ed25519, write deploy key, on-page verified Read/write
- Fingerprint: SHA256:GLE8EiOYXXNAharFhe3x8K3G/5+ai7Fqb6WvfHsgSDQ
- Owner agent: phage closer (agent-01M3NBN44M300VPTW2E810BSEZ); keypair generated by the closer, private half never transited
- Relay: closer pubkey via Main 2026-09-29 07:03 IST; first body mistranscribed, STOP+correction relayed 07:03, closer fingerprint match confirmed by Main 07:04 before install
- GitHub sudo: email code flow, POST replayed, key list re-verified (3 deploy keys)

## phage-capsule-rbp-kpneumoniae-phase2 — 2026-09-29
- Repo: uditakankananonononono/phage-capsule-rbp-kpneumoniae (PRIVATE)
- Key: ssh-ed25519, write deploy key, on-page verified Read/write
- Fingerprint: SHA256:jr/GWNp9l+2/9mCtHW2d7SPgbMKzo6scFHRUtMpMtFc
- Owner agent: phage phase-2 (agent-01M3NDTSJPCT0KCZ9444EV6GAT); keypair generated by the agent, private half never transited
- Relay: pubkey via Main 2026-09-29 07:23 IST; agent fingerprint match (incl. ssh-keygen -y body reproduction) confirmed by Main 07:24 before install
- Sudo: prior window active, no re-prompt; keys list re-verified (4 deploy keys)
- Lifecycle: closer key (SHA256:GLE8EiOY...) remains until phase-2 first push verifies, then removed as dead per Main instruction

## phage key removals — 2026-09-29 07:55 IST
- REMOVED phage-capsule-rbp-kpneumoniae-phase2 (SHA256:jr/GWNp9l+2/9mCtHW2d7SPgbMKzo6scFHRUtMpMtFc): agent retiring; its first real push verified (remote HEAD b45a985fbccfbfc4ea8ad7cdf4cc6462a4489687 confirmed pre-removal). Removal per Main's explicit relayed instruction naming the key.
- REMOVED phage-capsule-rbp-kpneumoniae-closer (SHA256:GLE8EiOYXXNAharFhe3x8K3G/5+ai7Fqb6WvfHsgSDQ): dead since closer agent retired. Removal per Main's explicit relayed instruction naming the key.
- On-page verified after removals: 2 deploy keys remain (orch-phage-capsule-rbp-kpneumoniae-20260929, phage-capsule-rbp-kpneumoniae-builder).
- Phase-3 continuation lane (agent-01M3NFNN01S7MGEBJHSCEA8KVD) minting its own key per one-key-per-agent rule.

## phage-capsule-rbp-kpneumoniae-phase3 — 2026-09-29
- Repo: uditakankananonononono/phage-capsule-rbp-kpneumoniae (PRIVATE)
- Key: ssh-ed25519, write deploy key, on-page verified
- Fingerprint: SHA256:Gg5bBvy/5d6jPjjS3lnKXqf36QCDV3CaZUyCIi+kKRk
- Owner agent: phage phase-3 (agent-01M3NFNN01S7MGEBJHSCEA8KVD); keypair generated by the agent, private half never transited
- Relay: pubkey via Main 2026-09-29 07:55 IST; agent fingerprint match (incl. ssh-keygen -y body reproduction) confirmed by Main 07:57 before install
- Sudo: prior window active, no re-prompt; keys list re-verified (3 deploy keys: orch, builder, phase3)
| 2026-09-29 | orch_mega27-20 | mega27-20-drug-target-prediction | write | ADDED | SHA256:zStOZHBrWHUzc2soxYf2/n892jPV2rdcu6Iz7BOchcU | Orchestrator builder deploy key; added under standing builder-key grant with Main 1:34:05 approval; used to push tag r3-ckpt-c23-b7168 for checkpoint release |

## 2026-09-29 15:52 IST - builder deploy keys for formatting-patch courier work (3)

Per builder-key pattern (one per repo, write, her 2026-09-24 grant; patches relayed via Main):
- builder-mega27-19-deploy on mega27-19-medical-microbots-xenobots, SHA256:5Six0gffHmiLshtGHdklPPRoysv6FxlDgiqB2VoQhMs, read/write, on-page verified (Delete button present). Private half: orchestrator ~/.ssh/builder_m19.
- builder-mega27-02-deploy on mega27-02-virtual-cell, SHA256:3IFLxuNrP3mzd44uOhBrpnXfnH2nJ8qr7zYg4LdVPf8, read/write, on-page verified. Private half: orchestrator ~/.ssh/builder_m02.
- builder-mega27-09a-deploy on mega27-09a-amp-design-discovery, SHA256:E5nG8aJEUjDs+8BKmvpAfik3eRPKNVRgTOYaKIUsJEM, read/write, on-page verified. Private half: orchestrator ~/.ssh/builder_m09a.
Sudo gate passed via her Gmail code flow during first add; window reused for the other two.

## 2026-09-29 17:26 IST - lane deploy key mega27-09d-oncovax-pep (1)

Per builder-key pattern (one per repo, write, her 2026-09-24 grant; key body + lane fingerprint relayed via Main 17:25):
- "mega27-09d-oncovax-pep deploy 2026-09-29" on mega27-09d-oncovax-pep, SHA256:Wt3nGOnEt6q4Y9ERFrv6YQJRZEund4QZseobvS+tuuE, read/write, on-page verified (Delete button present, fingerprint matches lane-relayed value; ssh-keygen -lf matched before add). Private half: 09d lane. Lane holds commit 635707f waiting to push.

## 2026-09-30 08:29 IST - embryo-lane recovery: lane-generated deploy keys (4 added, 2 orchestrator keys added then discarded)

Context: lane agent-01M3EMY005T2GTKTF0D2N7VQ38 sandbox wiped (repos+keys lost). Flow per Main 08:26: lane generates its own keypairs; only public keys travel (relayed via Main 08:27); orchestrator adds under her standing 2026-09-24 "You add" grant (one write deploy key per repo). All four added via browser (sudo email-code window) and verified on-page (Delete <title> button present; page fingerprint == ssh-keygen -lf of relayed pubkey; Read/write):
- "mega27-m14-builder-20260930" on mega27-14-digital-embryo, SHA256:Jr6RCOorvzfo9x46XStxUS5q5TvZaHRE7UwaG7oj4U4, read/write.
- "mega27-m07-builder-20260930" on mega27-07-pancreatic-ai-and-codon-optimizer, SHA256:2ldqn2kTaevH3bY021id2EZuC1FFxFXkZt9Dh/ubAzI, read/write.
- "mega27-m13b-builder-20260930" on mega27-13b-deep-rl-4-5, SHA256:ktYeD6ZIRbyX2xrYe9N5803mpjvf5cuCBimSscIngD4, read/write.
- "mega27-m23b-builder-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:8M/kG8jGoXMeVYT91WofvrO4SmqjpR6u91IoFG20tP8, read/write.
Private halves: lane's own sandbox only. Orchestrator holds no private key material for this lane.

Discarded first attempt (Main 08:26 flow change, security improvement): orchestrator had generated 4 local keypairs and added two ("mega27-14-digital-embryo builder 2026-09-30" SHA256:R6tbW3oLAd44kQot1cOIXMX/V/2RhOM5gIXJ+F6i388 on mega27-14; "mega27-07-pancreatic builder 2026-09-30" SHA256:G2hMgq7/Ws909b/wKDIK71mE0r++FnLHEGLQpdTAXoU on mega27-07). Both REMOVED from the repos 08:29 IST (on-page verified gone, lane keys intact) and all four local private+public halves shredded. No live remnant.

## 2026-09-30 08:34 IST - dreaming lane deploy key mega27-22 (1)

Same pattern (lane-generated, pubkey + fingerprint relayed via Main 08:34; her standing 2026-09-24 "You add" grant):
- "dreaming22-builder-20260930" on mega27-22-sleep-eeg-neurodegeneration, SHA256:baol3eGYPSIpsk0GV58w/JYYwugJYebMOnNkjH2Va+I, read/write, on-page verified (Delete button present; page fingerprint matches relayed value; ssh-keygen -lf matched before add). Private half: dreaming lane locally.

## 2026-09-30 08:37 IST - one-shot orchestrator builder key mega27-22 (added, used, removed)

Per Main 08:36 (authorized builder for DREAMING lane patch push; lane's SSH route blocked):
- "orch-dreaming22-builder-20260930" on mega27-22-sleep-eeg-neurodegeneration, SHA256:1Rwt9z4iuwtIU8rGkUgIK9ZsroT7W0si7DmS7ozzouQ, read/write. Used once to push commit 65bd0c793d8072688a786a505eb92a9ad7d88777 (lane's 896de5e checkpoint patch, authorship preserved as-is). REMOVED 08:37 IST (on-page verified gone; lane's own dreaming22-builder-20260930 key intact). Local private+public halves shredded; clone deleted. No live remnant.

## 2026-09-30 08:44 IST - one-shot orchestrator builder key mega27-22 #2 (added, used, removed)

Per Main 08:43 (builder task 2, DREAMING follow-up patch d2fe439c):
- "orch-dreaming22-builder2-20260930" on mega27-22-sleep-eeg-neurodegeneration, SHA256:h4ga0xoqgVMWUHP2g1/WpeDAVJyFydrSkCQKhAouGFk, read/write. Used once to push commit e32aeaef8ade5c067fa11568a3da7416800257d0 (patch applied cleanly onto 65bd0c7, authorship preserved). REMOVED 08:44 IST (on-page verified gone; lane's dreaming22-builder-20260930 intact). Local key material shredded; clone deleted. No live remnant.

## 2026-09-30 08:46 IST - one-shot orchestrator builder key mega27-22 #3 (added, used, removed)

Per Main 08:45 (builder task 3, DREAMING documentation-correction patch):
- "orch-dreaming22-builder3-20260930" on mega27-22-sleep-eeg-neurodegeneration, SHA256:pG1zuX9VRs0/vDfe4KKwp7drCMhRm0IGkwNyGidIRs0, read/write. Used once to push commit 6195c9032955d6eff647c87b309651d51da9a987 (applied cleanly onto e32aeae, authorship preserved). REMOVED 08:46 IST (on-page verified gone; lane key intact). Local key material shredded; clone deleted. No live remnant.

## 2026-09-30 08:47 IST - one-shot orchestrator builder keys for embryo-lane patches (2 added, used, removed)

Per Main 08:45 (two builder tasks, embryo lane patches relayed as attachments):
- "orch-m07-builder-20260930" on mega27-07-pancreatic-ai-and-codon-optimizer, SHA256:6UzS6w1zQFuacXKo917sKvprFHybeJq3wMpzrO1oYGE, read/write. Used once to push d8df974ba1d604e4c025ed5778005358b7cee81c (pathway patch applied cleanly onto a983bf55 via git am, authorship/date/message preserved). REMOVED 08:47 IST (verified gone; lane key mega27-m07-builder-20260930 intact).
- "orch-m23b-builder-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:9q6Yy9YL5V0jgQQMI4FtBKF/y2T4BKTBv+fHHYfQ65I, read/write. Used once to push 26da13f1da44c41794bdf9c67ca06e9a07afd409 (constraint patch applied cleanly onto a82be019 via git am, authorship/date/message preserved). REMOVED 08:48 IST (verified gone; lane key mega27-m23b-builder-20260930 intact).
Local key material for both shredded; clones deleted. No live remnants.

## 2026-09-30 09:00 IST - one-shot orchestrator builder key mega27-07 #2 (added, used, removed)

Per Main 08:59 (CPTAC+yeast patch):
- "orch-m07-builder2-20260930" on mega27-07-pancreatic-ai-and-codon-optimizer, SHA256:+Xi05YAnrjc3nBnoY0FnOq89ycBAPA6E3ALNJVYXu5s, read/write. Used once to push c0ff61b03f400cca0a8417f800dd22e69e7a88a9 (applied cleanly onto d8df974 via git am, authorship preserved). REMOVED 09:00 IST (verified gone; lane key intact). Key material shredded; clone deleted. No live remnant.

## 2026-09-30 09:01 IST - one-shot orchestrator builder key mega27-13b (added, used, removed)

Per Main 09:00 (multiseed patch):
- "orch-m13b-builder-20260930" on mega27-13b-deep-rl-4-5, SHA256:t6OBHibUT/U9IXdyHUghKXcIM5IWGHrlGMWKg3d10tE, read/write. Used once to push 76b384e88b9073909cfcbf00a2ffe02464654050 (applied cleanly onto 750a38f3 via git am, authorship preserved). REMOVED 09:01 IST (verified gone; lane key intact). Key material shredded; clone deleted. No live remnant.

## 2026-09-30 09:05-09:07 IST - one-shot orchestrator builder keys, three patch pushes (added, used, removed)

Per Main 09:04-09:06 builder tasks:
- "orch-m07-builder3-20260930" on mega27-07-pancreatic-ai-and-codon-optimizer, SHA256:Y52Eo+CKP0iIDAHq/rMey0RlYaqXZNYEzNNHyciwDm4, read/write. Pushed daf06569976c9ff4507f3532d2a43856bd4c9aad (synonymous patch onto c0ff61b0, git am, authorship preserved). REMOVED 09:05 IST, verified gone; lane key intact.
- "orch-m13b-builder2-20260930" on mega27-13b-deep-rl-4-5, SHA256:ONBjo2vD+au7GvOsEuZcLSHrVq2YAagDXg2ZcEJK8/w, read/write. Pushed 8538eedd9ad34dd26ae362f9b7a2d2288687f11b (seed-correction patch onto 76b384e8 via git am). REMOVED 09:06 IST, verified gone; lane key intact.
- "orch-m23b-builder2-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:PvPpWaanQJHt161CBAJWddHcsRY+MAZt1dSsy9461Do, read/write. Pushed ed7dbbbb246cd72fce9c73685757f7ce853a39e0 (paper-corrections patch onto 26da13f1 via git am). REMOVED 09:07 IST, verified gone; lane key intact.
All local private/public halves shredded; clones deleted. No live remnants.

## 2026-09-30 09:05-09:07 IST - one-shot orchestrator builder keys, three more patch pushes (added, used, removed)

Per Main 09:04-09:06 builder tasks:
- "orch-m07-builder3-20260930" on mega27-07-pancreatic-ai-and-codon-optimizer, SHA256:Y52Eo+CKP0iIDAHq/rMey0RlYaqXZNYEzNNHyciwDm4, read/write. Pushed daf06569976c9ff4507f3532d2a43856bd4c9aad (synonymous patch onto c0ff61b0, git am). REMOVED 09:05 IST, verified gone; lane key intact.
- "orch-m13b-builder2-20260930" on mega27-13b-deep-rl-4-5, SHA256:ONBjo2vD+au7GvOsEuZcLSHrVq2YAagDXg2ZcEJK8/w, read/write. Pushed 8538eedd9ad34dd26ae362f9b7a2d2288687f11b (seed-correction patch onto 76b384e8 via git am). REMOVED 09:06 IST, verified gone; lane key intact.
- "orch-m23b-builder2-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:PvPpWaanQJHt161CBAJWddHcsRY+MAZt1dSsy9461Do, read/write. Pushed ed7dbbbb246cd72fce9c73685757f7ce853a39e0 (paper-corrections patch onto 26da13f1 via git am). REMOVED 09:07 IST, verified gone; lane key intact.
All local key material shredded; clones deleted. No live remnants.

## 2026-09-30 09:12-09:14 IST - one-shot orchestrator builder keys mega27-23b #3 and #4 (added, used, removed)

Per Main 09:11 and 09:12 sequential builder tasks:
- "orch-m23b-builder3-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:N29xQiY1N7nCxIUuDOUDoRdCFIur4ZbGAHb2732uxTc, read/write. Used once to push 96b9dad1a144d9a96cb7a3465a384fa6a3058eeb (channel-correction patch onto ed7dbbbb via git am, authorship preserved). REMOVED 09:13 IST (verified gone; lane key mega27-m23b-builder-20260930 intact). Key material shredded; clone deleted.
- "orch-m23b-builder4-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:SdgTCv426T+Z98ZQteRC5Fvn5t2PaDSXx0rtFRLGTUU, read/write. Used once to push 87ca49becc0bf6d6f2063bedb8d1917a6bd4e346 (soft-erasure-fix patch onto 96b9dad1 via git am, authorship preserved). REMOVED 09:14 IST (verified gone; lane key intact). Key material shredded; clone deleted.
No live remnants.

## 2026-09-30 09:14-09:15 IST - one-shot orchestrator builder key mega27-14 (added, used, removed)

Per Main 09:14 (flower-radius patch resend; first 09:08 send never arrived):
- "orch-m14-builder2-20260930" on mega27-14-digital-embryo, SHA256:FJvxatR5+JcC2JN2rzMVmh8LO6UrqLJOvCHvwJ/4M9g, read/write. Used once to push 74076abe1feddffb25e6897d435bee3e263f469a (flower-radius patch onto 8e01fe87 via git am, authorship preserved). REMOVED 09:15 IST (verified gone; lane key mega27-m14-builder-20260930 intact). Key material shredded; clone deleted. No live remnant.

## 2026-09-30 09:19-09:20 IST - one-shot orchestrator builder key mega27-23b #5 (added, used, removed)

Per Main 09:19 (external-Fountain geometry audit patch):
- "orch-m23b-builder5-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:7y4RG+rr7EtEYcin/+NBrHij1ogMpJJz+2Cb+Co45PE, read/write. Used once to push 75a61363575b3828c5e34c5a59b49f76792eb6dd (external-fountain-geometry patch onto 87ca49be via git am, authorship preserved). REMOVED 09:20 IST (verified gone; lane key mega27-m23b-builder-20260930 intact). Key material shredded; clone deleted. No live remnant.

## 2026-09-30 09:33 IST - one-shot orchestrator builder key mega27-23b #6 (added, used, removed)

Per Main 09:32 (clean-graph threshold audit patch):
- "orch-m23b-builder6-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:qcwU7o7fJBXT4OwPe8I6AxPL9zPEZHBBshDihVwU9cI, read/write. Used once to push f9a3ac5bee80ebd9ad71be2cdadbb3fc3d408a7e (clean-graph-threshold patch onto 75a6136 via git am, authorship preserved). REMOVED 09:33 IST (verified gone; lane key mega27-m23b-builder-20260930 intact). Key material shredded; clone deleted. No live remnant.

## 2026-09-30 09:41 IST - one-shot orchestrator builder key mega27-23b #7 (added, used, removed)

Per Main 09:40 (valid-noise tradeoff audit patch):
- "orch-m23b-builder7-20260930" on mega27-23b-dna-encoder-cyborg-cell, SHA256:1KGXITX4nc1t+MsvIquP+Q1kJBYqD/YQGPmNoMYtVb4, read/write. Used once to push 2f3548655646317ad67e6959897a9e4fb432379e (valid-noise-tradeoff patch onto f9a3ac5 via git am, authorship preserved). REMOVED 09:41 IST (verified gone; lane key mega27-m23b-builder-20260930 intact). Key material shredded; clone deleted. No live remnant.

## 2026-09-30 09:47 IST - one-shot orchestrator builder key mega27-07 #4 (added, used, removed)

Per Main 09:46 (protein-cluster specificity audit patch):
- "orch-m07-builder4-20260930" on mega27-07-pancreatic-ai-and-codon-optimizer, SHA256:hUGddCsypeS63HG7kmv/NWqaWQYv9R1SuDEeGGUzh5Y, read/write. Used once to push 3d1c43d683f9abffd896b7994937aa14bf109f5d (protein-cluster-specificity patch onto daf06569 via git am, authorship preserved). REMOVED 09:47 IST (verified gone; lane key mega27-m07-builder-20260930 intact). Key material shredded; clone deleted. No live remnant.
