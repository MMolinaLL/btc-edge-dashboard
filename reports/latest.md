# 🟡 Negative rolling window persists: 21 bets, gross -8.8 bps, net -11.8 bps after 3 bps cost; BTC ~$59.6k, flat

_Updated 2026-06-26 10:30 UTC · model claude-opus-4-8_

> **WATCH:** Rolling window gross edge still negative (-8.8 bps over 21 bets) vs ~+4 bps expected; small sample, keep watching.

**Regime:** Strategy is flat (signal=0) with no open position and BTC near $59,600. The rolling window remains negative both gross and net — an early degradation sign, not yet conclusive.

**How it's doing:** The current rolling window covers just **21 bets**, with a **42.9% win rate**, **gross −8.76 bps**, and **net −11.76 bps** after 3 bps of cost. That is the wrong sign: this signal was only ever expected to earn about **+4 bps gross per bet**, and even that is marginal versus its ~3.9 bps breakeven cost. Right now the window is losing money both before and after costs.

**What changed:** Last check showed 26 bets at gross −9.2 / net −12.2 bps. The window has rolled forward (now 21 bets) but the picture is essentially the same — still negative, slightly less negative. BTC is roughly flat (~$59.6k vs ~$59.4k). No position is open (signal=0), and the persistent ledger has **0 resolved trades**, so there's no realized P&L to confirm anything yet.

**What the numbers do and don't tell us:** 21 bets is a tiny sample. With a ~4 bps edge, normal noise easily swings a window this small into the red, so this is **not** proof the edge is gone. But two consecutive negative windows is worth flagging. Separately, the offline edge search now finds **0 survivors** meeting the bar (net positive on both venues at 5 bps cost), reinforcing that this strategy was always marginal.

**Bottom line:** Stay cautious, not panicked. The edge was thin to begin with and is currently not showing up live. Keep watching; do not assume profitability.
