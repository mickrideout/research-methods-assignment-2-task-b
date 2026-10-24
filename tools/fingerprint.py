#!/usr/bin/env python3
"""Print the hashes and timestamp that grading reports record in their frontmatter.

Usage:
  python3 tools/fingerprint.py Q2     # answer_sha256 (section Q2, meta excluded), file hashes, generated
  python3 tools/fingerprint.py        # whole-file hashes plus every section hash
Output is YAML, ready to paste into a report's frontmatter. Run it before and
after grading: identical output (apart from `generated`) proves nothing was edited.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml  # noqa: E402
from _common import ToolError, die, find_root, load_details, now, path_of, sha256_file  # noqa: E402
import _sections  # noqa: E402
import answer_section  # noqa: E402


def main():
    qid = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        root = find_root()
        d = load_details(root)
        answers = path_of(d, "answers", root)
        data = answers.read_bytes()
        spans = _sections.parse(data)
        out = {"generated": now().isoformat()}
        if qid:
            if qid not in spans:
                raise ToolError(f"no section {qid}")
            out["qid"] = qid
            out["answer_sha256"] = answer_section.content_hash(data, spans[qid])
        out["answers_sha256"] = sha256_file(answers)
        for key in ("rubric_yaml", "checklist_yaml"):
            p = path_of(d, key, root)
            out[key.replace("_yaml", "_sha256")] = sha256_file(p) if p.exists() else None
        if not qid:
            out["sections"] = {s: answer_section.content_hash(data, sp) for s, sp in spans.items()}
    except (ToolError, OSError) as e:
        die(str(e))
    print(yaml.safe_dump(out, sort_keys=False).strip())


if __name__ == "__main__":
    main()
