"""Shared helpers for the assignment tools. Standard library plus PyYAML."""
from __future__ import annotations

import datetime as _dt
import hashlib
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: python3 -m pip install pyyaml")

DETAILS_REL = Path("context/assignment.md")
QID_PATTERN = r"[A-Za-z][A-Za-z0-9._-]*"
RESERVED_SECTIONS = {"AI-ACK"}


class ToolError(Exception):
    pass


def find_root(start: Path | None = None) -> Path:
    """Project root: $ASSIGNMENT_ROOT, else the nearest ancestor of cwd holding
    context/assignment.md or templates/assignment.md, else the tools' parent."""
    env = os.environ.get("ASSIGNMENT_ROOT")
    if env:
        return Path(env).resolve()
    here = (start or Path.cwd()).resolve()
    for d in (here, *here.parents):
        if (d / DETAILS_REL).is_file() or (d / "templates" / "assignment.md").is_file():
            return d
    return Path(__file__).resolve().parent.parent


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise ToolError("file does not start with YAML frontmatter ('---')")
    lines = text.splitlines(keepends=True)
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            data = yaml.safe_load("".join(lines[1:i])) or {}
            if not isinstance(data, dict):
                raise ToolError("frontmatter is not a YAML mapping")
            return data, "".join(lines[i + 1:])
    raise ToolError("frontmatter has no closing '---'")


def load_details(root: Path | None = None) -> dict:
    root = root or find_root()
    path = root / DETAILS_REL
    if not path.is_file():
        raise ToolError(f"common details file not found: {path} (run tools/init_project.py)")
    data, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    return data


def path_of(details: dict, key: str, root: Path | None = None) -> Path:
    root = root or find_root()
    rel = (details.get("paths") or {}).get(key)
    if not rel:
        raise ToolError(f"paths.{key} is not set in {DETAILS_REL}")
    return root / rel


def get_dotted(data, key: str):
    cur = data
    for part in key.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise KeyError(key)
    return cur


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def now() -> _dt.datetime:
    return _dt.datetime.now().astimezone().replace(microsecond=0)


def stamp() -> str:
    """Filename-safe, sortable local timestamp, e.g. 20261019-143005."""
    return now().strftime("%Y%m%d-%H%M%S")


def rel(path: Path, root: Path | None = None) -> str:
    root = root or find_root()
    try:
        return str(Path(path).resolve().relative_to(root))
    except ValueError:
        return str(path)


def die(msg: str, code: int = 1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)
