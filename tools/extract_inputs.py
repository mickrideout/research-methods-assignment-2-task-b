#!/usr/bin/env python3
"""Extract text from inputs/ into context/extracted/ with page/slide markers. Incremental.

Each input <inputs>/<sub>/<file> becomes <extracted>/<sub>/<file>.md, with
location markers that skills cite as `inputs/<sub>/<file>#p.N`:
  PDF   -> "## [p. N]"     (needs poppler's pdftotext)
  PPTX  -> "## [slide N]"  (speaker notes appended under "### Notes")
  DOCX  -> "## [para N]"   every paragraph numbered; headings kept; "## [table N]" as Markdown tables
  IPYNB -> "## [cell N]"
  MD/TXT/HTML/CSV(first 50 rows)/JSON -> copied with "## [line N]" every 50 lines
Code, data and image files are indexed (sha256, size) but not extracted;
read them directly. inputs/**/README.md (template guidance) is ignored.

Writes <extracted>/INDEX.md (for reading) and <extracted>/index.json (state).
Only files whose sha256 changed are re-extracted; removed inputs are dropped.

Usage:
  python3 tools/extract_inputs.py           # incremental
  python3 tools/extract_inputs.py --force   # re-extract everything
  python3 tools/extract_inputs.py --check   # exit 1 if anything is new/changed/removed
"""
from __future__ import annotations

import argparse
import csv
import html.parser
import io
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ToolError, die, find_root, load_details, now, path_of, sha256_file  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
TEXT_EXT = {".md", ".markdown", ".txt", ".rst", ".tex"}
SKIP_DIRS = {"data", "starter"}  # indexed but never extracted


def pdf(path: Path) -> tuple[str, str]:
    if not shutil.which("pdftotext"):
        raise ToolError("pdftotext not installed (poppler-utils)")
    out = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=True).stdout
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    if not any(p.strip() for p in pages):
        raise ToolError("no text layer (scanned PDF?): needs OCR or an agent that can read the PDF directly")
    return "\n".join(f"## [p. {i}]\n\n{p.rstrip()}\n" for i, p in enumerate(pages, 1)), "pdftotext"


