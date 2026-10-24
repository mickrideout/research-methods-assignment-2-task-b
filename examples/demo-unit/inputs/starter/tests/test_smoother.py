import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smoother import moving_average, rmse  # noqa: E402


def test_constant_series_unchanged():
    assert moving_average([2.0] * 6, 3) == [2.0] * 6


def test_centred_window():
    assert moving_average([0, 3, 6, 9, 12], 3)[2] == 6


def test_same_length():
    assert len(moving_average(list(range(10)), 7)) == 10


def test_rmse():
    assert math.isclose(rmse([0, 0], [3, 4]), math.sqrt(12.5))
