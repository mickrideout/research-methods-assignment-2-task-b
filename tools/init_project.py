#!/usr/bin/env python3
"""Set up a fresh assignment project from the template. Idempotent: never overwrites.

Copies fill-in templates to their working locations and creates the agent
discovery symlinks. The answer file is NOT created here; it needs the question
list, so define-details runs `answer_section.py init` once the details are filled.

Usage:
  python3 tools/init_project.py            # from the project root
  python3 tools/init_project.py --dry-run
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import find_root  # noqa: E402

COPIES = [  # template -> destination (defaults; later changes live in paths.*)
    ("templates/assignment.md", "context/assignment.md"),
    ("templates/ai-use-log.md", "work/ai-use-log.md"),
    ("templates/references.bib", "work/references/references.bib"),
]
DIRS = ["context/extracted", "work/questions", "work/code", "work/results/figures",
        "work/results/tables", "work/results/logs", "answers", "export",
        "reports/grading/assignment", "reports/compliance", "reports/environment", "reports/presubmission"]
LINKS = [  # link -> target (relative)
    (".claude/skills", "../skills"),
    ("CLAUDE.md", "AGENTS.md"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    root = find_root()
    act = (lambda msg, fn: print(f"would {msg}")) if a.dry_run else (lambda msg, fn: (fn(), print(msg)))
    for d in DIRS:
        p = root / d
        if not p.is_dir():
            act(f"create {d}/", lambda p=p: p.mkdir(parents=True, exist_ok=True))
    for src, dst in COPIES:
        s, t = root / src, root / dst
        if t.exists():
            print(f"keep   {dst} (exists)")
        elif not s.exists():
            print(f"skip   {dst} (template {src} missing)")
        else:
            act(f"copy   {src} -> {dst}", lambda s=s, t=t: (t.parent.mkdir(parents=True, exist_ok=True),
                                                           shutil.copyfile(s, t)))
    for link, target in LINKS:
        p = root / link
        if p.is_symlink() or p.exists():
            print(f"keep   {link} (exists)")
        else:
            act(f"link   {link} -> {target}", lambda p=p, target=target: (p.parent.mkdir(parents=True, exist_ok=True),
                                                                        os.symlink(target, p)))
    print("next: put files in inputs/, then run the define-details skill")


if __name__ == "__main__":
    main()
