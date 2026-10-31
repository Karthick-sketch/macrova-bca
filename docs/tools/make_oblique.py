"""Generate oblique (synthetic italic) variants of the DejaVu Serif family.

The build environment used for this report does not ship an italic cut of
DejaVu Serif.  Rather than mixing font families inside running text, this
utility derives an oblique variant directly from the regular and bold faces by
shearing the glyph outlines, and gives each derived face a unique PostScript
name so that ReportLab registers it as a distinct font resource.

Usage:
    python3 make_oblique.py

Outputs (written next to the source fonts in assets/fonts):
    DejaVuSerif-Italic.ttf
    DejaVuSerif-BoldItalic.ttf
"""

from __future__ import annotations

import math
import os

from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "assets", "fonts")


def oblique(src: str, dst: str, family: str, ps_name: str, angle: float = 12.0) -> None:
    font = TTFont(src)
    glyf = font["glyf"]
    glyph_set = font.getGlyphSet()
    shear = math.tan(math.radians(angle))

    for name in font.getGlyphOrder():
        glyph = glyf[name]
        if glyph.numberOfContours == 0:
            continue
        pen = TTGlyphPen(glyph_set)
        glyph.draw(TransformPen(pen, (1, 0, shear, 1, 0, 0)), glyf)
        new_glyph = pen.glyph()
        new_glyph.recalcBounds(glyf)
        glyf[name] = new_glyph

    font["hhea"].italicAngle = -angle
    font["post"].italicAngle = -angle
    names = {1: family, 2: "Italic", 3: f"{ps_name};oblique", 4: family,
             6: ps_name, 16: family, 17: "Italic"}
    for record in font["name"].names:
        if record.nameID in names:
            record.string = names[record.nameID]
    font.save(dst)
    print(f"wrote {dst}")


if __name__ == "__main__":
    oblique(
        os.path.join(FONT_DIR, "DejaVuSerif.ttf"),
        os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf"),
        family="DejaVu Serif Oblique",
        ps_name="DejaVuSerifOblique",
    )
    oblique(
        os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"),
        os.path.join(FONT_DIR, "DejaVuSerif-BoldItalic.ttf"),
        family="DejaVu Serif Oblique Bold",
        ps_name="DejaVuSerifObliqueBold",
    )
