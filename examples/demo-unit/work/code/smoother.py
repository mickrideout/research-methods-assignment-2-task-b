"""DSCI9001 Assignment 2, Question 2: centred moving-average smoother (fictional example)."""
import math


def moving_average(values, window):
    """Return the centred moving average of `values` with an odd `window`.

    Edge handling: shrink the window at the edges so the output has the same length.
    """
    if window < 1 or window % 2 == 0:
        raise ValueError("window must be a positive odd integer")
    half = window // 2
    out = []
    for i in range(len(values)):
        lo, hi = max(0, i - half), min(len(values), i + half + 1)
        out.append(sum(values[lo:hi]) / (hi - lo))
    return out


def rmse(a, b):
    """Root-mean-square error between equal-length sequences."""
    if len(a) != len(b):
        raise ValueError("sequences must have equal length")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))
