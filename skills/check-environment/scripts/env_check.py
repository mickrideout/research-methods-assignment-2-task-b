#!/usr/bin/env python3
"""Check the local environment against the `code:` block of context/assignment.md.

Read-only: never installs anything. Prints JSON (default) or a Markdown table.

Usage (from the project root):
  python3 skills/check-environment/scripts/env_check.py            # JSON results
  python3 skills/check-environment/scripts/env_check.py --md       # Markdown table
  python3 skills/check-environment/scripts/env_check.py --smoke    # also run code.starter.smoke_test
  python3 skills/check-environment/scripts/env_check.py --python work/code/.venv/bin/python
Exit status 1 if any requirement FAILs.

Each result: {category, requirement, found, status: PASS|FAIL|WARN|SKIP, detail, fix}.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
sys.path.insert(0, str(TOOLS))
from _common import ToolError, die, find_root, load_details, path_of, rel  # noqa: E402

LANG_CMD = {
    "python": ["{python}", "--version"], "r": ["R", "--version"], "node": ["node", "--version"],
    "javascript": ["node", "--version"], "typescript": ["tsc", "--version"], "java": ["java", "-version"],
    "julia": ["julia", "--version"], "go": ["go", "version"], "rust": ["rustc", "--version"],
    "c": ["gcc", "--version"], "c++": ["g++", "--version"], "cpp": ["g++", "--version"],
    "matlab": ["matlab", "-batch", "disp(version)"], "octave": ["octave", "--version"],
    "sql": ["sqlite3", "--version"], "bash": ["bash", "--version"],
}
LOCK_FILES = ["requirements.txt", "requirements.lock", "uv.lock", "poetry.lock", "Pipfile.lock",
              "environment.yml", "renv.lock", "package-lock.json", "pnpm-lock.yaml", "Cargo.lock", "go.sum"]


def sh(cmd, cwd=None, timeout=60):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                           shell=isinstance(cmd, str))
        return r.returncode, (r.stdout + r.stderr).strip()
    except FileNotFoundError:
        return 127, "not found"
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"


def vtuple(v: str):
    return tuple(int(x) for x in re.findall(r"\d+", v)[:4])


def satisfies(found: str, spec: str | None) -> bool:
    if not spec:
        return True
    fv = vtuple(found)
    for c in spec.split(","):
        m = re.match(r"\s*(>=|<=|==|!=|~=|>|<)?\s*([\d.*]+)", c)
        if not m:
            continue
        op, v = m.group(1) or "==", m.group(2)
        if v.endswith("*"):
            pre = vtuple(v.rstrip(".*"))
            ok = fv[:len(pre)] == pre
            ok = (not ok) if op == "!=" else ok
        else:
            tv = vtuple(v)
            n = max(len(fv), len(tv))
            a, b = fv + (0,) * (n - len(fv)), tv + (0,) * (n - len(tv))
            ok = {">=": a >= b, "<=": a <= b, "==": a == b, "!=": a != b, ">": a > b, "<": a < b,
                  "~=": a >= b and a[:len(tv) - 1] == b[:len(tv) - 1]}[op]
        if not ok:
            return False
    return True


def first_version(text: str) -> str | None:
    m = re.search(r"\d+\.\d+(?:\.\d+)?", text)
    return m.group(0) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--md", action="store_true")
    ap.add_argument("--smoke", action="store_true", help="run code.starter.smoke_test in paths.code_dir")
    ap.add_argument("--python", help="interpreter to check Python packages against")
    a = ap.parse_args()
    try:
        root = find_root()
        d = load_details(root)
        code = d.get("code") or {}
        code_dir = path_of(d, "code_dir", root)
    except ToolError as e:
        die(str(e))
    py = a.python or code.get("interpreter") or (
        str(code_dir / ".venv/bin/python") if (code_dir / ".venv/bin/python").exists() else sys.executable)
    res = []

    def add(cat, req, found, status, detail="", fix=""):
        res.append({"category": cat, "requirement": req, "found": found, "status": status,
                    "detail": detail, "fix": fix})

    if code.get("required") is not True:
        add("scope", "code.required", str(code.get("required")), "SKIP", "details say no code is required")
    add("system", "platform", f"{platform.system()} {platform.release()} ({platform.machine()})", "PASS")

    for lang in code.get("languages") or []:
        name = str(lang.get("name", "")).lower()
        cmd = [c.replace("{python}", py) for c in LANG_CMD.get(name, [name, "--version"])]
        rc, out = sh(cmd)
        ver = first_version(out) if rc == 0 else None
        req = f"{name} {lang.get('version') or ''}".strip()
        if ver is None:
            add("language", req, "not found", "FAIL", out[:200], f"install {name} {lang.get('version') or ''}".strip())
        elif satisfies(ver, lang.get("version")):
            add("language", req, ver, "PASS", " ".join(cmd))
        else:
            add("language", req, ver, "FAIL", "version mismatch", f"install {name} {lang['version']}")

    pip = [p for p in code.get("packages") or [] if (p.get("ecosystem") or "pip") == "pip"]
    if pip:
        probe = ("import json,sys,importlib.metadata as m\nout={}\nfor n in sys.argv[1:]:\n"
                 "    try: out[n]=m.version(n)\n    except Exception: out[n]=None\nprint(json.dumps(out))")
        rc, out = sh([py, "-c", probe, *[p["name"] for p in pip]])
        found = json.loads(out.splitlines()[-1]) if rc == 0 else {}
        for p in pip:
            v = found.get(p["name"])
            req = f"{p['name']}{p.get('version') or ''}"
            if v is None:
                add("package (pip)", req, "not installed", "FAIL", f"interpreter {py}",
                    f"{py} -m pip install '{req}'")
            elif satisfies(v, p.get("version")):
                add("package (pip)", req, v, "PASS")
            else:
                add("package (pip)", req, v, "FAIL", "version mismatch", f"{py} -m pip install '{req}'")
    for p in code.get("packages") or []:
        eco = (p.get("ecosystem") or "pip").lower()
        req = f"{p['name']}{p.get('version') or ''}"
        if eco == "pip":
            continue
        if eco == "npm":
            rc, out = sh(["npm", "ls", p["name"], "--json", "--depth=0"], cwd=code_dir)
            try:
                v = json.loads(out).get("dependencies", {}).get(p["name"], {}).get("version")
            except json.JSONDecodeError:
                v = None
        elif eco in ("r", "cran"):
            rc, out = sh(["Rscript", "-e", f'cat(as.character(packageVersion("{p["name"]}")))'])
            v = first_version(out) if rc == 0 else None
        else:
            add(f"package ({eco})", req, "-", "SKIP", f"no automatic check for ecosystem {eco}; verify by hand")
            continue
        if v and satisfies(v, p.get("version")):
            add(f"package ({eco})", req, v, "PASS")
        else:
            add(f"package ({eco})", req, v or "not installed", "FAIL", "",
                f"npm install '{p['name']}@{p.get('version') or 'latest'}'" if eco == "npm"
                else f"Rscript -e 'install.packages(\"{p['name']}\")'")

    for t in code.get("tools") or []:
        cmd = t.get("check") or f"{t['name']} --version"
        rc, out = sh(cmd)
        add("tool", t["name"], (first_version(out) or "present") if rc == 0 else "not found",
            "PASS" if rc == 0 else "FAIL", out.splitlines()[0][:120] if out else "", t.get("install", ""))

    hw = code.get("hardware") or {}
    if hw.get("gpu"):
        rc, out = sh(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"])
        add("hardware", "GPU", out.splitlines()[0] if rc == 0 and out else "none", "PASS" if rc == 0 else "FAIL",
            "", "" if rc == 0 else "use a GPU machine (lab, cloud) or ask whether CPU runs are acceptable")
        if hw.get("cuda"):
            rc2, out2 = sh(["nvidia-smi"])
            m = re.search(r"CUDA Version:\s*([\d.]+)", out2)
            cv = m.group(1) if m else None
            add("hardware", f"CUDA {hw['cuda']}", cv or "unknown",
                "PASS" if cv and satisfies(cv, str(hw["cuda"])) else "FAIL")
    if hw.get("min_ram_gb"):
        ram = None
        try:
            ram = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30
        except (ValueError, OSError, AttributeError):
            pass
        add("hardware", f"RAM >= {hw['min_ram_gb']} GB", f"{ram:.1f} GB" if ram else "unknown",
            "PASS" if ram and ram >= hw["min_ram_gb"] else ("WARN" if ram is None else "FAIL"))
    if hw.get("min_disk_gb"):
        free = shutil.disk_usage(root).free / 2**30
        add("hardware", f"free disk >= {hw['min_disk_gb']} GB", f"{free:.1f} GB",
            "PASS" if free >= hw["min_disk_gb"] else "FAIL")

    for ds in code.get("datasets") or []:
        p = root / ds.get("path", "")
        ok = p.exists()
        add("dataset", ds.get("name") or ds.get("path"), rel(p, root) if ok else "missing",
            "PASS" if ok else "FAIL", ds.get("source") or "",
            "" if ok else f"download from {ds.get('url') or 'the unit site'} into {ds.get('path')}")

    starter = (code.get("starter") or {})
    sp = root / starter["path"] if starter.get("path") else None
    has_starter = bool(sp and sp.exists() and any(f.name != "README.md" and not f.name.startswith(".")
                                                for f in sp.rglob("*") if f.is_file()))
    code_files = [f for f in code_dir.rglob("*") if f.is_file() and f.name != "README.md"
                  and not f.name.startswith(".") and ".venv" not in f.parts] if code_dir.exists() else []
    if has_starter:
        add("starter code", rel(sp, root), "copied to " + rel(code_dir, root) if code_files else "not copied",
            "PASS" if code_files else "WARN", "", "" if code_files else f"copy {rel(sp, root)}/ into {rel(code_dir, root)}/")
    locks = [f for f in LOCK_FILES if (code_dir / f).exists()]
    if code.get("required") is True:
        add("lock file", "dependency/lock file in " + rel(code_dir, root), ", ".join(locks) or "none",
            "PASS" if locks else "WARN", "", "" if locks else "create one (the skill asks first)")
    if a.smoke:
        cmd = starter.get("smoke_test")
        if not cmd:
            add("smoke test", "code.starter.smoke_test", "not set", "SKIP")
        else:
            rc, out = sh(cmd, cwd=code_dir, timeout=300)
            add("smoke test", cmd, f"exit {rc}", "PASS" if rc == 0 else "FAIL", "\n".join(out.splitlines()[-15:]))

    if a.md:
        print("| Category | Requirement | Found | Status | Detail | Proposed fix |\n|---|---|---|---|---|---|")
        for r in res:
            cells = [str(r[k]).replace("|", "/").replace("\n", "<br>") for k in
                     ("category", "requirement", "found", "status", "detail", "fix")]
            print("| " + " | ".join(cells) + " |")
    else:
        print(json.dumps({"interpreter": py, "results": res}, indent=2))
    sys.exit(1 if any(r["status"] == "FAIL" for r in res) else 0)


if __name__ == "__main__":
    main()
