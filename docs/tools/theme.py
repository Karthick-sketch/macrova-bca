"""Layout engine, typographic theme and flowable helpers for the
Macrova BCA project report.

The module registers a Times-like serif family (DejaVu Serif), a humanist
sans family for headings, captions and tables (DejaVu Sans) and a monospaced
family for source listings (DejaVu Sans Mono).  It provides:

    * a two-pass aware ``ReportDoc`` document template that renders running
      headers, footers, roman/arabic page numbering and PDF bookmarks;
    * numbered figure / table / listing / algorithm helpers;
    * leader-dot table-of-contents renderers.
"""

from __future__ import annotations

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)

# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")

SERIF = "Serif"
SERIF_B = "Serif-Bold"
SERIF_I = "Serif-Italic"
SERIF_BI = "Serif-BoldItalic"
SANS = "Sans"
SANS_B = "Sans-Bold"
MONO = "Mono"

_FONT_FILES = {
    SERIF: "DejaVuSerif.ttf",
    SERIF_B: "DejaVuSerif-Bold.ttf",
    SERIF_I: "DejaVuSerif-Italic.ttf",
    SERIF_BI: "DejaVuSerif-BoldItalic.ttf",
    SANS: "DejaVuSans.ttf",
    SANS_B: "DejaVuSans-Bold.ttf",
    MONO: "DejaVuSansMono.ttf",
}

_fonts_ready = False


def register_fonts() -> None:
    global _fonts_ready
    if _fonts_ready:
        return
    for name, filename in _FONT_FILES.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, filename)))
    pdfmetrics.registerFontFamily(
        SERIF, normal=SERIF, bold=SERIF_B, italic=SERIF_I, boldItalic=SERIF_BI
    )
    pdfmetrics.registerFontFamily(
        SANS, normal=SANS, bold=SANS_B, italic=SERIF_I, boldItalic=SERIF_BI
    )
    _fonts_ready = True


# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------
INK = colors.HexColor("#1f2937")
INK_SOFT = colors.HexColor("#4b5563")
MUTED = colors.HexColor("#6b7280")
TEAL = colors.HexColor("#1a9c8a")
TEAL_DARK = colors.HexColor("#13786b")
TEAL_PALE = colors.HexColor("#e6f7f5")
TEAL_MID = colors.HexColor("#b2e4de")
RULE = colors.HexColor("#c9d6d3")
GRID = colors.HexColor("#9fb4b0")
TABLE_ALT = colors.HexColor("#f4f8f7")
CODE_BG = colors.HexColor("#f5f7f7")
NOTE_BG = colors.HexColor("#fbf7e8")
NOTE_BORDER = colors.HexColor("#d9c27a")
WARN = colors.HexColor("#b45309")

PAGE_W, PAGE_H = A4
LM, RM, TM, BM = 1.02 * inch, 0.92 * inch, 0.98 * inch, 0.92 * inch
CONTENT_W = PAGE_W - LM - RM

RUNNING_TITLE = "MACROVA  \u2014  INTELLIGENT DIET & MACRONUTRIENT PLANNING SYSTEM"
FOOTER_LEFT = "BCA Project Report  \u00b7  Department of Computer Applications, SRMIST (DDE)"

# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
S = {}