def docx(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as z:
        body = ET.fromstring(z.read("word/document.xml")).find(f"{W}body")
    ptext = lambda p: "".join(t.text or "" for t in p.iter(f"{W}t")).strip()  # noqa: E731
    parts, n, nt = [], 0, 0
    for el in body:
        if el.tag == f"{W}p":
            text = ptext(el)
            if not text:
                continue
            n += 1
            style = el.find(f"{W}pPr/{W}pStyle")
            sval = style.get(f"{W}val", "") if style is not None else ""
            m = re.match(r"Heading(\d)", sval)
            prefix = "#" * (int(m.group(1)) + 2) + " " if m else ""
            parts.append(f"## [para {n}]\n\n{prefix}{text}\n")
        elif el.tag == f"{W}tbl":
            nt += 1
            rows = []
            for tr in el.iter(f"{W}tr"):
                cells = [" ".join(ptext(p) for p in tc.iter(f"{W}p")).replace("|", "/") for tc in tr.iter(f"{W}tc")]
                rows.append("| " + " | ".join(cells) + " |")
            if rows:
                rows.insert(1, "|" + "---|" * rows[0].count(" | ") + "---|")
            parts.append(f"## [table {nt}]\n\n" + "\n".join(rows) + "\n")
    return "\n".join(parts), "docx-xml"


def pptx(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        slides = sorted((n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                        key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[1]).group(1)))
        parts = []
        for s in slides:
            num = int(re.search(r"slide(\d+)\.xml", s).group(1))
            paras = ["".join(t.text or "" for t in p.iter(f"{A}t")) for p in ET.fromstring(z.read(s)).iter(f"{A}p")]
            body = "\n".join(p for p in paras if p.strip())
            notes = ""
            relf = f"ppt/slides/_rels/slide{num}.xml.rels"
            if relf in names:
                for r in ET.fromstring(z.read(relf)):
                    tgt = r.get("Target", "")
                    if "notesSlide" in tgt:
                        np_ = "ppt/" + tgt.replace("../", "")
                        if np_ in names:
                            nps = ["".join(t.text or "" for t in p.iter(f"{A}t"))
                                   for p in ET.fromstring(z.read(np_)).iter(f"{A}p")]
                            notes = "\n".join(p for p in nps if p.strip() and not p.strip().isdigit())
            parts.append(f"## [slide {num}]\n\n{body}\n" + (f"\n### Notes\n\n{notes}\n" if notes else ""))
    return "\n".join(parts), "pptx-xml"


def ipynb(path: Path) -> tuple[str, str]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    parts = []
    for i, c in enumerate(nb.get("cells", []), 1):
        src = "".join(c.get("source", []))
        fence = "```\n" if c.get("cell_type") == "code" else ""
        parts.append(f"## [cell {i}] ({c.get('cell_type')})\n\n{fence}{src}\n{fence}")
    return "\n".join(parts), "ipynb-json"


class _Strip(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.skip = [], False

    def handle_starttag(self, tag, attrs):
        self.skip = tag in ("script", "style")
        if tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        self.skip = False

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def text_lines(text: str) -> str:
    lines = text.splitlines()
    return "\n".join((f"\n## [line {i + 1}]\n\n" if i % 50 == 0 else "") + l for i, l in enumerate(lines)) + "\n"


def plain(path: Path) -> tuple[str, str]:
    ext = path.suffix.lower()
    raw = path.read_text(encoding="utf-8", errors="replace")
    if ext in (".html", ".htm"):
        s = _Strip()
        s.feed(raw)
        raw = re.sub(r"\n{3,}", "\n\n", "".join(s.out))
        return text_lines(raw), "html-strip"
    if ext == ".csv":
        rows = list(csv.reader(io.StringIO(raw)))
        head = "\n".join(",".join(r) for r in rows[:50])
        return f"## [line 1]\n\n```\n{head}\n```\n\n({len(rows)} rows; first 50 shown)\n", "csv-head"
    return text_lines(raw), "text"


def extractor_for(rel_parts: tuple[str, ...], path: Path):
    ext = path.suffix.lower()
    if rel_parts and rel_parts[0] in SKIP_DIRS:
        return None
    return {".pdf": pdf, ".docx": docx, ".pptx": pptx, ".ipynb": ipynb}.get(ext) or (
        plain if ext in TEXT_EXT | {".html", ".htm", ".csv", ".json"} else None)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    try:
        root = find_root()
        d = load_details(root)
        inputs, out = path_of(d, "inputs", root), path_of(d, "extracted", root)
    except ToolError as e:
        die(str(e))
    state_f = out / "index.json"
    state = json.loads(state_f.read_text()) if state_f.exists() and not a.force else {}
    files = sorted(p for p in inputs.rglob("*") if p.is_file() and not p.name.startswith(".")
                   and not (p.name == "README.md" and len(p.relative_to(inputs).parts) <= 2))
    new_state, changed = {}, []
    for p in files:
        key = str(p.relative_to(inputs))
        st = p.stat()
        prev = state.get(key)
        if prev and prev.get("size") == st.st_size and prev.get("mtime") == st.st_mtime:
            digest = prev["sha256"]
        else:
            digest = sha256_file(p)
        entry = {"size": st.st_size, "mtime": st.st_mtime, "sha256": digest}
        if prev and prev.get("sha256") == digest and (prev.get("status") != "error"):
            new_state[key] = {**prev, **entry}
            continue
        changed.append(key)
        fn = extractor_for(p.relative_to(inputs).parts, p)
        target = out / f"{key}.md"
        if a.check:
            new_state[key] = entry
            continue
        if fn is None:
            new_state[key] = {**entry, "status": "indexed", "extracted": None, "method": None, "units": None}
            continue
        try:
            body, method = fn(p)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"<!-- extracted from {inputs.name}/{key} sha256={digest} "
                              f"on {now().isoformat()} via {method} -->\n\n{body}", encoding="utf-8")
            units = len(re.findall(r"^## \[", body, re.M))
            new_state[key] = {**entry, "status": "ok", "extracted": str(target.relative_to(root)),
                              "method": method, "units": units}
        except Exception as e:  # report, never skip silently
            new_state[key] = {**entry, "status": "error", "error": str(e), "extracted": None,
                              "method": None, "units": None}
    removed = sorted(set(state) - set(new_state))
    if a.check:
        for k in changed:
            print(f"changed/new: {k}")
        for k in removed:
            print(f"removed:     {k}")
        print("extracted text is up to date" if not (changed or removed) else "run: python3 tools/extract_inputs.py")
        sys.exit(1 if changed or removed else 0)
    for k in removed:
        (out / f"{k}.md").unlink(missing_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    state_f.write_text(json.dumps(new_state, indent=2, sort_keys=True))
    rows = ["# Extracted inputs index", "",
            f"Generated {now().isoformat()} by tools/extract_inputs.py. Cite as `inputs/<path>#p.N` "
            "(or `#slide.N`, `#para.N`, `#table.N`, `#cell.N`, `#line.N`).", "",
            "| Input | Status | Method | Units | sha256 (12) | Extracted text |", "|---|---|---|---|---|---|"]
    for k, v in sorted(new_state.items()):
        status = v["status"] if v["status"] != "error" else f"ERROR: {v.get('error')}"
        rows.append(f"| inputs/{k} | {status} | {v.get('method') or '-'} | {v.get('units') or '-'} | "
                    f"{v['sha256'][:12]} | {v.get('extracted') or '(read directly)'} |")
    (out / "INDEX.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    errors = [k for k, v in new_state.items() if v["status"] == "error"]
    print(f"{len(files)} input(s); {len(changed)} (re)processed; {len(removed)} removed; {len(errors)} error(s)")
    for k in errors:
        print(f"ERROR inputs/{k}: {new_state[k]['error']}")
    if not files:
        print("inputs/ is empty: add the spec and rubric first (see inputs/README.md)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
