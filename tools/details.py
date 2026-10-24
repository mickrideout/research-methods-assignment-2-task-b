#!/usr/bin/env python3
"""Read and validate the common details file (context/assignment.md).

Usage:
  python3 tools/details.py validate          # schema + consistency checks; exit 1 on errors
  python3 tools/details.py get assignment.due  # print one field (JSON for lists/maps)
  python3 tools/details.py path answers      # print paths.<name> relative to the project root
  python3 tools/details.py qids              # question IDs, one per line
  python3 tools/details.py question Q2       # one question's fields as JSON
  python3 tools/details.py open              # unresolved open questions

Convention: `null` means UNKNOWN and must be covered by an open question whose
`field` names it; "n/a" (or false/[] where typed) means NOT APPLICABLE.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import QID_PATTERN, ToolError, die, find_root, get_dotted, load_details  # noqa: E402

# Facts that must be known (or explicitly raised as an open question).
REQUIRED_FACTS = [
    "unit.code", "unit.name", "assignment.title", "assignment.due", "assignment.weighting_pct",
    "assignment.total_marks", "referencing.style", "format.file_type", "submission.method",
    "spelling", "code.required", "genai.policy", "genai.acknowledgement_required",
]
PER_QUESTION_FACTS = ["marks", "word_limit"]
REQUIRED_PATHS = ["details", "inputs", "extracted", "rubric_md", "rubric_yaml", "checklist_md",
                  "checklist_yaml", "answers", "questions_dir", "bibliography", "csl", "code_dir",
                  "results_dir", "results_manifest", "ai_log", "reports_dir", "export_dir",
                  "templates_dir", "tools_dir"]
ENUMS = {
    "spelling": {"en-AU", "en-GB", "en-US", "en-NZ", "en-CA"},
    "genai.policy": {"prohibited", "restricted", "permitted", "unclear"},
    "status": {"draft", "confirmed"},
}
QTYPES = {"written", "code", "mixed"}


def _get(d, key, default="__missing__"):
    try:
        return get_dotted(d, key)
    except (KeyError, IndexError, ValueError, TypeError):
        return default


def validate(d: dict, root: Path) -> tuple[list[str], list[str]]:
    err, warn = [], []
    oq = d.get("open_questions") or []
    unresolved = {o.get("field") for o in oq if o.get("answer") in (None, "")}
    covered = {o.get("field") for o in oq}

    for key in REQUIRED_FACTS:
        v = _get(d, key)
        if v == "__missing__":
            err.append(f"missing field: {key}")
        elif v is None and key not in covered:
            err.append(f"{key} is null (unknown) but no open question has field: {key}")
    for key, allowed in ENUMS.items():
        v = _get(d, key, None)
        if v is not None and v not in allowed:
            err.append(f"{key}={v!r} not in {sorted(allowed)}")

    qs = d.get("questions") or []
    if not qs:
        err.append("questions: list is empty")
    seen = set()
    for i, q in enumerate(qs):
        qid = q.get("id")
        if not qid or not re.fullmatch(QID_PATTERN, str(qid)):
            err.append(f"questions[{i}].id {qid!r} invalid (pattern {QID_PATTERN})")
            continue
        if qid in seen:
            err.append(f"duplicate question id {qid}")
        seen.add(qid)
        if qid == "AI-ACK":
            err.append("AI-ACK is reserved")
        for f in PER_QUESTION_FACTS:
            if f not in q:
                err.append(f"{qid}: missing {f}")
            elif q[f] is None and f"questions.{qid}.{f}" not in covered:
                err.append(f"{qid}.{f} is null but no open question has field: questions.{qid}.{f}")
        if q.get("type") not in QTYPES:
            err.append(f"{qid}.type must be one of {sorted(QTYPES)}")
        if not q.get("source"):
            warn.append(f"{qid}: no source (file#page) recorded")
    total = _get(d, "assignment.total_marks", None)
    marks = [q.get("marks") for q in qs]
    if isinstance(total, (int, float)) and all(isinstance(m, (int, float)) for m in marks) and marks:
        if abs(sum(marks) - total) > 1e-9:
            warn.append(f"question marks sum to {sum(marks)} but total_marks is {total} "
                        "(fine only if some marks are assignment-wide; say so in the body)")

    bands = d.get("grade_bands") or []
    mins = [b.get("min_pct") for b in bands]
    if not bands:
        err.append("grade_bands is empty")
    elif any(not isinstance(m, (int, float)) for m in mins):
        err.append("every grade band needs a numeric min_pct")
    else:
        if any(a <= b for a, b in zip(mins, mins[1:])):
            err.append("grade_bands must be ordered by strictly descending min_pct")
        if mins[-1] != 0:
            err.append("the lowest grade band must have min_pct: 0")

    wc = d.get("word_count") or {}
    from wordcount import KNOWN
    bad = set(wc.get("exclude") or []) - KNOWN
    if bad:
        err.append(f"word_count.exclude has unknown items {sorted(bad)}; known: {sorted(KNOWN)}")

    code = d.get("code") or {}
    if code.get("required") is True and not code.get("languages"):
        err.append("code.required is true but code.languages is empty")

    paths = d.get("paths") or {}
    for p in REQUIRED_PATHS:
        if p not in paths:
            err.append(f"paths.{p} missing")
    for p in ("details", "inputs", "templates_dir", "tools_dir"):
        if p in paths and not (root / paths[p]).exists():
            err.append(f"paths.{p} -> {paths[p]} does not exist")
    for p in ("answers", "rubric_yaml", "checklist_yaml", "bibliography", "ai_log", "csl"):
        if p in paths and not (root / paths[p]).exists():
            warn.append(f"paths.{p} -> {paths[p]} does not exist yet")

    for o in oq:
        if not o.get("id") or not o.get("question"):
            err.append(f"open question {o!r} needs id and question")
    blocking = [o["id"] for o in oq if o.get("blocking") and o.get("answer") in (None, "")]
    if blocking:
        warn.append(f"unresolved BLOCKING open questions: {', '.join(blocking)}")
    if unresolved - {None}:
        warn.append(f"{len([o for o in oq if o.get('answer') in (None, '')])} open question(s) unresolved")
    if d.get("status") == "confirmed" and unresolved - {None}:
        warn.append("status is 'confirmed' but open questions remain unresolved")
    return err, warn


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["validate", "get", "path", "qids", "question", "open"])
    ap.add_argument("arg", nargs="?")
    a = ap.parse_args()
    try:
        root = find_root()
        d = load_details(root)
    except ToolError as e:
        die(str(e))
    if a.command == "validate":
        err, warn = validate(d, root)
        for w in warn:
            print(f"WARN  {w}")
        for e in err:
            print(f"ERROR {e}")
        print(f"{len(err)} error(s), {len(warn)} warning(s)")
        sys.exit(1 if err else 0)
    if a.command == "qids":
        print("\n".join(q["id"] for q in d.get("questions") or []))
    elif a.command == "open":
        for o in d.get("open_questions") or []:
            if o.get("answer") in (None, ""):
                flag = "BLOCKING " if o.get("blocking") else ""
                print(f"{o.get('id')}: {flag}{o.get('question')} [affects: {', '.join(o.get('affects') or [])}]")
    elif not a.arg:
        die(f"'{a.command}' needs an argument")
    elif a.command == "path":
        v = (d.get("paths") or {}).get(a.arg)
        if v is None:
            die(f"paths.{a.arg} not set")
        print(v)
    elif a.command == "question":
        q = next((q for q in d.get("questions") or [] if q.get("id") == a.arg), None)
        if q is None:
            die(f"no question {a.arg}")
        print(json.dumps(q, indent=2, default=str))
    else:
        v = _get(d, a.arg)
        if v == "__missing__":
            die(f"no field {a.arg}")
        print(json.dumps(v, indent=2, default=str) if isinstance(v, (dict, list)) else v)


if __name__ == "__main__":
    main()
