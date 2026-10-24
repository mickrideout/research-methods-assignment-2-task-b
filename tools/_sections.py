"""Parse the delimited sections of the common answer file.

A section is:
    <!-- BEGIN Q2 -->
    ...inner content...
    <!-- END Q2 -->
Markers must sit on their own lines. Parsing works on bytes so that callers
can guarantee everything outside a section stays byte-identical.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from _common import QID_PATTERN, ToolError

_ID = QID_PATTERN.encode()
MARKER_RE = re.compile(rb"^<!-- (BEGIN|END) (" + _ID + rb") -->[ \t]*\r?$", re.M)
LOOSE_RE = re.compile(rb"^[ \t]*<!--[ \t]*(BEGIN|END)\b.*$", re.M | re.I)
META_RE = re.compile(r"^<!-- meta: .*-->[ \t]*\r?\n?", re.M)


@dataclass
class Span:
    id: str
    begin: int        # offset of the BEGIN line
    inner_start: int  # offset just after the BEGIN line's newline
    inner_end: int    # offset of the END line
    end: int          # offset just after the END line (incl. newline if present)


def _line_end(data: bytes, pos: int) -> int:
    nl = data.find(b"\n", pos)
    return len(data) if nl == -1 else nl + 1


def parse(data: bytes) -> dict[str, Span]:
    """Return sections in file order. Raises ToolError on malformed markers."""
    strict = {m.start() for m in MARKER_RE.finditer(data)}
    for m in LOOSE_RE.finditer(data):
        if m.start() not in strict:
            line = data.count(b"\n", 0, m.start()) + 1
            raise ToolError(f"malformed section marker on line {line}: {m.group(0).decode(errors='replace').strip()!r}"
                            " (expected '<!-- BEGIN <ID> -->' or '<!-- END <ID> -->' on its own line)")
    spans: dict[str, Span] = {}
    open_id = open_at = None
    for m in MARKER_RE.finditer(data):
        kind, sid = m.group(1).decode(), m.group(2).decode()
        line = data.count(b"\n", 0, m.start()) + 1
        if kind == "BEGIN":
            if open_id is not None:
                raise ToolError(f"line {line}: BEGIN {sid} inside open section {open_id} (nesting not allowed)")
            if sid in spans:
                raise ToolError(f"line {line}: duplicate section {sid}")
            open_id, open_at = sid, m.start()
        else:
            if open_id != sid:
                raise ToolError(f"line {line}: END {sid} does not close {open_id or 'any open section'}")
            spans[sid] = Span(sid, open_at, _line_end(data, open_at), m.start(), _line_end(data, m.start()))
            open_id = None
    if open_id is not None:
        raise ToolError(f"section {open_id} has no END marker")
    return spans


def newline_of(data: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in data else b"\n"


def inner_text(data: bytes, span: Span) -> str:
    return data[span.inner_start:span.inner_end].decode("utf-8")
