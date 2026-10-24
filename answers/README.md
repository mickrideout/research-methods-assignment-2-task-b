# answers/

`answers.md` is the single common answer file, created by `python3 tools/answer_section.py init`
(define-details runs it). Each question owns a section between `<!-- BEGIN <ID> -->` and
`<!-- END <ID> -->`. Sections are written only with `tools/answer_section.py put`, which leaves
everything else byte-identical.
