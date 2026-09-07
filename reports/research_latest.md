# Automated research run — 2026-09-07 13:56 UTC

**Rationale:** I'm targeting mechanisms that reflect real order-flow economics rather than raw price patterns, and that shouldn't invert between a thin and a deep book. The unifying angle is CONDITIONAL/INTERACTION signals: the sign of a trade only matters when gated by how the market absorbed it (price-impact per volume, path efficiency, volume-weighted vs equal-weighted return divergence, higher-moment reversal, volatility-of-volatility regime). These use volume as a genuine information filter, not as a standalone predictor, so bid-ask-bounce artifacts (which carry no consistent impact/efficiency structure) should wash out cross-venue. None are guaranteed to clear the bar, but each has a distinct structural rationale from the rejected classics.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| vol_of_vol_momentum_gate | -4.986 |  |
| realized_skew_reversal | -4.995 |  |
| kyle_lambda_gate | -5.043 |  |
| vw_ew_return_divergence | -5.1 |  |
| variance_ratio_regime | -5.219 |  |
| range_exhaustion_reversal | -5.798 |  |