def build_styles() -> dict:
    register_fonts()
    S.clear()
    S["Body"] = ParagraphStyle(
        "Body", fontName=SERIF, fontSize=9.7, leading=14.2, alignment=TA_JUSTIFY,
        spaceAfter=5.4, textColor=INK, firstLineIndent=0,
    )
    S["BodyTight"] = ParagraphStyle("BodyTight", parent=S["Body"], spaceAfter=2)
    S["BodyCenter"] = ParagraphStyle(
        "BodyCenter", parent=S["Body"], alignment=TA_CENTER
    )
    S["Lead"] = ParagraphStyle(
        "Lead", parent=S["Body"], fontSize=10.2, leading=15.2, textColor=INK,
    )
    S["Bullet"] = ParagraphStyle(
        "Bullet", parent=S["Body"], leftIndent=13, bulletIndent=3,
        spaceAfter=3.6, bulletFontName=SERIF, bulletFontSize=9.7,
    )
    S["Numbered"] = ParagraphStyle(
        "Numbered", parent=S["Bullet"], leftIndent=18, bulletIndent=2,
    )
    S["Ref"] = ParagraphStyle(
        "Ref", parent=S["Body"], leftIndent=20, firstLineIndent=-20,
        spaceAfter=2.4, leading=12.6,
    )
    S["H1Label"] = ParagraphStyle(
        "H1Label", fontName=SANS_B, fontSize=9.4, leading=12, alignment=TA_LEFT,
        textColor=TEAL, spaceAfter=2.5,
    )
    S["H1"] = ParagraphStyle(
        "H1", fontName=SERIF_B, fontSize=16.5, leading=20.5, alignment=TA_LEFT,
        textColor=INK, spaceAfter=3,
    )
    S["H2"] = ParagraphStyle(
        "H2", fontName=SERIF_B, fontSize=11.6, leading=15, textColor=TEAL_DARK,
        spaceBefore=11, spaceAfter=4.2, keepWithNext=1,
    )
    S["H3"] = ParagraphStyle(
        "H3", fontName=SANS_B, fontSize=9.9, leading=13, textColor=INK,
        spaceBefore=8, spaceAfter=3, keepWithNext=1,
    )
    S["Caption"] = ParagraphStyle(
        "Caption", fontName=SANS, fontSize=8.1, leading=10.6, alignment=TA_CENTER,
        textColor=INK_SOFT, spaceBefore=3.2, spaceAfter=9,
    )
    S["CaptionLeft"] = ParagraphStyle(
        "CaptionLeft", parent=S["Caption"], alignment=TA_LEFT,
    )
    S["TableHead"] = ParagraphStyle(
        "TableHead", fontName=SANS_B, fontSize=7.9, leading=9.8,
        textColor=colors.white,
    )
    S["TableCell"] = ParagraphStyle(
        "TableCell", fontName=SANS, fontSize=7.7, leading=9.7, textColor=INK,
    )
    S["TableCellMono"] = ParagraphStyle(
        "TableCellMono", fontName=MONO, fontSize=7.1, leading=9.4, textColor=INK,
    )
    S["TableCaption"] = ParagraphStyle(
        "TableCaption", fontName=SANS_B, fontSize=8.2, leading=10.8,
        textColor=TEAL_DARK, spaceBefore=7, spaceAfter=3.5, keepWithNext=1,
    )
    S["Code"] = ParagraphStyle(
        "Code", fontName=MONO, fontSize=6.9, leading=9.0, textColor=colors.HexColor("#1b2b34"),
        alignment=TA_LEFT,
    )
    S["ListingCaption"] = ParagraphStyle(
        "ListingCaption", fontName=SANS_B, fontSize=7.9, leading=10.4,
        textColor=TEAL_DARK, spaceBefore=6, spaceAfter=3, keepWithNext=1,
    )
    S["Note"] = ParagraphStyle(
        "Note", fontName=SERIF, fontSize=8.8, leading=12.6, textColor=INK,
        alignment=TA_JUSTIFY,
    )
    S["Small"] = ParagraphStyle(
        "Small", fontName=SANS, fontSize=7.6, leading=10.4, textColor=MUTED,
    )
    S["TOC0"] = ParagraphStyle(
        "TOC0", fontName=SANS_B, fontSize=8.9, leading=12.4, textColor=INK,
    )
    S["TOC1"] = ParagraphStyle(
        "TOC1", fontName=SANS, fontSize=8.3, leading=11.6, textColor=INK_SOFT,
        leftIndent=15,
    )
    S["TOC2"] = ParagraphStyle(
        "TOC2", fontName=SANS, fontSize=7.8, leading=11.0, textColor=MUTED,
        leftIndent=30,
    )
    S["CoverTitle"] = ParagraphStyle(
        "CoverTitle", fontName=SERIF_B, fontSize=20, leading=26, alignment=TA_CENTER,
        textColor=INK,
    )
    S["CoverSub"] = ParagraphStyle(
        "CoverSub", fontName=SANS_B, fontSize=10.6, leading=15, alignment=TA_CENTER,
        textColor=TEAL_DARK,
    )
    S["CoverMeta"] = ParagraphStyle(
        "CoverMeta", fontName=SERIF, fontSize=10.2, leading=14.4, alignment=TA_CENTER,
        textColor=INK,
    )
    S["CoverSmall"] = ParagraphStyle(
        "CoverSmall", fontName=SANS, fontSize=8.9, leading=12.4, alignment=TA_CENTER,
        textColor=INK_SOFT,
    )
    S["PrelimH"] = ParagraphStyle(
        "PrelimH", fontName=SANS_B, fontSize=12.4, leading=16, alignment=TA_CENTER,
        textColor=INK, spaceAfter=14,
    )
    return S


