"""
candle_microstructure.py — edge search in the CANDLE MICROSTRUCTURE family.

Family thesis: the *shape* of a 5-minute candle (body vs range, upper/lower
wick balance, gaps between candles, range expansion/contraction, inside/outside
bars) carries information about the next candle's direction.

Every signal here uses ONLY data through row i (rolling / expanding / shift(+k)
windows). No future values, no whole-series statistics, no parameters fit on the
full set. The evaluator measures the NEXT candle as the outcome.

Honest framing of what we expect (and find): most candle-shape edges on a thin
book (Binance.US) are bid-ask bounce — they look strong there but INVERT or
vanish on a deep book (Coinbase). The cross-venue requirement in search_runner
is designed to expose exactly that. The few features that ARE sign-consistent
across venues (gap fade, inside-bar fade) have gross edges well under 1 bp and
do not clear a realistic 2 bps round-trip cost.

Conventions:
  signal in {-1, 0, +1}: +1 bet next candle closes UP, -1 DOWN, 0 no bet.
  o,h,l,c,v columns; UTC index.
"""
import numpy as np
import pandas as pd


# --------------------------------------------------------------------------
# shared helpers (all backward-looking)
# --------------------------------------------------------------------------
def _parts(df):
    o = df["open"].astype(float)
    h = df["high"].astype(float)
    l = df["low"].astype(float)
    c = df["close"].astype(float)
    rng = (h - l)
    body = (c - o)
    upper = h - np.maximum(o, c)        # upper wick length
    lower = np.minimum(o, c) - l        # lower wick length
    return o, h, l, c, rng, body, upper, lower


def _finalize(sig, df):
    """Coerce to clean int array in {-1,0,+1}, aligned to df.index, no NaN."""
    s = pd.Series(sig, index=df.index)
    s = s.replace([np.inf, -np.inf], 0).fillna(0)
    return np.sign(s.values).astype(int)


# --------------------------------------------------------------------------
# 1. GAP FADE
#    The open vs the previous close is a "gap". Fade it, but only when the gap
#    is large relative to its own recent volatility (vol-normalised, past only).
#    This is the single feature whose sign is consistent across BOTH venues.
# --------------------------------------------------------------------------
def gap_fade(df, z_thresh=1.0, win=96):
    o, h, l, c, *_ = _parts(df)
    prev_c = c.shift(1)
    gap = (o - prev_c) / prev_c
    gstd = gap.shift(1).rolling(win).std()          # past-only scale
    gz = gap / gstd
    sig = np.where(gz > z_thresh, -1.0,
                   np.where(gz < -z_thresh, 1.0, 0.0))
    return _finalize(sig, df)


# --------------------------------------------------------------------------
# 2. WICK IMBALANCE FADE
#    A long lower wick (rejection of lower prices) vs a long upper wick.
#    Body/range and wick ratios. wick_imb = (lower - upper)/range.
#    Trade ONLY when imbalance is strong relative to its recent distribution.
# --------------------------------------------------------------------------
def wick_imbalance(df, thresh=0.5, win=48):
    o, h, l, c, rng, body, upper, lower = _parts(df)
    rng_safe = rng.replace(0, np.nan)
    imb = (lower - upper) / rng_safe                # +ve = long lower wick
    # require the candle to have a real range vs recent (avoid micro candles)
    med_rng = rng.shift(1).rolling(win).median()
    real = rng > med_rng
    # long lower wick (buyers stepped in low) -> lean UP; long upper -> DOWN
    sig = np.where(real & (imb > thresh), 1.0,
                   np.where(real & (imb < -thresh), -1.0, 0.0))
    return _finalize(sig, df)


# --------------------------------------------------------------------------
# 3. RANGE-EXPANSION FADE
#    When the current candle's range is much larger than its recent median
#    (a volatility burst), fade the body direction of that burst.
# --------------------------------------------------------------------------
def range_expansion_fade(df, mult=2.0, win=48):
    o, h, l, c, rng, body, *_ = _parts(df)
    med = rng.shift(1).rolling(win).median()
    big = rng > mult * med
    body_dir = np.sign(body)
    sig = np.where(big, -body_dir, 0.0)
    return _finalize(sig, df)


# --------------------------------------------------------------------------
# 4. INSIDE-BAR FADE
#    Inside bar = high < prev high AND low > prev low (compression / coil).
#    Fade the prior candle's body direction. This is the second feature whose
#    sign held up on both venues (though gross edge is tiny).
# --------------------------------------------------------------------------
def inside_bar_fade(df):
    o, h, l, c, rng, body, *_ = _parts(df)
    inside = (h < h.shift(1)) & (l > l.shift(1))
    prev_body_dir = np.sign(c.shift(1) - o.shift(1))
    sig = np.where(inside, -prev_body_dir, 0.0)
    return _finalize(sig, df)


# --------------------------------------------------------------------------
# 5. OUTSIDE-BAR FADE
#    Outside / engulfing bar = high > prev high AND low < prev low (range
#    expansion that swept both sides). Fade this candle's body direction.
# --------------------------------------------------------------------------
def outside_bar_fade(df):
    o, h, l, c, rng, body, *_ = _parts(df)
    outside = (h > h.shift(1)) & (l < l.shift(1))
    body_dir = np.sign(body)
    sig = np.where(outside, -body_dir, 0.0)
    return _finalize(sig, df)


# --------------------------------------------------------------------------
# 6. CLOSE-LOCATION FADE
#    Close-location value within the candle range (0 = at low, 1 = at high).
#    A close pinned near the high after the bar is often an over-extension;
#    fade it. (Strong on the thin book, ~zero on the deep book — included so
#    the cross-venue audit can show the bid-ask-bounce mirage explicitly.)
# --------------------------------------------------------------------------
def close_location_fade(df, hi=0.9, lo=0.1, win=48):
    o, h, l, c, rng, *_ = _parts(df)
    rng_safe = rng.replace(0, np.nan)
    clv = (c - l) / rng_safe
    med_rng = rng.shift(1).rolling(win).median()
    real = rng > 0.5 * med_rng                      # ignore micro candles
    sig = np.where(real & (clv > hi), -1.0,
                   np.where(real & (clv < lo), 1.0, 0.0))
    return _finalize(sig, df)


STRATEGIES = {
    "gap_fade": gap_fade,
    "wick_imbalance": wick_imbalance,
    "range_expansion_fade": range_expansion_fade,
    "inside_bar_fade": inside_bar_fade,
    "outside_bar_fade": outside_bar_fade,
    "close_location_fade": close_location_fade,
}
