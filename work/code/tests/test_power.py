import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from power import min_detectable_d, n_for_power, power_two_sample, simulated_power  # noqa: E402


def test_power_at_zero_effect_equals_alpha():
    assert power_two_sample(0.0, 50, 0.05) == pytest.approx(0.05, abs=1e-9)


def test_power_increases_with_n_and_d():
    assert power_two_sample(0.5, 40) < power_two_sample(0.5, 80)
    assert power_two_sample(0.3, 60) < power_two_sample(0.6, 60)


def test_n_for_power_is_minimal():
    n = n_for_power(0.5, 0.05, 0.80)
    assert power_two_sample(0.5, n) >= 0.80 > power_two_sample(0.5, n - 1)


def test_analytic_matches_simulation():
    n = n_for_power(0.5, 0.05, 0.80)
    sim = simulated_power(0.5, n, reps=20_000, seed=1)
    assert sim["welch"] == pytest.approx(power_two_sample(0.5, n), abs=0.015)


@pytest.mark.parametrize("n", [20, 60, 64, 130])
def test_min_detectable_d_inverts_power(n):
    d = min_detectable_d(n, 0.05, 0.80)
    assert 0 < d < 2
    assert power_two_sample(d, n) == pytest.approx(0.80, abs=1e-6)


@pytest.mark.parametrize("d", [2.0, 2.5, 4.5])
def test_power_finite_for_large_effects(d):
    p = power_two_sample(d, 64)
    assert p == pytest.approx(1.0, abs=1e-6)
