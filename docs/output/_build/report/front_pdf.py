"""Preliminary pages for the PDF build (ReportLab flowables)."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (Image, NextPageTemplate, PageBreak, Paragraph, Spacer,
                                Table, TableStyle)

import front
from builder import ASSETS, toc_line
from doc import Doc
from pdfkit import FRAME_W, TEAL, esc, roman, styles

S = styles()

TITLE_MAIN = ParagraphStyle("tm", fontName="TNR-Bold", fontSize=14.4, leading=19,
                            alignment=TA_CENTER, textColor=colors.HexColor("#0f3b3a"),
                            spaceAfter=5)
TITLE_SUB = ParagraphStyle("ts", fontName="TNR", fontSize=11.5, leading=15.5,
                           alignment=TA_CENTER, textColor=colors.HexColor("#111111"))
TITLE_BOLD = ParagraphStyle("tb", fontName="TNR-Bold", fontSize=12, leading=16,
                            alignment=TA_CENTER, textColor=colors.HexColor("#111111"))
HEAD = ParagraphStyle("head", fontName="TNR-Bold", fontSize=16, leading=20, alignment=TA_CENTER,
                      textColor=TEAL, spaceAfter=18)
BODY = ParagraphStyle("fb", fontName="TNR", fontSize=12, leading=18.4, alignment=TA_JUSTIFY,
                      spaceAfter=10)
SIGN = ParagraphStyle("sig", parent=BODY, alignment=TA_CENTER)


def _k(par, key):
    par._key = key
    return par


def title_page():
    s = [Spacer(1, 4)]
    logo = Image(f"{ASSETS}/macrova-logo.png", width=1.0 * inch, height=1.0 * inch)
    logo.hAlign = "CENTER"
    s += [logo, Spacer(1, 10), _k(Paragraph("A PROJECT REPORT", TITLE_BOLD), "fp-title"),
          Spacer(1, 10)]
    for line in front.TITLE_LINES:
        s.append(Paragraph(esc(line), TITLE_MAIN))
    s += [Spacer(1, 14)]
    for text, style in [
        ("A project report submitted to", TITLE_SUB),
        ("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY", TITLE_BOLD),
        ("in partial fulfillment of the requirements for the award of the degree of", TITLE_SUB),
        ("BACHELOR OF COMPUTER APPLICATIONS", TITLE_BOLD),
    ]:
        s.append(Paragraph(esc(text), style))
    s.append(Spacer(1, 14))
    s.append(Paragraph("BY", TITLE_SUB))
    s.append(Paragraph(front.STUDENT, TITLE_BOLD))
    s.append(Paragraph(f"REG. NO. &lt;{front.REGNUM}&gt;", TITLE_SUB))
    s.append(Spacer(1, 14))
    s.append(Paragraph("UNDER THE GUIDANCE OF", TITLE_SUB))
    s.append(Paragraph(front.GUIDE, TITLE_BOLD))
    s.append(Paragraph("ASSISTANT PROFESSOR, SRMIST-DDE", TITLE_SUB))
    s.append(Spacer(1, 16))
    for text in ["DEPARTMENT OF COMPUTER APPLICATIONS", "DIRECTORATE OF DISTANCE EDUCATION",
                 "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY"]:
        s.append(Paragraph(text, TITLE_BOLD))
    s.append(Paragraph("(Deemed to be university u/s 3 of UGC Act, 1956)", TITLE_SUB))
    s.append(Paragraph("Kattankulathur \u2013 603 203, Chennai, Tamilnadu", TITLE_SUB))
    s.append(Spacer(1, 12))
    s.append(Paragraph(front.MONTH, TITLE_BOLD))
    return s


def certificate():
    s = [Spacer(1, 18), _k(Paragraph("BONAFIDE CERTIFICATE", HEAD), "fp-cert")]
    for para in front.CERTIFICATE:
        s.append(Paragraph(esc(para), BODY))
    s.append(Spacer(1, 52))
    row = Table([[Paragraph("", SIGN), Paragraph("", SIGN)],
                 [Paragraph("<b>PROJECT GUIDE</b>", SIGN),
                  Paragraph("<b>HEAD OF THE DEPARTMENT</b>", SIGN)],
                 [Paragraph(front.SIGN_GUIDE.replace("\n", "<br/>"), SIGN),
                  Paragraph(front.SIGN_HOD.replace("\n", "<br/>"), SIGN)]],
                colWidths=[FRAME_W * 0.5, FRAME_W * 0.5])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    s.append(row)
    s.append(Spacer(1, 34))
    exam = Table([[Paragraph("<b>INTERNAL EXAMINER</b>", SIGN),
                   Paragraph("<b>EXTERNAL EXAMINER</b>", SIGN)]],
                 colWidths=[FRAME_W * 0.5, FRAME_W * 0.5])
    exam.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 26)]))
    s.append(exam)
    return s


def declaration():
    s = [Spacer(1, 18), _k(Paragraph("DECLARATION", HEAD), "fp-decl")]
    s.append(Paragraph("I declare that this project report is my own work.", BODY))
    s.append(Spacer(1, 6))
    for para in front.DECLARATION:
        s.append(Paragraph(esc(para), BODY))
    s.append(Spacer(1, 40))
    s.append(Table([[Paragraph("", SIGN), Paragraph("<b>Signature of the Candidate</b>", SIGN)]],
                   colWidths=[FRAME_W * 0.55, FRAME_W * 0.45]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Place: Chennai<br/>Date: ", ParagraphStyle("pl", parent=BODY)))
    return s


def acknowledgement():
    s = [Spacer(1, 18), _k(Paragraph("ACKNOWLEDGEMENT", HEAD), "fp-ack")]
    for para in front.ACKNOWLEDGEMENT:
        s.append(Paragraph(esc(para), BODY))
    s.append(Spacer(1, 24))
    s.append(Table([[Paragraph("", SIGN), Paragraph("<b>" + front.STUDENT + "</b>", SIGN)]],
                   colWidths=[FRAME_W * 0.55, FRAME_W * 0.45]))
    return s


def abstract():
    s = [Spacer(1, 18), _k(Paragraph("ABSTRACT", HEAD), "fp-abs")]
    for para in front.ABSTRACT:
        s.append(Paragraph(esc(para), BODY))
    s.append(Spacer(1, 4))
    s.append(Paragraph("<b>Keywords:</b> " + esc(front.KEYWORDS), BODY))
    return s


def _page_of(refs, key):
    if not refs:
        return "--"
    page = refs.get(key)
    return roman(page) if page else "--"


def toc_page(doc: Doc, data):
    refs = data[0] if data else None
    offset = data[1] if data else 0
    s = [Spacer(1, 6), _k(Paragraph("TABLE OF CONTENTS", S.toch), "fp-toc")]

    def body_page(key):
        if not refs:
            return "--"
        page = refs.get(key)
        return str(max(1, page - offset)) if page else "--"

    prelim = [("Title Page", "fp-title"), ("Bonafide Certificate", "fp-cert"),
              ("Declaration", "fp-decl"), ("Acknowledgement", "fp-ack"),
              ("Abstract", "fp-abs"), ("Table of Contents", "fp-toc"),
              ("List of Figures", "fp-figure"), ("List of Tables", "fp-table"),
              ("Abbreviations and Acronyms", "fp-abbrev")]
    for label, key in prelim:
        s.append(toc_line(label, _page_of(refs, key), S.toc1))
    s.append(Spacer(1, 8))
    for level, label, key in doc.toc:
        style = S.toc0 if level == 0 else (S.toc1 if level == 1 else S.toc2)
        s.append(toc_line(label, body_page(key), style))
    return s


def list_page(doc: Doc, data, kind):
    refs = data[0] if data else None
    offset = data[1] if data else 0
    items = doc.figures if kind == "figure" else doc.tables
    head = "LIST OF FIGURES" if kind == "figure" else "LIST OF TABLES"
    s = [Spacer(1, 6), _k(Paragraph(head, S.toch), "fp-" + kind)]
    for label, caption, key in items:
        page = refs.get(key) if refs else None
        page_txt = str(max(1, page - offset)) if page else "--"
        s.append(toc_line(f"{kind.capitalize()} {label}: {caption}", page_txt, S.toc1))
    return s


def abbreviations():
    s = [Spacer(1, 6), _k(Paragraph("ABBREVIATIONS AND ACRONYMS", S.toch), "fp-abbrev")]
    rows = [[Paragraph("<b>Abbreviation</b>", S.cell_styles(8.6)[1]),
             Paragraph("<b>Expansion</b>", S.cell_styles(8.6)[1])]]
    for a, b in front.ABBREV:
        rows.append([Paragraph(f"<b>{esc(a)}</b>", S.cell_styles(8.6)[0]),
                     Paragraph(esc(b), S.cell_styles(8.6)[0])])
    t = Table(rows, colWidths=[FRAME_W * 0.24, FRAME_W * 0.76], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b9c9cd")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f2f1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(t)
    return s


def make_front(doc: Doc, mode, data):
    s = list(title_page())
    s.append(NextPageTemplate("front"))
    for builder in (certificate, declaration, acknowledgement, abstract):
        s.append(PageBreak())
        s.extend(builder())
    s.append(PageBreak())
    s.extend(toc_page(doc, data))
    s.append(PageBreak())
    s.extend(list_page(doc, data, "figure"))
    s.append(PageBreak())
    s.extend(list_page(doc, data, "table"))
    s.append(PageBreak())
    s.extend(abbreviations())
    return s
