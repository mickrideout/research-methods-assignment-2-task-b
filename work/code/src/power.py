"""Sample-size and power calculation for the Task B design (TB).

Design: two independent, randomised groups (pessimistic vs neutral framing), continuous
outcome (0-100 perceived ten-year ownership likelihood), two-sided test at alpha.
With equal group sizes and equal SDs, Welch's degrees of freedom equal Student's (2n - 2),
so the analytic power below applies to both; a seeded Monte Carlo check confirms it.

Usage:
  python3 src/power.py --d 0.5 --alpha 0.05 --power 0.80 \
      --out-md ../results/tables/TB-power.md --out-json ../results/tables/TB-power.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy import stats


def power_two_sample(d: float, n: int, alpha: float = 0.05) -> float:
    """Exact power of a two-sided two-sample t-test with n per group and effect size d."""
    df = 2 * n - 2
    ncp = d * np.sqrt(n / 2)
    t_crit = stats.t.ppf(1 - alpha / 2, df)
    upper = stats.nct.sf(t_crit, df, ncp)
    if not np.isfinite(upper):  # scipy's nct tail returns nan for large ncp, where power is ~1
        upper = 1.0 - stats.nct.cdf(t_crit, df, ncp)
        if not np.isfinite(upper):
            upper = 1.0
    lower = stats.nct.cdf(-t_crit, df, ncp)
    return float(min(1.0, upper + (lower if np.isfinite(lower) else 0.0)))


def n_for_power(d: float, alpha: float = 0.05, power: float = 0.80, n_max: int = 10_000) -> int:
    """Smallest n per group whose power reaches the target."""
    for n in range(2, n_max + 1):
        if power_two_sample(d, n, alpha) >= power:
            return n
    raise ValueError("target power not reached within n_max")


def min_detectable_d(n: int, alpha: float = 0.05, power: float = 0.80) -> float:
    """Smallest d detectable with the target power at n per group (bisection)."""
    lo, hi = 0.0, 5.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if power_two_sample(mid, n, alpha) >= power else (mid, hi)
    return hi


def simulated_power(d: float, n: int, alpha: float = 0.05, reps: int = 20_000, seed: int = 20261025) -> dict:
    """Monte Carlo power of Welch's t-test and the Mann-Whitney U test under normal data."""
    rng = np.random.default_rng(seed)
    a = rng.normal(d, 1.0, size=(reps, n))
    b = rng.normal(0.0, 1.0, size=(reps, n))
    p_welch = stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
    p_mwu = stats.mannwhitneyu(a, b, axis=1, alternative="two-sided").pvalue
    return {"welch": float(np.mean(p_welch < alpha)), "mann_whitney": float(np.mean(p_mwu < alpha)),
            "reps": reps, "seed": seed}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--d", type=float, default=0.5)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.80)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-json", required=True)
    a = ap.parse_args()

    n = n_for_power(a.d, a.alpha, a.power)
    grid = [{"d": d, "power": pw, "n_per_group": n_for_power(d, a.alpha, pw)}
            for d in (0.4, 0.5, 0.6) for pw in (0.80, 0.90)]
    at_n = {m: {"power_at_d": power_two_sample(a.d, m, a.alpha),
                "min_detectable_d": min_detectable_d(m, a.alpha, a.power)} for m in (60, n)}
    sim = simulated_power(a.d, n, a.alpha)

    res = {"design": "two independent groups, two-sided test", "alpha": a.alpha, "target_power": a.power,
           "d": a.d, "n_per_group": n, "total_n": 2 * n, "analytic_power_at_n": power_two_sample(a.d, n, a.alpha),
           "planned_n_comparison": at_n, "sensitivity": grid, "simulation_at_n": sim}
    Path(a.out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out_json).write_text(json.dumps(res, indent=2), encoding="utf-8")

    md = [
        f"Table: Required sample size for a two-sided two-sample t-test (alpha = {a.alpha}).",
        "",
        "| Effect size (Cohen's d) | Target power | n per group | Total N |",
        "|---|---|---|---|",
    ]
    md += [f"| {g['d']:.1f} | {g['power']:.2f} | {g['n_per_group']} | {2 * g['n_per_group']} |" for g in grid]
    md += ["",
           f"Primary design (d = {a.d}, power {a.power:.2f}): **{n} per group, {2 * n} in total** "
           f"(analytic power {res['analytic_power_at_n']:.3f}).",
           "",
           "| n per group | Power at d = 0.5 | Minimum detectable d (power 0.80) |",
           "|---|---|---|"]
    md += [f"| {m} | {v['power_at_d']:.3f} | {v['min_detectable_d']:.3f} |" for m, v in at_n.items()]
    md += ["",
           f"Monte Carlo check at n = {n} per group (normal data, equal SDs, {sim['reps']:,} replications, "
           f"seed {sim['seed']}): Welch's t-test power {sim['welch']:.3f}; Mann-Whitney U power {sim['mann_whitney']:.3f}.",
           ""]
    Path(a.out_md).write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
