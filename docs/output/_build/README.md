# Report build

Rebuild the report from the repository root:

```sh
cd docs/output/_build
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
python logo.py                       # regenerates assets/macrova-logo.png
python crop_shots.py                 # regenerates assets/shots/shot-1..15.png
cd report && ../.venv/bin/python -c "import driver; driver.main()"
```

`driver.main(pdf=True, docx=True)` writes
`docs/output/Macrova_BCA_Project_Report.pdf` and `.docx`.

## Layout of the build directory

| Path | Contents |
| --- | --- |
| `report/doc.py` | renderer-agnostic block model, heading registers, figure and table numbering |
| `report/content_a.py` | chapters 1–4 |
| `report/content_b.py` | chapters 5–8 |
| `report/content_c.py` | chapters 9–12, references, appendices A–D |
| `report/content.py` | `build_all()` plus the cross-reference audit |
| `report/pdfkit.py` | fonts, styles, page templates, `MacrovaDoc` |
| `report/builder.py` | Doc → ReportLab flowables, iterative two-pass build |
| `report/front.py`, `report/front_pdf.py` | preliminary pages |
| `report/docxbuild.py` | Doc → Word document |
| `report/driver.py` | entry point |
| `fonts/` | four Tinos faces converted from WOFF (Times-metric compatible) |
| `crop_shots.py` | trims browser chrome and canvas margins from `assets/N-*.png` |
| `logo.py` | draws the brand mark with matplotlib |

## Notes

* The Tinos latin subset lacks `≈ ≤ ≥`; use words instead.
* `register_fonts()` must run before any ReportLab paragraph is built — the
  `styles()` accessor does it.
* The two-pass build iterates to a fixed point so that the table of contents
  page numbers stay correct once the contents itself grows to three pages.
