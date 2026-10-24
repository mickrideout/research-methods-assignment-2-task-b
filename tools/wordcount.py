#!/usr/bin/env python3
"""Count words per answer section using the spec's counting rules.

Rules come from `word_count.exclude` in context/assignment.md. Supported
exclusions: headings, code_blocks, inline_code, tables, captions, citations,
references, footnotes, quotes, math. HTML comments (markers, meta lines) and
pandoc div fences are never counted. Tokens made only of punctuation are not
words. When citations are counted, each citation key counts as two words
(author + year), approximating the rendered in-text citation.

Usage:
  python3 tools/wordcount.py                 # every section, table output
  python3 tools/wordcount.py Q1 Q2 --json    # selected sections, JSON
  python3 tools/wordcount.py --text draft.md # count a loose file
  python3 tools/wordcount.py --exclude headings,citations ...  # override rules
Exit status 1 if any counted section is over its limit (plus tolerance).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import RESERVED_SECTIONS, ToolError, die, find_root, load_details, path_of  # noqa: E402
import _sections  # noqa: E402

KNOWN = {"headings", "code_blocks", "inline_code", "tables", "captions", "citations",
         "references", "footnotes", "quotes", "math"}
REF_HEADING = re.compile(r"^(#{1,6})\s*(references|reference list|bibliography|works cited)\s*(\{.*\})?\s*$", re.I)
HEADING = re.compile(r"^(#{1,6})\s")
CITE_BRACKET = re.compile(r"\[([^\[\]]*@[A-Za-z0-9_][^\[\]]*)\]")
CITE_KEY = re.compile(r"-?@([A-Za-z0-9_][\w:.#$%&+?<>~/-]*)")
PUNCT_ONLY = re.compile(r"^[\W_]+$", re.U)


def count_words(text: str, exclude: set[str]) -> int:
    unknown = exclude - KNOWN
    if unknown:
        raise ToolError(f"unknown word_count exclusions: {sorted(unknown)} (known: {sorted(KNOWN)})")
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    lines, out = text.splitlines(), []
    in_fence, fence = False, ""
    skip_level = 0  # inside an excluded references section of this heading level
    for line in lines:
        s = line.strip()
        m = re.match(r"^(`{3,}|~{3,})", s)
        if in_fence:
            if s.startswith(fence):
                in_fence = False
            elif "code_blocks" not in exclude:
                out.append(line)
            continue
        if m:
            in_fence, fence = True, m.group(1)
            continue
        h = HEADING.match(s)
        if skip_level:
            if h and len(h.group(1)) <= skip_level:
                skip_level = 0
            else:
                continue
        if "references" in exclude and REF_HEADING.match(s):
            skip_level = len(REF_HEADING.match(s).group(1))
            continue
        if s.startswith(":::"):
            continue
        if h:
            if "headings" in exclude:
                continue
            line = s[len(h.group(1)):]
            line = re.sub(r"\{[^}]*\}\s*$", "", line)
        if s.startswith("|") or re.match(r"^\+[-=+:]+\+$", s):
            if "tables" in exclude:
                continue
            line = line.replace("|", " ")
        if re.match(r"^Table:\s", s) and "captions" in exclude:
            continue
        if re.match(r"^\[\^[^\]]+\]:", s):
            if "footnotes" in exclude:
                continue
            line = re.sub(r"^\s*\[\^[^\]]+\]:", " ", line)
        if s.startswith(">"):
            if "quotes" in exclude:
                continue
            line = re.sub(r"^\s*(>\s?)+", "", line)
        out.append(line)
    t = "\n".join(out)
    # images: ![caption](path){attrs}
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)(\{[^}]*\})?",
               lambda m: " " if "captions" in exclude else f" {m.group(1)} ", t)
    t = re.sub(r"\[\^[^\]]+\]", " ", t)  # footnote refs
    # citations
    def cite(m):
        if "citations" in exclude:
            return " "
        inner = m.group(1)
        keys = CITE_KEY.findall(inner)
        rest = CITE_KEY.sub(" ", inner).replace(";", " ")
        return " " + " ".join("Author Year" for _ in keys) + " " + rest + " "
    t = CITE_BRACKET.sub(cite, t)
    t = re.sub(r"(?<![\w.])@[A-Za-z0-9_][\w:.#$%&+?<>~/-]*",
               lambda m: " " if "citations" in exclude else " Author Year ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r" \1 ", t)  # links -> text
    if "math" in exclude:
        t = re.sub(r"\$\$.*?\$\$|\$[^$\n]+\$", " ", t, flags=re.S)
    else:
        t = re.sub(r"\$\$.*?\$\$|\$[^$\n]+\$", " MATH ", t, flags=re.S)
    if "inline_code" in exclude:
        t = re.sub(r"`[^`\n]+`", " ", t)
    t = re.sub(r"^\s*([-*+]|\d+[.)])\s+", " ", t, flags=re.M)  # list markers
    t = re.sub(r"[*_`~]+", "", t)  # emphasis / code ticks
    return sum(1 for tok in t.split() if not PUNCT_ONLY.match(tok))


def rules(details: dict, override: str | None) -> tuple[set[str], float]:
    wc = details.get("word_count") or {}
    excl = set(override.split(",")) if override is not None else set(wc.get("exclude") or [])
    excl.discard("")
    return excl, float(wc.get("tolerance_pct") or 0)


def section_counts(details: dict, data: bytes, exclude: set[str], tol: float, ids=None):
    spans = _sections.parse(data)
    limits = {q["id"]: q.get("word_limit") for q in details.get("questions") or []}
    rows = []
    for sid in ids or [s for s in spans if s not in RESERVED_SECTIONS]:
        if sid not in spans:
            raise ToolError(f"no section {sid} in answer file")
        words = count_words(_sections.inner_text(data, spans[sid]), exclude)
        limit = limits.get(sid)
        status = "no limit"
        if isinstance(limit, (int, float)) and limit:
            allowed = limit * (1 + tol / 100)
            status = "OVER" if words > allowed else ("OK (near limit)" if words > 0.95 * limit else "OK")
        rows.append({"id": sid, "words": words, "limit": limit if isinstance(limit, (int, float)) else None,
                     "tolerance_pct": tol, "status": status})
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--file", help="answer file (default: paths.answers)")
    ap.add_argument("--text", help="count words in this file as a whole instead")
    ap.add_argument("--exclude", help="comma-separated exclusions overriding word_count.exclude")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        root = find_root()
        details = load_details(root)
        exclude, tol = rules(details, a.exclude)
        if a.text:
            n = count_words(Path(a.text).read_text(encoding="utf-8"), exclude)
            print(json.dumps({"file": a.text, "words": n}) if a.json else n)
            return
        f = Path(a.file) if a.file else path_of(details, "answers", root)
        rows = section_counts(details, f.read_bytes(), exclude, tol, a.ids or None)
    except (ToolError, OSError) as e:
        die(str(e))
    total_limit = (details.get("word_count") or {}).get("total_limit")
    total = sum(r["words"] for r in rows)
    if a.json:
        print(json.dumps({"exclude": sorted(exclude), "sections": rows, "total": total,
                          "total_limit": total_limit}, indent=2))
    else:
        print(f"Excluded from count: {', '.join(sorted(exclude)) or 'nothing'}; tolerance {tol:g}%")
        print(f"{'Section':<10} {'Words':>6} {'Limit':>6}  Status")
        for r in rows:
            print(f"{r['id']:<10} {r['words']:>6} {str(r['limit'] or '-'):>6}  {r['status']}")
        print(f"{'TOTAL':<10} {total:>6} {str(total_limit or '-'):>6}")
    over = any(r["status"] == "OVER" for r in rows) or (
        isinstance(total_limit, (int, float)) and total_limit and total > total_limit * (1 + tol / 100))
    sys.exit(1 if over else 0)


if __name__ == "__main__":
    main()
