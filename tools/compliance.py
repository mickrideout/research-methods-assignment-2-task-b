#!/usr/bin/env python3
"""Deterministic compliance checks on the common answer file.

Checks: section markers, word limits, placeholders, stale meta lines,
citation keys vs bibliography, unverifiable bib entries, local links/images,
figures traceable to the results manifest, spelling convention, required
sections, AI acknowledgement, blocking open questions.

Usage:
  python3 tools/compliance.py                       # print Markdown report
  python3 tools/compliance.py --out "$(python3 tools/report_path.py compliance)"
  python3 tools/compliance.py --json
Exit status 1 if any check FAILs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml  # noqa: E402
from _common import ToolError, die, find_root, load_details, now, path_of, rel, sha256_bytes, sha256_file  # noqa: E402
import _sections  # noqa: E402
import answer_section  # noqa: E402
import wordcount  # noqa: E402

PLACEHOLDERS = re.compile(r"\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|lorem ipsum|_Not yet answered\._|"
                          r"\[citation needed\]|\?\?\?|\[INSERT[^\]]*\]", re.I)
IZE = re.compile(r"\b[A-Za-z]+(?:iz(?:e|es|ed|ing|ation|ations|er|ers)|yz(?:e|es|ed|ing))\b")
IZE_OK = {"size", "sizes", "sized", "sizing", "seize", "seizes", "seized", "seizing", "prize", "prizes",
          "maize", "baize", "capsize", "capsized", "downsize", "downsized", "downsizing", "resize", "resized",
          "resizing", "oversize", "oversized", "upsize", "assize", "outsize", "outsized"}
BIB_ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)(?=^\s*@\w+\s*\{|\Z)", re.S | re.M)


def strip_code(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"^(```|~~~).*?^\1\s*$", " ", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]+`", " ", text)


def cite_keys(text: str) -> list[str]:
    t = strip_code(text)
    t = re.sub(r"\]\([^)]*\)", "]", t)  # drop link targets (URLs may contain @)
    t = re.sub(r"<[^>]+@[^>]+>|\S+@\S+\.\w+", " ", t)  # emails
    return re.findall(r"(?<![\w.])-?@([A-Za-z0-9_][\w:.#$%&+?<>~/-]*[\w])", t)


def bib_entries(bib: Path) -> dict[str, dict]:
    if not bib.exists():
        return {}
    out = {}
    for m in BIB_ENTRY.finditer(bib.read_text(encoding="utf-8", errors="replace")):
        if m.group(1).lower() in ("comment", "string", "preamble"):
            continue
        fields = {k.lower() for k in re.findall(r"^\s*(\w+)\s*=", m.group(3), re.M)}
        out[m.group(2)] = {"type": m.group(1).lower(), "fields": fields}
    return out


def manifest_outputs(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = {}
    for run in data.get("runs") or []:
        for o in run.get("outputs") or []:
            out[o["path"]] = {"sha256": o.get("sha256"), "run": run.get("id"), "status": run.get("status")}
    return out


def run_checks(root: Path, d: dict) -> tuple[list[dict], dict]:
    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    answers = path_of(d, "answers", root)
    if not answers.exists():
        add("answer file", "FAIL", f"{rel(answers, root)} missing")
        return checks, {}
    data = answers.read_bytes()
    text = data.decode("utf-8")
    try:
        spans = _sections.parse(data)
    except ToolError as e:
        add("section markers", "FAIL", str(e))
        return checks, {"answers_sha256": sha256_bytes(data)}
    expected = answer_section._expected_ids(d)
    missing = [s for s in expected if s not in spans]
    extra = [s for s in spans if s not in expected]
    add("section markers", "FAIL" if missing or extra else "PASS",
        f"missing: {missing or 'none'}; unexpected: {extra or 'none'}")

    exclude, tol = wordcount.rules(d, None)
    rows = wordcount.section_counts(d, data, exclude, tol)
    over = [f"{r['id']} {r['words']}/{r['limit']}" for r in rows if r["status"] == "OVER"]
    total = sum(r["words"] for r in rows)
    tl = (d.get("word_count") or {}).get("total_limit")
    if isinstance(tl, (int, float)) and tl and total > tl * (1 + tol / 100):
        over.append(f"TOTAL {total}/{tl}")
    add("word limits", "FAIL" if over else "PASS",
        (f"over: {', '.join(over)}; " if over else "") +
        ", ".join(f"{r['id']}={r['words']}/{r['limit'] or '-'}" for r in rows) +
        f" (excluding {', '.join(sorted(exclude)) or 'nothing'}; tolerance {tol:g}%)")

    hits = []
    for sid, sp in spans.items():
        for m in PLACEHOLDERS.finditer(_sections.inner_text(data, sp)):
            hits.append(f"{sid}: {m.group(0)!r}")
    add("placeholders", "FAIL" if hits else "PASS", "; ".join(hits) or "none found")

    stale = []
    for sid, sp in spans.items():
        inner = _sections.inner_text(data, sp)
        m = re.search(r"words=(\d+)/", inner)
        if "status=empty" in inner:
            continue
        if m and int(m.group(1)) != wordcount.count_words(inner, exclude):
            stale.append(sid)
    add("meta lines current", "WARN" if stale else "PASS",
        f"word count in meta differs from content in: {', '.join(stale)} (section edited by hand?)" if stale else "ok")

    bib = path_of(d, "bibliography", root)
    entries = bib_entries(bib)
    keys = cite_keys("".join(_sections.inner_text(data, sp) for sp in spans.values()))
    undefined = sorted(set(keys) - set(entries))
    unused = sorted(set(entries) - set(keys))
    add("citations resolve", "FAIL" if undefined else "PASS",
        f"{len(set(keys))} key(s) cited; undefined: {', '.join(undefined) or 'none'}")
    add("unused bibliography entries", "WARN" if unused else "PASS", ", ".join(unused) or "none")
    unverifiable = [k for k, v in entries.items() if not v["fields"] & {"doi", "url", "file", "isbn"}]
    add("bib entries verifiable", "WARN" if unverifiable else "PASS",
        (f"no doi/url/file/isbn: {', '.join(unverifiable)}" if unverifiable else "all have doi/url/file/isbn"))

    man = manifest_outputs(path_of(d, "results_manifest", root))
    broken, untraced, changed = [], [], []
    for m in re.finditer(r"(!?)\[[^\]]*\]\(([^)\s]+)[^)]*\)", strip_code(text)):
        target = m.group(2)
        if re.match(r"^[a-z]+:|^#", target):
            continue
        p = (answers.parent / target).resolve()
        if not p.exists():
            broken.append(target)
            continue
        if m.group(1):
            r = rel(p, root)
            if r not in man:
                untraced.append(r)
            elif man[r]["sha256"] and man[r]["sha256"] != sha256_file(p):
                changed.append(r)
    add("local links and images", "FAIL" if broken else "PASS", f"broken: {', '.join(broken) or 'none'}")
    add("figures traceable to logged runs", "WARN" if untraced or changed else "PASS",
        "; ".join(filter(None, [f"not in manifest: {', '.join(untraced)}" if untraced else "",
                                f"changed since logged run: {', '.join(changed)}" if changed else ""])) or "ok")

    spelling = d.get("spelling")
    if spelling in ("en-AU", "en-GB", "en-NZ"):
        wl = {}
        for line in (Path(__file__).parent / "data" / "us_spellings.txt").read_text().splitlines():
            if line.strip() and not line.startswith("#"):
                us, uk = line.split()
                wl[us] = uk
        found = {}
        body = strip_code("".join(_sections.inner_text(data, sp) for sp in spans.values()))
        body = re.sub(r"\[[^\]]*@[^\]]*\]|\([^)]*://[^)]*\)|https?://\S+", " ", body)
        for w in re.findall(r"[A-Za-z]+", body):
            lw = w.lower()
            if lw in wl:
                found[w] = wl[lw]
        for w in IZE.findall(body):
            if w.lower() not in IZE_OK and not w[0].isupper():
                found[w] = re.sub(r"yz", "ys", re.sub(r"iz", "is", w))
        add(f"spelling ({spelling})", "WARN" if found else "PASS",
            ", ".join(f"{k}->{v}" for k, v in sorted(found.items())) or "no US spellings found")

    req = (d.get("format") or {}).get("required_sections") or []
    heads = [h.strip().lower() for h in re.findall(r"^#{1,6}\s+(.+?)(?:\s*\{.*\})?\s*$", text, re.M)]
    miss = [r for r in req if not any(r.lower() in h for h in heads)]
    add("required sections present", "FAIL" if miss else "PASS", f"missing: {', '.join(miss) or 'none'}")

    g = d.get("genai") or {}
    if g.get("acknowledgement_required") is True:
        sp = spans.get("AI-ACK")
        bad = sp is None or answer_section.PLACEHOLDER in _sections.inner_text(data, sp)
        add("AI acknowledgement", "FAIL" if bad else "PASS",
            "AI-ACK section missing or empty (export-submission writes it)" if bad else "present")
    if g.get("policy") == "prohibited":
        add("generative-AI policy", "FAIL", "unit policy is 'prohibited': AI-drafted content must not be submitted")
    elif g.get("policy") in (None, "unclear"):
        add("generative-AI policy", "WARN", "policy unclear: resolve before submitting")

    blocking = [o["id"] for o in d.get("open_questions") or [] if o.get("blocking") and o.get("answer") in (None, "")]
    add("blocking open questions", "WARN" if blocking else "PASS", ", ".join(blocking) or "none")
    return checks, {"answers_sha256": sha256_bytes(data)}


def render(checks, meta, d) -> str:
    fails = sum(c["status"] == "FAIL" for c in checks)
    warns = sum(c["status"] == "WARN" for c in checks)
    fm = {"kind": "compliance", "generated": now().isoformat(), "result": "FAIL" if fails else "PASS",
          "fails": fails, "warnings": warns, **meta}
    lines = ["---", yaml.safe_dump(fm, sort_keys=False).strip(), "---", "",
             f"# Compliance report: {(d.get('unit') or {}).get('code') or ''} {(d.get('assignment') or {}).get('title') or ''}".rstrip(),
             "", f"**Result: {fm['result']}** ({fails} fail, {warns} warning)", "",
             "| Check | Status | Detail |", "|---|---|---|"]
    for c in checks:
        lines.append(f"| {c['check']} | {c['status']} | {c['detail'].replace('|', '/')} |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        root = find_root()
        d = load_details(root)
        checks, meta = run_checks(root, d)
    except ToolError as e:
        die(str(e))
    if a.json:
        print(json.dumps({"checks": checks, **meta}, indent=2))
    else:
        report = render(checks, meta, d)
        if a.out:
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_text(report, encoding="utf-8")
            print(f"wrote {a.out}")
        print(report)
    sys.exit(1 if any(c["status"] == "FAIL" for c in checks) else 0)


if __name__ == "__main__":
    main()
