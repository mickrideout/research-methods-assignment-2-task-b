#!/usr/bin/env python3
"""Validate every skills/<name>/SKILL.md against the Agent Skills format and project conventions.

Errors: missing/invalid frontmatter; `name` not matching the folder or not
lowercase-hyphenated (1-64 chars, no leading/trailing/double hyphens);
`description` missing, over 1024 chars, too short, or lacking a "when to use"
clause; unknown frontmatter keys; missing required body sections; relative
links to files that do not exist.
Warnings: vendor-specific wording in the body; SKILL.md over 500 lines.

Usage:
  python3 tools/validate_skills.py [skills_dir]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ToolError, split_frontmatter  # noqa: E402

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_SECTIONS = ["Purpose", "When to use", "Inputs", "Procedure", "Output", "Quality checks",
                     "If inputs are missing"]
VENDOR = re.compile(r"\b(claude code|codex|gemini cli|cursor|copilot|\.claude/)\b", re.I)


def check(skill_dir: Path) -> tuple[list[str], list[str]]:
    err, warn = [], []
    f = skill_dir / "SKILL.md"
    if not f.is_file():
        return [f"{skill_dir.name}: no SKILL.md"], []
    text = f.read_text(encoding="utf-8")
    try:
        fm, body = split_frontmatter(text)
    except ToolError as e:
        return [f"{skill_dir.name}: {e}"], []
    name, desc = fm.get("name"), fm.get("description")
    if name != skill_dir.name:
        err.append(f"name {name!r} does not match folder {skill_dir.name!r}")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        err.append(f"name {name!r} must be 1-64 chars of lowercase letters, digits and single hyphens")
    if not isinstance(desc, str) or not desc.strip():
        err.append("description missing")
    else:
        if len(desc) > 1024:
            err.append(f"description is {len(desc)} chars (max 1024)")
        if len(desc) < 120:
            err.append(f"description is only {len(desc)} chars; say what it does AND when to use it")
        if not re.search(r"\b(use when|use this when|use after|use before|use to|trigger)", desc, re.I):
            err.append("description lacks a 'Use when ...' trigger clause")
    extra = set(fm) - ALLOWED_KEYS
    if extra:
        err.append(f"unknown frontmatter keys: {sorted(extra)}")
    if "compatibility" in fm and len(str(fm["compatibility"])) > 500:
        err.append("compatibility over 500 chars")
    heads = [h.strip().lower() for h in re.findall(r"^##\s+(.+)$", body, re.M)]
    for s in REQUIRED_SECTIONS:
        if not any(h.startswith(s.lower()) for h in heads):
            err.append(f"missing section '## {s}'")
    prose = re.sub(r"^(```|~~~).*?^\1\s*$", " ", body, flags=re.S | re.M)
    prose = re.sub(r"`[^`\n]+`", " ", prose)
    for target in re.findall(r"\]\(([^)#\s]+)\)", prose):
        if not re.match(r"^[a-z]+:", target) and not (skill_dir / target).exists():
            err.append(f"broken relative link: {target}")
    for m in VENDOR.finditer(body):
        warn.append(f"vendor-specific wording: {m.group(0)!r}")
    n = text.count("\n")
    if n > 500:
        warn.append(f"SKILL.md is {n} lines; move detail into references/")
    return err, warn


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "skills"
    dirs = sorted(p for p in base.iterdir() if p.is_dir())
    total_err = 0
    for d in dirs:
        err, warn = check(d)
        total_err += len(err)
        print(f"{'FAIL' if err else 'ok  '} {d.name}")
        for e in err:
            print(f"     ERROR {e}")
        for w in warn:
            print(f"     WARN  {w}")
    print(f"{len(dirs)} skill(s), {total_err} error(s)")
    sys.exit(1 if total_err or not dirs else 0)


if __name__ == "__main__":
    main()
