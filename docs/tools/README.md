# Report generator

The project report is generated from source with ReportLab, so that every figure is vector,
every caption is numbered automatically and the table of contents cannot drift from the body.

    docs/report/Macrova_Project_Report.pdf     <- build output (90 pages)
    docs/tools/theme.py                        <- page geometry, styles, report doc, helpers
    docs/tools/figlib.py                       <- vector drawing toolkit (top-left coordinates)
    docs/tools/screens.py                      <- 12 interface renderings
    docs/tools/diagrams_arch.py                <- architecture, DFD, journey, stack, tokens
    docs/tools/diagrams_uml.py                 <- use case, class, sequence, activity, state, ER
    docs/tools/content_front.py                <- cover, certificate, declaration, abstract, TOC/LOF/LOT
    docs/tools/content_ch1.py                  <- Chapter 1
    docs/tools/content_ch23.py                 <- Chapters 2 and 3
    docs/tools/content_ch4.py                  <- Chapter 4
    docs/tools/content_ch5.py                  <- Chapter 5
    docs/tools/content_ch6.py                  <- Chapter 6 (modules, algorithms, listings, screens)
    docs/tools/content_ch7.py                  <- Chapter 7
    docs/tools/content_ch8.py                  <- Chapter 8 and the reference list
    docs/tools/content_appendix.py             <- Appendices A to D
    docs/tools/build.py                        <- three-pass build driver

## Build

    pip install --break-system-packages reportlab
    python3 docs/tools/build.py                # writes docs/report/Macrova_Project_Report.pdf

An explicit output path may be given: `python3 docs/tools/build.py /tmp/report.pdf`.

## Why three passes

`ReportDoc` records every heading, figure caption and table caption with the page label on
which it lands, and the front matter lists are rendered from those records. Adding entries of
course changes the length of the front matter and therefore every page label after it, so:

    pass 1  empty lists            -> count headings, figures and tables
    pass 2  lists from pass 1      -> page labels for that layout
    pass 3  lists from pass 2      -> final PDF, byte-identical front matter to pass 2

The labels collected in pass 2 are therefore correct for the document written in pass 3.

## Conventions

* Body page numbers are arabic and start at 1 on the first page of Chapter 1; the preliminary
  pages use lower-case roman numerals and the cover is unnumbered.
* Figures are numbered `Figure <chapter>.<n>`, tables `Table <chapter>.<n>`, listings
  `Listing <chapter>.<n>`; appendices pass explicit labels (`Table A.1`, `Listing C.3`).
* Fonts are DejaVu (serif for body, sans for headings and diagrams, mono for code) taken from
  `docs/tools/assets/fonts`; the italic faces are sheared from the roman ones by
  `make_oblique.py`, because no italic TTF is available in that directory.
* Interface figures in Chapter 6 are vector renderings reconstructed from the Angular
  templates and their scoped stylesheets, not photographic captures; the report says so
  explicitly in a note at the end of Chapter 4.
