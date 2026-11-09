"""Render the same Doc model into a Word document with python-docx."""

import os

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import front
from builder import ASSETS

TEAL = RGBColor(0x0F, 0x5F, 0x55)
GREY = RGBColor(0x5B, 0x6B, 0x70)
BODY_FONT = "Times New Roman"


def _field(par, instr):
    run = par.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), instr)
    run._r.addnext(fld)


def page_number_footer(section):
    par = section.footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    par._p.append(fld)


def shade(cell, colour):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), colour)
    tc_pr.append(shd)


def setup(doc):
    st = doc.styles["Normal"]
    st.font.name = BODY_FONT
    st.font.size = Pt(12)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.4
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for name, size, colour, bold in [("Heading 1", 18, TEAL, True), ("Heading 2", 14, TEAL, True),
                                     ("Heading 3", 12, RGBColor(0x11, 0x11, 0x11), True)]:
        h = doc.styles[name]
        h.font.name = BODY_FONT
        h.font.size = Pt(size)
        h.font.bold = bold
        h.font.color.rgb = colour
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h.paragraph_format.keep_with_next = True


def para(doc, text, size=12, bold=False, italic=False, align=None, space_after=6):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p


def rich_para(doc, text, style="Normal"):
    """Handle the small <b>/<i> tag set used by the content files."""
    p = doc.add_paragraph(style=style)
    buf, tag = "", None
    i = 0
    while i < len(text):
        if text[i] == "<" and text[i + 1:i + 2] in ("b", "i") and text[i + 2] == ">":
            if buf:
                r = p.add_run(buf)
                r.bold = tag == "b"
                r.italic = tag == "i"
                buf = ""
            tag = text[i + 1]
            i += 3
        elif text[i:i + 4] in ("</b>", "</i>"):
            if buf:
                r = p.add_run(buf)
                r.bold = tag == "b"
                r.italic = tag == "i"
                buf = ""
            tag = None
            i += 4
        else:
            buf += text[i]
            i += 1
    if buf:
        r = p.add_run(buf)
        r.bold = tag == "b"
        r.italic = tag == "i"
    return p


def add_table(doc, block):
    rows = len(block.rows) + 1
    cols = len(block.header)
    t = doc.add_table(rows=rows, cols=cols)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    size = max(7.0, float(block.meta.get("font") or 8.6) - 1.0)
    widths = block.meta.get("widths")
    total = float(sum(widths)) if widths else cols
    for j, head in enumerate(block.header):
        cell = t.cell(0, j)
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(head)
        r.bold = True
        r.font.size = Pt(size)
        shade(cell, "E8F2F1")
    for i, row in enumerate(block.rows, start=1):
        for j, value in enumerate(row):
            cell = t.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            r = p.add_run(str(value))
            r.font.size = Pt(size)
            p.paragraph_format.space_after = Pt(1)
    if widths:
        for j in range(cols):
            w = Cm(16.0 * float(widths[j]) / total)
            for row in t.rows:
                row.cells[j].width = w
    return t


