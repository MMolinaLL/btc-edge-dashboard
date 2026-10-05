# Automated research run — 2026-10-05 16:45 UTC

**Rationale:** I'm targeting conditional feature-interactions and microstructure regimes that survive on a deep order book rather than directional primitives. Key angles: (1) price-impact (Amihud illiquidity) as a regime switch that flips the sign of autocorrelation — the economically real reason momentum vs reversal alternates; (2) volume absorption (big flow, no price move) as a leading reversal indicator distinct from raw volume z-score; (3) jumps vs diffusion separated via bipower-style median vol so only genuine jumps are faded; (4) volume-concentration (HHI) as a gate that only lets momentum through when participation is broad; (5) wick-flow imbalance only when backed by flow; (6) range-compression WITH participation and close-location for a non-naive breakout. All use only past data and are shifted one bar to be strictly causal.

Proposed 6 strategies; **0 cleared the strict cross-venue bar.**

| strategy | min net @5bps | survives |
|---|---|---|
| volume_absorption_reversal | -4.608 |  |
| jump_vs_diffusion_fade | -4.865 |  |
| amihud_regime_flip | -4.979 |  |
| compression_participation_break | -5.151 |  |
| dispersion_gated_momentum | -5.248 |  |
| wick_flow_rejection | -5.583 |  |
