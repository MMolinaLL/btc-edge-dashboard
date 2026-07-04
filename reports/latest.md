# 🟢 Idle (signal=0); 16-bet window net -0.07 bps — essentially flat, still far too thin to judge; BTC ~$62.5k

_Updated 2026-07-04 08:12 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position), BTC near $62,462, roughly $300 above last check. The rolling window is a negligible 16 bets — no statistically meaningful read.

**Status:** The strategy is sitting on its hands — `signal=0`, no open position. This is normal and expected: it only trades ~1-2% of candles, so live samples accumulate slowly.

**What changed:** The rolling window ticked from 14 to 16 bets. Net went from about +0.05 bps to **-0.068 bps** per bet — a tiny move that flips the sign but means nothing at this sample size. Gross edge is 2.93 bps against an assumed 3.0 bps cost, so this window is essentially breakeven-to-slightly-negative. Win rate is 62.5%. The formal ledger still shows **0 resolved trades**, so there is no confirmed live track record yet.

**What the numbers do tell us:** Nothing is blowing up. The window behavior (gross barely covering costs) is exactly what the validation warned about — this signal's edge is marginal (~4 bps gross vs ~3.9 bps breakeven) and likely not net-profitable after realistic costs.

**What they don't tell us:** With 16 bets, you cannot distinguish edge from noise. A single trade swings the average. Do not read anything into the sign flip.

**Also worth noting:** the edge search currently shows **0 survivors** against the strict bar (net positive on both venues at 5 bps cost, no look-ahead) — consistent with this being a marginal candidate, not a robust money-maker.

**Bottom line:** Flat, quiet, and far too thin to judge. No degradation to flag, but no proof of profit either. Keep watching; wait for dozens of resolved trades before drawing conclusions.
