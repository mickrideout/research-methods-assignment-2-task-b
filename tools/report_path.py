#!/usr/bin/env python3
"""Print a new, unused, timestamped report path (and create its folder).

Usage:
  python3 tools/report_path.py grading Q2        # reports/grading/Q2/20261019-143005.md
  python3 tools/report_path.py grading-assignment
  python3 tools/report_path.py compliance
  python3 tools/report_path.py environment
  python3 tools/report_path.py presubmission
  python3 tools/report_path.py --latest grading Q2   # newest existing report, or exit 1
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ToolError, die, find_root, load_details, path_of, rel, stamp  # noqa: E402

KINDS = {"grading": "grading/{qid}", "grading-assignment": "grading/assignment",
         "compliance": "compliance", "environment": "environment", "presubmission": "presubmission"}


def report_dir(kind: str, qid: str | None) -> Path:
    if kind not in KINDS:
        raise ToolError(f"unknown kind {kind}; one of {sorted(KINDS)}")
    if kind == "grading" and not qid:
        raise ToolError("grading needs a question id")
    if kind == "grading" and qid == "assignment":
        raise ToolError("'assignment' is reserved; use kind grading-assignment")
    root = find_root()
    return path_of(load_details(root), "reports_dir", root) / KINDS[kind].format(qid=qid)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind")
    ap.add_argument("qid", nargs="?")
    ap.add_argument("--latest", action="store_true")
    a = ap.parse_args()
    try:
        d = report_dir(a.kind, a.qid)
        if a.latest:
            files = sorted(d.glob("*.md")) if d.is_dir() else []
            if not files:
                sys.exit(1)
            print(rel(files[-1]))
            return
        d.mkdir(parents=True, exist_ok=True)
        base = stamp()
        p, n = d / f"{base}.md", 2
        while p.exists():
            p, n = d / f"{base}-{n}.md", n + 1
        print(rel(p))
    except ToolError as e:
        die(str(e))


if __name__ == "__main__":
    main()
