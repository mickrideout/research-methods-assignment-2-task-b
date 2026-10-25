# assignment_template

A template project for answering a Master's-level assignment with an AI agent. You copy it once
per assignment. Agent skills take you from "assignment released" to "ready to submit":

- understanding the brief
- sharpening the rubric
- answering one question at a time
- grading against the rubric before you submit

Agent-facing instructions are in [AGENTS.md](AGENTS.md).

## Requirements

- Python 3.10+ with PyYAML (`python3 -m pip install -r tools/requirements.txt`)
- pandoc (export), poppler-utils `pdftotext` (PDF extraction)
- For PDF output: xelatex (TeX Live). PDF is compiled from a LaTeX file that pandoc writes first
- Any agent that can read files and run shell commands. Skills are in the open Agent Skills
  format under `skills/`.

## Start a new assignment

```bash
git clone --origin template <this-template-repo> COMP9001-A2
cd COMP9001-A2
python3 tools/init_project.py          # copies templates, creates agent symlinks; never overwrites
```

Then drop the files into `inputs/`. Each subfolder's README says what goes there.
At minimum you need `spec/` and `rubric/`. The rest makes the rubric and the answers better.

To pull later template fixes (skills, tools) into an assignment: `git pull template main`.

### Agent setup

- **Agents that read `AGENTS.md`** (most do): nothing to do.
- **Agents that read `CLAUDE.md` and `.claude/skills/`**: the symlinks are already created.
- **Other agents with a skills folder**: one line, e.g. `mkdir -p .agents && ln -s ../skills .agents/skills`.
  Check your agent's docs for its folder name. Never copy the files.
- **Agents without skills support**: say "follow skills/answer-question/SKILL.md for Q2". AGENTS.md
  tells them how.

## Running each step

Invoke skills by name, e.g. `/answer-question Q2` in agents with slash commands, or
"run answer-question for Q2" in plain language.

| Step | You say | What you get |
|---|---|---|
| 1 | `define-details` | `context/assignment.md` filled in, plus a list of **open questions** |
| 1h | (you) answer the open questions in `context/assignment.md` (`answer:` fields) | |
| 2 | `enhance-rubric` | `context/rubric.md` / `.yaml`, `context/checklist.md` / `.yaml` |
| 3 | `check-environment` (code assignments only) | `reports/environment/<ts>.md` |
| 4 | `plan-question Q1` | `work/questions/Q1/plan.md` |
| 5 | `research-question Q1` (optional) | evidence bank, `.bib` entries, a "to obtain" list for you |
| 6 | `run-experiments Q2` (code questions) | code, figures and tables, `work/results/manifest.yaml` |
| 7 | `answer-question Q1` | section Q1 of `answers/answers.md` |
| 8 | `grade-question Q1` (preferably in a **new session**) | `reports/grading/Q1/<ts>.md` |
| 7r | `answer-question Q1 --from reports/grading/Q1/<ts>.md` | revised section Q1 |
| 9 | `check-compliance` | `reports/compliance/<ts>.md` |
| 10 | `grade-assignment` | total estimate, band, prioritised fix list |
| 11 | `export-submission` | `export/<file>.docx`/`.pdf`, GO / NO-GO report |

Agents never answer a question you didn't name, and graders never edit answers.

Useful direct commands:

```bash
python3 tools/details.py validate        # is the details file complete?
python3 tools/details.py open            # unresolved open questions
python3 tools/answer_section.py list     # sections, word counts, status
python3 tools/wordcount.py               # word counts vs limits
python3 skills/grade-assignment/scripts/report_status.py   # which grades are stale
python3 tools/compliance.py              # quick compliance check
```

## A typical session

1. Day 1:
   - Clone, run `init_project.py`, add the spec and rubric, and run `define-details`.
   - Answer its open questions; ask on the unit forum if needed, and save the replies to `inputs/clarifications/`.
   - Run `enhance-rubric`, and read `context/rubric.md`. It's the best summary of what the marker wants.
   - Commit.
2. For each question:
   - Run `plan-question Qn` and check the plan.
   - Add the readings it asks for, then run `research-question Qn` and/or `run-experiments Qn`.
   - Run `answer-question Qn`, then commit.
   - Open a **new session** and run `grade-question Qn`.
   - Revise with `answer-question Qn --from <report>` until the gains flatten out.
3. Near the deadline:
   - Run `check-compliance` and `grade-assignment`.
   - Work the fix list from the top.
   - Run `export-submission`, then read the exported file yourself.
   - Fill in the "Your review" column of `work/ai-use-log.md`.
   - Submit.

## Where things live

| Path | What |
|---|---|
| `inputs/` | originals from the university (read-only for agents) |
| `context/assignment.md` | **common details file**: facts and all paths; every skill reads it first |
| `context/rubric.*`, `context/checklist.*` | enhanced rubric and requirements checklist |
| `work/` | plans, research, references, code, results, AI-use log |
| `answers/answers.md` | **the one answer file**, in per-question sections |
| `reports/` | timestamped grading, compliance, environment and pre-submission reports |
| `export/` | what you upload |
| `templates/` | fill-in templates (copied by setup; don't edit them in an instance) |
| `skills/`, `tools/` | the skills and their scripts |
| `examples/demo-unit/` | a fictional assignment taken through every stage |

Verify the template still works with `python3 tools/selftest.py` and `python3 tools/validate_skills.py`.

## Skills reference

These are other skill collections, for inspiration:

- research-agent-skills - https://github.com/KalarisLabs/research-agent-skills
- teaching-skills - https://github.com/YujxZJCN/teaching-skills
