# Automated research run — 2026-10-19 15:15 UTC

**Rationale:** The cross-venue test specifically kills microstructure/bid-ask artifacts, so a real edge must come from genuine supply/demand dynamics that are common to BTC across venues. I'm avoiding raw price-direction classics and instead targeting SECOND-ORDER structure: price-impact per unit volume (Kyle's-lambda-style liquidity regime), scale-dependent memory (variance-ratio adaptive switching), the shape of the return distribution (realized skew as a fade signal), liquidity ABSORPTION (large flow that fails to move price = informed accumulation), instability of the volatility process itself (vol-of-vol as a reversion trigger), and flow leading price (volume acceleration preceding directional resolution). These are conditional/interaction signals rather than relabeled momentum, and each is anchored to a mechanism that should be venue-invariant if real.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| realized_skew_reversal | -4.94 |  |
| vol_of_vol_reversion | -4.945 |  |
| variance_ratio_adaptive | -5.062 |  |
| kyle_lambda_regime | -5.473 |  |
| absorption_continuation | -5.683 |  |
| volume_accel_lead | -6.282 |  |
