---
name: research-question
description: Gathers verifiable evidence for ONE named assignment question. It mines the provided readings, lectures and other inputs for quotes and data with page numbers, adds verified BibTeX entries, and lists sources the student must obtain; it searches the web only when research.web_search is true. Writes work/questions/<QID>/research.md. Use when a question's plan shows evidence gaps or the user asks to research, find sources or build an evidence bank for a specific question ID.
---

# research-question

## Purpose

Build an evidence bank of claims, verbatim quotes or data, and exact locations, so the answer
never relies on memory and never cites anything that was not read.

## When to use

- The user names exactly one question ID, usually after `plan-question` lists evidence gaps.
- Re-run to extend the evidence bank (append-only).

Do not use it to draft answer text, to cite sources from memory, or for more than one question.

## Inputs

Path placeholders such as `<bibliography>` mean `paths.bibliography` in the details file.
Argument: **one question ID (required)**.

1. `context/assignment.md` (always first): `referencing`, `research.web_search` and paths.
2. `<questions_dir>/<QID>/plan.md`: the evidence needed. If it is missing, derive the needs from the question and criteria, and say so.
3. `<extracted>/` text of `<inputs>/readings/`, `<inputs>/lectures/` and `<inputs>/exemplars/`; `<bibliography>`.
4. Guide: [references/source-verification.md](references/source-verification.md). Format: `templates/question-research.md`.

## Procedure

1. Confirm the ID (`python3 <tools>/details.py question <QID>`). Read the plan's "Evidence needed" table.
2. Refresh the extracted text: `python3 <tools>/extract_inputs.py`.
3. For each evidence need, search the extracted inputs. Record each hit as: claim supported, verbatim quote or data, `inputs/<path>#p.N`, and how it was verified (opened at that location).
4. If `research.web_search: true`, search for the remaining gaps. Keep only sources whose metadata you can verify (DOI resolves, or publisher or official page). Record the URL. Prefer peer-reviewed and official sources. Do not quote material you have not read in full text. List it under "To obtain" instead.
5. Add BibTeX entries to `<bibliography>` only for sources actually read. Each entry needs a `doi`, `url`, `isbn` or `file` field (`file = {inputs/readings/x.pdf}`). Use keys of the form `authorYYYYword`. Never delete or rewrite existing entries; if one is wrong, report it.
6. Write or extend `<questions_dir>/<QID>/research.md`. Append new rows; keep existing rows.
7. Log the run: `python3 <tools>/log_ai_use.py --skill research-question --qid <QID> --action "Collected evidence (web: on|off)" --files <questions_dir>/<QID>/research.md,<bibliography>`.

## Output

- `<questions_dir>/<QID>/research.md`: evidence bank, bibliography entries added, and a "To obtain" list.
- `<bibliography>`: appended entries only.
- Final message: gaps closed and gaps remaining, sources the user should download into `<inputs>/readings/`, and the next suggested command (not run).

## Quality checks

- Every quote appears verbatim in the cited extracted text or the opened page.
- Every new bib entry has `doi`, `url`, `isbn` or `file`, and was read.
- No bib entry was removed or altered.
- Web search was used only if enabled.

## If inputs are missing

- No readings and web search off: produce the "To obtain" list (topics, search terms, likely source types) and stop. Do not fill gaps from memory.
- A source is behind a paywall or unreadable: list it under "To obtain" with its DOI or URL.
- No plan: proceed from the question and criteria, and recommend running plan-question.