# --------------------------------------------------------------------------
# Document context (chapter / numbering counters)
# --------------------------------------------------------------------------
class Ctx:
    def __init__(self):
        self.reset()

    def reset(self):
        self.chapter = 0
        self.fig = 0
        self.tab = 0
        self.lst = 0
        self.algo = 0
        self.figure_book = []   # (label, caption)
        self.table_book = []    # (label, caption)
        self.listing_book = []
        self.headings = []      # (level, text, page_label)

    def start_chapter(self, n: int):
        self.chapter = n
        self.fig = 0
        self.tab = 0
        self.lst = 0
        self.algo = 0

    def next_fig(self):
        self.fig += 1
        return f"Figure {self.chapter}.{self.fig}"

    def next_tab(self):
        self.tab += 1
        return f"Table {self.chapter}.{self.tab}"

    def next_lst(self):
        self.lst += 1
        return f"Listing {self.chapter}.{self.lst}"

    def next_algo(self):
        self.algo += 1
        return f"Algorithm {self.chapter}.{self.algo}"


CTX = Ctx()


def roman(n: int) -> str:
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"),
            (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"),
            (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, sym in vals:
        while n >= v:
            out += sym
            n -= v
    return out


def page_label(doc, abs_page: int) -> str:
    if getattr(doc, "body_start", None):
        return str(abs_page - doc.body_start + 1)
    return roman(abs_page)


# --------------------------------------------------------------------------
# Custom flowables
# --------------------------------------------------------------------------
class HRule(Flowable):
    def __init__(self, width=CONTENT_W, thickness=1.1, color=TEAL, space=6):
        Flowable.__init__(self)
        self.width_ = width
        self.thickness = thickness
        self.color = color
        self.space = space

    def wrap(self, aw, ah):
        return (self.width_, self.thickness + self.space)

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.thickness)
        c.setLineCap(0)
        c.line(0, 0, self.width_, 0)


class H(Paragraph):
    """Paragraph that is registered in the table of contents."""

    def __init__(self, text, style, level=1, toc_text=None, chapter=False,
                 chapter_label=None):
        Paragraph.__init__(self, text, style)
        self.toc_level = level
        self.toc_text = toc_text if toc_text is not None else text
        self.chapter = chapter
        self.chapter_label = chapter_label


class Cap(Paragraph):
    """Caption paragraph that is registered in the list of figures/tables."""

    def __init__(self, text, style, label, kind):
        Paragraph.__init__(self, text, style)
        self.label = label
        self.kind = kind


class TOCLine(Flowable):
    """Leader-dot contents line."""

    def __init__(self, text, page, level=0, width=CONTENT_W, styles=None):
        Flowable.__init__(self)
        self.text = text
        self.page = str(page)
        self.level = level
        self.w = width
        self.st = styles
        self.h = 13.4 if level == 0 else 12.2

    def wrap(self, aw, ah):
        self.w = min(self.w, aw)
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        st = self.st["TOC0"] if self.level == 0 else (
            self.st["TOC1"] if self.level == 1 else self.st["TOC2"])
        indent = st.leftIndent
        size = st.fontSize
        font = st.fontName
        c.setFont(font, size)
        c.setFillColor(st.textColor)
        page_w = pdfmetrics.stringWidth(self.page, font, size)
        max_text = self.w - indent - page_w - 10
        txt = self.text
        while pdfmetrics.stringWidth(txt, font, size) > max_text and len(txt) > 4:
            txt = txt[:-2]
        if txt != self.text:
            txt = txt[:-1] + "\u2026"
        c.drawString(indent, 3.2, txt)
        c.drawRightString(self.w, 3.2, self.page)
        used = indent + pdfmetrics.stringWidth(txt, font, size)
        # dots must stop before the page-number column: measure the ". " unit
        unit = pdfmetrics.stringWidth(". ", font, size)
        avail = self.w - page_w - 8 - (used + 5)
        n = int(avail / unit) if unit > 0 else 0
        if n > 2:
            dots = (". " * n).rstrip()
            c.setFillColor(MUTED)
            c.setFont(font, size)
            c.drawString(used + 5, 3.2, dots)


# --------------------------------------------------------------------------
# Document template
# --------------------------------------------------------------------------
class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(
            self, filename, pagesize=A4, leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=BM,
            title="Macrova: An Intelligent Diet, Macro-Tracking and AI Food "
                  "Recommendation System",
            author="Project Report \u2014 Bachelor of Computer Applications",
            subject="BCA Project Report",
            **kw,
        )
        frame = Frame(LM, BM, CONTENT_W, PAGE_H - TM - BM, id="main",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="main", frames=[frame])])
        self.body_start = None
        self.headings = []
        self.figures = []
        self.tables = []
        self.current_chapter = ""
        self.current_chapter_label = ""
        self.bookmarks = 0

    # -- running header / footer ------------------------------------------
    def afterPage(self):
        c = self.canv
        p = self.page
        if p == 1:          # cover page is intentionally unnumbered
            return
        label = page_label(self, p)
        c.saveState()
        # header
        c.setFont(SANS, 6.9)
        c.setFillColor(MUTED)
        c.drawString(LM, PAGE_H - TM + 17, RUNNING_TITLE)
        c.drawRightString(PAGE_W - RM, PAGE_H - TM + 17, self.current_chapter)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(LM, PAGE_H - TM + 11, PAGE_W - RM, PAGE_H - TM + 11)
        # footer
        c.setStrokeColor(RULE)
        c.line(LM, BM - 16, PAGE_W - RM, BM - 16)
        c.setFont(SANS, 7.2)
        c.setFillColor(MUTED)
        c.drawString(LM, BM - 27, FOOTER_LEFT)
        c.setFont(SANS_B, 7.8)
        c.setFillColor(INK_SOFT)
        c.drawRightString(PAGE_W - RM, BM - 27, f"Page {label}")
        c.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Cap):
            entry = (flowable.label, flowable.plain, page_label(self, self.page))
            if flowable.kind == "fig":
                self.figures.append(entry)
            elif flowable.kind == "tab":
                self.tables.append(entry)
            return
        if isinstance(flowable, TOCLine) or isinstance(flowable, HRule):
            return
        if isinstance(flowable, H):
            label = page_label(self, self.page)
            if flowable.chapter:
                self.body_start = self.body_start or self.page
                self.current_chapter = flowable.chapter_label or flowable.toc_text
                self.current_chapter_label = flowable.chapter_label or ""
                label = page_label(self, self.page)
            elif flowable.toc_level == 0:
                # back matter: references and appendices get their own running head
                txt = flowable.toc_text
                self.current_chapter = (
                    " ".join(txt.split()[:2]) if txt.upper().startswith("APPENDIX") else txt
                )[:46]
            self.headings.append((flowable.toc_level, flowable.toc_text, label))
            key = f"bm{len(self.headings)}"
            self.canv.bookmarkPage(key)
            try:
                self.canv.addOutlineEntry(
                    flowable.toc_text.replace("&amp;", "&")[:110], key,
                    min(flowable.toc_level, 2), 0)
            except Exception:
                pass


