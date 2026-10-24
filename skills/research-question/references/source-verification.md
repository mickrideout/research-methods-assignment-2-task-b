# Source verification rules

## Acceptable evidence

| Source | Accept when | Record |
|---|---|---|
| Provided readings and lectures | Always (they are in `inputs/`) | `inputs/<path>#p.N` plus a bib entry with `file` |
| Journal article / conference paper | DOI resolves and metadata matches; full text read | `doi` |
| Book / chapter | ISBN or publisher page matches; the relevant pages read | `isbn`, pages |
| Official report, standard, documentation | Hosted on the issuing body's domain | `url`, access date (`urldate`) |
| Preprint | Only if the spec allows, or no peer-reviewed alternative exists; label it as a preprint | `url`/`doi`, `note = {preprint}` |
| Blog, forum, AI output, Wikipedia | Not as evidence. Fine for finding a real source | n/a |

## Never

- Cite from memory or from an abstract alone for a claim the abstract does not state.
- Invent page numbers. If a location is unknown, write "location unknown". The source cannot then be quoted.
- Paraphrase in a way that changes a claim's strength (e.g. "may" → "does").
- Add an entry to `.bib` for a source that has not been read.

## BibTeX conventions

```bibtex
@article{smith2021reproducibility,
  author  = {Smith, Jane and Lee, Wei},
  title   = {Reproducibility in Practice},
  journal = {Journal of Data Science},
  year    = {2021},
  volume  = {19},
  pages   = {1--20},
  doi     = {10.1234/jds.2021.001},
}
@misc{unit2026week3,
  author = {{DSCI9001 Teaching Team}},
  title  = {Week 3: Reproducible Workflows (lecture slides)},
  year   = {2026},
  file   = {inputs/lectures/week03.pptx},
}
```

Keys: `firstauthorYYYYfirstword`, lowercase. Cite in answers as `[@smith2021reproducibility, p. 4]`.
