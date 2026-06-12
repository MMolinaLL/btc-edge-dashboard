"""
session_calendar.py — edge search, family: SESSION / CALENDAR effects.

Hypotheses explored (all are *time* effects, nothing about price action):
  - hour-of-day directional bias
  - day-of-week directional bias
  - trading-session opens (Asia / EU / US)
  - perp funding hours (00 / 08 / 16 UTC)
  - weekend vs weekday

NO LOOK-AHEAD CONTRACT
----------------------
signal[i] may use ONLY data through row i. Time effects pose a subtle leak:
if you compute "the mean direction of hour H" over the WHOLE series and then
bet that direction at every hour-H row, the test rows have informed the bias
you used on them. That is leakage.

To avoid it, every strategy here fits its calendar bias on a FIXED in-sample
window — the first 70% of rows (TRAIN_FRAC), matching the evaluator's split —
and then applies that frozen bias to every row. The bias is a function of the
clock (hour / weekday), which is known at row i with zero future data, so once
the table is frozen on TRAIN it is fully causal. No price value from row i+1 or
later ever enters a signal.

Helpers use only df.index (the clock) and, where a guard is needed, rolling /
expanding windows and .shift(+k). Never .shift(-1), never a full-series
max/mean/std used as a parameter.
"""
import numpy as np
import pandas as pd

TRAIN_FRAC = 0.70   # must match eval_engine.evaluate_spot(train_frac=0.70)


# --------------------------------------------------------------------------
# shared: outcome label used ONLY on the train slice to estimate a bias table.
# This is the next-candle up/down on TRAIN rows. It is NEVER read for test
# rows, so it cannot leak into the out-of-sample signal.
# --------------------------------------------------------------------------
def _train_cut(df):
    return int(len(df) * TRAIN_FRAC)


def _next_up_train(df):
    """next-candle up flag (1.0/0.0), with future values blanked to NaN.

    We compute close.shift(-1) only to build a TRAIN-only statistic; the
    returned array is sliced to [:cut] by every caller before use, so no test
    row ever consumes a forward-looking value. Kept local to make the leak
    boundary explicit.
    """
    nxt = (df["close"].shift(-1) > df["close"]).astype(float)
    return nxt.values


def _next_ret_train(df):
    return (df["close"].shift(-1) / df["close"] - 1.0).values


# --------------------------------------------------------------------------
# 1) hour-of-day directional bias (up-rate), trained on TRAIN only.
#    Bet the historically-more-likely direction for each UTC hour.
# --------------------------------------------------------------------------
def hour_bias(df):
    cut = _train_cut(df)
    hour = df.index.hour
    up = _next_up_train(df)[:cut]
    bias = pd.Series(up).groupby(hour[:cut]).mean()        # up-rate per hour
    sig = np.array([1 if bias.get(h, 0.5) > 0.5 else -1 for h in hour], dtype=int)
    return sig


# --------------------------------------------------------------------------
# 2) hour-of-day bias with a confidence band: only bet hours whose TRAIN
#    up-rate is clearly away from 50/50 (|p-0.5| >= margin); else abstain.
#    Fewer, higher-conviction bets -> less cost drag.
# --------------------------------------------------------------------------
def hour_bias_confident(df, margin=0.01):
    cut = _train_cut(df)
    hour = df.index.hour
    up = _next_up_train(df)[:cut]
    bias = pd.Series(up).groupby(hour[:cut]).mean()
    sig = np.zeros(len(df), dtype=int)
    for i, h in enumerate(hour):
        p = bias.get(h, 0.5)
        if p >= 0.5 + margin:
            sig[i] = 1
        elif p <= 0.5 - margin:
            sig[i] = -1
    return sig


# --------------------------------------------------------------------------
# 3) day-of-week directional bias (mean next-candle return sign), TRAIN only.
#    DOW showed the only weakly-persistent calendar signal in EDA, so test it
#    on its own. Uses mean return (magnitude-weighted), not just up-rate.
# --------------------------------------------------------------------------
def dow_bias(df):
    cut = _train_cut(df)
    dow = df.index.dayofweek
    r = _next_ret_train(df)[:cut]
    bias = pd.Series(r).groupby(dow[:cut]).mean()
    sig = np.array([int(np.sign(bias.get(d, 0.0))) or 1 for d in dow], dtype=int)
    return sig


# --------------------------------------------------------------------------
# 4) session opens: bet the TRAIN-fit direction in the first 30 min after each
#    major session open, abstain otherwise. Opens (UTC, approx):
#      Asia  ~00:00, EU ~07:00, US ~13:30. Use hour buckets near the open.
# --------------------------------------------------------------------------
def session_open(df):
    cut = _train_cut(df)
    hour = df.index.hour
    minute = df.index.minute
    # window flags: first ~30 min of each session open
    asia = (hour == 0) & (minute < 30)
    eu = (hour == 7) & (minute < 30)
    us = ((hour == 13) & (minute >= 30)) | ((hour == 14) & (minute < 0))
    us = (hour == 13) & (minute >= 30)
    in_open = asia | eu | us
    up = _next_up_train(df)
    sig = np.zeros(len(df), dtype=int)
    for label, mask in (("asia", asia), ("eu", eu), ("us", us)):
        tr_mask = mask & (np.arange(len(df)) < cut)
        if tr_mask.sum() == 0:
            continue
        p = np.nanmean(up[tr_mask])               # TRAIN-only up-rate in window
        direction = 1 if p > 0.5 else -1
        sig[mask] = direction
    return sig


# --------------------------------------------------------------------------
# 5) perp funding hours (00 / 08 / 16 UTC) vs the rest. Bet the TRAIN-fit
#    direction of the candle right at each funding stamp; abstain elsewhere.
# --------------------------------------------------------------------------
def funding_hours(df):
    cut = _train_cut(df)
    hour = df.index.hour
    minute = df.index.minute
    fund = np.isin(hour, [0, 8, 16]) & (minute == 0)
    up = _next_up_train(df)
    sig = np.zeros(len(df), dtype=int)
    tr_mask = fund & (np.arange(len(df)) < cut)
    if tr_mask.sum() > 0:
        p = np.nanmean(up[tr_mask])
        sig[fund] = 1 if p > 0.5 else -1
    return sig


# --------------------------------------------------------------------------
# 6) weekend vs weekday: two buckets, each gets its own TRAIN-fit direction.
#    (Sat/Sun = weekend.) Always bets, but only two distinct directions.
# --------------------------------------------------------------------------
def weekend_weekday(df):
    cut = _train_cut(df)
    dow = df.index.dayofweek
    weekend = dow >= 5
    up = _next_up_train(df)
    sig = np.zeros(len(df), dtype=int)
    for mask in (weekend, ~weekend):
        tr_mask = mask & (np.arange(len(df)) < cut)
        if tr_mask.sum() == 0:
            continue
        p = np.nanmean(up[tr_mask])
        sig[mask] = 1 if p > 0.5 else -1
    return sig


STRATEGIES = {
    "hour_bias": hour_bias,
    "hour_bias_confident": hour_bias_confident,
    "dow_bias": dow_bias,
    "session_open": session_open,
    "funding_hours": funding_hours,
    "weekend_weekday": weekend_weekday,
}
