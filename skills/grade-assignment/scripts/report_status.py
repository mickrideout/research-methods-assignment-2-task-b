#!/usr/bin/env python3
"""List the latest grading report per question and whether it is still fresh.

A report is FRESH when its answer_sha256 matches the section's current content
hash (meta line excluded) and its rubric_sha256 matches the current rubric.yaml.

Usage (from the project root):
  python3 skills/grade-assignment/scripts/report_status.py          # table
  python3 skills/grade-assignment/scripts/report_status.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
sys.path.insert(0, str(TOOLS))
from _common import ToolError, die, find_root, load_details, path_of, rel, sha256_file, split_frontmatter  # noqa: E402
import _sections  # noqa: E402
import answer_section  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        root = find_root()
        d = load_details(root)
        data = path_of(d, "answers", root).read_bytes()
        spans = _sections.parse(data)
        rubric = path_of(d, "rubric_yaml", root)
        rubric_sha = sha256_file(rubric) if rubric.exists() else None
        reports = path_of(d, "reports_dir", root) / "grading"
    except (ToolError, OSError) as e:
        die(str(e))
    rows = []
    for q in d.get("questions") or []:
        qid = q["id"]
        files = sorted((reports / qid).glob("*.md")) if (reports / qid).is_dir() else []
        row = {"qid": qid, "marks_available": q.get("marks"), "report": None, "marks_awarded": None,
               "status": "NOT GRADED"}
        if qid not in spans:
            row["status"] = "NO SECTION"
        elif files:
            fm, _ = split_frontmatter(files[-1].read_text(encoding="utf-8"))
            current = answer_section.content_hash(data, spans[qid])
            stale = []
            if fm.get("answer_sha256") != current:
                stale.append("answer changed")
            if rubric_sha and fm.get("rubric_sha256") != rubric_sha:
                stale.append("rubric changed")
            row.update(report=rel(files[-1], root), marks_awarded=fm.get("marks_awarded"),
                       level=fm.get("overall_level"), status="STALE: " + ", ".join(stale) if stale else "FRESH")
        rows.append(row)
    if a.json:
        print(json.dumps(rows, indent=2))
        return
    print(f"{'QID':<8} {'Status':<32} {'Marks':>11}  Report")
    for r in rows:
        m = f"{r['marks_awarded'] if r['marks_awarded'] is not None else '-'}/{r['marks_available'] or '-'}"
        print(f"{r['qid']:<8} {r['status']:<32} {m:>11}  {r['report'] or '-'}")


if __name__ == "__main__":
    main()