# --------------------------------------------------------------------------
# Content helpers
# --------------------------------------------------------------------------
def body(text, style="Body"):
    return Paragraph(text, S[style])


def para(text, style="Body"):
    return [Paragraph(text, S[style])]


def bullets(items, style="Bullet", marker="\u2022"):
    out = []
    for it in items:
        out.append(Paragraph(it, S[style], bulletText=marker))
    return out


def numbered(items, start=1):
    out = []
    for i, it in enumerate(items, start):
        out.append(Paragraph(it, S["Numbered"], bulletText=f"{i}."))
    return out


def chapter(n, title, label=None):
    """Start a new chapter: returns flowables."""
    CTX.start_chapter(n)
    lab = label if label is not None else f"CHAPTER {n}"
    out = [PageBreak()]
    out.append(Spacer(1, 10))
    out.append(Paragraph(lab, S["H1Label"]))
    out.append(H(_esc(title), S["H1"], level=0, toc_text=f"Chapter {n}: {title}",
                   chapter=True,
                   chapter_label=f"Chapter {n}: {title.split(':')[0].strip()}"))
    out.append(Spacer(1, 2))
    out.append(HRule(width=CONTENT_W, thickness=1.4, color=TEAL, space=10))
    out.append(Spacer(1, 6))
    return out


def prelim(title, toc=False, level=0):
    out = [PageBreak(), Spacer(1, 6)]
    if toc:
        out.append(H(_esc(title), S["PrelimH"], level=level, toc_text=title))
    else:
        out.append(Paragraph(_esc(title), S["PrelimH"]))
    out.append(HRule(width=CONTENT_W * 0.32, thickness=0.9, color=TEAL, space=12))
    out.append(Spacer(1, 8))
    return out


