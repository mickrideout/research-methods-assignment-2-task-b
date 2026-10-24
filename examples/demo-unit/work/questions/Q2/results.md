# Results: Q2

Written by run-experiments on 2026-10-21. Numbers are copied from the output files.

| Output | Shows | Manifest run | Key numbers |
|---|---|---|---|
| work/results/tables/Q2-rmse.md | RMSE vs reference for raw, w=3, w=7 | 20261019-095255-Q2-rmse-figure | raw 0.789; w=3 0.517; w=7 0.426 |
| work/results/figures/Q2-smoothing.png | observed, reference, w=3 and w=7 smoothed | same | n/a |
| (tests) | 4/4 supplied tests pass | 20261019-095253-Q2-tests | exit 0 |

Caveats: single fixed series (60 samples), so no variance across seeds. Edge handling: the window shrinks at the edges.
