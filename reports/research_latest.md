# Automated research run — 2026-09-21 14:49 UTC

**Rationale:** Cross-venue survival means the edge must live in bar-level *structure* (how price/volume interact over a window), not in tick-level spread capture. My angle is conditional/interaction signals: take a weak directional primitive (short momentum or close-location) and gate or flip it using an orthogonal statistical state variable (variance-ratio regime, price-impact/liquidity, path efficiency, vol-of-vol, absorption). These state variables are computed the same way on any venue's OHLCV, so a genuine effect should replicate while a microstructure mirage will not. Each is a distinct hypothesis about when the same primitive should be followed vs faded vs suppressed.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| variance_ratio_regime_switch | -5.049 |  |
| kyle_lambda_liquidity_momentum | -5.857 |  |
| volume_weighted_close_pressure | -5.966 |  |
| vol_of_vol_stability_filter | -6.35 |  |
| efficiency_ratio_gated_trend | -6.818 |  |
| absorption_close_location | -12.557 |  |
