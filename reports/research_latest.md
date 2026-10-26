# Automated research run — 2026-10-26 14:48 UTC

**Rationale:** I'm targeting second-order microstructure and liquidity features that survive deep order books rather than first-order price patterns. The classics that failed are mostly linear functions of recent returns/volume. My angles: (1) realized semivariance asymmetry (downside vs upside variance has genuine reversal content in crypto), (2) Amihud-illiquidity gating momentum (trends persist only when the book absorbs flow cheaply — an interaction not a lone signal), (3) Kyle-lambda residual fading (price moves unexplained by signed flow are unsustainable), (4) volatility-of-volatility regime that flips follow/fade, (5) range-compression combined with volume-weighted intrabar tilt (conditional breakout direction), and (6) order-flow acceleration (second derivative of signed volume). These are conditional/interaction constructions meant to be venue-robust, not bid-ask-bounce artifacts.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| semivar_asymmetry_reversal | -4.997 |  |
| kyle_lambda_residual_fade | -5.187 |  |
| compression_volflow_breakout | -5.193 |  |
| volofvol_regime_flip | -5.236 |  |
| flow_acceleration | -5.91 |  |
| amihud_gated_momentum | -6.22 |  |
