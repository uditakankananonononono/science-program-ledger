# B2 frozen actual-pipeline timing, development

Same three skeleton hashes and exact ten-query lists as B1 RESULTS.json. No new
query/mask selection. Unit time=1, exposure=0, scenarios=(1,2). No physiology,
novelty, difficult-minimax, statistical or stable superiority claim.

Named comparator heap Dijkstra on original graph, same implementation as B1.
Candidate aggregate_chains plus ten scalar budget routes and witness expansions.
Time actual contiguous candidate preprocessing+queries, not separately paired
arithmetic. Baseline times ten contiguous Dijkstra queries; graph loading/build
shared and excluded from both timings. Each dataset/repetition runs a fresh worker.
Five repetitions, order alternates by index. No warmup inside measured pipeline;
coordinate BFS computed first for objective checks, outside timing. Validate
outputs/adjacency after each measured pipeline. Report each raw duration, medians
and observed sign, with B1 instability side by side. All losses preserved.
90-second timeout per worker; no RAM cap. No post-freeze tuning. Git ordering is
provenance, not external proof no earlier private experiment happened.
