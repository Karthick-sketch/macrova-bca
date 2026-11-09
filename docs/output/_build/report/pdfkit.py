"""Typography, page templates and the two-pass document class for the PDF build."""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(os.path.dirname(HERE), "fonts")

PDF_W, PDF_H = A4
LM = RM = 90
TM = 74
BM = 74
FRAME_W = PDF_W - LM - RM
FRAME_H = PDF_H - TM - BM

TEAL = colors.HexColor("#0f5f55")
GREY = colors.HexColor("#5b6b70")
RULE = colors.HexColor("#c8d6d6")
DOT = colors.HexColor("#a9b8b8")
HEAD_BG = colors.HexColor("#e8f2f1")

ROMAN = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
         (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]


def roman(n):
    if not n:
        return "--"
    out = []
    for value, glyph in ROMAN:
        while n >= value:
            out.append(glyph)
            n -= value
    return "".join(out)


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rich(text):
    """Escape, then restore the small inline tag set the content files use."""
    text = esc(text)
    for tag in ("b", "i"):
        text = text.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return text


def register_fonts():
    if "TNR" in pdfmetrics.getRegisteredFontNames():
        return
    pairs = [("TNR", "Tinos-400-normal.ttf"), ("TNR-Bold", "Tinos-700-normal.ttf"),
             ("TNR-Italic", "Tinos-400-italic.ttf"),
             ("TNR-BoldItalic", "Tinos-700-italic.ttf")]
    for name, filename in pairs:
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, filename)))
    pdfmetrics.registerFontFamily("TNR", normal="TNR", bold="TNR-Bold",
                                  italic="TNR-Italic", boldItalic="TNR-BoldItalic")


class _S:
    """Style namespace, filled once the fonts are registered."""

    def __init__(self):
        self.body = ParagraphStyle("body", fontName="TNR", fontSize=12, leading=17.4,
                                   alignment=TA_JUSTIFY, spaceAfter=7,
                                   hyphenationLang="en_GB")
        self.bullet = ParagraphStyle("bullet", parent=self.body, leftIndent=20,
                                     bulletIndent=6, spaceAfter=5)
        self.bullet_left = ParagraphStyle("bulletl", parent=self.body, leftIndent=20,
                                          bulletIndent=6, spaceAfter=5,
                                          alignment=TA_LEFT)
        self.note = ParagraphStyle("note", parent=self.body, leftIndent=18, rightIndent=18,
                                   fontSize=11.4, leading=16.4)
        self.h2 = ParagraphStyle("h2", fontName="TNR-Bold", fontSize=13.6, leading=17.5,
                                 textColor=TEAL, spaceBefore=13, spaceAfter=5)
        self.h3 = ParagraphStyle("h3", fontName="TNR-Bold", fontSize=12, leading=15.5,
                                 spaceBefore=9, spaceAfter=3)
        self.chapter_no = ParagraphStyle("chno", fontName="TNR-Bold", fontSize=15, leading=18,
                                         alignment=TA_CENTER, textColor=GREY, spaceAfter=4)
        self.chapter_title = ParagraphStyle("cht", fontName="TNR-Bold", fontSize=18, leading=22,
                                            alignment=TA_CENTER, textColor=TEAL,
                                            spaceBefore=2, spaceAfter=10)
        self.part_title = ParagraphStyle("part", fontName="TNR-Bold", fontSize=19, leading=24,
                                         alignment=TA_CENTER, textColor=TEAL,
                                         spaceBefore=120, spaceAfter=14)
        self.figcap = ParagraphStyle("figcap", fontName="TNR-BoldItalic", fontSize=10, leading=13,
                                     alignment=TA_CENTER, spaceBefore=3, spaceAfter=11,
                                     textColor=colors.HexColor("#243a3a"))
        self.tabcap = ParagraphStyle("tabcap", fontName="TNR-BoldItalic", fontSize=10, leading=13,
                                     alignment=TA_LEFT, spaceAfter=4,
                                     textColor=colors.HexColor("#243a3a"))
        self.codecap = ParagraphStyle("codecap", fontName="TNR-BoldItalic", fontSize=9.6,
                                      leading=12.6, spaceBefore=5, spaceAfter=3)
        self.code = ParagraphStyle("code", fontName="Courier", fontSize=7.3, leading=9.4,
                                   alignment=TA_LEFT)
        self.toch = ParagraphStyle("toch", fontName="TNR-Bold", fontSize=13, leading=16,
                                   alignment=TA_CENTER, textColor=TEAL, spaceAfter=12)
        self.toc0 = ParagraphStyle("toc0", fontName="TNR-Bold", fontSize=10.6, leading=15,
                                   spaceBefore=7)
        self.toc1 = ParagraphStyle("toc1", fontName="TNR", fontSize=10.2, leading=14,
                                   leftIndent=14)
        self.toc2 = ParagraphStyle("toc2", fontName="TNR", fontSize=9.6, leading=12.8,
                                   leftIndent=30)
        self.cell = None
        self.cell_head = None
        self._cells = {}

    def cell_styles(self, size):
        key = round(size, 1)
        if key not in self._cells:
            head = ParagraphStyle(f"ch{key}", fontName="TNR-Bold", fontSize=key,
                                  leading=key + 2.6)
            cell = ParagraphStyle(f"cc{key}", fontName="TNR", fontSize=key, leading=key + 2.6)
            self._cells[key] = (cell, head)
        return self._cells[key]


