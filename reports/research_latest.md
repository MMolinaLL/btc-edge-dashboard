# Automated research run — 2026-09-14 14:41 UTC

**Rationale:** I'm avoiding the well-trodden price/volume classics and instead targeting second-order microstructure and distributional features that (a) require real order flow to persist and thus should survive on a deep book, and (b) express conditional feature interactions rather than a single indicator. Core themes: price-impact/illiquidity regimes (Amihud/Kyle-lambda style) that separate 'informed efficient' moves from 'exhaustion' moves, realized higher-moments (skew) as a directional predictor, volatility-of-volatility as a gate for when trend is even tradable, order-flow persistence measured by acceleration rather than level, and intrabar buying-pressure drift. These are genuinely different mechanisms; some may still fail the cross-venue bar, but they are not relabeled momentum/mean-reversion.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| compression_impact_break | -4.944 |  |
| realized_skew_reversal | -5.071 |  |
| illiquidity_regime_split | -5.077 |  |
| clv_drift | -5.113 |  |
| vol_of_vol_gated_trend | -5.162 |  |
| signed_flow_persistence | -5.231 |  |
