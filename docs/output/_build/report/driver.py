"""Build the report: PDF through ReportLab and DOCX through python-docx."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(os.path.dirname(HERE))  # docs/output

from doc import Doc  # noqa: E402
import content        # noqa: E402
import builder        # noqa: E402
import front_pdf      # noqa: E402


def make_doc():
    doc = Doc()
    content.build_all(doc)
    assert doc.chapter == 12, f"last chapter is {doc.chapter}"
    assert len(doc.figures) >= 29, len(doc.figures)
    assert len(doc.tables) >= 34, len(doc.tables)
    return doc


def main(pdf=True, docx=True, pdf_path=None, docx_path=None):
    doc = make_doc()
    print(f"blocks {len(doc.blocks)}  figures {len(doc.figures)}  tables {len(doc.tables)}  "
          f"toc {len(doc.toc)}")
    for k, v in content.check_references(doc).items():
        if v:
            print(f"  {k}: {v}")

    if pdf:
        pdf_path = pdf_path or os.path.join(OUT, "Macrova_BCA_Project_Report.pdf")
        d = builder.build(doc, pdf_path, lambda mode, data: front_pdf.make_front(doc, mode, data))
        print(f"PDF  {pdf_path}  pages {d.page}")
        refs = d.refs
        missing = [(lbl, key) for _, lbl, key in doc.toc if not refs.get(key)]
        if missing:
            print("  missing TOC pages:", missing[:8])
        firsts = {}
        for lvl, lbl, key in doc.toc:
            if lvl == 0 and key.startswith("ch"):
                firsts[lbl.split(":")[0]] = max(1, refs.get(key, 0) - d.last_front_page)
        print("  chapter starts:", firsts)
        print("  front pages:", d.last_front_page)

    if docx:
        docx_path = docx_path or os.path.join(OUT, "Macrova_BCA_Project_Report.docx")
        import docxbuild
        print("DOCX", docx_path, docxbuild.build(doc, docx_path))
    return doc


if __name__ == "__main__":
    args = sys.argv[1:]
    main(pdf="--docx" not in args or "--pdf" in args,
         docx="--pdf" not in args or "--docx" in args)
