#!/usr/bin/env python3
"""End-to-end regression test of the deterministic pipeline on examples/demo-unit.

Copies the template to a temporary directory (as you would for a new assignment),
adds the demo inputs, then stands in for the agent-written artefacts (details, rubric,
checklist, bib, code, answers) using the demo's versions, and runs every tool,
including negative cases. Nothing in this repository is modified.

Usage:
  python3 tools/selftest.py            # full run (PDF export too, if xelatex is installed)
  python3 tools/selftest.py --keep     # keep the temp project and print its path
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEMO = REPO / "examples" / "demo-unit"
sys.path.insert(0, str(REPO / "tools"))
import _sections  # noqa: E402
from wordcount import count_words  # noqa: E402

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = ""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


def run(proj: Path, *args, ok_codes=(0,)) -> subprocess.CompletedProcess:
    r = subprocess.run(list(args), cwd=proj, capture_output=True, text=True)
    r.ok = r.returncode in ok_codes
    return r


def demo_section(sid: str) -> str:
    data = (DEMO / "answers" / "answers.md").read_bytes()
    return _sections.inner_text(data, _sections.parse(data)[sid])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="assignment-selftest-"))
    proj = tmp / "DEMO-A2"
    try:
        shutil.copytree(REPO, proj, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", "examples", "build", "__pycache__", ".pytest_cache"))
        py = sys.executable

        # --- word count unit cases
        ex = {"headings", "code_blocks", "tables", "captions", "references"}
        cases = [("Hello world.", set(), 2), ("## Heading here\n\nOne two three.", ex, 3),
                 ("Text.\n\n```\ncode not counted\n```\n", ex, 1), ("As shown [@a2020, p. 4].", ex, 6),
                 ("As shown [@a2020].", ex | {"citations"}, 2), ("| a | b |\n|---|---|\n| c | d |\n\nWord", ex, 1),
                 ("![Caption words](x.png)", ex, 0), ("Body.\n\n## References\n\nSmith 2020.", ex, 1),
                 ("Dash — counts? No.", set(), 3), ("<!-- meta: words=9 -->\nTwo words", set(), 2)]
        bad = [(t, e, count_words(t, e)) for t, e, want in cases if count_words(t, e) != want]
        check("wordcount rules (10 cases)", not bad, str(bad))

        # --- stage 0: init on a clean template copy
        check("template ships without context/assignment.md", not (proj / "context/assignment.md").exists())
        r = run(proj, py, "tools/init_project.py")
        check("init_project creates details/log/bib", r.ok and (proj / "context/assignment.md").exists()
              and (proj / "work/ai-use-log.md").exists(), r.stderr)
        r = run(proj, py, "tools/details.py", "validate", ok_codes=(1,))
        check("unfilled template details fail validation", r.ok, r.stdout[-300:])
        r2 = run(proj, py, "tools/init_project.py")
        check("init_project is idempotent", r2.ok and "copy" not in r2.stdout.replace("keep", ""), r2.stdout)

        # --- inputs + agent-written artefacts (taken from the demo)
        shutil.copytree(DEMO / "inputs", proj / "inputs", dirs_exist_ok=True)
        for rel in ["context/assignment.md", "context/rubric.yaml", "context/checklist.yaml",
                    "work/references/references.bib", "work/references/style.csl"]:
            shutil.copy(DEMO / rel, proj / rel)
        shutil.copytree(DEMO / "work/code", proj / "work/code", dirs_exist_ok=True)

        r = run(proj, py, "tools/extract_inputs.py")
        idx = json.loads((proj / "context/extracted/index.json").read_text())
        check("extract_inputs processes all inputs", r.ok and len(idx) == 11, r.stdout + r.stderr)
        check("pdf/docx/pptx extracted with locators",
              all(idx[k]["status"] == "ok" for k in idx if k.endswith((".pdf", ".docx", ".pptx"))) and
              "## [slide 4]" in (proj / "context/extracted/lectures/week03-reproducible-workflows.pptx.md").read_text()
              and "## [table 1]" in (proj / "context/extracted/rubric/dsci9001-a2-rubric.docx.md").read_text())
        r = run(proj, py, "tools/extract_inputs.py")
        check("extract_inputs is incremental", r.ok and "0 (re)processed" in r.stdout, r.stdout)
        check("extract_inputs --check clean", run(proj, py, "tools/extract_inputs.py", "--check").ok)

        r = run(proj, py, "tools/details.py", "validate")
        check("details validate (demo)", r.ok, r.stdout[-400:])
        check("details qids", run(proj, py, "tools/details.py", "qids").stdout.split() == ["Q1", "Q2"])
        check("details path", run(proj, py, "tools/details.py", "path", "answers").stdout.strip() == "answers/answers.md")

        r = run(proj, py, "tools/check_rubric.py")
        check("check_rubric (demo)", r.ok, r.stdout[-400:])
        rub = proj / "context/rubric.yaml"
        good = rub.read_text()
        rub.write_text(good.replace("weight: 20", "weight: 25").replace("applies_to:\n  - Q2", "applies_to:\n  - Q9"))
        r = run(proj, py, "tools/check_rubric.py", ok_codes=(1,))
        check("check_rubric catches bad weights and unknown QIDs", r.ok and "sum to" in r.stdout and "Q9" in r.stdout,
              r.stdout[-400:])
        rub.write_text(good)

        # --- answer file
        r = run(proj, py, "tools/answer_section.py", "init")
        check("answer_section init", r.ok and "Q1, Q2, AI-ACK" in r.stdout, r.stdout + r.stderr)
        r = run(proj, py, "tools/answer_section.py", "init")
        check("answer_section init is insert-only", r.ok and "nothing changed" in r.stdout)
        ans = proj / "answers/answers.md"
        for sid in ("Q1", "Q2", "AI-ACK"):
            draft = tmp / f"{sid}.md"
            draft.write_text(demo_section(sid))
            before = ans.read_bytes()
            sp = _sections.parse(before)[sid]
            r = run(proj, py, "tools/answer_section.py", "put", sid, "--from", str(draft), "--criteria", "C1")
            after = ans.read_bytes()
            sp2 = _sections.parse(after)[sid]
            same = before[:sp.inner_start] == after[:sp2.inner_start] and before[sp.inner_end:] == after[sp2.inner_end:]
            check(f"put {sid}: only its section changed", r.ok and same, r.stderr)
        hist = list((proj / "work/questions/Q1/history").glob("*.md")) if (proj / "work/questions/Q1/history").exists() else []
        check("placeholder sections are not saved to history", not hist)
        draft = tmp / "Q1.md"
        r = run(proj, py, "tools/answer_section.py", "put", "Q1", "--from", str(draft), "--status", "revised")
        hist = list((proj / "work/questions/Q1/history").glob("*.md"))
        check("replacing a real answer saves history", r.ok and len(hist) == 1)
        bad_draft = tmp / "bad.md"
        bad_draft.write_text("text\n<!-- END Q1 -->\n")
        snapshot = ans.read_bytes()
        r = run(proj, py, "tools/answer_section.py", "put", "Q2", "--from", str(bad_draft), ok_codes=(1,))
        check("put rejects drafts containing markers", r.ok and ans.read_bytes() == snapshot)
        r = run(proj, py, "tools/answer_section.py", "put", "Q7", "--from", str(draft), ok_codes=(1,))
        check("put refuses unknown section without --create", r.ok and ans.read_bytes() == snapshot)
        scratch = tmp / "scratch-answers.md"
        scratch.write_bytes(snapshot)
        r = run(proj, py, "tools/answer_section.py", "put", "Q7", "--from", str(draft), "--create", "--file", str(scratch))
        new = scratch.read_bytes()
        off = _sections.parse(new)["Q7"].begin
        check("put --create inserts a new section, rest byte-identical",
              r.ok and new.startswith(snapshot[:off - 1]) and new.endswith(snapshot[off - 1:]) and
              list(_sections.parse(new)) == ["Q1", "Q2", "AI-ACK", "Q7"], r.stderr)
        scratch.write_bytes(snapshot.replace(b"<!-- END Q2 -->", b"<!--END Q2-->"))
        r = run(proj, py, "tools/answer_section.py", "check", "--file", str(scratch), ok_codes=(1,))
        check("malformed markers are detected", r.ok and "malformed" in r.stderr, r.stderr)
        check("answer_section check", run(proj, py, "tools/answer_section.py", "check").ok)
        r = run(proj, py, "tools/wordcount.py", "--json")
        wc = json.loads(r.stdout)
        check("wordcount within limits", r.ok and all(s["status"].startswith("OK") for s in wc["sections"]), r.stdout)

        # --- experiments
        r = run(proj, py, "tools/run_logged.py", "--name", "Q2-tests", "--qid", "Q2", "--", py, "-m", "pytest", "-q")
        check("run_logged: tests pass", r.ok, r.stdout + r.stderr)
        try:
            import matplotlib  # noqa: F401
            have_mpl = True
        except ImportError:
            have_mpl = False
        if have_mpl:
            r = run(proj, py, "tools/run_logged.py", "--name", "Q2-rmse-figure", "--qid", "Q2", "--outputs",
                    "work/results/tables/Q2-rmse.md,work/results/figures/Q2-smoothing.png", "--", py, "run_q2.py",
                    "--data", "../../inputs/data/sensor.csv", "--table", "../results/tables/Q2-rmse.md",
                    "--figure", "../results/figures/Q2-smoothing.png")
            same = (proj / "work/results/tables/Q2-rmse.md").read_text() == (DEMO / "work/results/tables/Q2-rmse.md").read_text()
            check("run_logged: outputs recorded and reproduce the demo table", r.ok and same, r.stdout)
        else:
            shutil.copytree(DEMO / "work/results", proj / "work/results", dirs_exist_ok=True)
            check("run_logged: figure run skipped (matplotlib missing); demo results copied", True)
        r = run(proj, py, "tools/run_logged.py", "--name", "missing", "--outputs", "work/results/nope.png", "--",
                py, "-c", "pass", ok_codes=(1,))
        check("run_logged fails when declared outputs are missing", r.ok)

        # --- compliance
        r = run(proj, py, "tools/compliance.py", "--json")
        res = json.loads(r.stdout)
        fails = [c for c in res["checks"] if c["status"] == "FAIL"]
        check("compliance passes on demo answers", r.ok and not fails, str(fails))
        good_q2 = tmp / "Q2.md"
        bad_q2 = tmp / "Q2-bad.md"
        bad_q2.write_text(good_q2.read_text() + "\nThe color is TODO [@nosuchkey]. " + "word " * 250 +
                          "\n![x](../work/results/figures/missing.png)\n")
        run(proj, py, "tools/answer_section.py", "put", "Q2", "--from", str(bad_q2))
        r = run(proj, py, "tools/compliance.py", "--json", ok_codes=(1,))
        res = {c["check"]: c for c in json.loads(r.stdout)["checks"]}
        want = {"word limits": "FAIL", "placeholders": "FAIL", "citations resolve": "FAIL",
                "local links and images": "FAIL", "spelling (en-AU)": "WARN"}
        got = {k: res[k]["status"] for k in want}
        check("compliance catches limit/placeholder/citation/link/spelling problems", r.ok and got == want, str(got))
        run(proj, py, "tools/answer_section.py", "put", "Q2", "--from", str(good_q2))
        check("compliance passes again after restoring Q2", run(proj, py, "tools/compliance.py").ok)

        # --- reports, fingerprints, grading status
        p1 = run(proj, py, "tools/report_path.py", "grading", "Q1").stdout.strip()
        (proj / p1).write_text("---\nanswer_sha256: x\n---\n")
        p2 = run(proj, py, "tools/report_path.py", "grading", "Q1").stdout.strip()
        check("report_path never reuses a path", p1 != p2 and p1.startswith("reports/grading/Q1/"), f"{p1} {p2}")
        fp1 = run(proj, py, "tools/fingerprint.py", "Q1").stdout
        h = run(proj, py, "tools/answer_section.py", "hash", "Q1").stdout.strip()
        check("fingerprint matches section hash", f"answer_sha256: {h}" in fp1)
        r = run(proj, py, "skills/grade-assignment/scripts/report_status.py", "--json")
        st = {x["qid"]: x["status"] for x in json.loads(r.stdout)}
        check("report_status flags stale and ungraded", st == {"Q1": "STALE: answer changed, rubric changed",
                                                               "Q2": "NOT GRADED"}, str(st))
        r = run(proj, py, "tools/log_ai_use.py", "--skill", "selftest", "--action", "test | pipe")
        check("log_ai_use appends a row", r.ok and "test \\| pipe" in (proj / "work/ai-use-log.md").read_text())

        # --- environment check
        r = run(proj, py, "skills/check-environment/scripts/env_check.py", "--smoke", ok_codes=(0, 1))
        env = json.loads(r.stdout)
        smoke = [x for x in env["results"] if x["category"] == "smoke test"]
        check("env_check runs and smoke-tests the code", smoke and smoke[0]["status"] == "PASS", r.stdout[-400:])

        # --- export
        r = run(proj, py, "tools/export.py", "--to", "docx")
        docx = proj / "export/DSCI9001_A2_12345678.docx"
        check("export docx + code zip", r.ok and docx.exists() and (proj / "export/DSCI9001_A2_12345678_code.zip").exists(),
              r.stdout + r.stderr)
        txt = subprocess.run(["pandoc", str(docx), "-t", "plain"], capture_output=True, text=True).stdout
        check("export renders citations, no markers leak", "(Nguyen, 2024)" in txt and "<!--" not in txt
              and "BEGIN Q1" not in txt and "@nguyen" not in txt)
        if shutil.which("xelatex"):
            r = run(proj, py, "tools/export.py", "--to", "pdf")
            check("export pdf via LaTeX", r.ok and (proj / "export/DSCI9001_A2_12345678.pdf").read_bytes()[:4] == b"%PDF"
                  and (proj / "export/build/DSCI9001_A2_12345678.tex").exists(), r.stdout[-300:] + r.stderr[-300:])

        # --- skills
        r = run(proj, py, "tools/validate_skills.py")
        check("validate_skills", r.ok, r.stdout[-400:])
        check(".claude/skills symlink resolves", (proj / ".claude/skills/answer-question/SKILL.md").exists())
    finally:
        failed = [n for n, ok, _ in results if not ok]
        print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
        if a.keep:
            print(f"temp project kept at {proj}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
