#!/usr/bin/env python3
"""Append one row to the AI-use log (paths.ai_log). Every skill calls this once per run.

Usage:
  python3 tools/log_ai_use.py --skill answer-question --qid Q2 \
      --action "Drafted answer from plan and research notes" \
      --files answers/answers.md,work/questions/Q2/sources.md [--agent "agent/model name"]

The 'Your review' column is left blank for you to fill in; many units require
you to describe how you checked or changed AI output.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ToolError, die, find_root, load_details, now, path_of  # noqa: E402

HEADER = "| When | Skill | Question | Agent / model | What the AI did | Files touched | Your review |\n" \
         "|---|---|---|---|---|---|---|\n"


def cell(s: str) -> str:
    return (s or "-").replace("|", "\\|").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", required=True)
    ap.add_argument("--qid", default="-")
    ap.add_argument("--action", required=True)
    ap.add_argument("--files", default="-")
    ap.add_argument("--agent", default="-")
    a = ap.parse_args()
    try:
        root = find_root()
        log = path_of(load_details(root), "ai_log", root)
    except ToolError as e:
        die(str(e))
    if not log.exists():
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text("# AI-use log\n\n" + HEADER, encoding="utf-8")
    text = log.read_text(encoding="utf-8")
    if "| When | Skill |" not in text:
        text += ("\n" if not text.endswith("\n") else "") + "\n" + HEADER
    elif not text.endswith("\n"):
        text += "\n"
    row = "| " + " | ".join(cell(x) for x in (now().isoformat(timespec="minutes"), a.skill, a.qid,
                                               a.agent, a.action, a.files.replace(",", ", "))) + " |  |\n"
    log.write_text(text + row, encoding="utf-8")
    print(f"logged: {a.skill} {a.qid}")


if __name__ == "__main__":
    main()
