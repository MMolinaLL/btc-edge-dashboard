"""
multi_timeframe.py — edge search in the MULTI-TIMEFRAME family.

Idea: resample the 5m bars up to a higher timeframe (HTF) — 15m (3 bars),
1h (12 bars), 4h (48 bars), 12h (144 bars) — to read a slower trend or a
support/resistance level, then place the next-5m-candle bet in alignment with
(or fading) that HTF context.

All higher-timeframe context is computed with ONLY past-and-current data:
rolling/expanding windows plus .shift(+k). Nothing reads df["close"].shift(-1)
or any future bar. signal[i] depends only on rows <= i.

Each fn(df) -> np.ndarray in {-1, 0, +1} aligned to df.index:
    +1 bet next 5m candle closes UP, -1 DOWN, 0 no bet.

Evaluate:
    python "...\\search_runner.py" --user "...\\search_user\\multi_timeframe.py" --cost-bps 2

NOTE (honest framing): exploratory analysis showed BTC 5m returns have strongly
negative lag-1 autocorrelation on Binance.US (~ -0.20) but ~0 on Coinbase. So
any "fade the 5m move" edge is a thin-book bid-ask-bounce artifact that does not
transfer to the deep Coinbase book. These strategies are the genuinely-motivated
HTF ideas; the runner's two-venue requirement is expected to reject most/all.
"""
import numpy as np
import pandas as pd

# Higher-timeframe horizons expressed in 5-minute bars.
BARS_15M = 3
BARS_1H = 12
BARS_4H = 48
BARS_12H = 144


def _ret(df):
    return df["close"].diff()


def htf_trend_align(df):
    """Trade the 5m candle WITH the 1h trend (HTF momentum / trend-following).

    HTF trend = sign of the 1h price change, read from the close 12 bars ago
    (a clean 1h-resampled direction). Bet that direction every bar.
    Pure trend-continuation; no 5m mean-reversion component.
    """
    c = df["close"]
    htf = np.sign(c - c.shift(BARS_1H))
    sig = htf.fillna(0).astype(int).values
    return sig


def htf_pullback_continuation(df):
    """With the 4h trend, but only enter after a 5m PULLBACK against it.

    When the slow (4h) trend is up and the last 5m candle ticked down (a dip),
    bet up — buy the dip in an uptrend. Symmetric for downtrends. This is a
    classic multi-timeframe pullback entry that does NOT just fade the last
    candle in isolation; it requires HTF agreement.
    """
    c = df["close"]
    r = _ret(df)
    htf = np.sign(c - c.shift(BARS_4H))
    last5 = np.sign(r)
    pull = (last5 == -htf) & (htf != 0)
    sig = np.where(pull.values, htf.values, 0)
    return np.nan_to_num(sig).astype(int)


def htf_extension_fade(df):
    """Fade an oversized 5m thrust that runs WITH the 1h trend (exhaustion).

    When the 1h trend is up and the latest 5m candle is an outsized up-move
    (> 1 rolling sigma of recent 5m returns), bet down — fade the extension.
    Combines HTF direction with a 5m magnitude filter. (Expected to look great
    on Binance.US and fail on Coinbase: the classic two-venue trap.)
    """
    c = df["close"]
    r = _ret(df)
    htf = np.sign(c - c.shift(BARS_1H))
    last5 = np.sign(r)
    vol = r.rolling(24).std()
    extend = (last5 == htf) & (htf != 0)
    big = r.abs() > 1.0 * vol
    cond = (extend & big).fillna(False).values
    sig = np.where(cond, -htf.values, 0)
    return np.nan_to_num(sig).astype(int)


def htf_alignment_stack(df):
    """Trade only when 15m, 1h AND 4h trends all agree (multi-TF confluence).

    Strong trend-following filter: act only when three timeframes point the same
    way, betting that direction. Fewer, higher-conviction trend bets.
    """
    c = df["close"]
    t15 = np.sign(c - c.shift(BARS_15M))
    t1h = np.sign(c - c.shift(BARS_1H))
    t4h = np.sign(c - c.shift(BARS_4H))
    agree_up = (t15 > 0) & (t1h > 0) & (t4h > 0)
    agree_dn = (t15 < 0) & (t1h < 0) & (t4h < 0)
    sig = np.zeros(len(df), dtype=int)
    sig[agree_up.values] = 1
    sig[agree_dn.values] = -1
    return sig


def htf_sr_bounce(df):
    """Bounce off a higher-timeframe support/resistance level (12h range).

    Build the 12h range from rolling high/low (shifted so only past bars are
    used). If the close sits in the bottom 15% of that range (near support),
    bet up; if in the top 15% (near resistance), bet down. A mean-reversion
    read of HTF S/R proximity rather than the immediately-prior 5m candle.
    """
    c = df["close"]
    hi = df["high"].rolling(BARS_12H).max().shift(1)
    lo = df["low"].rolling(BARS_12H).min().shift(1)
    rng = (hi - lo)
    pos = (c - lo) / rng  # 0 = at support, 1 = at resistance
    near_support = pos < 0.15
    near_resistance = pos > 0.85
    sig = np.zeros(len(df), dtype=int)
    sig[near_support.fillna(False).values] = 1
    sig[near_resistance.fillna(False).values] = -1
    return sig


STRATEGIES = {
    "htf_trend_align": htf_trend_align,
    "htf_pullback_continuation": htf_pullback_continuation,
    "htf_extension_fade": htf_extension_fade,
    "htf_alignment_stack": htf_alignment_stack,
    "htf_sr_bounce": htf_sr_bounce,
}
