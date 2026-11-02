# Automated research run — 2026-11-02 17:45 UTC

**Rationale:** I'm targeting edges rooted in microstructure and behavioral finance that are venue-robust because they derive from consolidated OHLCV geometry (price impact, jump vs diffusion decomposition, semivariance skew, absorption, round-number psychology) rather than from quote-level bid-ask dynamics. These rely on feature interactions and conditional regimes rather than a single classic indicator, so they should not reduce to bid-ask-bounce mirages and have a chance of surviving the cross-venue test.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| semivariance_skew_fade | -4.981 |  |
| vol_accel_return_corr | -4.996 |  |
| kyle_lambda_regime | -5.113 |  |
| round_number_magnet | -5.145 |  |
| jump_reversion_bipower | -5.651 |  |
| absorption_breakout | -7.259 |  |
