"""
Template for an edge-search strategy file.

Expose a dict STRATEGIES = {name: fn}, where each fn takes a DataFrame `df` and
returns a signal array in {-1, 0, +1}, aligned to df.index:
    +1 = bet the next 5m candle closes UP
    -1 = bet it closes DOWN
     0 = no bet

df columns: open, high, low, close, volume   (index = UTC timestamp)

HARD RULE — NO LOOK-AHEAD: signal[i] may use ONLY data through df.iloc[i]
(close, and earlier). Never use df["close"].shift(-1) or any future value in a
signal. The evaluator measures the NEXT candle as the outcome; if your signal
peeks at it, you'll manufacture a fake edge that the audit will reject.

Evaluate honestly (both venues, train/test split, net of cost):
    python "<abs path>/search_runner.py" --user "<abs path>/search_user/_template.py" --cost-bps 2
"""
import numpy as np


def example_meanrev(df):
    r = df["close"].diff()
    return (-np.sign(r)).fillna(0).astype(int).values


STRATEGIES = {
    "example_meanrev": example_meanrev,
}