def h2(text, toc=True):
    return H(_esc(text), S["H2"], level=1 if toc else 9, toc_text=text)


def h3(text, toc=False):
    return H(_esc(text), S["H3"], level=2 if toc else 9, toc_text=text)


def _esc(t: str) -> str:
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fit(drawing, max_w=CONTENT_W * 0.98):
    """Scale a reportlab Drawing (or svg2rlg object) to fit max_w."""
    w = float(drawing.width)
    h = float(drawing.height)
    if w > max_w:
        s = max_w / w
        drawing.scale(s, s)
        drawing.width = w * s
        drawing.height = h * s
    return drawing


def figure(drawing, caption, max_w=CONTENT_W * 0.98, spacing=8):
    """Numbered figure with centred caption."""
    lab = CTX.next_fig()
    d = fit(drawing, max_w)
    cap = Cap(f"<b>{lab}:</b> {_esc(caption)}", S["Caption"], lab, "fig")
    cap.plain = caption
    return [Spacer(1, spacing), d, cap]


def figure_plain(drawing, caption, max_w=CONTENT_W * 0.98):
    d = fit(drawing, max_w)
    return [Spacer(1, 7), d, Paragraph(_esc(caption), S["Caption"])]


def table_caption(text, label=None):
    lab = label or CTX.next_tab()
    cap = Cap(f"<b>{lab}:</b> {text}", S["TableCaption"], lab, "tab")
    cap.plain = text
    return cap


def table(headers, rows, widths=None, caption=None, font_size=None,
          zebra=True, align=None, repeat=True, col_style=None, keep=1,
          max_rows_note=None, header_bg=TEAL_DARK):
    """Build a styled data table (Platypus Table) with an optional caption."""
    cap = None
    if caption:
        cap = table_caption(caption)
    head_style = S["TableHead"]
    cell_style = S["TableCell"]
    if font_size:
        head_style = ParagraphStyle("th2", parent=head_style,
                                    fontSize=font_size, leading=font_size * 1.25)
        cell_style = ParagraphStyle("tc2", parent=cell_style,
                                    fontSize=font_size, leading=font_size * 1.28)
    data = [[Paragraph(str(h), head_style) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(cell), cell_style) for cell in r])
    ncol = len(headers)
    if widths is None:
        widths = [CONTENT_W / ncol] * ncol
    else:
        tot = sum(widths)
        widths = [w / tot * CONTENT_W for w in widths]
    t = Table(data, colWidths=widths, repeatRows=1 if repeat else 0,
              hAlign="LEFT", splitByRow=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.6),
        ("TOPPADDING", (0, 0), (-1, -1), 2.9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.1),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT))
    if align:
        for col, a in enumerate(align):
            if a == "C":
                cmds.append(("ALIGN", (col, 1), (col, -1), "CENTER"))
            elif a == "R":
                cmds.append(("ALIGN", (col, 1), (col, -1), "RIGHT"))
    if col_style:
        cmds.extend(col_style)
    t.setStyle(TableStyle(cmds))
    out = []
    if cap is not None:
        out.append(cap)
    out.append(t)
    out.append(Spacer(1, 9))
    return out


def code_block(text, caption="Source code excerpt", width=CONTENT_W,
               keep_together=False, label=None):
    lab = label or CTX.next_lst()
    txt = text.rstrip("\n").replace("\t", "    ")
    rows = []
    for line in txt.split("\n"):
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rows.append([XPreformatted(line if line.strip() else " ", S["Code"])])
    inner = Table(rows, colWidths=[width - 10], hAlign="LEFT")
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    outer = Table([[inner]], colWidths=[width], hAlign="LEFT")
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    cap = Paragraph(f"<b>{lab}:</b> {_esc(caption)}", S["ListingCaption"])
    story = [cap]
    if keep_together:
        story.append(KeepTogether([outer]))
    else:
        story.append(outer)
    story.append(Spacer(1, 8))
    return story


def note_box(text, title="Note"):
    inner = Paragraph(f"<b>{title}.</b> {text}", S["Note"])
    t = Table([[inner]], colWidths=[CONTENT_W], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NOTE_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, NOTE_BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, colors.HexColor("#c8a13a")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 9)]


def toc_lines(entries, styles=None):
    st = styles or S
    out = []
    for level, text, page in entries:
        out.append(TOCLine(text, page, level=level, styles=st))
    return out
