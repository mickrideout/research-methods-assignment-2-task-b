# Experiment hygiene

- **Reproducible:** fixed seeds, pinned dependencies (lock file in `work/code/`), commands
  recorded by `tools/run_logged.py`, and the git commit captured. Commit code before important runs
  so `git_dirty: false`.
- **Honest:** report every configuration you tried that informs a claim, not just the best.
  Report variance (mean ± sd over seeds) when results are stochastic. Never tune on test data.
- **Traceable:** every number in an answer comes from an output file listed in the manifest.
  Copy numbers from that file. If a figure is regenerated, cite the new run.
- **Proportionate:** start with the smallest run that answers the question (subset, fewer
  epochs) and scale only with approval. Respect `code.max_run_minutes`.
- **Separated:** `inputs/starter/` and `inputs/data/` are read-only. Derived data goes to
  `work/results/` (or `work/code/` cache folders that are git-ignored).
- **Presentable:** figures have axis labels and units, legible fonts and a caption-ready
  title in results.md. Tables are Markdown with units in the headers.
