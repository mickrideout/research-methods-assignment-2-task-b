#!/usr/bin/env python3
"""Assemble the submission from the common answer file with pandoc.

Strips section markers and meta lines, resolves [@key] citations with
--citeproc against paths.bibliography (and paths.csl if present), and writes
the file type(s) in `format.file_type` to paths.export_dir. Optionally zips
paths.code_dir when `submission.code_bundle` is true. Writes export/MANIFEST.md.

Usage:
  python3 tools/export.py                 # build every required format
  python3 tools/export.py --to docx,pdf   # override formats
  python3 tools/export.py --dry-run       # show pandoc commands only
Filename comes from `submission.filename_pattern`, with placeholders
{unit_code} {assignment_number} {assignment_title} {student_id} {student_name}.
PDF goes via LaTeX (xelatex), or via DOCX + LibreOffice when
`format.reference_docx` is set, so the docx styling carries over.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ToolError, die, find_root, load_details, now, path_of, rel, sha256_bytes, sha256_file  # noqa: E402
import _sections  # noqa: E402
import wordcount  # noqa: E402

STRIP = re.compile(r"^<!-- (?:BEGIN|END) [^>]*-->[ \t]*\r?\n|^<!-- meta: .*-->[ \t]*\r?\n", re.M)
ZIP_EXCLUDE = {".venv", "venv", "__pycache__", ".ipynb_checkpoints", ".pytest_cache", ".mypy_cache", ".git",
               "node_modules"}


def filename(d: dict) -> str:
    u, a, s = d.get("unit") or {}, d.get("assignment") or {}, d.get("student") or {}
    pat = (d.get("submission") or {}).get("filename_pattern") or "{unit_code}_{assignment_title}"
    vals = {"unit_code": u.get("code"), "assignment_number": a.get("number"),
            "assignment_title": a.get("title"), "student_id": s.get("id"), "student_name": s.get("name")}
    missing = [k for k in re.findall(r"\{(\w+)\}", pat) if not vals.get(k)]
    if missing:
        raise ToolError(f"filename_pattern needs values for {missing} in the details file")
    name = pat.format(**{k: str(v) for k, v in vals.items() if v is not None})
    return re.sub(r"[^\w.-]+", "_", name).strip("_")


def run(cmd, cwd, dry):
    print("$ " + " ".join(str(c) for c in cmd))
    if not dry:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        if r.stdout.strip() or r.stderr.strip():
            print((r.stdout + r.stderr).strip())
        if r.returncode:
            raise ToolError(f"{cmd[0]} failed with exit {r.returncode}")


def verify(path: Path, fmt: str):
    if not path.exists() or path.stat().st_size == 0:
        raise ToolError(f"{path} was not produced")
    if fmt == "docx":
        with zipfile.ZipFile(path) as z:
            if "word/document.xml" not in z.namelist():
                raise ToolError(f"{path} is not a valid docx")
    if fmt == "pdf" and path.read_bytes()[:4] != b"%PDF":
        raise ToolError(f"{path} is not a valid PDF")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--to", help="comma-separated formats (default: format.file_type)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        if not shutil.which("pandoc"):
            raise ToolError("pandoc is not installed")
        root = find_root()
        d = load_details(root)
        answers = path_of(d, "answers", root)
        out_dir = path_of(d, "export_dir", root)
        bib, csl = path_of(d, "bibliography", root), path_of(d, "csl", root)
        fmt = d.get("format") or {}
        formats = (a.to or fmt.get("file_type") or "docx")
        formats = [f.strip().lower() for f in (formats if isinstance(formats, list) else formats.split(",")) if f.strip()]
        name = filename(d)
        data = answers.read_bytes()
        spans = _sections.parse(data)
        build = out_dir / "build"
        build.mkdir(parents=True, exist_ok=True)
        src = build / "answers.export.md"
        src.write_bytes(STRIP.sub("", data.decode("utf-8")).encode())
        base = ["pandoc", str(src), "--standalone", "--citeproc", f"--resource-path={answers.parent}:{root}",
                "-M", f"lang={d.get('spelling') or 'en-AU'}", "-M", "link-citations=true"]
        if bib.exists():
            base.append(f"--bibliography={bib}")
        if csl.exists():
            base.append(f"--csl={csl}")
        else:
            print(f"note: {rel(csl, root)} not found; pandoc's default style (Chicago author-date) will be used. "
                  "Download the required CSL from https://www.zotero.org/styles")
        ref_docx = fmt.get("reference_docx")
        if ref_docx == "n/a":
            ref_docx = None
        produced = []
        for f in formats:
            target = out_dir / f"{name}.{f}"
            if f == "pdf" and ref_docx:
                docx = build / f"{name}.docx"
                run(base + ["-o", str(docx), f"--reference-doc={root / ref_docx}"], answers.parent, a.dry_run)
                run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx)],
                    answers.parent, a.dry_run)
            elif f == "pdf":
                hdr = build / "keep-figures-in-place.tex"
                # Latin Modern has no Greek glyphs, so typeset Unicode Greek (α = .05) in math mode.
                greek = {"α": "alpha", "β": "beta", "χ": "chi", "δ": "delta", "ε": "epsilon", "η": "eta",
                         "μ": "mu", "ρ": "rho", "σ": "sigma", "τ": "tau", "Δ": "Delta", "Σ": "Sigma"}
                hdr.write_text("\\usepackage{float}\n\\floatplacement{figure}{H}\n\\usepackage{newunicodechar}\n"
                               + "".join(f"\\newunicodechar{{{c}}}{{\\ensuremath{{\\{n}}}}}\n" for c, n in greek.items()),
                               encoding="utf-8")
                run(base + ["-o", str(target), "--pdf-engine=xelatex", "-V", "geometry:margin=2.5cm",
                            "-H", str(hdr)], answers.parent, a.dry_run)
            elif f == "docx":
                run(base + ["-o", str(target)] + ([f"--reference-doc={root / ref_docx}"] if ref_docx else []),
                    answers.parent, a.dry_run)
            else:
                run(base + ["-o", str(target)], answers.parent, a.dry_run)
            if not a.dry_run:
                verify(target, f)
            produced.append(target)
        sub = d.get("submission") or {}
        if sub.get("code_bundle"):
            code = path_of(d, "code_dir", root)
            z = out_dir / f"{name}_code.zip"
            print(f"zip {rel(code, root)} -> {rel(z, root)}")
            if not a.dry_run:
                with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
                    for p in sorted(code.rglob("*")):
                        if (p.is_file() and not (set(p.relative_to(code).parts) & ZIP_EXCLUDE)
                                and p.suffix != ".pyc" and not p.name.startswith(".")):
                            zf.write(p, Path(code.name) / p.relative_to(code))
            produced.append(z)
        if a.dry_run:
            return
        exclude, tol = wordcount.rules(d, None)
        rows = wordcount.section_counts(d, data, exclude, tol)
        lines = ["# Export manifest", "", f"Generated {now().isoformat()} by tools/export.py from "
                 f"`{rel(answers, root)}` (sha256 {sha256_bytes(data)[:12]}).", "",
                 "| File | Bytes | sha256 (12) |", "|---|---|---|"]
        lines += [f"| {p.name} | {p.stat().st_size} | {sha256_file(p)[:12]} |" for p in produced]
        lines += ["", "| Section | Words | Limit |", "|---|---|---|"]
        lines += [f"| {r['id']} | {r['words']} | {r['limit'] or '-'} |" for r in rows]
        lines += ["", f"Sections: {', '.join(spans)}", ""]
        (out_dir / "MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")
        for p in produced:
            print(f"produced {rel(p, root)}")
    except (ToolError, OSError) as e:
        die(str(e))


if __name__ == "__main__":
    main()
