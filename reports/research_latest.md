# Automated research run — 2026-11-23 19:47 UTC

**Rationale:** I'm targeting microstructure-econometric features that are observable from OHLCV but encode *book depth / price-impact* information rather than raw direction — these are harder to fake via bid-ask bounce and can persist across venues. Key novelty is in conditional interactions: gating a directional bet on an estimated liquidity/impact state (Amihud illiquidity, Kyle's lambda, variance ratio, jump-vs-diffusion separation, absorption, and up/down impact asymmetry) rather than firing on price alone. A bounce artifact has symmetric impact and no persistence, so these gates should disproportionately survive the cross-venue cut.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| impact_asymmetry | -5.043 |  |
| variance_ratio_regime | -5.048 |  |
| absorption_reversal | -5.261 |  |
| amihud_illiq_reversion | -5.288 |  |
| kyle_lambda_momentum | -6.25 |  |
| jump_vs_diffusion | -7.846 |  |
