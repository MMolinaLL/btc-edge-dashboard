# 🟢 Signal flat (0); live sample still tiny (5-10 trades), net slightly negative but too thin to judge — BTC ~$64.6k

_Updated 2026-07-26 15:06 UTC · model claude-opus-4-8_

**Regime:** Signal is currently inactive (signal=0) with no clear regime shift. The live sample is far too small to distinguish real edge decay from ordinary noise.

## How it's doing

The signal is currently **inactive** (signal=0), so nothing is being traded right now. BTC sits near **$64,645**.

The live track record is still tiny. The rolling window shows **10 bets, 50% win rate, gross +0.08 bps, net -2.9 bps** (at an assumed 3.0 bps cost). The resolved ledger holds just **5 trades, 20% wins, averaging -8.2 bps each (-41 bps total)**. Two losers dominate: -13.0 bps (2026-07-06) and -22.8 bps (2026-07-17). The most recent trade (2026-07-24) was a rare winner at +3.1 bps net.

## What changed vs last time

Essentially nothing material. Same flat signal, same too-thin sample. The prior read (none) still holds.

## What the numbers do and don't tell us

- **Do:** Recent live results have been negative, consistent with a strategy whose gross edge (~4 bps) barely clears its ~3.9 bps breakeven cost. It is marginal by design.
- **Don't:** With only 5-10 resolved trades, the numbers carry no statistical weight. One or two large moves swing the whole average. This is squarely in noise territory — you cannot conclude the edge is broken, nor that it works.

Separately, `edge_search_survivors=0` is a reminder that no variant cleared the stricter dual-venue 5 bps bar — this was never a confident money-maker.

## Bottom line

Too thin to judge. Results lean negative but are well within noise for such a small sample. Keep collecting data; no action warranted. Do not expect reliable profit from this marginal signal.
