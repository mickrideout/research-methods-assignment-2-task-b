#!/usr/bin/env python3
"""Run a command with full provenance and record its outputs in the results manifest.

Answers may only cite figures, tables and numbers that trace to a manifest entry.

Usage:
  python3 tools/run_logged.py --name baseline --qid Q2 \
      --outputs work/results/figures/q2-smoothing.png,work/results/tables/q2-rmse.md \
      [--cwd work/code] [--timeout-min 30] -- python3 src/smooth.py --seed 1

Writes:
  <results_dir>/logs/<timestamp>-<name>.log   header (command, cwd, git commit, Python) + stdout/stderr
  <results_manifest>                          appended run entry with output sha256s
Exit status is the command's (124 on timeout). Declared outputs that are
missing after the run are recorded as missing and make the run fail.
"""
from __future__ import annotations

import argparse
import platform
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml  # noqa: E402
from _common import ToolError, die, find_root, load_details, now, path_of, rel, sha256_file, stamp  # noqa: E402


def git_state(root: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True,
                                check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True,
                                    text=True).stdout.strip())
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="short run name, e.g. baseline")
    ap.add_argument("--qid", default="-")
    ap.add_argument("--outputs", default="", help="comma-separated output paths (relative to project root)")
    ap.add_argument("--cwd", help="working directory (default: paths.code_dir)")
    ap.add_argument("--timeout-min", type=float, help="default: code.max_run_minutes")
    ap.add_argument("--note", default="")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd[:1] == ["--"] else a.cmd
    if not cmd:
        die("no command given (put it after --)")
    try:
        root = find_root()
        d = load_details(root)
        results, manifest = path_of(d, "results_dir", root), path_of(d, "results_manifest", root)
        cwd = Path(a.cwd).resolve() if a.cwd else path_of(d, "code_dir", root)
    except ToolError as e:
        die(str(e))
    timeout = a.timeout_min or (d.get("code") or {}).get("max_run_minutes") or 30
    run_id = f"{stamp()}-{a.name}"
    log = results / "logs" / f"{run_id}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    commit, dirty = git_state(root)
    started, t0 = now(), time.monotonic()
    header = (f"# command: {' '.join(cmd)}\n# cwd: {rel(cwd, root)}\n# started: {started.isoformat()}\n"
              f"# git: {commit} dirty={dirty}\n# python: {platform.python_version()} ({sys.executable})\n"
              f"# platform: {platform.platform()}\n# timeout_min: {timeout}\n\n")
    with open(log, "w", encoding="utf-8") as f:
        f.write(header)
        f.flush()
        try:
            proc = subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, timeout=timeout * 60)
            code = proc.returncode
        except subprocess.TimeoutExpired:
            code = 124
            f.write(f"\n# TIMEOUT after {timeout} min\n")
        except OSError as e:
            code = 127
            f.write(f"\n# FAILED TO START: {e}\n")
    duration = round(time.monotonic() - t0, 2)
    outs = []
    for o in [x.strip() for x in a.outputs.split(",") if x.strip()]:
        p = root / o
        outs.append({"path": o, "sha256": sha256_file(p) if p.is_file() else None, "exists": p.is_file()})
    missing = [o["path"] for o in outs if not o["exists"]]
    entry = {"id": run_id, "name": a.name, "qid": a.qid, "command": cmd,
             "cwd": rel(cwd, root), "started": started.isoformat(), "duration_s": duration,
             "exit_code": code, "git_commit": commit, "git_dirty": dirty, "log": rel(log, root),
             "outputs": outs, "note": a.note,
             "status": "ok" if code == 0 and not missing else "failed"}
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) if manifest.exists() else None
    data = data or {"runs": []}
    data.setdefault("runs", []).append(entry)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("# Results manifest: written by tools/run_logged.py; do not edit by hand.\n"
                        + yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    print(f"run {entry['id']}: exit {code}, {duration}s, log {rel(log, root)}")
    if missing:
        print(f"MISSING declared outputs: {', '.join(missing)}")
    sys.exit(code if code else (1 if missing else 0))


if __name__ == "__main__":
    main()
