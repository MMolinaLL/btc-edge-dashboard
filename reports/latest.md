# 🟢 26 resolved trades net -2.0 bps/bet (-51.8 bps total); last-7 window +3.5 bps. Still too thin to judge; signal flat.

_Updated 2026-09-13 17:18 UTC · model claude-opus-4-8_

**Regime:** BTC ~$77.3k, in the higher-price regime (~$77-81k) where recent trades have clustered positive, versus the early losing cluster down at $63-66k. Live signal is flat (0), so nothing is trading right now.

**How it's doing.** Over the full live ledger of 26 trades, the strategy is running at **-2.0 bps per bet (-51.8 bps total)** with a **38% win rate** — below break-even. But the more recent 7-bet window is **+3.5 bps net** (69% wins), and the trades cluster by regime: the early losers happened at BTC ~$63-66k, while the ~$77-81k trades (e.g. +48.7, +25.9, +16.2, +13.0 bps) have mostly won.

**What changed vs last time.** Essentially nothing. Counts, means and the flat live signal are the same as the prior read. No new resolved trades pushed the picture either way.

**What the numbers do and don't tell us.** They do tell us the strategy has NOT demonstrated a reliable net edge live — cumulative PnL is negative. They do NOT tell us it's broken: this is a marginal signal (gross ~4 bps vs ~3.9 bps breakeven cost), 26 trades is a tiny sample, and single trades swing ±25-60 bps, so the mean is dominated by noise. The recent positive streak is equally unreliable as evidence of a 'fix.'

**Bottom line.** Marginal-by-design, negative so far live, but too thin to conclude degradation OR recovery. No action warranted. Note that `edge_search_survivors = 0` at the stricter 5-bps/both-venues bar — a standing reminder this is unlikely to be net-profitable after realistic costs. No profit should be assumed.
