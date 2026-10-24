#!/usr/bin/env python3
"""Create, read or replace exactly one section of the common answer file.

Everything outside the target section stays byte-identical; the script
verifies this after every write and restores the original on failure.

Usage:
  python3 tools/answer_section.py init              # create answers file from templates/answers.md,
                                                    # or add sections for new question IDs (insert-only)
  python3 tools/answer_section.py check             # validate markers against the question list
  python3 tools/answer_section.py list              # IDs, word counts, meta lines
  python3 tools/answer_section.py get Q2            # print the section's content
  python3 tools/answer_section.py hash Q2           # sha256 of content (meta line excluded)
  python3 tools/answer_section.py put Q2 --from draft.md --criteria C1,C3 [--status draft|revised|final]
  python3 tools/answer_section.py put Q2 --from - --create   # read stdin; create section if absent

`put` writes a meta line (word count/limit, criteria, date, status) after the
section's first heading and saves the replaced content to
<paths.questions_dir>/<ID>/history/<timestamp>.md.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (QID_PATTERN, RESERVED_SECTIONS, ToolError, die, find_root, load_details,  # noqa: E402
                     path_of, rel, sha256_bytes, stamp, now)
import _sections  # noqa: E402
import wordcount  # noqa: E402

PLACEHOLDER = "_Not yet answered._"


def _questions(details):
    return [q for q in details.get("questions") or [] if q.get("id")]


def _expected_ids(details):
    ids = [q["id"] for q in _questions(details)]
    if (details.get("genai") or {}).get("acknowledgement_required") is True:
        ids.append("AI-ACK")
    return ids


def _fill(text: str, details: dict) -> str:
    def sub(m):
        cur = details
        for part in m.group(1).split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        return "" if cur is None else str(cur)
    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", sub, text)


def _empty_section(sid: str, details: dict, nl: str) -> str:
    q = next((q for q in _questions(details) if q["id"] == sid), None)
    if sid == "AI-ACK":
        heading, limit = "## Acknowledgement of generative AI use", "-"
    else:
        title = (q or {}).get("title") or "Title"
        heading, limit = f"## {sid}. {title}", (q or {}).get("word_limit") or "-"
    body = [f"<!-- BEGIN {sid} -->", heading,
            f"<!-- meta: words=0/{limit} | criteria=- | updated=- | status=empty -->", "",
            PLACEHOLDER, f"<!-- END {sid} -->"]
    return nl.join(body) + nl


def _insert_offset(data: bytes, spans, sid: str, order: list[str]) -> tuple[int, bool]:
    """Where to insert a new section, following the details question order.
    Returns (offset, needs_leading_newline)."""
    idx = order.index(sid) if sid in order else len(order)
    for prev in reversed(order[:idx]):
        if prev in spans:
            end = spans[prev].end
            return end, not data[:end].endswith(b"\n")
    for nxt in order[idx + 1:]:
        if nxt in spans:
            return spans[nxt].begin, False
    if spans:
        last = list(spans.values())[-1]
        return last.end, not data[:last.end].endswith(b"\n")
    m = re.search(rb"^#+\s*References\b", data, re.M)
    if m:
        return m.start(), False
    return len(data), bool(data) and not data.endswith(b"\n")


def _atomic_write(path: Path, data: bytes):
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _verify(path: Path, before: bytes, prefix_len: int, suffix_len: int, expect_ids: list[str]):
    after = path.read_bytes()
    ok = (after[:prefix_len] == before[:prefix_len]
          and (suffix_len == 0 or after[-suffix_len:] == before[-suffix_len:]))
    try:
        ids = list(_sections.parse(after))
    except ToolError as e:
        ok, ids = False, [str(e)]
    if not ok or ids != expect_ids:
        _atomic_write(path, before)
        raise ToolError(f"post-write verification failed; original restored (sections now: {ids})")


def cmd_init(root, details, answers: Path):
    nl = "\n"
    if not answers.exists():
        tpl = (root / (details.get("paths") or {}).get("templates_dir", "templates") / "answers.md")
        text = tpl.read_text(encoding="utf-8")
        first = re.search(r"^<!-- BEGIN ", text, re.M)
        last_end = list(re.finditer(r"^<!-- END .*-->[ \t]*\n?", text, re.M))
        header = text[:first.start()] if first else text
        footer = text[last_end[-1].end():] if last_end else ""
        body = nl.join(_empty_section(sid, details, nl) for sid in _expected_ids(details))
        answers.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(answers, _fill(header, details).encode() + body.encode() + footer.encode())
        _sections.parse(answers.read_bytes())
        print(f"created {rel(answers, root)} with sections: {', '.join(_expected_ids(details))}")
        return
    data = answers.read_bytes()
    spans = _sections.parse(data)
    order = _expected_ids(details)
    added = []
    for sid in order:
        if sid in spans:
            continue
        nlb = _sections.newline_of(data)
        off, lead = _insert_offset(data, spans, sid, order)
        block = (nlb if lead else b"") + nlb + _empty_section(sid, details, nlb.decode()).encode()
        new = data[:off] + block + data[off:]
        _atomic_write(answers, new)
        _verify(answers, data, off, len(data) - off, list(_sections.parse(new)))
        data, spans = new, _sections.parse(new)
        added.append(sid)
    print(f"added sections: {', '.join(added)}" if added else "answer file already has every section; nothing changed")


def cmd_check(details, answers: Path) -> int:
    spans = _sections.parse(answers.read_bytes())
    expected = _expected_ids(details)
    missing = [s for s in expected if s not in spans]
    extra = [s for s in spans if s not in expected and s not in RESERVED_SECTIONS]
    order_ok = [s for s in spans if s in expected] == [s for s in expected if s in spans]
    print(f"sections: {', '.join(spans) or '(none)'}")
    if missing:
        print(f"MISSING: {', '.join(missing)} (run: python3 tools/answer_section.py init)")
    if extra:
        print(f"UNEXPECTED (not in question list): {', '.join(extra)}")
    if not order_ok:
        print("WARNING: section order differs from the question list")
    print("markers OK" if not (missing or extra) else "markers have problems")
    return 1 if missing or extra else 0


def content_hash(data: bytes, span) -> str:
    inner = _sections.inner_text(data, span)
    return sha256_bytes(_sections.META_RE.sub("", inner).encode())


def cmd_put(root, details, answers: Path, sid, src, criteria, status, create):
    if not re.fullmatch(QID_PATTERN, sid):
        raise ToolError(f"invalid section id {sid!r}")
    draft = sys.stdin.read() if src == "-" else Path(src).read_text(encoding="utf-8")
    if _sections.MARKER_RE.search(draft.encode()) or _sections.LOOSE_RE.search(draft.encode()):
        raise ToolError("draft contains BEGIN/END markers; supply only the section content")
    draft = _sections.META_RE.sub("", draft).strip("\n")
    data = answers.read_bytes()
    nl = _sections.newline_of(data).decode()
    spans = _sections.parse(data)
    created = sid not in spans
    if created and not create:
        raise ToolError(f"no section {sid} in {rel(answers, root)}; pass --create to add it")

    exclude, _ = wordcount.rules(details, None)
    words = wordcount.count_words(draft, exclude)
    q = next((q for q in _questions(details) if q["id"] == sid), {})
    meta = (f"<!-- meta: words={words}/{q.get('word_limit') or '-'} | criteria={criteria or '-'} | "
            f"updated={now().date().isoformat()} | status={status} -->")
    lines = draft.split("\n")
    first = next((i for i, l in enumerate(lines) if l.strip()), 0)
    at = first + 1 if lines and lines[first].lstrip().startswith("#") else 0
    lines.insert(at, meta)
    inner = nl.join(l.rstrip("\r") for l in lines) + nl

    if created:
        off, lead = _insert_offset(data, spans, sid, _expected_ids(details))
        block = (nl if lead else "") + nl + f"<!-- BEGIN {sid} -->{nl}{inner}<!-- END {sid} -->{nl}"
        new = data[:off] + block.encode() + data[off:]
        prefix, suffix = off, len(data) - off
        expect = list(_sections.parse(new))
    else:
        sp = spans[sid]
        old = _sections.inner_text(data, sp)
        if old.strip() and PLACEHOLDER not in old:
            hist = path_of(details, "questions_dir", root) / sid / "history" / f"{stamp()}.md"
            hist.parent.mkdir(parents=True, exist_ok=True)
            hist.write_text(old, encoding="utf-8")
            print(f"previous content saved to {rel(hist, root)}")
        new = data[:sp.inner_start] + inner.encode() + data[sp.inner_end:]
        prefix, suffix = sp.inner_start, len(data) - sp.inner_end
        expect = list(spans)
    _atomic_write(answers, new)
    _verify(answers, data, prefix, suffix, expect)
    print(f"{'created' if created else 'replaced'} section {sid} in {rel(answers, root)}: "
          f"{words} words (limit {q.get('word_limit') or '-'}); rest of file byte-identical")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["init", "check", "list", "get", "hash", "put"])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--from", dest="src", help="file with the new section content, or - for stdin")
    ap.add_argument("--criteria", default="", help="comma-separated rubric criterion IDs targeted")
    ap.add_argument("--status", default="draft", choices=["draft", "revised", "final"])
    ap.add_argument("--create", action="store_true", help="create the section if it does not exist")
    ap.add_argument("--file", help="answer file (default: paths.answers)")
    a = ap.parse_args()
    try:
        root = find_root()
        details = load_details(root)
        answers = Path(a.file) if a.file else path_of(details, "answers", root)
        if a.command == "init":
            return cmd_init(root, details, answers)
        if not answers.exists():
            raise ToolError(f"{rel(answers, root)} does not exist (run: python3 tools/answer_section.py init)")
        if a.command == "check":
            sys.exit(cmd_check(details, answers))
        data = answers.read_bytes()
        spans = _sections.parse(data)
        if a.command == "list":
            exclude, _ = wordcount.rules(details, None)
            for sid, sp in spans.items():
                inner = _sections.inner_text(data, sp)
                m = _sections.META_RE.search(inner)
                print(f"{sid:<10} {wordcount.count_words(inner, exclude):>6} words  "
                      f"{m.group(0).strip() if m else '(no meta line)'}")
            return
        if not a.id:
            raise ToolError(f"'{a.command}' needs a section id")
        if a.command == "put":
            if not a.src:
                raise ToolError("put needs --from FILE (or --from - for stdin)")
            return cmd_put(root, details, answers, a.id, a.src, a.criteria, a.status, a.create)
        if a.id not in spans:
            raise ToolError(f"no section {a.id}")
        if a.command == "get":
            sys.stdout.write(_sections.inner_text(data, spans[a.id]))
        elif a.command == "hash":
            print(content_hash(data, spans[a.id]))
    except (ToolError, OSError) as e:
        die(str(e))


if __name__ == "__main__":
    main()
