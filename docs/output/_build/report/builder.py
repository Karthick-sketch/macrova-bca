"""Turn the Doc model into ReportLab flowables and run the two-pass build."""

import os
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (Image, KeepTogether, NextPageTemplate, PageBreak, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)

from doc import Doc, Block
from pdfkit import (DOT, FRAME_W, HEAD_BG, S, esc, register_fonts, rich, styles)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "assets")


def keyed(style, key, text):
    par = Paragraph(rich(text), style)
    par._key = key
    return par


def toc_line(label, page, style, width=FRAME_W):
    """TOC row: label, dotted leader rule drawn under it, page number at the right."""
    font, size = style.fontName, style.fontSize
    page_txt = str(page)
    page_w = stringWidth(page_txt, font, size) + 8
    left_w = width - page_w
    max_label = left_w - 10
    if stringWidth(label, font, size) > max_label:
        while label and stringWidth(label + "\u2026", font, size) > max_label:
            label = label[:-1]
        label = label.rstrip(" ,;:") + "\u2026"
    left_st = ParagraphStyle("tl", parent=style, leftIndent=0, firstLineIndent=0,
                             rightIndent=0, spaceBefore=0, spaceAfter=0)
    right_st = ParagraphStyle("tp", parent=left_st, alignment=TA_RIGHT)
    row = Table([[Paragraph(esc(label), left_st), Paragraph(page_txt, right_st)]],
                colWidths=[left_w, page_w])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2),
        ("LINEBELOW", (0, 0), (0, 0), 0.6, DOT, 0, (1, 2.6)),
    ]))
    return row


class BodyBuilder:
    def __init__(self, doc: Doc):
        self.doc = doc
        self.s = styles()

    # ------------------------------------------------------------- pieces
    def _figure(self, block: Block):
        num = block.meta["label"]
        path = block.path if os.path.isabs(block.path) else os.path.join(ASSETS, block.path)
        from PIL import Image as PILImage
        w, h = PILImage.open(path).size
        width = min(block.width, FRAME_W / inch - 0.06) * inch
        img = Image(path, width=width, height=width * h / w)
        img.hAlign = "CENTER"
        cap = Paragraph(f"Figure {num}: {esc(block.caption)}", self.s.figcap)
        cap._key = f"fig{num}"
        return [Spacer(1, 4), KeepTogether([img, cap])]

    def _table(self, block: Block):
        num = block.meta["label"]
        size = block.meta.get("font") or 8.6
        cell_st, head_st = self.s.cell_styles(size)
        header = [Paragraph(esc(h), head_st) for h in block.header]
        rows = [[Paragraph(esc(c), cell_st) for c in r] for r in block.rows]
        widths = block.meta.get("widths")
        if widths:
            total = float(sum(widths))
            widths = [FRAME_W * w / total for w in widths]
        t = Table([header] + rows, colWidths=widths, repeatRows=1, hAlign="CENTER")
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b9c9cd")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
        for i in range(2, len(rows) + 1, 2):
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f6faf9")))
        t.setStyle(TableStyle(style))
        cap = Paragraph(f"Table {num}: {esc(block.caption)}", self.s.tabcap)
        cap._key = f"tab{num}"
        return [Spacer(1, 6), cap, t, Spacer(1, 10)]

    def _code(self, block: Block):
        lines = []
        for raw in block.text.rstrip("\n").split("\n"):
            lines.extend(textwrap.wrap(raw, 96, drop_whitespace=False,
                                       subsequent_indent="    ") or [""])
        text = "\n".join(esc(l) for l in lines)
        box = Table([[Preformatted(text, self.s.code)]], colWidths=[FRAME_W])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f7f7")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cdd9dc")),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        cap = Paragraph(esc(block.caption), self.s.codecap)
        cap.keepWithNext = True
        return [Spacer(1, 2), KeepTogether([cap, box]), Spacer(1, 10)]

    # --------------------------------------------------------------- story
    def build_story(self):
        s = self.s
        story = []
        first_chapter = True
        for block in self.doc.blocks:
            k = block.kind
            if k == "chapter":
                story.append(NextPageTemplate("body"))
                story.append(PageBreak())
                story.append(Spacer(1, 12))
                p1 = Paragraph(f"CHAPTER {block.meta['number']}", s.chapter_no)
                p2 = Paragraph(esc(block.text.upper()), s.chapter_title)
                p2._key = block.key
                p2._chapter = (block.meta["number"], block.text.upper())
                if first_chapter:
                    p2._first_chapter = True
                    first_chapter = False
                story.append(KeepTogether([p1, p2]))
                story.append(Spacer(1, 4))
            elif k == "part":
                story.append(PageBreak())
                story.append(Spacer(1, 12))
                par = keyed(s.part_title, block.key, block.text.upper())
                par._hdr = block.text.upper()
                story.append(par)
            elif k == "h2":
                par = keyed(s.h2, block.key, block.text)
                if block.text.startswith("Appendix "):
                    par._hdr = block.text.split("  ")[0] + " \u2014 " + block.text.split("  ")[1]
                story.append(par)
            elif k == "h3":
                story.append(keyed(s.h3, block.key, block.text))
            elif k == "p":
                if block.text:
                    story.append(Paragraph(rich(block.text), s.body))
            elif k == "bullets":
                for item in block.items:
                    st = s.bullet_left if "http" in item else s.bullet
                    story.append(Paragraph(rich(item), st, bulletText="\u2022"))
                story.append(Spacer(1, 4))
            elif k == "numbered":
                for i, item in enumerate(block.items, 1):
                    story.append(Paragraph(rich(item), s.bullet, bulletText=f"{i}."))
                story.append(Spacer(1, 4))
            elif k == "note":
                story.append(Paragraph(rich(block.text), s.note))
            elif k == "code":
                story.extend(self._code(block))
            elif k == "table":
                story.extend(self._table(block))
            elif k == "figure":
                story.extend(self._figure(block))
            elif k == "spacer":
                story.append(Spacer(1, block.meta.get("h", 10)))
            elif k == "pagebreak":
                story.append(PageBreak())
            else:
                raise ValueError(f"unknown block {k}")
        return story


def build(doc: Doc, out_path: str, front_builder):
    """Iterate the two-pass build until the page numbers stop moving, then write the file.

    The table of contents grows by a page once it carries real page numbers, which shifts every
    subsequent page by one; iterating to a fixed point removes that off-by-one.
    """
    register_fonts()
    from pdfkit import MacrovaDoc

    tmp = out_path.replace(".pdf", "-pass.pdf")
    refs = None
    history = []
    for _ in range(5):
        front_pages = (refs["__first"] - 1) if refs else 0
        data = (refs, front_pages) if refs else None
        story = front_builder("pass", data) + BodyBuilder(doc).build_story()
        d = MacrovaDoc(tmp, doc)
        d.last_front_page = front_pages
        d.build(story)
        new_refs = dict(d.refs)
        new_refs["__first"] = d.first_chapter_page or 1
        new_refs["__pages"] = d.page
        stable = refs is not None and all(
            refs.get(k) == v for k, v in new_refs.items() if not k.startswith("__"))
        history.append((d.page, new_refs["__first"]))
        refs = new_refs
        if stable:
            break

    front_pages = refs["__first"] - 1
    story = front_builder("final", (refs, front_pages)) + BodyBuilder(doc).build_story()
    out = MacrovaDoc(out_path, doc)
    out.last_front_page = front_pages
    out.build(story)
    out.history = history
    try:
        os.remove(tmp)
    except OSError:
        pass
    return out
