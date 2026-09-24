# algo50/74 - Greedy set cover for bait/panel design

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
On biologically-shaped instances (25 gene families x 8 members at 95% identity), greedy set cover designs a 31-bait panel covering all 200 targets - 4.3x fewer baits than random picking (median 132) and within 1.24x of the pairwise-disjointness lower bound (25), far under the (1+ln 200) ~ 6.3x worst-case bound. Each chosen bait averages 6.5 targets. The original 25-mer/60%-identity design was degenerate (zero shared k-mers, cover ~ 1/target) - k-mer sharing needs ~95%+ identity at k=15, itself a useful design fact.

## Gates
- Original (seed 61, K=25/60% identity): degenerate instance (documented); G3 FAIL (random ~ greedy ~ 200), others trivially PASS.
- Amendment 1 (seed 67, K=15/95% identity): P1-P4 all PASS.
Original degenerate + documented; pivot PASSES.

## Data
Simulated: family consensus 500 bp, members resampled at 5% of positions; baits = all distinct 15-mers (53,345).

## Caveats
- Real panels add GC/Tm/secondary-structure bait filters - coverage-only here.
- The pairwise-disjoint LB (25) is loose vs LP; true OPT is in [25,31].

## Reproduce
`python3 code/run.py` (seed 61), `code/pivot.py` (seed 67); numpy only, ~30 s.
