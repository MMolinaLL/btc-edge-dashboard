# 🟢 Signal -1 active; 17-trade ledger at -7.9 bps/trade but tail-loss-driven, recent 13-window near gross-flat — still too thin to judge.

_Updated 2026-08-18 14:34 UTC · model claude-opus-4-8_

**Regime:** BTC chopping around $64.8k with a short (fade) signal live. With only ~4 bps expected gross edge per bet, one or two trend-day losses can swamp the entire live record.

**How it's doing:** The full live ledger now shows 17 resolved trades averaging **-7.9 bps** (total -134 bps), which looks bad on the surface. But this is dominated by a handful of tail losses: a single -60.9 bps trade (2026-07-31), plus -22.8, -18.2, -15.2 and two -13 bps trades. Strip the one worst trade and the average roughly halves. This is exactly the failure mode we warned about — a selective mean-reversion fade gets caught on a trend day and gives back many bets' worth of edge at once.

**What changed vs last time:** One more trade resolved. The rolling 13-bet window is **gross -1.8 bps** (net -4.8 bps after 3 bps cost) — essentially *gross-flat*, not clearly bleeding. Most recent trades have small positive gross that gets eaten by cost, consistent with a marginal edge, not a collapse.

**What the numbers do and don't tell us:** With only 17 trades, and results driven by 1-2 tail events, this sample **cannot** confirm or reject the edge. The two win-rate figures (23% ledger vs 69% window) differ because tail-loss magnitude, not frequency, drives P&L. Note also `edge_search_survivors: 0` — nothing cleared the stricter 5 bps/dual-venue bar, reinforcing that this was always marginal.

**Bottom line:** No profit is demonstrated, and none should be expected net of realistic costs. But the recent window is near gross-flat and losses are tail-driven, so this is not a confirmed breakdown either. Too thin to act — keep monitoring; watch for repeated trend-day losses.
