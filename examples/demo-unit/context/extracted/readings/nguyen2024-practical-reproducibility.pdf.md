<!-- extracted from inputs/readings/nguyen2024-practical-reproducibility.pdf sha256=2f8225f9a075b4ee06f9612aabeb228529d6ad319eb3a139b3f44997da38385d on 2026-10-19T09:50:17+11:00 via pdftotext -->

## [p. 1]

                     Practical reproducibility for data analysts

                  A. Nguyen (FICTIONAL READING for the template demo)

                                                   2024


Introduction
Analyses fail to reproduce mainly because the computational environment is not recorded. Pinning package
versions in a lock file allows another analyst to rebuild the environment, although lock files alone do not
capture operating-system libraries.


Version control
Version control records every change to analysis code, which makes it possible to identify exactly which code
produced a result. However, version control does not track large data files well, so data versions must be
managed separately.


Conclusion
No single practice guarantees reproducibility; practices must be combined.




                                                     1
