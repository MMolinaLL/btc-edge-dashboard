# Automated research run — 2026-10-12 17:18 UTC

**Rationale:** The classics failed because they lean on raw price/volume levels that are either arbitraged away or are pure bid-ask-bounce. I'm targeting second-order microstructure invariants that should survive cross-venue: price-impact (Kyle lambda) regimes, jump-vs-diffusion informativeness, path efficiency (fractal roughness), downside/upside semivariance asymmetry, and variance-ratio-based conditional switching. The core novelty is CONDITIONING the direction decision on an impact/elasticity/efficiency state rather than on the move itself — a thin bounce and a deep-book informed move look identical to a momentum signal but opposite under these gates, which is exactly what a cross-venue test should separate.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| variance_ratio_conditional | -5.002 |  |
| semivariance_panic_reversion | -5.044 |  |
| path_efficiency_switch | -5.291 |  |
| thin_move_fade | -5.342 |  |
| kyle_lambda_deep_momentum | -6.128 |  |
| jump_continuation_informed | -7.564 |  |
