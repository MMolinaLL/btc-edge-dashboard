# Automated research run — 2026-11-16 17:51 UTC

**Rationale:** I'm avoiding all the rejected classics by targeting order-flow *mechanics* and higher-moment / impact-decomposition features that should express themselves identically on any deep venue (so they survive the cross-venue bounce test). The common thread: decompose each bar's return into an 'impact-explained' part vs an 'unexplained' part, read absorption/exhaustion from the range-volume-location interaction, let a variance-ratio decide whether to trend or fade rather than hard-coding one, and exploit documented higher-moment effects (realized skewness, isolated jumps). These are conditional interactions, not single indicators, which is where the un-picked edge usually hides.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| jump_overshoot_fade | -4.495 |  |
| absorption_reversal | -4.888 |  |
| realized_skew_reversal | -5.071 |  |
| variance_ratio_regime | -5.072 |  |
| kyle_lambda_residual | -5.221 |  |
| flow_price_divergence | -5.518 |  |
