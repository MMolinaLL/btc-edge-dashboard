# Automated research run — 2026-09-28 16:24 UTC

**Rationale:** The classic single-factor signals are exhausted, so I'm targeting nonlinear FEATURE INTERACTIONS and microstructure quantities that reflect *liquidity absorption* rather than price patterns — these are the things most likely to survive on a deep book (Coinbase) and are not bid-ask-bounce artifacts. Core themes: (1) Kyle-lambda price-impact: whether a move was absorbed by liquidity (continuation) or thin-book overshoot (reversion); (2) realized semivariance asymmetry as a directional persistence proxy that ignores mean return; (3) a variance-ratio regime switch that decides momentum-vs-reversion sign rather than assuming one; (4) asymmetric liquidation-cascade reversion (down-moves overshoot more than up-moves on deep venues); (5) volatility compression + volume expansion as a genuine breakout conditioner; (6) effective-depth trend vs price trend divergence (informed pushing a thinning book). All use only backward-looking rolling windows.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| liquidation_cascade_reversion | -4.804 |  |
| variance_ratio_regime | -5.002 |  |
| kyle_lambda_absorption | -5.183 |  |
| compression_expansion_break | -5.377 |  |
| realized_semivariance_skew | -5.753 |  |
| depth_withdrawal_flow | -6.317 |  |
