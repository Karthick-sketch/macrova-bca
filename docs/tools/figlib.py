"""Small vector-diagram toolkit used to draw the figures of the report.

All coordinates are given in *top-left* space (x grows right, ``top`` grows
down) to keep the diagram definitions readable; the class converts to the
bottom-left origin used by reportlab automatically.
"""

from __future__ import annotations

import math

from reportlab.graphics.shapes import (
    Circle,
    Drawing,
    Ellipse,
    Group,
    Line,
    Path,
    Polygon,
    Rect,
    String,
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics

from theme import INK, INK_SOFT, MUTED, SANS, SANS_B, SERIF, SERIF_B, TEAL, TEAL_DARK, TEAL_MID, TEAL_PALE

WHITE = colors.white
BLUE_PALE = colors.HexColor("#e8f0fa")
BLUE = colors.HexColor("#3d6fb4")
AMBER_PALE = colors.HexColor("#fdf3dc")
AMBER = colors.HexColor("#b5820a")
GREEN_PALE = colors.HexColor("#e9f6ee")
GREEN = colors.HexColor("#2f8f5b")
ROSE_PALE = colors.HexColor("#fdeaea")
ROSE = colors.HexColor("#b3403c")
GREY_PALE = colors.HexColor("#f2f4f4")
GREY = colors.HexColor("#7b8a88")


def sw(text, font, size):
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text, font, size, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if sw(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class D:
    """Drawing facade with top-left coordinates and diagram primitives."""

    def __init__(self, w, h):
        self.w = float(w)
        self.h = float(h)
        self.d = Drawing(w, h)
        self.d.hAlign = "CENTER"

    # -- coordinate helpers -------------------------------------------------
    def y(self, top):
        return self.h - top

    def _add(self, shape):
        self.d.add(shape)
        return shape

    # -- primitives ---------------------------------------------------------
    def rrect(self, x, top, w, h, r=6, fill=WHITE, stroke=TEAL, lw=1.0, dash=None):
        y = self.y(top + h)
        p = Path(strokeColor=stroke, fillColor=fill, strokeWidth=lw, strokeDashArray=dash)
        r = min(r, w / 2, h / 2)
        p.moveTo(x + r, y)
        p.lineTo(x + w - r, y)
        p.curveTo(x + w - r * 0.45, y, x + w, y + r * 0.45, x + w, y + r)
        p.lineTo(x + w, y + h - r)
        p.curveTo(x + w, y + h - r * 0.45, x + w - r * 0.45, y + h, x + w - r, y + h)
        p.lineTo(x + r, y + h)
        p.curveTo(x + r * 0.45, y + h, x, y + h - r * 0.45, x, y + h - r)
        p.lineTo(x, y + r)
        p.curveTo(x, y + r * 0.45, x + r * 0.45, y, x + r, y)
        p.closePath()
        return self._add(p)

    def rect(self, x, top, w, h, fill=WHITE, stroke=colors.HexColor("#c9d6d3"), lw=0.8, dash=None):
        y = self.y(top + h)
        return self._add(Rect(x, y, w, h, fillColor=fill, strokeColor=stroke,
                              strokeWidth=lw, strokeDashArray=dash))

    def line(self, x1, t1, x2, t2, color=INK_SOFT, lw=0.9, dash=None):
        return self._add(Line(x1, self.y(t1), x2, self.y(t2), strokeColor=color,
                              strokeWidth=lw, strokeDashArray=dash))

    def text(self, x, top, s, size=8, font=SANS, color=INK, anchor="start"):
        return self._add(String(x, self.y(top), s, fontName=font, fontSize=size,
                                fillColor=color, textAnchor=anchor))

    def para(self, x, top, w, s, size=7.6, font=SANS, color=INK_SOFT, leading=None,
             align="center"):
        leading = leading or size * 1.28
        lines = wrap(s, font, size, w)
        for i, ln in enumerate(lines):
            if align == "center":
                self.text(x + w / 2, top + size * 0.86 + i * leading, ln, size, font, color, "middle")
            elif align == "right":
                self.text(x + w, top + size * 0.86 + i * leading, ln, size, font, color, "end")
            else:
                self.text(x, top + size * 0.86 + i * leading, ln, size, font, color, "start")
        return len(lines) * leading

    def box(self, x, top, w, h, title, sub=None, fill=WHITE, stroke=TEAL,
            lw=1.0, radius=5, tsize=8.2, ssize=6.8, tfont=SANS_B, sfont=SANS,
            tcolor=INK, scolor=INK_SOFT, dash=None, align="center"):
        self.rrect(x, top, w, h, r=radius, fill=fill, stroke=stroke, lw=lw, dash=dash)
        tl = wrap(title, tfont, tsize, w - 10)
        sl = wrap(sub, sfont, ssize, w - 10) if sub else []
        block = len(tl) * tsize * 1.3 + (len(sl) * ssize * 1.3 + 2 if sl else 0)
        ty = top + (h - block) / 2 + tsize * 0.86
        for i, ln in enumerate(tl):
            if align == "center":
                self.text(x + w / 2, ty + i * tsize * 1.3, ln, tsize, tfont, tcolor, "middle")
            else:
                self.text(x + 6, ty + i * tsize * 1.3, ln, tsize, tfont, tcolor, "start")
        sy = ty + len(tl) * tsize * 1.3 + 1
        for i, ln in enumerate(sl):
            if align == "center":
                self.text(x + w / 2, sy + i * ssize * 1.3, ln, ssize, sfont, scolor, "middle")
            else:
                self.text(x + 6, sy + i * ssize * 1.3, ln, ssize, sfont, scolor, "start")

    def oval(self, x, top, w, h, title, sub=None, fill=TEAL_PALE, stroke=TEAL,
             tsize=7.4, ssize=6.4):
        y = self.y(top + h)
        self._add(Ellipse(x + w / 2, y + h / 2, w / 2, h / 2, fillColor=fill,
                          strokeColor=stroke, strokeWidth=0.9))
        lines = wrap(title, SANS, tsize, w * 0.78)
        sl = wrap(sub, SANS, ssize, w * 0.78) if sub else []
        block = len(lines) * tsize * 1.25 + (len(sl) * ssize * 1.25 if sl else 0)
        ty = top + (h - block) / 2 + tsize * 0.85
        for i, ln in enumerate(lines):
            self.text(x + w / 2, ty + i * tsize * 1.25, ln, tsize, SANS, INK, "middle")
        for i, ln in enumerate(sl):
            self.text(x + w / 2, ty + len(lines) * tsize * 1.25 + i * ssize * 1.25,
                      ln, ssize, SANS, MUTED, "middle")

    def arrow(self, x1, t1, x2, t2, color=TEAL_DARK, lw=1.0, head=6.5, dash=None,
              both=False):
        ang = math.atan2(-(t2 - t1), x2 - x1)
        self.line(x1, t1, x2, t2, color, lw, dash)
        self._head(x2, t2, ang, head, color)
        if both:
            self._head(x1, t1, ang + math.pi, head, color)

    def _head(self, x, top, ang, size, color):
        y = self.y(top)
        a1 = ang + math.radians(24)
        a2 = ang - math.radians(24)
        pts = [x, y,
               x - size * math.cos(a1), y + size * math.sin(a1),
               x - size * math.cos(a2), y + size * math.sin(a2)]
        self._add(Polygon(pts, fillColor=color, strokeColor=color, strokeWidth=0.5))

    def poly(self, pts, color=TEAL_DARK, lw=1.0, dash=None, head=True, head_size=6.5):
        """Orthogonal connector: pts = [(x, top), ...]"""
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, lw, dash)
        if head:
            (x1, t1), (x2, t2) = pts[-2], pts[-1]
            ang = math.atan2(-(t2 - t1), x2 - x1)
            self._head(x2, t2, ang, head_size, color)

    def datastore(self, x, top, w, h, title, fill=WHITE, stroke=TEAL_DARK):
        """DFD data store (open-ended rectangle)."""
        y = self.y(top + h)
        self._add(Rect(x, y, w, h, fillColor=fill, strokeColor=stroke, strokeWidth=0.9))
        self.line(x + 7, top, x + 7, top + h, stroke, 0.9)
        self.text(x + 12, top + h / 2 + 2.8, title, 7.0, SANS_B, INK)

    def actor(self, x, top, label, color=TEAL_DARK):
        """Stick-figure actor centred at (x, top)."""
        head_r = 3.4
        self._add(Circle(x, self.y(top + head_r), head_r, fillColor=WHITE,
                         strokeColor=color, strokeWidth=1.0))
        self.line(x, top + 2 * head_r, x, top + 15, color, 1.0)
        self.line(x - 6, top + 8, x + 6, top + 8, color, 1.0)
        self.line(x, top + 15, x - 5, top + 22, color, 1.0)
        self.line(x, top + 15, x + 5, top + 22, color, 1.0)
        self.text(x, top + 33, label, 7.0, SANS_B, INK, "middle")

    def cylinder(self, x, top, w, h, title, sub=None, fill=BLUE_PALE, stroke=BLUE, tsize=7.6, ssize=6.4):
        """Database cylinder."""
        y = self.y(top + h)
        ry = min(7.0, h / 5)
        body = Path(strokeColor=stroke, fillColor=fill, strokeWidth=0.9)
        body.moveTo(x, y + h - ry)
        body.curveTo(x, y + h + ry * 0.2, x + w, y + h + ry * 0.2, x + w, y + h - ry)
        body.lineTo(x + w, y + ry)
        body.curveTo(x + w, y - ry * 0.2, x, y - ry * 0.2, x, y + ry)
        body.closePath()
        self._add(body)
        self._add(Ellipse(x + w / 2, y + h - ry, w / 2, ry, fillColor=fill,
                          strokeColor=stroke, strokeWidth=0.9))
        self.text(x + w / 2, top + h / 2 + 3.5, title, tsize, SANS_B, INK, "middle")
        if sub:
            self.text(x + w / 2, top + h / 2 + 3.5 + tsize + 1.6, sub, ssize, SANS, MUTED, "middle")

    def band(self, x, top, w, h, label, fill, stroke=None, size=7.2, font=SANS_B,
             color=None, vertical=True, dash=None):
        self.rect(x, top, w, h, fill=fill, stroke=stroke or colors.HexColor("#d5dedd"), dash=dash)
        if vertical:
            st = String(0, 0, label, fontName=font, fontSize=size,
                        fillColor=color or INK_SOFT, textAnchor="middle")
            grp = Group([st], transform=(0, 1, -1, 0, x + 9, self.y(top + h / 2)))
            self._add(grp)
        else:
            self.text(x + w / 2, top + h / 2 + size * 0.4, label, size, font,
                      color or INK_SOFT, "middle")

    def badge(self, x, top, text, fill=TEAL_PALE, stroke=TEAL_MID, color=TEAL_DARK,
              size=6.4, pad=5, h=12):
        w = sw(text, SANS_B, size) + pad * 2
        self.rrect(x, top, w, h, r=h / 2, fill=fill, stroke=stroke, lw=0.7)
        self.text(x + w / 2, top + h / 2 + size * 0.36, text, size, SANS_B, color, "middle")
        return w

    def legend(self, x, top, items, size=6.8, gap=14):
        """items = [(label, fill, stroke)]"""
        cx = x
        for label, fill, stroke in items:
            self.rect(cx, top, 9, 9, fill=fill, stroke=stroke, lw=0.8)
            self.text(cx + 12, top + 7, label, size, SANS, INK_SOFT)
            cx += 12 + sw(label, SANS, size) + gap
        return cx - x

    def frame(self, x, top, w, h, label=None, fill=None, stroke=colors.HexColor("#b9c9c6"),
              dash=(2, 2), size=6.8):
        self.rect(x, top, w, h, fill=fill or colors.white, stroke=stroke, lw=0.8, dash=dash)
        if label:
            tw = sw(label, SANS_B, size) + 10
            self.rect(x + 8, top - 6, tw, 12, fill=colors.white, stroke=stroke, lw=0.6, dash=dash)
            self.text(x + 13, top + 2.4, label, size, SANS_B, MUTED)

    def outcome(self):
        return self.d
