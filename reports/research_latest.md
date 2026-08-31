# Automated research run — 2026-08-31 15:48 UTC

**Rationale:** Cross-venue survival (Binance.US AND Coinbase) kills bid-ask-bounce artifacts, so I avoid anything that profits from tick reversion in a thin book. Instead I target microstructure/behavioral signatures that should exist on both venues: (1) price-impact/liquidity conditioning of momentum (Amihud/Kyle-lambda ideas) where moves 'backed' by liquidity persist while low-liquidity spasms revert; (2) higher-moment (realized skew) and vol-of-vol regime gating rather than plain vol switching; (3) directional asymmetry in price-impact efficiency (does it cost less volume to push up than down?); (4) return/flow elasticity via rolling regression rather than raw imbalance. These are conditional feature interactions, not relabeled classics, and each is designed to be venue-agnostic.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| realized_skew_reversal | -5.094 |  |
| impact_efficiency_asymmetry | -5.118 |  |
| liquidity_backed_momentum | -5.166 |  |
| flow_elasticity_regression | -6.057 |  |
| volofvol_gated_drift | -6.246 |  |
| range_efficiency_trend | -6.935 |  |