S = None


def styles():
    global S
    if S is None:
        register_fonts()
        S = _S()
    return S


class MacrovaDoc(BaseDocTemplate):
    """Two-pass document; records the page of every keyed flowable in ``refs``."""

    def __init__(self, filename, doc, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=A4, leftMargin=LM, rightMargin=RM,
                                 topMargin=TM, bottomMargin=BM,
                                 title="Macrova: A Web-Based Diet and Macronutrient "
                                       "Tracking Application",
                                 author="Karthick S", **kw)
        self.doc = doc
        self.refs = {}
        self.current_chapter = ""
        self.first_chapter_page = None
        self.last_front_page = 0
        frame_front = Frame(LM, BM, FRAME_W, FRAME_H, id="ff", showBoundary=0,
                            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        frame_body = Frame(LM, BM, FRAME_W, FRAME_H, id="fb", showBoundary=0,
                           leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="front", frames=[frame_front], onPage=self._start,
                         onPageEnd=self._front_furniture),
            PageTemplate(id="body", frames=[frame_body], onPage=self._start,
                         onPageEnd=self._body_furniture),
        ])

    # ------------------------------------------------------------ furniture
    def _start(self, canvas, doc):
        pass

    def _header(self, canvas, right_text):
        canvas.saveState()
        canvas.setFont("TNR", 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(LM, PDF_H - 52, "MACROVA \u2014 DIET & MACRONUTRITION TRACKING")
        canvas.drawRightString(PDF_W - RM, PDF_H - 52, right_text)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.6)
        canvas.line(LM, PDF_H - 58, PDF_W - RM, PDF_H - 58)
        canvas.restoreState()

    def _footer(self, canvas, text):
        canvas.saveState()
        canvas.setFont("TNR", 9)
        canvas.setFillColor(GREY)
        canvas.drawCentredString(PDF_W / 2, 42, text)
        canvas.restoreState()

    def _front_furniture(self, canvas, doc):
        page = canvas.getPageNumber()
        if page == 1:
            return
        self._header(canvas, "Preliminary Pages")
        self._footer(canvas, roman(page))

    def _body_furniture(self, canvas, doc):
        page = canvas.getPageNumber()
        self._header(canvas, self.current_chapter or "Chapter")
        self._footer(canvas, str(max(1, page - self.last_front_page)))

    # ---------------------------------------------------------------- hooks
    def afterFlowable(self, flowable):
        page = self.page
        key = getattr(flowable, "_key", None)
        if key and key not in self.refs:
            self.refs[key] = page
        hdr = getattr(flowable, "_hdr", None)
        if hdr:
            self.current_chapter = hdr
        chapter = getattr(flowable, "_chapter", None)
        if chapter:
            number, title = chapter
            self.current_chapter = f"Chapter {number}: {title.title()}"
        self.refs.setdefault("__hdr", {})[page] = self.current_chapter
        if getattr(flowable, "_first_chapter", False) and not self.first_chapter_page:
            self.first_chapter_page = page
