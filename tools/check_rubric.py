#!/usr/bin/env python3
"""Validate the enhanced rubric and requirements checklist (YAML) before graders use them.

Usage:
  python3 tools/check_rubric.py            # validates paths.rubric_yaml and paths.checklist_yaml
  python3 tools/check_rubric.py --json

Errors (exit 1): schema problems, unknown question IDs, uncovered questions,
weights not summing to total_marks, missing levels, bad mark ranges, additions
without sources, sources pointing at files that do not exist.
Warnings: original wording not found verbatim in extracted text (often PDF
line-wrapping), criteria with no evidence/pitfalls, empty checklist.
Source format: `inputs/<path>#p.N` (or #slide.N, #para.N, #table.N, #cell.N, #line.N, #section-name).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml  # noqa: E402
from _common import ToolError, die, find_root, load_details, path_of  # noqa: E402

STRENGTHS = {"must", "should"}


def norm(s: str) -> str:
    s = re.sub(r"^## \[[^\]]+\]\s*$", " ", s, flags=re.M)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


class Checker:
    def __init__(self, root: Path, details: dict):
        self.root, self.d = root, details
        self.err, self.warn = [], []
        self.qids = {q["id"] for q in details.get("questions") or [] if q.get("id")}
        self.extracted = path_of(details, "extracted", root)

    def source_ok(self, src, where: str) -> bool:
        if not src or not isinstance(src, str):
            self.err.append(f"{where}: missing source")
            return False
        path = src.split("#", 1)[0]
        if not (self.root / path).exists():
            self.err.append(f"{where}: source file not found: {path}")
            return False
        if "#" not in src and not path.endswith((".md", ".txt")):
            self.warn.append(f"{where}: source {src} has no page/slide locator")
        return True

    def applies(self, items, where: str) -> set:
        if not isinstance(items, list) or not items:
            self.err.append(f"{where}: applies_to must be a non-empty list of question IDs or [ALL]")
            return set()
        if items == ["ALL"]:
            return set(self.qids)
        bad = [i for i in items if i not in self.qids]
        if bad:
            self.err.append(f"{where}: unknown question IDs {bad}")
        return set(items) & self.qids

    def verbatim(self, text: str, src: str, where: str):
        if not text or not src:
            return
        path = src.split("#", 1)[0]
        rel_in = path.split("/", 1)[1] if "/" in path else path
        candidates = [self.extracted / f"{rel_in}.md", self.root / path]
        hay = ""
        for c in candidates:
            if c.exists() and c.suffix in (".md", ".txt"):
                hay = norm(c.read_text(encoding="utf-8", errors="replace"))
                break
        if not hay:
            self.warn.append(f"{where}: cannot verify verbatim wording (no extracted text for {path})")
        elif norm(text) not in hay:
            self.warn.append(f"{where}: original wording not found verbatim in {path} (check for paraphrase)")

    def rubric(self, r: dict):
        total = (self.d.get("assignment") or {}).get("total_marks")
        levels = r.get("levels")
        if not isinstance(levels, list) or not levels:
            self.err.append("rubric: 'levels' must list performance levels, highest first")
            levels = []
        crit = r.get("criteria") or []
        if not crit:
            self.err.append("rubric: no criteria")
        ids, covered, weight_sum = set(), set(), 0.0
        for i, c in enumerate(crit):
            cid = c.get("id") or f"criteria[{i}]"
            w = f"rubric {cid}"
            if cid in ids:
                self.err.append(f"{w}: duplicate id")
            ids.add(cid)
            for f in ("name", "original_wording", "original_source", "weight", "applies_to", "levels"):
                if c.get(f) in (None, "", []):
                    self.err.append(f"{w}: missing {f}")
            self.source_ok(c.get("original_source"), f"{w}.original_source")
            self.verbatim(c.get("original_wording"), c.get("original_source"), f"{w}.original_wording")
            covered |= self.applies(c.get("applies_to"), w)
            weight = c.get("weight")
            if isinstance(weight, (int, float)):
                weight_sum += weight
            got = [lv.get("level") for lv in c.get("levels") or []]
            if got != levels:
                self.err.append(f"{w}: levels {got} must equal rubric levels {levels} in order")
            prev_lo = None
            for lv in c.get("levels") or []:
                lw = f"{w} level {lv.get('level')}"
                m = lv.get("marks")
                if not (isinstance(m, list) and len(m) == 2 and all(isinstance(x, (int, float)) for x in m)
                        and m[0] <= m[1]):
                    self.err.append(f"{lw}: marks must be [min, max]")
                else:
                    if isinstance(weight, (int, float)) and (m[0] < 0 or m[1] > weight):
                        self.err.append(f"{lw}: marks {m} outside 0..{weight}")
                    if prev_lo is not None and m[1] > prev_lo:
                        self.err.append(f"{lw}: max {m[1]} overlaps the level above (min {prev_lo})")
                    prev_lo = m[0]
                if not lv.get("observable"):
                    self.err.append(f"{lw}: no observable descriptors")
                for j, s in enumerate(lv.get("sources") or []):
                    self.source_ok(s, f"{lw}.sources[{j}]")
                if lv.get("observable") and not lv.get("sources") and not lv.get("original"):
                    self.err.append(f"{lw}: additions need sources (or 'original' wording)")
            for kind in ("evidence", "pitfalls"):
                items = c.get(kind) or []
                if not items:
                    self.warn.append(f"{w}: no {kind}")
                for j, it in enumerate(items):
                    if not isinstance(it, dict) or not it.get("text"):
                        self.err.append(f"{w}.{kind}[{j}]: needs text and source")
                    else:
                        self.source_ok(it.get("source"), f"{w}.{kind}[{j}]")
        unit = r.get("weight_unit", "marks")
        target = 100 if unit == "percent" else total
        if isinstance(target, (int, float)) and abs(weight_sum - target) > 1e-6:
            self.err.append(f"rubric: criterion weights sum to {weight_sum:g}, expected {target} ({unit})")
        missing = self.qids - covered
        if missing:
            self.err.append(f"rubric: questions not covered by any criterion: {sorted(missing)}")
        for j, cf in enumerate(r.get("conflicts") or []):
            if not cf.get("description") or not cf.get("resolution"):
                self.err.append(f"rubric conflicts[{j}]: needs description and resolution")
            for s in cf.get("sources") or []:
                self.source_ok(s, f"rubric conflicts[{j}]")
        return ids

    def checklist(self, c: dict):
        items = c.get("items") or []
        if not items:
            self.warn.append("checklist: no items")
        seen = set()
        for i, it in enumerate(items):
            iid = it.get("id") or f"items[{i}]"
            w = f"checklist {iid}"
            if iid in seen:
                self.err.append(f"{w}: duplicate id")
            seen.add(iid)
            if not it.get("text"):
                self.err.append(f"{w}: missing text")
            if it.get("strength") not in STRENGTHS:
                self.err.append(f"{w}: strength must be one of {sorted(STRENGTHS)}")
            self.applies(it.get("applies_to"), w)
            if self.source_ok(it.get("source"), w) and it.get("verbatim"):
                self.verbatim(it["verbatim"], it["source"], f"{w}.verbatim")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        root = find_root()
        d = load_details(root)
        ck = Checker(root, d)
        for key, fn in (("rubric_yaml", ck.rubric), ("checklist_yaml", ck.checklist)):
            p = path_of(d, key, root)
            if not p.exists():
                ck.err.append(f"{key}: {p.relative_to(root)} does not exist")
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            if not isinstance(data, dict):
                ck.err.append(f"{key}: not a YAML mapping")
                continue
            fn(data)
    except (ToolError, yaml.YAMLError) as e:
        die(str(e))
    if a.json:
        print(json.dumps({"errors": ck.err, "warnings": ck.warn}, indent=2))
    else:
        for w in ck.warn:
            print(f"WARN  {w}")
        for e in ck.err:
            print(f"ERROR {e}")
        print(f"{len(ck.err)} error(s), {len(ck.warn)} warning(s)")
    sys.exit(1 if ck.err else 0)


if __name__ == "__main__":
    main()