def build(doc_model, out_path):
    doc = Document()
    setup(doc)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.top_margin = sec.bottom_margin = Cm(2.2)
    page_number_footer(sec)

    # ------------------------------------------------------------- title page
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(f"{ASSETS}/macrova-logo.png", width=Cm(2.6))
    para(doc, "A PROJECT REPORT", 12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    for line in front.TITLE_LINES:
        para(doc, line, 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    for text, bold in [("A project report submitted to", False),
                       ("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY", True),
                       ("in partial fulfillment of the requirements for the award of the degree of",
                        False),
                       ("BACHELOR OF COMPUTER APPLICATIONS", True),
                       ("BY", False), (front.STUDENT, True),
                       (f"REG. NO. <{front.REGNUM}>", False),
                       ("UNDER THE GUIDANCE OF", False), (front.GUIDE, True),
                       ("ASSISTANT PROFESSOR, SRMIST-DDE", False),
                       ("DEPARTMENT OF COMPUTER APPLICATIONS", True),
                       ("DIRECTORATE OF DISTANCE EDUCATION", True),
                       ("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY", True),
                       ("(Deemed to be university u/s 3 of UGC Act, 1956)", False),
                       ("Kattankulathur \u2013 603 203, Chennai, Tamilnadu", False),
                       (front.MONTH, True)]:
        para(doc, text, 11.5, bold=bold, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)

    def heading_page(title, paragraphs, sign=None):
        doc.add_page_break()
        doc.add_heading(title, level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
        for text in paragraphs:
            para(doc, text)
        if sign:
            for _ in range(2):
                para(doc, "")
            para(doc, sign, align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)

    heading_page("BONAFIDE CERTIFICATE", front.CERTIFICATE,
                 f"{front.SIGN_GUIDE}\n\nPROJECT GUIDE")
    heading_page("DECLARATION", front.DECLARATION, front.STUDENT)
    heading_page("ACKNOWLEDGEMENT", front.ACKNOWLEDGEMENT, front.STUDENT)
    heading_page("ABSTRACT", front.ABSTRACT)
    para(doc, "Keywords: " + front.KEYWORDS, 11)

    # ------------------------------------------------------- contents pages
    doc.add_page_break()
    doc.add_heading("TABLE OF CONTENTS", level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), r'TOC \o "1-3" \h \z \u')
    holder = OxmlElement("w:r")
    t_el = OxmlElement("w:t")
    t_el.text = "Right-click and choose Update Field to build the contents."
    holder.append(t_el)
    fld.append(holder)
    p._p.append(fld)

    for kind, items in [("LIST OF FIGURES", doc_model.figures),
                        ("LIST OF TABLES", doc_model.tables)]:
        doc.add_page_break()
        doc.add_heading(kind, level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
        for label, caption, _key in items:
            para(doc, f"{kind.split()[-1].capitalize()} {label}: {caption}", 10.5, space_after=2)

    # ----------------------------------------------------------- abbreviations
    doc.add_page_break()
    doc.add_heading("ABBREVIATIONS AND ACRONYMS", level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    t = doc.add_table(rows=len(front.ABBREV) + 1, cols=2)
    t.style = "Table Grid"
    for j, head in enumerate(["Abbreviation", "Expansion"]):
        c = t.cell(0, j)
        c.text = ""
        r = c.paragraphs[0].add_run(head)
        r.bold = True
        shade(c, "E8F2F1")
    for i, (a, b) in enumerate(front.ABBREV, start=1):
        t.cell(i, 0).text = a
        t.cell(i, 1).text = b

    # ------------------------------------------------------------------- body
    for block in doc_model.blocks:
        k = block.kind
        if k == "chapter":
            doc.add_page_break()
            para(doc, f"CHAPTER {block.meta['number']}", 15, bold=True,
                 align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
            h = doc.add_heading(block.text.upper(), level=1)
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif k == "part":
            doc.add_page_break()
            doc.add_heading(block.text.upper(), level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif k == "h2":
            doc.add_heading(block.text, level=2)
        elif k == "h3":
            doc.add_heading(block.text, level=3)
        elif k == "p":
            if block.text:
                rich_para(doc, block.text)
        elif k == "bullets":
            for item in block.items:
                rich_para(doc, item, style="List Bullet")
        elif k == "numbered":
            for item in block.items:
                rich_para(doc, item, style="List Number")
        elif k == "note":
            rich_para(doc, block.text)
        elif k == "code":
            cap = para(doc, block.caption, 9.5, bold=True, italic=True, space_after=2)
            cap.paragraph_format.keep_with_next = True
            for line in block.text.rstrip("\n").split("\n"):
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(line if line else " ")
                r.font.name = "Consolas"
                r.font.size = Pt(8)
            para(doc, "", space_after=4)
        elif k == "table":
            cap = para(doc, f"Table {block.meta['label']}: {block.caption}", 9.5, bold=True,
                       italic=True, space_after=3)
            cap.paragraph_format.keep_with_next = True
            add_table(doc, block)
            para(doc, "", space_after=6)
        elif k == "figure":
            path = block.path if os.path.isabs(block.path) else os.path.join(ASSETS, block.path)
            from PIL import Image as PILImage
            w, h = PILImage.open(path).size
            width = min(block.width, 16.0)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(path, width=Cm(width))
            cap = para(doc, f"Figure {block.meta['label']}: {block.caption}", 9.5, bold=True,
                       italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
        elif k == "pagebreak":
            doc.add_page_break()
        elif k == "spacer":
            para(doc, "", space_after=2)
        else:
            raise ValueError(k)

    doc.save(out_path)
    return (f"{len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables, "
            f"{len(doc.sections)} sections, {len(doc.inline_shapes)} images")
