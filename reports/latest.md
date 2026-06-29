# 🟢 Idle (signal=0); 3-bet window net +0.4 bps — still far too thin to judge; BTC ~$60.3k

_Updated 2026-06-29 20:32 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $60,300, up ~$1k since last check. The rolling window now spans just 3 bets, carrying essentially no statistical signal either way.

## Status

The strategy is currently **idle** — `signal=0`, so there's no open position. BTC sits around **$60,330**, up roughly $1,000 from the ~$59,300 noted last time.

## What changed

The rolling window ticked from 2 bets to **3 bets**, and the headline number flipped from slightly negative (~-2.4 bps) to slightly positive: **+0.4 bps net** (3.4 bps gross minus 3.0 bps assumed cost), with 1/3 wins reported... actually win-rate shows 1.0 on this tiny window. The persistent trade ledger still shows **0 resolved trades** and 0.0 total bps — so nothing has fully closed out yet.

## What the numbers do and don't tell us

They tell us almost nothing about edge. Three bets is noise, not evidence. Recall the validated picture: the gross edge is only ~**4 bps/bet** against a ~**3.9 bps breakeven cost** — marginal, and likely *not* net-profitable after realistic costs. A +0.4 bps window is fully consistent with both a real (tiny) edge and pure luck. Notably, `edge_search_survivors=0`: nothing currently clears the stricter bar (positive net on both venues at 5 bps cost), a reminder this signal is fragile.

## Bottom line

No action needed and no alarm. The data is **too thin to judge** — we'd want dozens of resolved trades before drawing any conclusion. No profit is implied or guaranteed; treat this as a marginal candidate still under observation.
