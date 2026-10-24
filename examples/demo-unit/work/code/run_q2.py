"""Compute RMSE for window sizes 3 and 7 and plot raw vs smoothed vs reference."""
import argparse
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from smoother import moving_average, rmse  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--table", required=True)
ap.add_argument("--figure", required=True)
a = ap.parse_args()

with open(a.data) as f:
    rows = list(csv.DictReader(f))
t = [int(r["t"]) for r in rows]
obs = [float(r["observed"]) for r in rows]
ref = [float(r["reference"]) for r in rows]

lines = ["| Window | RMSE vs reference |", "|---|---|", f"| raw (1) | {rmse(obs, ref):.3f} |"]
smoothed = {}
for w in (3, 7):
    smoothed[w] = moving_average(obs, w)
    lines.append(f"| {w} | {rmse(smoothed[w], ref):.3f} |")
with open(a.table, "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(t, obs, ".", color="0.6", label="observed")
ax.plot(t, ref, "-", color="black", label="reference")
for w, style in ((3, "--"), (7, "-")):
    ax.plot(t, smoothed[w], style, label=f"moving average (w={w})")
ax.set_xlabel("t (samples)")
ax.set_ylabel("sensor value")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(a.figure, dpi=150)
