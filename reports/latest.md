# 🟢 Signal flat (0); 7-trade ledger now net -17 bps/bet after a -61 bps outlier, but sample still too thin — BTC ~$62.7k

_Updated 2026-07-31 16:02 UTC · model claude-opus-4-8_

**Regime:** Signal is currently flat (signal=0), so no new exposure right now. The live ledger leans clearly negative, but with only 7 resolved trades it remains well inside the noise band for a strategy whose expected gross edge is just ~4 bps/bet.

**How it's doing:** No live position at the moment (signal=0). The strategy remains what we always said it was — marginal, with a gross edge of only ~4 bps/bet against a ~3.9 bps breakeven cost. That leaves essentially no room for error after realistic costs.

**What changed since last time:** The ledger grew from 6 to 7 resolved trades. The single new trade (2026-07-31) was a sizeable loser at **-60.9 bps**, dragging the ledger mean to **-17.2 bps/bet** (total **-120.2 bps**, win rate 1-of-7 ≈ 14%). The broader rolling window of 15 bets is less dramatic: 60% wins, gross **+0.7 bps**, net **-2.3 bps** after a 3 bps cost assumption.

**What the numbers do and don't tell us:** They tell us recent live results are negative and lumpy — dominated by a couple of large adverse moves (-61, -23, -18 bps). They do **not** tell us the edge is broken. Seven trades is far too few to distinguish a genuine breakdown from ordinary bad luck; a strategy with a ~4 bps edge can easily print a stretch like this by chance. One -61 bps outlier alone swings the whole mean.

**Honest bottom line:** Too thin to judge, and leaning negative. This was always a borderline, probably-not-net-profitable candidate (edge search still finds 0 survivors). Keep collecting data; if dozens of trades stay materially negative, we escalate to watch/alert. No profit is implied or expected here.
